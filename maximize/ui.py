# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""The Max menu in the 3D Viewport header and the Max command panel in the sidebar (stock Blender);
in Moritz, the Command Panel's tabs and the Max menu's entries in Blender's own menus."""

import os

import bpy
import bpy.utils.previews
from bpy.props import BoolProperty, StringProperty
from bpy.types import Menu, Operator, Panel

from . import compound, primitives, uvw_map, vocabulary
from .shapes import EXTENDED_SPLINES, SPLINES
from .nodes import draw_modifier_inputs
from .preferences import draw_keymap_switch
from .vocabulary import ALIASES
from .mx_icons import has_icon, mx_icon


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
        layout.operator("maximize.swift_loop")
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
# Moritz has no Max menu: nothing there reads as an add-on (Seb's rule). The Max menu's entries
# sit in Blender's own menus instead; Create and Shapes are in Add, the modifiers in Add Modifier,
# the keymap switch in Preferences.

# Menu -> entries: an operator, or ("menu", idname).
_MORITZ_ENTRIES = {
    "VIEW3D_MT_edit_mesh_vertices": ("maximize.chamfer", "maximize.connect"),
    "VIEW3D_MT_edit_mesh_edges": ("maximize.chamfer", "maximize.connect", "maximize.swift_loop"),
    "VIEW3D_MT_edit_mesh_delete": ("maximize.delete_subobject",),
    "VIEW3D_MT_transform_object": ("maximize.transform_typein", "maximize.affect_pivot_only",
                                   "maximize.center_pivot", "maximize.align_pivot_world"),
    "VIEW3D_MT_object_apply": ("maximize.reset_xform",),
    "VIEW3D_MT_object": ("maximize.align", "maximize.array", "maximize.spacing", "maximize.clone"),
    "VIEW3D_MT_select_object": ("maximize.select_by_name", ("menu", "MAXIMIZE_MT_selection_sets")),
    "VIEW3D_MT_select_edit_mesh": (("menu", "MAXIMIZE_MT_selection_sets"),),
    "VIEW3D_MT_view": ("maximize.viewport_maximize", "maximize.camera_from_view"),
    "TOPBAR_MT_render": ("maximize.render_setup", "maximize.material_editor"),
}

# The Max-named aliases the name scheme doesn't already give (Weld, Attach and the like are
# Blender's own entries renamed), in the menu of the operator they call. Only with Max names.
_MORITZ_ALIASES = {
    "VIEW3D_MT_edit_mesh_merge": ("target_weld", "collapse_sub"),
    "VIEW3D_MT_edit_mesh_vertices": ("break_vertex", "create_poly"),
    "VIEW3D_MT_edit_mesh_edges": ("paint_connect", "build_corner", "split", "turn", "hard", "smooth_edges"),
    "VIEW3D_MT_edit_mesh_faces": ("bevel_poly", "make_planar", "quadrify", "meshsmooth"),
    "VIEW3D_MT_select_edit_mesh": ("select_by_angle", "grow", "shrink", "loop", "ring", "similar",
                                   "select_outline", "select_fill", "select_nonquads", "select_open",
                                   "select_random", "select_mirror"),
}
_ALIAS_LABELS = {alias[0]: alias[1] for alias in ALIASES}


def _moritz_menu_draw(menu):
    entries = _MORITZ_ENTRIES.get(menu, ())
    aliases = _MORITZ_ALIASES.get(menu, ())

    def draw(self, context):
        layout = self.layout
        if entries:
            layout.separator()
            for entry in entries:
                if isinstance(entry, tuple):
                    layout.menu(entry[1])
                elif entry == "maximize.affect_pivot_only":
                    layout.operator(entry, depress=context.scene.tool_settings.use_transform_data_origin)
                else:
                    layout.operator(entry)
        if aliases and vocabulary.name_scheme(context) != 'BLENDER':
            layout.separator()
            for ident in aliases:
                layout.operator("maximize." + ident, text=_ALIAS_LABELS[ident], translate=False)
    return draw


_moritz_draws = {}


def _register_moritz_menus():
    for menu in sorted(set(_MORITZ_ENTRIES) | set(_MORITZ_ALIASES)):
        menu_type = getattr(bpy.types, menu, None)
        if menu_type is not None:
            _moritz_draws[menu] = _moritz_menu_draw(menu)
            menu_type.append(_moritz_draws[menu])


