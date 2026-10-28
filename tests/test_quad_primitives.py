# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Quad caps and quad poles: no n-gons, closed meshes facing out, triangles only where Sides is odd
(one per cap) or at a cone's tip; Quad Cap off gives the old geometry back.

moritz --factory-startup -b --python tests/test_quad_primitives.py
"""

import os
import sys

import bmesh
import bpy
from mathutils import Matrix

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import addon_utils  # noqa: E402

addon_utils.enable("maximize", default_set=True)
from maximize import primitives  # noqa: E402

failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)
        print("FAIL", msg)


def evaluated(obj):
    bpy.context.view_layer.update()
    eval_obj = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    bm = bmesh.new()
    bm.from_mesh(eval_obj.to_mesh())
    eval_obj.to_mesh_clear()
    return bm


def stats(bm):
    sides = [len(f.verts) for f in bm.faces]
    open_edges = sum(1 for e in bm.edges if not e.is_manifold)
    volume = bm.calc_volume(signed=True)
    zs = [v.co.z for v in bm.verts]
    return {
        "tris": sides.count(3), "quads": sides.count(4), "ngons": sum(1 for s in sides if s > 4),
        "open": open_edges, "volume": volume, "zmin": min(zs), "zmax": max(zs),
        "uv": bm.loops.layers.uv.get("UVMap") is not None,
    }


def make(kind, **params):
    obj = primitives._create_object(bpy.context, kind, Matrix())
    for name, value in params.items():
        primitives.parameter(obj, name).value = value
    obj.update_tag()
    return obj


def expect(kind, label, tris, height=None, **params):
    obj = make(kind, **params)
    s = stats(evaluated(obj))
    name = "{} {}".format(kind, label)
    if tris is not None:
        check(s["ngons"] == 0, "{}: {} n-gons".format(name, s["ngons"]))
    check(s["open"] == 0, "{}: {} open edges".format(name, s["open"]))
    check(s["volume"] > 0, "{}: faces point inward (volume {:.4f})".format(name, s["volume"]))
    if tris is not None:
        check(s["tris"] == tris, "{}: {} triangles, expected {}".format(name, s["tris"], tris))
    if height is not None:
        check(abs(s["zmax"] - s["zmin"] - height) < 1e-3,
              "{}: height {:.4f}, expected {}".format(name, s["zmax"] - s["zmin"], height))
    print(name, s)
    return obj, s


for sides in (24, 8, 10, 5, 7, 3):
    odd = sides % 2
    expect('CYLINDER', "sides {}".format(sides), 2 * odd, 1.0, Sides=sides)
    expect('CHAMFERCYL', "sides {}".format(sides), 2 * odd, 1.0, Sides=sides)
    expect('SPINDLE', "sides {}".format(sides), 2 * odd, 2.0, Sides=sides)
    if sides >= 4:
        expect('SPHERE', "segments {}".format(sides), 2 * odd, 1.0, Segments=sides)
    expect('CAPSULE', "sides {}".format(sides), 2 * odd, 2.0, Sides=sides)
    expect('OILTANK', "sides {}".format(sides), 2 * odd, 2.0, Sides=sides)

# Rings and segments.
expect('CYLINDER', "cap segs 3, height segs 4", 0, 1.0, **{"Cap Segments": 3, "Height Segments": 4})
expect('CHAMFERCYL', "cap segs 2", 0, 1.0, **{"Cap Segs": 2})
expect('SPINDLE', "cap segs 3", 0, 2.0, **{"Cap Segs": 3, "Height Segs": 2})
expect('CAPSULE', "cap segs 1", 0, 2.0, **{"Cap Segs": 1})
expect('CAPSULE', "cap segs 12", 0, 2.0, **{"Cap Segs": 12})
expect('SPHERE', "segments 64", 0, 1.0, Segments=64)

# Cone: the tip is a fan of triangles (one per side); a frustum has two quad caps.
expect('CONE', "tip", 24, 1.0)
expect('CONE', "frustum", 0, 1.0, **{"Radius 2": 0.25})

# Gengon and Prism: polygon caps.
expect('GENGON', "5 sides", 2, 1.0)
expect('GENGON', "8 sides", 0, 1.0, Sides=8)
expect('GENGON', "6 sides filleted", 0, 1.0, Sides=6, Fillet=0.1, **{"Fillet Segs": 2})
expect('PRISM', "triangle", 2, 1.0)
# L-Ext and C-Ext: caps split into convex quads (2 and 3).
obj, s = expect('L_EXT', "quad caps", 0, 1.0)
check(s["quads"] == 6 + 4, "L_EXT: 6 walls and 4 cap quads, got {}".format(s))
obj, s = expect('C_EXT', "quad caps", 0, 1.0)
check(s["quads"] == 8 + 6, "C_EXT: 8 walls and 6 cap quads, got {}".format(s))
obj, s = expect('L_EXT', "quad cap off", None, 1.0, **{"Quad Cap": False})
check(s["ngons"] == 2, "L_EXT quad cap off: two n-gon caps, got {}".format(s))

# Quad Cap off: the old caps (Cap Segments 1: one n-gon each).
obj, s = expect('CYLINDER', "quad cap off", None, 1.0, **{"Quad Cap": False, "Cap Segments": 1})
check(s["ngons"] == 2 and s["quads"] == 24, "CYLINDER quad cap off: two n-gon caps expected, got {}".format(s))
obj, s = expect('GENGON', "quad cap off", None, 1.0, **{"Quad Cap": False})
check(s["ngons"] == 2, "GENGON quad cap off: two n-gon caps expected, got {}".format(s))

# UVs: the quad caps keep a UV map in the Cylinder node's layout.
obj, s = expect('CYLINDER', "uv", 0, 1.0)
check(s["uv"], "CYLINDER: no UVMap")

print("FAILURES", len(failures))
if failures:
    sys.exit(1)
