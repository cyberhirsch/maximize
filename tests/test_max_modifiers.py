# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Max's modifiers as Geometry Nodes: Extrude (Extrude / Bevel / Profile), Noise, Normal, STL Check.

moritz --factory-startup -b --python tests/test_max_modifiers.py
"""

import os
import sys

import bpy
import bmesh

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import addon_utils  # noqa: E402

addon_utils.enable("maximize", default_set=True)
from maximize import max_modifiers  # noqa: E402
from maximize.nodes import modifier_input  # noqa: E402

failures = []


def check(ok, what):
    print(("ok   " if ok else "FAIL ") + what)
    if not ok:
        failures.append(what)


def evaluated(obj):
    """(vertex count, face count, min corner, max corner, mesh) of the evaluated object."""
    obj.update_tag()
    dg = bpy.context.evaluated_depsgraph_get()
    e = obj.evaluated_get(dg)
    me = e.to_mesh()
    cos = [v.co.copy() for v in me.vertices]
    bm = bmesh.new()
    bm.from_mesh(me)
    closed = all(len(ed.link_faces) == 2 for ed in bm.edges)
    volume = bm.calc_volume(signed=True)
    bm.free()
    out = (len(me.vertices), len(me.polygons),
           tuple(round(min(c[i] for c in cos), 3) for i in range(3)) if cos else None,
           tuple(round(max(c[i] for c in cos), 3) for i in range(3)) if cos else None, closed, volume)
    e.to_mesh_clear()
    return out


ctx = bpy.context
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o)

# A 2 x 2 square shape (closed poly spline).
curve = bpy.data.curves.new("Square", 'CURVE')
curve.dimensions = '2D'
spline = curve.splines.new('POLY')
spline.points.add(3)
for p, co in zip(spline.points, ((-1, -1), (1, -1), (1, 1), (-1, 1))):
    p.co = (co[0], co[1], 0.0, 1.0)
spline.use_cyclic_u = True
shape = bpy.data.objects.new("Square", curve)
ctx.collection.objects.link(shape)
ctx.view_layer.objects.active = shape
shape.select_set(True)

bpy.ops.maximize.add_extrude()
mod = shape.modifiers[-1]
modifier_input(mod, "Amount").value = 0.5
n, f, lo, hi, closed, vol = evaluated(shape)
print("extrude", n, f, lo, hi, closed, vol)
check(lo == (-1.0, -1.0, 0.0) and hi == (1.0, 1.0, 0.5), "Extrude: 2 x 2 x 0.5 box")
check(closed and f == 6, "Extrude: capped, 6 faces")
check(abs(vol - 2.0) < 1e-4, "Extrude: normals point out (volume 2)")

# Drawn clockwise: same box, still facing out.
for p, co in zip(spline.points, ((-1, -1), (-1, 1), (1, 1), (1, -1))):
    p.co = (co[0], co[1], 0.0, 1.0)
check(abs(evaluated(shape)[5] - 2.0) < 1e-4, "Extrude: clockwise shape faces out too")
modifier_input(mod, "Segments").value = 3
n, f, _lo, _hi, closed, _vol = evaluated(shape)
check(f == 14 and closed, "Extrude: 3 segments")
modifier_input(mod, "Segments").value = 1

modifier_input(mod, "Mode").value = "Bevel"
modifier_input(mod, "Level 1 Height").value = 0.2
modifier_input(mod, "Level 2").value = True
modifier_input(mod, "Level 2 Height").value = 0.1
modifier_input(mod, "Level 2 Outline").value = -0.1
n, f, lo, hi, closed, vol = evaluated(shape)
print("bevel", n, f, lo, hi, closed, vol)
check(abs(hi[2] - 0.3) < 1e-3 and closed, "Bevel: two levels, 0.3 high, closed")
check(abs(vol - 1.16133) < 1e-3, "Bevel: mitered outline (volume of a box plus a frustum)")
top = [round(c, 3) for c in hi[:2]]
check(top == [1.0, 1.0], "Bevel: widest at the bottom")

# Profile: a small 2-point profile spline.
pcurve = bpy.data.curves.new("Profile", 'CURVE')
ps = pcurve.splines.new('POLY')
ps.points.add(1)
ps.points[0].co = (0.0, 0.0, 0.0, 1.0)
ps.points[1].co = (0.0, 0.4, 0.0, 1.0)
profile = bpy.data.objects.new("Profile", pcurve)
ctx.collection.objects.link(profile)
modifier_input(mod, "Mode").value = "Profile"
modifier_input(mod, "Profile").value = profile
n, f, lo, hi, closed, vol = evaluated(shape)
print("profile", n, f, lo, hi, closed, vol)
check(n > 0 and abs((hi[2] - lo[2]) - 0.4) < 1e-3, "Profile: swept profile 0.4 high")

# Noise on a subdivided plane.
bpy.ops.mesh.primitive_grid_add(x_subdivisions=10, y_subdivisions=10, size=2)
grid = ctx.active_object
bpy.ops.maximize.add_noise()
nmod = grid.modifiers[-1]
modifier_input(nmod, "Strength").value = (0.0, 0.0, 0.5)
_n, _f, lo, hi, _c, _v = evaluated(grid)
print("noise", lo, hi)
check(hi[2] - lo[2] > 0.05 and lo[0] == -1.0, "Noise: moves along Z only")
modifier_input(nmod, "Seed").value = 3
_n, _f, lo2, hi2, _c, _v = evaluated(grid)
check((lo2, hi2) != (lo, hi), "Noise: another seed, another result")

# Normal: flips a closed cube inside out.
bpy.ops.mesh.primitive_cube_add()
cube = ctx.active_object
bpy.ops.maximize.add_normal()
_n, _f, _lo, _hi, _c, vol = evaluated(cube)
check(vol < 0, "Normal: flipped")

# STL Check: a closed cube is fine; an open one gets red marks and a warning.
bpy.ops.maximize.add_stl_check()
n_closed = evaluated(cube)[0]
check(n_closed == 8, "STL Check: closed cube unchanged")
bm = bmesh.new()
bm.from_mesh(cube.data)
bm.faces.ensure_lookup_table()
bm.faces.remove(bm.faces[0])
bm.to_mesh(cube.data)
bm.free()
cube.data.update()
n_open = evaluated(cube)[0]
check(n_open > 8, "STL Check: open edges marked")
smod = cube.modifiers[-1]
warnings = [w.message for w in getattr(smod, "node_warnings", ())]
print("warnings", warnings)
check(any("4 problem edges" in w for w in warnings), "STL Check: warning counts 4 open edges")

print("FAILURES", len(failures))
if failures:
    sys.exit(1)
