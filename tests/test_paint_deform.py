# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Paint Deform: the painting brushes and Shift on a flat grid, seen from the top.

moritz --factory-startup -b --python tests/test_paint_deform.py
"""

import os
import sys

import bmesh
import bpy
from mathutils import Vector

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import addon_utils  # noqa: E402

addon_utils.enable("maximize", default_set=True)
from maximize import paint_deform  # noqa: E402
from maximize.freeform import brush_weights  # noqa: E402

failures = []


def check(ok, what):
    print(("ok   " if ok else "FAIL ") + what)
    if not ok:
        failures.append(what)


for o in list(bpy.data.objects):
    bpy.data.objects.remove(o)
ctx = bpy.context
bpy.ops.mesh.primitive_grid_add(x_subdivisions=10, y_subdivisions=10, size=2.0)
obj = ctx.active_object
check(bpy.ops.maximize.paint_deform.poll(), "Paint Deform available in Object Mode")
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(obj.data)
bm.verts.ensure_lookup_table()
originals = [v.co.copy() for v in bm.verts]
mid = min(bm.verts, key=lambda v: v.co.length).index
down = Vector((0.0, 0.0, -1.0))


def top_view(p):
    return Vector((p.x * 100.0, p.y * 100.0))


def under(radius=40.0):
    return brush_weights(obj, bm, top_view, (bm.verts[mid].co.x * 100.0, bm.verts[mid].co.y * 100.0), radius, down)


def at(index=None):
    return bm.verts[mid if index is None else index].co.copy()


def step(mode, **kw):
    kw.setdefault("world_radius", 0.4)
    return paint_deform.paint_step(obj, bm, under(), mode, 1.0, **kw)


def reset():
    for v, co in zip(bm.verts, originals):
        v.co = co
    bmesh.update_edit_mesh(obj.data)


step('PUSH_PULL', push=0.25)
check(abs(at().z - 0.1) < 1e-4, "Push: the middle up by a quarter of the brush ({:.3f})".format(at().z))
step('PUSH_PULL', push=0.25, invert=True)
check(abs(at().z) < 1e-4, "Pull (Ctrl): back down")

reset()
bm.verts[mid].co.z = 0.2
step('RELAX')
check(at().z < 0.2 - 0.1, "Relax: a spike comes down ({:.3f})".format(at().z))
reset()
bm.verts[mid].co.z = 0.2
step('EXAGGERATE')
check(at().z > 0.3, "Exaggerate: a spike grows ({:.3f})".format(at().z))

reset()
bm.verts[mid].co.z = 0.2
step('FLATTEN')
check(at().z < 0.1, "Flatten: a spike flattens ({:.3f})".format(at().z))

reset()
near = next(e.other_vert(bm.verts[mid]).index for e in bm.verts[mid].link_edges)
before = (at(near) - at()).length
step('PINCH')
check((at(near) - at()).length < before, "Pinch: neighbours drawn in")
reset()
step('PINCH', invert=True)
check((at(near) - at()).length > before, "Spread (Ctrl): neighbours pushed out")

reset()
step('SMUDGE', stroke=Vector((0.1, 0.0, 0.0)))
check(abs(at().x - 0.1) < 1e-4, "Smudge: the middle goes with the stroke")

reset()
step('NOISE', push=0.5)
check(any(abs(v.co.z) > 1e-4 for v in bm.verts), "Noise: bumps")

reset()
step('PUSH_PULL', push=0.25)
step('REVERT', originals=originals)
check(abs(at().z) < 1e-4, "Revert: back to how it was")

reset()
paint_deform.shift(obj, under(), lambda p, w: p + Vector((0.0, 0.0, 0.3)) * w)
check(abs(at().z - 0.3) < 1e-4 and abs(bm.verts[0].co.z) < 1e-6, "Shift: the middle lifts, the corner stays")

bpy.ops.object.mode_set(mode='OBJECT')
print("FAILURES", len(failures))
if failures:
    sys.exit(1)
