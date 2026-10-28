# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Max's Smart Extrude: extrude the selected polygons along their normal; pushed into the mesh they
cut a pocket (or a hole when they come out the other side), and where they run into other
geometry the two are merged.

Out into free space it is a plain extrude (the quads stay as they are). Inward, or when the
extrusion hits the mesh, the extruded shape is cut away from (inward) or joined to (outward) the
mesh with the exact boolean. The drag shows a plain extrusion; the result is worked out when you
let go, as one undo step.
"""

import bmesh
import bpy
from bpy.props import BoolProperty, FloatProperty
from bpy.types import Operator
from bpy_extras import view3d_utils
from mathutils import Vector
from mathutils.bvhtree import BVHTree

# The extruded shape starts this much (of the mesh size) outside the surface, so its base doesn't lie
# in the faces it cuts.
_SKIN = 1e-4


def _selected_faces(bm):
    return [f for f in bm.faces if f.select and not f.hide]


def _direction(faces):
    normal = sum((f.normal * f.calc_area() for f in faces), Vector())
    return normal.normalized() if normal.length > 1e-12 else Vector((0.0, 0.0, 1.0))


def _size(bm):
    if not bm.verts:
        return 1.0
    lo = Vector(map(min, *(v.co for v in bm.verts))) if len(bm.verts) > 1 else bm.verts[0].co.copy()
    hi = Vector(map(max, *(v.co for v in bm.verts))) if len(bm.verts) > 1 else bm.verts[0].co.copy()
    return max((hi - lo).length, 1e-6)


def _hits(bm, faces, offset):
    """Whether the extrusion by `offset` runs into the rest of the mesh."""
    selected = set(faces)
    others = [f for f in bm.faces if f not in selected and not f.hide]
    if not others:
        return False
    index = {v: i for i, v in enumerate(bm.verts)}
    tree = BVHTree.FromPolygons([v.co for v in bm.verts], [[index[v] for v in f.verts] for f in others])
    length = offset.length
    direction = offset.normalized()
    for face in faces:
        center = face.calc_center_median()
        # The face's center and its corners pulled a little toward it, so the rays leave from inside
        # the face and don't touch the neighbors at its edges.
        for point in [center] + [v.co.lerp(center, 0.02) for v in face.verts]:
            start = point + direction * (length * 1e-4)
            hit = tree.ray_cast(start, direction, length * (1.0 - 2e-4))
            if hit[0] is not None:
                return True
    # Inward, the walls can also run along the neighbors (a whole side pushed in).
    return offset.dot(_direction(faces)) < 0.0


def _plain_extrude(bm, faces, offset):
    result = bmesh.ops.extrude_face_region(bm, geom=faces)
    verts = [e for e in result["geom"] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=offset, verts=verts)
    bmesh.ops.delete(bm, geom=faces, context='FACES')
    for f in bm.faces:
        f.select = False
    for e in result["geom"]:
        if isinstance(e, bmesh.types.BMFace):
            e.select = True
    bm.select_flush(True)


def _widening(faces, offset):
    """Where pushing in would run the walls along a neighbor (a whole side pushed in), the cut is
    made a little wider there: past those edges is outside the mesh, and walls lying exactly in the
    neighbor's plane trip up the boolean. Returns {vertex: outward direction}."""
    selected = set(faces)
    direction = offset.normalized()
    out = {}
    for face in faces:
        center = face.calc_center_median()
        for edge in face.edges:
            others = [f for f in edge.link_faces if f not in selected]
            if len(others) != 1:
                continue
            neighbor = others[0]
            mid = (edge.verts[0].co + edge.verts[1].co) / 2.0
            along = abs(neighbor.normal.dot(direction)) < 1e-3
            ahead = (neighbor.calc_center_median() - mid).dot(direction) > 0.0
            if not (along and ahead):
                continue
            tangent = (edge.verts[1].co - edge.verts[0].co).normalized()
            away = mid - center
            away -= tangent * away.dot(tangent)
            if away.length < 1e-12:
                continue
            for v in edge.verts:
                out[v] = out.get(v, Vector()) + away.normalized()
    return out


def _footprint(faces):
    """The selected polygons as a tree to cast rays at (they stay where they are while the mesh
    changes)."""
    verts = []
    polys = []
    for f in faces:
        polys.append(list(range(len(verts), len(verts) + len(f.verts))))
        verts.extend(v.co.copy() for v in f.verts)
    return BVHTree.FromPolygons(verts, polys)


