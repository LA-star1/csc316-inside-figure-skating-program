"""Derive v68 with smoothed calf and ankle-to-toe direction tracks."""
import json
import math
from pathlib import Path

import bpy
import numpy as np
from mathutils import Matrix, Quaternion, Vector


ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "static" / "movement" / "axel-1a-prototype"
DATA_PATH = ASSET / "joint-reference.json"
SOURCE_NAME = "single-axel-1a-human-rink-v67.blend"
OUT = ASSET / "single-axel-1a-human-rink-v68.blend"
WEB_OUT = ASSET / "single-axel-1a-human-rink-v68-web.glb"
BODY_HEIGHT = 1.72
BODY_FIT = 0.86
SITE_REFERENCE_ANCHOR = Vector((0.0, 0.045, 0.035)) * 1.8
ICE_TOP_Z = 0.0
TARGET_CLEARANCE = 0.005


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_poses(raw_frames, count, display_scale):
    poses = []
    previous_forward = None
    for raw in raw_frames[:count]:
        points = [Vector(point) for point in raw]
        up = (points[12] - points[0]).normalized()
        lateral = (points[17] - points[16]).normalized()
        forward = lateral.cross(up).normalized()
        if previous_forward is not None and forward.dot(previous_forward) < 0.0:
            lateral.negate()
            forward.negate()
        previous_forward = forward.copy()
        local = [Vector(((point - points[0]).dot(lateral),
                         (point - points[0]).dot(up),
                         (point - points[0]).dot(forward)))
                 for point in points]
        poses.append([Vector((point.x * display_scale * BODY_FIT,
                              -point.z * display_scale * BODY_FIT,
                              point.y * display_scale * BODY_FIT))
                      for point in local])
    return poses


def smooth_directions(vectors, weights):
    radius = len(weights) // 2
    smoothed = []
    for index in range(len(vectors)):
        total = Vector((0.0, 0.0, 0.0))
        weight_sum = 0.0
        for offset, weight in zip(range(-radius, radius + 1), weights):
            sample = min(len(vectors) - 1, max(0, index + offset))
            total += vectors[sample] * weight
            weight_sum += weight
        smoothed.append((total / weight_sum).normalized())
    return smoothed


def foot_direction_track(target_poses, foot_pair):
    raw = [(points[foot_pair[1]] - points[foot_pair[0]]).normalized()
           for points in target_poses]
    return smooth_directions(raw, (1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1))


def skate_quaternion_track(target_poses, foot_pair, directions):
    reference = Vector((0.0, -0.11, -0.09)).normalized()
    reference_up = Vector((0.0, 0.0, 1.0))
    reference_up -= reference * reference_up.dot(reference)
    reference_up.normalize()
    reference_side = reference_up.cross(reference).normalized()
    quaternions = []
    previous = None
    for direction in directions:
        shoe_up = Vector((0.0, 0.0, 1.0))
        shoe_up -= direction * shoe_up.dot(direction)
        if previous is not None:
            old_direction = previous @ reference
            transport = old_direction.rotation_difference(direction)
            carried = transport @ (previous @ reference_up)
            reliability = min(1.0, shoe_up.length_squared / 0.25)
            if shoe_up.length_squared > 1e-8:
                shoe_up.normalize()
                roll = math.atan2(direction.dot(carried.cross(shoe_up)), carried.dot(shoe_up))
                correction = max(-math.radians(4.0), min(math.radians(4.0),
                                                         roll * 0.35 * reliability))
                carried.rotate(Quaternion(direction, correction))
            shoe_up = carried - direction * carried.dot(direction)
        elif shoe_up.length_squared < 1e-8:
            shoe_up = Vector((1.0, 0.0, 0.0)) - direction * direction.x
        shoe_up.normalize()
        side = shoe_up.cross(direction).normalized()
        shoe_up = direction.cross(side).normalized()
        desired_basis = Matrix((side, shoe_up, direction)).transposed()
        reference_basis = Matrix((reference_side, reference_up, reference)).transposed()
        previous = (desired_basis @ reference_basis.inverted()).to_quaternion()
        quaternions.append(previous.copy())

    filtered = []
    for index, current in enumerate(quaternions):
        accum = [0.0, 0.0, 0.0, 0.0]
        total = 0.0
        for neighbour in range(max(0, index - 2), min(len(quaternions), index + 3)):
            candidate = quaternions[neighbour]
            weight = 3.0 - abs(neighbour - index)
            sign = -1.0 if current.dot(candidate) < 0.0 else 1.0
            for axis in range(4):
                accum[axis] += candidate[axis] * weight * sign
            total += weight
        filtered.append(Quaternion(tuple(value / total for value in accum)).normalized())

    # Restore exact foot-axis alignment after symmetric roll smoothing.
    aligned = []
    for rotation, direction in zip(filtered, directions):
        fitted_direction = rotation @ reference
        aligned.append(fitted_direction.rotation_difference(direction) @ rotation)
    return aligned, directions


