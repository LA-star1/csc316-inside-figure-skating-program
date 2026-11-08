"""Derive v67 from v66 by removing the disconnected heel fragment in each website boot."""

import json
from pathlib import Path

import bpy
import bmesh
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "static" / "movement" / "axel-1a-prototype"
OUT = ASSET / "single-axel-1a-human-rink-v67.blend"
WEB_OUT = ASSET / "single-axel-1a-human-rink-v67-web.glb"
ICE_TOP_Z = 0.0


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def face_components(bm):
    unseen = set(bm.faces)
    components = []
    while unseen:
        first = unseen.pop()
        component = [first]
        stack = [first]
        while stack:
            face = stack.pop()
            for edge in face.edges:
                for adjacent in edge.link_faces:
                    if adjacent in unseen:
                        unseen.remove(adjacent)
                        component.append(adjacent)
                        stack.append(adjacent)
        components.append(component)
    return sorted(components, key=len, reverse=True)


def clean_boot(side):
    obj = bpy.data.objects.get(f"{side} skate · website boot v64")
    require(obj is not None and obj.type == "MESH", f"Missing {side} website boot")
    obj.data = obj.data.copy()
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    components = face_components(bm)
    require(len(components) == 2,
            f"Expected two connected boot islands for {side}, found {list(map(len, components))}")
    main, fragment = components
    require(len(main) > 10_000 and 300 <= len(fragment) <= 800,
            f"Unexpected {side} component sizes: {list(map(len, components))}")
    main_edges = {edge for face in main for edge in face.edges}
    fragment_edges = {edge for face in fragment for edge in face.edges}
    require(not any(edge.is_boundary for edge in main_edges),
            f"The {side} main boot shell unexpectedly has an open boundary")
    fragment_boundaries = sum(edge.is_boundary for edge in fragment_edges)
    require(fragment_boundaries > 0, f"The {side} secondary island topology changed")
    bmesh.ops.delete(bm, geom=fragment, context="FACES")
    loose = [vertex for vertex in bm.verts if not vertex.link_faces]
    if loose:
        bmesh.ops.delete(bm, geom=loose, context="VERTS")
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()
    for polygon in obj.data.polygons:
        polygon.use_smooth = True
    return {
        "side": side,
        "removed_faces": len(fragment),
        "fragment_boundary_edges": fragment_boundaries,
        "remaining_vertices": len(obj.data.vertices),
        "remaining_faces": len(obj.data.polygons),
    }


def render(scene, frame, suffix, camera_name):
    camera = bpy.data.objects.get(camera_name)
    require(camera is not None and camera.type == "CAMERA", f"Missing camera {camera_name}")
    scene.frame_set(frame)
    scene.camera = camera
    preview = ASSET / f"single-axel-1a-human-rink-v67-frame{frame:03d}-{suffix}.png"
    scene.render.filepath = str(preview)
    bpy.ops.render.render(write_still=True)
    return str(preview)


def main():
    require(Path(bpy.data.filepath).name == "single-axel-1a-human-rink-v66.blend",
            f"Expected the v66 source file; got {bpy.data.filepath}")
    require(not OUT.exists() and not WEB_OUT.exists(), "Refusing to overwrite a v67 output")
    scene = next((candidate for candidate in bpy.data.scenes if "v66" in candidate.name), None)
    require(scene is not None, "Missing v66 action scene")
    default_scene = bpy.data.scenes.get("Scene")
    require(default_scene is not None, "Original default Scene is missing")
    default_names = sorted(obj.name for obj in default_scene.objects)
    require(default_names == ["Camera", "Cube", "Light"],
            f"Original default Scene changed: {default_names}")

    boot_report = [clean_boot(side) for side in ("Left", "Right")]
    scene.name = "Single Axel 1A · cleaned website boots v67"
    scene["version"] = "v67"
    scene["boot_mesh_cleanup"] = (
        "Merged duplicate triangle vertices; removed the disconnected 573-face heel fragment "
        "from each website boot; recalculated normals and enabled smooth shading."
    )
    scene["motion_status"] = (
        "ILLUSTRATIVE / SIMULATED — generic 22-joint pose retargeting; not athlete capture"
    )
    scene.frame_set(74)
    side_camera = bpy.data.objects.get("Action side view · horizontal follow composition")
    require(side_camera is not None, "Missing horizontal side camera")
    scene.camera = side_camera
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

    scene.render.resolution_x = 900
    scene.render.resolution_y = 675
    scene.render.resolution_percentage = 65
    previews = [
        render(scene, 39, "side", "Action side view · horizontal follow composition"),
        render(scene, 74, "side", "Action side view · horizontal follow composition"),
        render(scene, 93, "side", "Action side view · horizontal follow composition"),
        render(scene, 74, "front", "Action front view"),
        render(scene, 74, "skate-inspection", "Skate inspection · close view"),
    ]

    blade_report = {}
    depsgraph = bpy.context.evaluated_depsgraph_get()
    for side in ("Left", "Right"):
        blade = bpy.data.objects.get(f"{side} skate · website blade v64")
        require(blade is not None and blade.type == "MESH", f"Missing {side} blade")
        vertices = np.array([tuple(vertex.co) for vertex in blade.data.vertices], dtype=np.float64)
        homogeneous = np.column_stack((vertices, np.ones(len(vertices))))
        minima = []
        for frame in range(scene.frame_start, scene.frame_end + 1):
            scene.frame_set(frame)
            depsgraph.update()
            matrix = np.asarray(blade.evaluated_get(depsgraph).matrix_world, dtype=np.float64)
            minima.append(float((homogeneous @ matrix.T)[:, 2].min()))
        blade_report[side] = {
            "integer_frames": len(minima),
            "minimum_blade_z_m": round(min(minima), 5),
            "minimum_frame": minima.index(min(minima)) + scene.frame_start,
            "samples_below_ice": sum(value < ICE_TOP_Z for value in minima),
        }

    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.camera = side_camera
    scene.frame_set(74)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT), check_existing=False)
    print("V67_REPORT " + json.dumps({
        "blend": str(OUT), "web_glb": str(WEB_OUT), "boots": boot_report,
        "blade_clearance_integer_frames": blade_report,
        "previews": previews, "default_scene_objects": default_names,
        "motion_status": scene["motion_status"],
    }, ensure_ascii=False))


main()
