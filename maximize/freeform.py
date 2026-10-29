# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""The Freeform modifier: Max's Freeform tab (PolyDraw) as one stack entry, for retopology.

- The modifier is a Geometry Nodes modifier named "Freeform" that keeps the mesh on a target
  surface (Draw On), Offset above it. Stock Blender evaluates it.
- Its panel holds the PolyDraw tools, which draw onto the target: Drag (move on the surface), Step
  Build / Extend / Optimize (Blender's Poly Build), the Conform brushes (Conform paints the vertices
  onto the surface; Move, Rotate, Scale and Relax change them and keep them on it), Conform All
  (the whole selection at once), Strips, Surface, Shapes, Topology, Branches and Splines (drawn strokes), and Solve Surface.
- Paint Deform is sculpting: the Sculpt modifier covers it.
"""

import math

import bmesh
import bpy
import gpu
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, PointerProperty
from bpy.types import Operator, PropertyGroup
from bpy_extras import view3d_utils
from gpu_extras.batch import batch_for_shader
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import intersect_line_line_2d
from mathutils.kdtree import KDTree

from .nodes import GroupBuilder, find_group, modifier_input

MODIFIER_NAME = "Freeform"
GROUP_NAME = "MX Freeform"
KIND = "freeform"


# ------------------------------------------------------------------------------
# The modifier


def ensure_group():
    group = find_group(GROUP_NAME)
    if group is not None:
        return group
    g = GroupBuilder(GROUP_NAME, KIND)
    geometry = g.input("Geometry", 'NodeSocketGeometry')
    target = g.input("Surface", 'NodeSocketObject')
    offset = g.input("Offset", 'NodeSocketFloat', 0.0, subtype='DISTANCE')
    strength = g.input("Conform", 'NodeSocketFloat', 1.0, 0.0, 1.0, subtype='FACTOR')
    out = g.output()
    surface = g.node('GeometryNodeObjectInfo', {"Object": target}, transform_space='RELATIVE').outputs["Geometry"]
    position = g.node('GeometryNodeInputPosition').outputs[0]

    def nearest(value):
        node = g.node('GeometryNodeSampleNearestSurface', {"Mesh": surface, "Value": value,
                                                           "Sample Position": position}, data_type='FLOAT_VECTOR')
        return node.outputs["Value"]
    on_surface = nearest(g.node('GeometryNodeInputPosition').outputs[0])
    normal = nearest(g.node('GeometryNodeInputNormal').outputs[0])
    goal = g.vmath('ADD', on_surface, g.node('ShaderNodeVectorMath', {0: normal, "Scale": offset},
                                             operation='SCALE').outputs["Vector"])
    moved = g.vmath('ADD', position, g.node('ShaderNodeVectorMath', {
        0: g.vmath('SUBTRACT', goal, position), "Scale": strength}, operation='SCALE').outputs["Vector"])
    # Without a target (or an empty one) the mesh stays as it is.
    faces = g.node('GeometryNodeAttributeDomainSize', {"Geometry": surface}, component='MESH').outputs["Face Count"]
    has_target = g.node('FunctionNodeCompare', {"A": faces, "B": 0}, data_type='INT',
                        operation='GREATER_THAN').outputs[0]
    g.set(out, g.node('GeometryNodeSetPosition', {"Geometry": geometry, "Selection": has_target,
                                                  "Position": moved}).outputs[0])
    return g.tree


def freeform_modifier(obj):
    if obj is None:
        return None
    for mod in obj.modifiers:
        if mod.type == 'NODES' and mod.node_group is not None and mod.node_group.get("maximize_kind") == KIND:
            return mod
    return None


def target_of(obj):
    mod = freeform_modifier(obj)
    return modifier_input(mod, "Surface").value if mod is not None else None


def offset_of(obj):
    mod = freeform_modifier(obj)
    return modifier_input(mod, "Offset").value if mod is not None else 0.0


def add_freeform(obj, target):
    mod = obj.modifiers.new(MODIFIER_NAME, 'NODES')
    mod.node_group = ensure_group()
    mod.show_in_editmode = True
    if target is not None:
        modifier_input(mod, "Surface").value = target
    obj.modifiers.active = mod
    return mod


def _drawing_setup(context):
    """Snapping onto surfaces and the Retopology overlay, as Freeform's drawing needs."""
    ts = context.scene.tool_settings
    ts.use_snap = True
    try:
        ts.snap_elements = {'FACE_NEAREST'}
    except TypeError:
        ts.snap_elements = {'FACE'}
    if hasattr(ts, "use_snap_self"):
        ts.use_snap_self = False
    for area in context.window.screen.areas if context.window else ():
        if area.type == 'VIEW_3D':
            overlay = area.spaces.active.overlay
            if hasattr(overlay, "show_retopology"):
                overlay.show_retopology = True


class MAXIMIZE_OT_freeform_add(Operator):
    """Add a Freeform modifier: the mesh stays on the surface of another object (Draw On), and its
    panel has Max's PolyDraw tools. Another selected mesh becomes the surface"""
    bl_idname = "maximize.freeform_add"
    bl_label = "Freeform"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == 'MESH' and freeform_modifier(obj) is None

    def execute(self, context):
        obj = context.active_object
        target = next((o for o in context.selected_objects if o is not obj and o.type == 'MESH'), None)
        add_freeform(obj, target)
        return {'FINISHED'}


class MAXIMIZE_OT_freeform_new_object(Operator):
    """New Object: an empty mesh with a Freeform modifier on the selected object's surface, in Edit
    Mode, ready to draw new topology on it"""
    bl_idname = "maximize.freeform_new_object"
    bl_label = "New Object"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == 'MESH' and context.mode == 'OBJECT'

    def execute(self, context):
        target = context.active_object
        if freeform_modifier(target) is not None:
            # Already a Freeform object: a new one on the same surface.
            target = target_of(target) or target
        mesh = bpy.data.meshes.new("Freeform")
        obj = bpy.data.objects.new("Freeform", mesh)
        collection = target.users_collection[0] if target.users_collection else context.collection
        collection.objects.link(obj)
        add_freeform(obj, target)
        for o in context.selected_objects:
            o.select_set(False)
        obj.select_set(True)
        context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type='VERT')
        _drawing_setup(context)
        return {'FINISHED'}