def _unregister_moritz_menus():
    for menu, draw in _moritz_draws.items():
        menu_type = getattr(bpy.types, menu, None)
        if menu_type is not None:
            menu_type.remove(draw)
    _moritz_draws.clear()


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
    plus: BoolProperty()

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
        if self.plus:
            props["plus"] = True
        with context.temp_override(area=area, region=region):
            op('INVOKE_DEFAULT', **props)
        return {'FINISHED'}


def _create_button(layout, operator, text, icon, kind="", plus=False):
    if has_command_panel():
        op = layout.operator("maximize.create_in_viewport", text=text, icon=icon)
        op.operator = operator
        op.kind = kind
        op.plus = plus
    elif kind:
        layout.operator(operator, text=text, icon=icon).kind = kind
    elif plus:
        layout.operator(operator, text=text, icon=icon).plus = True
    else:
        layout.operator(operator, text=text, icon=icon)


# The categories Maximize fills. Max's sub-categories (Standard / Extended Primitives, Compound
# Objects; Splines / Extended Splines) are not chosen from a dropdown: the Command Panel has room
# for all of them at once (Seb), in Max's order with a gap between the groups.
CATEGORIES = {'GEOMETRY', 'SHAPES'}


def _kind_buttons(grid, kinds):
    for ident in kinds:
        _create_button(grid, "maximize.add_primitive", primitives.kind_label(ident), _KIND_ICONS[ident], ident)


_KIND_ICONS = {kind[0]: kind[3] for kind in primitives.KINDS}


def draw_object_types(layout, context, category):
    """Moritz's Create tab hook: Max's parametric primitives and shapes."""
    if category not in CATEGORIES:
        return False
    wm = context.window_manager
    col = layout.column()
    col.enabled = context.mode == 'OBJECT'
    row = col.row()
    row.prop(context.scene, "maximize_autogrid")
    if category == 'SHAPES':
        row.prop(wm, "maximize_start_new_shape")

    def group():
        return col.grid_flow(row_major=True, columns=2, even_columns=True, align=True)

    if category == 'GEOMETRY':
        grid = group()
        for ident in primitives.STANDARD_PRIMITIVES:
            _kind_buttons(grid, (ident,))
            if ident == 'TEAPOT':
                # Blender's monkey beside Max's teapot (Seb).
                _create_button(grid, "maximize.add_suzanne", "Suzanne", 'MESH_MONKEY')
        _create_button(grid, "maximize.add_text", "TextPlus", 'OUTLINER_OB_FONT', plus=True)
        col.separator(factor=0.5)
        _kind_buttons(group(), primitives.EXTENDED_PRIMITIVES)
        col.separator(factor=0.5)
        # A single button: half the width, as in the grids above.
        _create_button(col.split(factor=0.5, align=True), "maximize.add_blobmesh", "BlobMesh", 'META_BALL')
    else:
        grid = group()
        _create_button(grid, "maximize.line", "Line", 'IPO_LINEAR')
        _kind_buttons(grid, SPLINES[:7])
        _create_button(grid, "maximize.add_text", "Text", 'OUTLINER_OB_FONT')
        _kind_buttons(grid, SPLINES[7:])
        _create_button(grid, "maximize.section_plane", "Section", 'MOD_BOOLEAN')
        _create_button(grid, "maximize.freehand", "Freehand", 'GREASEPENCIL')
        col.separator(factor=0.5)
        _kind_buttons(group(), EXTENDED_SPLINES)
    return True


# Modify panel tool buttons per row (Max's two are wider than needed in Blender's panel).
TOOL_COLUMNS = 4


class ToolGrid:
    """Tool buttons TOOL_COLUMNS to a row, in order. Use it like a layout, one call per button,
    then `pad()` so a short last row keeps the button width (Blender's grid flow drops columns
    when fewer rows would do)."""

    def __init__(self, layout):
        self._column = layout.column(align=True)
        self._row = None
        self._count = 0

    def _cell(self):
        if self._count % TOOL_COLUMNS == 0:
            self._row = self._column.row(align=True)
        self._count += 1
        return self._row

    def __getattr__(self, name):
        return getattr(self._cell(), name)

    def pad(self):
        while self._count % TOOL_COLUMNS:
            self._cell().label(text="")

    def wide(self):
        """A row of its own, the full width (a tool with a long name, as Max gives it)."""
        self.pad()
        return self._column.row(align=True)


