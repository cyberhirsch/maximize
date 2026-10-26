# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Max's Edit Poly tools that Blender lacks or has under another shape: Material IDs (Set ID,
Select ID with Clear Selection, select by name), Make Planar X / Y / Z, Create Shape, Outline,
Max-style vertex / edge / border Extrude, Extrude Along Spline, Hinge From Edge, Insert Vertex,
Slice Plane (Split, Reset Plane), Named Selections Copy / Paste, edge / vertex Crease and Weight,
Show Cage.

Max's material IDs are Blender's material slots, counted from 1. Crease and Weight are Blender's
own `crease_edge`, `crease_vert` and `bevel_weight_edge` attributes. Nothing new is stored.
"""

import math

import bmesh
import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, FloatVectorProperty, IntProperty, \
    PointerProperty, StringProperty
from bpy.types import GizmoGroup, Operator, Panel
from bpy_extras import view3d_utils
from mathutils import Euler, Matrix, Quaternion, Vector, geometry


def _edit_meshes(context):
    return [o for o in context.objects_in_mode_unique_data if o.type == 'MESH']


class _EditMesh:
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'


class MAXIMIZE_OT_set_material_id(_EditMesh, Operator):
    """Max's Set ID: give the selected polygons a material ID (material slot, from 1)"""
    bl_idname = "maximize.set_material_id"
    bl_label = "Set ID"

    material_id: IntProperty(name="ID", default=1, min=1, max=32767)

    def execute(self, context):
        count = 0
        for obj in _edit_meshes(context):
            bm = bmesh.from_edit_mesh(obj.data)
            for face in bm.faces:
                if face.select:
                    face.material_index = self.material_id - 1
                    count += 1
            bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)
        if not count:
            self.report({'WARNING'}, "Select polygons first")
            return {'CANCELLED'}
        return {'FINISHED'}


class MAXIMIZE_OT_select_material_id(_EditMesh, Operator):
    """Max's Select ID: select the polygons with a material ID"""
    bl_idname = "maximize.select_material_id"
    bl_label = "Select ID"

    material_id: IntProperty(name="ID", default=1, min=1, max=32767)
    clear: BoolProperty(name="Clear Selection", default=True,
                        description="Deselect everything else first (off: add to the selection)")

    def execute(self, context):
        for obj in _edit_meshes(context):
            bm = bmesh.from_edit_mesh(obj.data)
            if self.clear:
                for seq in (bm.verts, bm.edges, bm.faces):
                    for elem in seq:
                        elem.select = False
            for face in bm.faces:
                if face.material_index == self.material_id - 1:
                    face.select = True
            bm.select_flush_mode()
            bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)
        return {'FINISHED'}


class MAXIMIZE_OT_make_planar_axis(_EditMesh, Operator):
    """Max's Make Planar X / Y / Z: flatten the selection along an object axis, about its center"""
    bl_idname = "maximize.make_planar_axis"
    bl_label = "Make Planar Axis"

    axis: EnumProperty(name="Axis", items=(('X', "X", ""), ('Y', "Y", ""), ('Z', "Z", "")))

    def execute(self, context):
        settings = context.scene.tool_settings
        pivot = settings.transform_pivot_point
        settings.transform_pivot_point = 'MEDIAN_POINT'
        try:
            i = "XYZ".index(self.axis)
            value = [1.0, 1.0, 1.0]
            value[i] = 0.0
            bpy.ops.transform.resize(value=value, orient_type='LOCAL',
                                     constraint_axis=tuple(k == i for k in range(3)))
        finally:
            settings.transform_pivot_point = pivot
        return {'FINISHED'}


class MAXIMIZE_OT_create_shape(_EditMesh, Operator):
    """Max's Create Shape: make a spline object from the selected edges"""
    bl_idname = "maximize.create_shape"
    bl_label = "Create Shape"

    smooth: BoolProperty(name="Smooth", description="Smooth vertices instead of Linear (corners)")

    def execute(self, context):
        source = context.edit_object
        bm = bmesh.from_edit_mesh(source.data)
        edges = [e for e in bm.edges if e.select]
        if not edges:
            self.report({'WARNING'}, "Select edges first")
            return {'CANCELLED'}
        index = {}
        verts = []
        for e in edges:
            for v in e.verts:
                if v.index not in index:
                    index[v.index] = len(verts)
                    verts.append(v.co.copy())
        mesh = bpy.data.meshes.new(source.name + " Shape")
        mesh.from_pydata(verts, [(index[e.verts[0].index], index[e.verts[1].index]) for e in edges], [])
        shape = bpy.data.objects.new(mesh.name, mesh)
        shape.matrix_world = source.matrix_world
        for coll in source.users_collection:
            coll.objects.link(shape)
        bpy.ops.object.mode_set(mode='OBJECT')
        try:
            with context.temp_override(active_object=shape, object=shape, selected_objects=[shape],
                                       selected_editable_objects=[shape]):
                bpy.ops.object.convert(target='CURVE')
            curve = shape.data
            for spline in curve.splines:
                if spline.type != 'BEZIER':
                    spline.type = 'BEZIER'
                kind = 'AUTO' if self.smooth else 'VECTOR'
                for bp in spline.bezier_points:
                    bp.handle_left_type = bp.handle_right_type = kind
        finally:
            bpy.ops.object.mode_set(mode='EDIT')
        self.report({'INFO'}, "Created {:s}".format(shape.name))
        return {'FINISHED'}


