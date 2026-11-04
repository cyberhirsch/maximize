# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Hover highlight, as in Max: the object, or the vertex, edge, border, polygon or element under the
mouse lights up before you click.

Built as a gizmo that never takes the click: Blender calls `test_select` on every mouse move in the
view, the gizmo finds what is under the mouse there and draws it. Objects and elements show their
outer outline, as in Max: drawn from a mask of the shape on screen, so it follows the view. Nothing
tells the gizmo when the mouse leaves, so a timer watches the mouse while something is lit.
"""

import os
import sys

import bmesh
import bpy
import gpu
import numpy as np
from bpy.app.handlers import persistent
from bpy.types import Gizmo, GizmoGroup, Operator
from bpy_extras import view3d_utils
from gpu_extras.batch import batch_for_shader
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import intersect_point_line, tessellate_polygon

from .preferences import get_prefs
from .selection import current_level

COLOR = (1.0, 0.82, 0.25, 1.0)
FILL = (1.0, 0.82, 0.25, 0.22)
MAX_OBJECT_TRIS = 1_000_000
OUTLINE_PIXELS = 2.0
WATCH_SECONDS = 0.15

# Edit-mesh BVH trees by object name; cleared when the mesh changes.
_bvh_cache = {}
# What is highlighted now (for scripts and tests).
state = {"key": None}
# The view the highlight shows in: (window pointer, region x, y, width, height), or None once the
# mouse has left it. Every view of a quad view has its own gizmo; only this one draws.
_shown = None
_mouse = None
# The mask of the lit shape, kept until the view or the shape changes.
_mask = {"offscreen": None, "size": None, "key": None, "wanted": None}
_outline_shader = None
_outline_quad = None


@persistent
def _on_depsgraph_update(_scene, depsgraph):
    if not _bvh_cache:
        return
    for update in depsgraph.updates:
        if update.is_updated_geometry:
            _bvh_cache.clear()
            return


@persistent
def _on_change(*_args):
    _bvh_cache.clear()


def _ray(context, location):
    region, rv3d = context.region, context.region_data
    origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, location)
    direction = view3d_utils.region_2d_to_vector_3d(region, rv3d, location)
    return origin, direction


def _screen(context, co):
    return view3d_utils.location_3d_to_region_2d(context.region, context.region_data, co)


def _pick_object(context, location):
    origin, direction = _ray(context, location)
    depsgraph = context.evaluated_depsgraph_get()
    hit, _loc, _normal, _index, obj, _matrix = context.scene.ray_cast(depsgraph, origin, direction)
    if not hit or obj is None:
        return None, None
    obj = obj.original
    if obj.hide_select or not obj.visible_get():
        return None, None
    return ("OBJECT", obj.name), lambda: _object_shape(context, obj)


def _object_shape(context, obj):
    ob_eval = obj.evaluated_get(context.evaluated_depsgraph_get())
    mw = np.array(ob_eval.matrix_world)
    mesh = None
    if ob_eval.type == 'MESH':
        mesh = ob_eval.data
    elif ob_eval.type in {'CURVE', 'SURFACE', 'FONT', 'META'}:
        mesh = ob_eval.to_mesh()
    try:
        if mesh is not None and 0 < len(mesh.loop_triangles) <= MAX_OBJECT_TRIS:
            co = np.empty(len(mesh.vertices) * 3, dtype=np.float32)
            mesh.vertices.foreach_get("co", co)
            co = co.reshape(-1, 3) @ mw[:3, :3].T.astype(np.float32) + mw[:3, 3].astype(np.float32)
            idx = np.empty(len(mesh.loop_triangles) * 3, dtype=np.int32)
            mesh.loop_triangles.foreach_get("vertices", idx)
            return {"outline": (co, idx.reshape(-1, 3))}
    finally:
        if ob_eval.type != 'MESH' and mesh is not None:
            ob_eval.to_mesh_clear()
    # Huge objects and those without faces: the bounding box.
    corners = np.array([c[:] for c in ob_eval.bound_box]) @ mw[:3, :3].T + mw[:3, 3]
    box = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
    return {"lines": (corners.astype(np.float32), np.array(box, dtype=np.int32))}


def _bvh(obj, bm):
    tree = _bvh_cache.get(obj.name)
    if tree is None:
        tree = _bvh_cache[obj.name] = BVHTree.FromBMesh(bm)
    return tree


def _pick_subobject(context, location):
    level = current_level(context)
    origin, direction = _ray(context, location)
    best = None
    for obj in context.objects_in_mode_unique_data:
        bm = bmesh.from_edit_mesh(obj.data)
        if not bm.faces:
            continue
        inv = obj.matrix_world.inverted()
        local_origin = inv @ origin
        local_dir = (inv.to_3x3() @ direction).normalized()
        loc, _normal, index, _dist = _bvh(obj, bm).ray_cast(local_origin, local_dir)
        if loc is None:
            continue
        dist = (obj.matrix_world @ loc - origin).length
        if best is None or dist < best[0]:
            best = (dist, obj, bm, index)
    if best is None:
        return None, None
    _dist, obj, bm, index = best
    bm.faces.ensure_lookup_table()
    if index >= len(bm.faces):
        _bvh_cache.clear()
        return None, None
    face = bm.faces[index]
    if face.hide:
        return None, None
    mw = obj.matrix_world
    mouse = Vector(location)

    def screen(co):
        return _screen(context, mw @ co) or Vector((1e9, 1e9))

    if level == 'VERTEX':
        vert = min(face.verts, key=lambda v: (screen(v.co) - mouse).length)
        co = mw @ vert.co
        return ("VERT", obj.name, vert.index), lambda: {"points": [co]}

    def edge_distance(e):
        a, b = screen(e.verts[0].co), screen(e.verts[1].co)
        point, t = intersect_point_line(mouse, a, b)
        t = min(1.0, max(0.0, t))
        return (a.lerp(b, t) - mouse).length

    if level in {'EDGE', 'BORDER'}:
        edges = face.edges if level == 'EDGE' else [e for e in face.edges if e.is_boundary]
        if not edges:
            return None, None
        edge = min(edges, key=edge_distance)
        if level == 'EDGE':
            segs = [(mw @ edge.verts[0].co, mw @ edge.verts[1].co)]
            return ("EDGE", obj.name, edge.index), lambda: {"segments": segs}
        border = _border(edge)
        key = ("BORDER", obj.name, min(e.index for e in border))
        return key, lambda: {"segments": [(mw @ e.verts[0].co, mw @ e.verts[1].co) for e in border]}

    faces = [face] if level == 'POLYGON' else _element(face)
    key = ("FACE" if level == 'POLYGON' else "ELEMENT", obj.name, min(f.index for f in faces))
    return key, lambda: _faces_shape(mw, faces, level != 'POLYGON')


def pick_curve(context, location, radius=15.0):
    """Editable Spline: the vertex, segment or spline under the mouse (by level), as (key, shape)."""
    from .spline_tools import _polyline, _read, spline_level
    level = spline_level(context)
    mouse = Vector(location)
    best = None
    for obj in context.objects_in_mode_unique_data:
        if obj.type != 'CURVE':
            continue
        mw = obj.matrix_world
        for si, spline in enumerate(obj.data.splines):
            if spline.type != 'BEZIER' or spline.hide:
                continue
            points = _read(spline)
            if level == 'VERTEX':
                for pi, p in enumerate(points):
                    at = _screen(context, mw @ p.co)
                    if at is not None:
                        d = (at - mouse).length
                        if d < radius and (best is None or d < best[0]):
                            best = (d, obj, si, pi, None)
                continue
            poly = _polyline(points, spline.use_cyclic_u)
            for (u0, a), (u1, b) in zip(poly, poly[1:]):
                pa, pb = _screen(context, mw @ a), _screen(context, mw @ b)
                if pa is None or pb is None:
                    continue
                _point, t = intersect_point_line(mouse, pa, pb)
                t = min(1.0, max(0.0, t))
                d = (pa.lerp(pb, t) - mouse).length
                if d < radius and (best is None or d < best[0]):
                    best = (d, obj, si, int(u0), poly)
    if best is None:
        return None, None
    _d, obj, si, index, poly = best
    mw = obj.matrix_world
    if level == 'VERTEX':
        co = mw @ obj.data.splines[si].bezier_points[index].co
        return ("KNOT", obj.name, si, index), lambda: {"points": [co]}
    if level == 'SEGMENT':
        poly = [(u, co) for u, co in poly if index <= u <= index + 1]
        key = ("SEGMENT", obj.name, si, index)
    else:
        key = ("SPLINE", obj.name, si)
    segs = [(mw @ a, mw @ b) for (_u0, a), (_u1, b) in zip(poly, poly[1:])]
    return key, lambda: {"segments": segs}


def _border(edge):
    border = {edge}
    stack = [edge]
    while stack:
        e = stack.pop()
        for v in e.verts:
            for other in v.link_edges:
                if other.is_boundary and other not in border:
                    border.add(other)
                    stack.append(other)
    return border


def _element(face):
    element = {face}
    stack = [face]
    while stack:
        f = stack.pop()
        for e in f.edges:
            for other in e.link_faces:
                if other not in element and not other.hide:
                    element.add(other)
                    stack.append(other)
    return element


def _faces_shape(mw, faces, outline=False):
    tris = []
    segs = []
    for f in faces:
        co = [mw @ v.co for v in f.verts]
        if len(co) == 3:
            tris.append(co)
        else:
            tris += [[co[i] for i in tri] for tri in tessellate_polygon([co])]
        segs += [(co[i], co[(i + 1) % len(co)]) for i in range(len(co))]
    if outline:
        return {"tris": tris, "outline": (np.array(tris, dtype=np.float32).reshape(-1, 3), None)}
    return {"tris": tris, "segments": segs}


def _batches(shape):
    shader = gpu.shader.from_builtin('UNIFORM_COLOR')
    batches = []
    if "tris" in shape and shape["tris"]:
        pos = [c for tri in shape["tris"] for c in tri]
        batches.append(('TRIS', batch_for_shader(shader, 'TRIS', {"pos": pos})))
    if "outline" in shape:
        co, idx = shape["outline"]
        batches.append(('OUTLINE', batch_for_shader(shader, 'TRIS', {"pos": co}, indices=idx)))
    if "lines" in shape:
        co, idx = shape["lines"]
        batches.append(('LINES', batch_for_shader(shader, 'LINES', {"pos": co}, indices=idx)))
    if "segments" in shape:
        pos = [c for seg in shape["segments"] for c in seg]
        batches.append(('LINES', batch_for_shader(shader, 'LINES', {"pos": pos})))
    if "points" in shape:
        batches.append(('POINTS', batch_for_shader(shader, 'POINTS', {"pos": shape["points"]})))
    return shader, batches


def _shader_outline():
    """Draws the mask's outer edge: pixels outside the shape with the shape close by."""
    global _outline_shader, _outline_quad
    if _outline_shader is None:
        iface = gpu.types.GPUStageInterfaceInfo("maximize_hover_iface")
        iface.smooth('VEC2', "uv")
        info = gpu.types.GPUShaderCreateInfo()
        info.push_constant('VEC4', "color")
        info.push_constant('VEC2', "texel")
        info.sampler(0, 'FLOAT_2D', "mask")
        info.vertex_in(0, 'VEC2', "pos")
        info.vertex_out(iface)
        info.fragment_out(0, 'VEC4', "fragColor")
        info.vertex_source("void main() { uv = pos * 0.5 + 0.5; gl_Position = vec4(pos, 0.0, 1.0); }")
        info.fragment_source("""
void main() {
  if (texture(mask, uv).r > 0.5) {
    discard;
  }
  float near = 0.0;
  for (int i = 0; i < 12; i++) {
    float angle = float(i) * 0.5236;
    vec2 dir = vec2(cos(angle), sin(angle)) * texel;
    near += texture(mask, uv + dir).r + texture(mask, uv + dir * 0.5).r;
  }
  fragColor = vec4(color.rgb, color.a * clamp(near / 3.0, 0.0, 1.0));
}
""")
        _outline_shader = gpu.shader.create_from_info(info)
        _outline_quad = batch_for_shader(
            _outline_shader, 'TRIS',
            {"pos": ((-1.0, -1.0), (1.0, -1.0), (1.0, 1.0), (-1.0, -1.0), (1.0, 1.0), (-1.0, 1.0))})
    return _outline_shader, _outline_quad


