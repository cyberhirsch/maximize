# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Editable (parametric) primitives built from Geometry Nodes.

Each primitive is an object whose geometry comes from a "Parameters" Geometry Nodes modifier, so
its size and segments stay editable until it is collapsed (Convert to Editable Poly). Box, Cylinder,
Cone and Tube have their pivot at the base, as in Max. Shapes are curve objects with their
parameters on the curve data (`shapes.py`); they are created the same way.
"""

import bpy
from bpy.props import EnumProperty
from bpy.types import Operator
from bpy_extras import view3d_utils
from mathutils import Matrix, Vector
from mathutils.geometry import intersect_line_plane

from .nodes import GroupBuilder, draw_modifier_inputs, find_group, modifier_input
from .shapes import (
    SHAPE_KINDS, SHAPE_STEPS, SHAPES, create_shape, draw_shape_parameters, shape_input, shape_kind,
)

MODIFIER_NAME = "Parameters"

KINDS = (
    ('BOX', "Box", "", 'MESH_CUBE', 0),
    ('SPHERE', "Sphere", "", 'MESH_UVSPHERE', 1),
    ('CYLINDER', "Cylinder", "", 'MESH_CYLINDER', 2),
    ('CONE', "Cone", "", 'MESH_CONE', 3),
    ('TUBE', "Tube", "", 'MESH_CIRCLE', 4),
    ('TORUS', "Torus", "", 'MESH_TORUS', 5),
    ('PLANE', "Plane", "", 'MESH_PLANE', 6),
) + SHAPE_KINDS

DIST = 'NodeSocketFloat'
INT = 'NodeSocketInt'
BOOL = 'NodeSocketBool'


def _build_box(b):
    length = b.input("Length", DIST, 1.0, 0.0, subtype='DISTANCE')
    width = b.input("Width", DIST, 1.0, 0.0, subtype='DISTANCE')
    height = b.input("Height", DIST, 1.0, 0.0, subtype='DISTANCE')
    l_segs = b.input("Length Segs", INT, 1, 1, 200)
    w_segs = b.input("Width Segs", INT, 1, 1, 200)
    h_segs = b.input("Height Segs", INT, 1, 1, 200)
    cube = b.node('GeometryNodeMeshCube', {
        "Size": b.combine(width, length, height),
        "Vertices X": b.math('ADD', w_segs, 1.0),
        "Vertices Y": b.math('ADD', l_segs, 1.0),
        "Vertices Z": b.math('ADD', h_segs, 1.0),
    })
    geo = b.store_uv(cube.outputs["Mesh"], cube.outputs["UV Map"])
    return b.node('GeometryNodeTransform', {
        "Geometry": geo, "Translation": b.combine(z=b.math('MULTIPLY', height, 0.5))}).outputs[0]


def _build_sphere(b):
    radius = b.input("Radius", DIST, 0.5, 0.0, subtype='DISTANCE')
    segments = b.input("Segments", INT, 32, 4, 500)
    smooth = b.input("Smooth", BOOL, True)
    sphere = b.node('GeometryNodeMeshUVSphere', {
        "Segments": segments, "Rings": b.math('MAXIMUM', b.math('DIVIDE', segments, 2.0), 3.0), "Radius": radius})
    geo = b.store_uv(sphere.outputs["Mesh"], sphere.outputs["UV Map"])
    return b.node('GeometryNodeSetShadeSmooth', {"Mesh": geo, "Shade Smooth": smooth}).outputs[0]


def _build_cylinder(b, cone=False):
    if cone:
        radius1 = b.input("Radius 1", DIST, 0.5, 0.0, subtype='DISTANCE')
        radius2 = b.input("Radius 2", DIST, 0.0, 0.0, subtype='DISTANCE')
    else:
        radius1 = b.input("Radius", DIST, 0.5, 0.0, subtype='DISTANCE')
    height = b.input("Height", DIST, 1.0, 0.0, subtype='DISTANCE')
    h_segs = b.input("Height Segments", INT, 1, 1, 200)
    c_segs = b.input("Cap Segments", INT, 1, 1, 100)
    sides = b.input("Sides", INT, 24, 3, 500)
    smooth = b.input("Smooth", BOOL, True)
    if cone:
        prim = b.node('GeometryNodeMeshCone', {
            "Vertices": sides, "Side Segments": h_segs, "Fill Segments": c_segs,
            "Radius Top": radius2, "Radius Bottom": radius1, "Depth": height})
    else:
        prim = b.node('GeometryNodeMeshCylinder', {
            "Vertices": sides, "Side Segments": h_segs, "Fill Segments": c_segs,
            "Radius": radius1, "Depth": height})
    geo = b.store_uv(prim.outputs["Mesh"], prim.outputs["UV Map"])
    geo = b.node('GeometryNodeSetShadeSmooth', {
        "Mesh": geo, "Selection": prim.outputs["Side"], "Shade Smooth": smooth}).outputs[0]
    if cone:
        # The Cone node already starts at z = 0.
        return geo
    return b.node('GeometryNodeTransform', {
        "Geometry": geo, "Translation": b.combine(z=b.math('MULTIPLY', height, 0.5))}).outputs[0]


def _build_tube(b):
    radius1 = b.input("Radius 1", DIST, 0.5, 0.0, subtype='DISTANCE')
    radius2 = b.input("Radius 2", DIST, 0.3, 0.0, subtype='DISTANCE')
    height = b.input("Height", DIST, 1.0, 0.0, subtype='DISTANCE')
    sides = b.input("Sides", INT, 24, 3, 500)
    smooth = b.input("Smooth", BOOL, True)
    # Sweep a rectangle (the wall's cross section) around a circle in the middle of the wall.
    path = b.node('GeometryNodeCurvePrimitiveCircle', {
        "Resolution": sides, "Radius": b.math('MULTIPLY', b.math('ADD', radius1, radius2), 0.5)})
    profile = b.node('GeometryNodeCurvePrimitiveQuadrilateral', {
        "Width": b.math('ABSOLUTE', b.math('SUBTRACT', radius1, radius2)), "Height": height})
    mesh = b.node('GeometryNodeCurveToMesh', {"Curve": path.outputs[0], "Profile Curve": profile.outputs[0]})
    # UVs: U around the tube; V up the walls, and from inner to outer radius on the caps.
    px, py, pz = b.separate(b.node('GeometryNodeInputPosition').outputs[0])
    radial = b.vmath('LENGTH', b.combine(px, py))
    wall_v = b.math('ADD', b.math('DIVIDE', pz, b.math('MAXIMUM', height, 1e-6)), 0.5)
    cap_v = b.math('DIVIDE', b.math('SUBTRACT', radial, b.math('MINIMUM', radius1, radius2)),
                   b.math('MAXIMUM', b.math('ABSOLUTE', b.math('SUBTRACT', radius1, radius2)), 1e-6))
    _nx, _ny, nz = b.separate(b.on_faces(b.node('GeometryNodeInputNormal').outputs["Normal"], 'FLOAT_VECTOR'))
    is_cap = b.node('FunctionNodeCompare', {"A": b.math('ABSOLUTE', nz), "B": 0.5},
                    data_type='FLOAT', operation='GREATER_THAN').outputs[0]
    v = b.node('GeometryNodeSwitch', {"Switch": is_cap, "False": wall_v, "True": cap_v},
               input_type='FLOAT').outputs[0]
    geo = b.store_uv(mesh.outputs[0], b.combine(b.seam_angle(py, px), v))
    geo = b.node('GeometryNodeSetShadeSmooth', {"Mesh": geo, "Shade Smooth": smooth}).outputs[0]
    return b.node('GeometryNodeTransform', {
        "Geometry": geo, "Translation": b.combine(z=b.math('MULTIPLY', height, 0.5))}).outputs[0]


def _build_torus(b):
    radius1 = b.input("Radius 1", DIST, 0.75, 0.0, subtype='DISTANCE')
    radius2 = b.input("Radius 2", DIST, 0.25, 0.0, subtype='DISTANCE')
    segments = b.input("Segments", INT, 24, 3, 500)
    sides = b.input("Sides", INT, 12, 3, 500)
    smooth = b.input("Smooth", BOOL, True)
    path = b.node('GeometryNodeCurvePrimitiveCircle', {"Resolution": segments, "Radius": radius1})
    profile = b.node('GeometryNodeCurvePrimitiveCircle', {"Resolution": sides, "Radius": radius2})
    mesh = b.node('GeometryNodeCurveToMesh', {"Curve": path.outputs[0], "Profile Curve": profile.outputs[0]})
    # UVs: U around the ring, V around the tube.
    px, py, pz = b.separate(b.node('GeometryNodeInputPosition').outputs[0])
    radial = b.math('SUBTRACT', b.vmath('LENGTH', b.combine(px, py)), radius1)
    geo = b.store_uv(mesh.outputs[0], b.combine(b.seam_angle(py, px), b.seam_angle(pz, radial)))
    return b.node('GeometryNodeSetShadeSmooth', {"Mesh": geo, "Shade Smooth": smooth}).outputs[0]


def _build_plane(b):
    length = b.input("Length", DIST, 2.0, 0.0, subtype='DISTANCE')
    width = b.input("Width", DIST, 2.0, 0.0, subtype='DISTANCE')
    l_segs = b.input("Length Segs", INT, 4, 1, 1000)
    w_segs = b.input("Width Segs", INT, 4, 1, 1000)
    grid = b.node('GeometryNodeMeshGrid', {
        "Size X": width, "Size Y": length,
        "Vertices X": b.math('ADD', w_segs, 1.0), "Vertices Y": b.math('ADD', l_segs, 1.0)})
    return b.store_uv(grid.outputs["Mesh"], grid.outputs["UV Map"])


_BUILDERS = {
    'BOX': _build_box,
    'SPHERE': _build_sphere,
    'CYLINDER': _build_cylinder,
    'CONE': lambda b: _build_cylinder(b, cone=True),
    'TUBE': _build_tube,
    'TORUS': _build_torus,
    'PLANE': _build_plane,
}


def kind_label(kind):
    return next(name for ident, name, *_ in KINDS if ident == kind)


def ensure_group(kind):
    name = "MX " + kind_label(kind)
    group = find_group(name)
    if group is None:
        builder = GroupBuilder(name, kind)
        geometry_out = builder.output()
        builder.set(geometry_out, _BUILDERS[kind](builder))
        group = builder.tree
    return group


def primitive_modifier(obj):
    """The Parameters modifier of an editable primitive, or None. Shapes saved by earlier versions
    have one too."""
    if obj is None:
        return None
    mod = obj.modifiers.get(MODIFIER_NAME)
    if mod is not None and mod.type == 'NODES' and mod.node_group is not None and \
            (mod.node_group.get("maximize_kind") in _BUILDERS or mod.node_group.get("maximize_kind") in SHAPES):
        return mod
    return None


def is_parametric(obj):
    """An editable primitive or shape whose parameters can still be changed."""
    return primitive_modifier(obj) is not None or shape_kind(obj) is not None


def draw_parameters(layout, obj):
    """Draw the parameters of an editable primitive or shape, like Max's Parameters rollout."""
    if shape_kind(obj) is not None:
        draw_shape_parameters(layout, obj)
        return True
    mod = primitive_modifier(obj)
    if mod is None:
        return False
    draw_modifier_inputs(layout, mod)
    return True