def outline(bm, amount):
    """Max's Outline: move the outer edges of each selected polygon region outward (negative:
    inward) in the polygons' plane, so the border edges stay parallel. Returns the moved count."""
    selected = {f for f in bm.faces if f.select}
    moves = {}
    for face in selected:
        for loop in face.loops:
            edge = loop.edge
            if sum(1 for f in edge.link_faces if f in selected) != 1:
                continue
            a, b = loop.vert, loop.link_loop_next.vert
            # The loop runs counter-clockwise around the face normal: outward is to its right.
            out = (b.co - a.co).cross(face.normal)
            if out.length < 1e-12:
                continue
            out.normalize()
            for v in (a, b):
                moves.setdefault(v, []).append(out)
    for v, dirs in moves.items():
        # Unique edge directions; offsetting both edges by `amount` puts the corner on the bisector.
        unique = []
        for d in dirs:
            if all((d - u).length > 1e-6 for u in unique):
                unique.append(d)
        total = sum(unique, unique[0] * 0)
        if total.length < 1e-9:
            continue
        bisector = total.normalized()
        cos = max(min(bisector.dot(unique[0]), 1.0), 0.2)
        v.co += bisector * (amount / cos)
    return len(moves)


class MAXIMIZE_OT_outline(_EditMesh, Operator):
    """Max's Outline: move the outer edges of the selected polygons in their plane, adding no geometry"""
    bl_idname = "maximize.outline"
    bl_label = "Outline"

    amount: FloatProperty(name="Outline Amount", default=0.1, unit='LENGTH', step=1)

    def execute(self, context):
        count = 0
        for obj in _edit_meshes(context):
            bm = bmesh.from_edit_mesh(obj.data)
            bm.normal_update()
            count += outline(bm, self.amount)
            bmesh.update_edit_mesh(obj.data)
        if not count:
            self.report({'WARNING'}, "Select polygons first")
            return {'CANCELLED'}
        return {'FINISHED'}


def extrude_vertices(bm, verts, height, width):
    """Max's vertex Extrude: each vertex's edges are cut at `width` and the vertex rises by
    `height` along its normal, making a pyramid. Returns the new tips."""
    tips = []
    for v in list(verts):
        if not v.is_valid or not v.link_faces:
            continue
        origin, normal = v.co.copy(), v.normal.copy()
        result = bmesh.ops.bevel(bm, geom=[v], offset=width, offset_type='OFFSET', segments=1,
                                 profile=0.5, affect='VERTICES', clamp_overlap=True)
        faces = result["faces"]
        if not faces:
            continue
        poked = bmesh.ops.poke(bm, faces=faces)
        tip = poked["verts"][0]
        tip.co = origin + normal * height
        tips.append(tip)
    return tips


def extrude_edges(bm, edges, height, width):
    """Max's edge Extrude: each edge is cut at `width` on both sides and rises by `height`
    along its normal, making a ridge. Returns the new ridge vertices."""
    lines = []
    for e in edges:
        a, b = e.verts
        normal = (a.normal + b.normal)
        lines.append((a.co.copy(), b.co.copy(), normal.normalized() if normal.length else normal))
    result = bmesh.ops.bevel(bm, geom=list(edges), offset=width, offset_type='OFFSET', segments=2,
                             profile=0.5, affect='EDGES', clamp_overlap=True)
    ridge = []
    for v in result["verts"]:
        for a, b, normal in lines:
            ab = b - a
            t = 0.0 if ab.length < 1e-12 else max(0.0, min(1.0, (v.co - a).dot(ab) / ab.length_squared))
            if (a + ab * t - v.co).length < width * 0.25:
                ridge.append((v, normal))
                break
    for v, normal in ridge:
        v.co += normal * height
    return [v for v, _n in ridge]


def extrude_border(bm, edges, height, width):
    """Max's border Extrude: new polygons from the open border edges, raised by `height` along
    the border's normals and moved `width` outward in the surface. Returns the new vertices."""
    border = [e for e in edges if e.is_boundary]
    moves = {}
    for e in border:
        loop = e.link_loops[0]
        a, b = loop.vert, loop.link_loop_next.vert
        out = (b.co - a.co).cross(loop.face.normal)
        if out.length > 1e-12:
            out.normalize()
        for v in (a, b):
            moves.setdefault(v, []).append((out, loop.face.normal.copy()))
    if not border:
        return []
    result = bmesh.ops.extrude_edge_only(bm, edges=border)
    new_verts = [g for g in result["geom"] if isinstance(g, bmesh.types.BMVert)]
    # The extruded copies sit on the old ones; find each copy's source by position.
    for v in new_verts:
        source = min(moves, key=lambda s: (s.co - v.co).length_squared)
        outs = [o for o, _n in moves[source]]
        normals = [n for _o, n in moves[source]]
        unique = []
        for o in outs:
            if all((o - u).length > 1e-6 for u in unique):
                unique.append(o)
        out = sum(unique, unique[0] * 0)
        normal = sum(normals, normals[0] * 0)
        if out.length:
            # As in Outline: both border edges move by `width`, so the corner goes further.
            out = out.normalized() / max(min(out.normalized().dot(unique[0]), 1.0), 0.2)
        if normal.length:
            normal.normalize()
        v.co += normal * height + out * width
    return new_verts


class MAXIMIZE_OT_extrude_max(_EditMesh, Operator):
    """Max's vertex / edge / border Extrude: Height raises the result, Width cuts around a vertex
    or edge (a border moves outward by it)"""
    bl_idname = "maximize.extrude_max"
    bl_label = "Extrude"

    height: FloatProperty(name="Extrusion Height", default=0.1, unit='LENGTH', step=1)
    width: FloatProperty(name="Extrusion Base Width", default=0.05, min=0.0, unit='LENGTH', step=1)

    def execute(self, context):
        from .selection import current_level
        vertex_mode = context.tool_settings.mesh_select_mode[0]
        border = current_level(context) == 'BORDER'
        count = 0
        for obj in _edit_meshes(context):
            bm = bmesh.from_edit_mesh(obj.data)
            bm.normal_update()
            if vertex_mode:
                new = extrude_vertices(bm, [v for v in bm.verts if v.select], self.height, self.width)
            elif border:
                new = extrude_border(bm, [e for e in bm.edges if e.select], self.height, self.width)
            else:
                new = extrude_edges(bm, [e for e in bm.edges if e.select], self.height, self.width)
            for seq in (bm.verts, bm.edges, bm.faces):
                for elem in seq:
                    elem.select = False
            for v in new:
                v.select = True
            bm.select_flush_mode()
            bm.normal_update()
            bmesh.update_edit_mesh(obj.data)
            count += len(new)
        if not count:
            self.report({'WARNING'}, "Select vertices or edges on polygons first")
            return {'CANCELLED'}
        return {'FINISHED'}