def _render_mask():
    """Runs from a timer: rendering it inside the view's draw breaks the rest of that draw (Vulkan)."""
    wanted, _mask["wanted"] = _mask["wanted"], None
    if wanted is None:
        return None
    size, key, view_matrix, window_matrix, shader, batch = wanted
    if _mask["size"] != size:
        if _mask["offscreen"] is not None:
            _mask["offscreen"].free()
        _mask["offscreen"] = gpu.types.GPUOffScreen(*size)
        _mask["size"] = size
    with _mask["offscreen"].bind():
        gpu.state.active_framebuffer_get().clear(color=(0.0, 0.0, 0.0, 0.0))
        gpu.state.blend_set('NONE')
        gpu.state.depth_test_set('NONE')
        with gpu.matrix.push_pop(), gpu.matrix.push_pop_projection():
            gpu.matrix.load_matrix(view_matrix)
            gpu.matrix.load_projection_matrix(window_matrix)
            shader.uniform_float("color", (1.0, 1.0, 1.0, 1.0))
            batch.draw(shader)
    _mask["key"] = key
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()
    return None


def _draw_outline(context, shader, batch):
    region, rv3d = context.region, context.region_data
    size = (region.width, region.height)
    key = (size, id(batch), tuple(map(tuple, rv3d.perspective_matrix)))
    if _mask["key"] != key:
        # For the next redraw; this one shows the last mask (the view turned by a frame at most).
        _mask["wanted"] = (size, key, rv3d.view_matrix.copy(), rv3d.window_matrix.copy(), shader, batch)
        if not bpy.app.timers.is_registered(_render_mask):
            bpy.app.timers.register(_render_mask, first_interval=0.0)
    if _mask["offscreen"] is None or _mask["size"] != size or (_mask["key"] or (0, 0))[1] != id(batch):
        return
    gpu.state.blend_set('ALPHA')
    outline, quad = _shader_outline()
    pixels = OUTLINE_PIXELS * context.preferences.system.ui_scale
    outline.uniform_float("color", COLOR)
    outline.uniform_float("texel", (pixels / region.width, pixels / region.height))
    outline.uniform_sampler("mask", _mask["offscreen"].texture_color)
    quad.draw(outline)


