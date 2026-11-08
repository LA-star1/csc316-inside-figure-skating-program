"""Derive v69 from v68 with a closer horizontal side camera for skate readability."""

import json
from pathlib import Path

import bpy


ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "static" / "movement" / "axel-1a-prototype"
SOURCE_NAME = "single-axel-1a-human-rink-v68.blend"
OUT = ASSET / "single-axel-1a-human-rink-v69.blend"
WEB_OUT = ASSET / "single-axel-1a-human-rink-v69-web.glb"
SIDE_CAMERA = "Action side view · horizontal follow composition"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    require(Path(bpy.data.filepath).name == SOURCE_NAME,
            f"Expected {SOURCE_NAME}, got {bpy.data.filepath}")
    require(not OUT.exists() and not WEB_OUT.exists(), "Refusing to overwrite v69 outputs")

    default_scene = bpy.data.scenes.get("Scene")
    scene = bpy.data.scenes.get("Single Axel 1A · motion continuity and website skates v68")
    require(default_scene is not None and scene is not None, "v68 source scenes are missing")
    require(sorted(obj.name for obj in default_scene.objects) == ["Camera", "Cube", "Light"],
            "The original default Scene is not intact")
    require((scene.frame_start, scene.frame_end, scene.render.fps) == (1, 160, 12),
            "Unexpected v68 animation range or timing")

    camera = bpy.data.objects.get(SIDE_CAMERA)
    require(camera is not None and camera.type == "CAMERA" and camera.data.type == "PERSP",
            "Expected the perspective horizontal side camera")
    require(scene.objects.get(camera.name) is camera,
            "The horizontal side camera is not in the v68 action scene")
    camera.data.lens = 104.0
    scene.camera = camera
    scene.name = "Single Axel 1A · motion continuity and readable side camera v69"
    scene["prototype_version"] = "v69"
    scene["side_camera_lens_mm_v69"] = 104.0
    scene["camera_revision_v69"] = (
        "The horizontal side view is framed 15.6% closer than v68; the skater, both skates, "
        "and nearby ice remain within the action camera in the checked approach, apex, and landing renders."
    )
    scene.frame_set(74)
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
        (39, "side", SIDE_CAMERA),
        (50, "side", SIDE_CAMERA),
        (51, "side", SIDE_CAMERA),
        (74, "side", SIDE_CAMERA),
        (86, "side", SIDE_CAMERA),
        (87, "side", SIDE_CAMERA),
        (93, "side", SIDE_CAMERA),
        (74, "front", "Action front view"),
        (74, "skate-inspection", "Skate inspection · close view"),
    ):
        active_camera = bpy.data.objects.get(camera_name)
        require(active_camera is not None, f"Missing preview camera: {camera_name}")
        scene.frame_set(frame)
        scene.camera = active_camera
        preview = ASSET / f"single-axel-1a-human-rink-v69-frame{frame:03d}-{suffix}.png"
        scene.render.filepath = str(preview)
        bpy.ops.render.render(write_still=True)
        previews[f"{suffix}_{frame}"] = str(preview)

    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.render.filepath = "//"
    scene.camera = camera
    scene.frame_set(74)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT), check_existing=False)
    print("V69_REPORT " + json.dumps({
        "blend": str(OUT),
        "web_glb": str(WEB_OUT),
        "frame_range": [scene.frame_start, scene.frame_end],
        "fps": scene.render.fps,
        "side_camera_lens_mm": camera.data.lens,
        "default_scene_objects": sorted(obj.name for obj in default_scene.objects),
        "action_scene_objects": len(scene.objects),
        "previews": previews,
    }, ensure_ascii=False))


main()