# Moritz's Max icons for tool buttons, by operator (`maximize.` + key); stock Blender draws them without.
_TOOL_ICONS = {
    "grow": 'MX_MS_GROW', "shrink": 'MX_MS_SHRINK', "loop": 'MX_MS_LOOP', "ring": 'MX_MS_RING',
    "cut": 'MX_ED_CUT', "paint_connect": 'MX_ED_P_CONNECT', "swift_loop": 'MX_ED_SWIFT_LOOP',
    "quickslice": 'MX_ED_QSLICE', "relax": 'MX_GE_RELAX', "create_poly": 'MX_GE_CREATE',
    "meshsmooth": 'MX_SD_MESHSMOOTH', "tessellate": 'MX_SD_TESSELLATE',
    "hard": 'MX_PR_HARD', "smooth_edges": 'MX_PR_SMOOTH',
}


def tool_icon(op):
    """The icon of the tool button for `maximize.<op>`: its Max icon in Moritz, else none."""
    return mx_icon(_TOOL_ICONS.get(op, 'NONE'))


def rollout(layout, idname, label, closed=False):
    """A Max rollout: a collapsible section; returns its body, or None while it is closed."""
    header, body = layout.panel(idname, default_closed=closed)
    header.label(text=label)
    return body


def draw_poly_selection(layout, context):
    """Edit Poly's Selection rollout: the five levels, Grow / Shrink, Loop / Ring."""
    from .selection import current_level
    current = current_level(context) if context.mode == 'EDIT_MESH' else None
    row = layout.row(align=True)
    for level in ('VERTEX', 'EDGE', 'BORDER', 'POLYGON', 'ELEMENT'):
        row.operator("maximize.subobject", text="", depress=current == level, **level_icon(level)).level = level
    if context.mode == 'EDIT_MESH':
        # Row by row, keeping Max's pairs together: Grow / Shrink, Loop / Ring, Dot Loop / Dot Ring.
        grid = ToolGrid(layout)
        for op in ("grow", "shrink", "loop", "ring"):
            grid.operator("maximize." + op, icon=tool_icon(op))
        grid.operator("maximize.dot_loop", text="Dot Loop").ring = False
        grid.operator("maximize.dot_loop", text="Dot Ring").ring = True
        for op in ("similar", "select_fill", "select_outline"):
            grid.operator("maximize." + op)
        # Max's ribbon: one step at a time along loops and rings, and Random Loops.
        for text, action, ring in (("Grow Loop", 'GROW', False), ("Shrink Loop", 'SHRINK', False),
                                   ("Grow Ring", 'GROW', True), ("Shrink Ring", 'SHRINK', True)):
            props = grid.operator("maximize.step_loop", text=text)
            props.action, props.ring = action, ring
        grid.operator("maximize.random_loops")
        grid.pad()
        # Loop / Ring mode: a click picks the whole loop or ring.
        layout.row(align=True).prop(context.window_manager, "maximize_click_mode", expand=True)
        header, body = layout.panel("maximize_poly_select_by", default_closed=True)
        header.label(text="Select By")
        if body:
            grid = ToolGrid(body)
            for op in ("select_nonquads", "select_open", "select_random", "select_mirror"):
                grid.operator("maximize." + op)
            for side in ('TOP', 'BOTTOM', 'LEFT', 'RIGHT'):
                grid.operator("maximize.select_side", text=side.title()).side = side
            for op in ("select_half", "select_perspective", "select_by_view", "select_pivot_distance",
                       "select_numeric"):
                grid.operator("maximize." + op)
            grid.pad()


