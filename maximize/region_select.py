# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Region selection by drag direction (Moritz keymap): left to right is window, right to left is
crossing, as with Max's "Auto Window/Crossing by Direction".

Window selects only what lies fully inside the rectangle. Objects count even when other objects
hide them (Max); sub-objects count only when visible, unless X-ray is on (Alt+X, Alt+Shift+X).
"""

import bmesh
import bpy
import gpu
import numpy as np
from bpy.props import EnumProperty
from bpy.types import Operator
from gpu_extras.batch import batch_for_shader

from .selection import current_level

MODES = (
    ('SET', "Set", "Replace the selection"),
    ('ADD', "Extend", "Add to the selection"),
    ('SUB', "Subtract", "Remove from the selection"),
    ('AND', "Intersect", "Keep only what is in both"),
)
_DASH = 6


def _combine(mode, current, target):
    if mode == 'SET':
        return set(target)
    if mode == 'ADD':
        return current | target
    if mode == 'SUB':
        return current - target
    return current & target


def project(region, rv3d, coords):
    """World coordinates (N, 3) to region pixels (N, 2); `valid` is False behind the view."""
    coords = np.asarray(coords, dtype=np.float64).reshape(-1, 3)
    h = np.c_[coords, np.ones(len(coords))] @ np.array(rv3d.perspective_matrix).T
    w = h[:, 3]
    valid = w > 1e-6
    w = np.where(valid, w, 1.0)
    xy = np.empty((len(coords), 2))
    xy[:, 0] = (h[:, 0] / w * 0.5 + 0.5) * region.width
    xy[:, 1] = (h[:, 1] / w * 0.5 + 0.5) * region.height
    return xy, valid


def _inside(xy, valid, rect):
    xmin, xmax, ymin, ymax = rect
    return valid & (xy[:, 0] >= xmin) & (xy[:, 0] <= xmax) & (xy[:, 1] >= ymin) & (xy[:, 1] <= ymax)


def _segment_hits_rect(a, b, rect):
    """Liang-Barsky: does the 2D segment a-b touch the rectangle?"""
    xmin, xmax, ymin, ymax = rect
    t0, t1 = 0.0, 1.0
    dx, dy = b[0] - a[0], b[1] - a[1]
    for p, q in ((-dx, a[0] - xmin), (dx, xmax - a[0]), (-dy, a[1] - ymin), (dy, ymax - a[1])):
        if p == 0.0:
            if q < 0.0:
                return False
            continue
        t = q / p
        if p < 0.0:
            t0 = max(t0, t)
        else:
            t1 = min(t1, t)
        if t0 > t1:
            return False
    return True


# ------------------------------------------------------------------------------
# Objects


def _object_points(obj, depsgraph):
    ob_eval = obj.evaluated_get(depsgraph)
    mw = np.array(ob_eval.matrix_world)
    corners = np.array([c[:] for c in ob_eval.bound_box])
    pts = None
    if ob_eval.type == 'MESH' and ob_eval.data and 0 < len(ob_eval.data.vertices) <= 500_000:
        mesh = ob_eval.data
        pts = np.empty(len(mesh.vertices) * 3)
        mesh.vertices.foreach_get("co", pts)
        pts = pts.reshape(-1, 3)
    local = pts if pts is not None else corners
    return local @ mw[:3, :3].T + mw[:3, 3]


def _objects_window(context, rect):
    region, rv3d = context.region, context.region_data
    depsgraph = context.evaluated_depsgraph_get()
    found = set()
    for obj in context.visible_objects:
        if obj.hide_select:
            continue
        xy, valid = project(region, rv3d, _object_points(obj, depsgraph))
        if len(xy) and _inside(xy, valid, rect).all():
            found.add(obj)
    return found


def _select_objects(context, rect, mode, window):
    if not window:
        bpy.ops.view3d.select_box(xmin=rect[0], xmax=rect[1], ymin=rect[2], ymax=rect[3],
                                  wait_for_input=False, mode=mode)
        return
    target = _objects_window(context, rect)
    current = {o for o in context.visible_objects if o.select_get()}
    final = _combine(mode, current, target)
    for obj in context.visible_objects:
        obj.select_set(obj in final)
    if mode != 'SUB' and target and context.view_layer.objects.active not in final:
        context.view_layer.objects.active = next(iter(target))


# ------------------------------------------------------------------------------
# Sub-objects


def _native_box(context, rect, select_mode):
    """Visible elements inside the rectangle, from Blender's own box select (respects X-ray)."""
    context.tool_settings.mesh_select_mode = select_mode
    bpy.ops.view3d.select_box(xmin=rect[0], xmax=rect[1], ymin=rect[2], ymax=rect[3],
                              wait_for_input=False, mode='SET')
    result = {}
    for obj in context.objects_in_mode_unique_data:
        bm = bmesh.from_edit_mesh(obj.data)
        seq = bm.verts if select_mode[0] else bm.faces
        result[obj] = {i for i, el in enumerate(seq) if el.select}
    return result