def smooth_calf_tracks(scene, poses, frame_numbers):
    report = {}
    for side, pair in (("left", (4, 7)), ("right", (5, 8))):
        obj = bpy.data.objects.get(f"Human · {side} leg volume 4")
        require(obj is not None, f"Missing {side} calf volume")
        raw_vectors = [points[pair[1]] - points[pair[0]] for points in poses]
        directions = smooth_directions(raw_vectors, (1, 4, 6, 4, 1))
        before = angle_between(raw_vectors[49], raw_vectors[50])
        for frame, direction in zip(frame_numbers, directions):
            scene.frame_set(frame)
            obj.rotation_mode = "QUATERNION"
            obj.rotation_quaternion = Vector((0.0, 0.0, 1.0)).rotation_difference(direction)
            obj.keyframe_insert(data_path="rotation_quaternion", frame=frame,
                                group="Smoothed 22-joint calf directions v68")
        for axis in range(4):
            set_linear(obj, "rotation_quaternion", axis)
        report[side] = {"frame_50_51_before_deg": round(before, 4),
                        "frame_50_51_after_deg": round(angle_between(directions[49], directions[50]), 4)}
    return report


def angle_between(first, second):
    return math.degrees(math.acos(max(-1.0, min(1.0, first.normalized().dot(second.normalized())))))


def set_scene_frame(scene, frame):
    base = int(frame)
    scene.frame_set(base, subframe=float(frame - base))


def action_curve(obj, path, axis):
    animation = obj.animation_data
    if not animation or not animation.action or not animation.action_slot:
        return None
    slot_id = animation.action_slot.identifier
    for layer in animation.action.layers:
        for strip in layer.strips:
            if strip.type == "KEYFRAME":
                for bag in strip.channelbags:
                    if bag.slot and bag.slot.identifier == slot_id:
                        for curve in bag.fcurves:
                            if curve.data_path == path and curve.array_index == axis:
                                return curve
    return None


def set_linear(obj, path, axis):
    curve = action_curve(obj, path, axis)
    require(curve is not None, f"Missing animation curve {obj.name} {path}[{axis}]")
    for point in curve.keyframe_points:
        point.interpolation = "LINEAR"