def _max_name(base):
    """Max-style names: Box001, Box002..."""
    i = 1
    while "{:s}{:03d}".format(base, i) in bpy.data.objects:
        i += 1
    return "{:s}{:03d}".format(base, i)


# Interactive creation steps per primitive, as in Max: the first step is a drag on the grid,
# the others follow the mouse until the next click.
#   RECT: drag a rectangle (Width, Length); RADIUS: drag from the center (Radius / Radius 1);
#   HEIGHT: move up or down; RADIUS2: move in the grid plane (Radius 2).
STEPS = {
    'BOX': ('RECT', 'HEIGHT'),
    'PLANE': ('RECT',),
    'SPHERE': ('RADIUS',),
    'CYLINDER': ('RADIUS', 'HEIGHT'),
    'CONE': ('RADIUS', 'HEIGHT', 'RADIUS2'),
    'TUBE': ('RADIUS', 'RADIUS2', 'HEIGHT'),
    'TORUS': ('RADIUS', 'RADIUS2'),
    **SHAPE_STEPS,
}
_RADIUS_INPUT = {'SPHERE': "Radius", 'CYLINDER': "Radius", 'CIRCLE': "Radius", 'ARC': "Radius", 'NGON': "Radius"}
_SIZE_INPUTS = ("Width", "Length", "Radius", "Radius 1")


