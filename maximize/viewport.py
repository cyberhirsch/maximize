# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Viewport commands with Max behavior, and the Max layout for new files."""

import bpy
from bpy.app.handlers import persistent
from bpy.props import BoolProperty, EnumProperty
from bpy.types import Operator


class MAXIMIZE_OT_view_projection(Operator):
    """Switch the viewport to a perspective (P) or orthographic user view (U)"""
    bl_idname = "maximize.view_projection"
    bl_label = "Perspective / User View"

    projection: EnumProperty(
        items=(('PERSP', "Perspective", ""), ('ORTHO', "Orthographic User", "")),
    )

    @classmethod
    def poll(cls, context):
        return context.region_data is not None

    def execute(self, context):
        context.region_data.view_perspective = self.projection
        return {'FINISHED'}


# The main view's state while another quad view is maximized, per 3D View space.
_saved_main_view = {}

_VIEW_PROPS = ("view_location", "view_rotation", "view_distance", "view_perspective", "view_camera_zoom",
               "view_camera_offset", "is_orthographic_side_view")


def _copy_view(src, dst):
    for prop in _VIEW_PROPS:
        value = getattr(src, prop) if not isinstance(src, dict) else src[prop]
        if hasattr(value, "copy"):
            value = value.copy()
        setattr(dst, prop, value)


class MAXIMIZE_OT_viewport_maximize(Operator):
    """Maximize the viewport under the mouse; again to return to the four views (Alt+W)"""
    bl_idname = "maximize.viewport_maximize"
    bl_label = "Maximize Viewport Toggle"

    @classmethod
    def poll(cls, context):
        return context.area is not None and context.area.type == 'VIEW_3D'

    def invoke(self, context, event):
        area = context.area
        space = area.spaces.active
        main = space.region_3d
        key = space.as_pointer()
        main_region = next(r for r in reversed(area.regions) if r.type == 'WINDOW')

        if space.region_quadviews:
            # Which of the four views is under the mouse?
            under = None
            for region in area.regions:
                if region.type == 'WINDOW' and region.x <= event.mouse_x < region.x + region.width and \
                        region.y <= event.mouse_y < region.y + region.height:
                    under = region.data
            if under is None:
                under = context.region_data or main
            picked = None if under == main else {p: _snapshot(getattr(under, p)) for p in _VIEW_PROPS}
            with context.temp_override(region=main_region):
                bpy.ops.screen.region_quadview()
            if picked is not None:
                # The single view keeps the main view's data: show the picked view in it, and
                # remember the main view to restore it when going back to four views.
                _saved_main_view[key] = {p: _snapshot(getattr(main, p)) for p in _VIEW_PROPS}
                _copy_view(picked, space.region_3d)
            return {'FINISHED'}

        with context.temp_override(region=main_region):
            bpy.ops.screen.region_quadview()
        saved = _saved_main_view.pop(key, None)
        if saved is not None:
            _copy_view(saved, space.region_3d)
        return {'FINISHED'}

    def execute(self, _context):
        # Without a mouse position there is no view to pick: plain quad view toggle.
        return bpy.ops.screen.region_quadview()


def _snapshot(value):
    return value.copy() if hasattr(value, "copy") else value


class MAXIMIZE_OT_camera_from_view(Operator):
    """Create a camera that matches the current view and look through it (Ctrl+C)"""
    bl_idname = "maximize.camera_from_view"
    bl_label = "Create Camera From View"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.region_data is not None and context.mode == 'OBJECT'

    def execute(self, context):
        rv3d = context.region_data
        if rv3d.view_perspective == 'CAMERA':
            rv3d.view_perspective = 'PERSP'
        bpy.ops.object.camera_add()
        camera = context.active_object
        context.scene.camera = camera
        bpy.ops.view3d.camera_to_view()
        return {'FINISHED'}