# ------------------------------------------------------------------------------
# Extrude Along Spline and Hinge From Edge


def spline_samples(curve_obj, count, to_local):
    """`count` + 1 points spaced evenly along the first spline of `curve_obj`, in the space of
    `to_local`, with unit tangents."""
    spline = curve_obj.data.splines[0]
    world = to_local @ curve_obj.matrix_world
    dense = []
    if spline.type == 'BEZIER':
        pts = spline.bezier_points
        n = len(pts) if spline.use_cyclic_u else len(pts) - 1
        for i in range(n):
            a, b = pts[i], pts[(i + 1) % len(pts)]
            seg = geometry.interpolate_bezier(a.co, a.handle_right, b.handle_left, b.co, 24)
            dense.extend(seg if not dense else seg[1:])
    else:
        dense = [p.co.xyz for p in spline.points]
        if spline.use_cyclic_u:
            dense.append(dense[0])
    dense = [world @ Vector(c) for c in dense]
    lengths = [0.0]
    for a, b in zip(dense, dense[1:]):
        lengths.append(lengths[-1] + (b - a).length)
    total = lengths[-1] or 1.0
    out = []
    j = 0
    for k in range(count + 1):
        d = total * k / count
        while j < len(dense) - 2 and lengths[j + 1] < d:
            j += 1
        span = lengths[j + 1] - lengths[j] or 1.0
        out.append(dense[j].lerp(dense[j + 1], (d - lengths[j]) / span))
    tangents = []
    for k in range(len(out)):
        t = out[min(k + 1, len(out) - 1)] - out[max(k - 1, 0)]
        tangents.append(t.normalized() if t.length else Vector((0, 0, 1)))
    return out, tangents


def _regions(faces):
    """Connected groups of `faces`."""
    left = set(faces)
    groups = []
    while left:
        stack = [left.pop()]
        group = set(stack)
        while stack:
            f = stack.pop()
            for e in f.edges:
                for g in e.link_faces:
                    if g in left:
                        left.discard(g)
                        group.add(g)
                        stack.append(g)
        groups.append(group)
    return groups


def _extrude_steps(bm, faces, transforms):
    """Extrude `faces` once per matrix in `transforms`; each matrix maps the region's original
    vertex positions to that step. Returns the top faces."""
    top = list(faces)
    start = {v: v.co.copy() for f in top for v in f.verts}
    origin = {v: v for v in start}
    for m in transforms:
        result = bmesh.ops.extrude_face_region(bm, geom=top, use_keep_orig=False)
        new_verts = [g for g in result["geom"] if isinstance(g, bmesh.types.BMVert)]
        new_faces = [g for g in result["geom"] if isinstance(g, bmesh.types.BMFace)]
        # Map each new vertex to its original: the extruded copy sits where the old top was.
        tops = {v: v for f in top for v in f.verts}
        old_pos = {v.co.copy().freeze(): v for v in tops}
        for v in new_verts:
            source = old_pos.get(v.co.copy().freeze())
            if source is None:
                source = min(tops, key=lambda t: (t.co - v.co).length_squared)
            origin[v] = origin.get(source, source)
        for v in new_verts:
            v.co = m @ start[origin[v]]
        bmesh.ops.delete(bm, geom=[f for f in top if f.is_valid], context='FACES_ONLY')
        top = new_faces
    return top


def _rotation_between(a, b):
    return a.rotation_difference(b).to_matrix().to_4x4()


class MAXIMIZE_OT_extrude_along_spline(_EditMesh, Operator):
    """Max's Extrude Along Spline: extrude the selected polygons along a spline"""
    bl_idname = "maximize.extrude_along_spline"
    bl_label = "Extrude Along Spline"

    spline: StringProperty(name="Spline", description="The curve object to follow")
    segments: IntProperty(name="Segments", default=6, min=1, max=500)
    taper: FloatProperty(name="Taper Amount", default=0.0, min=-1.0, max=10.0)
    twist: FloatProperty(name="Twist", default=0.0, subtype='ANGLE')
    align: BoolProperty(name="Align to Face Normal", default=True,
                        description="Turn the spline so it leaves the polygons along their normal")

    def draw(self, context):
        layout = self.layout
        layout.prop_search(self, "spline", context.scene, "objects")
        for name in ("segments", "taper", "twist", "align"):
            layout.prop(self, name)

    def invoke(self, context, event):
        if not self.spline:
            curves = [o for o in context.selected_objects if o.type == 'CURVE']
            if curves:
                self.spline = curves[0].name
        if not self.spline:
            return context.window_manager.invoke_props_dialog(self)
        return self.execute(context)

    def execute(self, context):
        curve = bpy.data.objects.get(self.spline)
        if curve is None or curve.type != 'CURVE' or not curve.data.splines:
            self.report({'WARNING'}, "Pick a spline to extrude along")
            return {'CANCELLED'}
        obj = context.edit_object
        bm = bmesh.from_edit_mesh(obj.data)
        bm.normal_update()
        points, tangents = spline_samples(curve, self.segments, obj.matrix_world.inverted())
        regions = _regions([f for f in bm.faces if f.select])
        if not regions:
            self.report({'WARNING'}, "Select polygons first")
            return {'CANCELLED'}
        for region in regions:
            centre = sum((f.calc_center_median() for f in region), Vector()) / len(region)
            normal = sum((f.normal for f in region), Vector())
            normal = normal.normalized() if normal.length else Vector((0, 0, 1))
            # The path starts at the region's centre; aligned, its first tangent is the normal.
            align = _rotation_between(tangents[0], normal) if self.align else Matrix.Identity(4)
            steps = []
            for k in range(1, self.segments + 1):
                f = k / self.segments
                turn = align @ _rotation_between(tangents[0], tangents[k]) @ align.inverted()
                axis = (turn.to_3x3() @ normal).normalized()
                spin = Quaternion(axis, self.twist * f).to_matrix().to_4x4()
                scale = Matrix.Scale(max(1.0 + self.taper * f, 0.0), 4)
                offset = align.to_3x3() @ (points[k] - points[0])
                steps.append(Matrix.Translation(centre + offset) @ spin @ turn @ scale @
                             Matrix.Translation(-centre))
            _extrude_steps(bm, region, steps)
        bm.normal_update()
        bmesh.update_edit_mesh(obj.data)
        return {'FINISHED'}


