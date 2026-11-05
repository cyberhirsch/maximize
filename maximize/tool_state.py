# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""What a running tool shows: the mouse pointer in the viewport and its lit button in the panels.

Which tool runs is asked of Blender (`Window.modal_operators`), so a button can't stay lit after a
tool ended in an unexpected way, such as an error. Only a button that hands over to one of Blender's
tools is remembered, while that tool runs (`watch`), since Cut and Paint Connect run the same one.
"""

import bpy

_handed_over = {}  # the button's operator: the Blender operator it started


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


def watch(idname, target):
    """Call when the button's operator `idname` has started Blender's modal tool `target`: the button
    is lit until that ends. Blender's tools don't tell the panels, so a timer redraws them."""
    _handed_over[idname] = target
    redraw()

    def check():
        if is_running(target):
            return 0.2
        if _handed_over.get(idname) == target:
            del _handed_over[idname]
        redraw()
        return None
    bpy.app.timers.register(check, first_interval=0.2, persistent=True)


def viewport(context):
    """Arguments for `temp_override`: the 3D View for a tool started from a panel button, nothing for
    one started in a 3D View."""
    if context.area is not None and context.area.type == 'VIEW_3D':
        return {}
    from .vocabulary import view3d_override
    return view3d_override(context) or {}


def can_click_in_viewport(context):
    """Poll of a tool that clicks in a 3D View: in one, or from a panel of a window that has one."""
    return context.area is not None and (context.area.type == 'VIEW_3D' or bool(viewport(context)))


def start_in_viewport(operator, context):
    """Call first in the tool's invoke. From a panel button: starts the tool again in the 3D View and
    returns the result for this call, which ends. In a 3D View: None, go on."""
    override = viewport(context)
    if not override:
        return None
    module, name = type(operator).bl_idname.split(".")
    props = {p.identifier: getattr(operator.properties, p.identifier) for p in operator.properties.bl_rna.properties
             if p.identifier != "rna_type" and operator.properties.is_property_set(p.identifier)}
    with context.temp_override(**override):
        getattr(getattr(bpy.ops, module), name)('INVOKE_DEFAULT', **props)
    # The tool makes its own undo step when it ends.
    return {'CANCELLED'}


def is_running(idname, **props):
    """True while the operator `idname` ("maximize.line") runs, with these property values if given."""
    module, name = _handed_over.get(idname, idname).split(".")
    identifier = module.upper() + "_OT_" + name
    for window in bpy.context.window_manager.windows:
        for op in window.modal_operators:
            if op.bl_idname == identifier and all(getattr(op.properties, key, None) == value
                                                  for key, value in props.items()):
                return True
    return False
