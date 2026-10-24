# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Hover highlight, as in Max: the object, or the vertex, edge, border, polygon or element under the
mouse lights up before you click.

Built as a gizmo that never takes the click: Blender calls `test_select` on every mouse move, the
gizmo finds what is under the mouse there and draws it.
"""

import bmesh
import bpy
import gpu
import numpy as np
from bpy.app.handlers import persistent
from bpy.types import Gizmo, GizmoGroup
from bpy_extras import view3d_utils
from gpu_extras.batch import batch_for_shader
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import intersect_point_line, tessellate_polygon

from .preferences import get_prefs
from .selection import current_level

COLOR = (1.0, 0.82, 0.25, 1.0)
FILL = (1.0, 0.82, 0.25, 0.22)
MAX_OBJECT_EDGES = 300_000

# Edit-mesh BVH trees by object name; cleared when the mesh changes.
_bvh_cache = {}
# What is highlighted now (for scripts and tests).
state = {"key": None}


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
    mesh = ob_eval.data if ob_eval.type == 'MESH' else None
    if mesh is not None and 0 < len(mesh.edges) <= MAX_OBJECT_EDGES:
        co = np.empty(len(mesh.vertices) * 3, dtype=np.float32)
        mesh.vertices.foreach_get("co", co)
        co = co.reshape(-1, 3) @ mw[:3, :3].T.astype(np.float32) + mw[:3, 3].astype(np.float32)
        idx = np.empty(len(mesh.edges) * 2, dtype=np.int32)
        mesh.edges.foreach_get("vertices", idx)
        return {"lines": (co, idx.reshape(-1, 2))}
    # Big or non-mesh objects: the bounding box.
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
    return key, lambda: _faces_shape(mw, faces)


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


def _faces_shape(mw, faces):
    tris = []
    segs = []
    for f in faces:
        co = [mw @ v.co for v in f.verts]
        if len(co) == 3:
            tris.append(co)
        else:
            tris += [[co[i] for i in tri] for tri in tessellate_polygon([co])]
        segs += [(co[i], co[(i + 1) % len(co)]) for i in range(len(co))]
    return {"tris": tris, "segments": segs}


def _batches(shape):
    shader = gpu.shader.from_builtin('UNIFORM_COLOR')
    batches = []
    if "tris" in shape and shape["tris"]:
        pos = [c for tri in shape["tris"] for c in tri]
        batches.append(('TRIS', batch_for_shader(shader, 'TRIS', {"pos": pos})))
    if "lines" in shape:
        co, idx = shape["lines"]
        batches.append(('LINES', batch_for_shader(shader, 'LINES', {"pos": co}, indices=idx)))
    if "segments" in shape:
        pos = [c for seg in shape["segments"] for c in seg]
        batches.append(('LINES', batch_for_shader(shader, 'LINES', {"pos": pos})))
    if "points" in shape:
        batches.append(('POINTS', batch_for_shader(shader, 'POINTS', {"pos": shape["points"]})))
    return shader, batches


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
            else:
                key, shape = _pick_subobject(context, location)
            if key != self.key:
                self.shader, self.batches = _batches(shape()) if shape else (None, [])
        except (ReferenceError, ValueError, IndexError):
            # The edit mesh was rebuilt under us: start again on the next mouse move.
            _bvh_cache.clear()
            key, self.shader, self.batches = None, None, []
        if key != self.key:
            self.key = state["key"] = key
            context.area.tag_redraw()
        # Never take the click.
        return -1

    def draw(self, _context):
        if not self.batches:
            return
        gpu.state.blend_set('ALPHA')
        gpu.state.depth_test_set('NONE')
        gpu.state.line_width_set(2.0)
        gpu.state.point_size_set(9.0)
        for kind, batch in self.batches:
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
        return prefs is not None and prefs.use_hover_highlight and context.mode in {'OBJECT', 'EDIT_MESH'}

    def setup(self, _context):
        self.gizmos.new(MAXIMIZE_GT_hover.bl_idname)


classes = (
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
    for handlers, fn in _HANDLERS:
        if fn in handlers:
            handlers.remove(fn)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    _bvh_cache.clear()