def _pick_edge(context, event, edges, matrix):
    """The edge of `edges` nearest the mouse on screen, with the parameter 0..1 along it."""
    region, rv3d = context.region, context.region_data
    mouse = Vector((event.mouse_region_x, event.mouse_region_y))
    best = None
    for e in edges:
        a, b = (view3d_utils.location_3d_to_region_2d(region, rv3d, matrix @ v.co) for v in e.verts)
        if a is None or b is None:
            continue
        ab = b - a
        t = 0.0 if ab.length < 1e-6 else max(0.0, min(1.0, (mouse - a).dot(ab) / ab.length_squared))
        d = (a + ab * t - mouse).length
        if best is None or d < best[0]:
            best = (d, e, t)
    return (best[1], best[2]) if best and best[0] < 40 else (None, None)


class _PickEdgeOperator:
    """Modal: click an edge in the viewport, then `apply(bm, edge, t)` runs; Esc / right-click ends."""
    bl_options = {'REGISTER', 'UNDO'}
    hint = "Click an edge"

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH' and context.area is not None and context.area.type == 'VIEW_3D'

    def candidates(self, bm):
        return bm.edges

    def invoke(self, context, event):
        context.workspace.status_text_set(self.hint + " (Esc / right-click: done)")
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type in {'ESC', 'RIGHTMOUSE'} and event.value == 'PRESS':
            context.workspace.status_text_set(None)
            return {'FINISHED'} if self.picked else {'CANCELLED'}
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            obj = context.edit_object
            bm = bmesh.from_edit_mesh(obj.data)
            edge, t = _pick_edge(context, event, self.candidates(bm), obj.matrix_world)
            if edge is not None:
                self.apply(bm, edge, t)
                bmesh.update_edit_mesh(obj.data)
                self.picked = True
                if self.once:
                    context.workspace.status_text_set(None)
                    return {'FINISHED'}
            return {'RUNNING_MODAL'}
        return {'PASS_THROUGH'}

    picked = False
    once = False


def insert_vertex(bm, edge, t):
    """Max's Insert Vertex: a new vertex on `edge` at the parameter t (0..1)."""
    _new_edge, vert = bmesh.utils.edge_split(edge, edge.verts[0], t)
    return vert


class MAXIMIZE_OT_insert_vertex(_PickEdgeOperator, Operator):
    """Max's Insert Vertex: click on edges to add vertices there"""
    bl_idname = "maximize.insert_vertex"
    bl_label = "Insert Vertex"
    hint = "Click on an edge to insert a vertex"

    def apply(self, bm, edge, t):
        insert_vertex(bm, edge, t)


def hinge(bm, faces, edge, angle, segments):
    """Max's Hinge From Edge: extrude `faces` by rotating them about `edge` in `segments` steps."""
    a, b = (v.co.copy() for v in edge.verts)
    axis = (b - a).normalized()
    steps = [Matrix.Translation(a) @ Quaternion(axis, angle * k / segments).to_matrix().to_4x4() @
             Matrix.Translation(-a) for k in range(1, segments + 1)]
    top = _extrude_steps(bm, faces, steps)
    # The copies of the hinge edge stay on it: weld them back onto the hinge.
    on_hinge = [v for v in bm.verts if (v.co - a).cross(axis).length < 1e-6]
    bmesh.ops.remove_doubles(bm, verts=on_hinge, dist=1e-6)
    return [f for f in top if f.is_valid]


class MAXIMIZE_OT_hinge_from_edge(_PickEdgeOperator, Operator):
    """Max's Hinge From Edge: click the hinge edge; the selected polygons swing about it, extruding"""
    bl_idname = "maximize.hinge_from_edge"
    bl_label = "Hinge From Edge"
    hint = "Click the hinge edge"
    once = True

    angle: FloatProperty(name="Angle", default=math.radians(90.0), subtype='ANGLE')
    segments: IntProperty(name="Segments", default=1, min=1, max=100)
    hinge_index: IntProperty(name="Hinge Edge", default=-1, min=-1, options={'HIDDEN'})

    def apply(self, bm, edge, t):
        self.hinge_index = edge.index
        self._run(bm)

    def _run(self, bm):
        bm.edges.ensure_lookup_table()
        faces = [f for f in bm.faces if f.select]
        if not faces or not 0 <= self.hinge_index < len(bm.edges):
            return False
        hinge(bm, faces, bm.edges[self.hinge_index], self.angle, self.segments)
        bm.normal_update()
        return True

    def execute(self, context):
        obj = context.edit_object
        bm = bmesh.from_edit_mesh(obj.data)
        if not self._run(bm):
            self.report({'WARNING'}, "Select polygons and pick a hinge edge")
            return {'CANCELLED'}
        bmesh.update_edit_mesh(obj.data)
        return {'FINISHED'}


