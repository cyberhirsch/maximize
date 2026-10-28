# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""The Freeform modifier: conform onto a surface, and the PolyDraw builders.

moritz --factory-startup -b --python tests/test_freeform.py
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
from maximize import freeform  # noqa: E402
from maximize.nodes import modifier_input  # noqa: E402

failures = []


def check(ok, what):
    print(("ok   " if ok else "FAIL ") + what)
    if not ok:
        failures.append(what)


def radii(obj):
    bpy.context.view_layer.update()
    ev = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mesh = ev.to_mesh()
    out = [(obj.matrix_world @ v.co).length for v in mesh.vertices]
    ev.to_mesh_clear()
    return out


for o in list(bpy.data.objects):
    bpy.data.objects.remove(o)
ctx = bpy.context
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=64, ring_count=32)
sphere = ctx.active_object
bpy.ops.mesh.primitive_grid_add(x_subdivisions=4, y_subdivisions=4, size=0.6, location=(0.0, 0.0, 2.0))
patch = ctx.active_object
sphere.select_set(True)
patch.select_set(True)
ctx.view_layer.objects.active = patch

# The modifier: the patch lands on the sphere, Offset above it.
check(bpy.ops.maximize.freeform_add() == {'FINISHED'}, "Freeform added")
mod = freeform.freeform_modifier(patch)
check(mod is not None and mod.name == "Freeform" and freeform.target_of(patch) == sphere, "target is the other mesh")
r = radii(patch)
check(all(abs(x - 1.0) < 0.01 for x in r), "conformed onto the sphere ({:.3f}..{:.3f})".format(min(r), max(r)))
modifier_input(mod, "Offset").value = 0.1
patch.update_tag()
r = radii(patch)
check(all(abs(x - 1.1) < 0.01 for x in r), "Offset 0.1 above it ({:.3f})".format(min(r)))
modifier_input(mod, "Conform").value = 0.0
patch.update_tag()
check(all(abs(x - 2.0) < 0.2 for x in radii(patch)), "Conform 0: left where it is")
modifier_input(mod, "Conform").value = 1.0
modifier_input(mod, "Offset").value = 0.0
modifier_input(mod, "Surface").value = None
patch.update_tag()
check(all(x > 1.9 for x in radii(patch)), "no target: left where it is")
modifier_input(mod, "Surface").value = sphere

# Conform (bake): the vertices themselves go onto the surface.
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
check(bpy.ops.maximize.freeform_conform() == {'FINISHED'}, "Conform runs")
bm = bmesh.from_edit_mesh(patch.data)
check(all(abs((patch.matrix_world @ v.co).length - 1.0) < 0.01 for v in bm.verts), "Conform: vertices on the surface")

# Builders, on an empty Freeform object.
bpy.ops.object.mode_set(mode='OBJECT')
for o in ctx.selected_objects:
    o.select_set(False)
sphere.select_set(True)
ctx.view_layer.objects.active = sphere
check(bpy.ops.maximize.freeform_new_object() == {'FINISHED'}, "New Object")
obj = ctx.active_object
check(obj is not sphere and obj.mode == 'EDIT' and freeform.target_of(obj) == sphere, "new object on the sphere, editing")


def arc(count, z=0.0):
    pts = []
    for i in range(count):
        a = i * 0.1
        n = Vector((math.cos(a), math.sin(a), z)).normalized()
        pts.append((n.copy(), n, 0.01))
    return pts


def counts():
    bm = bmesh.from_edit_mesh(obj.data)
    return len(bm.verts), len(bm.faces), sum(1 for f in bm.faces if len(f.verts) == 4)


made = freeform.build_strip(obj, arc(6), 20)
v, f, q = counts()
check(made == 5 and f == 5 and q == 5 and v == 12, "Strips: 5 quads along 6 points, got {}".format((v, f, q)))
bm = bmesh.from_edit_mesh(obj.data)
check(all(f.normal.dot(f.calc_center_median().normalized()) > 0.9 for f in bm.faces), "Strips face out of the surface")
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.delete(type='VERT')
made = freeform.build_strip(obj, arc(6), 60, 3)
check(made == 15 and counts()[1] == 15, "Surface: 3 quads across, 15 quads")
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.delete(type='VERT')

ring = []
for i in range(8):
    a = 2.0 * math.pi * i / 8.0
    p = Vector((0.3 * math.cos(a), 0.3 * math.sin(a), 1.0))
    ring.append((p, Vector((0.0, 0.0, 1.0)), 0.01))
ring.append(ring[0])
check(freeform.build_shape(obj, ring) == 1 and counts()[:2] == (8, 1), "Shapes: an 8-sided polygon, got {}".format(counts()))

# Branches: the shape extrudes along a stroke and thins out.
stroke = [(Vector((0.0, 0.0, 1.0 + 0.2 * i)), Vector((0.0, 0.0, 1.0)), 0.01) for i in range(4)]
check(freeform.build_branch(obj, stroke, -0.9) == 3, "Branches: 3 steps")
bm = bmesh.from_edit_mesh(obj.data)
top = [f for f in bm.faces if f.select]
size = max((v.co.xy.length for f in top for v in f.verts), default=0.0)
check(len(top) == 1 and abs(size - 0.03) < 1e-3 and abs(top[0].calc_center_median().z - 1.6) < 1e-4,
      "Branches: end at 1.6, thinned to a tenth ({:.3f})".format(size))
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.delete(type='VERT')

# Topology: 3 lines one way, 3 across: 4 quads.
along = [[Vector((-5.0, y)), Vector((25.0, y))] for y in (0.0, 10.0, 20.0)]
across = [[Vector((x, -5.0)), Vector((x, 25.0))] for x in (0.0, 10.0, 20.0)]


def cast(screen):
    return Vector((screen.x / 10.0, screen.y / 10.0, 1.0)), Vector((0.0, 0.0, 1.0))


check(freeform.build_topology(obj, along + across, cast) == 4, "Topology: 4 quads")
v, f, q = counts()
check((v, f, q) == (9, 4, 4), "Topology: 3 x 3 vertices, got {}".format((v, f, q)))
bm = bmesh.from_edit_mesh(obj.data)
check(all(f.normal.z > 0.9 for f in bm.faces), "Topology: faces up")

# Splines: a new spline object.
curve = freeform.build_spline(ctx, obj, arc(5))
check(curve is not None and curve.type == 'CURVE' and len(curve.data.splines[0].points) == 5, "Splines: a spline object")

# Solve Surface runs.
check(bpy.ops.maximize.freeform_solve() == {'FINISHED'}, "Solve Surface")
bpy.ops.object.mode_set(mode='OBJECT')

print("FAILURES", len(failures))
if failures:
    sys.exit(1)
