# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Moritz has no Max sidebar tab (Seb's decision): every panel in the sidebar's "Max" category
hides there, in Object Mode and in Edit Mode. In stock Blender the tab stays.

moritz --factory-startup -b --python tests/test_no_max_tab.py
"""

import os
import sys

import bpy

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import addon_utils  # noqa: E402

addon_utils.enable("maximize", default_set=True)

failures = []


def check(ok, what):
    print(("ok   " if ok else "FAIL ") + what)
    if not ok:
        failures.append(what)


moritz = hasattr(bpy.types, "PROPERTIES_PT_create")
panels = [cls for cls in bpy.types.Panel.__subclasses__()
          if getattr(cls, "bl_category", None) == "Max" and getattr(cls, "bl_region_type", None) == 'UI'
          and getattr(cls, "is_registered", False)]
check(len(panels) >= 4, "found the Max panels: " + ", ".join(sorted(c.__name__ for c in panels)))

bpy.ops.mesh.primitive_cube_add()
win = bpy.context.window_manager.windows[0]
area = next(a for a in win.screen.areas if a.type == 'VIEW_3D')
region = next(r for r in area.regions if r.type == 'UI')


def shown(mode):
    with bpy.context.temp_override(window=win, area=area, region=region):
        return [c.__name__ for c in panels if not hasattr(c, "poll") or c.poll(bpy.context)]


bpy.context.tool_settings.mesh_select_mode = (False, False, True)
in_object = shown('OBJECT')
bpy.ops.object.mode_set(mode='EDIT')
in_edit = shown('EDIT_MESH')
bpy.ops.object.mode_set(mode='OBJECT')
if moritz:
    check(not in_object, "Moritz, Object Mode: no Max tab " + str(in_object))
    check(not in_edit, "Moritz, Edit Mode: no Max tab " + str(in_edit))
else:
    check(bool(in_object), "Blender: the Max tab stays " + str(in_object))


# The header Max menu: stock Blender only. In Moritz its entries are in Blender's own menus.
from maximize import ui  # noqa: E402
header = [f.__name__ for f in bpy.types.VIEW3D_MT_editor_menus._dyn_ui_initialize()]
if moritz:
    check("_header_menu" not in header, "Moritz: no Max menu in the header")
    for menu, entries in ui._MORITZ_ENTRIES.items():
        check(menu in ui._moritz_draws, "Moritz: entries in " + menu)
    for menu in ui._MORITZ_ALIASES:
        check(menu in ui._moritz_draws, "Moritz: aliases in " + menu)
    ops = {e for entries in ui._MORITZ_ENTRIES.values() for e in entries if isinstance(e, str)}
    menu_ops = {"maximize.uvw_map"}  # Add Modifier
    for name in ("MAXIMIZE_MT_modify", "MAXIMIZE_MT_edit_poly", "MAXIMIZE_MT_hierarchy",
                 "MAXIMIZE_MT_tools", "MAXIMIZE_MT_views"):
        import inspect
        src = inspect.getsource(getattr(ui, name))
        import re
        for op in re.findall(r'operator\("(maximize\.[a-z_]+)"', src):
            check(op in ops or op in menu_ops, "Moritz: " + op + " has a place")
    labels = {e[1] for e in __import__("bl_operators.moritz_modifier_list", fromlist=["x"]).entries(
        bpy.context.active_object)}
    check(not any("Max" in label.split() or "(Max)" in label for label in labels),
          "Moritz: no Max-named entries in Add Modifier")
    check(bpy.types.MAXIMIZE_MT_spline_tools.bl_label == "Spline Tools", "Moritz: Spline Tools")
else:
    check("_header_menu" in header, "Blender: the Max menu stays in the header")
    check(not ui._moritz_draws, "Blender: nothing added to its menus")

print("FAILURES", len(failures), failures)