# ------------------------------------------------------------------------------
# Cap


def _border_loops(edges):
    """The selected open border edges, grouped into connected loops."""
    left = {e for e in edges if e.is_boundary}
    loops = []
    while left:
        stack = [left.pop()]
        loop = set(stack)
        while stack:
            e = stack.pop()
            for v in e.verts:
                for f in v.link_edges:
                    if f in left:
                        left.discard(f)
                        loop.add(f)
                        stack.append(f)
        loops.append(loop)
    return loops


def _select_only(bm, edges):
    for elem in (*bm.verts, *bm.edges, *bm.faces):
        elem.select = False
    for e in edges:
        e.select = True
    bm.select_flush_mode()


def _grid_fill(obj, loop):
    """Fill the border `loop` with a quad grid; an odd border gets one triangle. Returns success."""
    bm = bmesh.from_edit_mesh(obj.data)
    extra = None
    if len(loop) % 2:
        # Even out the border with a temporary vertex, fill, then dissolve it: the grid face
        # next to it becomes the one triangle.
        edge = max(loop, key=lambda e: e.calc_length())
        new_edge, extra = bmesh.utils.edge_split(edge, edge.verts[0], 0.5)
        loop = set(loop) | {new_edge}
    _select_only(bm, loop)
    bmesh.update_edit_mesh(obj.data)
    try:
        ok = bpy.ops.mesh.fill_grid() == {'FINISHED'}
    except RuntimeError:
        ok = False
    bm = bmesh.from_edit_mesh(obj.data)
    if extra is not None and extra.is_valid:
        # Merge the temporary vertex into a border neighbor: the wall face is whole again and
        # the grid face next to it becomes the triangle.
        neighbor = next(e.other_vert(extra) for e in extra.link_edges if e.is_boundary or
                        len(e.link_faces) == 2 and not all(f.select for f in e.link_faces))
        bmesh.ops.pointmerge(bm, verts=[extra, neighbor], merge_co=neighbor.co)
    bmesh.update_edit_mesh(obj.data)
    return ok


class MAXIMIZE_OT_cap(_EditMesh, Operator):
    """Cap the selected borders: a quad grid (Ctrl: one polygon, as in Max; Shift: an inset ring
    with a quad grid inside)"""
    bl_idname = "maximize.cap"
    bl_label = "Cap"

    mode: EnumProperty(name="Cap", items=(
        ('QUAD', "Quad Cap", "A grid of quads (an odd border gets one triangle)"),
        ('NGON', "Single Polygon", "One polygon, as Max's Cap (Ctrl)"),
        ('INSET', "Inset Quad Cap", "A ring of quads along the border, then a quad grid inside (Shift)")))
    ring: FloatProperty(name="Ring Width", default=0.2, min=0.01, max=0.9, subtype='FACTOR',
                        description="Inset ring width, as a part of the border's radius")

    def invoke(self, context, event):
        self.mode = 'NGON' if event.ctrl else 'INSET' if event.shift else 'QUAD'
        return self.execute(context)

    def execute(self, context):
        obj = context.edit_object
        bm = bmesh.from_edit_mesh(obj.data)
        loops = _border_loops([e for e in bm.edges if e.select])
        if not loops:
            self.report({'WARNING'}, "Select open borders first")
            return {'CANCELLED'}
        if self.mode == 'NGON':
            faces = []
            for loop in loops:
                faces += bmesh.ops.holes_fill(bm, edges=list(loop), sides=0)["faces"]
            _select_only(bm, [])
            for f in faces:
                f.select = True
            bm.select_flush_mode()
            bmesh.update_edit_mesh(obj.data)
            return {'FINISHED'}
        failed = 0
        for loop in loops:
            bm = bmesh.from_edit_mesh(obj.data)
            loop = {e for e in loop if e.is_valid}
            if self.mode == 'INSET' and len(loop) >= 3:
                face = bmesh.ops.holes_fill(bm, edges=list(loop), sides=0)["faces"][0]
                centre = face.calc_center_median()
                radius = sum((v.co - centre).length for v in face.verts) / len(face.verts)
                bmesh.ops.inset_region(bm, faces=[face], thickness=radius * self.ring, use_even_offset=True)
                inner = set(face.edges)
                bmesh.ops.delete(bm, geom=[face], context='FACES_ONLY')
                loop = {e for e in inner if e.is_valid}
            if not _grid_fill(obj, loop):
                bm = bmesh.from_edit_mesh(obj.data)
                bmesh.ops.holes_fill(bm, edges=[e for e in loop if e.is_valid], sides=0)
                bmesh.update_edit_mesh(obj.data)
                failed += 1
        if failed:
            self.report({'INFO'}, "{:d} border(s) got one polygon: no quad grid fits".format(failed))
        return {'FINISHED'}


# ------------------------------------------------------------------------------
# Slice Plane


def _selection_centre(bm):
    verts = [v for v in bm.verts if v.select] or list(bm.verts)
    return sum((v.co for v in verts), Vector()) / max(len(verts), 1)


def slice_plane(bm, co, no, split):
    """Max's Slice: cut every polygon (the selected ones, if any) with the plane; Split also
    separates the mesh along the cut."""
    faces = [f for f in bm.faces if f.select] or list(bm.faces)
    geom = list({v for f in faces for v in f.verts}) + list({e for f in faces for e in f.edges}) + faces
    result = bmesh.ops.bisect_plane(bm, geom=geom, plane_co=co, plane_no=no)
    cut = [g for g in result["geom_cut"] if isinstance(g, bmesh.types.BMEdge)]
    if split and cut:
        bmesh.ops.split_edges(bm, edges=cut)
    return len(cut)