def _region_key(context):
    region = context.region
    return (context.window.as_pointer(), region.x, region.y, region.width, region.height)


def _cursor_over_moritz():
    """False when another program's window is under the mouse (Windows): no mouse events come then,
    so the last position can still be in the view."""
    if sys.platform != 'win32' or bpy.app.use_event_simulate:
        return True
    try:
        import ctypes
        from ctypes import wintypes
        user32 = ctypes.WinDLL("user32")
        user32.WindowFromPoint.argtypes = (wintypes.POINT,)
        user32.WindowFromPoint.restype = wintypes.HWND
        user32.GetWindowThreadProcessId.argtypes = (wintypes.HWND, ctypes.POINTER(wintypes.DWORD))
        point, process = wintypes.POINT(), wintypes.DWORD()
        user32.GetCursorPos(ctypes.byref(point))
        user32.GetWindowThreadProcessId(user32.WindowFromPoint(point), ctypes.byref(process))
    except (OSError, AttributeError, ValueError):
        return True
    return process.value == os.getpid()


def _mouse_in_view(window):
    """Whether the mouse is still on the view that shows the highlight, not on a panel over it."""
    x, y = _mouse
    _ptr, rx, ry, width, height = _shown
    if not (rx <= x < rx + width and ry <= y < ry + height):
        return False
    for area in window.screen.areas:
        if area.x <= x < area.x + area.width and area.y <= y < area.y + area.height:
            for region in area.regions:
                if (region.type != 'WINDOW' and region.width > 1 and region.height > 1 and
                        region.x <= x < region.x + region.width and region.y <= y < region.y + region.height):
                    return False
    return True


