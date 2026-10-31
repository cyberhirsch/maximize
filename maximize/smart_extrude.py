# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Max's Smart Extrude: extrude the selected polygons along their normal; pushed into the mesh they
cut a pocket (or a hole when they come out the other side), and where they run into other
geometry the two are merged. Shift+drag with the Move, Rotate or Scale tool extrudes them by that
move, turn or scale.

Out into free space it is a plain extrude (the quads stay as they are). Inward, or when the
extrusion hits the mesh, the extruded shape is cut away from (inward) or joined to (outward) the
mesh with the exact boolean. The drag shows a plain extrusion; the result is worked out when you
let go, as one undo step.
"""

import bmesh
import bpy
from bpy.props import BoolProperty, FloatProperty, FloatVectorProperty
from bpy.types import Operator
from bpy_extras import view3d_utils
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree

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


def _mean_move(faces, moves):
    """The average move of the polygons' corners."""
    verts = {v for f in faces for v in f.verts}
    return sum((moves.get(v, Vector()) for v in verts), Vector()) / len(verts)


def _hits(bm, faces, moves):
    """Whether the extrusion (each corner moved by `moves[vertex]`) runs into the rest of the mesh."""
    selected = set(faces)
    others = [f for f in bm.faces if f not in selected and not f.hide]
    if not others:
        return False
    index = {v: i for i, v in enumerate(bm.verts)}
    tree = BVHTree.FromPolygons([v.co for v in bm.verts], [[index[v] for v in f.verts] for f in others])
    for face in faces:
        center = face.calc_center_median()
        center_move = sum((moves.get(v, Vector()) for v in face.verts), Vector()) / len(face.verts)
        # The face's center and its corners pulled a little toward it, so the rays leave from inside
        # the face and don't touch the neighbors at its edges.
        points = [(center, center_move)] + [(v.co.lerp(center, 0.02), moves.get(v, Vector()).lerp(center_move, 0.02))
                                            for v in face.verts]
        for point, move in points:
            length = move.length
            if length < 1e-9:
                continue
            direction = move / length
            start = point + direction * (length * 1e-4)
            hit = tree.ray_cast(start, direction, length * (1.0 - 2e-4))
            if hit[0] is not None:
                return True
    # Inward, the walls can also run along the neighbors (a whole side pushed in).
    return _mean_move(faces, moves).dot(_direction(faces)) < 0.0


def _copies(originals, copies):
    """{copy: original} for vertices copied in place (at the same position)."""
    at = {v.co.to_tuple(): v for v in originals}
    return {c: at.get(c.co.to_tuple()) for c in copies}


def _plain_extrude(bm, faces, moves):
    """Extrude `faces`, each corner moved by `moves[vertex]`. Returns {new vertex: original}."""
    region = {v for f in faces for v in f.verts}
    result = bmesh.ops.extrude_face_region(bm, geom=faces)
    verts = [e for e in result["geom"] if isinstance(e, bmesh.types.BMVert)]
    origin = _copies(region, verts)
    for v in verts:
        v.co += moves.get(origin[v], Vector())
    bmesh.ops.delete(bm, geom=faces, context='FACES')
    for f in bm.faces:
        f.select = False
    for e in bm.edges:
        e.select = False
    for v in bm.verts:
        v.select = False
    # As in Max, only the cap stays selected, not the new walls.
    moved = set(verts)
    for e in result["geom"]:
        if isinstance(e, bmesh.types.BMFace) and all(v in moved for v in e.verts):
            e.select = True
    bm.select_flush(True)
    return origin


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


def _solid_tree(solid):
    """The extruded shape (a closed solid, normals out) as a tree, copied: it stays as it is while
    the mesh changes."""
    verts = []
    polys = []
    for f in solid:
        polys.append(list(range(len(verts), len(verts) + len(f.verts))))
        verts.extend(v.co.copy() for v in f.verts)
    return BVHTree.FromPolygons(verts, polys)


# Off every axis, so the ray doesn't run along the walls or through their edges.
_RAY = Vector((0.5773, 0.5167, 0.6324)).normalized()


def _in_extrusion(shape, point, step):
    """Whether `point` is inside the extruded shape: a ray from it crosses its surface an odd
    number of times."""
    crossings = 0
    start = point
    for _i in range(64):
        location = shape.ray_cast(start, _RAY)[0]
        if location is None:
            break
        crossings += 1
        start = location + _RAY * step
    return crossings % 2 == 1