# ------------------------------------------------------------------------------
# The surface


DRAW_ON = (
    ('GRID', "Grid", "Draw on the grid: the ground plane, or in a Top / Front / Side view that view's plane "
     "through the origin"),
    ('SURFACE', "Surface", "Draw on the Surface object (the modifier's Surface input)"),
    ('SELECTION', "Selection", "Draw on the selected polygons of the mesh itself"),
)


def _grid_plane(rv3d):
    """The plane Max's home grid shows in a view: in an axis-aligned orthographic view the plane
    through the origin facing it, otherwise the ground."""
    if rv3d is not None and rv3d.view_perspective == 'ORTHO' and getattr(rv3d, "is_orthographic_side_view", False):
        axis = rv3d.view_rotation @ Vector((0.0, 0.0, 1.0))
        return Vector(), Vector([round(c) for c in axis]).normalized()
    return Vector(), Vector((0.0, 0.0, 1.0))


class Surface:
    """What the Freeform tools draw on, in world space: the Surface object, the grid or the
    selected polygons (Draw On). Without any, a plane facing the view through the 3D cursor."""

    def __init__(self, context, obj, draw_on=None, rv3d=None):
        draw_on = draw_on or settings(context).draw_on
        self.offset = offset_of(obj)
        self.tree = None
        self.plane = None
        if draw_on == 'GRID':
            self.plane = _grid_plane(rv3d if rv3d is not None else getattr(context, "region_data", None))
        elif draw_on == 'SELECTION':
            self._from_selection(obj)
        else:
            target = target_of(obj)
            if target is not None and target.type == 'MESH':
                self.tree = BVHTree.FromObject(target, context.evaluated_depsgraph_get())
                self.matrix = target.matrix_world.copy()
        if self.tree is not None:
            self.inverse = self.matrix.inverted_safe()
        self.cursor = context.scene.cursor.location.copy()

    def _from_selection(self, obj):
        """The selected polygons as they are now (what is drawn later doesn't count)."""
        if obj.mode == 'EDIT':
            bm = bmesh.from_edit_mesh(obj.data)
            faces = [f for f in bm.faces if f.select and not f.hide]
            if faces:
                self.tree = BVHTree.FromPolygons([v.co.copy() for v in bm.verts],
                                                 [[v.index for v in f.verts] for f in faces])
        else:
            mesh = obj.data
            polys = [p.vertices[:] for p in mesh.polygons if p.select]
            if polys:
                self.tree = BVHTree.FromPolygons([v.co.copy() for v in mesh.vertices], polys)
        self.matrix = obj.matrix_world.copy()

    def _lift(self, location, normal):
        n = (self.inverse.to_3x3().transposed() @ normal).normalized()
        return self.matrix @ location + n * self.offset, n

    def cast(self, region, rv3d, mouse):
        """(point, normal) under the mouse, lifted by the Offset; None where the surface isn't."""
        origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, mouse)
        direction = view3d_utils.region_2d_to_vector_3d(region, rv3d, mouse)
        if self.tree is not None:
            o = self.inverse @ origin
            d = (self.inverse.to_3x3() @ direction).normalized()
            location, normal, _index, _distance = self.tree.ray_cast(o, d)
            if location is None:
                return None
            return self._lift(location, normal)
        if self.plane is not None:
            point = self._plane_hit(origin, direction)
            if point is None:
                return None
            normal = self._plane_normal(direction)
            return point + normal * self.offset, normal
        point = view3d_utils.region_2d_to_location_3d(region, rv3d, mouse, self.cursor)
        return point, -direction.normalized()

    def _plane_normal(self, facing):
        """The plane's normal on the side `facing` (a view or vertex direction) comes from."""
        normal = self.plane[1]
        return -normal if normal.dot(facing) > 0.0 else normal.copy()

    def _plane_hit(self, origin, direction):
        from mathutils.geometry import intersect_line_plane
        co, normal = self.plane
        if abs(direction.dot(normal)) < 1e-6:
            return None
        return intersect_line_plane(origin, origin + direction, co, normal)

    def nearest(self, point):
        """The nearest surface point to `point` (world), lifted by the Offset, or None."""
        if self.plane is not None:
            co, normal = self.plane
            side = 1.0 if (point - co).dot(normal) >= 0.0 else -1.0
            return point - normal * (point - co).dot(normal) + normal * side * self.offset
        if self.tree is None:
            return None
        location, normal, _index, _distance = self.tree.find_nearest(self.inverse @ point)
        if location is None:
            return None
        return self._lift(location, normal)[0]

    def along(self, point, direction):
        """Where the line through `point` (world) along `direction` meets the surface, the nearer of
        the two ways, lifted by the Offset; None where it doesn't."""
        if direction.length_squared < 1e-12:
            return None
        if self.plane is not None:
            hit = self._plane_hit(point, direction)
            if hit is None:
                return None
            return hit + self._plane_normal(hit - point if (hit - point).length_squared > 1e-12
                                            else direction) * self.offset
        if self.tree is None:
            return None
        o = self.inverse @ point
        d = (self.inverse.to_3x3() @ direction).normalized()
        best = None
        for way in (d, -d):
            location, normal, _index, distance = self.tree.ray_cast(o, way)
            if location is not None and (best is None or distance < best[2]):
                best = (location, normal, distance)
        if best is None:
            return None
        return self._lift(best[0], best[1])[0]

    def conform(self, point, normal, direction):
        """Where Conform puts a vertex at `point` with the world `normal`: the nearest surface point
        ('TARGET', along the surface's normal) or along the vertex normal ('OBJECT')."""
        if direction == 'OBJECT':
            return self.along(point, normal)
        return self.nearest(point)

    @property
    def usable(self):
        return self.tree is not None or self.plane is not None


