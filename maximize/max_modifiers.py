# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Max's modifiers that Blender lacks, as Geometry Nodes groups: Extrude (with Bevel and Bevel
Profile as its other two modes), Noise, Normal and STL Check.

Each one is a Geometry Nodes modifier, so stock Blender evaluates it unchanged; only Moritz's
modifier list knows their Max names. They are added from the Add Modifier list.
"""

import bpy
from bpy.props import EnumProperty
from bpy.types import Operator

from .nodes import GroupBuilder, find_group, modifier_input

DIST = 'NodeSocketFloat'


# ------------------------------------------------------------------------------
# Extrude / Bevel / Bevel Profile

EXTRUDE_MODES = (
    ('EXTRUDE', "Extrude", "Extrude the shape straight up (its local Z)"),
    ('BEVEL', "Bevel", "Extrude in up to three levels, each with a height and an outline"),
    ('PROFILE', "Profile", "Sweep a profile shape around the shape"),
)


def _miter(b):
    """Per point of a poly curve in the XY plane: the direction that moves it out by 1 on both
    neighboring segments (a mitered outline, as Max's Outline and Bevel do)."""
    position = b.node('GeometryNodeInputPosition').outputs[0]
    index = b.node('GeometryNodeInputIndex').outputs[0]
    up = b.combine(z=1.0)

    def neighbor(offset):
        node = b.node('GeometryNodeOffsetPointInCurve', {"Point Index": index, "Offset": offset})
        at = b.node('GeometryNodeFieldAtIndex', {"Index": node.outputs["Point Index"], "Value": position},
                    data_type='FLOAT_VECTOR', domain='POINT').outputs[0]
        return node.outputs["Is Valid Offset"], at

    def side(a, c):
        return b.vmath('NORMALIZE', b.vmath('CROSS_PRODUCT', b.vmath('SUBTRACT', c, a), up))

    prev_ok, prev = neighbor(-1)
    next_ok, nxt = neighbor(1)
    # At an open end there is only one segment.
    after = b.node('GeometryNodeSwitch', {"Switch": next_ok, "False": side(prev, position),
                                          "True": side(position, nxt)}, input_type='VECTOR').outputs[0]
    before = b.node('GeometryNodeSwitch', {"Switch": prev_ok, "False": after,
                                           "True": side(prev, position)}, input_type='VECTOR').outputs[0]
    bisector = b.vmath('NORMALIZE', b.vmath('ADD', before, after))
    cos = b.math('MAXIMUM', b.vmath('DOT_PRODUCT', bisector, after), 0.2)
    return b.node('ShaderNodeVectorMath', {0: bisector, "Scale": b.math('DIVIDE', 1.0, cos)},
                  operation='SCALE').outputs["Vector"]


def _build_extrude(b):
    shape = b.input("Geometry", 'NodeSocketGeometry')
    mode = b.node('GeometryNodeMenuSwitch', data_type='INT')
    items = mode.enum_items
    while len(items) > 0:
        items.remove(items[0])
    for _ident, name, _desc in EXTRUDE_MODES:
        items.new(name)
    for i in range(len(EXTRUDE_MODES)):
        mode.inputs[i + 1].default_value = i
    b.set(mode.inputs[0], b.input("Mode", 'NodeSocketMenu'))
    mode_value = mode.outputs[0]
    amount = b.input("Amount", DIST, 0.1, subtype='DISTANCE')
    segments = b.input("Segments", 'NodeSocketInt', 1, 1, 1000)
    start_outline = b.input("Start Outline", DIST, 0.0, subtype='DISTANCE')
    levels = []
    for i in range(3):
        on = b.input("Level {:d}".format(i + 1), 'NodeSocketBool', i == 0)
        h = b.input("Level {:d} Height".format(i + 1), DIST, 0.1 if i == 0 else 0.0, subtype='DISTANCE')
        o = b.input("Level {:d} Outline".format(i + 1), DIST, 0.0, subtype='DISTANCE')
        levels.append((on, h, o))
    profile_object = b.input("Profile", 'NodeSocketObject')
    cap_start = b.input("Cap Start", 'NodeSocketBool', True)
    cap_end = b.input("Cap End", 'NodeSocketBool', True)
    flip = b.input("Flip Normals", 'NodeSocketBool', False)
    smooth = b.input("Smooth", 'NodeSocketBool', False)

    def is_mode(i):
        return b.node('FunctionNodeCompare', {"A": mode_value, "B": i}, data_type='INT', operation='EQUAL').outputs[0]

    def pick(cond, if_false, if_true, kind='FLOAT'):
        return b.node('GeometryNodeSwitch', {"Switch": cond, "False": if_false, "True": if_true},
                      input_type=kind).outputs[0]

    def store(geometry, name, value, data_type='FLOAT'):
        return b.node('GeometryNodeStoreNamedAttribute', {"Geometry": geometry, "Name": name, "Value": value},
                      data_type=data_type, domain='POINT').outputs[0]

    def named(name, data_type='FLOAT'):
        return b.node('GeometryNodeInputNamedAttribute', {"Name": name}, data_type=data_type).outputs[0]

    def sample(geometry, value, index):
        return b.node('GeometryNodeSampleIndex', {"Geometry": geometry, "Value": value, "Index": index},
                      data_type='FLOAT', domain='POINT', clamp=True).outputs[0]

    # The profile, as points (outline, height): Extrude is a straight line of Segments pieces,
    # Bevel a polyline through the levels, Profile another shape's spline (its X out, Y up).
    line = b.node('GeometryNodeCurvePrimitiveLine', {"End": b.combine(0.0, amount)}).outputs[0]
    line = b.node('GeometryNodeResampleCurve', {"Curve": line, "Count": b.math('ADD', segments, 1)}).outputs[0]
    corners = [(b.combine(start_outline, 0.0), None)]
    height = 0.0
    outline = start_outline
    for on, h, o in levels:
        height = b.math('ADD', height, b.math('MULTIPLY', h, on))
        outline = b.math('ADD', outline, b.math('MULTIPLY', o, on))
        corners.append((b.combine(outline, height), on))
    points = b.node('GeometryNodeJoinGeometry')
    # Join Geometry puts the last linked input first: link the last level first.
    for corner, on in reversed(corners):
        point = b.node('GeometryNodePoints', {"Count": 1, "Position": corner}).outputs[0]
        if on is not None:
            off = b.node('FunctionNodeBooleanMath', {0: on}, operation='NOT').outputs[0]
            point = b.node('GeometryNodeDeleteGeometry', {"Geometry": point, "Selection": off},
                           domain='POINT').outputs[0]
        b.set(points.inputs[0], point)
    bevel = b.node('GeometryNodePointsToCurves', {"Points": points.outputs[0]}).outputs[0]
    picked = b.node('GeometryNodeObjectInfo', {"Object": profile_object}, transform_space='ORIGINAL').outputs["Geometry"]
    picked = b.node('GeometryNodeRealizeInstances', {"Geometry": picked}).outputs[0]
    picked = b.node('GeometryNodeResampleCurve', {"Curve": picked}, mode='EVALUATED').outputs[0]
    profile = pick(is_mode(1), line, bevel, 'GEOMETRY')
    profile = pick(is_mode(2), profile, picked, 'GEOMETRY')
    profile_pos = b.separate(b.node('GeometryNodeInputPosition').outputs[0])
    profile = store(profile, "mx_out", profile_pos[0])
    profile = store(profile, "mx_up", profile_pos[1])
    # Clamped, a large index samples the last point.
    last = 1 << 30
    start_out, start_up = sample(profile, profile_pos[0], 0), sample(profile, profile_pos[1], 0)
    end_out, end_up = sample(profile, profile_pos[0], last), sample(profile, profile_pos[1], last)

    # The shape as a poly line in its XY plane, with each point's base position and miter.
    path = b.node('GeometryNodeResampleCurve', {"Curve": shape}, mode='EVALUATED').outputs[0]
    path = b.node('GeometryNodeTransform', {"Geometry": path, "Scale": b.combine(1.0, 1.0, 0.0)}).outputs[0]
    path = store(path, "mx_base", b.node('GeometryNodeInputPosition').outputs[0], 'FLOAT_VECTOR')
    # A clockwise shape (by its signed area) turns the miter and the faces around, so outlines go
    # out and normals face out whichever way the shape was drawn.
    position = b.node('GeometryNodeInputPosition').outputs[0]
    step = b.node('GeometryNodeOffsetPointInCurve', {"Point Index": b.node('GeometryNodeInputIndex').outputs[0],
                                                     "Offset": 1})
    following = b.node('GeometryNodeFieldAtIndex', {"Index": step.outputs["Point Index"], "Value": position},
                       data_type='FLOAT_VECTOR', domain='POINT').outputs[0]
    here, there = b.separate(position), b.separate(following)
    cross = b.math('SUBTRACT', b.math('MULTIPLY', here[0], there[1]), b.math('MULTIPLY', there[0], here[1]))
    cross = b.math('MULTIPLY', cross, step.outputs["Is Valid Offset"])
    area = b.node('GeometryNodeAttributeStatistic', {"Geometry": path, "Attribute": cross},
                  data_type='FLOAT', domain='POINT').outputs["Sum"]
    clockwise = b.node('FunctionNodeCompare', {"A": area, "B": 0.0}, data_type='FLOAT',
                       operation='LESS_THAN').outputs[0]
    turn = b.node('GeometryNodeSwitch', {"Switch": clockwise, "False": 1.0, "True": -1.0},
                  input_type='FLOAT').outputs[0]
    miter = b.node('ShaderNodeVectorMath', {0: _miter(b), "Scale": turn}, operation='SCALE').outputs["Vector"]
    path = store(path, "mx_side", miter, 'FLOAT_VECTOR')

    def placed(out, up):
        """Base + miter * outline + Z * height."""
        side = b.node('ShaderNodeVectorMath', {0: named("mx_side", 'FLOAT_VECTOR'), "Scale": out},
                      operation='SCALE').outputs["Vector"]
        return b.vmath('ADD', b.vmath('ADD', named("mx_base", 'FLOAT_VECTOR'), side), b.combine(z=up))

    walls = b.node('GeometryNodeCurveToMesh', {"Curve": path, "Profile Curve": profile}).outputs[0]
    walls = b.node('GeometryNodeSetPosition', {"Geometry": walls, "Position": placed(
        named("mx_out"), named("mx_up"))}).outputs[0]
    no_profile = b.node('FunctionNodeBooleanMath', {0: is_mode(2)}, operation='NOT').outputs[0]

    # Caps: the shape filled at the start and at the end of the profile.
    def cap(out, up, on, flip_cap):
        ring = b.node('GeometryNodeSetPosition', {"Geometry": path, "Position": placed(out, 0.0)}).outputs[0]
        mesh = b.node('GeometryNodeFillCurve', {"Curve": ring, "Mode": "N-gons"}).outputs[0]
        mesh = b.node('GeometryNodeTransform', {"Geometry": mesh, "Translation": b.combine(z=up)}).outputs[0]
        # Fill Curve faces follow the drawing direction, as the walls do.
        turned = b.node('FunctionNodeBooleanMath', {0: clockwise, 1: flip_cap}, operation='XOR').outputs[0]
        mesh = b.node('GeometryNodeFlipFaces', {"Mesh": mesh, "Selection": turned}).outputs[0]
        keep = b.node('FunctionNodeBooleanMath', {0: on, 1: no_profile}, operation='AND').outputs[0]
        return b.node('GeometryNodeSwitch', {"Switch": keep, "True": mesh}, input_type='GEOMETRY').outputs[0]

    joined = b.node('GeometryNodeJoinGeometry')
    b.set(joined.inputs[0], cap(end_out, end_up, cap_end, True))
    b.set(joined.inputs[0], cap(start_out, start_up, cap_start, False))
    b.set(joined.inputs[0], walls)
    mesh = b.node('GeometryNodeMergeByDistance', {"Geometry": joined.outputs[0], "Distance": 1e-5}).outputs[0]
    for name in ("mx_base", "mx_side", "mx_out", "mx_up"):
        mesh = b.node('GeometryNodeRemoveAttribute', {"Geometry": mesh, "Name": name}).outputs[0]
    # Walls swept along a counterclockwise shape face in: turn them out, unless Flip Normals.
    outward = b.node('FunctionNodeBooleanMath', {0: flip, 1: clockwise}, operation='XNOR').outputs[0]
    mesh = b.node('GeometryNodeFlipFaces', {"Mesh": mesh, "Selection": outward}).outputs[0]
    return b.node('GeometryNodeSetShadeSmooth', {"Mesh": mesh, "Shade Smooth": smooth}, domain='FACE').outputs[0]


# ------------------------------------------------------------------------------
# Noise

def _build_noise(b):
    geometry = b.input("Geometry", 'NodeSocketGeometry')
    seed = b.input("Seed", 'NodeSocketInt', 0, 0)
    scale = b.input("Scale", DIST, 1.0, 0.001, subtype='DISTANCE')
    fractal = b.input("Fractal", 'NodeSocketBool', False)
    roughness = b.input("Roughness", DIST, 0.5, 0.0, 1.0, subtype='FACTOR')
    iterations = b.input("Iterations", DIST, 6.0, 1.0, 10.0)
    strength = b.input("Strength", 'NodeSocketVector', (0.0, 0.0, 0.1), subtype='TRANSLATION')
    animate = b.input("Animate Noise", 'NodeSocketBool', False)
    frequency = b.input("Frequency", DIST, 0.25, 0.0)
    phase = b.input("Phase", DIST, 0.0)
    position = b.node('GeometryNodeInputPosition').outputs[0]
    # Max's Noise: Scale is the size of the noise; Seed moves to another part of it.
    seed_offset = b.node('ShaderNodeVectorMath', {0: b.combine(17.31, 5.73, 11.97), "Scale": seed},
                         operation='SCALE').outputs["Vector"]
    sample = b.vmath('ADD', b.node('ShaderNodeVectorMath', {0: position, 1: b.combine(scale, scale, scale)},
                                   operation='DIVIDE').outputs["Vector"], seed_offset)
    seconds = b.node('GeometryNodeInputSceneTime').outputs["Seconds"]
    time = b.math('ADD', b.math('MULTIPLY', b.math('MULTIPLY', seconds, frequency), animate), phase)
    detail = b.node('GeometryNodeSwitch', {"Switch": fractal, "False": 0.0, "True": iterations},
                    input_type='FLOAT').outputs[0]
    noise = b.node('ShaderNodeTexNoise', {"Vector": sample, "W": time, "Detail": detail, "Roughness": roughness,
                                          "Scale": 1.0}, noise_dimensions='4D').outputs["Color"]
    centered = b.vmath('SUBTRACT', noise, b.combine(0.5, 0.5, 0.5))
    offset = b.vmath('MULTIPLY', b.vmath('MULTIPLY', centered, b.combine(2.0, 2.0, 2.0)), strength)
    return b.node('GeometryNodeSetPosition', {"Geometry": geometry, "Offset": offset}).outputs[0]


# ------------------------------------------------------------------------------
# Normal

def _build_normal(b):
    geometry = b.input("Geometry", 'NodeSocketGeometry')
    flip = b.input("Flip Normals", 'NodeSocketBool', True)
    return b.node('GeometryNodeFlipFaces', {"Mesh": geometry, "Selection": flip}).outputs[0]


# ------------------------------------------------------------------------------
# STL Check

STL_MATERIAL = "MX STL Check"


def _stl_material():
    mat = bpy.data.materials.get(STL_MATERIAL)
    if mat is None:
        mat = bpy.data.materials.new(STL_MATERIAL)
        mat.diffuse_color = (1.0, 0.05, 0.05, 1.0)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf is not None:
            bsdf.inputs["Base Color"].default_value = (1.0, 0.05, 0.05, 1.0)
            bsdf.inputs["Emission Color"].default_value = (1.0, 0.05, 0.05, 1.0)
            bsdf.inputs["Emission Strength"].default_value = 1.0
    return mat


def _build_stl_check(b):
    geometry = b.input("Geometry", 'NodeSocketGeometry')
    check = b.input("Check", 'NodeSocketBool', True)
    open_edges = b.input("Open Edges", 'NodeSocketBool', True)
    multiple = b.input("Multiple Edges", 'NodeSocketBool', True)
    spikes = b.input("Spikes", 'NodeSocketBool', True)
    width = b.input("Mark Width", DIST, 0.005, 0.0, subtype='DISTANCE')
    material = b.input("Material", 'NodeSocketMaterial')
    faces = b.node('GeometryNodeInputMeshEdgeNeighbors').outputs["Face Count"]

    def compare(a, op, value):
        return b.node('FunctionNodeCompare', {"A": a, "B": value}, data_type='INT', operation=op).outputs[0]

    def both(a, c, op='AND'):
        return b.node('FunctionNodeBooleanMath', {0: a, 1: c}, operation=op).outputs[0]

    open_sel = both(compare(faces, 'EQUAL', 1), open_edges)
    multi_sel = both(compare(faces, 'GREATER_THAN', 2), multiple)
    # A spike: a face with no neighbor, sticking out on its own.
    lone = b.node('GeometryNodeInputMeshFaceNeighbors').outputs["Face Count"]
    spike_face = both(compare(lone, 'EQUAL', 0), spikes)
    spike_edge = b.node('GeometryNodeFieldOnDomain', {"Value": spike_face}, domain='EDGE',
                        data_type='BOOLEAN').outputs[0]
    bad = both(both(open_sel, multi_sel, 'OR'), spike_edge, 'OR')
    bad = both(bad, check)

    # Mark the bad edges with thin red tubes, and say how many there are in the modifier.
    curves = b.node('GeometryNodeMeshToCurve', {"Mesh": geometry, "Selection": bad}).outputs[0]
    circle = b.node('GeometryNodeCurvePrimitiveCircle', {"Resolution": 6, "Radius": width}).outputs[0]
    tubes = b.node('GeometryNodeCurveToMesh', {"Curve": curves, "Profile Curve": circle}).outputs[0]
    tubes = b.node('GeometryNodeSetMaterial', {"Geometry": tubes, "Material": material}).outputs[0]
    stats = b.node('GeometryNodeAttributeStatistic', {"Geometry": geometry, "Selection": bad, "Attribute": 1.0},
                   data_type='FLOAT', domain='EDGE').outputs["Sum"]
    count = b.node('FunctionNodeFloatToInt', {"Float": stats}, rounding_mode='ROUND').outputs[0]
    text = b.node('FunctionNodeValueToString', {"Value": count}, data_type='INT').outputs[0]
    join = b.node('GeometryNodeStringJoin', {"Delimiter": ""})
    b.set(join.inputs[1], b.node('FunctionNodeInputString', string=" problem edges (open, multiple or spikes)").outputs[0])
    b.set(join.inputs[1], text)
    warning = b.node('GeometryNodeWarning', {"Show": compare(count, 'GREATER_THAN', 0), "Message": join.outputs[0]},
                     warning_type='WARNING')
    joined = b.node('GeometryNodeJoinGeometry')
    b.set(joined.inputs[0], tubes)
    b.set(joined.inputs[0], geometry)
    # The Warning node passes its Show value on; switching on it keeps the node evaluated.
    return b.node('GeometryNodeSwitch', {"Switch": warning.outputs[0], "False": joined.outputs[0],
                                         "True": joined.outputs[0]}, input_type='GEOMETRY').outputs[0]


# ------------------------------------------------------------------------------
# Adding them

# kind: (group name, builder, modifier name, object types)
KINDS = {
    'EXTRUDE': ("MX Extrude", _build_extrude, "Extrude", {'CURVE', 'FONT'}),
    'NOISE': ("MX Noise", _build_noise, "Noise", {'MESH', 'CURVE', 'FONT', 'SURFACE', 'LATTICE'}),
    'NORMAL': ("MX Normal", _build_normal, "Normal", {'MESH'}),
    'STL_CHECK': ("MX STL Check", _build_stl_check, "STL Check", {'MESH'}),
}


def ensure_group(kind):
    name, build, _label, _types = KINDS[kind]
    group = find_group(name)
    if group is None:
        b = GroupBuilder(name, "max_" + kind.lower())
        out = b.output()
        b.set(out, build(b))
        group = b.tree
    return group


def add_modifier(obj, kind):
    _name, _build, label, _types = KINDS[kind]
    mod = obj.modifiers.new(label, 'NODES')
    mod.node_group = ensure_group(kind)
    if kind == 'STL_CHECK':
        modifier_input(mod, "Material").value = _stl_material()
    return mod


class MAXIMIZE_OT_max_modifier_add(Operator):
    """Add one of Max's modifiers (a Geometry Nodes modifier)"""
    bl_idname = "maximize.max_modifier_add"
    bl_label = "Add Max Modifier"
    bl_options = {'REGISTER', 'UNDO'}

    kind: EnumProperty(name="Modifier", items=[(k, v[2], "") for k, v in KINDS.items()])

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        obj = context.object
        if obj.type not in KINDS[self.kind][3]:
            self.report({'WARNING'}, "{:s} doesn't work on this kind of object".format(KINDS[self.kind][2]))
            return {'CANCELLED'}
        mod = add_modifier(obj, self.kind)
        obj.modifiers.active = mod
        return {'FINISHED'}


def _kind_operator(kind):
    """An operator per modifier, so Moritz's list can add each by its own entry."""
    return type("MAXIMIZE_OT_add_" + kind.lower(), (Operator,), {
        "bl_idname": "maximize.add_" + kind.lower(),
        "bl_label": KINDS[kind][2],
        "bl_description": "Add a {:s} modifier".format(KINDS[kind][2]),
        "bl_options": {'REGISTER', 'UNDO', 'INTERNAL'},
        "poll": classmethod(lambda cls, context: context.object is not None and
                            context.object.type in KINDS[kind][3]),
        "execute": lambda self, context: bpy.ops.maximize.max_modifier_add(kind=kind),
    })


_KEYWORDS = {
    'EXTRUDE': "bevel profile extrude shape spline sweep thickness",
    'NOISE': "random displace jitter fractal turbulence",
    'NORMAL': "flip normals unify faces",
    'STL_CHECK': "3d print errors open edges non manifold holes",
}

classes = (MAXIMIZE_OT_max_modifier_add,) + tuple(_kind_operator(k) for k in KINDS)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    from .vocabulary import modifier_list
    mlist = modifier_list()
    if mlist is not None:
        for kind, (_name, _build, label, types) in KINDS.items():
            mlist.register_entry(label, "maximize.add_" + kind.lower(), _KEYWORDS[kind], sorted(types))


def unregister():
    from .vocabulary import modifier_list
    mlist = modifier_list()
    if mlist is not None:
        for kind in KINDS:
            mlist.unregister_entry("maximize.add_" + kind.lower())
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
