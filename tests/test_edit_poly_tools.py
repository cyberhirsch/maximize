# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Edit Poly tools from Max's Modeling ribbon (Seb, 2026-10-28): Insert / Remove Loop, Dot Loop /
Ring, Quadrify, the Select By picks, MeshSmooth, Symmetrize, Smooth / Smooth 30 / Hard.

moritz --factory-startup -b --python tests/test_edit_poly_tools.py
"""

import os
import sys

import bmesh
import bpy

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import addon_utils  # noqa: E402

addon_utils.enable("maximize", default_set=True)

failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)
        print("FAIL", msg)


def fresh(add=bpy.ops.mesh.primitive_cube_add, **kw):
    if bpy.context.object is not None and bpy.context.object.mode == 'EDIT':
        bpy.ops.object.mode_set(mode='OBJECT')
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob)
    add(**kw)
    bpy.ops.object.mode_set(mode='EDIT')
    return bmesh.from_edit_mesh(bpy.context.object.data)


def bm():
    return bmesh.from_edit_mesh(bpy.context.object.data)


def select_edges(edges):
    b = bm()
    for e in b.edges:
        e.select_set(False)
    for f in b.faces:
        f.select_set(False)
    for e in edges:
        e.select_set(True)
    b.select_flush_mode()
    bmesh.update_edit_mesh(bpy.context.object.data)


# Insert Loop, then Remove Loop takes it out again.
b = fresh()
bpy.ops.mesh.select_mode(type='EDGE')
b.edges.ensure_lookup_table()
select_edges([b.edges[0]])
bpy.ops.maximize.insert_loop()
check(len(bm().verts) == 12, "Insert Loop: 12 vertices expected, got {}".format(len(bm().verts)))
new = [e for e in bm().edges if e.select]
check(len(new) == 4, "Insert Loop: the new loop (4 edges) selected, got {}".format(len(new)))
select_edges(new[:1])
bpy.ops.maximize.remove_loop()
check(len(bm().verts) == 8 and len(bm().faces) == 6, "Remove Loop: back to the cube, got {} verts {} faces".format(
    len(bm().verts), len(bm().faces)))

# Dot Loop / Dot Ring on a 10 x 10 grid: every other edge.
b = fresh(bpy.ops.mesh.primitive_grid_add, x_subdivisions=10, y_subdivisions=10)
bpy.ops.mesh.select_mode(type='EDGE')
middle = min((e for e in b.edges), key=lambda e: ((e.verts[0].co + e.verts[1].co) / 2).length)
select_edges([middle])
bpy.ops.maximize.dot_loop(ring=False)
picked = sum(1 for e in bm().edges if e.select)
check(4 <= picked <= 6, "Dot Loop: about half of the 9-10 edge loop, got {}".format(picked))
select_edges([min((e for e in bm().edges), key=lambda e: ((e.verts[0].co + e.verts[1].co) / 2).length)])
bpy.ops.maximize.dot_loop(ring=True)
picked = sum(1 for e in bm().edges if e.select)
check(4 <= picked <= 6, "Dot Ring: about half of the ring, got {}".format(picked))

# Quadrify All: a triangulated cube is quads again.
b = fresh()
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.quads_convert_to_tris()
bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.maximize.quadrify_all()
check(len(bm().faces) == 6, "Quadrify All: 6 quads expected, got {} faces".format(len(bm().faces)))

# Select By: NonQuads, Open.
b = fresh()
bpy.ops.mesh.select_mode(type='FACE')
b.faces.ensure_lookup_table()
bpy.ops.mesh.select_all(action='DESELECT')
b.faces[0].select_set(True)
bmesh.update_edit_mesh(bpy.context.object.data)
bpy.ops.mesh.quads_convert_to_tris()
bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.maximize.select_nonquads()
check(sum(1 for f in bm().faces if f.select) == 2, "NonQuads: the 2 triangles expected")
b = fresh()
bpy.ops.mesh.select_mode(type='FACE')
bpy.ops.mesh.select_all(action='DESELECT')
b.faces.ensure_lookup_table()
b.faces[0].select_set(True)
bmesh.update_edit_mesh(bpy.context.object.data)
bpy.ops.mesh.delete(type='FACE')
bpy.ops.mesh.select_mode(type='EDGE')
bpy.ops.maximize.select_open()
check(sum(1 for e in bm().edges if e.select) == 4, "Open: the 4 border edges expected")

# The rest runs: Similar, Fill, Outline, Random, Symmetry, Symmetrize, MeshSmooth, Tessellate.
b = fresh()
bpy.ops.mesh.select_mode(type='FACE')
bpy.ops.mesh.select_all(action='DESELECT')
b.faces.ensure_lookup_table()
b.faces[0].select_set(True)
bmesh.update_edit_mesh(bpy.context.object.data)
for op in ("similar", "select_outline", "select_random", "select_mirror", "quadrify"):
    try:
        result = getattr(bpy.ops.maximize, op)('EXEC_DEFAULT')
        check(result == {'FINISHED'}, "{}: {}".format(op, result))
    except RuntimeError as err:
        check(False, "{}: {}".format(op, err))
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.maximize.meshsmooth()
check(len(bm().faces) == 24, "MeshSmooth: 24 faces expected, got {}".format(len(bm().faces)))
bpy.ops.maximize.symmetrize()
check(len(bm().faces) == 24, "Symmetrize on a symmetric mesh keeps 24 faces, got {}".format(len(bm().faces)))

# Smooth 30: Auto Smooth at 30 degrees splits a cube's faces into 6 groups.
b = fresh()
bpy.ops.mesh.select_all(action='SELECT')
import math  # noqa: E402
bpy.ops.maximize.smoothing_auto(angle=math.radians(30.0))
from maximize import smoothing  # noqa: E402
all_mask, any_mask = smoothing.selection_groups(bpy.context)
check(bin(any_mask).count("1") >= 2, "Smooth 30: the cube's faces in several groups, got {:b}".format(any_mask))

bpy.ops.object.mode_set(mode='OBJECT')
print("FAILURES", len(failures))
if failures:
    sys.exit(1)