def draw_poly_geometry(layout, context):
    """Edit Poly's Edit Geometry rollout (Edit Mode)."""
    grid = ToolGrid(layout)
    grid.operator("mesh.extrude_context_move", text="Extrude")
    for op in ("bevel_poly", "chamfer", "inset", "connect", "cut", "paint_connect", "swift_loop", "weld",
               "target_weld", "collapse_sub", "bridge", "cap", "remove", "detach", "quickslice",
               "relax"):
        if op == "bevel_poly":
            # The Max vocabulary renames Blender's Bevel to Chamfer: keep Max's Bevel.
            grid.operator("maximize." + op, text="Bevel", translate=False)
        elif op == "swift_loop":
            # Pressed while the mode runs, as in Max.
            from .poly_tools import MAXIMIZE_OT_swift_loop
            grid.operator("maximize." + op, icon=tool_icon(op), depress=MAXIMIZE_OT_swift_loop.running)
        else:
            grid.operator("maximize." + op, icon=tool_icon(op))
    grid.pad()
    row = layout.row(align=True)
    row.operator("maximize.make_planar", text="Make Planar", icon=mx_icon('MX_AL_MAKE_PLANAR'))
    for axis in "XYZ":
        row.operator("maximize.make_planar_axis", text=axis).axis = axis
    row = layout.row(align=True)
    row.operator("maximize.align_to", text="To View", icon=mx_icon('MX_AL_TO_VIEW')).target = 'VIEW'
    row.operator("maximize.align_to", text="To Grid", icon=mx_icon('MX_AL_TO_GRID')).target = 'GRID'
    layout.prop(context.scene.tool_settings, "use_transform_correct_face_attributes", text="Preserve UVs",
                icon=mx_icon('MX_PM_PRESERVE_UVS'))
    # Max's Edit Mesh Show Normals and Scale, for the main viewport (the panel is in the Command Panel).
    from .vocabulary import view3d_override
    view = view3d_override(context)
    overlay = view["area"].spaces.active.overlay if view else None
    if overlay is not None:
        row = layout.row(align=True)
        row.prop(overlay, "show_face_normals", text="Show Normals")
        sub = row.row(align=True)
        sub.active = overlay.show_face_normals
        sub.prop(overlay, "normals_length", text="Scale")
    from .poly_tools import draw_extras
    draw_extras(layout, context)
    # Max's ribbon Geometry (All) and Subdivision, used less: closed sub-sections.
    for idname, label, ops in (("maximize_poly_geometry_all", "Geometry (All)",
                                ("quadrify_all", "quadrify", "symmetrize", "explode")),
                               ("maximize_poly_subdivision", "Subdivision", ("meshsmooth", "tessellate"))):
        header, body = layout.panel(idname, default_closed=True)
        header.label(text=label)
        if body:
            grid = ToolGrid(body)
            for op in ops:
                grid.operator("maximize." + op, icon=tool_icon(op))
            grid.pad()
            if idname == "maximize_poly_geometry_all":
                # Max's ribbon Modify Mode: up and down the modifier stack.
                row = body.row(align=True)
                row.operator("maximize.modifier_step", text="Previous Modifier", icon='TRIA_DOWN').direction = 'PREVIOUS'
                row.operator("maximize.modifier_step", text="Next Modifier", icon='TRIA_UP').direction = 'NEXT'
            else:
                body.operator_menu_enum("maximize.generate_topology", "pattern", text="Generate Topology")


# Max's per-level Edit rollout: (label, operator, text) in Max's order.
_POLY_LEVEL_TOOLS = {
    'VERTEX': ("Edit Vertices", ("remove", "break_vertex", "extrude_max", "insert_vertex", "chamfer", "weld", "target_weld", "connect",
                                 "remove_isolated")),
    'EDGE': ("Edit Edges", ("insert_vertex", "remove", "split", "extrude_max", "chamfer", "weld", "target_weld", "bridge", "connect",
                            "create_shape", "turn", "hard", "smooth_edges")),
    'BORDER': ("Edit Borders", ("extrude_max", "insert_vertex", "cap", "bridge", "chamfer", "connect", "create_shape")),
    'POLYGON': ("Edit Polygons", ("smart_extrude", "bevel_poly", "inset", "outline", "bridge", "flip", "turn",
                                  "select_by_angle", "create_poly", "geopoly", "hinge_from_edge",
                                  "extrude_along_spline")),
    'ELEMENT': ("Edit Elements", ("flip", "create_poly")),
}


# Tools whose names don't fit a quarter of the panel: a full row each, at the end of their rollout.
_WIDE_TOOLS = {"hinge_from_edge", "extrude_along_spline"}


def draw_soft_selection(layout, context):
    """Max's Soft Selection rollout: Blender's proportional editing, in Max's words."""
    ts = context.scene.tool_settings
    layout.prop(ts, "use_proportional_edit", text="Use Soft Selection")
    col = layout.column()
    col.active = ts.use_proportional_edit
    col.prop(ts, "use_proportional_connected", text="Edge Distance")
    col.prop(ts, "use_proportional_projected", text="Projected (2D)")
    col.prop(ts, "proportional_size", text="Falloff")
    col.prop(ts, "proportional_edit_falloff", text="Curve")


