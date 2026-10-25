# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""The Max menu in the 3D Viewport header and the Max command panel in the sidebar."""

import os

import bpy
import bpy.utils.previews
from bpy.props import StringProperty
from bpy.types import Menu, Operator, Panel

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
# Command panel: Moritz's Command Panel (Create and Modify tabs), or the sidebar > Max tab in Blender

def has_command_panel():
    """Moritz's Properties editor is Max's Command Panel, with a Create tab."""
    return hasattr(bpy.types, "PROPERTIES_PT_create")


class MAXIMIZE_OT_create_in_viewport(Operator):
    """Create the object by dragging in the 3D Viewport, as from Max's Create panel"""
    bl_idname = "maximize.create_in_viewport"
    bl_label = "Create"
    bl_options = {'INTERNAL'}

    operator: StringProperty()
    kind: StringProperty()

    def invoke(self, context, _event):
        # The drag creation runs in a 3D Viewport; the button sits in the Command Panel.
        areas = [area for area in context.screen.areas if area.type == 'VIEW_3D']
        if not areas:
            return {'CANCELLED'}
        area = max(areas, key=lambda area: area.width * area.height)
        region = next(region for region in area.regions if region.type == 'WINDOW')
        module, name = self.operator.split(".")
        op = getattr(getattr(bpy.ops, module), name)
        props = {"kind": self.kind} if self.kind else {}
        with context.temp_override(area=area, region=region):
            op('INVOKE_DEFAULT', **props)
        return {'FINISHED'}


def _create_button(layout, operator, text, icon, kind=""):
    if has_command_panel():
        op = layout.operator("maximize.create_in_viewport", text=text, icon=icon)
        op.operator = operator
        op.kind = kind
    elif kind:
        layout.operator(operator, text=text, icon=icon).kind = kind
    else:
        layout.operator(operator, text=text, icon=icon)


def draw_object_types(layout, context, category):
    """Moritz's Create tab hook: Max's parametric primitives and shapes."""
    if category == 'GEOMETRY':
        grid = layout.grid_flow(row_major=True, columns=2, even_columns=True, align=True)
        grid.enabled = context.mode == 'OBJECT'
        for ident, name, _desc, icon, _num in primitives.KINDS:
            if ident not in primitives.SHAPES:
                _create_button(grid, "maximize.add_primitive", name, icon, ident)
        return True
    if category == 'SHAPES':
        grid = layout.grid_flow(row_major=True, columns=2, even_columns=True, align=True)
        grid.enabled = context.mode == 'OBJECT'
        _create_button(grid, "maximize.line", "Line", 'IPO_LINEAR')
        for ident, name, _desc, icon, _num in primitives.SHAPE_KINDS:
            _create_button(grid, "maximize.add_primitive", name, icon, ident)
        return True
    return False


def draw_modify(layout, context):
    """Max's Modify panel below the stack: parameters, UVW Map, Selection, Edit Geometry."""
    obj = context.active_object
    if obj is None:
        layout.label(text="Nothing selected")
        return
    if not has_command_panel():
        layout.prop(obj, "name", text="")
    if primitives.is_parametric(obj):
        box = layout.box()
        box.label(text="Parameters")
        primitives.draw_parameters(box, obj)
        if primitives.is_shape(obj):
            layout.operator("maximize.convert_spline", text="Convert to Editable Spline")
        layout.operator("maximize.convert_poly", text="Convert to Editable Poly")
    if obj.type == 'CURVE':
        from . import edit_spline
        box = layout.box()
        box.label(text="Edit Spline")
        edit_spline.draw(box, context, obj)
    if obj.type == 'CURVE' and not primitives.is_shape(obj):
        _draw_editable_spline(layout, context, obj)
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
            row = box.row(align=True)
            row.operator("maximize.make_planar", text="Make Planar")
            for axis in "XYZ":
                row.operator("maximize.make_planar_axis", text=axis).axis = axis
            box.prop(context.scene.tool_settings, "use_transform_correct_face_attributes", text="Preserve UVs")
            from .poly_tools import draw_extras
            draw_extras(box, context)
            _draw_poly_level(layout, context)


# Max's per-level Edit rollout: (label, operator, text) in Max's order.
_POLY_LEVEL_TOOLS = {
    'VERTEX': ("Edit Vertices", ("remove", "break_vertex", "extrude_max", "insert_vertex", "chamfer", "weld", "target_weld", "connect",
                                 "remove_isolated")),
    'EDGE': ("Edit Edges", ("insert_vertex", "remove", "split", "extrude_max", "chamfer", "weld", "target_weld", "bridge", "connect",
                            "create_shape", "turn", "hard", "smooth_edges")),
    'BORDER': ("Edit Borders", ("extrude_max", "insert_vertex", "cap", "bridge", "chamfer", "connect", "create_shape")),
    'POLYGON': ("Edit Polygons", ("bevel_poly", "inset", "outline", "bridge", "flip", "hinge_from_edge",
                                  "extrude_along_spline", "turn", "select_by_angle",
                                  "create_poly")),
    'ELEMENT': ("Edit Elements", ("flip", "create_poly")),
}