def _open_editor_window(context, ui_type, setup=None):
    """Open a new window showing one editor, like Max's floating dialogs."""
    windows = set(context.window_manager.windows)
    bpy.ops.wm.window_new()
    new = [w for w in context.window_manager.windows if w not in windows]
    if not new:
        return False
    area = new[0].screen.areas[0]
    area.ui_type = ui_type
    if setup:
        setup(area.spaces.active)
    return True


class MAXIMIZE_OT_open_editor(Operator):
    """Open an editor in its own window"""
    bl_idname = "maximize.open_editor"
    bl_label = "Open Editor"

    ui_type: bpy.props.StringProperty(name="Editor", default='PROPERTIES')

    def execute(self, context):
        try:
            opened = _open_editor_window(context, self.ui_type)
        except TypeError:
            self.report({'ERROR'}, "Unknown editor: " + self.ui_type)
            return {'CANCELLED'}
        return {'FINISHED'} if opened else {'CANCELLED'}


class MAXIMIZE_OT_material_editor(Operator):
    """Open the material editor in its own window (M)"""
    bl_idname = "maximize.material_editor"
    bl_label = "Material Editor"

    def execute(self, context):
        return {'FINISHED'} if _open_editor_window(context, 'ShaderNodeTree') else {'CANCELLED'}


class MAXIMIZE_OT_render_setup(Operator):
    """Open the render settings in their own window (F10)"""
    bl_idname = "maximize.render_setup"
    bl_label = "Render Setup"

    def execute(self, context):
        def setup(space):
            space.context = 'RENDER'
        return {'FINISHED'} if _open_editor_window(context, 'PROPERTIES', setup) else {'CANCELLED'}


class MAXIMIZE_OT_angle_snap(Operator):
    """Toggle angle snap: rotations snap to the angle increment, moves stay free (A)"""
    bl_idname = "maximize.angle_snap"
    bl_label = "Angle Snap Toggle"

    def execute(self, context):
        ts = context.scene.tool_settings
        scene = context.scene
        if scene.get("maximize_angle_snap"):
            saved = scene["maximize_angle_snap"]
            ts.use_snap = bool(saved.get("use_snap", False))
            ts.use_snap_translate = bool(saved.get("translate", True))
            ts.use_snap_scale = bool(saved.get("scale", True))
            ts.use_snap_rotate = bool(saved.get("rotate", True))
            del scene["maximize_angle_snap"]
            self.report({'INFO'}, "Angle Snap: Off")
        else:
            scene["maximize_angle_snap"] = {
                "use_snap": ts.use_snap,
                "translate": ts.use_snap_translate,
                "scale": ts.use_snap_scale,
                "rotate": ts.use_snap_rotate,
            }
            if not ts.use_snap:
                # Snap only rotations, like Max's separate angle snap.
                ts.use_snap_translate = False
                ts.use_snap_scale = False
            ts.use_snap = True
            ts.use_snap_rotate = True
            self.report({'INFO'}, "Angle Snap: On ({:.0f}°)".format(
                ts.snap_angle_increment_3d * 57.29578))
        return {'FINISHED'}


# ------------------------------------------------------------------------------
# Max layout for new files

def _apply_layout():
    from .preferences import get_prefs
    prefs = get_prefs()
    if prefs is None or not prefs.use_startup_layout:
        return None
    scene = bpy.context.scene
    if scene is None or scene.get("maximize_layout"):
        return None

    units = scene.unit_settings
    units.system = 'METRIC'
    units.length_unit = 'CENTIMETERS'

    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type != 'VIEW_3D':
                continue
            space = area.spaces.active
            space.show_region_ui = True
            from .cameras import apply_viewport_defaults
            apply_viewport_defaults(space)
            region = next((r for r in area.regions if r.type == 'WINDOW'), None)
            if region is None:
                continue
            # Only the main viewport of the Layout workspace becomes a quad view.
            if area.width > 500 and not space.region_quadviews:
                with bpy.context.temp_override(window=window, area=area, region=region):
                    bpy.ops.screen.region_quadview()
    scene["maximize_layout"] = True
    # The sidebar tabs only exist once the sidebar has been drawn.
    bpy.app.timers.register(_select_max_tab, first_interval=0.5)
    return None


