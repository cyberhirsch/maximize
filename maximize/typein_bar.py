# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Transform Type-In in the status bar, as Max shows it at the bottom left: while Move, Rotate or
Scale is the active tool, X / Y / Z fields for the selection, Absolute or Offset.

Typing a value moves, rotates or scales the selection at once (one undo step each). Offset fields
go back to 0 (100% for Scale) after each entry, as in Max. F12 still opens the Type-In dialog.
"""

import math

import bpy
from bpy.props import BoolProperty, FloatVectorProperty

from .transform import apply_typein, read_absolute

_TOOLS = {
    'builtin.move': 'MOVE',
    'builtin.transform': 'MOVE',
    'builtin.rotate': 'ROTATE',
    'builtin.scale': 'SCALE',
    'builtin.scale_cage': 'SCALE',
}


def tool_mode(context):
    """'MOVE' / 'ROTATE' / 'SCALE' while that tool is active on something to transform, else None."""
    if context.mode not in {'OBJECT', 'EDIT_MESH'} or context.active_object is None:
        return None
    workspace = context.workspace
    if workspace is None:
        return None
    tool = workspace.tools.from_space_view3d_mode(context.mode, create=False)
    return _TOOLS.get(tool.idname) if tool else None


def _identity(mode):
    return (100.0, 100.0, 100.0) if mode == 'SCALE' else (0.0, 0.0, 0.0)


def _getter(mode):
    def get(wm):
        context = bpy.context
        if wm.maximize_typein_offset or tool_mode(context) != mode:
            values = _identity(mode)
        else:
            values = read_absolute(context, mode)
        return tuple(math.radians(v) for v in values) if mode == 'ROTATE' else values
    return get


def _setter(mode):
    def set_(wm, values):
        context = bpy.context
        if tool_mode(context) != mode:
            return
        values = tuple(math.degrees(v) for v in values) if mode == 'ROTATE' else tuple(values)
        if wm.maximize_typein_offset:
            if all(abs(v - i) < 1e-9 for v, i in zip(values, _identity(mode))):
                return
            apply_typein(context, mode, offset=values)
        else:
            start = read_absolute(context, mode)
            if all(abs(v - s) < 1e-9 for v, s in zip(values, start)):
                return
            apply_typein(context, mode, absolute=values, start=start)
        bpy.ops.ed.undo_push(message="Transform Type-In")
    return set_


def draw(self, context):
    mode = tool_mode(context)
    if mode is None:
        return
    wm = context.window_manager
    layout = self.layout
    row = layout.row(align=True)
    offset = wm.maximize_typein_offset
    row.prop(wm, "maximize_typein_offset", text="Offset" if offset else "Absolute", toggle=True)
    fields = row.row(align=True)
    fields.ui_units_x = 16
    # Edit Mode has no absolute rotation or scale.
    fields.enabled = offset or mode == 'MOVE' or context.mode == 'OBJECT'
    fields.prop(wm, {'MOVE': "maximize_typein_move", 'ROTATE': "maximize_typein_rotate",
                     'SCALE': "maximize_typein_scale"}[mode], text="")
    layout.separator()


def _redraw_status(*_args):
    """The fields follow the selection as it moves."""
    if tool_mode(bpy.context) is None:
        return
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'STATUSBAR':
                area.tag_redraw()


def register():
    wm = bpy.types.WindowManager
    wm.maximize_typein_offset = BoolProperty(
        name="Offset", description="Type an offset from where the selection is, instead of absolute values")
    wm.maximize_typein_move = FloatVectorProperty(
        name="Move", size=3, subtype='TRANSLATION', unit='LENGTH', get=_getter('MOVE'), set=_setter('MOVE'),
        description="Position of the selection (Transform Type-In)")
    wm.maximize_typein_rotate = FloatVectorProperty(
        name="Rotate", size=3, subtype='EULER', get=_getter('ROTATE'), set=_setter('ROTATE'),
        description="Rotation of the selection (Transform Type-In)")
    wm.maximize_typein_scale = FloatVectorProperty(
        name="Scale %", size=3, subtype='XYZ', get=_getter('SCALE'), set=_setter('SCALE'),
        description="Scale of the selection, in percent (Transform Type-In)")
    bpy.types.STATUSBAR_HT_header.prepend(draw)
    bpy.app.handlers.depsgraph_update_post.append(_redraw_status)


def unregister():
    if _redraw_status in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(_redraw_status)
    bpy.types.STATUSBAR_HT_header.remove(draw)
    wm = bpy.types.WindowManager
    for name in ("maximize_typein_offset", "maximize_typein_move", "maximize_typein_rotate",
                 "maximize_typein_scale"):
        delattr(wm, name)
