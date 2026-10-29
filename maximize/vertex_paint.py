# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Max's VertexPaint modifier (native in Moritz): a color layer in the stack. Painting happens on a
stand-in holding the stack's result up to the modifier, in Vertex Paint mode; leaving stores the
colors in the modifier, which writes them onto its input. What's below must keep its vertex count.
"""

import bpy
from bpy.types import Operator

from . import edit_poly

SESSION = "maximize_vertex_paint_session"


def native():
    return 'VERTEX_PAINT' in {it.identifier for it in
                              bpy.types.Modifier.bl_rna.properties["type"].enum_items}


def active_vertex_paint(obj):
    mod = obj.modifiers.active if obj is not None else None
    return mod if mod is not None and mod.type == 'VERTEX_PAINT' else None


def begin_paint(context, obj, mod):
    """Vertex Paint mode on a stand-in with the stack's result up to `mod` (its colors included)."""
    if context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    mesh = edit_poly._evaluated_mesh(context, obj, mod, include=True)
    mesh.name = obj.name + " VertexPaint"
    attr = mesh.color_attributes.get(mod.layer)
    if attr is None:
        attr = mesh.color_attributes.new(mod.layer, 'FLOAT_COLOR', 'POINT')
        for c in attr.data:
            c.color = (1.0, 1.0, 1.0, 1.0)
    mesh.color_attributes.active_color = attr
    standin = edit_poly._helper_object(obj.name + " VertexPaint", mesh)
    context.scene.collection.objects.link(standin)
    standin.matrix_world = obj.matrix_world
    for o in context.selected_objects:
        o.select_set(False)
    obj.hide_set(True)
    standin.select_set(True)
    context.view_layer.objects.active = standin
    context.scene[SESSION] = {"object": obj.name, "modifier": mod.name, "edited": standin.name}
    bpy.ops.object.mode_set(mode='VERTEX_PAINT')
    return standin


def end_paint(context, keep=True):
    """Leave the session; with `keep`, store the painted colors in the modifier."""
    session = context.scene.get(SESSION)
    if session is None:
        return False
    session = session.to_dict()
    del context.scene[SESSION]
    obj = bpy.data.objects.get(session["object"])
    standin = bpy.data.objects.get(session["edited"])
    ok = True
    if standin is not None:
        if standin.mode != 'OBJECT':
            with context.temp_override(active_object=standin, object=standin):
                bpy.ops.object.mode_set(mode='OBJECT')
        mod = obj.modifiers.get(session["modifier"]) if obj is not None else None
        if keep and mod is not None:
            ok = mod.store(mesh=standin.data)
        mesh = standin.data
        bpy.data.objects.remove(standin)
        if mesh.users == 0:
            bpy.data.meshes.remove(mesh)
    if obj is not None:
        obj.hide_set(False)
        obj.select_set(True)
        context.view_layer.objects.active = obj
        obj.update_tag()
    return ok


def in_session(context):
    return context.scene.get(SESSION) is not None


class MAXIMIZE_OT_vertex_paint_toggle(Operator):
    """Paint the VertexPaint modifier's colors, or store them and leave"""
    bl_idname = "maximize.vertex_paint_toggle"
    bl_label = "Paint"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if in_session(context):
            return True
        return context.mode == 'OBJECT' and active_vertex_paint(context.active_object) is not None

    def execute(self, context):
        if in_session(context):
            if not end_paint(context):
                self.report({'WARNING'}, "The colors could not be kept (see the modifier)")
        else:
            obj = context.active_object
            begin_paint(context, obj, active_vertex_paint(obj))
        return {'FINISHED'}


class MAXIMIZE_OT_vertex_paint_cancel(Operator):
    """Leave painting without keeping the new strokes"""
    bl_idname = "maximize.vertex_paint_cancel"
    bl_label = "Cancel"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return in_session(context)

    def execute(self, context):
        end_paint(context, keep=False)
        return {'FINISHED'}


class MAXIMIZE_OT_vertex_paint_add(Operator):
    """Add Max's VertexPaint modifier and start painting"""
    bl_idname = "maximize.vertex_paint_add"
    bl_label = "VertexPaint"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == 'MESH' and context.mode == 'OBJECT' and native()

    def execute(self, context):
        obj = context.active_object
        mod = obj.modifiers.new("VertexPaint", 'VERTEX_PAINT')
        obj.modifiers.active = mod
        begin_paint(context, obj, mod)
        return {'FINISHED'}


def draw(layout, context, mod):
    """The VertexPaint rollout: Paint / Done, Cancel and Clear."""
    row = layout.row(align=True)
    if in_session(context):
        row.operator("maximize.vertex_paint_toggle", text="Done", icon='CHECKMARK', depress=True)
        row.operator("maximize.vertex_paint_cancel", text="", icon='X')
    else:
        row.operator("maximize.vertex_paint_toggle", text="Paint", icon='BRUSH_DATA')
        row.enabled = context.mode == 'OBJECT'
    if mod is not None and mod.has_colors:
        layout.operator("object.mx_vertex_paint_clear", text="Clear Colors")


class OBJECT_OT_mx_vertex_paint_clear(Operator):
    """Forget the VertexPaint modifier's stored colors"""
    bl_idname = "object.mx_vertex_paint_clear"
    bl_label = "Clear Colors"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return active_vertex_paint(context.active_object) is not None

    def execute(self, context):
        active_vertex_paint(context.active_object).clear()
        return {'FINISHED'}


classes = (
    MAXIMIZE_OT_vertex_paint_toggle,
    MAXIMIZE_OT_vertex_paint_cancel,
    MAXIMIZE_OT_vertex_paint_add,
    OBJECT_OT_mx_vertex_paint_clear,
)


def _header_draw(self, context):
    if in_session(context):
        row = self.layout.row(align=True)
        row.operator("maximize.vertex_paint_toggle", text="Done", icon='CHECKMARK', depress=True)
        row.operator("maximize.vertex_paint_cancel", text="", icon='X')


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_HT_tool_header.append(_header_draw)


def unregister():
    bpy.types.VIEW3D_HT_tool_header.remove(_header_draw)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