def _in_extrusion(footprint, offset, skin, point):
    """Whether `point` is inside the space the polygons sweep through when moved by `offset`."""
    length = offset.length
    hit = footprint.ray_cast(point, -offset.normalized(), length + skin)
    return hit[0] is not None and hit[3] > skin * 0.5


def _cap_plane(faces, offset):
    center = sum((f.calc_center_median() for f in faces), Vector()) / len(faces)
    return center + offset, offset.normalized()


def smart_extrude(obj, offset):
    """Extrude the selected polygons of `obj` (in Edit Mode) by `offset`. Returns 'PLAIN', 'CUT',
    'MERGE' or None (nothing selected)."""
    bm = bmesh.from_edit_mesh(obj.data)
    faces = _selected_faces(bm)
    if not faces or offset.length < 1e-9:
        return None
    if not _hits(bm, faces, offset):
        _plain_extrude(bm, faces, offset)
        bmesh.update_edit_mesh(obj.data)
        return 'PLAIN'
    inward = offset.dot(_direction(faces)) < 0.0
    cap_point, cap_normal = _cap_plane(faces, offset)
    skin = _size(bm) * _SKIN
    back = -offset.normalized() * skin
    footprint = _footprint(faces)
    # The extruded shape as a closed solid of its own: the faces copied, moved a little back out of
    # the surface, and extruded past the original by `offset`.
    widen = _widening(faces, offset) if inward else {}
    copied = bmesh.ops.duplicate(bm, geom=faces)
    base = [e for e in copied["geom"] if isinstance(e, bmesh.types.BMFace)]
    base_verts = list({v for f in base for v in f.verts})
    bmesh.ops.translate(bm, vec=back, verts=base_verts)
    for vert, out in widen.items():
        copied["vert_map"][vert].co += out * (skin * 20.0)
    extruded = bmesh.ops.extrude_face_region(bm, geom=base, use_keep_orig=True)
    moved = [e for e in extruded["geom"] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=offset - back, verts=moved)
    solid = base + [e for e in extruded["geom"] if isinstance(e, bmesh.types.BMFace)]
    bmesh.ops.recalc_face_normals(bm, faces=solid)
    for f in bm.faces:
        f.select = False
    for f in solid:
        f.select = True
    bm.select_flush(True)
    bmesh.update_edit_mesh(obj.data)
    bpy.ops.mesh.intersect_boolean(operation='DIFFERENCE' if inward else 'UNION', use_swap=False,
                                   use_self=False, solver='EXACT')
    bm = bmesh.from_edit_mesh(obj.data)
    if inward:
        # The cut keeps the cutter's faces facing as they were, into the material: turn the ones
        # lining the cut toward it.
        step = skin * 5.0

        def cut_away(point):
            return _in_extrusion(footprint, offset, skin, point)
        wrong = [f for f in bm.faces if cut_away(f.calc_center_median() - f.normal * step)
                 and not cut_away(f.calc_center_median() + f.normal * step)]
        bmesh.ops.reverse_faces(bm, faces=wrong)
    # Max leaves the extruded polygons selected: those on the cap's plane.
    tolerance = skin * 10.0
    for f in bm.faces:
        on_cap = abs((f.calc_center_median() - cap_point).dot(cap_normal)) < tolerance and \
            abs(abs(f.normal.dot(cap_normal)) - 1.0) < 1e-3
        f.select = on_cap
    bm.select_flush(True)
    bmesh.update_edit_mesh(obj.data)
    return 'CUT' if inward else 'MERGE'


