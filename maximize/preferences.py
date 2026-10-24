# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Add-on preferences and the Moritz / Max / Blender keymap switch."""

import bpy
from bpy.props import BoolProperty, EnumProperty


KEYMAPS = (
    ('Moritz', "Moritz", "Max keys with Blender's selection ideas (the default)"),
    ('Max', "Max", "3ds Max keymap (Industry Compatible with Max keys)"),
    ('Blender', "Blender", "Stock Blender keymap, for following Blender tutorials"),
    ('Industry_Compatible', "Industry Compatible", "Blender's Maya-like keymap"),
)


def get_prefs(context=None):
    context = context or bpy.context
    addon = context.preferences.addons.get(__package__)
    return addon.preferences if addon else None


def active_keymap(context):
    return context.preferences.keymap.active_keyconfig


def _update_vocabulary(self, _context):
    from . import vocabulary
    vocabulary.set_enabled(self.use_max_english)


class MAXIMIZE_OT_keymap_set(bpy.types.Operator):
    """Switch between the Moritz and Max keymaps and Blender's own keymaps"""
    bl_idname = "maximize.keymap_set"
    bl_label = "Switch Keymap"
    bl_options = {'INTERNAL'}

    keymap: EnumProperty(name="Keymap", items=KEYMAPS)

    def execute(self, context):
        filepath = bpy.utils.preset_find(self.keymap, "keyconfig")
        if not filepath:
            self.report({'ERROR'}, "Keymap preset \"{:s}\" not found".format(self.keymap))
            return {'CANCELLED'}
        bpy.ops.preferences.keyconfig_activate(filepath=filepath)
        context.preferences.is_dirty = True
        self.report({'INFO'}, "Keymap: {:s}".format(self.keymap.replace("_", " ")))
        return {'FINISHED'}


def draw_keymap_switch(layout, context):
    row = layout.row(align=True)
    current = active_keymap(context)
    for ident, name, _desc in KEYMAPS:
        row.operator("maximize.keymap_set", text=name, depress=(current == ident)).keymap = ident


class MaximizePreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    use_max_english: BoolProperty(
        name="Max English",
        description="Use 3ds Max names in the interface (Weld, Chamfer, Attach, Swift Loop and more)",
        default=True,
        update=_update_vocabulary,
    )
    use_startup_layout: BoolProperty(
        name="Max Layout for New Files",
        description="New files open with a quad view, centimeters and the Max sidebar tab",
        default=True,
    )
    use_hover_highlight: BoolProperty(
        name="Hover Highlight",
        description="Highlight the object or sub-object under the mouse before you click, as in Max",
        default=True,
    )
    first_run_done: BoolProperty(default=False, options={'HIDDEN'})

    def draw(self, context):
        layout = self.layout
        layout.label(text="Keymap")
        draw_keymap_switch(layout, context)
        layout.separator()
        col = layout.column()
        col.prop(self, "use_max_english")
        col.prop(self, "use_startup_layout")
        col.prop(self, "use_hover_highlight")
        inputs = context.preferences.inputs
        col.prop(inputs, "use_rotate_around_active", text="Orbit Around Selection")
        col.prop(inputs, "use_zoom_to_mouse", text="Zoom About Mouse Point")


def first_run_setup():
    """Max navigation defaults and the Moritz keymap, applied once when the add-on is first enabled."""
    prefs = get_prefs()
    if prefs is None or prefs.first_run_done:
        return
    inputs = bpy.context.preferences.inputs
    inputs.use_rotate_around_active = True
    inputs.use_zoom_to_mouse = True
    prefs.first_run_done = True
    # Start in the Moritz keymap; Preferences > Keymap or the Max sidebar switch back.
    from .keymaps import activate
    bpy.app.timers.register(lambda: activate("Moritz") and None, first_interval=0.0)


classes = (
    MAXIMIZE_OT_keymap_set,
    MaximizePreferences,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
