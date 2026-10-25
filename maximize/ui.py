# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""The Max menu in the 3D Viewport header and the Max command panel in the sidebar."""

import os

import bpy
import bpy.utils.previews
from bpy.types import Menu, Panel

from . import primitives, uvw_map
from .nodes import draw_modifier_inputs
from .preferences import draw_keymap_switch
from .vocabulary import ALIASES


def _aliases(layout, menu):
    for ident, label, _target, _props, alias_menu, _desc in ALIASES:
        if alias_menu == menu:
            # Alias labels are already Max terms: don't run them through the Max vocabulary again.
            layout.operator("maximize." + ident, text=label, translate=False)


# ------------------------------------------------------------------------------
# Icons for the Border and Element levels, which Blender has no icons for

_icons = None


def level_icon(level):
    """Keyword arguments for a button icon of a sub-object level."""
    builtin = {'VERTEX': 'VERTEXSEL', 'EDGE': 'EDGESEL', 'POLYGON': 'FACESEL'}
    if level in builtin:
        return {"icon": builtin[level]}
    return {"icon_value": _icons[level.lower()].icon_id}


def _load_icons():
    global _icons
    _icons = bpy.utils.previews.new()
    folder = os.path.join(os.path.dirname(__file__), "icons")
    for name in ("border", "element"):
        _icons.load(name, os.path.join(folder, name + ".png"), 'IMAGE')


# ------------------------------------------------------------------------------
# Max menu

class MAXIMIZE_MT_modify(Menu):
    bl_label = "Modifiers"

    def draw(self, _context):
        layout = self.layout
        layout.operator("maximize.uvw_map", text="UVW Map")
        _aliases(layout, 'MODIFY')


class MAXIMIZE_MT_edit_poly(Menu):
    bl_label = "Edit Poly"

    def draw(self, _context):
        layout = self.layout
        layout.operator("maximize.chamfer")
        layout.operator("maximize.connect")
        layout.operator("maximize.delete_subobject", text="Delete")
        _aliases(layout, 'POLY')


class MAXIMIZE_MT_hierarchy(Menu):
    bl_label = "Hierarchy"

    def draw(self, context):
        layout = self.layout
        layout.operator("maximize.affect_pivot_only",
                        depress=context.scene.tool_settings.use_transform_data_origin)
        layout.operator("maximize.center_pivot")
        layout.operator("maximize.align_pivot_world")
        layout.operator("maximize.reset_xform")


class MAXIMIZE_MT_tools(Menu):
    bl_label = "Tools"

    def draw(self, _context):
        layout = self.layout
        layout.operator("maximize.transform_typein", text="Transform Type-In...")
        layout.operator("maximize.align", text="Align")
        layout.operator("maximize.array", text="Array...")
        layout.operator("maximize.spacing", text="Spacing Tool...")
        layout.operator("maximize.clone", text="Clone...")
        layout.separator()
        layout.operator("maximize.select_by_name", text="Select by Name...")
        layout.menu("MAXIMIZE_MT_selection_sets")
        layout.separator()
        _aliases(layout, 'OBJECT')


class MAXIMIZE_MT_views(Menu):
    bl_label = "Views"

    def draw(self, _context):
        layout = self.layout
        _aliases(layout, 'DISPLAY')
        layout.operator("maximize.viewport_maximize")
        layout.operator("maximize.camera_from_view")
        layout.separator()
        layout.operator("maximize.material_editor")
        layout.operator("maximize.render_setup")


class MAXIMIZE_MT_keymap(Menu):
    bl_label = "Keymap"

    def draw(self, context):
        draw_keymap_switch(self.layout.column(), context)


class MAXIMIZE_MT_main(Menu):
    bl_label = "Max"

    def draw(self, _context):
        layout = self.layout
        layout.menu("MAXIMIZE_MT_create", text="Create")
        layout.menu("MAXIMIZE_MT_modify")
        layout.menu("MAXIMIZE_MT_edit_poly")
        layout.menu("MAXIMIZE_MT_hierarchy")
        layout.menu("MAXIMIZE_MT_tools")
        layout.menu("MAXIMIZE_MT_views")
        layout.separator()
        layout.menu("MAXIMIZE_MT_keymap")


def _header_menu(self, context):
    if context.area.type == 'VIEW_3D':
        self.layout.menu("MAXIMIZE_MT_main")


# ------------------------------------------------------------------------------
# Command panel (sidebar > Max)

class MaxPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Max"


class MAXIMIZE_PT_create(MaxPanel, Panel):
    bl_label = "Create"

    def draw(self, context):
        grid = self.layout.grid_flow(columns=2, even_columns=True, align=True)
        grid.enabled = context.mode == 'OBJECT'
        for ident, name, _desc, icon, _num in primitives.KINDS:
            grid.operator("maximize.add_primitive", text=name, icon=icon).kind = ident