class MAXIMIZE_OT_smart_extrude(Operator):
    """Smart Extrude: drag the selected polygons along their normal; into the mesh they cut a pocket
    or a hole, into other geometry they merge with it"""
    bl_idname = "maximize.smart_extrude"
    bl_label = "Smart Extrude"
    bl_options = {'REGISTER', 'UNDO', 'GRAB_CURSOR', 'BLOCKING'}

    distance: FloatProperty(name="Distance", subtype='DISTANCE', default=0.0,
                            description="How far along the normal (negative goes into the mesh)")
    release_confirm: BoolProperty(name="Confirm on Release", options={'HIDDEN', 'SKIP_SAVE'},
                                  description="Releasing the mouse button ends the drag")

    @classmethod
    def poll(cls, context):
        obj = context.edit_object
        return obj is not None and obj.type == 'MESH' and context.tool_settings.mesh_select_mode[2]

    def execute(self, context):
        obj = context.edit_object
        bm = bmesh.from_edit_mesh(obj.data)
        faces = _selected_faces(bm)
        if not faces:
            self.report({'WARNING'}, "Select polygons first")
            return {'CANCELLED'}
        result = smart_extrude(obj, _direction(faces) * self.distance)
        return {'FINISHED'} if result else {'CANCELLED'}

    def invoke(self, context, event):
        obj = context.edit_object
        bm = bmesh.from_edit_mesh(obj.data)
        faces = _selected_faces(bm)
        if not faces or context.region_data is None:
            return self.execute(context)
        self._direction = _direction(faces)
        self._center = sum((f.calc_center_median() for f in faces), Vector()) / len(faces)
        # The mesh as it was, to go back to when the drag ends.
        self._before = bpy.data.meshes.new("Smart Extrude")
        bm.to_mesh(self._before)
        # The preview: a plain extrusion that the drag moves.
        result = bmesh.ops.extrude_face_region(bm, geom=faces)
        bmesh.ops.delete(bm, geom=faces, context='FACES')
        self._moving = [e for e in result["geom"] if isinstance(e, bmesh.types.BMVert)]
        self._origin = [v.co.copy() for v in self._moving]
        bmesh.update_edit_mesh(obj.data)
        # One unit along the normal, on screen.
        region, rv3d = context.region, context.region_data
        world = obj.matrix_world
        a = view3d_utils.location_3d_to_region_2d(region, rv3d, world @ self._center)
        b = view3d_utils.location_3d_to_region_2d(region, rv3d, world @ (self._center + self._direction))
        if a is None or b is None or (b - a).length < 1e-3:
            a, b = Vector((0.0, 0.0)), Vector((0.0, 100.0))
        self._screen_axis = b - a
        self._mouse = Vector((event.mouse_region_x, event.mouse_region_y))
        self.distance = 0.0
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def _restore(self, context):
        obj = context.edit_object
        bm = bmesh.from_edit_mesh(obj.data)
        bm.clear()
        bm.from_mesh(self._before)
        bmesh.update_edit_mesh(obj.data)
        bpy.data.meshes.remove(self._before)
        context.area.header_text_set(None)

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            mouse = Vector((event.mouse_region_x, event.mouse_region_y))
            axis = self._screen_axis
            self.distance = (mouse - self._mouse).dot(axis) / axis.length_squared
            if event.ctrl:
                # Ctrl: in steps of a tenth of a unit.
                self.distance = round(self.distance, 1)
            obj = context.edit_object
            offset = self._direction * self.distance
            for v, co in zip(self._moving, self._origin):
                v.co = co + offset
            bmesh.update_edit_mesh(obj.data, loop_triangles=True, destructive=False)
            context.area.header_text_set("Smart Extrude: {:.4f}  (Ctrl: steps; into the mesh cuts, into geometry "
                                         "merges)".format(self.distance))
        elif (event.type in {'LEFTMOUSE', 'RET', 'NUMPAD_ENTER'} and event.value == 'PRESS' or
              event.type == 'LEFTMOUSE' and event.value == 'RELEASE' and self.release_confirm):
            self._restore(context)
            return self.execute(context)
        elif event.type in {'RIGHTMOUSE', 'ESC'} and event.value == 'PRESS':
            self._restore(context)
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}


# The Move tool (and the Transform tool, which has the move handles).
_MOVE_TOOLS = {"builtin.move", "builtin.transform"}


class MAXIMIZE_OT_smart_extrude_drag(Operator):
    """Shift+drag of polygons with the Move tool: Smart Extrude, as in Max"""
    bl_idname = "maximize.smart_extrude_drag"
    bl_label = "Smart Extrude (Shift+Drag)"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        obj = context.edit_object
        if obj is None or obj.type != 'MESH' or not context.tool_settings.mesh_select_mode[2]:
            return False
        if context.region_data is None or obj.data.total_face_sel == 0:
            return False
        tool = context.workspace.tools.from_space_view3d_mode(context.mode, create=False)
        return tool is not None and tool.idname in _MOVE_TOOLS

    def invoke(self, context, _event):
        # The button is still down: letting go of it ends the extrusion.
        result = bpy.ops.maximize.smart_extrude('INVOKE_DEFAULT', release_confirm=True)
        return {'FINISHED'} if 'RUNNING_MODAL' in result or 'FINISHED' in result else {'CANCELLED'}


classes = (
    MAXIMIZE_OT_smart_extrude,
    MAXIMIZE_OT_smart_extrude_drag,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