def _create_object(context, kind, matrix):
    name = _max_name(kind_label(kind))
    if kind in SHAPES:
        obj = create_shape(context, kind, name)
    else:
        obj = bpy.data.objects.new(name, bpy.data.meshes.new(name))
        obj.modifiers.new(MODIFIER_NAME, 'NODES').node_group = ensure_group(kind)
    context.collection.objects.link(obj)
    obj.matrix_world = matrix
    for other in context.selected_objects:
        other.select_set(False)
    obj.select_set(True)
    context.view_layer.objects.active = obj
    return obj


def parameter(obj, name):
    """A parameter of an editable primitive or shape by its UI name; read and write its `value`."""
    if shape_kind(obj) is not None:
        return shape_input(obj, name)
    return modifier_input(obj.modifiers[MODIFIER_NAME], name)


def _has_input(obj, name):
    try:
        parameter(obj, name)
    except KeyError:
        return False
    return True


def _grid_plane(rv3d):
    """Construction plane of a view: the ground in perspective, the view plane in axis views."""
    ground = (Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1)))
    if rv3d.is_perspective:
        return ground
    rot = rv3d.view_rotation
    axes = [rot @ Vector(a) for a in ((1, 0, 0), (0, 1, 0), (0, 0, 1))]
    if max(abs(c) for c in axes[2]) < 0.999:
        return ground
    return tuple(Vector([round(c) for c in axis]) for axis in axes)


