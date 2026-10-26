# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Max quad menu on right-click: four quadrants (Display, Viewport, Tools, Transform), per mode.

It is a popover laid out as a 2x2 grid whose quadrants meet at the mouse, as in Max: the top
quadrants end at the cursor line and the bottom ones start there. Blender opens a popover with
its selected button under the mouse, so an invisible, always-on toggle in the middle row anchors
the grid's center to the cursor.
"""

import bpy
from bpy.props import BoolProperty
from bpy.types import Panel

# Quadrant entries: ("op", idname, text, props, options), ("menu", idname, text), ("gap",) and
# ("ops", [(idname, text, props), ...]) for a row of small buttons. Every entry is one row high,
# so quadrants can be padded to line up at the cursor.


def _tool(text, tool, icon):
    return ("op", "wm.tool_set_by_id", text, {"name": tool}, {"icon": icon})


def _state(on):
    # A checkbox icon instead of a pressed-in button: the popover anchors on pressed-in buttons.
    return {"icon": 'CHECKBOX_HLT' if on else 'CHECKBOX_DEHLT'}


def _toggle(text, data_path, on):
    return ("op", "wm.context_toggle", text, {"data_path": data_path}, _state(on))


def _transform(context):
    items = [
        _tool("Move", "builtin.move", 'OBJECT_ORIGIN'),
        _tool("Rotate", "builtin.rotate", 'ORIENTATION_GIMBAL'),
        _tool("Scale", "builtin.scale", 'FULLSCREEN_ENTER'),
        _tool("Select", "builtin.select_box", 'RESTRICT_SELECT_OFF'),
        ("op", "maximize.transform_typein", "Transform Type-In...", {}, {}),
    ]
    if context.mode == 'OBJECT':
        items += [
            ("op", "maximize.clone", "Clone...", {}, {}),
            ("op", "maximize.affect_pivot_only", "Affect Pivot Only", {},
             _state(context.scene.tool_settings.use_transform_data_origin)),
            ("op", "maximize.reset_xform", "Reset XForm", {}, {}),
            ("op", "maximize.open_editor", "Curve Editor...", {"ui_type": 'FCURVES'}, {}),
            ("op", "maximize.open_editor", "Object Properties...", {"ui_type": 'PROPERTIES'}, {}),
        ]
    return items


def _display(context):
    items = [("op", "view3d.localview", "Isolate Selection", {}, {})]
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
        ("op", "maximize.viewport_maximize", "Maximize Viewport Toggle", {}, {}),
    ]


def _tools_object(context):
    obj = context.active_object
    if obj is not None and obj.type == 'CURVE':
        first = [("op", "maximize.convert_spline", "Convert to Editable Spline", {}, {}),
                 ("op", "maximize.edit_spline_add", "Edit Spline Modifier", {}, {})]
    else:
        first = [("op", "maximize.edit_poly_add", "Edit Poly Modifier", {}, {})]
    return first + [
        ("op", "maximize.convert_poly", "Convert to Editable Poly", {}, {}),
        ("op", "maximize.attach", "Attach", {}, {}),
        ("op", "maximize.collapse_all", "Collapse All", {}, {}),
        ("op", "maximize.align", "Align", {}, {}),
        ("op", "maximize.array", "Array...", {}, {}),
        ("op", "maximize.spacing", "Spacing Tool...", {}, {}),
        ("op", "maximize.uvw_map", "UVW Map", {}, {}),
        ("menu", "MAXIMIZE_MT_selection_sets", "Named Selection Sets"),
        ("menu", "MAXIMIZE_MT_create", "Create"),
        ("menu", "MAXIMIZE_MT_create_shapes", "Shapes"),
    ]


def _tools_poly(_context):
    levels = (('VERTEX', "Vert"), ('EDGE', "Edge"), ('BORDER', "Bord"), ('POLYGON', "Poly"),
              ('ELEMENT', "Elem"), ('OBJECT', "Top"))
    return [
        ("ops", [("maximize.subobject", label, {"level": level}) for level, label in levels]),
        ("op", "mesh.extrude_context_move", "Extrude", {}, {}),
        # Untranslated: the Max vocabulary renames Blender's Bevel to Chamfer.
        ("op", "maximize.bevel_poly", "Bevel", {}, {"translate": False}),
        ("op", "maximize.chamfer", "Chamfer", {}, {}),
        ("op", "maximize.inset", "Inset", {}, {}),
        ("op", "maximize.cut", "Cut", {}, {}),
        ("op", "maximize.swift_loop", "Swift Loop", {}, {}),
        ("op", "maximize.connect", "Connect", {}, {}),
        ("op", "maximize.weld", "Weld", {}, {}),
        ("op", "maximize.target_weld", "Target Weld", {}, {}),
        ("op", "maximize.collapse_sub", "Collapse", {}, {}),
        ("op", "maximize.bridge", "Bridge", {}, {}),
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
        ("ops", types),
        ("ops", beziers),
        ("op", "maximize.spline_reset_tangents", "Reset Tangents", {}, {}),
        ("op", "maximize.spline_make_first", "Make First", {}, {}),
        ("op", "curve.switch_direction", "Reverse", {}, {}),
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


def _draw_entries(col, entries):
    for entry in entries:
        kind = entry[0]
        if kind == "gap":
            col.label(text="")
        elif kind == "menu":
            col.menu(entry[1], text=entry[2])
        elif kind == "ops":
            row = col.row(align=True)
            for idname, text, props in entry[1]:
                op = row.operator(idname, text=text)
                for key, value in props.items():
                    setattr(op, key, value)
        else:
            _kind, idname, text, props, options = entry
            op = col.operator(idname, text=text, **options)
            for key, value in props.items():
                setattr(op, key, value)


def _quadrant(layout, title, entries, rows, title_last):
    """A quadrant padded to `rows` entries; the title sits next to the cursor."""
    col = layout.box().column(align=True)
    pad = [("gap",)] * (rows - len(entries))
    if title_last:
        # Top quadrants grow upward from the cursor.
        _draw_entries(col, pad + entries)
        col.label(text=title)
    else:
        col.label(text=title)
        _draw_entries(col, entries + pad)


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

        top_rows = max(len(display), len(viewport))
        top = layout.split(factor=0.5)
        _quadrant(top, "Display", display, top_rows, title_last=True)
        _quadrant(top, "Viewport", viewport, top_rows, title_last=True)

        # Anchor: the popover puts 80% of its selected button's width under the mouse, so a
        # 0.625-wide selected toggle centers the grid on the cursor.
        anchor = layout.split(factor=0.625)
        anchor.scale_y = 0.3
        anchor.prop(context.window_manager, "maximize_quad_anchor", text="", toggle=True, emboss=False)
        anchor.label(text="")

        bottom_rows = max(len(tools), len(transform))
        bottom = layout.split(factor=0.5)
        _quadrant(bottom, tools_title, tools, bottom_rows, title_last=False)
        _quadrant(bottom, "Transform", transform, bottom_rows, title_last=False)


def _keep_anchor_on(self, _context):
    if not self.maximize_quad_anchor:
        self.maximize_quad_anchor = True


classes = (
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