def _cap_plane(faces, moves):
    """The plane the moved polygons end up in: through their moved center, facing as they then do
    (a move, also along a gizmo arrow or in a plane, doesn't turn them; a rotation does)."""
    at = {v: v.co + moves.get(v, Vector()) for f in faces for v in f.verts}
    center = sum(at.values(), Vector()) / len(at)
    normal = Vector()
    for f in faces:
        corners = [at[v] for v in f.verts]
        for i in range(1, len(corners) - 1):
            normal += (corners[i] - corners[0]).cross(corners[i + 1] - corners[0])
    return center, (normal.normalized() if normal.length > 1e-12 else _direction(faces))


def _on_segment(point, a, b, tolerance):
    ab = b - a
    t = (point - a).dot(ab) / max(ab.length_squared, 1e-18)
    return -1e-6 <= t <= 1.0 + 1e-6 and (a + ab * t - point).length < tolerance


def _clean_up(bm, old_edges, old_verts, tolerance):
    """After the boolean: weld the slivers the skin leaves, and dissolve the flat edges the boolean
    added (where walls lie flush with the mesh), keeping the mesh's own edges."""
    tree = KDTree(len(old_verts))
    for i, co in enumerate(old_verts):
        tree.insert(co, i)
    tree.balance()
    new = [v for v in bm.verts if not old_verts or tree.find(v.co)[2] > tolerance * 0.01]
    if new:
        near = KDTree(len(bm.verts))
        for v in bm.verts:
            near.insert(v.co, v.index)
        near.balance()
        bm.verts.ensure_lookup_table()
        weld = {bm.verts[i] for v in new for _co, i, _d in near.find_range(v.co, tolerance)}
        bmesh.ops.remove_doubles(bm, verts=list(weld), dist=tolerance)
        # Back onto the mesh's own points (the weld can land between the two).
        for v in bm.verts:
            if v.is_valid and old_verts:
                co, _i, d = tree.find(v.co)
                if d < tolerance:
                    v.co = co
    flat = []
    for e in bm.edges:
        faces = e.link_faces
        if len(faces) != 2 or faces[0].normal.dot(faces[1].normal) < 1.0 - 1e-6:
            continue
        a, b = e.verts[0].co, e.verts[1].co
        if any(_on_segment(a, p, q, tolerance) and _on_segment(b, p, q, tolerance) for p, q in old_edges):
            continue
        flat.append(e)
    if flat:
        bmesh.ops.dissolve_edges(bm, edges=flat, use_verts=True)


