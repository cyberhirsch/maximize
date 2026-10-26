# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""Max's Scene Explorer in Blender's Outliner: the type filter row in the header, double-click
selects an object and its children, Unhide All / Unfreeze All.

Nothing new is stored: the filters are the Outliner's own (Moritz adds Shapes), hiding and freezing
are Blender's hide_viewport / hide_select.
"""

import bpy
from bpy.types import Operator

# Max's Scene Explorer toolbar, left to right: Geometry, Shapes, Lights, Cameras, Helpers, Bones.
_TYPE_FILTERS = (
    ("use_filter_object_mesh", 'MESH_DATA', "Geometry"),
    ("use_filter_object_shapes", 'CURVE_DATA', "Shapes"),
    ("use_filter_object_light", 'LIGHT_DATA', "Lights"),
    ("use_filter_object_camera", 'CAMERA_DATA', "Cameras"),
    ("use_filter_object_empty", 'EMPTY_DATA', "Helpers"),
    ("use_filter_object_armature", 'ARMATURE_DATA', "Bones"),
    ("use_filter_object_others", 'MOD_PHYSICS', "Others"),
)


def draw_type_filters(self, context):
    space = context.space_data
    if space.display_mode not in {'VIEW_LAYER', 'SCENES'}:
        return
    row = self.layout.row(align=True)
    row.active = space.use_filter_object
    for prop, icon, _name in _TYPE_FILTERS:
        if hasattr(space, prop):
            row.prop(space, prop, text="", icon=icon)


def _descendants(obj):
    out = []
    stack = list(obj.children)
    while stack:
        child = stack.pop()
        out.append(child)
        stack.extend(child.children)
    return out


class MAXIMIZE_OT_outliner_select_children(Operator):
    """Select the object under the mouse and all its children (Max's Scene Explorer double-click)"""
    bl_idname = "maximize.outliner_select_children"
    bl_label = "Select with Children"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.area is not None and context.area.type == 'OUTLINER'

    def invoke(self, context, event):
        bpy.ops.outliner.item_activate('INVOKE_DEFAULT', deselect_all=True)
        return self.execute(context)

    def execute(self, context):
        obj = context.view_layer.objects.active
        if obj is None or not obj.select_get():
            return {'FINISHED'}
        for child in _descendants(obj):
            if child.name in context.view_layer.objects and child.visible_get() and not child.hide_select:
                child.select_set(True)
        return {'FINISHED'}


class MAXIMIZE_OT_unhide_all(Operator):
    """Unhide All: show every hidden object in the view layer"""
    bl_idname = "maximize.unhide_all"
    bl_label = "Unhide All"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in context.view_layer.objects:
            if obj.hide_get():
                obj.hide_set(False)
        return {'FINISHED'}


class MAXIMIZE_OT_unfreeze_all(Operator):
    """Unfreeze All: every frozen object can be selected again"""
    bl_idname = "maximize.unfreeze_all"
    bl_label = "Unfreeze All"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in context.view_layer.objects:
            obj.hide_select = False
        return {'FINISHED'}


class MAXIMIZE_OT_color_by_layer(Operator):
    """Color By Layer: objects take their collection's color tag as object color (Max's By Layer
    wire color); the viewport shows it with Solid shading's Object color"""
    bl_idname = "maximize.color_by_layer"
    bl_label = "Color By Layer"
    bl_options = {'REGISTER', 'UNDO'}

    selected_only: bpy.props.BoolProperty(name="Selected Only", default=False)

    def execute(self, context):
        theme = context.preferences.themes[0].collection_color
        count = 0
        objects = context.selected_objects if self.selected_only else context.view_layer.objects
        for obj in objects:
            for coll in obj.users_collection:
                tag = coll.color_tag
                if tag != 'NONE':
                    obj.color[:3] = theme[int(tag[-2:]) - 1].color
                    count += 1
                    break
        for screen_area in context.screen.areas if context.screen else ():
            if screen_area.type == 'VIEW_3D':
                screen_area.spaces.active.shading.color_type = 'OBJECT'
        self.report({'INFO'}, f"{count} objects colored by layer")
        return {'FINISHED'}


def draw_context_extras(self, _context):
    layout = self.layout
    layout.separator()
    layout.operator("maximize.unhide_all", icon='HIDE_OFF')
    layout.operator("maximize.unfreeze_all", icon='FREEZE')
    layout.operator("maximize.color_by_layer", icon='COLOR')


classes = (
    MAXIMIZE_OT_outliner_select_children,
    MAXIMIZE_OT_unhide_all,
    MAXIMIZE_OT_unfreeze_all,
    MAXIMIZE_OT_color_by_layer,
)

_MENUS = ("OUTLINER_MT_context_menu", "OUTLINER_MT_object", "OUTLINER_MT_collection")


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.OUTLINER_HT_header.append(draw_type_filters)
    for name in _MENUS:
        menu = getattr(bpy.types, name, None)
        if menu is not None:
            menu.append(draw_context_extras)


def unregister():
    for name in _MENUS:
        menu = getattr(bpy.types, name, None)
        if menu is not None:
            menu.remove(draw_context_extras)
    bpy.types.OUTLINER_HT_header.remove(draw_type_filters)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
