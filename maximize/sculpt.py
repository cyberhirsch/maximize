# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""The Sculpt modifier (Seb's design, modeled on Max's Retopology modifier): one stack entry with
the Multires levels and the brush settings; entering it starts Sculpt Mode on it.

- At the bottom of the stack it is Blender's Multires modifier, named "Sculpt": stock Blender opens
  it as a normal Multires. Dyntopo bakes the levels into the mesh first (asks before).
- Mid-stack (Moritz builds) it is a native Edit Poly modifier in Deform mode, named "Sculpt":
  the sculpt happens on a stand-in holding the result of the stack below, and leaving stores the
  vertex offsets. What's below must keep its vertex count (else the sculpt follows the nearest
  vertices, as Edit Poly does); Dyntopo and remeshing are off there. Stock Blender keeps it
  disabled and saves it back.
"""

import bpy
from bpy.types import Operator

from . import edit_poly

SCULPT_NAME = "Sculpt"
# The object's mid-stack sculpt modifiers: ["name", ...] (Edit Poly modifiers used for sculpting).
MIDSTACK = "mx_sculpt_modifiers"
SESSION = "maximize_sculpt_session"


def is_sculpt(obj, mod):
    if mod is None:
        return False
    if mod.type == 'MULTIRES':
        return mod.name.startswith(SCULPT_NAME)
    return mod.type == 'EDIT_POLY' and mod.name in obj.get(MIDSTACK, [])


def is_midstack(obj, mod):
    return mod is not None and mod.type == 'EDIT_POLY' and mod.name in obj.get(MIDSTACK, [])


def active_sculpt(obj):
    mod = obj.modifiers.active if obj is not None else None
    return mod if is_sculpt(obj, mod) else None


def add_sculpt(context, obj):
    """A Sculpt modifier at the top of the stack: Multires when the stack is empty (or in Blender
    builds without the native Edit Poly), else the mid-stack kind."""
    if obj.modifiers and edit_poly.native():
        mod = obj.modifiers.new(SCULPT_NAME, 'EDIT_POLY')
        names = list(obj.get(MIDSTACK, []))
        names.append(mod.name)
        obj[MIDSTACK] = names
    else:
        mod = obj.modifiers.new(SCULPT_NAME, 'MULTIRES')
        # Multires only works first in the stack.
        with context.temp_override(object=obj, active_object=obj):
            bpy.ops.object.modifier_move_to_index(modifier=mod.name, index=0)
    obj.modifiers.active = mod
    return mod


class MAXIMIZE_OT_sculpt_add(Operator):
    """Add the Sculpt modifier: Multires and the brush settings in one stack entry (mid-stack in
    Moritz, with limits)"""
    bl_idname = "maximize.sculpt_add"
    bl_label = "Sculpt"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == 'MESH' and context.mode == 'OBJECT'

    def execute(self, context):
        mod = add_sculpt(context, context.active_object)
        if mod.type == 'EDIT_POLY':
            self.report({'INFO'}, "Mid-stack Sculpt: what's below must keep its topology; no Dyntopo here")
        return {'FINISHED'}


def begin_sculpt(context, obj, mod):
    if mod.type == 'MULTIRES':
        context.view_layer.objects.active = obj
        obj.modifiers.active = mod
        bpy.ops.object.mode_set(mode='SCULPT')
        return obj
    # Mid-stack: a stand-in with the stack's result up to here.
    edited_ob, base = edit_poly._native_stand_in(context, obj, mod)
    for o in context.selected_objects:
        o.select_set(False)
    context.scene.collection.objects.link(edited_ob)
    edited_ob.matrix_world = obj.matrix_world
    obj.hide_set(True)
    edited_ob.select_set(True)
    context.view_layer.objects.active = edited_ob
    context.scene[SESSION] = {"object": obj.name, "modifier": mod.name, "edited": edited_ob.name,
                              "input": base.name}
    bpy.ops.object.mode_set(mode='SCULPT')
    return edited_ob


def end_sculpt(context):
    session = context.scene.get(SESSION)
    if session is None:
        if context.mode == 'SCULPT':
            bpy.ops.object.mode_set(mode='OBJECT')
        return False
    session = session.to_dict()
    del context.scene[SESSION]
    obj = bpy.data.objects.get(session["object"])
    edited_ob = bpy.data.objects.get(session["edited"])
    if edited_ob is not None:
        if edited_ob.mode != 'OBJECT':
            with context.temp_override(active_object=edited_ob, object=edited_ob):
                bpy.ops.object.mode_set(mode='OBJECT')
        edit_poly._sanitize_orig(edited_ob.data)
        for coll in list(edited_ob.users_collection):
            coll.objects.unlink(edited_ob)
        edit_poly._native_store(obj, session, edited_ob)
    if obj is not None:
        obj.hide_set(False)
        obj.select_set(True)
        context.view_layer.objects.active = obj
        obj.update_tag()
    return True


class MAXIMIZE_OT_sculpt_toggle(Operator):
    """Enter or leave the Sculpt modifier's level: Sculpt Mode on it"""
    bl_idname = "maximize.sculpt_toggle"
    bl_label = "Sculpt"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if context.mode == 'SCULPT':
            return True
        return context.mode == 'OBJECT' and active_sculpt(context.active_object) is not None

    def execute(self, context):
        if context.mode == 'SCULPT':
            end_sculpt(context)
        else:
            obj = context.active_object
            begin_sculpt(context, obj, active_sculpt(obj))
        return {'FINISHED'}