def smart_extrude(obj, offset=None, moved=None):
    """Extrude the selected polygons of `obj` (in Edit Mode) by `offset`, or with each corner moved
    to `moved[vertex index]` (a rotation or scale). Returns 'PLAIN', 'CUT', 'MERGE' or None
    (nothing selected, or nothing moved)."""
    bm = bmesh.from_edit_mesh(obj.data)
    faces = _selected_faces(bm)
    if not faces:
        return None
    region = {v for f in faces for v in f.verts}
    if moved is not None:
        bm.verts.index_update()
        moves = {v: Vector(moved[v.index]) - v.co if v.index in moved else Vector() for v in region}
    else:
        moves = {v: Vector(offset) for v in region}
    if max(m.length for m in moves.values()) < 1e-9:
        return None
    # Turned so that some corners go in and others out, or moved only along the surface (scaled in
    # place): a plain extrude (cutting and merging need a shape with depth, on one side of it).
    along = [m.dot(_direction(faces)) for m in moves.values()]
    tolerance = _size(bm) * 1e-6
    flat = max(abs(a) for a in along) <= tolerance
    mixed = min(along) < -tolerance and max(along) > tolerance
    if flat or mixed or not _hits(bm, faces, moves):
        _plain_extrude(bm, faces, moves)
        bmesh.update_edit_mesh(obj.data)
        return 'PLAIN'
    mean = _mean_move(faces, moves)
    inward = mean.dot(_direction(faces)) < 0.0
    cap_point, cap_normal = _cap_plane(faces, moves)
    skin = _size(bm) * _SKIN
    # A little back out of the surface, against the move (turned or scaled in place: the normal).
    away = -mean if mean.length > tolerance else _direction(faces)
    back = away.normalized() * skin
    old_edges = [(e.verts[0].co.copy(), e.verts[1].co.copy()) for e in bm.edges if not e.hide]
    old_verts = [v.co.copy() for v in bm.verts]
    # The extruded shape as a closed solid of its own: the faces copied, moved a little back out of
    # the surface, and extruded past the original with the move.
    widen = _widening(faces, mean) if inward and mean.length > tolerance else {}
    copied = bmesh.ops.duplicate(bm, geom=faces)
    base = [e for e in copied["geom"] if isinstance(e, bmesh.types.BMFace)]
    original = {c: o for o, c in copied["vert_map"].items() if isinstance(o, bmesh.types.BMVert)}
    base_verts = list({v for f in base for v in f.verts})
    bmesh.ops.translate(bm, vec=back, verts=base_verts)
    for vert, out in widen.items():
        copied["vert_map"][vert].co += out * (skin * 20.0)
    extruded = bmesh.ops.extrude_face_region(bm, geom=base, use_keep_orig=True)
    ends = [e for e in extruded["geom"] if isinstance(e, bmesh.types.BMVert)]
    for end, base_vert in _copies(base_verts, ends).items():
        end.co += moves[original[base_vert]] - back
    # The base, the end and the walls between (the walls are not in the operator's result).
    solid = list(set(base) | {f for v in ends for f in v.link_faces})
    bmesh.ops.recalc_face_normals(bm, faces=solid)
    shape = _solid_tree(solid)
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
            return _in_extrusion(shape, point, skin * 1e-3)
        wrong = [f for f in bm.faces if cut_away(f.calc_center_median() - f.normal * step)
                 and not cut_away(f.calc_center_median() + f.normal * step)]
        bmesh.ops.reverse_faces(bm, faces=wrong)
    bm.verts.index_update()
    _clean_up(bm, old_edges, old_verts, skin * 30.0)
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
    offset: FloatVectorProperty(name="Offset", subtype='TRANSLATION', options={'SKIP_SAVE'},
                                description="Extrude by this move instead of along the normal (Shift+drag)")
    turned: BoolProperty(options={'HIDDEN', 'SKIP_SAVE'},
                         description="Extrude by the last Shift+Rotate or Shift+Scale drag")

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
        if self.turned:
            result = smart_extrude(obj, moved=_last_turn)
            return {'FINISHED'} if result else {'CANCELLED'}
        offset = Vector(self.offset)
        if offset.length < 1e-9:
            offset = _direction(faces) * self.distance
        result = smart_extrude(obj, offset)
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


# The tools whose Shift+drag extrudes, with the transform a drag off the gizmo starts (on the
# Transform tool's handles, the handle's own move, turn or scale).
_TOOLS = {"builtin.move": "translate", "builtin.transform": "translate",
          "builtin.rotate": "rotate", "builtin.scale": "resize"}


_pending_drag = None
# {vertex index: position} of the last Shift+Rotate or Shift+Scale (the redo panel runs it again).
_last_turn = {}


