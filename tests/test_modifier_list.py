# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Moritz's modifier list: Max names by name scheme, presets, keywords, add-on entries.

moritz --factory-startup -b --python tests/test_modifier_list.py
"""

import os
import sys

import bpy

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import addon_utils  # noqa: E402

addon_utils.enable("maximize", default_set=True)
from bl_operators import moritz_modifier_list as mlist  # noqa: E402
from maximize import vocabulary  # noqa: E402

failures = []


def check(ok, what):
    print(("ok   " if ok else "FAIL ") + what)
    if not ok:
        failures.append(what)


ctx = bpy.context
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o)
bpy.ops.mesh.primitive_cube_add()
cube = ctx.active_object

vocabulary.set_scheme('BLENDER')
labels = {e[1]: e for e in mlist.entries(cube)}
check("Simple Deform" in labels and "Bend" not in labels, "Blender scheme: Blender's names")
check("bend" in labels["Simple Deform"][2].lower() + labels["Simple Deform"][3], "Simple Deform finds bend")
check("Shell" in labels["Solidify"][2], "Solidify lists Shell")
check("UVW Map" in labels and "Freeform (Max)" in labels, "Add-on entries in the list")

vocabulary.set_scheme('MAX')
labels = {e[1]: e for e in mlist.entries(cube)}
check(all(n in labels for n in ("Bend", "Taper", "Twist", "Stretch", "Lathe", "Shell", "Skin", "Smooth",
                                "Lattice", "Chamfer", "TurboSmooth")), "Max scheme: Max's names")
check("Simple Deform" not in labels and "Screw" not in labels, "Max scheme: covered Blender names gone")
check("Triangulate" in labels, "Max scheme: Blender's own modifiers stay")
check(labels["Skin"][2] == "Armature" and labels["Lattice"][2] == "Wireframe", "Clashes: Skin = Armature, Lattice = Wireframe")
check(labels["Smooth"][0] == "OP:object.shade_auto_smooth" and labels["FFD"][2] == "Lattice",
      "Smooth = Smooth by Angle, FFD = Lattice")
check("Skin (Blender)" in labels and "Smooth (Blender)" in labels, "Blender's Skin and Smooth renamed in the Max scheme")

mlist.add(ctx, labels["Taper"][0], "Taper")
mod = cube.modifiers[-1]
check(mod.type == 'SIMPLE_DEFORM' and mod.deform_method == 'TAPER' and mod.name == "Taper", "Taper preset and name")
mlist.add(ctx, labels["Lathe"][0], "Lathe")
check(cube.modifiers[-1].type == 'SCREW' and cube.modifiers[-1].name == "Lathe", "Lathe is Screw")

vocabulary.set_scheme('BLENDER')
mlist.add(ctx, "SOLIDIFY", "Solidify")
check(cube.modifiers[-1].name == "Solidify", "Blender scheme keeps Blender's name")

# Search items: keywords after "|".
vocabulary.set_scheme('MAX')
items = mlist._search_items(None, ctx)
bend = [name for _k, name, _d, _i in items if name.startswith("Bend|")]
check(bend and "Simple Deform" in bend[0], "Search item: Bend with Simple Deform as hint")
vocabulary.set_scheme('BLENDER')

bpy.ops.curve.primitive_bezier_curve_add()
labels = {e[1] for e in mlist.entries(ctx.active_object)}
check("Subdivision Surface" in labels and "Weighted Normal" in labels and "Edit Poly" not in labels,
      "Curve: only modifiers that work on curves")

print("FAILURES", len(failures))
if failures:
    sys.exit(1)
