# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Object Paint: Max's tool for painting copies of objects onto the grid, a surface or the
selection.

- Paint Objects: the list of objects to paint with, picked from the selection; each copy is one of
  them at random. Copies are instances: they share the original's mesh.
- Paint On: Grid (the ground, or the view's plane in Top / Front / Side), Surface (any object
  under the brush) or Selection (only the objects selected when painting starts), with an Offset.
- Brush settings: Spacing along the stroke; Align (the copy's X, Y or Z, flipped or not, along the
  surface's normal); Scatter U / V / W; Rotation and Scale (with random amounts, and a uniform
  lock for scale).
- Fill: places a number of copies evenly along the last stroke, in place of what it painted.
- While painting, right-click or Enter commits, Esc cancels the whole session (Max's Commit /
  Cancel).

Blender has no object painter of its own, so this is Maximize's.
"""

import math
import random

import bpy
import gpu
from bpy.props import (BoolProperty, CollectionProperty, EnumProperty, FloatProperty, FloatVectorProperty,
                       IntProperty, PointerProperty)
from bpy.types import Operator, PropertyGroup
from bpy_extras import view3d_utils
from gpu_extras.batch import batch_for_shader
from mathutils import Euler, Matrix, Vector

PAINT_ON = (
    ('GRID', "Grid", "Paint on the grid: the ground, or in a Top / Front / Side view that view's plane"),
    ('SURFACE', "Surface", "Paint on any object under the brush"),
    ('SELECTION', "Selection", "Paint only on the objects selected when painting starts"),
)
AXES = (('X', "X", ""), ('Y', "Y", ""), ('Z', "Z", ""))


class MaximizePaintObject(PropertyGroup):
    obj: PointerProperty(name="Object", type=bpy.types.Object)


class MaximizeObjectPaintSettings(PropertyGroup):
    objects: CollectionProperty(type=MaximizePaintObject)
    active: IntProperty()
    paint_on: EnumProperty(name="Paint On", items=PAINT_ON, default='SURFACE')
    offset: FloatProperty(name="Offset", default=0.0, subtype='DISTANCE',
                          description="Distance of the copies from the surface, along its normal")
    spacing: FloatProperty(name="Spacing", default=1.0, min=0.001, subtype='DISTANCE',
                           description="Distance between the copies along the stroke")
    fill_count: IntProperty(name="Fill #", default=10, min=1, description="Copies Fill places along the last stroke")
    align: EnumProperty(name="Align", items=AXES, default='Z',
                        description="The copies' axis that points along the surface's normal")
    flip: BoolProperty(name="Flip", description="The axis points into the surface instead")
    scatter: FloatVectorProperty(name="Scatter", size=3, default=(0.0, 0.0, 0.0), min=0.0, subtype='XYZ',
                                 description="Random offset along the stroke (U), across it (V) and off the surface (W)")
    rotation: FloatVectorProperty(name="Rotation", size=3, default=(0.0, 0.0, 0.0), subtype='EULER',
                                  description="Rotation of the copies about their own axes")
    rotation_random: FloatVectorProperty(name="Random Rotation", size=3, default=(0.0, 0.0, 0.0), min=0.0,
                                         max=math.pi, subtype='EULER',
                                         description="Up to this much more rotation, at random, either way")
    scale: FloatVectorProperty(name="Scale", size=3, default=(100.0, 100.0, 100.0), min=0.1, subtype='XYZ',
                               description="Scale of the copies, in percent")
    scale_uniform: BoolProperty(name="Uniform", default=True, description="One scale for X, Y and Z (X's)")
    scale_random: FloatProperty(name="Random Scale", default=0.0, min=0.0, max=100.0, subtype='PERCENTAGE',
                                description="Up to this much bigger or smaller, at random")
    seed: IntProperty(name="Seed", default=0, min=0)


def settings(context):
    return context.scene.maximize_object_paint


def paint_objects(context):
    return [item.obj for item in settings(context).objects if item.obj is not None]


# ------------------------------------------------------------------------------
# Placing


_AXIS_VECTORS = {'X': Vector((1.0, 0.0, 0.0)), 'Y': Vector((0.0, 1.0, 0.0)), 'Z': Vector((0.0, 0.0, 1.0))}


def placement(s, point, normal, along, rng):
    """The world matrix of a copy at `point` on a surface with `normal`, the stroke going `along`:
    the chosen axis along the normal, then Rotation, Scatter and Scale (with their random parts
    from `rng`)."""
    normal = normal.normalized()
    side = normal.cross(along)
    if side.length_squared < 1e-12:
        side = normal.orthogonal()
    side.normalize()
    forward = side.cross(normal).normalized()
    # The frame: U along the stroke, V across it, W off the surface.
    frame = Matrix((forward, side, normal)).transposed()
    axis = _AXIS_VECTORS[s.align] * (-1.0 if s.flip else 1.0)
    # Turn the copy so its chosen axis is the frame's W (Z), the next one its U.
    to_frame = axis.rotation_difference(Vector((0.0, 0.0, 1.0))).to_matrix()
    turn = Euler(tuple(s.rotation[i] + rng.uniform(-1.0, 1.0) * s.rotation_random[i] for i in range(3))).to_matrix()
    rotation = frame @ to_frame @ turn
    offset = Vector(tuple(rng.uniform(-1.0, 1.0) * s.scatter[i] for i in range(3)))
    location = point + frame @ Vector((offset.x, offset.y, offset.z + s.offset))
    factor = 1.0 + rng.uniform(-1.0, 1.0) * s.scale_random / 100.0
    scale = Vector((s.scale[0],) * 3 if s.scale_uniform else tuple(s.scale)) * (factor / 100.0)
    return Matrix.LocRotScale(location, rotation.to_quaternion(), scale)


def place(context, source, matrix):
    """A copy of `source` (sharing its data) at `matrix`, in the active collection."""
    copy = source.copy()
    copy.parent = None
    copy.matrix_world = matrix
    context.collection.objects.link(copy)
    return copy


def stroke_points(path, spacing, start=0.0):
    """Points every `spacing` along `path` [(point, normal)]: [(point, normal, direction)], and the
    distance left over after the last one (where the next one is due)."""
    out = []
    due = start
    walked = 0.0
    for (a, na), (b, nb) in zip(path, path[1:]):
        length = (b - a).length
        if length < 1e-9:
            continue
        direction = (b - a) / length
        while due <= walked + length:
            t = (due - walked) / length
            out.append((a.lerp(b, t), na.lerp(nb, t).normalized(), direction))
            due += spacing
        walked += length
    return out, due - walked


def fill_points(path, count):
    """`count` points evenly along `path`, from its start to its end."""
    total = sum((b - a).length for (a, _na), (b, _nb) in zip(path, path[1:]))
    if total < 1e-9 or count < 1:
        return []
    if count == 1:
        points, _rest = stroke_points(path, total * 2.0, total * 0.5)
        return points
    points, _rest = stroke_points(path, total / (count - 1))
    return points[:count]


# ------------------------------------------------------------------------------
# Where the brush is


class PaintSurface:
    """What the brush paints on: the grid, any object (Surface) or the selected ones."""

    def __init__(self, context, rv3d, painted):
        s = settings(context)
        self.mode = s.paint_on
        self.depsgraph = context.evaluated_depsgraph_get()
        self.scene = context.scene
        self.skip = painted
        self.only = set(context.selected_objects) if self.mode == 'SELECTION' else None
        from .freeform import _grid_plane
        self.plane = _grid_plane(rv3d)

    def cast(self, region, rv3d, mouse):
        origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, mouse)
        direction = view3d_utils.region_2d_to_vector_3d(region, rv3d, mouse)
        if self.mode == 'GRID':
            from mathutils.geometry import intersect_line_plane
            co, normal = self.plane
            if abs(direction.dot(normal)) < 1e-6:
                return None
            hit = intersect_line_plane(origin, origin + direction, co, normal)
            return hit, (-normal if normal.dot(direction) > 0.0 else normal.copy())
        start = origin
        for _attempt in range(64):
            hit, location, normal, _index, obj, _matrix = self.scene.ray_cast(self.depsgraph, start, direction)
            if not hit:
                return None
            obj = obj.original
            if obj not in self.skip and (self.only is None or obj in self.only):
                return location, normal
            # Through copies painted in this session, and objects not selected.
            start = location + direction * 1e-4
        return None


class MAXIMIZE_OT_object_paint(Operator):
    """Object Paint: paint copies of the Paint Objects (right-click or Enter commits, Esc cancels)"""
    bl_idname = "maximize.object_paint"
    bl_label = "Paint"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and bool(paint_objects(context))

    def invoke(self, context, event):
        if context.region_data is None:
            from .vocabulary import view3d_override
            override = view3d_override(context)
            if override is None:
                return {'CANCELLED'}
            with context.temp_override(**override):
                bpy.ops.maximize.object_paint('INVOKE_DEFAULT')
            return {'FINISHED'}
        self._region = context.region
        self._rv3d = context.region_data
        self._area = context.area
        self._sources = paint_objects(context)
        self._placed = []
        self._surface = PaintSurface(context, self._rv3d, set(self._sources))
        self._path = None
        self._last = None
        self._due = 0.0
        self._mouse = None
        self._rng = random.Random(settings(context).seed)
        from .freeform import ui_state
        self._state = ui_state(context)
        self._handle = bpy.types.SpaceView3D.draw_handler_add(self._draw, (), 'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        context.area.header_text_set("Object Paint: drag to paint; right-click or Enter commits, Esc cancels")
        return {'RUNNING_MODAL'}

    def _add_point(self, context):
        hit = self._surface.cast(self._region, self._rv3d, self._mouse)
        if hit is None:
            return
        self._path.append(hit)
        s = settings(context)
        if len(self._path) == 1:
            # The first copy where the stroke starts; the next one Spacing further on.
            points, self._due = [(hit[0], hit[1], hit[1].orthogonal())], s.spacing
        else:
            points, self._due = stroke_points(self._path[-2:], s.spacing, self._due)
        for point, normal, along in points:
            copy = place(context, self._rng.choice(self._sources), placement(s, point, normal, along, self._rng))
            self._placed.append(copy)
            self._surface.skip.add(copy)

    def _end(self, context, cancel=False):
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        self._area.header_text_set(None)
        self._area.tag_redraw()
        if cancel:
            for obj in self._placed:
                bpy.data.objects.remove(obj)
            self._placed = []
        elif self._last is not None:
            # Fill works on the last stroke that was committed.
            _last_stroke[:], _last_copies[:] = self._last
        return {'FINISHED'} if self._placed else {'CANCELLED'}

    def modal(self, context, event):
        from .freeform import outside, ui_state
        self._area.tag_redraw()
        if ui_state(context) != self._state:
            return self._end(context)
        if outside(self._region, event) and self._path is None:
            self._mouse = None
            return {'PASS_THROUGH'}
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE', 'TRACKPADPAN', 'TRACKPADZOOM'} or \
                event.type.startswith('NDOF'):
            return {'PASS_THROUGH'}
        if event.type in {'MOUSEMOVE', 'LEFTMOUSE'}:
            self._mouse = Vector((event.mouse_x - self._region.x, event.mouse_y - self._region.y))
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            self._path = []
            self._due = 0.0
            self._stroke_start = len(self._placed)
            self._add_point(context)
            return {'RUNNING_MODAL'}
        if event.type == 'MOUSEMOVE' and self._path is not None:
            self._add_point(context)
            return {'RUNNING_MODAL'}
        if event.type == 'LEFTMOUSE' and event.value == 'RELEASE' and self._path is not None:
            self._last = ([(p.copy(), n.copy()) for p, n in self._path],
                          [o.name for o in self._placed[self._stroke_start:]])
            self._path = None
            return {'RUNNING_MODAL'}
        if event.value == 'PRESS' and event.type == 'ESC':
            return self._end(context, cancel=True)
        if event.value == 'PRESS' and event.type in {'RIGHTMOUSE', 'RET', 'NUMPAD_ENTER', 'SPACE'}:
            return self._end(context)
        return {'RUNNING_MODAL'}

    def _draw(self):
        try:
            mouse = self._mouse
        except ReferenceError:
            return
        if mouse is None:
            return
        points = [(mouse.x + 12.0 * math.cos(a * math.tau / 24), mouse.y + 12.0 * math.sin(a * math.tau / 24))
                  for a in range(25)]
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        gpu.state.blend_set('ALPHA')
        shader.uniform_float("color", (0.27, 0.76, 0.76, 0.9))
        batch_for_shader(shader, 'LINE_STRIP', {"pos": points}).draw(shader)
        gpu.state.blend_set('NONE')


# The last stroke and what it painted, for Fill.
_last_stroke = []
_last_copies = []


def fill(context, path, count, replace=()):
    """Fill: `count` copies evenly along `path`, in place of the objects named in `replace`."""
    for name in replace:
        obj = bpy.data.objects.get(name)
        if obj is not None:
            bpy.data.objects.remove(obj)
    s = settings(context)
    rng = random.Random(s.seed)
    sources = paint_objects(context)
    placed = [place(context, rng.choice(sources), placement(s, point, normal, along, rng))
              for point, normal, along in fill_points(path, count)]
    return placed


class MAXIMIZE_OT_object_paint_fill(Operator):
    """Fill: place Fill # copies evenly along the last stroke, in place of what it painted"""
    bl_idname = "maximize.object_paint_fill"
    bl_label = "Fill"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and len(_last_stroke) > 1 and bool(paint_objects(context))

    def execute(self, context):
        placed = fill(context, _last_stroke, settings(context).fill_count, _last_copies)
        _last_copies[:] = [o.name for o in placed]
        return {'FINISHED'}


