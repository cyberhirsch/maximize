# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Max quad menu on right-click: four quadrants (Display, Viewport, Tools, Transform), per mode.

Max 2026's look: flat text rows without icons, thin lines between groups, the text facing the
cursor (right-aligned on the left, left-aligned on the right), a settings square at the outer edge
for tools with a caddy, a checkmark on the current sub-object level, submenus for longer lists.

It is a popover laid out as a 2x2 grid whose quadrants meet at the mouse, as in Max: the top
quadrants end at the cursor line and the bottom ones start there. Blender opens a popover with
its selected button under the mouse, so an invisible, always-on toggle in the middle row anchors
the grid's center to the cursor.
"""

import bpy
from bpy.props import BoolProperty
from bpy.types import Menu, Panel

# Quadrant entries: ("op", idname, text, props, options), ("menu", idname, text), ("gap",), ("sep",)
# for a thin line between groups, and ("ops", [(idname, text, props), ...]) for a row of small
# buttons. Rows and lines are padded per pair of quadrants, so they line up at the cursor.
# options: "settings" adds the caddy's settings square; other keys go to `layout.operator`.
SEP = ("sep",)


def _tool(text, tool):
    return ("op", "wm.tool_set_by_id", text, {"name": tool}, {})


def _settings():
    return {"settings": True}


def _state(on):
    # A checkbox icon instead of a pressed-in button: the popover anchors on pressed-in buttons.
    return {"icon": 'CHECKBOX_HLT' if on else 'CHECKBOX_DEHLT'}


def _toggle(text, data_path, on):
    return ("op", "wm.context_toggle", text, {"data_path": data_path}, _state(on))


def _transform(context):
    items = [
        _tool("Move", "builtin.move"),
        _tool("Rotate", "builtin.rotate"),
        _tool("Scale", "builtin.scale"),
        _tool("Select", "builtin.select_box"),
        SEP,
        ("op", "maximize.transform_typein", "Transform Type-In...", {}, {}),
    ]
    if context.mode == 'OBJECT':
        items += [
            ("op", "maximize.clone", "Clone...", {}, {}),
            SEP,
            ("op", "maximize.affect_pivot_only", "Affect Pivot Only", {},
             _state(context.scene.tool_settings.use_transform_data_origin)),
            ("op", "maximize.reset_xform", "Reset XForm", {}, {}),
            ("op", "maximize.open_editor", "Curve Editor...", {"ui_type": 'FCURVES'}, {}),
            ("op", "maximize.open_editor", "Object Properties...", {"ui_type": 'PROPERTIES'}, {}),
        ]
    return items


def _display(context):
    items = [("op", "view3d.localview", "Isolate Selection", {}, {}), SEP]
    if context.mode == 'EDIT_MESH':
        items += [
            ("op", "mesh.hide", "Hide Selection", {"unselected": False}, {}),
            ("op", "mesh.hide", "Hide Unselected", {"unselected": True}, {}),
            ("op", "mesh.reveal", "Unhide All", {}, {}),
        ]
    else:
        items += [
            ("op", "object.hide_view_set", "Hide Selection", {"unselected": False}, {}),
            ("op", "object.hide_view_set", "Hide Unselected", {"unselected": True}, {}),
            ("op", "object.hide_view_clear", "Unhide All", {}, {}),
            SEP,
            ("op", "maximize.freeze", "Freeze Selection", {"freeze": True}, {}),
            ("op", "maximize.freeze", "Unfreeze All", {"freeze": False}, {}),
            ("op", "maximize.select_by_name", "Select by Name...", {}, {}),
        ]
    return items


def _viewport(context):
    space = context.space_data
    return [
        ("op", "wm.context_toggle_enum", "Wireframe / Shaded",
         {"data_path": "space_data.shading.type", "value_1": 'WIREFRAME', "value_2": 'SOLID'},
         _state(space.shading.type == 'WIREFRAME')),
        _toggle("Edged Faces", "space_data.overlay.show_wireframes", space.overlay.show_wireframes),
        ("op", "maximize.see_through_objects", "See-Through", {},
         _state(getattr(context.active_object, "show_see_through", space.shading.show_xray))),
        _toggle("Grid", "space_data.overlay.show_floor", space.overlay.show_floor),
        _toggle("Statistics", "space_data.overlay.show_stats", space.overlay.show_stats),
        SEP,
        ("op", "maximize.viewport_maximize", "Maximize Viewport Toggle", {}, {}),
    ]


def _tools_object(context):
    obj = context.active_object
    if obj is not None and obj.type == 'CURVE':
        first = [("op", "maximize.edit_spline_add", "Edit Spline Modifier", {}, {})]
    else:
        first = [("op", "maximize.edit_poly_add", "Edit Poly Modifier", {}, {})]
    return first + [
        ("menu", "MAXIMIZE_MT_quad_convert", "Convert To"),
        ("op", "maximize.attach", "Attach", {}, {}),
        ("op", "maximize.collapse_all", "Collapse All", {}, {}),
        SEP,
        ("op", "maximize.align", "Align", {}, {}),
        ("op", "maximize.array", "Array...", {}, {}),
        ("op", "maximize.spacing", "Spacing Tool...", {}, {}),
        ("op", "maximize.uvw_map", "UVW Map", {}, {}),
        SEP,
        ("menu", "MAXIMIZE_MT_selection_sets", "Named Selection Sets"),
        ("menu", "MAXIMIZE_MT_create", "Create"),
        ("menu", "MAXIMIZE_MT_create_shapes", "Shapes"),
    ]


def _tools_poly(_context):
    levels = (('VERTEX', "Vert"), ('EDGE', "Edge"), ('BORDER', "Bord"), ('POLYGON', "Poly"),
              ('ELEMENT', "Elem"), ('OBJECT', "Top"))
    return [
        ("ops", [("maximize.subobject", label, {"level": level}) for level, label in levels]),
        SEP,
        ("op", "mesh.extrude_context_move", "Extrude", {}, _settings()),
        # Untranslated: the Max vocabulary renames Blender's Bevel to Chamfer.
        ("op", "maximize.bevel_poly", "Bevel", {}, {"translate": False, "settings": True}),
        ("op", "maximize.chamfer", "Chamfer", {}, _settings()),
        ("op", "maximize.inset", "Inset", {}, _settings()),
        SEP,
        ("op", "maximize.cut", "Cut", {}, {}),
        ("op", "maximize.swift_loop", "Swift Loop", {}, {}),
        ("op", "maximize.connect", "Connect", {}, _settings()),
        SEP,
        ("op", "maximize.weld", "Weld", {}, _settings()),
        ("op", "maximize.target_weld", "Target Weld", {}, {}),
        ("op", "maximize.collapse_sub", "Collapse", {}, {}),
        ("op", "maximize.bridge", "Bridge", {}, _settings()),
        ("op", "maximize.cap", "Cap", {}, {}),
        ("op", "maximize.remove", "Remove", {}, {}),
        ("op", "maximize.detach", "Detach", {}, {}),
    ]


def _tools_spline(_context):
    """Max's Editable Spline quad: vertex types first, as in Max's tools1 quadrant."""
    types = [("maximize.spline_vertex_type", label, {"type": ident})
             for ident, label in (('CORNER', "Corner"), ('SMOOTH', "Smooth"))]
    beziers = [("maximize.spline_vertex_type", label, {"type": ident})
               for ident, label in (('BEZIER', "Bezier"), ('BEZIER_CORNER', "Bez Corner"))]
    levels = (('VERTEX', "Vert"), ('EDGE', "Seg"), ('BORDER', "Spline"), ('OBJECT', "Top"))
    return [
        ("ops", [("maximize.subobject", label, {"level": level}) for level, label in levels]),
        SEP,
        ("ops", types),
        ("ops", beziers),
        ("op", "maximize.spline_reset_tangents", "Reset Tangents", {}, {}),
        ("op", "maximize.spline_make_first", "Make First", {}, {}),
        ("op", "curve.switch_direction", "Reverse", {}, {}),
        SEP,
        ("ops", [("maximize.spline_weld", "Weld", {}), ("maximize.spline_fuse", "Fuse", {})]),
        ("ops", [("maximize.spline_divide", "Divide", {}), ("maximize.spline_detach", "Detach", {})]),
        ("ops", [("maximize.spline_close", "Close", {}), ("maximize.spline_explode", "Explode", {})]),
        ("op", "maximize.spline_mirror", "Mirror", {}, {}),
        ("op", "maximize.spline_fillet", "Fillet", {}, {}),
        ("op", "maximize.spline_chamfer", "Chamfer", {}, {}),
        ("op", "maximize.spline_outline", "Outline", {}, {}),
        ("op", "maximize.spline_break", "Break", {}, {}),
        ("op", "curve.make_segment", "Connect", {}, {}),
    ]


def _current_level(context):
    if context.mode == 'EDIT_CURVE':
        from .spline_tools import spline_level
        # The quad's spline buttons use the poly levels' names.
        return {'SEGMENT': 'EDGE', 'SPLINE': 'BORDER'}.get(spline_level(context), 'VERTEX')
    from .selection import current_level
    return current_level(context)


def _row(col, left):
    """A row whose text faces the cursor: right-aligned in the left quadrants."""
    row = col.row(align=True)
    row.alignment = 'RIGHT' if left else 'LEFT'
    return row


def _draw_entries(col, context, entries, left):
    from . import caddy
    caddy_on = caddy.use_caddy(context)
    level = _current_level(context)
    for entry in entries:
        kind = entry[0]
        if kind == "gap":
            col.label(text="")
        elif kind == "sep":
            col.separator(type='LINE')
        elif kind == "menu":
            _row(col, left).menu(entry[1], text=entry[2])
        elif kind == "ops":
            row = _row(col, left)
            for idname, text, props in entry[1]:
                # The current level is framed: a checkmark would squeeze the short labels, and a
                # pressed-in button would move the popover's anchor.
                op = row.operator(idname, text=text, emboss=props.get("level") == level)
                for key, value in props.items():
                    setattr(op, key, value)
        else:
            _kind, idname, text, props, options = entry
            options = dict(options)
            settings = options.pop("settings", False) and caddy_on and caddy.has_settings(idname)
            row = _row(col, left)
            # The settings square sits at the quadrant's outer edge, as in Max.
            if settings and left:
                row.operator("maximize.caddy_run", text="", icon='OPTIONS', emboss=False).tool = idname
            op = row.operator(idname, text=text, emboss=False, **options)
            for key, value in props.items():
                setattr(op, key, value)
            if settings and not left:
                row.operator("maximize.caddy_run", text="", icon='OPTIONS', emboss=False).tool = idname


def _counts(entries):
    seps = sum(1 for e in entries if e[0] == "sep")
    return len(entries) - seps, seps


def _quadrant(layout, context, title, entries, size, title_last, left):
    """A quadrant padded to `size` (rows, lines); the title sits next to the cursor, in a band
    through the middle of the menu as in Max."""
    col = layout.column(align=True)
    rows, seps = _counts(entries)
    pad = [("gap",)] * (size[0] - rows) + [SEP] * (size[1] - seps)
    if title_last:
        # Top quadrants grow upward from the cursor.
        _draw_entries(col, context, pad + entries, left)
        _title(col, title, left)
    else:
        _title(col, title, left)
        _draw_entries(col, context, entries + pad, left)


def _title(col, title, left):
    band = col.box()
    band.scale_y = 0.7
    row = _row(band, left)
    row.enabled = False
    row.label(text=title)


def _size(a, b):
    return tuple(max(x, y) for x, y in zip(_counts(a), _counts(b)))


class MAXIMIZE_MT_quad_convert(Menu):
    bl_label = "Convert To"

    def draw(self, context):
        layout = self.layout
        layout.operator("maximize.convert_poly", text="Convert to Editable Poly")
        obj = context.active_object
        if obj is not None and obj.type in {'CURVE', 'MESH'}:
            layout.operator("maximize.convert_spline", text="Convert to Editable Spline")


class MAXIMIZE_PT_quad(Panel):
    bl_label = "Quad Menu"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'INSTANCED'}
    bl_ui_units_x = 24

    def draw(self, context):
        layout = self.layout
        display, viewport = _display(context), _viewport(context)
        if context.mode == 'EDIT_MESH':
            tools_title, tools = "Edit Poly", _tools_poly(context)
        elif context.mode == 'EDIT_CURVE':
            tools_title, tools = "Edit Spline", _tools_spline(context)
        else:
            tools_title, tools = "Tools", _tools_object(context)
        transform = _transform(context)

        top_size = _size(display, viewport)
        top = layout.split(factor=0.5)
        _quadrant(top, context, "Display", display, top_size, title_last=True, left=True)
        _quadrant(top, context, "Viewport", viewport, top_size, title_last=True, left=False)

        # Anchor: the popover puts 80% of its selected button's width under the mouse, so a
        # 0.625-wide selected toggle centers the grid on the cursor.
        anchor = layout.split(factor=0.625)
        anchor.scale_y = 0.3
        anchor.prop(context.window_manager, "maximize_quad_anchor", text="", toggle=True, emboss=False)
        anchor.label(text="")

        bottom_size = _size(tools, transform)
        bottom = layout.split(factor=0.5)
        _quadrant(bottom, context, tools_title, tools, bottom_size, title_last=False, left=True)
        _quadrant(bottom, context, "Transform", transform, bottom_size, title_last=False, left=False)


def _keep_anchor_on(self, _context):
    if not self.maximize_quad_anchor:
        self.maximize_quad_anchor = True


classes = (
    MAXIMIZE_MT_quad_convert,
    MAXIMIZE_PT_quad,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.WindowManager.maximize_quad_anchor = BoolProperty(
        default=True, options={'SKIP_SAVE'}, update=_keep_anchor_on)


def unregister():
    del bpy.types.WindowManager.maximize_quad_anchor
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