def _draw_poly_level(layout, context):
    from .selection import current_level
    level = current_level(context)
    if level not in _POLY_LEVEL_TOOLS:
        return
    label, ops = _POLY_LEVEL_TOOLS[level]
    box = layout.box()
    box.label(text=label)
    grid = box.grid_flow(columns=2, even_columns=True, align=True)
    for op in ops:
        if op == "bevel_poly":
            grid.operator("maximize." + op, text="Bevel", translate=False)
        else:
            grid.operator("maximize." + op)
    if level in {'VERTEX', 'EDGE'}:
        from .poly_tools import draw_edge_properties
        draw_edge_properties(box, level)
    overlay = getattr(context.space_data, "overlay", None)
    if level == 'EDGE' and overlay is not None:
        box.prop(overlay, "show_edge_sharp", text="Display Hard Edges")
    if level in {'POLYGON', 'ELEMENT'}:
        from .poly_tools import draw_material_ids
        box = layout.box()
        box.label(text="Material IDs")
        draw_material_ids(box, context)


def _draw_editable_spline(layout, context, obj):
    """Max's Editable Spline rollouts: Rendering, Interpolation, Selection, Geometry."""
    from . import spline_render
    from .spline_tools import spline_level
    box = layout.box()
    box.label(text="Rendering")
    spline_render.draw(box, obj)
    box = layout.box()
    box.label(text="Interpolation")
    col = box.column(align=True)
    col.prop(obj.data, "resolution_u", text="Steps")
    if hasattr(obj.data, "use_optimize"):
        col.prop(obj.data, "use_optimize", text="Optimize")
    box = layout.box()
    box.label(text="Selection")
    row = box.row(align=True)
    current = spline_level(context) if context.mode == 'EDIT_CURVE' else None
    for level, label in (('VERTEX', "Vertex"), ('EDGE', "Segment"), ('BORDER', "Spline")):
        row.operator("maximize.subobject", text=label,
                     depress=current == {'VERTEX': 'VERTEX', 'EDGE': 'SEGMENT', 'BORDER': 'SPLINE'}[level]).level = level
    if context.mode != 'EDIT_CURVE':
        return
    box = layout.box()
    box.label(text="Geometry")
    p = obj.data.maximize_shape
    row = box.row(align=True)
    row.prop(p, "auto_weld")
    sub = row.row(align=True)
    sub.active = p.auto_weld
    sub.prop(p, "weld_threshold", text="Threshold")
    box.menu("MAXIMIZE_MT_spline_vertex_type")
    grid = box.grid_flow(columns=2, even_columns=True, align=True)
    for idname, text in (("maximize.spline_reset_tangents", "Reset Tangents"),
                         ("maximize.spline_make_first", "Make First"), ("curve.switch_direction", "Reverse"),
                         ("maximize.spline_weld", "Weld"), ("maximize.spline_fuse", "Fuse"),
                         ("maximize.spline_cross_insert", "CrossInsert"),
                         ("curve.make_segment", "Connect"), ("maximize.spline_break", "Break"),
                         ("maximize.spline_divide", "Divide"), ("maximize.spline_detach", "Detach"),
                         ("maximize.spline_close", "Close"), ("maximize.spline_mirror", "Mirror"),
                         ("maximize.spline_explode", "Explode"), ("maximize.spline_fillet", "Fillet"),
                         ("maximize.spline_chamfer", "Chamfer"), ("maximize.spline_outline", "Outline"),
                         ("maximize.spline_trim", "Trim"), ("maximize.spline_extend", "Extend"),
                         ("maximize.spline_level_delete", "Delete")):
        grid.operator(idname, text=text)


class MaxPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Max"


class MAXIMIZE_PT_create(MaxPanel, Panel):
    bl_label = "Create"

    @classmethod
    def poll(cls, _context):
        # In Moritz this is the Command Panel's Create tab.
        return not has_command_panel()

    def draw(self, context):
        draw_object_types(self.layout, context, 'GEOMETRY')
        self.layout.separator()
        draw_object_types(self.layout, context, 'SHAPES')


class MAXIMIZE_PT_modify(MaxPanel, Panel):
    bl_label = "Modify"

    @classmethod
    def poll(cls, _context):
        # In Moritz this is in the Command Panel's Modify tab.
        return not has_command_panel()

    def draw(self, context):
        draw_modify(self.layout, context)


class MAXIMIZE_PT_command_modify(Panel):
    """Moritz: Max's Modify rollouts in the Command Panel's Modify tab, below the stack"""
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "modifier"
    bl_label = "Max"
    bl_order = 1

    @classmethod
    def poll(cls, context):
        return has_command_panel() and context.active_object is not None

    def draw(self, context):
        draw_modify(self.layout, context)


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
    MAXIMIZE_OT_create_in_viewport,
    MAXIMIZE_PT_create,
    MAXIMIZE_PT_modify,
    MAXIMIZE_PT_command_modify,
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
    if has_command_panel():
        bpy.types.PROPERTIES_PT_create.object_type_draw = draw_object_types


def unregister():
    global _icons
    if has_command_panel() and bpy.types.PROPERTIES_PT_create.object_type_draw is draw_object_types:
        bpy.types.PROPERTIES_PT_create.object_type_draw = None
    if getattr(bpy.types.VIEW3D_HT_header, "select_mode_draw", None) is draw_levels:
        bpy.types.VIEW3D_HT_header.select_mode_draw = None
    bpy.types.VIEW3D_MT_editor_menus.remove(_header_menu)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    bpy.utils.previews.remove(_icons)
    _icons = None
