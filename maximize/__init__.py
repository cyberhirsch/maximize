# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

bl_info = {
    "name": "Maximize",
    "author": "Moritz Authors",
    "version": (1, 0, 0),
    "blender": (5, 3, 0),
    "location": "3D Viewport > Max menu, sidebar > Max tab, right-click quad menu",
    "description": "3ds Max workflow for Moritz: Max keymap, quad menu, Max vocabulary, "
                   "Transform Type-In, Align, Array, Spacing, editable primitives, UVW Map and more",
    "support": 'OFFICIAL',
    "category": "Interface",
}

if "bpy" in locals():
    import importlib
    for _mod in _modules:
        importlib.reload(_mod)

import bpy

from . import (
    keymaps,
    preferences,
    vocabulary,
    viewport,
    cameras,
    selection,
    region_select,
    hover,
    edit_poly,
    sculpt,
    spline_tools,
    spline_more,
    edit_spline,
    smoothing,
    poly_tools,
    smart_extrude,
    poly_ribbon,
    freeform,
    modifier_gizmos,
    transform,
    tools,
    shapes,
    primitives,
    uvw_map,
    max_scene,
    quad_menu,
    outliner,
    caddy,
    hold,
    ui,
)

_modules = (
    keymaps,
    preferences,
    vocabulary,
    viewport,
    cameras,
    selection,
    region_select,
    hover,
    edit_poly,
    sculpt,
    spline_tools,
    spline_more,
    edit_spline,
    smoothing,
    poly_tools,
    smart_extrude,
    poly_ribbon,
    freeform,
    modifier_gizmos,
    transform,
    tools,
    shapes,
    primitives,
    uvw_map,
    max_scene,
    quad_menu,
    outliner,
    caddy,
    hold,
    ui,
)


def register():
    for mod in _modules:
        mod.register()
    preferences.first_run_setup()
    keymaps.reload_active()


def unregister():
    for mod in reversed(_modules):
        mod.unregister()