def _hide(window):
    global _shown
    _shown = None
    state["key"] = None
    if window is not None:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()


def _watch_mouse():
    if _shown is None or state["key"] is None:
        return None
    window = next((w for w in bpy.context.window_manager.windows if w.as_pointer() == _shown[0]), None)
    if window is None:
        _hide(None)
        return None
    try:
        # An operator is the way to the window's mouse position: its event.
        with bpy.context.temp_override(window=window):
            bpy.ops.maximize.hover_mouse('INVOKE_DEFAULT')
    except (RuntimeError, ReferenceError):
        return WATCH_SECONDS
    if _mouse is None or (_mouse_in_view(window) and _cursor_over_moritz()):
        return WATCH_SECONDS
    _hide(window)
    return None


class MAXIMIZE_OT_hover_mouse(Operator):
    bl_idname = "maximize.hover_mouse"
    bl_label = "Hover Mouse Position"
    bl_options = {'INTERNAL'}

    def invoke(self, _context, event):
        global _mouse
        _mouse = (event.mouse_x, event.mouse_y)
        return {'FINISHED'}


class MAXIMIZE_GT_hover(Gizmo):
    bl_idname = "MAXIMIZE_GT_hover"

    def setup(self):
        self.key = None
        self.shader = None
        self.batches = []

    def test_select(self, context, location):
        try:
            if context.mode == 'OBJECT':
                key, shape = _pick_object(context, location)
            elif context.mode == 'EDIT_CURVE':
                key, shape = pick_curve(context, location)
            else:
                key, shape = _pick_subobject(context, location)
            if key != self.key:
                self.shader, self.batches = _batches(shape()) if shape else (None, [])
        except (ReferenceError, ValueError, IndexError):
            # The edit mesh was rebuilt under us: start again on the next mouse move.
            _bvh_cache.clear()
            key, self.shader, self.batches = None, None, []
        global _shown
        here = _region_key(context)
        if key != self.key or here != _shown:
            self.key = key
            _shown = here
            context.area.tag_redraw()
        state["key"] = key
        if key is not None and not bpy.app.timers.is_registered(_watch_mouse):
            bpy.app.timers.register(_watch_mouse, first_interval=WATCH_SECONDS)
        # Never take the click.
        return -1

    def draw(self, context):
        if not self.batches or _region_key(context) != _shown:
            return
        gpu.state.blend_set('ALPHA')
        gpu.state.depth_test_set('NONE')
        gpu.state.line_width_set(2.0)
        gpu.state.point_size_set(9.0)
        for kind, batch in self.batches:
            if kind == 'OUTLINE':
                _draw_outline(context, self.shader, batch)
                continue
            self.shader.uniform_float("color", FILL if kind == 'TRIS' else COLOR)
            batch.draw(self.shader)
        gpu.state.line_width_set(1.0)
        gpu.state.point_size_set(1.0)
        gpu.state.blend_set('NONE')