def main():
    require(Path(bpy.data.filepath).name == SOURCE_NAME,
            f"Expected {SOURCE_NAME}, got {bpy.data.filepath}")
    require(not OUT.exists() and not WEB_OUT.exists(), "Refusing to overwrite existing v68 outputs")
    scene = bpy.context.scene
    default_scene = bpy.data.scenes.get("Scene")
    require(default_scene is not None, "Original default Scene is missing")
    default_names = sorted(obj.name for obj in default_scene.objects)
    require(default_names == ["Camera", "Cube", "Light"],
            f"Original default Scene changed: {default_names}")

    joint_data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    raw_frames = joint_data["frames"]
    count = scene.frame_end - scene.frame_start + 1
    heights = [max(p[1] for p in frame) - min(p[1] for p in frame)
               for frame in raw_frames]
    display_scale = BODY_HEIGHT / max(heights)
    poses = canonical_poses(raw_frames, count, display_scale)
    foot_directions = {
        "Left": foot_direction_track(poses, (7, 10)),
        "Right": foot_direction_track(poses, (8, 11)),
    }
    tracks = {
        side: skate_quaternion_track(poses, pair, foot_directions[side])[0]
        for side, pair in (("Left", (7, 10)), ("Right", (8, 11)))
    }
    roots = {}
    anchors = {}
    ankles = {}
    for side in ("Left", "Right"):
        roots[side] = bpy.data.objects.get(f"{side} skate · exact website fit v64")
        anchors[side] = bpy.data.objects.get(f"{side} skate · fitted ankle anchor v4")
        ankles[side] = bpy.data.objects.get(f"Human · {side.lower()} ankle joint")
        require(all((roots[side], anchors[side], ankles[side])),
                f"Missing {side} skate anchor/root/ankle")

    root_name = "Skater root · simulated travel and 1.5-turn yaw v8"
    skater_root = bpy.data.objects.get(root_name)
    require(skater_root is not None, "Missing animated skater root")
    alignment_dots = {"Left": [], "Right": []}
    frame_numbers = list(range(scene.frame_start, scene.frame_end + 1))
    calf_smoothing = smooth_calf_tracks(scene, poses, frame_numbers)
    for side in ("Left", "Right"):
        root = roots[side]
        root.rotation_mode = "QUATERNION"
        root.animation_data_clear()

    for frame, track_index in zip(frame_numbers, range(count)):
        set_scene_frame(scene, frame)
        bpy.context.view_layer.update()
        for side in ("Left", "Right"):
            root, anchor, ankle = roots[side], anchors[side], ankles[side]
            parent_world = anchor.matrix_world.copy()
            parent_q = parent_world.to_quaternion()
            rig_q = skater_root.matrix_world.to_quaternion()
            target_world_q = (rig_q @ tracks[side][track_index]).normalized()
            ankle_world = ankle.matrix_world.translation
            desired_world = ankle_world - target_world_q @ SITE_REFERENCE_ANCHOR
            root.location = parent_world.inverted() @ desired_world
            root.rotation_quaternion = parent_q.inverted() @ target_world_q
            root.keyframe_insert(data_path="location", frame=frame,
                                 group="Website calibrated ankle fit v66")
            root.keyframe_insert(data_path="rotation_quaternion", frame=frame,
                                 group="Website calibrated ankle fit v66")
            direction = foot_directions[side][track_index]
            alignment_dots[side].append((tracks[side][track_index] @ Vector((0.0, -0.11, -0.09)).normalized()).dot(direction))

    for root in roots.values():
        for axis in range(3):
            set_linear(root, "location", axis)
        for axis in range(4):
            set_linear(root, "rotation_quaternion", axis)

    blade_vertices = {}
    for side in ("Left", "Right"):
        blade = bpy.data.objects.get(f"{side} skate · website blade v64")
        require(blade is not None and blade.type == "MESH", f"Missing {side} source blade")
        vertices = np.array([tuple(vertex.co) for vertex in blade.data.vertices], dtype=np.float64)
        blade_vertices[side] = (blade, np.column_stack((vertices, np.ones(len(vertices)))))

    def frame_min_z():
        bpy.context.view_layer.update()
        depsgraph = bpy.context.evaluated_depsgraph_get()
        return {side: float((vertices @ np.asarray(obj.evaluated_get(depsgraph).matrix_world,
                                                  dtype=np.float64).T)[:, 2].min())
                for side, (obj, vertices) in blade_vertices.items()}

    raw_minima = []
    for frame in frame_numbers:
        set_scene_frame(scene, frame)
        raw_minima.append(min(frame_min_z().values()))
    needed = [max(0.0, ICE_TOP_Z + TARGET_CLEARANCE - value) for value in raw_minima]
    smoothed = []
    for index, value in enumerate(needed):
        weights = (1, 2, 3, 2, 1)
        weighted = total = 0.0
        for offset, weight in zip(range(-2, 3), weights):
            sample = index + offset
            if 0 <= sample < len(needed):
                weighted += needed[sample] * weight
                total += weight
        smoothed.append(max(value, weighted / total))

    for side, root in roots.items():
        for frame, lift in zip(frame_numbers, smoothed):
            set_scene_frame(scene, frame)
            # Parent and rig rotations are around world Z, so local Z is vertical.
            root.location.z += lift
            root.keyframe_insert(data_path="location", index=2, frame=frame,
                                 group="Illustrative blade clearance correction v66")
        set_linear(root, "location", 2)

    sample_frames = [scene.frame_start + step * 0.25
                     for step in range((scene.frame_end - scene.frame_start) * 4 + 1)]
    minima = []
    for frame in sample_frames:
        set_scene_frame(scene, frame)
        minima.append(min(frame_min_z().values()))
    safety_raise = max(0.0, ICE_TOP_Z + TARGET_CLEARANCE - min(minima))
    if safety_raise > 1e-5:
        for root in roots.values():
            for frame in frame_numbers:
                set_scene_frame(scene, frame)
                root.location.z += safety_raise
                root.keyframe_insert(data_path="location", index=2, frame=frame,
                                     group="Illustrative blade clearance correction v66")
            set_linear(root, "location", 2)
        minima = []
        for frame in sample_frames:
            set_scene_frame(scene, frame)
            minima.append(min(frame_min_z().values()))

    scene.name = "Single Axel 1A · motion continuity and website skates v68"
    scene["prototype_version"] = "v68"
    scene["motion_smoothing_v68"] = (
        "Centered 5-tap smoothing on both calf axes and centered 11-tap smoothing on both "
        "ankle-to-toe direction tracks; skate long axes are aligned to the filtered foot directions."
    )
    scene["calf_direction_delta_report_v68"] = json.dumps(calf_smoothing, ensure_ascii=False)
    scene["skate_revision"] = (
        "Website SKATE geometry with heel island cleanup inherited from v67. The skate long axes "
        "follow centered-smoothed 22-joint ankle-to-forefoot directions; the body calves use "
        "centered-smoothed directions. Blade clearance is corrected from evaluated geometry; all motion remains simulated."
    )
    scene["skate_asset_source"] = (
        "Ice Skates by IsaacTheMaverick, Sketchfab/Objaverse, CC BY 4.0; exact geometry is "
        "embedded in static/movement/index.html and included in this file."
    )
    scene["motion_status"] = (
        "ILLUSTRATIVE / SIMULATED — generic 22-joint pose retargeting; not athlete capture"
    )
    scene["ground_fit_max_lift_m"] = round(max(smoothed, default=0.0) + safety_raise, 5)
    scene.frame_set(74)
    scene.camera = bpy.data.objects.get("Action side view · horizontal follow composition")
    require(scene.camera is not None, "Missing side camera")
    if bpy.context.window:
        bpy.context.window.scene = scene

    bpy.ops.wm.save_as_mainfile(filepath=str(OUT), check_existing=False)
    bpy.ops.export_scene.gltf(
        filepath=str(WEB_OUT), export_format="GLB", export_animations=True,
        export_cameras=True, export_lights=False, export_yup=True,
        use_selection=False, use_active_scene=True, use_visible=True,
        use_renderable=True, export_animation_mode="SCENE", export_frame_range=True,
        export_frame_step=1, export_optimize_animation_size=False,
    )

    previews = {}
    scene.render.resolution_x = 900
    scene.render.resolution_y = 675
    scene.render.resolution_percentage = 65
    for frame, suffix, camera_name in (
        (39, "side", "Action side view · horizontal follow composition"),
        (50, "side", "Action side view · horizontal follow composition"),
        (51, "side", "Action side view · horizontal follow composition"),
        (74, "side", "Action side view · horizontal follow composition"),
        (86, "side", "Action side view · horizontal follow composition"),
        (87, "side", "Action side view · horizontal follow composition"),
        (93, "side", "Action side view · horizontal follow composition"),
        (74, "front", "Action front view"),
        (74, "skate-inspection", "Skate inspection · close view"),
    ):
        camera = bpy.data.objects.get(camera_name)
        require(camera is not None, f"Missing preview camera: {camera_name}")
        set_scene_frame(scene, frame)
        scene.camera = camera
        preview = ASSET / f"single-axel-1a-human-rink-v68-frame{frame:03d}-{suffix}.png"
        scene.render.filepath = str(preview)
        bpy.ops.render.render(write_still=True)
        previews[f"{suffix}_{frame}"] = str(preview)
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.render.filepath = "//"
    scene.camera = bpy.data.objects.get("Action side view · horizontal follow composition")
    scene.frame_set(74)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT), check_existing=False)

    per_side = {}
    for side, (obj, vertices) in blade_vertices.items():
        samples = []
        for frame in sample_frames:
            set_scene_frame(scene, frame)
            depsgraph = bpy.context.evaluated_depsgraph_get()
            matrix = np.asarray(obj.evaluated_get(depsgraph).matrix_world, dtype=np.float64)
            samples.append(float((vertices @ matrix.T)[:, 2].min()))
        per_side[side] = {
            "min_z_m": round(min(samples), 5),
            "frame": sample_frames[samples.index(min(samples))],
            "samples_below_ice": sum(value < ICE_TOP_Z for value in samples),
            "quarter_frame_samples": len(samples),
            "toe_axis_dot_min": round(min(alignment_dots[side]), 6),
        }
    print("V68_REPORT " + json.dumps({
        "blend": str(OUT), "web_glb": str(WEB_OUT), "frames": [scene.frame_start, scene.frame_end],
        "fps": scene.render.fps, "max_smoothed_root_raise_m": round(max(smoothed, default=0.0), 5),
        "global_safety_raise_m": round(safety_raise, 5), "blade_clearance": per_side,
        "calf_smoothing": calf_smoothing,
        "previews": previews, "default_scene_objects": default_names,
    }, ensure_ascii=False))


main()