def can_draw(context, obj):
    """Whether the Freeform tools have something to work on: the Surface object, or Draw On set to
    the grid or the selection."""
    return settings(context).draw_on != 'SURFACE' or target_of(obj) is not None


def pixel_size(region, rv3d, mouse, point):
    """World length of one pixel at `point`."""
    a = view3d_utils.region_2d_to_location_3d(region, rv3d, mouse, point)
    b = view3d_utils.region_2d_to_location_3d(region, rv3d, (mouse[0] + 1.0, mouse[1]), point)
    return (b - a).length


# ------------------------------------------------------------------------------
# Building: each takes stroke points [(point, normal, pixel)] in world space


def _local(obj, point):
    return obj.matrix_world.inverted_safe() @ point


def _weld_new(bm, new_verts, distance):
    """Join new vertices onto existing ones nearby (a strip started on a border connects to it)."""
    old = [v for v in bm.verts if v not in new_verts]
    if not old or distance <= 0.0:
        return
    tree = KDTree(len(old))
    for i, v in enumerate(old):
        tree.insert(v.co, i)
    tree.balance()
    targetmap = {}
    for v in new_verts:
        co, i, d = tree.find(v.co)
        if i is not None and d < distance:
            targetmap[v] = old[i]
    if targetmap:
        bmesh.ops.weld_verts(bm, targetmap=targetmap)


def _orient(face, normal):
    face.normal_update()
    if face.normal.dot(normal) < 0.0:
        face.normal_flip()


def _finish(obj, bm, faces):
    for f in bm.faces:
        f.select = False
    for f in faces:
        if f.is_valid:
            f.select_set(True)
    bm.select_flush(True)
    bmesh.update_edit_mesh(obj.data)


def build_strip(obj, points, width, rows=1):
    """A strip of quads along the stroke, `width` pixels wide and `rows` quads across."""
    if len(points) < 2:
        return 0
    bm = bmesh.from_edit_mesh(obj.data)
    world_to_local = obj.matrix_world.inverted_safe()
    normal_matrix = world_to_local.to_3x3()
    columns = []
    new = []
    for i, (p, n, px) in enumerate(points):
        a = points[max(i - 1, 0)][0]
        b = points[min(i + 1, len(points) - 1)][0]
        side = n.cross(b - a)
        if side.length < 1e-12:
            side = Vector((1.0, 0.0, 0.0))
        side.normalize()
        half = width * px * 0.5
        column = []
        for k in range(rows + 1):
            v = bm.verts.new(world_to_local @ (p + side * half * (2.0 * k / rows - 1.0)))
            column.append(v)
            new.append(v)
        columns.append((column, normal_matrix @ n))
    faces = []
    for (c0, n0), (c1, _n1) in zip(columns, columns[1:]):
        for k in range(rows):
            f = bm.faces.new((c0[k], c1[k], c1[k + 1], c0[k + 1]))
            _orient(f, n0)
            faces.append(f)
    _weld_new(bm, new, min(width * points[0][2], width * points[-1][2]) * 0.35)
    _finish(obj, bm, faces)
    return len(faces)


def build_shape(obj, points):
    """A polygon from a closed stroke."""
    if len(points) > 3:
        # The stroke ends where it began: no second vertex there.
        spacing = sum((a[0] - b[0]).length for a, b in zip(points, points[1:])) / (len(points) - 1)
        if (points[0][0] - points[-1][0]).length < spacing * 1.5:
            points = points[:-1]
    if len(points) < 3:
        return 0
    bm = bmesh.from_edit_mesh(obj.data)
    verts = [bm.verts.new(_local(obj, p)) for p, _n, _px in points]
    normal = sum((n for _p, n, _px in points), Vector())
    f = bm.faces.new(verts)
    _orient(f, obj.matrix_world.inverted_safe().to_3x3() @ normal)
    _finish(obj, bm, [f])
    return 1


def build_branch(obj, points, taper):
    """Extrude the selected polygons along the stroke, thinning by `taper` (-1: to a point)."""
    bm = bmesh.from_edit_mesh(obj.data)
    faces = [f for f in bm.faces if f.select and not f.hide]
    if not faces or len(points) < 2:
        return 0
    world_to_local = obj.matrix_world.inverted_safe()
    steps = len(points) - 1
    previous = 1.0
    for i in range(1, len(points)):
        result = bmesh.ops.extrude_face_region(bm, geom=faces)
        bmesh.ops.delete(bm, geom=faces, context='FACES')
        faces = [e for e in result["geom"] if isinstance(e, bmesh.types.BMFace)]
        verts = list({v for f in faces for v in f.verts})
        delta = world_to_local.to_3x3() @ (points[i][0] - points[i - 1][0])
        bmesh.ops.translate(bm, vec=delta, verts=verts)
        scale = max(0.02, 1.0 + taper * i / steps)
        center = sum((v.co for v in verts), Vector()) / len(verts)
        for v in verts:
            v.co = center + (v.co - center) * (scale / previous)
        previous = scale
    _finish(obj, bm, faces)
    return steps


def build_spline(context, obj, points):
    """A new spline object along the stroke (Freeform's Splines)."""
    if len(points) < 2:
        return None
    curve = bpy.data.curves.new("Freeform Spline", 'CURVE')
    curve.dimensions = '3D'
    spline = curve.splines.new('POLY')
    spline.points.add(len(points) - 1)
    for sp, (p, _n, _px) in zip(spline.points, points):
        sp.co = (p.x, p.y, p.z, 1.0)
    new = bpy.data.objects.new("Freeform Spline", curve)
    collection = obj.users_collection[0] if obj.users_collection else context.collection
    collection.objects.link(new)
    return new


def _cumulative(screen):
    lengths = [0.0]
    for a, b in zip(screen, screen[1:]):
        lengths.append(lengths[-1] + (b - a).length)
    return lengths