def _boundary_loops(edges):
    """Group boundary edges into connected borders."""
    edges = set(edges)
    loops = []
    while edges:
        stack = [edges.pop()]
        loop = set(stack)
        while stack:
            e = stack.pop()
            for v in e.verts:
                for other in v.link_edges:
                    if other in edges:
                        edges.discard(other)
                        loop.add(other)
                        stack.append(other)
        loops.append(loop)
    return loops


def _islands(bm):
    island_of = {}
    islands = []
    for f in bm.faces:
        if f in island_of or f.hide:
            continue
        idx = len(islands)
        island = [f]
        island_of[f] = idx
        stack = [f]
        while stack:
            face = stack.pop()
            for e in face.edges:
                for other in e.link_faces:
                    if other not in island_of and not other.hide:
                        island_of[other] = idx
                        island.append(other)
                        stack.append(other)
        islands.append(island)
    return islands


def _targets(context, obj, bm, level, rect, window, verts_in, faces_in):
    """Indices of the elements (verts, edges or faces for the level) the rectangle selects."""
    vin = verts_in
    if level == 'VERTEX':
        return vin
    if level in {'EDGE', 'BORDER'}:
        if window:
            edges = {e for e in bm.edges if not e.hide and e.verts[0].index in vin and e.verts[1].index in vin}
        else:
            edges = {e for e in bm.edges if not e.hide and (e.verts[0].index in vin or e.verts[1].index in vin)}
            # Edges that pass through the rectangle without a vertex inside it.
            mw = obj.matrix_world
            cand = {e for i in faces_in for e in bm.faces[i].edges} - edges
            if cand:
                cand = list(cand)
                co = [mw @ v.co for e in cand for v in e.verts]
                xy, valid = project(context.region, context.region_data, co)
                for k, e in enumerate(cand):
                    if valid[2 * k] and valid[2 * k + 1] and _segment_hits_rect(xy[2 * k], xy[2 * k + 1], rect):
                        edges.add(e)
        if level == 'EDGE':
            return {e.index for e in edges}
        # Border: whole open borders; window needs the whole border inside.
        boundary = [e for e in bm.edges if e.is_boundary and not e.hide]
        result = set()
        for loop in _boundary_loops(boundary):
            if (loop <= edges) if window else (loop & edges):
                result |= {e.index for e in loop}
        return result
    # Polygon and Element.
    if window:
        faces = {f.index for f in bm.faces if not f.hide and all(v.index in vin for v in f.verts)}
    else:
        faces = set(faces_in) | {f.index for f in bm.faces
                                 if not f.hide and any(v.index in vin for v in f.verts)}
    if level == 'POLYGON':
        return faces
    result = set()
    for island in _islands(bm):
        ids = {f.index for f in island}
        if (ids <= faces) if window else (ids & faces):
            result |= ids
    return result


