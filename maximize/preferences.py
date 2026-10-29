# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Add-on preferences and the Moritz / Max / Blender keymap switch."""

import bpy
from bpy.props import BoolProperty, EnumProperty, FloatVectorProperty


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


def _update_names(_self, context):
    from . import vocabulary
    vocabulary.apply_scheme(context)


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
        from . import vocabulary
        vocabulary.apply_scheme(context)
        self.report({'INFO'}, "Keymap: {:s}".format(self.keymap.replace("_", " ")))
        return {'FINISHED'}


def draw_keymap_switch(layout, context):
    row = layout.row(align=True)
    current = active_keymap(context)
    for ident, name, _desc in KEYMAPS:
        row.operator("maximize.keymap_set", text=name, depress=(current == ident)).keymap = ident


class MaximizePreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    name_scheme: EnumProperty(
        name="Names",
        description="Which names the interface uses, as the keymap sets the keys",
        items=(('AUTO', "Follow Keymap", "Max's names with the Max keymap, Moritz's with the Moritz keymap, "
                "Blender's otherwise"),
               ('BLENDER', "Blender", "Blender's names"),
               ('MAX', "Max", "3ds Max's names wherever Max has one (Weld, Chamfer, Attach, Swift Loop and more)"),
               ('MORITZ', "Moritz", "Max's names, with Blender's name in the tooltip")),
        default='AUTO',
        update=_update_names,
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
    tool_settings_style: EnumProperty(
        name="Tool Settings",
        description="Where a Command Panel tool's values are adjusted",
        default='PANEL',
        items=(
            ('PANEL', "Adjust Last Operation", "Blender's panel in the corner of the viewport"),
            ('CADDY', "Caddy", "Max's caddy: a settings button next to each tool opens its values at the "
             "mouse, with OK, Apply and Continue and Cancel"),
        ),
    )
    first_run_done: BoolProperty(default=False, options={'HIDDEN'})
    # Max's Show Cage colors (Edit Poly > Edit Geometry).
    cage_color: FloatVectorProperty(
        name="Cage", subtype='COLOR', size=3, min=0.0, max=1.0, default=(1.0, 0.55, 0.1),
        description="Color of the cage's edges",
    )
    cage_selected_color: FloatVectorProperty(
        name="Selected Cage", subtype='COLOR', size=3, min=0.0, max=1.0, default=(1.0, 0.1, 0.1),
        description="Color of the cage's selected edges",
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Keymap")
        draw_keymap_switch(layout, context)
        layout.separator()
        col = layout.column()
        col.prop(self, "name_scheme")
        col.prop(self, "use_startup_layout")
        col.prop(self, "use_hover_highlight")
        col.prop(self, "tool_settings_style")
        inputs = context.preferences.inputs
        col.prop(inputs, "use_rotate_around_active", text="Orbit Around Selection")
        col.prop(inputs, "use_zoom_to_mouse", text="Zoom About Mouse Point")
        row = col.row(align=True)
        row.prop(self, "cage_color")
        row.prop(self, "cage_selected_color")


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