def autogrid_hit(context, region, mouse):
    """Max's AutoGrid: (point, u, v, normal) of the surface under the mouse when AutoGrid is on,
    else None."""
    if not context.scene.get("maximize_autogrid"):
        return None
    rv3d = region.data
    origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, mouse)
    direction = view3d_utils.region_2d_to_vector_3d(region, rv3d, mouse)
    hit, location, normal, _index, _obj, _matrix = context.scene.ray_cast(
        context.evaluated_depsgraph_get(), origin, direction)
    if not hit:
        return None
    normal = normal.normalized()
    # A tangent axis: the world X projected onto the surface, or Y when X is along the normal.
    u = Vector((1, 0, 0)) if abs(normal.x) < 0.9 else Vector((0, 1, 0))
    u = (u - normal * u.dot(normal)).normalized()
    return location, u, normal.cross(u), normal


class MAXIMIZE_OT_autogrid(Operator):
    """AutoGrid, as in Max: new objects are built on the surface under the mouse"""
    bl_idname = "maximize.autogrid"
    bl_label = "AutoGrid"
    bl_options = {'REGISTER'}

    def execute(self, context):
        context.scene["maximize_autogrid"] = not context.scene.get("maximize_autogrid", False)
        self.report({'INFO'}, "AutoGrid " + ("on" if context.scene["maximize_autogrid"] else "off"))
        return {'FINISHED'}