def draw_poly_rollouts(layout, context, key):
    """Edit Poly's rollouts, also Editable Poly's at the base (one code for both, as in Max):
    Selection, Soft Selection, Edit Geometry, and in Edit Mode the level's Edit rollout, Loops,
    Material IDs and Smoothing Groups. `key` keeps their open state apart."""
    body = rollout(layout, key + "_selection", "Selection")
    if body:
        draw_poly_selection(body, context)
    body = rollout(layout, key + "_soft_selection", "Soft Selection", closed=True)
    if body:
        draw_soft_selection(body, context)
    body = rollout(layout, key + "_geometry", "Edit Geometry")
    if body:
        if context.mode == 'EDIT_MESH':
            draw_poly_geometry(body, context)
        else:
            # Max's object level: Attach works on whole objects; the sub-object tools wait for a
            # level (1-5), greyed out as in Max.
            body.operator("maximize.attach", icon=tool_icon("attach"))
            col = body.column()
            col.enabled = False
            grid = ToolGrid(col)
            grid.operator("mesh.extrude_context_move", text="Extrude")
            for op in ("chamfer", "inset", "connect", "cut", "swift_loop", "weld", "bridge", "cap",
                       "remove", "detach", "quickslice", "relax"):
                grid.operator("maximize." + op, icon=tool_icon(op))
            grid.pad()
    if context.mode == 'EDIT_MESH':
        _draw_poly_level_rollouts(layout, context, key)
    # Last, as in Max.
    body = rollout(layout, key + "_paint_deform", "Paint Deform", closed=True)
    if body:
        from .paint_deform import draw as draw_paint_deform
        draw_paint_deform(body, context)


def _draw_poly_level_rollouts(layout, context, key):
    """Edit Mode: the level's Edit rollout, Loops, Material IDs and Smoothing Groups."""
    from .selection import current_level
    level = current_level(context)
    if level not in _POLY_LEVEL_TOOLS:
        return
    label, ops = _POLY_LEVEL_TOOLS[level]
    header, body = layout.panel(key + "_level", default_closed=False)
    header.label(text=label)
    # Max's caddy "Apply and Continue": run the last tool again with the same settings.
    header.operator("screen.repeat_last", text="", icon=mx_icon('MX_ED_REPEAT_LAST', 'ADD'))
    if body:
        grid = ToolGrid(body)
        from .caddy import tool_button
        for op in ops:
            if op == "bevel_poly":
                tool_button(grid, context, "maximize." + op, text="Bevel", translate=False)
            elif op in _WIDE_TOOLS:
                tool_button(grid.wide(), context, "maximize." + op)
            else:
                tool_button(grid, context, "maximize." + op, icon=tool_icon(op))
        grid.pad()
        if level in {'VERTEX', 'EDGE'}:
            from .poly_tools import draw_edge_properties
            draw_edge_properties(body, level)
        overlay = getattr(context.space_data, "overlay", None)
        if level == 'EDGE' and overlay is not None:
            body.prop(overlay, "show_edge_sharp", text="Display Hard Edges")
    if level in {'VERTEX', 'EDGE'}:
        # Max's ribbon Loops tools (Build End picks two vertices).
        body = rollout(layout, key + "_loops", "Loops")
        if body:
            grid = ToolGrid(body)
            for op in ("insert_loop", "remove_loop", "set_flow", "build_end", "build_corner", "distribute",
                       "center_loop", "loop_straighten", "loop_circle", "loop_curve"):
                grid.operator("maximize." + op)
            grid.pad()
    if level in {'POLYGON', 'ELEMENT'}:
        body = rollout(layout, key + "_material_ids", "Material IDs")
        if body:
            from .poly_tools import draw_material_ids
            draw_material_ids(body, context)
        body = rollout(layout, key + "_smoothing", "Smoothing Groups", closed=True)
        if body:
            from .smoothing import draw_smoothing_groups
            draw_smoothing_groups(body, context)


def draw_spline_selection(layout, context):
    from .spline_tools import spline_level
    row = layout.row(align=True)
    current = spline_level(context) if context.mode == 'EDIT_CURVE' else None
    for level, label in (('VERTEX', "Vertex"), ('EDGE', "Segment"), ('BORDER', "Spline")):
        # Max's icon buttons where Moritz has the icons, else the names.
        icon = 'MX_SPLINE_' + label.upper()
        kwargs = {"text": "", "icon": icon} if has_icon(icon) else {"text": label}
        row.operator("maximize.subobject", **kwargs,
                     depress=current == {'VERTEX': 'VERTEX', 'EDGE': 'SEGMENT', 'BORDER': 'SPLINE'}[level]).level = level


def draw_spline_geometry(layout, context, obj):
    p = obj.data.maximize_shape
    row = layout.row(align=True)
    row.prop(p, "auto_weld")
    sub = row.row(align=True)
    sub.active = p.auto_weld
    sub.prop(p, "weld_threshold", text="Threshold")
    layout.menu("MAXIMIZE_MT_spline_vertex_type")
    grid = ToolGrid(layout)
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
    grid.pad()
    from .spline_more import draw_geometry_extras
    draw_geometry_extras(layout, context, obj)