class MAXIMIZE_GGT_hover(GizmoGroup):
    bl_idname = "MAXIMIZE_GGT_hover"
    bl_label = "Hover Highlight"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}

    @classmethod
    def poll(cls, context):
        prefs = get_prefs(context)
        return prefs is not None and prefs.use_hover_highlight and \
            context.mode in {'OBJECT', 'EDIT_MESH', 'EDIT_CURVE'}

    def setup(self, _context):
        self.gizmos.new(MAXIMIZE_GT_hover.bl_idname)


classes = (
    MAXIMIZE_OT_hover_mouse,
    MAXIMIZE_GT_hover,
    MAXIMIZE_GGT_hover,
)

_HANDLERS = (
    (bpy.app.handlers.depsgraph_update_post, _on_depsgraph_update),
    (bpy.app.handlers.undo_post, _on_change),
    (bpy.app.handlers.redo_post, _on_change),
    (bpy.app.handlers.load_post, _on_change),
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    for handlers, fn in _HANDLERS:
        handlers.append(fn)


def unregister():
    global _outline_shader, _outline_quad
    if bpy.app.timers.is_registered(_watch_mouse):
        bpy.app.timers.unregister(_watch_mouse)
    if _mask["offscreen"] is not None:
        _mask["offscreen"].free()
    _mask.update(offscreen=None, size=None, key=None, wanted=None)
    if bpy.app.timers.is_registered(_render_mask):
        bpy.app.timers.unregister(_render_mask)
    _outline_shader = _outline_quad = None
    for handlers, fn in _HANDLERS:
        if fn in handlers:
            handlers.remove(fn)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    _bvh_cache.clear()