class MAXIMIZE_OT_slice_plane(_EditMesh, Operator):
    """Max's Slice Plane: cut the polygons with a plane (Reset Plane: through the selection, flat)"""
    bl_idname = "maximize.slice_plane"
    bl_label = "Slice Plane"

    plane_co: FloatVectorProperty(name="Position", subtype='TRANSLATION', size=3)
    plane_no: FloatVectorProperty(name="Normal", subtype='DIRECTION', size=3, default=(0.0, 0.0, 1.0))
    split: BoolProperty(name="Split", description="Separate the mesh along the cut")
    reset: BoolProperty(name="Reset Plane", description="Put the plane back through the selection, facing up")

    def invoke(self, context, _event):
        self.reset = True
        return self.execute(context)

    def execute(self, context):
        obj = context.edit_object
        bm = bmesh.from_edit_mesh(obj.data)
        if self.reset:
            self.plane_co = _selection_centre(bm)
            self.plane_no = (0.0, 0.0, 1.0)
            self.reset = False
        if Vector(self.plane_no).length < 1e-9:
            return {'CANCELLED'}
        count = slice_plane(bm, Vector(self.plane_co), Vector(self.plane_no).normalized(), self.split)
        bmesh.update_edit_mesh(obj.data)
        if not count:
            self.report({'INFO'}, "The plane cuts nothing")
        return {'FINISHED'}


def _slice_plane_world(wm):
    """The live Slice Plane in world space: position and normal."""
    rot = Euler(wm.maximize_slice_rotation).to_matrix()
    return Vector(wm.maximize_slice_location), (rot @ Vector((0.0, 0.0, 1.0))).normalized()


def _reset_slice_plane(context):
    obj = context.edit_object
    bm = bmesh.from_edit_mesh(obj.data)
    wm = context.window_manager
    wm.maximize_slice_location = obj.matrix_world @ _selection_centre(bm)
    wm.maximize_slice_rotation = (0.0, 0.0, 0.0)


class MAXIMIZE_OT_slice_plane_mode(_EditMesh, Operator):
    """Max's Slice Plane button: show a plane to move and rotate in the viewport, then Slice"""
    bl_idname = "maximize.slice_plane_mode"
    bl_label = "Slice Plane"

    action: EnumProperty(items=(
        ('TOGGLE', "Toggle", "Show or hide the plane"),
        ('RESET', "Reset Plane", "Put the plane back through the selection, facing up"),
        ('SLICE', "Slice", "Cut with the plane"),
        ('SPLIT', "Slice and Split", "Cut with the plane and separate the mesh along the cut"),
    ), default='TOGGLE')

    def execute(self, context):
        wm = context.window_manager
        if self.action == 'TOGGLE':
            wm.maximize_slice_active = not wm.maximize_slice_active
            if wm.maximize_slice_active:
                _reset_slice_plane(context)
            return {'FINISHED'}
        if self.action == 'RESET':
            _reset_slice_plane(context)
            return {'FINISHED'}
        co, no = _slice_plane_world(wm)
        mw_inv = context.edit_object.matrix_world.inverted_safe()
        return bpy.ops.maximize.slice_plane(
            plane_co=mw_inv @ co, plane_no=(mw_inv.transposed().to_3x3() @ no).normalized(),
            split=self.action == 'SPLIT')


class MAXIMIZE_GGT_slice_plane(GizmoGroup):
    bl_idname = "MAXIMIZE_GGT_slice_plane"
    bl_label = "Slice Plane"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH' and context.window_manager.maximize_slice_active

    def setup(self, context):
        wm = context.window_manager
        self.plane = self.gizmos.new("GIZMO_GT_primitive_3d")
        self.plane.draw_style = 'PLANE'
        self.plane.color = (1.0, 0.85, 0.2)
        self.plane.alpha = 0.25
        self.plane.hide_select = True
        self.move = self.gizmos.new("GIZMO_GT_move_3d")
        self.move.draw_options = {'FILL', 'ALIGN_VIEW'}
        self.move.target_set_prop("offset", wm, "maximize_slice_location")
        self.dials = []
        for index, color in ((0, (1.0, 0.3, 0.3)), (1, (0.4, 1.0, 0.4))):
            dial = self.gizmos.new("GIZMO_GT_dial_3d")
            dial.target_set_prop("offset", wm, "maximize_slice_rotation", index=index)
            dial.color = color
            dial.alpha = 0.6
            dial.alpha_highlight = 1.0
            self.dials.append(dial)
        for gz in (self.move, *self.dials):
            gz.color_highlight = (1.0, 1.0, 0.6)
        self.draw_prepare(context)

    def draw_prepare(self, context):
        co, _no = _slice_plane_world(context.window_manager)
        rot = Euler(context.window_manager.maximize_slice_rotation).to_matrix().to_4x4()
        base = Matrix.Translation(co)
        self.plane.matrix_basis = base @ rot
        self.plane.scale_basis = 2.0
        self.move.matrix_basis = Matrix.Translation(co)
        # The dials turn the plane about its own X and Y axes.
        x_axis = Matrix.Rotation(math.radians(90.0), 4, 'Y')
        y_axis = Matrix.Rotation(math.radians(-90.0), 4, 'X')
        self.dials[0].matrix_basis = base @ x_axis
        self.dials[1].matrix_basis = base @ y_axis


def draw_slice_plane(layout, context):
    wm = context.window_manager
    row = layout.row(align=True)
    row.operator("maximize.slice_plane_mode", text="Slice Plane",
                 depress=wm.maximize_slice_active).action = 'TOGGLE'
    if wm.maximize_slice_active:
        row.operator("maximize.slice_plane_mode", text="Slice").action = 'SLICE'
        row.operator("maximize.slice_plane_mode", text="Split").action = 'SPLIT'
        row.operator("maximize.slice_plane_mode", text="Reset Plane").action = 'RESET'
    else:
        row.operator("maximize.slice_plane", text="QuickSlice Flat")