def _crossing(a, b):
    """Where screen polylines a and b cross: (param along a, param along b, screen point) or None."""
    la, lb = _cumulative(a), _cumulative(b)
    for i in range(len(a) - 1):
        for j in range(len(b) - 1):
            hit = intersect_line_line_2d(a[i], a[i + 1], b[j], b[j + 1])
            if hit is not None:
                ta = la[i] + (hit - a[i]).length
                tb = lb[j] + (hit - b[j]).length
                return ta / max(la[-1], 1e-9), tb / max(lb[-1], 1e-9), hit
    return None


def build_topology(obj, strokes, cast):
    """Quads between drawn lines (Freeform's Topology): the strokes fall into two directions, and
    each crossing of one with the other becomes a vertex. `strokes` are screen polylines,
    `cast(screen_point) -> (point, normal) or None` puts a crossing on the surface."""
    if len(strokes) < 4:
        return 0
    first = (strokes[0][-1] - strokes[0][0]).normalized()
    across = [s for s in strokes if abs((s[-1] - s[0]).normalized().dot(first)) < 0.7071]
    along = [s for s in strokes if s not in across]
    if len(across) < 2 or len(along) < 2:
        return 0
    crossings = {}
    for i, a in enumerate(along):
        for j, b in enumerate(across):
            hit = _crossing(a, b)
            if hit is not None:
                crossings[i, j] = hit
    # Order each family by where it crosses the other.
    along_order = sorted(range(len(along)), key=lambda i: sum(
        crossings[i, j][1] for j in range(len(across)) if (i, j) in crossings) / max(
        1, sum(1 for j in range(len(across)) if (i, j) in crossings)))
    across_order = sorted(range(len(across)), key=lambda j: sum(
        crossings[i, j][0] for i in range(len(along)) if (i, j) in crossings) / max(
        1, sum(1 for i in range(len(along)) if (i, j) in crossings)))
    bm = bmesh.from_edit_mesh(obj.data)
    world_to_local = obj.matrix_world.inverted_safe()
    grid = {}
    normals = {}
    for r, i in enumerate(along_order):
        for c, j in enumerate(across_order):
            if (i, j) not in crossings:
                continue
            hit = cast(crossings[i, j][2])
            if hit is None:
                continue
            grid[r, c] = bm.verts.new(world_to_local @ hit[0])
            normals[r, c] = world_to_local.to_3x3() @ hit[1]
    faces = []
    for r in range(len(along) - 1):
        for c in range(len(across) - 1):
            corners = [(r, c), (r + 1, c), (r + 1, c + 1), (r, c + 1)]
            if all(k in grid for k in corners):
                f = bm.faces.new([grid[k] for k in corners])
                _orient(f, normals[r, c])
                faces.append(f)
    # Crossings that made no quad.
    used = {v for f in faces for v in f.verts}
    bmesh.ops.delete(bm, geom=[v for v in grid.values() if v not in used], context='VERTS')
    _finish(obj, bm, faces)
    return len(faces)


# ------------------------------------------------------------------------------
# Settings and tools


class MaximizeFreeformSettings(PropertyGroup):
    draw_on: EnumProperty(name="Draw On", items=DRAW_ON, default='SURFACE',
                          description="What the PolyDraw tools and the Conform brushes work on")
    min_distance: IntProperty(name="Min Distance", default=10, min=1, max=200, subtype='PIXEL',
                              description="Screen distance between the points of a drawn stroke")
    width: IntProperty(name="Width", default=24, min=2, max=1000, subtype='PIXEL',
                       description="Width of the strips (per quad across, for Surface)")
    surface_segments: IntProperty(name="Surface Segments", default=3, min=1, max=50,
                                  description="Quads across a Surface stroke")
    branch_taper: FloatProperty(name="Branch Taper", default=-0.9, min=-1.0, max=10.0,
                                description="How the branch thins out to its end (-1: to a point, 0: not at all)")
    conform_direction: EnumProperty(
        name="Normal", default='TARGET',
        items=(('TARGET', "Target", "Vertices move along the Draw On surface's normal, to the nearest point on it"),
               ('OBJECT', "Active Object", "Vertices move along their own normals, the conformed mesh's, "
                "until they meet the surface")),
        description="Which normal Conform moves the vertices along")
    brush_size: IntProperty(name="Brush Size", default=50, min=2, max=1000, subtype='PIXEL',
                            description="Conform brush radius ([ and ] while painting)")
    brush_strength: FloatProperty(name="Strength", default=0.5, min=0.0, max=1.0, subtype='FACTOR',
                                  description="How far the Conform brush moves the vertices each step")
    solve_angle: FloatProperty(name="Angle", default=math.radians(35.0), min=0.0, max=math.pi, subtype='ANGLE',
                               description="Solve Surface: edges sharper than this stay hard")


def settings(context):
    return context.scene.maximize_freeform


def _freeform_object(context):
    obj = context.active_object
    return obj if obj is not None and obj.type == 'MESH' else None


_MOUSE = {'LEFTMOUSE', 'RIGHTMOUSE', 'MIDDLEMOUSE', 'MOUSEMOVE', 'INBETWEEN_MOUSEMOVE', 'WHEELUPMOUSE',
          'WHEELDOWNMOUSE', 'TRACKPADPAN', 'TRACKPADZOOM'}


def outside(region, event):
    """True for a mouse event outside `region`: a click on a button, panel, the Outliner or a menu,
    which a modal tool passes through to the UI instead of blocking it."""
    if event.type not in _MOUSE:
        return False
    x, y = event.mouse_x - region.x, event.mouse_y - region.y
    return not (0 <= x < region.width and 0 <= y < region.height)


def ui_state(context):
    """What a click elsewhere can change that ends a modal tool: the mode, the active tool and the
    object being edited."""
    tool = context.workspace.tools.from_space_view3d_mode(context.mode, create=False)
    return context.mode, tool.idname if tool else None, context.active_object


