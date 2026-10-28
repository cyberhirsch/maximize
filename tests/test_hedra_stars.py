# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Hedra: the five solids, Star1 / Star2, and Axis Scaling P / Q / R.

moritz --factory-startup -b --python tests/test_hedra_stars.py
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


def check(ok, what):
    print(("ok   " if ok else "FAIL ") + what)
    if not ok:
        failures.append(what)


def shape(**params):
    obj = primitives._create_object(bpy.context, 'HEDRA', Matrix())
    for name, value in params.items():
        primitives.parameter(obj, name).value = value
    obj.update_tag()
    bpy.context.view_layer.update()
    ev = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    bm = bmesh.new()
    bm.from_mesh(ev.to_mesh())
    ev.to_mesh_clear()
    radii = [v.co.length for v in bm.verts]
    open_edges = sum(1 for e in bm.edges if not e.is_manifold)
    return {"verts": len(bm.verts), "faces": len(bm.faces), "open": open_edges,
            "rmax": max(radii), "rmin": min(radii), "volume": bm.calc_volume(signed=True)}


for family, faces in ((0, 4), (1, 6), (2, 8), (3, 12), (4, 20)):
    s = shape(Family=family)
    check(s["faces"] == faces and s["open"] == 0 and abs(s["rmax"] - 0.5) < 1e-3,
          "family {}: {} faces, radius 0.5, got {}".format(family, faces, s))

s = shape(Family=5)
check(s["faces"] == 60 and s["verts"] == 32 and s["open"] == 0 and abs(s["rmax"] - 0.5) < 1e-3 and s["volume"] > 0,
      "Star1: 12 five-sided spikes (60 triangles), tips at the radius, got {}".format(s))
s = shape(Family=6)
check(s["faces"] == 60 and s["verts"] == 32 and s["open"] == 0 and abs(s["rmax"] - 0.5) < 1e-3 and s["volume"] > 0,
      "Star2: 20 three-sided spikes (60 triangles), tips at the radius, got {}".format(s))

# Axis Scaling: P pushes the octahedron's triangles out, Q the cube's squares; R leaves them alone.
s = shape(Family=2, **{"Axis Scaling P": 150.0})
check(s["faces"] == 24 and s["open"] == 0 and s["volume"] > 0, "octahedron P 150: 8 spikes, got {}".format(s))
s = shape(Family=1, **{"Axis Scaling Q": 50.0})
check(s["faces"] == 24 and s["open"] == 0 and s["volume"] > 0, "cube Q 50: 6 dents, got {}".format(s))
s = shape(Family=1, **{"Axis Scaling R": 150.0})
check(s["faces"] == 6, "cube R 150: unchanged, got {}".format(s))

print("FAILURES", len(failures))
if failures:
    sys.exit(1)