def draw_spline_rollouts(layout, context, obj, key, base):
    """Editable Spline's rollouts; the Edit Spline modifier has Selection and Geometry only
    (`base` False), the base also Rendering and Interpolation."""
    if base:
        body = rollout(layout, key + "_rendering", "Rendering")
        if body:
            from . import spline_render
            spline_render.draw(body, obj)
        body = rollout(layout, key + "_interpolation", "Interpolation")
        if body:
            col = body.column(align=True)
            col.prop(obj.data, "resolution_u", text="Steps")
            if hasattr(obj.data, "use_optimize"):
                col.prop(obj.data, "use_optimize", text="Optimize")
            col.prop(obj.data.maximize_shape, "adaptive")
    body = rollout(layout, key + "_selection", "Selection")
    if body:
        draw_spline_selection(body, context)
    if context.mode == 'EDIT_CURVE':
        body = rollout(layout, key + "_geometry", "Geometry")
        if body:
            draw_spline_geometry(body, context, obj)


def draw_base(layout, context):
    """Moritz's Modify tab hook: the base object's settings, when the base is selected in the stack
    (Max's Editable Poly / Editable Spline / primitive parameters)."""
    obj = context.object
    from . import sculpt
    if sculpt.active_sculpt(obj) is None:
        # Sculpting the base mesh without a Sculpt modifier.
        sculpt.draw(layout, context, obj)
    if obj.get("maximize_section"):
        body = rollout(layout, "mx_base_section", "Section Parameters")
        if body:
            body.operator("maximize.section_create_shape")
    if primitives.is_parametric(obj):
        body = rollout(layout, "mx_base_parameters", "Parameters")
        if body:
            primitives.draw_parameters(body, obj)
            if compound.is_blobmesh(obj):
                compound.draw_blob_objects(body, obj)
        if primitives.is_shape(obj):
            layout.operator("maximize.convert_spline", text="Convert to Editable Spline")
        layout.operator("maximize.convert_poly", text="Convert to Editable Poly")
    elif obj.type == 'MESH':
        draw_poly_rollouts(layout, context, "mx_base_poly")
    elif obj.type == 'CURVE':
        draw_spline_rollouts(layout, context, obj, "mx_base_spline", base=True)


def draw_modify(layout, context):
    """The Max sidebar tab's Modify panel (Blender without Moritz's Command Panel): the base
    object's settings, the Edit Spline and UVW Map modifiers, and the Modifier List."""
    obj = context.active_object
    if obj is None:
        layout.label(text="Nothing selected")
        return
    layout.prop(obj, "name", text="")
    from . import sculpt
    if sculpt.active_sculpt(obj) is not None:
        sculpt.draw(layout, context, obj)
    if obj.type == 'CURVE':
        from . import edit_spline
        body = rollout(layout, "mx_edit_spline", "Edit Spline")
        if body:
            edit_spline.draw(body, context, obj)
    mod = uvw_map.uvw_modifier(obj)
    if mod is not None:
        body = rollout(layout, "mx_uvw_map", "UVW Map")
        if body:
            draw_modifier_inputs(body, mod)
    row = layout.row(align=True)
    row.operator_menu_enum("object.modifier_add", "type", text="Modifier List")
    row.menu("MAXIMIZE_MT_modify", text="", icon='DOWNARROW_HLT')
    draw_base(layout, context)


class MaxPanel:
    """The sidebar's Max tab: stock Blender only, Moritz has the Command Panel instead."""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Max"

    @classmethod
    def poll(cls, _context):
        return not has_command_panel()


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


class _ModifierRollouts:
    """Moritz: Maximize's rollouts inside a modifier's own panel in the Modify tab (a header-less
    subpanel of Blender's modifier panel; `custom_data` is the modifier)."""
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "modifier"
    bl_label = ""
    bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        return has_command_panel() and context.object is not None


class MAXIMIZE_PT_edit_poly_rollouts(_ModifierRollouts, Panel):
    bl_parent_id = "MOD_PT_EditPoly"

    def draw(self, context):
        from . import sculpt
        obj = context.object
        mod = self.custom_data
        if sculpt.is_midstack(obj, mod):
            # Maximize's mid-stack Sculpt is an Edit Poly underneath: its rollout only.
            sculpt.draw(self.layout, context, obj, mod)
            return
        # Max's Edit Poly Mode rollout comes first, with Show Cage.
        from .edit_poly import draw_show_cage
        draw_show_cage(self.layout, obj, mod)
        draw_poly_rollouts(self.layout, context, "mx_edit_poly")