def _select_max_tab():
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type != 'VIEW_3D':
                continue
            for region in area.regions:
                if region.type == 'UI':
                    try:
                        region.active_panel_category = "Max"
                    except (AttributeError, TypeError, ValueError):
                        pass
                    area.tag_redraw()
    return None


# ------------------------------------------------------------------------------
# Viewport undo / redo (Shift+Z, Shift+Y): a short history of view changes per viewport.

_HISTORY_SIZE = 50
_view_history = {}  # region_3d pointer -> {"states": [...], "index": int, "restoring": bool}
# Max's active viewport, as far as Python can tell: the one whose view changed last.
_active_view = None  # region_3d pointer


def active_view_region(window):
    """(area, region) of the active viewport in `window`: the one changed last, else None."""
    if _active_view is None or window is None:
        return None
    for area in window.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW' and region.data is not None and                         region.data.as_pointer() == _active_view:
                    return area, region
    return None


def _view_state(rv3d):
    return (tuple(rv3d.view_location), tuple(rv3d.view_rotation), rv3d.view_distance,
            rv3d.view_perspective, rv3d.is_perspective)


def _set_view_state(rv3d, state):
    location, rotation, distance, perspective, is_perspective = state
    rv3d.view_location = location
    rv3d.view_rotation = rotation
    rv3d.view_distance = distance
    rv3d.view_perspective = perspective
    rv3d.is_perspective = is_perspective


def _track_views():
    global _active_view
    try:
        windows = bpy.context.window_manager.windows
    except AttributeError:
        return 0.3
    for window in windows:
        for area in window.screen.areas:
            if area.type != 'VIEW_3D':
                continue
            for region in area.regions:
                rv3d = region.data if region.type == 'WINDOW' else None
                if rv3d is None:
                    continue
                state = _view_state(rv3d)
                entry = _view_history.setdefault(rv3d.as_pointer(), {"states": [state], "index": 0})
                if entry["states"][entry["index"]] != state:
                    _active_view = rv3d.as_pointer()
                    del entry["states"][entry["index"] + 1:]
                    entry["states"].append(state)
                    del entry["states"][:-_HISTORY_SIZE]
                    entry["index"] = len(entry["states"]) - 1
    return 0.3


class MAXIMIZE_OT_view_history(Operator):
    """Undo or redo a view change in this viewport (Shift+Z, Shift+Y)"""
    bl_idname = "maximize.view_history"
    bl_label = "Undo View Change"

    redo: BoolProperty(name="Redo")

    @classmethod
    def poll(cls, context):
        return context.region_data is not None

    def execute(self, context):
        rv3d = context.region_data
        _track_views()
        entry = _view_history.get(rv3d.as_pointer())
        if entry is None:
            return {'CANCELLED'}
        index = entry["index"] + (1 if self.redo else -1)
        if not 0 <= index < len(entry["states"]):
            return {'CANCELLED'}
        entry["index"] = index
        _set_view_state(rv3d, entry["states"][index])
        context.area.tag_redraw()
        return {'FINISHED'}


@persistent
def _load_post(_filepath):
    if not bpy.data.filepath:
        # Wait until the window and its areas exist.
        bpy.app.timers.register(_apply_layout, first_interval=0.05)


classes = (
    MAXIMIZE_OT_view_projection,
    MAXIMIZE_OT_viewport_maximize,
    MAXIMIZE_OT_camera_from_view,
    MAXIMIZE_OT_open_editor,
    MAXIMIZE_OT_material_editor,
    MAXIMIZE_OT_render_setup,
    MAXIMIZE_OT_angle_snap,
    MAXIMIZE_OT_view_history,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.app.handlers.load_post.append(_load_post)
    bpy.app.timers.register(_track_views, first_interval=1.0, persistent=True)


def unregister():
    if bpy.app.timers.is_registered(_track_views):
        bpy.app.timers.unregister(_track_views)
    _view_history.clear()
    if _load_post in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(_load_post)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