class MAXIMIZE_OT_object_paint_pick(Operator):
    """Add the selected objects to the Paint Objects"""
    bl_idname = "maximize.object_paint_pick"
    bl_label = "Add Selected"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bool(context.selected_objects)

    def execute(self, context):
        s = settings(context)
        have = set(paint_objects(context))
        for obj in context.selected_objects:
            if obj not in have:
                s.objects.add().obj = obj
        return {'FINISHED'}


class MAXIMIZE_OT_object_paint_remove(Operator):
    """Remove the object from the Paint Objects (the object itself stays)"""
    bl_idname = "maximize.object_paint_remove"
    bl_label = "Remove"
    bl_options = {'REGISTER', 'UNDO'}

    index: IntProperty()

    def execute(self, context):
        s = settings(context)
        if 0 <= self.index < len(s.objects):
            s.objects.remove(self.index)
        return {'FINISHED'}


def draw(layout, context):
    """Object Paint's controls (the Utilities tab, or the sidebar's Max tab)."""
    s = settings(context)
    layout.label(text="Paint Objects")
    col = layout.column(align=True)
    for i, item in enumerate(s.objects):
        row = col.row(align=True)
        row.label(text=item.obj.name if item.obj else "(deleted)", icon='OBJECT_DATA')
        row.operator("maximize.object_paint_remove", text="", icon='X').index = i
    layout.operator("maximize.object_paint_pick", icon='ADD')
    row = layout.row(align=True)
    row.scale_y = 1.4
    row.operator("maximize.object_paint", icon='BRUSH_DATA')
    row = layout.row(align=True)
    row.operator("maximize.object_paint_fill")
    row.prop(s, "fill_count")
    layout.label(text="Paint On")
    layout.row(align=True).prop(s, "paint_on", expand=True)
    layout.prop(s, "offset")
    layout.label(text="Brush Settings")
    col = layout.column()
    col.prop(s, "spacing")
    row = col.row(align=True)
    row.prop(s, "align", expand=True)
    row.prop(s, "flip", toggle=True)
    col.prop(s, "scatter", text="Scatter U / V / W")
    col.prop(s, "rotation")
    col.prop(s, "rotation_random")
    row = col.row(align=True)
    row.prop(s, "scale", text="Scale %")
    col.prop(s, "scale_uniform")
    col.prop(s, "scale_random")
    col.prop(s, "seed")


class MAXIMIZE_PT_object_paint(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Max"
    bl_label = "Object Paint"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        draw(self.layout, context)


classes = (
    MaximizePaintObject,
    MaximizeObjectPaintSettings,
    MAXIMIZE_OT_object_paint,
    MAXIMIZE_OT_object_paint_fill,
    MAXIMIZE_OT_object_paint_pick,
    MAXIMIZE_OT_object_paint_remove,
    MAXIMIZE_PT_object_paint,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.maximize_object_paint = PointerProperty(type=MaximizeObjectPaintSettings)


def unregister():
    del bpy.types.Scene.maximize_object_paint
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