class MAXIMIZE_PT_edit_spline_rollouts(_ModifierRollouts, Panel):
    bl_parent_id = "MOD_PT_EditSpline"

    def draw(self, context):
        from . import edit_spline
        obj = context.object
        edit_spline.draw(self.layout, context, obj)
        if obj.type == 'CURVE':
            draw_spline_rollouts(self.layout, context, obj, "mx_edit_spline", base=False)


class MAXIMIZE_PT_sculpt_rollout(_ModifierRollouts, Panel):
    bl_parent_id = "MOD_PT_Multires"

    def draw(self, context):
        from . import sculpt
        obj = context.object
        mod = self.custom_data
        if sculpt.is_sculpt(obj, mod):
            sculpt.draw(self.layout, context, obj, mod)


class MAXIMIZE_PT_freeform_rollout(_ModifierRollouts, Panel):
    bl_parent_id = "MOD_PT_GeometryNodes"

    def draw(self, context):
        from . import freeform
        mod = self.custom_data
        if mod is not None and mod == freeform.freeform_modifier(context.object):
            freeform.draw(self.layout, context, context.object, mod)


class MAXIMIZE_PT_vertex_paint_rollout(_ModifierRollouts, Panel):
    bl_parent_id = "MOD_PT_VertexPaint"

    def draw(self, context):
        from . import vertex_paint
        vertex_paint.draw(self.layout, context, self.custom_data)


class _CreateRollouts:
    """Moritz's Create tab, below Name and Color: the object just created, as in Max, until another
    object is picked."""
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "create"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (has_command_panel() and context.mode == 'OBJECT' and obj is not None and
                obj.name == context.window_manager.maximize_created and primitives.is_parametric(obj))


class MAXIMIZE_PT_create_keyboard_entry(_CreateRollouts, Panel):
    bl_label = "Keyboard Entry"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, _context):
        self.layout.operator("maximize.keyboard_entry", icon='KEYINGSET')


class MAXIMIZE_PT_create_parameters(_CreateRollouts, Panel):
    bl_label = "Parameters"

    def draw(self, context):
        obj = context.active_object
        primitives.draw_parameters(self.layout, obj)
        if compound.is_blobmesh(obj):
            compound.draw_blob_objects(self.layout, obj)


# Parent panels that exist only in Moritz (or in every Blender, for Multires and Geometry Nodes).
_MODIFIER_ROLLOUTS = (
    MAXIMIZE_PT_edit_poly_rollouts,
    MAXIMIZE_PT_edit_spline_rollouts,
    MAXIMIZE_PT_sculpt_rollout,
    MAXIMIZE_PT_freeform_rollout,
    MAXIMIZE_PT_vertex_paint_rollout,
)


def draw_utilities(layout, context):
    """The Utilities tab: Align with the pivot tools, Array, Spacing Tool and Object Paint (Moritz's
    Command Panel tab, or the sidebar's Max tab in Blender)."""
    body = rollout(layout, "mx_util_align", "Align")
    if body:
        col = body.column(align=True)
        col.operator("maximize.align", text="Align")
        col.operator("maximize.align_pivot_world")
        col.operator("maximize.center_pivot")
        col.operator("maximize.affect_pivot_only", depress=context.scene.tool_settings.use_transform_data_origin)
    body = rollout(layout, "mx_util_objects", "Array and Spacing")
    if body:
        row = body.row(align=True)
        row.operator("maximize.array", text="Array")
        row.operator("maximize.spacing", text="Spacing Tool")
    body = rollout(layout, "mx_util_object_paint", "Object Paint", closed=True)
    if body:
        from .object_paint import draw as draw_object_paint
        draw_object_paint(body, context)


class MAXIMIZE_PT_utilities(MaxPanel, Panel):
    bl_label = "Utilities"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, _context):
        # In Moritz this is the Command Panel's Utilities tab.
        return not hasattr(bpy.types, "PROPERTIES_PT_utilities")

    def draw(self, context):
        draw_utilities(self.layout, context)
        # In Blender the Max tab also gathers what Moritz has elsewhere (quad menu, F12, keys).
        col = self.layout.column(align=True)
        col.separator()
        col.operator("maximize.transform_typein", text="Transform Type-In")
        col.operator("maximize.clone", text="Clone")
        col.operator("maximize.reset_xform")
        col.operator("maximize.uvw_map", text="UVW Map")
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
    MAXIMIZE_PT_create_keyboard_entry,
    MAXIMIZE_PT_create_parameters,
    MAXIMIZE_PT_modify,
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