# ------------------------------------------------------------------------------
# Named Selections Copy / Paste, Crease and Weight, Show Cage

_named_clipboard = {}


class MAXIMIZE_OT_named_copy(_EditMesh, Operator):
    """Max's Named Selections Copy: copy a named sub-object selection set (by element number)"""
    bl_idname = "maximize.named_selection_copy"
    bl_label = "Copy"
    bl_options = {'REGISTER'}

    name: StringProperty(name="Set")

    def invoke(self, context, _event):
        from .selection import sub_set_names
        names = sub_set_names(context)
        if not self.name and names:
            self.name = names[-1][1]
        return self.execute(context)

    def execute(self, context):
        from .selection import _bm_seq, sub_set_names
        obj = context.edit_object
        bm = bmesh.from_edit_mesh(obj.data)
        for attr, label, domain in sub_set_names(context):
            if label == self.name:
                layer = _bm_seq(bm, domain).layers.int.get(attr)
                _named_clipboard.clear()
                _named_clipboard.update(name=label, domain=domain,
                                        indices=[e.index for e in _bm_seq(bm, domain) if e[layer]])
                self.report({'INFO'}, "Copied \"{:s}\"".format(label))
                return {'FINISHED'}
        self.report({'WARNING'}, "No named selection set to copy")
        return {'CANCELLED'}


class MAXIMIZE_OT_named_paste(_EditMesh, Operator):
    """Max's Named Selections Paste: paste the copied set into this mesh (same element numbers)"""
    bl_idname = "maximize.named_selection_paste"
    bl_label = "Paste"

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH' and bool(_named_clipboard)

    def execute(self, context):
        from .selection import SUB_PREFIX, _bm_seq
        obj = context.edit_object
        bm = bmesh.from_edit_mesh(obj.data)
        seq = _bm_seq(bm, _named_clipboard["domain"])
        seq.ensure_lookup_table()
        attr = SUB_PREFIX + _named_clipboard["name"]
        layer = seq.layers.int.get(attr) or seq.layers.int.new(attr)
        for e in seq:
            e[layer] = 0
        for i in _named_clipboard["indices"]:
            if i < len(seq):
                seq[i][layer] = 1
        bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)
        return {'FINISHED'}


_FLOAT_LAYERS = {"EDGE_CREASE": ("EDGE", "crease_edge"), "EDGE_WEIGHT": ("EDGE", "bevel_weight_edge"),
                 "VERTEX_CREASE": ("VERT", "crease_vert"), "VERTEX_WEIGHT": ("VERT", "bevel_weight_vert")}


class MAXIMIZE_OT_set_crease_weight(_EditMesh, Operator):
    """Max's Edge / Vertex Properties: set Crease or Weight of the selected edges or vertices"""
    bl_idname = "maximize.set_crease_weight"
    bl_label = "Set Crease / Weight"

    target: EnumProperty(name="Property", items=(
        ('EDGE_CREASE', "Edge Crease", ""), ('EDGE_WEIGHT', "Edge Weight", ""),
        ('VERTEX_CREASE', "Vertex Crease", ""), ('VERTEX_WEIGHT', "Vertex Weight", "")))
    value: FloatProperty(name="Value", default=1.0, min=0.0, max=1.0, subtype='FACTOR')

    def execute(self, context):
        domain, name = _FLOAT_LAYERS[self.target]
        count = 0
        for obj in _edit_meshes(context):
            bm = bmesh.from_edit_mesh(obj.data)
            seq = bm.edges if domain == "EDGE" else bm.verts
            layer = seq.layers.float.get(name) or seq.layers.float.new(name)
            for e in seq:
                if e.select:
                    e[layer] = self.value
                    count += 1
            bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)
        return {'FINISHED'} if count else {'CANCELLED'}


def _cage_modifiers(obj):
    return [m for m in obj.modifiers if m.type in {'SUBSURF', 'MULTIRES'}] if obj and obj.type == 'MESH' else []


def _get_show_cage(self):
    mods = _cage_modifiers(self)
    return bool(mods) and not any(m.show_on_cage for m in mods)


def _set_show_cage(self, value):
    # Max's Show Cage: the base mesh's wire shows around the smoothed result. Blender draws that
    # cage in Edit Mode when the smoothing is not applied on the cage.
    for m in _cage_modifiers(self):
        m.show_in_editmode = True
        m.show_on_cage = not value


_cage_handle = None


def _draw_cage():
    """Max's Show Cage colors: the base mesh's edges over the smoothed result, selected ones in their
    own color (Blender's own cage wire uses the theme's edit colors)."""
    context = bpy.context
    obj = context.edit_object
    if obj is None or obj.type != 'MESH' or not _get_show_cage(obj):
        return
    from . import preferences
    prefs = preferences.get_prefs(context)
    if prefs is None:
        return
    import gpu
    from gpu_extras.batch import batch_for_shader
    bm = bmesh.from_edit_mesh(obj.data)
    mw = obj.matrix_world
    lines, selected = [], []
    for e in bm.edges:
        if e.hide:
            continue
        pair = (mw @ e.verts[0].co, mw @ e.verts[1].co)
        (selected if e.select else lines).extend(pair)
    shader = gpu.shader.from_builtin('POLYLINE_UNIFORM_COLOR')
    region = context.region
    shader.uniform_float("viewportSize", (region.width, region.height))
    shader.uniform_float("lineWidth", 1.5)
    gpu.state.depth_test_set('LESS_EQUAL')
    gpu.state.blend_set('ALPHA')
    for points, color in ((lines, prefs.cage_color), (selected, prefs.cage_selected_color)):
        if points:
            shader.uniform_float("color", (*color, 1.0))
            batch_for_shader(shader, 'LINES', {"pos": points}).draw(shader)
    gpu.state.depth_test_set('NONE')
    gpu.state.blend_set('NONE')


