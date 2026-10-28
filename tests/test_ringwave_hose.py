# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""RingWave's animation (growth, crawling waves, inner edge) and Hose bound to object pivots.

moritz --factory-startup -b --python tests/test_ringwave_hose.py
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Matrix, Vector

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import addon_utils  # noqa: E402

addon_utils.enable("maximize", default_set=True)
from maximize import primitives  # noqa: E402

failures = []


def check(ok, what):
    print(("ok   " if ok else "FAIL ") + what)
    if not ok:
        failures.append(what)


def make(kind, **params):
    obj = primitives._create_object(bpy.context, kind, Matrix())
    for name, value in params.items():
        primitives.parameter(obj, name).value = value
    obj.update_tag()
    return obj


def verts(obj):
    bpy.context.view_layer.update()
    ev = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    bm = bmesh.new()
    bm.from_mesh(ev.to_mesh())
    ev.to_mesh_clear()
    return [v.co.copy() for v in bm.verts]


def radial(cos):
    return [Vector((c.x, c.y)).length for c in cos]


scene = bpy.context.scene
scene.frame_set(0)
ring = make('RINGWAVE', **{"Major Amplitude": 0.0})
r = radial(verts(ring))
check(abs(max(r) - 1.0) < 1e-3 and abs(min(r) - 0.8) < 1e-3, "still ring: 0.8 to 1.0, got {:.3f}..{:.3f}".format(min(r), max(r)))

# Growth: grow and stay over frames 0..60.
for name, value in (("Growth", 1), ("Grow Start", 0.0), ("Grow End", 60.0)):
    primitives.parameter(ring, name).value = value
ring.update_tag()
scene.frame_set(30)
check(abs(max(radial(verts(ring))) - 0.5) < 1e-3, "grow and stay: half size at frame 30")
scene.frame_set(90)
check(abs(max(radial(verts(ring))) - 1.0) < 1e-3, "grow and stay: full size after Grow End")
primitives.parameter(ring, "Growth").value = 2
ring.update_tag()
scene.frame_set(90)
check(abs(max(radial(verts(ring))) - 0.5) < 1e-3, "cyclic growth: starts again (half at frame 90)")
primitives.parameter(ring, "Growth").value = 0

# Crawl: the outer wave moves with time.
for name, value in (("Major Amplitude", 0.05), ("Major Crawl Time", 40.0)):
    primitives.parameter(ring, name).value = value
ring.update_tag()
scene.frame_set(0)
a = verts(ring)
scene.frame_set(10)
b = verts(ring)
moved = max((p - q).length for p, q in zip(a, b))
check(moved > 0.01, "crawling wave moves, {:.4f}".format(moved))
primitives.parameter(ring, "Major Crawl Time").value = 0.0
ring.update_tag()
scene.frame_set(0)
a = verts(ring)
scene.frame_set(10)
check(max((p - q).length for p, q in zip(a, verts(ring))) < 1e-6, "no crawl time: still")

# Inner edge breakup.
primitives.parameter(ring, "Inner Cycles").value = 5
primitives.parameter(ring, "Inner Amplitude").value = 0.05
ring.update_tag()
r = radial(verts(ring))
check(min(r) < 0.8 - 0.03, "inner edge waves, min radius {:.3f}".format(min(r)))

# Hose bound to two empties: it runs from one pivot to the other.
scene.frame_set(0)
hose = make('HOSE')
bottom = bpy.data.objects.new("Bottom", None)
top = bpy.data.objects.new("Top", None)
for o in (bottom, top):
    scene.collection.objects.link(o)
bottom.location = (0.0, 0.0, 0.0)
top.location = (2.0, 1.0, 3.0)
top.rotation_euler = (math.pi, 0.0, 0.0)
primitives.parameter(hose, "Bound to Object Pivots").value = True
primitives.parameter(hose, "Bottom Object").value = bottom
primitives.parameter(hose, "Top Object").value = top
hose.update_tag()
cos = verts(hose)
near_top = min((c - top.location).length for c in cos)
near_bottom = min(c.length for c in cos)
check(abs(near_top - 0.1) < 0.01, "bound hose ends at the top object, {:.3f} away".format(near_top))
check(abs(near_bottom - 0.1) < 0.01, "bound hose starts at the bottom object, {:.3f} away".format(near_bottom))
# The top points down: the hose comes up into it from below.
check(max(c.z for c in cos) < 3.0 + 0.11, "it reaches the top object from below")
primitives.parameter(hose, "Bound to Object Pivots").value = False
hose.update_tag()
zs = [c.z for c in verts(hose)]
check(abs(max(zs) - 1.0) < 1e-3, "free hose keeps its Height")

print("FAILURES", len(failures))
if failures:
    sys.exit(1)
