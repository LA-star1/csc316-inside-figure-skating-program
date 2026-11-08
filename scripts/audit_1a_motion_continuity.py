"""Audit the known calf and skate direction transitions in an open Blender scene."""

import json
import math
from pathlib import Path

import bpy
from mathutils import Vector


ASSET = Path(__file__).resolve().parents[1] / "static" / "movement" / "axel-1a-prototype"
SCENE = bpy.context.scene
REFERENCE = Vector((0.0, -0.11, -0.09)).normalized()


def angle_degrees(first, second):
    return math.degrees(math.acos(max(-1.0, min(1.0, first.normalized().dot(second.normalized())))))


def local_axis_track(obj, axis, frames):
    values = []
    for frame in frames:
        SCENE.frame_set(frame)
        bpy.context.view_layer.update()
        values.append((obj.rotation_quaternion @ axis).normalized())
    return values


def main():
    left_calf = bpy.data.objects.get("Human · left leg volume 4")
    right_calf = bpy.data.objects.get("Human · right leg volume 4")
    right_skate = bpy.data.objects.get("Right skate · exact website fit v64")
    left_blade = bpy.data.objects.get("Left skate · website blade v64")
    right_blade = bpy.data.objects.get("Right skate · website blade v64")
    required = (left_calf, right_calf, right_skate, left_blade, right_blade)
    if not all(required):
        raise RuntimeError("Required v67/v68 leg and skate objects are missing")

    frames = list(range(SCENE.frame_start, SCENE.frame_end + 1))
    left_axes = local_axis_track(left_calf, Vector((0.0, 0.0, 1.0)), frames)
    right_axes = local_axis_track(right_calf, Vector((0.0, 0.0, 1.0)), frames)
    right_foot_axes = local_axis_track(right_skate, REFERENCE, frames)
    deltas = {
        "left_calf_50_51_deg": angle_degrees(left_axes[49], left_axes[50]),
        "right_calf_50_51_deg": angle_degrees(right_axes[49], right_axes[50]),
        "right_skate_86_87_deg": angle_degrees(right_foot_axes[85], right_foot_axes[86]),
        "left_calf_max_47_55_deg": max(angle_degrees(left_axes[i - 1], left_axes[i]) for i in range(47, 55)),
        "right_calf_max_47_55_deg": max(angle_degrees(right_axes[i - 1], right_axes[i]) for i in range(47, 55)),
    }

    blade_min_z = {"left": float("inf"), "right": float("inf")}
    for frame in frames:
        SCENE.frame_set(frame)
        bpy.context.view_layer.update()
        depsgraph = bpy.context.evaluated_depsgraph_get()
        for side, blade in (("left", left_blade), ("right", right_blade)):
            evaluated = blade.evaluated_get(depsgraph)
            world = evaluated.matrix_world
            blade_min_z[side] = min(
                blade_min_z[side],
                min((world @ vertex.co).z for vertex in evaluated.data.vertices),
            )

    report = {
        "blend": bpy.data.filepath,
        "scene": SCENE.name,
        "frames": [SCENE.frame_start, SCENE.frame_end],
        "direction_jumps_deg": {key: round(value, 4) for key, value in deltas.items()},
        "blade_min_z_m_integer_frames": {key: round(value, 5) for key, value in blade_min_z.items()},
        "criteria": {
            "left_calf_50_51_deg_max": 10.0,
            "right_skate_86_87_deg_max": 22.0,
            "calf_max_47_55_deg_max": 16.0,
            "blade_min_z_m_min": 0.0,
        },
    }
    print("MOTION_CONTINUITY_AUDIT " + json.dumps(report, ensure_ascii=False))

    if deltas["left_calf_50_51_deg"] > 10.0:
        raise RuntimeError("Left calf 50→51 direction jump exceeds 10 degrees")
    if deltas["right_skate_86_87_deg"] > 22.0:
        raise RuntimeError("Right skate 86→87 direction jump exceeds 22 degrees")
    if max(deltas["left_calf_max_47_55_deg"], deltas["right_calf_max_47_55_deg"]) > 16.0:
        raise RuntimeError("A calf has a >16-degree adjacent direction jump near frame 50")
    if min(blade_min_z.values()) < -1e-5:
        raise RuntimeError("A skate blade crosses below ice z=0 at an integer frame")


main()
