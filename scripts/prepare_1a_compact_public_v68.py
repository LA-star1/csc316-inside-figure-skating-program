"""Create a compact public v68 Blender file while preserving the full local source."""

from pathlib import Path

import bpy


ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "static" / "movement" / "axel-1a-prototype"
OUT = ASSET / "single-axel-1a-human-rink-v68-public.blend"
KEEP_SCENES = {"Scene", "Single Axel 1A · motion continuity and website skates v68"}

if Path(bpy.data.filepath).name != "single-axel-1a-human-rink-v68.blend":
    raise RuntimeError(f"Expected v68 source, got {bpy.data.filepath}")
if OUT.exists():
    raise RuntimeError(f"Refusing to overwrite {OUT}")

scene_names = {scene.name for scene in bpy.data.scenes}
if not KEEP_SCENES.issubset(scene_names):
    raise RuntimeError(f"Missing required scenes: {KEEP_SCENES - scene_names}")
active = bpy.data.scenes["Single Axel 1A · motion continuity and website skates v68"]
default = bpy.data.scenes["Scene"]
if sorted(obj.name for obj in default.objects) != ["Camera", "Cube", "Light"]:
    raise RuntimeError("The original default Scene is not intact")

for scene in list(bpy.data.scenes):
    if scene.name not in KEEP_SCENES:
        bpy.data.scenes.remove(scene, do_unlink=True)

if bpy.context.window:
    bpy.context.window.scene = active

purged = bpy.data.orphans_purge(do_recursive=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT), check_existing=False)
print("V68_PUBLIC_REPORT", {
    "file": str(OUT),
    "scenes": [(scene.name, len(scene.objects)) for scene in bpy.data.scenes],
    "orphan_datablocks_purged": purged,
    "default_scene_objects": sorted(obj.name for obj in default.objects),
    "active_scene_objects": len(active.objects),
    "active_frame": active.frame_current,
})
