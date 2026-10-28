# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""The rest of Edit Poly: step loops, Random Loops, Build End, Distribute and the loop shapes,
GeoPoly, Generate Topology, To Grid, Previous / Next Modifier, and the Selection tab.

moritz --factory-startup -b --python tests/test_poly_ribbon.py
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import addon_utils  # noqa: E402

addon_utils.enable("maximize", default_set=True)
failures = []


def check(ok, what):
    print(("ok   " if ok else "FAIL ") + what)
    if not ok:
        failures.append(what)


def fresh(add, mode='EDGE', **kw):
    if bpy.context.object and bpy.context.object.mode == 'EDIT':
        bpy.ops.object.mode_set(mode='OBJECT')
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o)
    add(**kw)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type=mode)
    bpy.ops.mesh.select_all(action='DESELECT')
    return bm()


def bm():
    return bmesh.from_edit_mesh(bpy.context.object.data)


def flush(b):
    b.select_flush_mode()
    bmesh.update_edit_mesh(bpy.context.object.data)


def grid(n=6):
    return fresh(bpy.ops.mesh.primitive_grid_add, x_subdivisions=n, y_subdivisions=n, size=2.0)


def select_edges(b, test):
    for e in b.edges:
        if test(e):
            e.select_set(True)
    flush(b)


def column_edge(e, x, y_lo=-2.0, y_hi=2.0):
    a, c = e.verts
    return abs(a.co.x - x) < 1e-3 and abs(c.co.x - x) < 1e-3 and min(a.co.y, c.co.y) >= y_lo - 1e-4 and \
        max(a.co.y, c.co.y) <= y_hi + 1e-4


# Step loop: one edge in the middle of a column grows to three, shrinks back to one.
b = grid()
select_edges(b, lambda e: column_edge(e, 0.0, -0.34, 0.01))
check(sum(e.select for e in b.edges) == 1, "one middle edge")
bpy.ops.maximize.step_loop(action='GROW')
check(sum(e.select for e in bm().edges) == 3, "Grow Loop: three edges")
bpy.ops.maximize.step_loop(action='SHRINK')
check(sum(e.select for e in bm().edges) == 1, "Shrink Loop: one edge again")
bpy.ops.maximize.step_loop(action='GROW', ring=True)
check(sum(e.select for e in bm().edges) == 3, "Grow Ring: three edges")

# Random Loops: whole loops picked from the ring.
bpy.ops.maximize.random_loops(percent=50.0, seed=1)
b = bm()
xs = {round(e.verts[0].co.x, 3) for e in b.edges if e.select and abs(e.verts[0].co.x - e.verts[1].co.x) < 1e-4}
check(0 < sum(e.select for e in b.edges) and all(sum(1 for e in b.edges if e.select and column_edge(e, x)) == 6
                                                   for x in xs), "Random Loops: whole columns, {} {}".format(
    sorted(xs), [sum(1 for e in b.edges if e.select and column_edge(e, x)) for x in sorted(xs)]))

# Distribute: a column bunched up spreads out evenly.
b = grid()
for v in b.verts:
    if abs(v.co.x) < 1e-4:
        v.co.y = math.copysign(abs(v.co.y) ** 2, v.co.y)
select_edges(b, lambda e: column_edge(e, 0.0))
bpy.ops.maximize.distribute()
ys = sorted(v.co.y for v in bm().verts if abs(v.co.x) < 1e-4)
gaps = [b2 - a2 for a2, b2 in zip(ys, ys[1:])]
check(max(gaps) - min(gaps) < 1e-4, "Distribute: even gaps {}".format([round(g, 3) for g in gaps]))

# Straighten: a bent column becomes straight.
b = grid()
for v in b.verts:
    if abs(v.co.x) < 1e-4 and abs(v.co.y) < 0.9:
        v.co.x = 0.1
select_edges(b, lambda e: all(abs(v.co.x) < 0.11 and abs(v.co.x - 0.0) < 0.11 for v in e.verts) and
             abs(e.verts[0].co.y - e.verts[1].co.y) > 1e-4 and
             all(abs(v.co.x) < 1e-4 or abs(v.co.x - 0.1) < 1e-4 for v in e.verts))
bpy.ops.maximize.loop_straighten()
check(all(abs(v.co.x) < 1e-4 for v in bm().verts if abs(v.co.x) < 0.11 and abs(v.co.x - 0.0) < 0.11 and
          (abs(v.co.x) < 1e-4 or abs(v.co.x - 0.1) < 1e-4) and abs(v.co.y) <= 1.0),
      "Straighten: the column is straight again")

# Circle and Curve on a closed loop: the cylinder's top ring squashed becomes round again.
fresh(bpy.ops.mesh.primitive_cylinder_add, vertices=16)
b = bm()
for v in b.verts:
    if v.co.z > 0.5:
        v.co.x *= 0.5
select_edges(b, lambda e: all(v.co.z > 0.5 for v in e.verts) and e.is_boundary is False and
             len(e.link_faces) == 2 and all(len(f.verts) == 4 or len(f.verts) == 16 for f in e.link_faces)
             and any(len(f.verts) == 16 for f in e.link_faces))
bpy.ops.maximize.loop_circle()
radii = [Vector((v.co.x, v.co.y)).length for v in bm().verts if v.co.z > 0.5]
check(max(radii) - min(radii) < 1e-4, "Circle: round ({:.3f}..{:.3f})".format(min(radii), max(radii)))

# Curve: an open chain with a kink smooths out, ends kept.
b = grid()
for v in b.verts:
    if abs(v.co.x) < 1e-4 and abs(v.co.y) < 1e-4:
        v.co.x = 0.3
