# Run: moritz.exe (or blender.exe) --factory-startup -b --python tests/test_max_shapes_import.py
# Shapes exported from 3ds Max 2026 by max_side/moritz_export.ms (data/max2026_shapes.mxscene: a
# renderable Circle, a filleted distorted Star, a Line with corner/bezier/smooth knots, rotated,
# and a Rectangle with a rectangular render section) import with Max's knots and settings.
import json
import os
import sys

import addon_utils

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
addon_utils.enable("maximize", default_set=True)

import bpy
from mathutils import Vector

from maximize import max_scene, shapes


def say(*a): print("MXSI", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", name, *info)


path = os.path.join(HERE, "data", "max2026_shapes.mxscene")
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o)
max_scene.import_mxscene(bpy.context, path, convert_materials=False)
data = json.load(open(path, encoding="utf-8-sig"))
scale = max_scene._meters_per_unit(data)
for nd in data["nodes"]:
    obj = bpy.data.objects.get(nd["name"])
    if obj is None:
        check("import " + nd["name"], False, "missing")
        continue
    ref = nd["shape"]["splines"]
    worst = 0.0
    same = obj.type == 'CURVE' and len(obj.data.splines) == len(ref)
    for spline, rs in zip(obj.data.splines, ref):
        same &= len(spline.bezier_points) == len(rs["knots"]) and spline.use_cyclic_u == rs["closed"]
        n = len(rs["knots"])
        lines = {i for i, seg in enumerate(rs.get("segments", [])) if seg.lstrip("#") == "line"}
        for i, (bp, (p, left, right, _t)) in enumerate(zip(spline.bezier_points, rs["knots"])):
            # Max ignores the handles on its line segments; Moritz puts them on the line.
            pairs = [(bp.co, p)]
            if (i - 1) % n not in lines or (i == 0 and not rs["closed"]):
                pairs.append((bp.handle_left, left))
            if i not in lines:
                pairs.append((bp.handle_right, right))
            for a, b in pairs:
                worst = max(worst, (a - Vector(b) * scale).length)
    check("knots " + nd["name"], same and worst < 1e-5, shapes.shape_kind(obj), "worst", "{:.1e}".format(worst))

circle = bpy.data.objects["MxCircle"]
p = circle.data.maximize_shape
check("circle parametric + rendering", p.kind == 'CIRCLE' and p.render_renderer and p.render_viewport and
      abs(p.thickness - 2 * scale) < 1e-6 and circle.modifiers.get("Rendering") is not None, p.kind, p.thickness, p.render_renderer, p.render_viewport)
rect = bpy.data.objects["MxRect"].data.maximize_shape
check("rect rendering", rect.render_mode == 'RECTANGULAR' and rect.render_renderer and not rect.render_viewport and
      abs(rect.rect_length - 3 * scale) < 1e-6, rect.render_mode, rect.render_renderer, rect.render_viewport, rect.rect_length)
line = bpy.data.objects["MxLine"]
bp = line.data.splines[0].bezier_points
check("line types", shapes.shape_kind(line) is None and bp[1].handle_left_type == 'FREE' and
      abs(bp[0].handle_right.y) < 1e-9 and bp[2].handle_left_type == 'FREE',
      [(b.handle_left_type, b.handle_right_type) for b in bp])