class MAXIMIZE_OT_sculpt_dyntopo(Operator):
    """Dyntopo: bakes the Multires levels into the mesh first (they can't be kept), then sculpts
    with dynamic topology. Only at the bottom of the stack"""
    bl_idname = "maximize.sculpt_dyntopo"
    bl_label = "Dyntopo"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            return False
        if obj.mode == 'SCULPT' and obj.use_dynamic_topology_sculpting:
            return True
        mod = active_sculpt(obj)
        return mod is not None and mod.type == 'MULTIRES'

    def invoke(self, context, _event):
        obj = context.active_object
        mod = active_sculpt(obj)
        if mod is not None and mod.type == 'MULTIRES' and mod.total_levels > 0 and \
                not obj.use_dynamic_topology_sculpting:
            return context.window_manager.invoke_confirm(
                self, None, title="Apply the subdivisions?",
                message="Dyntopo can't keep the Multires levels: they are baked into the mesh.",
                confirm_text="Apply and Use Dyntopo")
        return self.execute(context)

    def execute(self, context):
        obj = context.active_object
        if obj.mode == 'SCULPT' and obj.use_dynamic_topology_sculpting:
            bpy.ops.sculpt.dynamic_topology_toggle()
            return {'FINISHED'}
        mod = active_sculpt(obj)
        if obj.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        if mod is not None and mod.type == 'MULTIRES':
            with context.temp_override(object=obj, active_object=obj):
                bpy.ops.object.modifier_apply(modifier=mod.name)
        bpy.ops.object.mode_set(mode='SCULPT')
        if not obj.use_dynamic_topology_sculpting:
            bpy.ops.sculpt.dynamic_topology_toggle()
        return {'FINISHED'}


def _brush_settings(layout, context):
    ts = context.tool_settings
    sculpt = ts.sculpt
    brush = getattr(sculpt, "brush", None)
    col = layout.column(align=True)
    if brush is not None:
        col.label(text=brush.name, icon='BRUSH_DATA')
        ups = getattr(sculpt, "unified_paint_settings", None) or getattr(ts, "unified_paint_settings", None)
        size_owner = ups if ups is not None and getattr(ups, "use_unified_size", False) else brush
        strength_owner = ups if ups is not None and getattr(ups, "use_unified_strength", False) else brush
        col.prop(size_owner, "size", text="Radius", slider=True)
        col.prop(strength_owner, "strength", slider=True)
        if hasattr(brush, "curve_distance_falloff_preset"):
            col.prop(brush, "curve_distance_falloff_preset", text="Falloff")
        elif hasattr(brush, "curve_preset"):
            col.prop(brush, "curve_preset", text="Falloff")
    obj = context.active_object
    if obj is not None and obj.type == 'MESH':
        row = layout.row(align=True)
        row.label(text="Symmetry")
        row.prop(obj.data, "use_mirror_x", text="X", toggle=True)
        row.prop(obj.data, "use_mirror_y", text="Y", toggle=True)
        row.prop(obj.data, "use_mirror_z", text="Z", toggle=True)


def draw(layout, context, obj, mod=None):
    """The Sculpt modifier's rollout in the Modify tab (`mod`, else the active Sculpt modifier)."""
    mod = mod or active_sculpt(obj)
    sculpting = context.mode == 'SCULPT'
    if mod is None and not sculpting:
        return
    box = layout.box()
    box.label(text="Sculpt", icon='SCULPTMODE_HLT')
    box.operator("maximize.sculpt_toggle", text="Leave Sculpt" if sculpting else "Sculpt",
                 depress=sculpting)
    if mod is not None and mod.type == 'MULTIRES':
        col = box.column(align=True)
        col.prop(mod, "levels", text="Level Viewport")
        col.prop(mod, "sculpt_levels", text="Sculpt")
        col.prop(mod, "render_levels", text="Render")
        row = box.row(align=True)
        for mode, text in (('CATMULL_CLARK', "Subdivide"), ('SIMPLE', "Simple"), ('LINEAR', "Linear")):
            op = row.operator("object.multires_subdivide", text=text)
            op.modifier = mod.name
            op.mode = mode
        row = box.row(align=True)
        row.operator("object.multires_unsubdivide", text="Unsubdivide").modifier = mod.name
        row.operator("object.multires_higher_levels_delete", text="Delete Higher").modifier = mod.name
        row = box.row(align=True)
        row.operator("object.multires_base_apply", text="Apply Base").modifier = mod.name
        row.operator("object.multires_rebuild_subdiv", text="Rebuild Subdivisions").modifier = mod.name
    elif mod is not None:
        box.label(text="Mid-stack: the stack below must keep its topology; no Dyntopo", icon='ERROR')
    obj_now = context.active_object
    dyntopo = obj_now is not None and obj_now.mode == 'SCULPT' and obj_now.use_dynamic_topology_sculpting
    row = box.row()
    row.enabled = mod is None or mod.type == 'MULTIRES'
    row.operator("maximize.sculpt_dyntopo", text="Dyntopo", depress=dyntopo)
    _brush_settings(box, context)


classes = (
    MAXIMIZE_OT_sculpt_add,
    MAXIMIZE_OT_sculpt_toggle,
    MAXIMIZE_OT_sculpt_dyntopo,
)


def _draw_add_menu(self, context):
    obj = context.object
    if obj is not None and obj.type == 'MESH':
        self.layout.separator()
        self.layout.operator("maximize.sculpt_add", text="Sculpt (Max)", icon='SCULPTMODE_HLT')


_MENUS = ("OBJECT_MT_modifier_add_flat", "OBJECT_MT_modifier_add")


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    for name in _MENUS:
        menu = getattr(bpy.types, name, None)
        if menu is not None:
            menu.append(_draw_add_menu)
            break


def unregister():
    for name in _MENUS:
        menu = getattr(bpy.types, name, None)
        if menu is not None:
            try:
                menu.remove(_draw_add_menu)
            except ValueError:
                pass
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
