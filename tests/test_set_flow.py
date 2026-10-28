# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Set Flow: the selected edges' vertices go onto the curve of the surface around them.

moritz --factory-startup -b --python tests/test_set_flow.py
"""

import os
import sys

import bmesh
import bpy

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import addon_utils  # noqa: E402

addon_utils.enable("maximize", default_set=True)
failures = []


def check(ok, what):
    print(("ok   " if ok else "FAIL ") + what)
    if not ok:
        failures.append(what)


def sphere_with_flat_equator(scale):
    """A UV sphere whose equator is pulled in to `scale`, with the equator selected."""
    if bpy.context.object and bpy.context.object.mode == 'EDIT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1.0)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='EDGE')
    bm = bmesh.from_edit_mesh(bpy.context.object.data)
    for v in bm.verts:
        v.select = False
    for e in bm.edges:
        e.select = all(abs(v.co.z) < 1e-5 for v in e.verts)
    for v in bm.verts:
        if abs(v.co.z) < 1e-5:
            v.co.xy *= scale
            v.select = True
    bm.select_flush_mode()
    bmesh.update_edit_mesh(bpy.context.object.data)


def equator_radii():
    bm = bmesh.from_edit_mesh(bpy.context.object.data)
    return [v.co.xy.length for v in bm.verts if abs(v.co.z) < 1e-5]


sphere_with_flat_equator(0.8)
check(bpy.ops.maximize.set_flow() == {'FINISHED'}, "runs")
radii = equator_radii()
check(len(radii) == 32 and all(abs(r - 1.0) < 0.01 for r in radii),
      "pulled-in equator goes back onto the sphere: {:.4f}..{:.4f}".format(min(radii), max(radii)))

sphere_with_flat_equator(0.8)
bpy.ops.maximize.set_flow(amount=0.5)
radii = equator_radii()
check(all(abs(r - 0.9) < 0.01 for r in radii), "Amount 0.5 goes half way: {:.4f}".format(radii[0]))

# Auto Loop: one selected edge does the whole ring.
sphere_with_flat_equator(0.8)
bm = bmesh.from_edit_mesh(bpy.context.object.data)
first = next(e for e in bm.edges if e.select)
for e in bm.edges:
    e.select = e is first
for v in bm.verts:
    v.select = v in first.verts
bmesh.update_edit_mesh(bpy.context.object.data)
bpy.ops.maximize.set_flow(auto_loop=True)
radii = equator_radii()
check(all(abs(r - 1.0) < 0.01 for r in radii), "Auto Loop does the whole ring")

# Nothing selected: a warning, nothing moves.
bpy.ops.mesh.select_all(action='DESELECT')
check(bpy.ops.maximize.set_flow() == {'CANCELLED'}, "nothing selected cancels")

bpy.ops.object.mode_set(mode='OBJECT')
print("FAILURES", len(failures))
if failures:
    sys.exit(1)