def draw_edge_properties(layout, level):
    row = layout.row(align=True)
    if level == 'VERTEX':
        row.operator("maximize.set_crease_weight", text="Crease").target = 'VERTEX_CREASE'
        row.operator("maximize.set_crease_weight", text="Weight").target = 'VERTEX_WEIGHT'
    else:
        row.operator("maximize.set_crease_weight", text="Crease").target = 'EDGE_CREASE'
        row.operator("maximize.set_crease_weight", text="Weight").target = 'EDGE_WEIGHT'


def draw_extras(layout, context):
    """Edit Geometry extras: Slice Plane, Named Selections, Show Cage."""
    draw_slice_plane(layout, context)
    row = layout.row(align=True)
    row.label(text="Named Selections:")
    row.operator("maximize.named_selection_copy")
    row.operator("maximize.named_selection_paste")
    obj = context.edit_object
    if _cage_modifiers(obj):
        row = layout.row(align=True)
        row.prop(obj, "maximize_show_cage")
        from . import preferences
        prefs = preferences.get_prefs(context)
        if prefs is not None:
            row.prop(prefs, "cage_color", text="")
            row.prop(prefs, "cage_selected_color", text="")


class MAXIMIZE_PT_material_ids(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Max"
    bl_label = "Polygon: Material IDs"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH' and context.tool_settings.mesh_select_mode[2]

    def draw(self, context):
        draw_material_ids(self.layout, context)


def _material_items(_self, context):
    obj = context.edit_object if context else None
    if obj is None:
        return [('1', "(none)", "")]
    return [(str(i + 1), "{:d}: {:s}".format(i + 1, s.material.name if s.material else "(empty)"), "")
            for i, s in enumerate(obj.material_slots)] or [('1', "(no materials)", "")]


class MAXIMIZE_OT_select_material_name(_EditMesh, Operator):
    """Max's select by name: select the polygons that use a material"""
    bl_idname = "maximize.select_material_name"
    bl_label = "Select By Name"
    bl_property = "material"

    material: EnumProperty(name="Material", items=_material_items)
    clear: BoolProperty(name="Clear Selection", default=True)

    def invoke(self, context, _event):
        context.window_manager.invoke_search_popup(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        return bpy.ops.maximize.select_material_id(material_id=int(self.material), clear=self.clear)


def draw_material_ids(layout, context):
    wm = context.window_manager
    row = layout.row(align=True)
    row.operator("maximize.set_material_id").material_id = wm.maximize_material_id
    row.prop(wm, "maximize_material_id", text="")
    row = layout.row(align=True)
    op = row.operator("maximize.select_material_id")
    op.material_id = wm.maximize_material_id
    op.clear = wm.maximize_material_clear
    row.prop(wm, "maximize_material_clear", text="Clear Selection")
    layout.operator("maximize.select_material_name").clear = wm.maximize_material_clear


classes = (
    MAXIMIZE_OT_set_material_id,
    MAXIMIZE_OT_select_material_id,
    MAXIMIZE_OT_make_planar_axis,
    MAXIMIZE_OT_create_shape,
    MAXIMIZE_OT_outline,
    MAXIMIZE_OT_extrude_max,
    MAXIMIZE_OT_extrude_along_spline,
    MAXIMIZE_OT_insert_vertex,
    MAXIMIZE_OT_hinge_from_edge,
    MAXIMIZE_OT_slice_plane,
    MAXIMIZE_OT_slice_plane_mode,
    MAXIMIZE_GGT_slice_plane,
    MAXIMIZE_OT_cap,
    MAXIMIZE_OT_named_copy,
    MAXIMIZE_OT_named_paste,
    MAXIMIZE_OT_set_crease_weight,
    MAXIMIZE_OT_select_material_name,
    MAXIMIZE_PT_material_ids,
)


def register():
    bpy.types.WindowManager.maximize_material_id = IntProperty(name="ID", default=1, min=1, max=32767)
    bpy.types.WindowManager.maximize_material_clear = BoolProperty(name="Clear Selection", default=True)
    bpy.types.WindowManager.maximize_slice_active = BoolProperty(name="Slice Plane")
    bpy.types.WindowManager.maximize_slice_location = FloatVectorProperty(
        name="Slice Plane Position", subtype='TRANSLATION', size=3)
    bpy.types.WindowManager.maximize_slice_rotation = FloatVectorProperty(
        name="Slice Plane Rotation", subtype='EULER', size=3)
    bpy.types.Object.maximize_show_cage = BoolProperty(
        name="Show Cage", get=_get_show_cage, set=_set_show_cage,
        description="Show the base mesh's wire around the smoothed result (TurboSmooth / Multires)")
    for cls in classes:
        bpy.utils.register_class(cls)
    global _cage_handle
    if not bpy.app.background:
        _cage_handle = bpy.types.SpaceView3D.draw_handler_add(_draw_cage, (), 'WINDOW', 'POST_VIEW')


def unregister():
    global _cage_handle
    if _cage_handle is not None:
        bpy.types.SpaceView3D.draw_handler_remove(_cage_handle, 'WINDOW')
        _cage_handle = None
    del bpy.types.Object.maximize_show_cage
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.WindowManager.maximize_slice_rotation
    del bpy.types.WindowManager.maximize_slice_location
    del bpy.types.WindowManager.maximize_slice_active
    del bpy.types.WindowManager.maximize_material_clear
    del bpy.types.WindowManager.maximize_material_id
