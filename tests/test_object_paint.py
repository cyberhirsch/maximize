# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Object Paint: placing copies along a stroke, aligned to the surface, and Fill.

moritz --factory-startup -b --python tests/test_object_paint.py
"""

import math
import os
import random
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import addon_utils  # noqa: E402

addon_utils.enable("maximize", default_set=True)
from maximize import object_paint  # noqa: E402

failures = []


def check(ok, what):
    print(("ok   " if ok else "FAIL ") + what)
    if not ok:
        failures.append(what)


ctx = bpy.context
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o)
bpy.ops.mesh.primitive_cone_add()
cone = ctx.active_object
s = object_paint.settings(ctx)
check(not bpy.ops.maximize.object_paint.poll(), "Paint needs Paint Objects")
bpy.ops.maximize.object_paint_pick()
check(object_paint.paint_objects(ctx) == [cone] and bpy.ops.maximize.object_paint.poll(), "Add Selected")

# Spacing: a 10 long stroke every 2.5 gives 5 points (0, 2.5, 5, 7.5, 10), in two pieces too.
path = [(Vector((0.0, 0.0, 0.0)), Vector((0.0, 0.0, 1.0))), (Vector((10.0, 0.0, 0.0)), Vector((0.0, 0.0, 1.0)))]
points, rest = object_paint.stroke_points(path, 2.5)
check([round(p.x, 3) for p, _n, _d in points] == [0.0, 2.5, 5.0, 7.5, 10.0], "Spacing along the stroke")
half = [(Vector((0.0, 0.0, 0.0)), path[0][1]), (Vector((4.0, 0.0, 0.0)), path[0][1])]
first, due = object_paint.stroke_points(half, 2.5)
second, _due = object_paint.stroke_points([half[1], path[1]], 2.5, due)
check([round(p.x, 3) for p, _n, _d in first + second] == [0.0, 2.5, 5.0, 7.5, 10.0], "Spacing carries over")
check([round(p.x, 3) for p, _n, _d in object_paint.fill_points(path, 3)] == [0.0, 5.0, 10.0], "Fill points: 3, evenly")

# Placement: Z along the normal; with the normal along X, the copy's Z points along X.
rng = random.Random(0)
m = object_paint.placement(s, Vector((1.0, 2.0, 3.0)), Vector((1.0, 0.0, 0.0)), Vector((0.0, 1.0, 0.0)), rng)
z = (m.to_3x3() @ Vector((0.0, 0.0, 1.0))).normalized()
check((m.translation - Vector((1.0, 2.0, 3.0))).length < 1e-5 and (z - Vector((1.0, 0.0, 0.0))).length < 1e-5,
      "Align Z to the normal")
s.flip = True
z = (object_paint.placement(s, Vector(), Vector((0.0, 0.0, 1.0)), Vector((1.0, 0.0, 0.0)), rng).to_3x3()
     @ Vector((0.0, 0.0, 1.0))).normalized()
check((z - Vector((0.0, 0.0, -1.0))).length < 1e-5, "Flip: into the surface")
s.flip = False
s.align = 'X'
x = (object_paint.placement(s, Vector(), Vector((0.0, 0.0, 1.0)), Vector((1.0, 0.0, 0.0)), rng).to_3x3()
     @ Vector((1.0, 0.0, 0.0))).normalized()
check((x - Vector((0.0, 0.0, 1.0))).length < 1e-5, "Align X to the normal")
s.align = 'Z'
s.offset = 0.5
m = object_paint.placement(s, Vector(), Vector((0.0, 0.0, 1.0)), Vector((1.0, 0.0, 0.0)), rng)
check(abs(m.translation.z - 0.5) < 1e-5, "Offset off the surface")
s.offset = 0.0
s.scale = (200.0, 50.0, 50.0)
check(all(abs(c - 2.0) < 1e-5 for c in object_paint.placement(
    s, Vector(), Vector((0.0, 0.0, 1.0)), Vector((1.0, 0.0, 0.0)), rng).to_scale()), "Uniform scale: X's for all")
s.scale_uniform = False
sc = object_paint.placement(s, Vector(), Vector((0.0, 0.0, 1.0)), Vector((1.0, 0.0, 0.0)), rng).to_scale()
check(abs(sc.x - 2.0) < 1e-5 and abs(sc.y - 0.5) < 1e-5, "Scale per axis")
s.scale = (100.0, 100.0, 100.0)
s.scale_uniform = True
s.rotation = (0.0, 0.0, math.pi / 2)
m = object_paint.placement(s, Vector(), Vector((0.0, 0.0, 1.0)), Vector((1.0, 0.0, 0.0)), rng)
check(((m.to_3x3() @ Vector((1.0, 0.0, 0.0))) - Vector((0.0, 1.0, 0.0))).length < 1e-5, "Rotation Z 90")
s.rotation = (0.0, 0.0, 0.0)

# Fill: 4 instances of the cone along the path, and again in place of them.
placed = object_paint.fill(ctx, path, 4)
check(len(placed) == 4 and all(o.data == cone.data for o in placed), "Fill: 4 instances")
names = [o.name for o in placed]
again = object_paint.fill(ctx, path, 2, names)
check(len(again) == 2 and not any(bpy.data.objects.get(n) for n in names if n not in {o.name for o in again}),
      "Fill again: replaces the last ones")

print("FAILURES", len(failures))
if failures:
    sys.exit(1)