select_edges(b, lambda e: all(abs(v.co.x) < 1e-4 or (abs(v.co.x - 0.3) < 1e-4 and abs(v.co.y) < 1e-4)
                              for v in e.verts) and abs(e.verts[0].co.y - e.verts[1].co.y) > 1e-4)
ends = sorted((v.co.y, v.co.x) for v in bm().verts if v.select)
bpy.ops.maximize.loop_curve()
after = sorted((v.co.y, v.co.x) for v in bm().verts if v.select)
check(abs(after[0][1] - ends[0][1]) < 1e-5 and abs(after[-1][1] - ends[-1][1]) < 1e-5 and
      max(x for _y, x in after) < 0.3 - 0.05, "Curve: kink smoothed, ends kept ({:.3f})".format(max(x for _y, x in after)))

# Center: a column moved off-center goes back between its neighbours.
b = grid()
for v in b.verts:
    if abs(v.co.x) < 1e-4 and abs(v.co.y) < 0.9:
        v.co.x = 0.2
select_edges(b, lambda e: all(abs(v.co.x - 0.2) < 1e-4 for v in e.verts))
bpy.ops.maximize.center_loop()
check(all(abs(v.co.x) < 1e-4 for v in bm().verts if v.select), "Center: back in the middle")

# Build End: two quads become three, the loops through them end.
b = grid(4)
b.verts.ensure_lookup_table()
edge = next(e for e in b.edges if column_edge(e, 0.0, -0.1, 1.1) and len(e.link_faces) == 2)
bpy.ops.mesh.select_mode(type='VERT')
b = bm()
start, end = sorted(edge.verts, key=lambda v: v.co.y)
for v in (start, end):
    v.select_set(True)
    b.select_history.add(v)
flush(b)
faces = len(b.faces)
bpy.ops.maximize.build_end()
b = bm()
check(len(b.faces) == faces + 1 and all(len(f.verts) == 4 for f in b.faces), "Build End: 2 quads become 3, all quads")
check(not any(e.is_wire for e in b.edges), "Build End: no loose edges")

# Build Corner (edge rotate on two quads).
b = grid(4)
select_edges(b, lambda e: column_edge(e, 0.0, -0.1, 1.1) and len(e.link_faces) == 2)
bpy.ops.maximize.build_corner()
check(all(len(f.verts) == 4 for f in bm().faces), "Build Corner: still quads")

# GeoPoly: a squashed square becomes a square.
fresh(bpy.ops.mesh.primitive_plane_add, mode='FACE')
b = bm()
b.verts.ensure_lookup_table()
b.verts[0].co += Vector((0.3, 0.1, 0.0))
for f in b.faces:
    f.select_set(True)
flush(b)
bpy.ops.maximize.geopoly()
b = bm()
lengths = [e.calc_length() for e in b.edges]
check(max(lengths) - min(lengths) < 1e-4, "GeoPoly: equal sides {}".format([round(x, 3) for x in lengths]))

# Generate Topology.
for pattern, faces in (('QUADS', 4), ('FAN', 4), ('TRIANGLES', 2), ('INSET', 5), ('DIAMOND', 4)):
    fresh(bpy.ops.mesh.primitive_plane_add, mode='FACE')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.maximize.generate_topology(pattern=pattern)
    check(len(bm().faces) == faces, "Generate Topology {}: {} faces, got {}".format(pattern, faces, len(bm().faces)))
fresh(bpy.ops.mesh.primitive_grid_add, mode='FACE', x_subdivisions=3, y_subdivisions=3)
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.maximize.generate_topology(pattern='DIAMOND')
b = bm()
check(sum(1 for f in b.faces if len(f.verts) == 4) >= 4, "Diamonds on a grid: inner diamonds are quads")

# To Grid: the selection lands on world Z = 0.
fresh(bpy.ops.mesh.primitive_cube_add, mode='VERT', location=(0.0, 0.0, 3.0))
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.maximize.align_to(target='GRID')
check(all(abs((bpy.context.object.matrix_world @ v.co).z) < 1e-5 for v in bm().verts), "To Grid: flat on Z = 0")

# Half, Pivot Distance, By Numeric.
b = grid()
bpy.ops.mesh.select_mode(type='VERT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.maximize.select_half(axis='X')
check(all(v.co.x >= 0.0 for v in bm().verts if v.select) and any(v.select for v in bm().verts), "Half: +X side")
bpy.ops.maximize.select_pivot_distance(distance=0.5)
check(all(v.co.length <= 0.5 for v in bm().verts if v.select) and any(v.select for v in bm().verts),
      "Pivot Distance: within 0.5")
bpy.ops.maximize.select_numeric(count=2, compare='EQUAL')
check(sum(v.select for v in bm().verts) == 4, "By Numeric: the 4 corners have 2 edges")

# Loop mode exists and passes on when off.
check(bpy.context.window_manager.maximize_click_mode == 'NONE' and not bpy.ops.maximize.loop_mode_pick.poll(),
      "Loop mode off by default")

# Previous / Next Modifier.
bpy.ops.object.mode_set(mode='OBJECT')
obj = bpy.context.object
obj.modifiers.new("A", 'SUBSURF')
obj.modifiers.new("B", 'SOLIDIFY')
obj.modifiers.active = obj.modifiers["B"]
bpy.ops.maximize.modifier_step(direction='PREVIOUS')
check(obj.modifiers.active.name == "A", "Previous Modifier: A")
bpy.ops.maximize.modifier_step(direction='NEXT')
check(obj.modifiers.active.name == "B", "Next Modifier: B")

print("FAILURES", len(failures))
if failures:
    sys.exit(1)
