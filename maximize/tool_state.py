# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""What a running tool shows: the mouse pointer in the viewport and its lit button in the panels.

Which tool runs is asked of Blender (`Window.modal_operators`), so a button can't stay lit after a
tool ended in an unexpected way, such as an error. Stored nowhere.
"""

import bpy


def redraw():
    """The panels show `is_running` only when redrawn."""
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type in {'PROPERTIES', 'VIEW_3D'}:
                area.tag_redraw()


def begin(context, cursor='CROSSHAIR'):
    """Call when a tool starts."""
    context.window.cursor_modal_set(cursor)
    redraw()


def end(context):
    """Call on every way a tool ends."""
    context.window.cursor_modal_restore()
    redraw()


def is_running(idname, **props):
    """True while the operator `idname` ("maximize.line") runs, with these property values if given."""
    module, name = idname.split(".")
    identifier = module.upper() + "_OT_" + name
    for window in bpy.context.window_manager.windows:
        for op in window.modal_operators:
            if op.bl_idname == identifier and all(getattr(op.properties, key, None) == value
                                                  for key, value in props.items()):
                return True
    return False
