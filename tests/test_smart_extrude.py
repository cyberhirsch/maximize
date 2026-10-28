# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Smart Extrude: out is a plain extrude, in cuts a pocket or a hole, into other geometry merges.

moritz --factory-startup -b --python tests/test_smart_extrude.py
"""

import os
import sys

import bmesh
import bpy
from mathutils import Vector

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import addon_utils  # noqa: E402

addon_utils.enable("maximize", default_set=True)

failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)
        print("FAIL", msg)


def cube(cuts=0):
    if bpy.context.object is not None and bpy.context.object.mode == 'EDIT':
        bpy.ops.object.mode_set(mode='OBJECT')
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob)
    bpy.ops.mesh.primitive_cube_add(size=2.0)
    bpy.ops.object.mode_set(mode='EDIT')
    if cuts:
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.subdivide(number_cuts=cuts)
    bpy.ops.mesh.select_mode(type='FACE')
    bpy.ops.mesh.select_all(action='DESELECT')


def select_face(center):
    bm = bmesh.from_edit_mesh(bpy.context.object.data)
    face = min(bm.faces, key=lambda f: (f.calc_center_median() - Vector(center)).length)
    face.select_set(True)
    bmesh.update_edit_mesh(bpy.context.object.data)


def stats():
    bm = bmesh.from_edit_mesh(bpy.context.object.data)
    zs = [v.co.z for v in bm.verts]
    return {"faces": len(bm.faces), "open": sum(1 for e in bm.edges if not e.is_manifold),
            "volume": bm.calc_volume(signed=True), "zmax": max(zs), "zmin": min(zs),
            "ngons": sum(1 for f in bm.faces if len(f.verts) > 4),
            "selected": sum(1 for f in bm.faces if f.select)}


def run(distance):
    result = bpy.ops.maximize.smart_extrude(distance=distance)
    return result, stats()


# Out into free space: a plain extrude.
cube()
select_face((0, 0, 1))
result, s = run(0.5)
check(s["faces"] == 10 and abs(s["zmax"] - 1.5) < 1e-5 and s["open"] == 0, "out: plain extrude, got {}".format(s))
check(abs(s["volume"] - 10.0) < 1e-4, "out: volume 10, got {}".format(s["volume"]))
check(s["selected"] == 1, "out: the cap stays selected, got {}".format(s))

# A whole side pushed in: the box gets shorter.
cube()
select_face((0, 0, 1))
result, s = run(-0.5)
check(s["open"] == 0 and abs(s["zmax"] - 0.5) < 1e-4 and abs(s["volume"] - 6.0) < 1e-3,
      "in, whole side: box 1.5 high, got {}".format(s))

# A pocket: the middle of a 3 x 3 side pushed in.
cube(cuts=2)
select_face((0, 0, 1))
result, s = run(-0.5)
pocket = (2.0 / 3.0) ** 2 * 0.5
check(s["open"] == 0 and abs(s["volume"] - (8.0 - pocket)) < 1e-3, "pocket: volume {}, got {}".format(8.0 - pocket, s))
check(s["selected"] >= 1, "pocket: its bottom stays selected, got {}".format(s))

# A notch: a corner cell pushed in (two edges along the box's sides, two inside).
cube(cuts=2)
select_face((2.0 / 3.0, 2.0 / 3.0, 1))
result, s = run(-0.5)
check(s["open"] == 0 and abs(s["volume"] - (8.0 - pocket)) < 1e-3, "notch: volume {}, got {}".format(8.0 - pocket, s))

# A hole: pushed through to the other side.
cube(cuts=2)
select_face((0, 0, 1))
result, s = run(-2.5)
hole = (2.0 / 3.0) ** 2 * 2.0
check(s["open"] == 0 and abs(s["volume"] - (8.0 - hole)) < 1e-3, "hole: volume {}, got {}".format(8.0 - hole, s))

# Merge: a side extruded out into a second part of the same mesh.
cube()
bpy.ops.mesh.primitive_cube_add(size=2.0, location=(0, 0, 3.0))
bpy.ops.mesh.select_all(action='DESELECT')
select_face((0, 0, 1))
result, s = run(1.5)
# Two boxes of 8, joined by a 2 x 2 x 1 bridge (the rest of the extrusion is inside the top box).
check(s["open"] == 0 and abs(s["volume"] - 20.0) < 1e-3, "merge: volume 20, got {}".format(s))

# Out with nothing in the way leaves quads: no boolean on a plain extrude.
cube(cuts=2)
select_face((0, 0, 1))
result, s = run(0.3)
check(s["ngons"] == 0, "plain extrude keeps quads, got {}".format(s))

# Shift+drag with the Move tool: the Max keymap starts Smart Extrude; other tools keep Shift+drag.
bpy.ops.preferences.keyconfig_activate(filepath=bpy.utils.preset_find("Max", "keyconfig"))
kc = bpy.context.window_manager.keyconfigs.active
check(any(it.idname == "maximize.smart_extrude_drag" and it.type == 'LEFTMOUSE' and it.value == 'CLICK_DRAG'
          and it.shift and not it.ctrl for it in kc.keymaps["Mesh"].keymap_items), "Shift+drag key in Mesh")
cube()
select_face((0, 0, 1))
area = next(a for a in bpy.context.screen.areas if a.type == 'VIEW_3D') if bpy.context.screen else None
if area is not None:
    region = next(r for r in area.regions if r.type == 'WINDOW')
    with bpy.context.temp_override(area=area, region=region):
        for tool, expected in (("builtin.select_box", False), ("builtin.move", True)):
            bpy.ops.wm.tool_set_by_id(name=tool)
            got = bpy.ops.maximize.smart_extrude_drag.poll()
            check(got == expected, "Shift+drag with {}: {}, got {}".format(tool, expected, got))

bpy.ops.object.mode_set(mode='OBJECT')
print("FAILURES", len(failures))
if failures:
    sys.exit(1)