def _draw_add_menu(self, _context):
    """Moritz's Add Modifier menu: Maximize's own modifiers and the Max names (Modifier List)."""
    if vocabulary.modifier_list() is not None:
        # Moritz lists them itself, by name scheme (`register` adds the entries).
        return
    layout = self.layout
    layout.separator()
    layout.operator("maximize.uvw_map", text="UVW Map")
    _aliases(layout, 'MODIFY')


def register():
    _load_icons()
    for cls in classes:
        bpy.utils.register_class(cls)
    # Rollouts inside the modifiers' own panels, where the parent panel exists (Blender's modifier
    # panels are not in bpy.types: registering fails without the parent).
    for cls in _MODIFIER_ROLLOUTS:
        try:
            bpy.utils.register_class(cls)
        except RuntimeError:
            pass
    if hasattr(bpy.types.DATA_PT_modifiers, "moritz_base_draw"):
        bpy.types.DATA_PT_modifiers.moritz_base_draw = draw_base
        bpy.types.DATA_PT_modifiers.moritz_base_entry = primitives.base_entry
    if hasattr(bpy.types, "OBJECT_MT_modifier_add_flat"):
        bpy.types.OBJECT_MT_modifier_add_flat.append(_draw_add_menu)
    mlist = vocabulary.modifier_list()
    if mlist is not None:
        mlist.register_entry("UVW Map", "maximize.uvw_map", "uv mapping planar box cylindrical spherical gizmo")
    if has_command_panel():
        _register_moritz_menus()
    else:
        bpy.types.VIEW3D_MT_editor_menus.append(_header_menu)
    # Moritz only: Blender's header has no hook.
    if hasattr(bpy.types.VIEW3D_HT_header, "select_mode_draw"):
        bpy.types.VIEW3D_HT_header.select_mode_draw = draw_levels
    wm = bpy.types.WindowManager
    # The same ID property the AutoGrid toggle (`maximize.autogrid`) flips.
    bpy.types.Scene.maximize_autogrid = BoolProperty(
        name="AutoGrid", description="Create objects on the surface under the mouse")
    # The object the Create tab shows Parameters for: the last one created.
    wm.maximize_created = StringProperty(options={'SKIP_SAVE'})
    wm.maximize_start_new_shape = BoolProperty(
        name="Start New Shape", default=True,
        description="Off: new lines are added as splines to the selected shape")
    if has_command_panel():
        bpy.types.PROPERTIES_PT_create.object_type_draw = draw_object_types
    if hasattr(bpy.types, "PROPERTIES_PT_utilities"):
        # Moritz's Command Panel Utilities tab.
        bpy.types.PROPERTIES_PT_utilities.utilities_draw = draw_utilities


def unregister():
    global _icons
    if has_command_panel() and bpy.types.PROPERTIES_PT_create.object_type_draw is draw_object_types:
        bpy.types.PROPERTIES_PT_create.object_type_draw = None
    if getattr(getattr(bpy.types, "PROPERTIES_PT_utilities", None), "utilities_draw", None) is draw_utilities:
        bpy.types.PROPERTIES_PT_utilities.utilities_draw = None
    del bpy.types.WindowManager.maximize_start_new_shape
    del bpy.types.WindowManager.maximize_created
    del bpy.types.Scene.maximize_autogrid
    if getattr(bpy.types.VIEW3D_HT_header, "select_mode_draw", None) is draw_levels:
        bpy.types.VIEW3D_HT_header.select_mode_draw = None
    _unregister_moritz_menus()
    bpy.types.VIEW3D_MT_editor_menus.remove(_header_menu)
    if hasattr(bpy.types, "OBJECT_MT_modifier_add_flat"):
        bpy.types.OBJECT_MT_modifier_add_flat.remove(_draw_add_menu)
    mlist = vocabulary.modifier_list()
    if mlist is not None:
        mlist.unregister_entry("maximize.uvw_map")
    if getattr(bpy.types.DATA_PT_modifiers, "moritz_base_draw", None) is draw_base:
        bpy.types.DATA_PT_modifiers.moritz_base_draw = None
        bpy.types.DATA_PT_modifiers.moritz_base_entry = None
    for cls in reversed(_MODIFIER_ROLLOUTS):
        if cls.is_registered:
            bpy.utils.unregister_class(cls)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    bpy.utils.previews.remove(_icons)
    _icons = None