def _select_subobjects(context, rect, mode, window):
    ts = context.tool_settings
    level = current_level(context)
    objs = list(context.objects_in_mode_unique_data)
    saved_mode = tuple(ts.mesh_select_mode)
    saved = {}
    for obj in objs:
        bm = bmesh.from_edit_mesh(obj.data)
        saved[obj] = ([v.select for v in bm.verts], [e.select for e in bm.edges], [f.select for f in bm.faces])

    verts_in = _native_box(context, rect, (True, False, False))
    faces_in = ({} if window or level == 'VERTEX' else _native_box(context, rect, (False, False, True)))
    ts.mesh_select_mode = saved_mode

    for obj in objs:
        bm = bmesh.from_edit_mesh(obj.data)
        bm.verts.index_update()
        bm.edges.index_update()
        bm.faces.index_update()
        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()
        bm.faces.ensure_lookup_table()
        sv, se, sf = saved[obj]
        target = _targets(context, obj, bm, level, rect, window, verts_in.get(obj, set()),
                          faces_in.get(obj, set()))
        domain = bm.verts if level == 'VERTEX' else bm.edges if level in {'EDGE', 'BORDER'} else bm.faces
        before = sv if level == 'VERTEX' else se if level in {'EDGE', 'BORDER'} else sf
        current = {i for i, on in enumerate(before) if on}
        final = _combine(mode, current, target)
        for seq in (bm.verts, bm.edges, bm.faces):
            for el in seq:
                el.select = False
        for i in final:
            domain[i].select_set(True)
        bm.select_flush_mode()
        bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)


# ------------------------------------------------------------------------------
# Operator


def _draw_rect(op, _context):
    (x0, y0), (x1, y1) = op.start, op.end
    corners = ((x0, y0), (x1, y0), (x1, y1), (x0, y1))
    lines = []
    for a, b in zip(corners, corners[1:] + corners[:1]):
        if op.end[0] >= op.start[0]:
            lines += [a, b]
            continue
        # Crossing: dashed, as in Max.
        length = max(abs(b[0] - a[0]), abs(b[1] - a[1]))
        steps = max(1, int(length // _DASH))
        for s in range(0, steps, 2):
            t0, t1 = s / steps, min(1.0, (s + 1) / steps)
            lines += [(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0),
                      (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)]
    shader = gpu.shader.from_builtin('UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'LINES', {"pos": lines})
    gpu.state.blend_set('ALPHA')
    shader.uniform_float("color", (1.0, 1.0, 1.0, 0.9))
    batch.draw(shader)
    gpu.state.blend_set('NONE')


class MAXIMIZE_OT_select_region(Operator):
    """Drag a selection rectangle: left to right selects what is fully inside (window), right to left
    also what it touches (crossing)"""
    bl_idname = "maximize.select_region"
    bl_label = "Region Select"
    bl_options = {'REGISTER', 'UNDO'}

    mode: EnumProperty(name="Mode", items=MODES, default='SET')

    @classmethod
    def poll(cls, context):
        return (context.area is not None and context.area.type == 'VIEW_3D' and
                context.region is not None and context.region.type == 'WINDOW' and
                context.mode in {'OBJECT', 'EDIT_MESH'})

    def invoke(self, context, event):
        region = context.region
        self.start = (event.mouse_prev_press_x - region.x, event.mouse_prev_press_y - region.y)
        self.end = (event.mouse_region_x, event.mouse_region_y)
        self._handle = bpy.types.SpaceView3D.draw_handler_add(_draw_rect, (self, context), 'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        region.tag_redraw()
        return {'RUNNING_MODAL'}

    def _finish(self, context):
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        context.region.tag_redraw()

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            self.end = (event.mouse_region_x, event.mouse_region_y)
            context.region.tag_redraw()
        elif event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            self.end = (event.mouse_region_x, event.mouse_region_y)
            self._finish(context)
            return self.select(context)
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            self._finish(context)
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}

    def select(self, context):
        (x0, y0), (x1, y1) = self.start, self.end
        rect = (int(min(x0, x1)), int(max(x0, x1)), int(min(y0, y1)), int(max(y0, y1)))
        window = x1 >= x0
        if context.mode == 'OBJECT':
            _select_objects(context, rect, self.mode, window)
        else:
            _select_subobjects(context, rect, self.mode, window)
        return {'FINISHED'}


classes = (
    MAXIMIZE_OT_select_region,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