class MAXIMIZE_PT_modify(MaxPanel, Panel):
    bl_label = "Modify"

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        if obj is None:
            layout.label(text="Nothing selected")
            return
        layout.prop(obj, "name", text="")
        if primitives.is_parametric(obj):
            box = layout.box()
            box.label(text="Parameters")
            primitives.draw_parameters(box, obj)
            if primitives.is_shape(obj):
                layout.operator("maximize.convert_spline", text="Convert to Editable Spline")
            layout.operator("maximize.convert_poly", text="Convert to Editable Poly")
        mod = uvw_map.uvw_modifier(obj)
        if mod is not None:
            box = layout.box()
            box.label(text="UVW Map")
            draw_modifier_inputs(box, mod)
        row = layout.row(align=True)
        row.operator_menu_enum("object.modifier_add", "type", text="Modifier List")
        row.menu("MAXIMIZE_MT_modify", text="", icon='DOWNARROW_HLT')
        if context.mode == 'EDIT_MESH' or (obj.type == 'MESH' and primitives.primitive_modifier(obj) is None):
            box = layout.box()
            box.label(text="Selection")
            row = box.row(align=True)
            for level in ('VERTEX', 'EDGE', 'BORDER', 'POLYGON', 'ELEMENT'):
                row.operator("maximize.subobject", text="", **level_icon(level)).level = level
            if context.mode == 'EDIT_MESH':
                grid = box.grid_flow(columns=2, even_columns=True, align=True)
                for op in ("grow", "shrink", "loop", "ring"):
                    grid.operator("maximize." + op)
                box = layout.box()
                box.label(text="Edit Geometry")
                grid = box.grid_flow(columns=2, even_columns=True, align=True)
                grid.operator("mesh.extrude_context_move", text="Extrude")
                for op in ("bevel_poly", "chamfer", "inset", "connect", "cut", "swift_loop", "weld",
                           "target_weld", "collapse_sub", "bridge", "cap", "remove", "detach", "quickslice",
                           "relax", "make_planar"):
                    if op == "bevel_poly":
                        # The Max vocabulary renames Blender's Bevel to Chamfer: keep Max's Bevel.
                        grid.operator("maximize." + op, text="Bevel", translate=False)
                    else:
                        grid.operator("maximize." + op)


class MAXIMIZE_PT_hierarchy(MaxPanel, Panel):
    bl_label = "Hierarchy"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        col = self.layout.column(align=True)
        col.operator("maximize.affect_pivot_only",
                     depress=context.scene.tool_settings.use_transform_data_origin)
        col.operator("maximize.center_pivot")
        col.operator("maximize.align_pivot_world")
        col.separator()
        col.operator("maximize.reset_xform")


class MAXIMIZE_PT_utilities(MaxPanel, Panel):
    bl_label = "Utilities"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        col = self.layout.column(align=True)
        col.operator("maximize.transform_typein", text="Transform Type-In")
        col.operator("maximize.align", text="Align")
        col.operator("maximize.array", text="Array")
        col.operator("maximize.spacing", text="Spacing Tool")
        col.operator("maximize.clone", text="Clone")
        col.operator("maximize.uvw_map", text="UVW Map")
        col.separator()
        col.operator("maximize.select_by_name", text="Select by Name")


class MAXIMIZE_PT_selection_sets(MaxPanel, Panel):
    bl_label = "Named Selection Sets"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        from .selection import sub_set_names
        layout = self.layout
        if context.mode == 'EDIT_MESH':
            names = [label for _attr, label, _domain in sub_set_names(context)]
        else:
            names = [s.name for s in context.scene.maximize_sets]
        col = layout.column(align=True)
        for name in names:
            row = col.row(align=True)
            row.operator("maximize.selset_select", text=name).name = name
            row.operator("maximize.selset_remove", text="", icon='X').name = name
        layout.operator("maximize.selset_create", text="Create Selection Set", icon='ADD')


class MAXIMIZE_PT_keymap(MaxPanel, Panel):
    bl_label = "Keymap"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        draw_keymap_switch(self.layout, context)


classes = (
    MAXIMIZE_MT_modify,
    MAXIMIZE_MT_edit_poly,
    MAXIMIZE_MT_hierarchy,
    MAXIMIZE_MT_tools,
    MAXIMIZE_MT_views,
    MAXIMIZE_MT_keymap,
    MAXIMIZE_MT_main,
    MAXIMIZE_PT_create,
    MAXIMIZE_PT_modify,
    MAXIMIZE_PT_hierarchy,
    MAXIMIZE_PT_utilities,
    MAXIMIZE_PT_selection_sets,
    MAXIMIZE_PT_keymap,
)


def draw_levels(layout, context):
    """Moritz's header hook: Max's five sub-object levels instead of Blender's three select modes."""
    if context.mode != 'EDIT_MESH':
        return False
    from .selection import current_level
    current = current_level(context)
    row = layout.row(align=True)
    for level in ('VERTEX', 'EDGE', 'BORDER', 'POLYGON', 'ELEMENT'):
        op = row.operator("maximize.subobject", text="", depress=(current == level), **level_icon(level))
        op.level = level
    return True


def register():
    _load_icons()
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_editor_menus.append(_header_menu)
    # Moritz only: Blender's header has no hook.
    if hasattr(bpy.types.VIEW3D_HT_header, "select_mode_draw"):
        bpy.types.VIEW3D_HT_header.select_mode_draw = draw_levels


def unregister():
    global _icons
    if getattr(bpy.types.VIEW3D_HT_header, "select_mode_draw", None) is draw_levels:
        bpy.types.VIEW3D_HT_header.select_mode_draw = None
    bpy.types.VIEW3D_MT_editor_menus.remove(_header_menu)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    bpy.utils.previews.remove(_icons)
    _icons = None