class MAXIMIZE_OT_add_primitive(Operator):
    """Create an editable primitive: drag in the viewport to size it, as in Max. Its parameters stay
    editable until you collapse it"""
    bl_idname = "maximize.add_primitive"
    bl_label = "Add Editable Primitive"
    bl_options = {'REGISTER', 'UNDO'}

    kind: EnumProperty(name="Type", items=KINDS)

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        """Without a mouse (scripts, redo): create with default sizes at the 3D cursor."""
        _create_object(context, self.kind, context.scene.cursor.matrix)
        return {'FINISHED'}

    # Interactive creation: stays in create mode for more objects until right-click or Esc.

    def invoke(self, context, _event):
        if context.area is None or context.area.type != 'VIEW_3D':
            return self.execute(context)
        self._obj = None
        self._step = 0
        self._region = None
        self._created = 0
        context.window_manager.modal_handler_add(self)
        context.window.cursor_modal_set('CROSSHAIR')
        self._status(context)
        return {'RUNNING_MODAL'}

    def _status(self, context):
        label = kind_label(self.kind)
        if self._obj is None:
            text = "Create {:s}: drag in a viewport (right-click or Esc to stop)".format(label)
        else:
            hints = {'RECT': "drag the base", 'RADIUS': "drag the radius",
                     'HEIGHT': "move to set the height, click to confirm",
                     'RADIUS2': "move to set the second radius, click to confirm"}
            text = "Create {:s}: {:s}".format(label, hints[STEPS[self.kind][self._step]])
        context.workspace.status_text_set(text)

    def _region_at(self, context, event):
        for region in context.area.regions:
            if (region.type == 'WINDOW' and region.x <= event.mouse_x < region.x + region.width and
                    region.y <= event.mouse_y < region.y + region.height):
                return region
        return None

    def _mouse(self, event):
        return (event.mouse_x - self._region.x, event.mouse_y - self._region.y)

    def _hit(self, event):
        """Mouse position on the construction plane."""
        rv3d = self._region.data
        co = self._mouse(event)
        origin = view3d_utils.region_2d_to_origin_3d(self._region, rv3d, co)
        direction = view3d_utils.region_2d_to_vector_3d(self._region, rv3d, co)
        return intersect_line_plane(origin, origin + direction, self._plane_origin, self._n)

    def _input(self, name):
        return parameter(self._obj, name)

    def _update(self, event):
        self._apply(event)
        # Setting modifier inputs from Python doesn't tag the object for re-evaluation.
        self._obj.update_tag()

    def _apply(self, event):
        step = STEPS[self.kind][self._step]
        if step == 'HEIGHT':
            dy = self._mouse(event)[1] - self._ref_y
            self._input("Height").value = abs(dy) * self._pixel
            return
        hit = self._hit(event)
        if hit is None:
            return
        d = hit - self._p0
        if step == 'RECT':
            du, dv = d.dot(self._u), d.dot(self._v)
            self._input("Width").value = abs(du)
            self._input("Length").value = abs(dv)
            self._obj.matrix_world.translation = self._p0 + self._u * (du / 2) + self._v * (dv / 2)
        elif step == 'RADIUS':
            self._input(_RADIUS_INPUT.get(self.kind, "Radius 1")).value = d.length
        elif step == 'RADIUS2':
            radius = d.length
            if self.kind == 'TORUS':
                # The second torus radius is measured from the ring, not from the center.
                radius = abs(d.length - self._input("Radius 1").value)
            self._input("Radius 2").value = radius

    def _begin(self, context, event):
        self._region = self._region_at(context, event)
        if self._region is None:
            return False
        self._u, self._v, self._n = _grid_plane(self._region.data)
        self._plane_origin = Vector()
        surface = autogrid_hit(context, self._region, self._mouse(event))
        if surface is not None:
            # AutoGrid: build on the surface under the mouse, facing out of it.
            self._plane_origin, self._u, self._v, self._n = surface
        hit = self._hit(event)
        if hit is None:
            return False
        self._p0 = hit
        basis = Matrix((self._u, self._v, self._n)).transposed().to_4x4()
        self._obj = _create_object(context, self.kind, Matrix.Translation(hit) @ basis)
        # Start the drag-sized inputs at zero so the object grows with the mouse.
        for name in _SIZE_INPUTS + ("Height",):
            if _has_input(self._obj, name):
                self._input(name).value = 0.0
        self._step = 0
        return True

    def _next_step(self, event):
        if self._step == 0 and all(self._input(n).value < 1e-6 for n in _SIZE_INPUTS if _has_input(self._obj, n)):
            # A click without a drag creates nothing.
            bpy.data.objects.remove(self._obj)
            self._obj = None
            return
        self._step += 1
        if self._step >= len(STEPS[self.kind]):
            self._obj = None
            self._created += 1
            return
        # The height follows the mouse in screen pixels, scaled to world units at the object's depth.
        rv3d = self._region.data
        x, y = self._mouse(event)
        depth = self._obj.matrix_world.translation
        a = view3d_utils.region_2d_to_location_3d(self._region, rv3d, (x, y), depth)
        b = view3d_utils.region_2d_to_location_3d(self._region, rv3d, (x, y + 100), depth)
        self._pixel = (b - a).length / 100.0
        self._ref_y = y

    def _end(self, context):
        context.workspace.status_text_set(None)
        context.window.cursor_modal_restore()
        return {'FINISHED'} if self._created else {'CANCELLED'}

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'} and event.value == 'PRESS':
            if self._obj is not None:
                bpy.data.objects.remove(self._obj)
                self._obj = None
            return self._end(context)
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE', 'WHEELINMOUSE', 'WHEELOUTMOUSE',
                          'TRACKPADPAN', 'TRACKPADZOOM'}:
            return {'PASS_THROUGH'}
        if event.type == 'MOUSEMOVE' and self._obj is not None:
            self._update(event)
        elif event.type == 'LEFTMOUSE':
            if self._obj is None:
                if event.value == 'PRESS':
                    if self._region_at(context, event) is None:
                        # Clicking outside the viewport ends create mode.
                        return self._end(context)
                    self._begin(context, event)
                    self._status(context)
            elif (self._step == 0 and event.value == 'RELEASE') or (self._step > 0 and event.value == 'PRESS'):
                self._update(event)
                self._next_step(event)
                self._status(context)
        return {'RUNNING_MODAL'}


def _entry_fields(kind):
    """(property, parameter name) pairs Keyboard Entry offers for a kind, from its creation steps."""
    fields = []
    for step in STEPS[kind]:
        if step == 'RECT':
            fields += [("length", "Length"), ("width", "Width")]
        elif step == 'RADIUS':
            fields.append(("radius", _RADIUS_INPUT.get(kind, "Radius 1")))
        elif step == 'RADIUS2':
            fields.append(("radius2", "Radius 2"))
        elif step == 'HEIGHT':
            fields.append(("height", "Height"))
    return fields