DRAW_KINDS = (
    ('STRIPS', "Strips", "Draw strips of quads on the surface"),
    ('SURFACE', "Surface", "Draw a wide patch of quads on the surface"),
    ('SHAPES', "Shapes", "Draw a closed shape: it becomes a polygon"),
    ('TOPOLOGY', "Topology", "Draw lines across each other; Enter (or right-click) makes quads where they cross"),
    ('BRANCHES', "Branches", "Drag from the selected polygons: they extrude along the stroke and thin out"),
    ('SPLINES', "Splines", "Draw splines on the surface (new spline objects)"),
)


class MAXIMIZE_OT_freeform_draw(Operator):
    """PolyDraw: draw on the Freeform surface"""
    bl_idname = "maximize.freeform_draw"
    bl_label = "PolyDraw"
    bl_options = {'REGISTER', 'UNDO'}

    kind: EnumProperty(name="Kind", items=DRAW_KINDS)

    @classmethod
    def description(cls, _context, properties):
        return next(d for k, _n, d in DRAW_KINDS if k == properties.kind)

    @classmethod
    def poll(cls, context):
        return _freeform_object(context) is not None

    def invoke(self, context, event):
        if context.region_data is None:
            # From the panel: draw in the active viewport.
            from .vocabulary import view3d_override
            override = view3d_override(context)
            if override is None:
                return {'CANCELLED'}
            with context.temp_override(**override):
                bpy.ops.maximize.freeform_draw('INVOKE_DEFAULT', kind=self.kind)
            return {'FINISHED'}
        obj = _freeform_object(context)
        if self.kind != 'SPLINES' and obj.mode != 'EDIT':
            bpy.ops.object.mode_set(mode='EDIT')
        self._obj = obj
        self._area = context.area
        self._region = context.region
        self._rv3d = context.region_data
        self._surface = Surface(context, obj)
        self._settings = settings(context)
        self._stroke = None
        self._strokes = []
        self._state = ui_state(context)
        self._handle = bpy.types.SpaceView3D.draw_handler_add(self._draw, (), 'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        self._header(context)
        return {'RUNNING_MODAL'}

    def _header(self, context):
        text = "{}: drag to draw".format(next(n for k, n, _d in DRAW_KINDS if k == self.kind))
        if self.kind == 'TOPOLOGY':
            text += " lines across each other; Enter or right-click makes the quads"
        context.area.header_text_set(text + "; Esc / right-click ends")

    def _mouse(self, event):
        return Vector((event.mouse_x - self._region.x, event.mouse_y - self._region.y))

    def _cast(self, mouse):
        return self._surface.cast(self._region, self._rv3d, mouse)

    def _points(self, screen):
        points = []
        for mouse in screen:
            hit = self._cast(mouse)
            if hit is not None:
                points.append((hit[0], hit[1], pixel_size(self._region, self._rv3d, mouse, hit[0])))
        return points

    def _build(self, context, screen):
        s = self._settings
        obj = self._obj
        if self.kind == 'SPLINES':
            build_spline(context, obj, self._points(screen))
        elif self.kind == 'STRIPS':
            build_strip(obj, self._points(screen), s.width)
        elif self.kind == 'SURFACE':
            build_strip(obj, self._points(screen), s.width * s.surface_segments, s.surface_segments)
        elif self.kind == 'SHAPES':
            build_shape(obj, self._points(screen))
        elif self.kind == 'BRANCHES':
            build_branch(obj, self._points(screen), s.branch_taper)

    def _end(self, context):
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        self._area.header_text_set(None)
        self._area.tag_redraw()

    def modal(self, context, event):
        self._area.tag_redraw()
        if ui_state(context) != self._state:
            # A button elsewhere changed the tool, mode or object: this tool is done.
            self._end(context)
            return {'CANCELLED'}
        if outside(self._region, event) and self._stroke is None:
            return {'PASS_THROUGH'}
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE', 'TRACKPADPAN', 'TRACKPADZOOM'} or \
                event.type.startswith('NDOF'):
            return {'PASS_THROUGH'}
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            self._stroke = [self._mouse(event)]
            return {'RUNNING_MODAL'}
        if event.type == 'MOUSEMOVE' and self._stroke is not None:
            mouse = self._mouse(event)
            if (mouse - self._stroke[-1]).length >= self._settings.min_distance:
                self._stroke.append(mouse)
            return {'RUNNING_MODAL'}
        if event.type == 'LEFTMOUSE' and event.value == 'RELEASE' and self._stroke is not None:
            stroke, self._stroke = self._stroke + [self._mouse(event)], None
            if len(stroke) >= 2:
                if self.kind == 'TOPOLOGY':
                    self._strokes.append(stroke)
                else:
                    self._build(context, stroke)
            return {'RUNNING_MODAL'}
        if event.value == 'PRESS' and event.type in {'RET', 'NUMPAD_ENTER', 'SPACE', 'RIGHTMOUSE', 'ESC'}:
            if self.kind == 'TOPOLOGY' and self._strokes and event.type != 'ESC':
                made = build_topology(self._obj, self._strokes, self._cast)
                if not made:
                    self.report({'WARNING'}, "Draw at least two lines each way, crossing each other")
            self._end(context)
            return {'FINISHED'}
        return {'RUNNING_MODAL'}

    def _draw(self):
        try:
            lines = self._strokes + ([self._stroke] if self._stroke else [])
        except ReferenceError:
            return
        if not lines:
            return
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        gpu.state.blend_set('ALPHA')
        gpu.state.line_width_set(2.0)
        shader.uniform_float("color", (1.0, 0.55, 0.1, 0.9))
        for line in lines:
            if len(line) >= 2:
                batch_for_shader(shader, 'LINE_STRIP', {"pos": [tuple(p) for p in line]}).draw(shader)
        gpu.state.line_width_set(1.0)
        gpu.state.blend_set('NONE')


def brush_weights(obj, bm, project, center, radius, view=None):
    """The vertices of `bm` (the edit mesh of `obj`; keep it while using the vertices) under the
    brush: [(vert, world point, world normal, weight)], the weight 1 at the middle falling off to 0
    at the rim. `project(world)` gives the screen position (None off screen); with `view` (the view
    direction) vertices facing away are left out, so the brush doesn't reach through to the back."""
    bm.normal_update()
    world = obj.matrix_world
    normal_matrix = world.to_3x3().inverted_safe().transposed()
    found = []
    for v in bm.verts:
        if v.hide:
            continue
        normal = (normal_matrix @ v.normal).normalized()
        if view is not None and normal.dot(view) > 0.0:
            continue
        point = world @ v.co
        screen = project(point)
        if screen is None:
            continue
        d = (Vector(screen) - Vector(center)).length
        if d <= radius:
            found.append((v, point, normal, (1.0 - (d / radius) ** 2) ** 2))
    return found


def conform_at(obj, surface, project, center, radius, strength, view=None, direction='TARGET'):
    """One dab of the Conform brush: the vertices under it move towards the surface, `strength` at
    the middle falling off to nothing at the rim. `direction` is the normal they move along (see
    Surface.conform). Returns how many moved."""
    inverse = obj.matrix_world.inverted_safe()
    bm = bmesh.from_edit_mesh(obj.data)
    moved = 0
    for v, point, normal, weight in brush_weights(obj, bm, project, center, radius, view):
        target = surface.conform(point, normal, direction)
        if target is not None:
            v.co = inverse @ point.lerp(target, strength * weight)
            moved += 1
    if moved:
        bmesh.update_edit_mesh(obj.data, loop_triangles=True, destructive=False)
    return moved


def relax_at(obj, surface, project, center, radius, strength, view=None, direction='TARGET'):
    """One dab of Conform Relax: the vertices under the brush move towards the middle of their
    neighbours, then onto the surface. Border vertices stay. Returns how many moved."""
    world = obj.matrix_world
    inverse = world.inverted_safe()
    bm = bmesh.from_edit_mesh(obj.data)
    moves = []
    for v, point, normal, weight in brush_weights(obj, bm, project, center, radius, view):
        if not v.link_edges or v.is_boundary:
            continue
        middle = sum((world @ e.other_vert(v).co for e in v.link_edges), Vector()) / len(v.link_edges)
        relaxed = point.lerp(middle, strength * weight)
        target = surface.conform(relaxed, normal, direction)
        moves.append((v, relaxed if target is None else relaxed.lerp(target, weight)))
    # All from the shape as it was, so the order doesn't matter.
    for v, point in moves:
        v.co = inverse @ point
    if moves:
        bmesh.update_edit_mesh(obj.data, loop_triangles=True, destructive=False)
    return len(moves)


def transform_conform(obj, surface, grabbed, transform, direction='TARGET'):
    """Conform Move / Rotate / Scale: `grabbed` is [(vert, world point, world normal, weight)] as
    the drag started; each vertex goes to `transform(point, weight)` and from there onto the
    surface (all the way at the middle of the brush, less towards the rim)."""
    inverse = obj.matrix_world.inverted_safe()
    for v, point, normal, weight in grabbed:
        moved = transform(point, weight)
        target = surface.conform(moved, normal, direction)
        v.co = inverse @ (moved if target is None else moved.lerp(target, weight))
    if grabbed:
        bmesh.update_edit_mesh(obj.data, loop_triangles=True, destructive=False)
    return len(grabbed)


CONFORM_BRUSHES = (
    ('CONFORM', "Conform", "Paint over the mesh: the vertices under the brush move onto the Draw On surface"),
    ('MOVE', "Conform Move", "Drag: the vertices under the brush move along the surface, staying on it"),
    ('ROTATE', "Conform Rotate", "Drag around the brush: the vertices under it turn about its middle, "
     "staying on the surface"),
    ('SCALE', "Conform Scale", "Drag right to spread, left to gather the vertices under the brush, "
     "staying on the surface"),
    ('RELAX', "Conform Relax", "Paint over the mesh: the vertices under the brush even out, staying on the surface"),
)


class MAXIMIZE_OT_freeform_conform_brush(Operator):
    """Conform brushes ([ and ] size the brush; right-click or Esc ends). Started in Object Mode,
    they edit the mesh and go back to Object Mode at the end"""
    bl_idname = "maximize.freeform_conform_brush"
    bl_label = "Conform"
    bl_options = {'REGISTER', 'UNDO'}

    mode: EnumProperty(name="Brush", items=CONFORM_BRUSHES)

    @classmethod
    def description(cls, _context, properties):
        return next(d for k, _n, d in CONFORM_BRUSHES if k == properties.mode) + \
            " ([ and ] size the brush; right-click or Esc ends)"

    @classmethod
    def poll(cls, context):
        obj = context.edit_object or context.active_object
        return obj is not None and obj.type == 'MESH' and obj.mode in {'EDIT', 'OBJECT'} and \
            can_draw(context, obj)

    def invoke(self, context, event):
        if context.region_data is None:
            from .vocabulary import view3d_override
            override = view3d_override(context)
            if override is None:
                return {'CANCELLED'}
            with context.temp_override(**override):
                bpy.ops.maximize.freeform_conform_brush('INVOKE_DEFAULT', mode=self.mode)
            return {'FINISHED'}
        obj = context.edit_object or context.active_object
        self._back_to_object = obj.mode == 'OBJECT'
        if self._back_to_object:
            bpy.ops.object.mode_set(mode='EDIT')
        self._obj = obj
        self._region = context.region
        self._rv3d = context.region_data
        self._surface = Surface(context, obj)
        self._settings = settings(context)
        self._painting = False
        self._mouse = None
        self._grab = None
        self._moved = 0
        self._area = context.area
        self._state = ui_state(context)
        self._handle = bpy.types.SpaceView3D.draw_handler_add(self._draw, (), 'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        name = next(n for k, n, _d in CONFORM_BRUSHES if k == self.mode)
        action = "paint over the mesh" if self.mode in {'CONFORM', 'RELAX'} else "drag"
        context.area.header_text_set("{}: {}; [ ] brush size; right-click or Esc ends".format(name, action))
        return {'RUNNING_MODAL'}

    def _project(self, point):
        return view3d_utils.location_3d_to_region_2d(self._region, self._rv3d, point)

    def _view(self):
        return view3d_utils.region_2d_to_vector_3d(self._region, self._rv3d, self._mouse)

    def _dab(self):
        s = self._settings
        paint = conform_at if self.mode == 'CONFORM' else relax_at
        self._moved += paint(self._obj, self._surface, self._project, self._mouse, s.brush_size,
                             s.brush_strength, self._view(), s.conform_direction)

    def _start_drag(self):
        """Move / Rotate / Scale: what is under the brush as the drag starts, and its middle."""
        self._bm = bmesh.from_edit_mesh(self._obj.data)
        grabbed = brush_weights(self._obj, self._bm, self._project, self._mouse, self._settings.brush_size,
                                self._view())
        if not grabbed:
            return
        hit = self._surface.cast(self._region, self._rv3d, self._mouse)
        total = sum(w for _v, _p, _n, w in grabbed)
        pivot = sum((p * w for _v, p, _n, w in grabbed), Vector()) / total
        normal = hit[1] if hit is not None else -self._view()
        self._grab = (grabbed, self._mouse.copy(), pivot, normal.normalized())

    def _drag(self):
        grabbed, start, pivot, normal = self._grab
        region, rv3d = self._region, self._rv3d
        if self.mode == 'MOVE':
            a = view3d_utils.region_2d_to_location_3d(region, rv3d, start, pivot)
            b = view3d_utils.region_2d_to_location_3d(region, rv3d, self._mouse, pivot)
            delta = b - a

            def transform(p, w):
                return p + delta * w
        elif self.mode == 'ROTATE':
            a, b = start - self._centre_start(), self._mouse - self._centre_start()
            if a.length < 1.0 or b.length < 1.0:
                return
            angle = -a.angle_signed(b)
            # Screen angles turn the other way round the surface's normal when it faces away.
            if normal.dot(self._view()) > 0.0:
                angle = -angle

            def transform(p, w):
                return pivot + Matrix.Rotation(angle * w, 3, normal) @ (p - pivot)
        else:
            factor = math.exp((self._mouse.x - start.x) / 200.0)

            def transform(p, w):
                return pivot + (p - pivot) * (1.0 + (factor - 1.0) * w)
        self._moved = transform_conform(self._obj, self._surface, grabbed, transform,
                                        self._settings.conform_direction)

    def _centre_start(self):
        """Rotate turns about the screen position of the middle of what it grabbed."""
        return self._project(self._grab[2]) or self._grab[1]

    def _centre(self):
        return self._grab[1] if self._grab is not None else self._mouse

    def _end(self):
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        self._area.header_text_set(None)
        self._area.tag_redraw()
        if self._back_to_object and self._obj.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'} if self._moved else {'CANCELLED'}

    def modal(self, context, event):
        self._area.tag_redraw()
        if ui_state(context) != self._state:
            # A button elsewhere changed the tool, mode or object: the brush is done.
            self._back_to_object = False
            return self._end()
        if outside(self._region, event) and not self._painting:
            # Buttons, panels, the Outliner and menus work while the brush is on.
            self._mouse = None
            return {'PASS_THROUGH'}
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE', 'TRACKPADPAN', 'TRACKPADZOOM'} or \
                event.type.startswith('NDOF'):
            return {'PASS_THROUGH'}
        if event.type in {'MOUSEMOVE', 'LEFTMOUSE', 'INBETWEEN_MOUSEMOVE'}:
            self._mouse = Vector((event.mouse_x - self._region.x, event.mouse_y - self._region.y))
        painting = self.mode in {'CONFORM', 'RELAX'}
        if event.type == 'LEFTMOUSE':
            self._painting = event.value == 'PRESS'
            if self._painting:
                if painting:
                    self._dab()
                else:
                    self._start_drag()
            else:
                self._grab = None
            return {'RUNNING_MODAL'}
        if event.type == 'MOUSEMOVE' and self._painting:
            if painting:
                self._dab()
            elif self._grab is not None:
                self._drag()
            return {'RUNNING_MODAL'}
        if event.value == 'PRESS' and event.type in {'LEFT_BRACKET', 'RIGHT_BRACKET'}:
            s = self._settings
            s.brush_size = int(s.brush_size * (0.9 if event.type == 'LEFT_BRACKET' else 1.0 / 0.9) + 0.5)
            return {'RUNNING_MODAL'}
        if event.value == 'PRESS' and event.type in {'RIGHTMOUSE', 'ESC', 'RET', 'NUMPAD_ENTER', 'SPACE'}:
            return self._end()
        return {'RUNNING_MODAL'}

    def _draw(self):
        try:
            mouse, radius = self._centre(), self._settings.brush_size
        except ReferenceError:
            return
        if mouse is None:
            return
        points = [(mouse.x + radius * math.cos(a * math.tau / 48), mouse.y + radius * math.sin(a * math.tau / 48))
                  for a in range(49)]
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        gpu.state.blend_set('ALPHA')
        shader.uniform_float("color", (1.0, 0.55, 0.1, 0.9))
        batch_for_shader(shader, 'LINE_STRIP', {"pos": points}).draw(shader)
        gpu.state.blend_set('NONE')


class MAXIMIZE_OT_freeform_conform(Operator):
    """Conform All: put the selected vertices (all, with none selected) onto the Draw On surface now"""
    bl_idname = "maximize.freeform_conform"
    bl_label = "Conform All"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.edit_object
        return obj is not None and obj.type == 'MESH' and can_draw(context, obj)

    def execute(self, context):
        obj = context.edit_object
        surface = Surface(context, obj)
        if not surface.usable:
            self.report({'WARNING'}, "Select polygons to draw on" if settings(context).draw_on == 'SELECTION'
                        else "Nothing to conform to")
            return {'CANCELLED'}
        direction = settings(context).conform_direction
        bm = bmesh.from_edit_mesh(obj.data)
        bm.normal_update()
        verts = [v for v in bm.verts if v.select and not v.hide] or [v for v in bm.verts if not v.hide]
        world = obj.matrix_world
        inverse = world.inverted_safe()
        normal_matrix = world.to_3x3().inverted_safe().transposed()
        # All from the shape as it was, so the order doesn't change the normals.
        targets = [(v, surface.conform(world @ v.co, (normal_matrix @ v.normal).normalized(), direction))
                   for v in verts]
        moved = 0
        for v, p in targets:
            if p is not None:
                v.co = inverse @ p
                moved += 1
        bmesh.update_edit_mesh(obj.data)
        return {'FINISHED'} if moved else {'CANCELLED'}


_TOOLS = (
    ('DRAG', "Drag", "Move vertices; they stay on the surface (Move tool with surface snapping)"),
    ('STEP_BUILD', "Step Build", "Click to add vertices on the surface, drag to make polygons "
     "(Blender's Poly Build: Ctrl+click adds, Shift+click removes)"),
    ('EXTEND', "Extend", "Drag a border edge or vertex out to make new polygons (Blender's Poly Build)"),
    ('OPTIMIZE', "Optimize", "Remove vertices and edges you click (Blender's Poly Build: Shift+click)"),
)


class MAXIMIZE_OT_freeform_tool(Operator):
    """Switch to a Freeform tool"""
    bl_idname = "maximize.freeform_tool"
    bl_label = "Freeform Tool"

    tool: EnumProperty(name="Tool", items=_TOOLS)

    @classmethod
    def description(cls, _context, properties):
        return next(d for k, _n, d in _TOOLS if k == properties.tool)

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        from .vocabulary import view3d_override
        override = view3d_override(context) if context.area is None or context.area.type != 'VIEW_3D' else None
        tool = "builtin.move" if self.tool == 'DRAG' else "builtin.poly_build"
        if override is not None:
            with context.temp_override(**override):
                bpy.ops.wm.tool_set_by_id(name=tool)
        else:
            bpy.ops.wm.tool_set_by_id(name=tool)
        _drawing_setup(context)
        return {'FINISHED'}


class MAXIMIZE_OT_freeform_solve(Operator):
    """Solve Surface: weld the drawn pieces, make the polygons face one way and smooth the shading,
    edges sharper than the Angle staying hard"""
    bl_idname = "maximize.freeform_solve"
    bl_label = "Solve Surface"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        angle = settings(context).solve_angle
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles(threshold=0.0001)
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.mesh.faces_shade_smooth()
        if hasattr(bpy.ops.mesh, "set_sharpness_by_angle"):
            bpy.ops.mesh.set_sharpness_by_angle(angle=angle)
        return {'FINISHED'}


# ------------------------------------------------------------------------------
# Panel


def draw(layout, context, obj, mod):
    """The Freeform modifier's rollouts: Draw On, PolyDraw, Display."""
    from .ui import ToolGrid, rollout
    s = settings(context)
    # Draw On (Surface, Offset, Conform) are the modifier's own inputs, above.
    layout.operator("maximize.freeform_new_object", icon='ADD')
    body = rollout(layout, "mx_freeform_polydraw", "PolyDraw")
    if body:
        if context.mode != 'EDIT_MESH':
            body.label(text="Edit the mesh to draw on the surface", icon='INFO')
        body.row(align=True).prop(s, "draw_on", expand=True)
        grid = ToolGrid(body)
        for tool, text in (('DRAG', "Drag"), ('STEP_BUILD', "Step Build"), ('EXTEND', "Extend"),
                           ('OPTIMIZE', "Optimize")):
            grid.operator("maximize.freeform_tool", text=text).tool = tool
        for mode, text, _d in CONFORM_BRUSHES:
            grid.operator("maximize.freeform_conform_brush", text=text).mode = mode
        grid.operator("maximize.freeform_conform")
        for kind, text, _d in DRAW_KINDS:
            grid.operator("maximize.freeform_draw", text=text).kind = kind
        grid.pad()
        col = body.column(align=True)
        col.prop(s, "min_distance")
        col.prop(s, "width")
        col.prop(s, "surface_segments")
        col.prop(s, "branch_taper")
        col = body.column(align=True)
        col.row(align=True).prop(s, "conform_direction", expand=True)
        col.prop(s, "brush_size")
        col.prop(s, "brush_strength")
        row = body.row(align=True)
        row.operator("maximize.freeform_solve")
        row.prop(s, "solve_angle")
    body = rollout(layout, "mx_freeform_display", "Display", closed=True)
    if body:
        from .vocabulary import view3d_override
        override = view3d_override(context)
        overlay = override["area"].spaces.active.overlay if override else None
        if overlay is not None and hasattr(overlay, "show_retopology"):
            body.prop(overlay, "show_retopology", text="See the Surface Through (Retopology)")
            body.prop(overlay, "retopology_offset", text="Offset")


def _draw_add_menu(self, context):
    obj = context.object
    if obj is not None and obj.type == 'MESH':
        self.layout.operator("maximize.freeform_add", text="Freeform (Max)", icon='GREASEPENCIL')


_MENUS = ("OBJECT_MT_modifier_add_flat", "OBJECT_MT_modifier_add")

classes = (
    MaximizeFreeformSettings,
    MAXIMIZE_OT_freeform_add,
    MAXIMIZE_OT_freeform_new_object,
    MAXIMIZE_OT_freeform_draw,
    MAXIMIZE_OT_freeform_conform_brush,
    MAXIMIZE_OT_freeform_conform,
    MAXIMIZE_OT_freeform_tool,
    MAXIMIZE_OT_freeform_solve,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.maximize_freeform = PointerProperty(type=MaximizeFreeformSettings)
    for name in _MENUS:
        menu = getattr(bpy.types, name, None)
        if menu is not None:
            menu.append(_draw_add_menu)
            break


def unregister():
    for name in _MENUS:
        menu = getattr(bpy.types, name, None)
        if menu is not None:
            try:
                menu.remove(_draw_add_menu)
            except ValueError:
                pass
    del bpy.types.Scene.maximize_freeform
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