def _watch_drag():
    """Timer: once the Move of the preview extrusion ends, turn the move into a Smart Extrude."""
    global _pending_drag
    if _pending_drag is None:
        return None
    global _last_turn
    window, area, name, before, pairs, ticks = _pending_drag
    try:
        running = any(op.bl_idname.startswith(("TRANSFORM_OT_", "GIZMOGROUP_OT_")) for op in window.modal_operators)
    except ReferenceError:
        _pending_drag = None
        before.free()
        return None
    if running or ticks < 2:
        _pending_drag = (window, area, name, before, pairs, ticks + 1)
        return 0.05
    _pending_drag = None
    # By name, not by reference: the undo below can reload the data and drop Python references.
    obj = bpy.data.objects.get(name)
    if obj is None or obj.mode != 'EDIT':
        before.free()
        return None
    bm = bmesh.from_edit_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    # Where each corner of the polygons ended up: {its index in the mesh before: position}.
    moved = {orig: bm.verts[new].co.copy() for new, orig, _start in pairs if new < len(bm.verts)}
    moves = [moved[orig] - start for _new, orig, start in pairs if orig in moved]
    offset = moves[0] if moves else Vector()
    changed = any(m.length > 1e-6 for m in moves)
    # Turned or scaled: the corners moved differently (a plain move stays an offset, for redo).
    turned = any((m - offset).length > 1e-6 * max(offset.length, 1.0) for m in moves)
    region = next((r for r in area.regions if r.type == 'WINDOW'), None)
    with bpy.context.temp_override(window=window, area=area, region=region):
        if changed:
            # The Move made an undo step with the preview in it: step back over it (to the mesh as it
            # was, the preview itself made none), so one undo takes the whole Smart Extrude away.
            bpy.ops.ed.undo()
            obj = bpy.data.objects.get(name)
            if obj is not None and obj.mode != 'EDIT':
                # The Move was the first step in Edit Mode, so the undo left it: back to the Move,
                # the mesh is put back from the copy below (two undo steps then, not one).
                bpy.ops.ed.redo()
                obj = bpy.data.objects.get(name)
        if obj is None or obj.mode != 'EDIT':
            before.free()
            return None
        bm = bmesh.from_edit_mesh(obj.data)
        # Also when only the selection differs: a selection made by script has no undo step.
        if (len(bm.verts) != len(before.verts) or len(bm.faces) != len(before.faces)
                or [f.index for f in bm.faces if f.select] != [f.index for f in before.faces if f.select]):
            mesh = bpy.data.meshes.new("Smart Extrude")
            before.to_mesh(mesh)
            bm.clear()
            bm.from_mesh(mesh)
            bpy.data.meshes.remove(mesh)
            bmesh.update_edit_mesh(obj.data)
        before.free()
        if changed and turned:
            _last_turn = moved
            bpy.ops.maximize.smart_extrude('EXEC_DEFAULT', turned=True)
        elif changed:
            bpy.ops.maximize.smart_extrude('EXEC_DEFAULT', offset=offset)
    return None


class MAXIMIZE_OT_smart_extrude_drag(Operator):
    """Shift+drag of polygons with the Move, Rotate or Scale tool: Smart Extrude by the move, turn
    or scale, as in Max"""
    bl_idname = "maximize.smart_extrude_drag"
    bl_label = "Smart Extrude (Shift+Drag)"
    bl_options = {'INTERNAL'}

    gizmo: BoolProperty(options={'HIDDEN', 'SKIP_SAVE'}, description="Started on a gizmo handle")

    @classmethod
    def poll(cls, context):
        obj = context.edit_object
        if obj is None or obj.type != 'MESH' or not context.tool_settings.mesh_select_mode[2]:
            return False
        if context.region_data is None or obj.data.total_face_sel == 0:
            return False
        tool = context.workspace.tools.from_space_view3d_mode(context.mode, create=False)
        return tool is not None and tool.idname in _TOOLS

    def invoke(self, context, _event):
        global _pending_drag
        obj = context.edit_object
        bm = bmesh.from_edit_mesh(obj.data)
        faces = _selected_faces(bm)
        if not faces:
            return {'CANCELLED'}
        bm.verts.index_update()
        # A detached copy, not a mesh data-block: the undo in _watch_drag can reload the data.
        before = bm.copy()
        index = {v: v.index for f in faces for v in f.verts}
        # A plain extrusion for the transform to drag (the gizmo's axis, X / Y / Z, snapping); when
        # it ends, the mesh goes back and Smart Extrude runs with the move, turn or scale.
        origin = _plain_extrude(bm, faces, {})
        bm.verts.index_update()
        pairs = [(new.index, index[orig], new.co.copy()) for new, orig in origin.items()]
        bmesh.update_edit_mesh(obj.data)
        _pending_drag = (context.window, context.area, obj.name, before, pairs, 0)
        bpy.app.timers.register(_watch_drag, first_interval=0.05)
        if self.gizmo:
            from .transform import gizmo_arrow_move
            if gizmo_arrow_move(context):
                return {'FINISHED'}
            # The next keymap item starts the gizmo's drag on the extrusion.
            return {'PASS_THROUGH'}
        tool = context.workspace.tools.from_space_view3d_mode(context.mode, create=False)
        getattr(bpy.ops.transform, _TOOLS[tool.idname])('INVOKE_DEFAULT', release_confirm=True)
        return {'FINISHED'}


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
