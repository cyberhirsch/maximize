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

print("FAILURES", len(failures), failures)
