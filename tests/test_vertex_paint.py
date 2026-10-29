# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Max's VertexPaint modifier session (Moritz builds): paint on a stand-in, store, cancel, clear.

moritz --factory-startup -b --python tests/test_vertex_paint.py
"""

import os
import sys

import bpy

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import addon_utils  # noqa: E402

addon_utils.enable("maximize", default_set=True)
from maximize import vertex_paint  # noqa: E402

failures = []


def check(ok, what):
    print(("ok   " if ok else "FAIL ") + what)
    if not ok:
        failures.append(what)


def evaluated(obj):
    dg = bpy.context.evaluated_depsgraph_get()
    obj.update_tag()
    dg.update()
    return obj.evaluated_get(dg).data


if not vertex_paint.native():
    print("SKIP: no native VertexPaint modifier in this build")
    print("FAILURES 0")
    sys.exit(0)

bpy.ops.mesh.primitive_cube_add()
cube = bpy.context.active_object
cube.modifiers.new("Bevel", 'BEVEL')
bpy.ops.maximize.vertex_paint_add()
standin = bpy.context.active_object
check(standin != cube and cube.hide_get() and standin.mode == 'VERTEX_PAINT', "session starts")
check(len(standin.data.vertices) == len(evaluated(cube).vertices), "stand-in holds the stack")
attr = standin.data.color_attributes.active_color
check(attr is not None and attr.name == "VertexPaint", "paint layer active")

# A "stroke": color the first half red.
bpy.ops.object.mode_set(mode='OBJECT')
for i, c in enumerate(attr.data):
    c.color = (1.0, 0.0, 0.0, 1.0) if i < len(attr.data) // 2 else (1.0, 1.0, 1.0, 1.0)
bpy.ops.object.mode_set(mode='VERTEX_PAINT')
bpy.ops.maximize.vertex_paint_toggle()
check(bpy.context.active_object == cube and not cube.hide_get(), "session ends on the object")
check("Cube VertexPaint" not in bpy.data.objects, "stand-in removed")
mod = cube.modifiers["VertexPaint"]
check(mod.has_colors, "colors stored")
out = evaluated(cube).color_attributes.get("VertexPaint")
check(out is not None and out.data[0].color[1] < 0.01, "colors in the stack")

# Cancel keeps the old colors.
bpy.ops.maximize.vertex_paint_toggle()
standin = bpy.context.active_object
bpy.ops.object.mode_set(mode='OBJECT')
for c in standin.data.color_attributes.active_color.data:
    c.color = (0.0, 0.0, 1.0, 1.0)
bpy.ops.maximize.vertex_paint_cancel()
out = evaluated(cube).color_attributes.get("VertexPaint")
check(out.data[0].color[0] > 0.99 and out.data[0].color[2] < 0.01, "cancel keeps old colors")

bpy.ops.object.mx_vertex_paint_clear()
check(not mod.has_colors, "clear")

print("FAILURES", len(failures), failures)