class MAXIMIZE_OT_keyboard_entry(Operator):
    """Keyboard Entry, as in Max: create a primitive or shape at a typed position with typed sizes"""
    bl_idname = "maximize.keyboard_entry"
    bl_label = "Keyboard Entry"
    bl_options = {'REGISTER', 'UNDO'}

    kind: EnumProperty(name="Type", items=KINDS)
    location: bpy.props.FloatVectorProperty(name="Position", subtype='TRANSLATION', unit='LENGTH')
    length: bpy.props.FloatProperty(name="Length", default=1.0, min=0.0, unit='LENGTH')
    width: bpy.props.FloatProperty(name="Width", default=1.0, min=0.0, unit='LENGTH')
    radius: bpy.props.FloatProperty(name="Radius", default=0.5, min=0.0, unit='LENGTH')
    radius2: bpy.props.FloatProperty(name="Radius 2", default=0.25, min=0.0, unit='LENGTH')
    height: bpy.props.FloatProperty(name="Height", default=1.0, unit='LENGTH')

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def invoke(self, context, _event):
        self.location = context.scene.cursor.location
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, _context):
        layout = self.layout
        layout.use_property_split = True
        layout.prop(self, "kind")
        layout.prop(self, "location")
        for prop, name in _entry_fields(self.kind):
            layout.prop(self, prop, text=name)

    def execute(self, context):
        obj = _create_object(context, self.kind, Matrix.Translation(self.location))
        for prop, name in _entry_fields(self.kind):
            parameter(obj, name).value = getattr(self, prop)
        obj.update_tag()
        return {'FINISHED'}


class MAXIMIZE_MT_create(bpy.types.Menu):
    bl_label = "Standard Primitives"
    bl_idname = "MAXIMIZE_MT_create"

    def draw(self, _context):
        layout = self.layout
        for ident, name, _desc, icon, _num in KINDS:
            if ident not in SHAPES:
                layout.operator("maximize.add_primitive", text=name, icon=icon).kind = ident
        _draw_create_options(layout)


def _draw_create_options(layout):
    layout.separator()
    layout.operator("maximize.keyboard_entry", icon='KEYINGSET')
    layout.operator("maximize.autogrid", icon='CHECKBOX_HLT' if bpy.context.scene.get("maximize_autogrid")
                    else 'CHECKBOX_DEHLT')


class MAXIMIZE_MT_create_shapes(bpy.types.Menu):
    bl_label = "Shapes"
    bl_idname = "MAXIMIZE_MT_create_shapes"

    def draw(self, _context):
        layout = self.layout
        layout.operator("maximize.line", icon='IPO_LINEAR')
        for ident, name, _desc, icon, _num in SHAPE_KINDS:
            layout.operator("maximize.add_primitive", text=name, icon=icon).kind = ident
        layout.operator("object.text_add", text="Text", icon='OUTLINER_OB_FONT')
        layout.operator("maximize.freehand", icon='GREASEPENCIL')
        layout.operator("maximize.section", icon='MOD_BOOLEAN')
        _draw_create_options(layout)


def is_shape(obj):
    if shape_kind(obj) is not None:
        return True
    mod = primitive_modifier(obj)
    return mod is not None and mod.node_group.get("maximize_kind") in SHAPES


class MAXIMIZE_OT_convert_spline(Operator):
    """Convert the shape to an editable spline: its splines stay, its parameters go"""
    bl_idname = "maximize.convert_spline"
    bl_label = "Convert to Editable Spline"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and is_shape(context.active_object)

    def execute(self, context):
        from .shapes import to_editable_spline
        to_editable_spline(context, context.active_object)
        return {'FINISHED'}


def _menu_add(self, _context):
    self.layout.separator()
    self.layout.menu("MAXIMIZE_MT_create", icon='MESH_CUBE')
    self.layout.menu("MAXIMIZE_MT_create_shapes", icon='CURVE_DATA')


classes = (
    MAXIMIZE_OT_add_primitive,
    MAXIMIZE_MT_create,
    MAXIMIZE_MT_create_shapes,
    MAXIMIZE_OT_convert_spline,
    MAXIMIZE_OT_keyboard_entry,
    MAXIMIZE_OT_autogrid,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_add.append(_menu_add)


def unregister():
    bpy.types.VIEW3D_MT_add.remove(_menu_add)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
