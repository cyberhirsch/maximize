# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""The rest of Max's Create panel geometry: GeoSphere and Pyramid (Standard Primitives) and the
Extended Primitives, as Geometry Nodes groups like the primitives in `primitives.py`.

Pivots as in Max: on the base for the objects that stand on the grid (Pyramid, ChamferBox,
ChamferCyl, OilTank, Capsule, Spindle, L-Ext, C-Ext, Gengon, RingWave, Hose, Prism), in the center
for GeoSphere, Hedra and Torus Knot.
"""

import math

from . import quad_caps as qc
from . import teapot_data
from .mx_icons import mx_icon

DIST = 'NodeSocketFloat'
INT = 'NodeSocketInt'
BOOL = 'NodeSocketBool'
FLOAT = 'NodeSocketFloat'

# (ident, label, description, icon, number), in Max's button order per sub-category.
STANDARD_KINDS = (
    ('GEOSPHERE', "GeoSphere", "", 'MESH_ICOSPHERE', 7),
    ('PYRAMID', "Pyramid", "", 'MESH_CONE', 8),
    # Moritz's teapot icon where the build has it (the monkey is Suzanne's).
    ('TEAPOT', "Teapot", "", mx_icon('MX_CR_TEAPOT', 'MESH_MONKEY'), 9),
)
EXTENDED_KINDS = (
    ('HEDRA', "Hedra", "", 'MESH_ICOSPHERE', 40),
    ('CHAMFERBOX', "ChamferBox", "", 'MESH_CUBE', 41),
    ('OILTANK', "OilTank", "", 'MESH_CAPSULE', 42),
    ('SPINDLE', "Spindle", "", 'MESH_CONE', 43),
    ('GENGON', "Gengon", "", 'MESH_CYLINDER', 44),
    ('RINGWAVE', "RingWave", "", 'MESH_CIRCLE', 45),
    ('PRISM', "Prism", "", 'MESH_CONE', 46),
    ('TORUS_KNOT', "Torus Knot", "", 'MESH_TORUS', 47),
    ('CHAMFERCYL', "ChamferCyl", "", 'MESH_CYLINDER', 48),
    ('CAPSULE', "Capsule", "", 'MESH_CAPSULE', 49),
    ('L_EXT', "L-Ext", "", 'MOD_SOLIDIFY', 50),
    ('C_EXT', "C-Ext", "", 'MOD_SOLIDIFY', 51),
    ('HOSE', "Hose", "", 'MOD_SCREW', 52),
)

# Creation steps (see primitives.STEPS) and the inputs each drag sets, where they differ from
# Width / Length, Radius, Height and Radius 2.
STEPS = {
    'GEOSPHERE': ('RADIUS',),
    'PYRAMID': ('RECT', 'HEIGHT'),
    'TEAPOT': ('RADIUS',),
    'HEDRA': ('RADIUS',),
    'CHAMFERBOX': ('RECT', 'HEIGHT'),
    'OILTANK': ('RADIUS', 'HEIGHT'),
    'SPINDLE': ('RADIUS', 'HEIGHT'),
    'GENGON': ('RADIUS', 'HEIGHT'),
    'RINGWAVE': ('RADIUS', 'RADIUS2'),
    'PRISM': ('RECT', 'HEIGHT'),
    'TORUS_KNOT': ('RADIUS', 'RADIUS2'),
    'CHAMFERCYL': ('RADIUS', 'HEIGHT'),
    'CAPSULE': ('RADIUS', 'HEIGHT'),
    'L_EXT': ('RECT', 'HEIGHT'),
    'C_EXT': ('RECT', 'HEIGHT'),
    'HOSE': ('RADIUS', 'HEIGHT'),
}
RECT_INPUTS = {
    'PYRAMID': ("Width", "Depth"),
    'PRISM': ("Side 1 Length", "Side 2 Length"),
    'L_EXT': ("Front Length", "Side Length"),
    'C_EXT': ("Front Length", "Back Length"),
}
# (input, value per dragged distance)
RADIUS_INPUTS = {
    'HOSE': ("Diameter", 2.0),
}
RADIUS2_INPUTS = {
    'RINGWAVE': "Ring Width",
    'TORUS_KNOT': "Section Radius",
}


def _scale(b, vector, factor):
    return b.node('ShaderNodeVectorMath', {"Vector": vector, "Scale": factor}, operation='SCALE').outputs["Vector"]


def _clamp_fillet(b, fillet, *sizes):
    """A fillet no larger than half the smallest size."""
    smallest = sizes[0]
    for size in sizes[1:]:
        smallest = b.math('MINIMUM', smallest, size)
    return b.math('MAXIMUM', b.math('MINIMUM', fillet, b.math('MULTIPLY', smallest, 0.5)), 1e-5)


def _smooth(b, geo, smooth):
    return b.node('GeometryNodeSetShadeSmooth', {"Mesh": geo, "Shade Smooth": smooth}).outputs[0]


def _lift(b, geo, z):
    return b.node('GeometryNodeTransform', {"Geometry": geo, "Translation": b.combine(z=z)}).outputs[0]


def _index_switch(b, index, values, data_type):
    node = b.node('GeometryNodeIndexSwitch', data_type=data_type)
    while len(node.index_switch_items) < len(values):
        node.index_switch_items.new()
    b.set(node.inputs["Index"], index)
    for i, value in enumerate(values):
        b.set(node.inputs[str(i)], value)
    return node.outputs[0]


def _prism(b, corners, height):
    """A closed prism: the polygon `corners` (counter-clockwise (x, y) pairs) extruded up by
    `height`."""
    return _extrude_fill(b, _polygon(b, corners), height)


def _quad_parts_prism(b, corners, parts, height):
    """The prism of `corners` with its caps made of the convex quads `parts` (corner indices,
    counter-clockwise): L-Ext and C-Ext, whose outlines are not convex."""
    walls = b.node('GeometryNodeExtrudeMesh', {
        "Mesh": b.node('GeometryNodeFillCurve', {"Curve": _polygon(b, corners), "Mode": "N-gons"}).outputs[0],
        "Offset": b.combine(z=height), "Individual": False}).outputs[0]
    _x, _y, nz = b.separate(b.node('GeometryNodeInputNormal').outputs[0])
    cap = b.node('FunctionNodeCompare', {"A": b.math('ABSOLUTE', nz), "B": 0.5},
                 data_type='FLOAT', operation='GREATER_THAN').outputs[0]
    walls = b.node('GeometryNodeDeleteGeometry', {"Geometry": walls, "Selection": cap},
                   domain='FACE', mode='ONLY_FACE').outputs[0]
    pieces = [walls]
    for part in parts:
        quad = b.node('GeometryNodeFillCurve', {"Curve": _polygon(b, [corners[i] for i in part]),
                                                "Mode": "N-gons"}).outputs[0]
        pieces.append(b.node('GeometryNodeFlipFaces', {"Mesh": quad}).outputs[0])
        pieces.append(b.node('GeometryNodeSetPosition', {"Geometry": quad, "Offset": b.combine(z=height)}).outputs[0])
    return qc.join_merge(b, *pieces)


def _polygon(b, corners):
    index = b.node('GeometryNodeInputIndex').outputs[0]
    position = _index_switch(b, index, [b.combine(x, y) for x, y in corners], 'VECTOR')
    points = b.node('GeometryNodePoints', {"Count": len(corners), "Position": position}).outputs[0]
    curve = b.node('GeometryNodePointsToCurves', {"Points": points}).outputs[0]
    return b.node('GeometryNodeSetSplineCyclic', {"Curve": curve, "Cyclic": True}).outputs[0]


def _extrude_fill(b, curve, height):
    """A closed curve filled and extruded up by `height`, with its bottom cap."""
    fill = b.node('GeometryNodeFillCurve', {"Curve": curve, "Mode": "N-gons"}).outputs[0]
    top = b.node('GeometryNodeExtrudeMesh', {"Mesh": fill, "Offset": b.combine(z=height),
                                            "Individual": False}).outputs[0]
    bottom = b.node('GeometryNodeFlipFaces', {"Mesh": fill}).outputs[0]
    join = b.node('GeometryNodeJoinGeometry')
    b.set(join.inputs[0], bottom)
    b.set(join.inputs[0], top)
    return b.node('GeometryNodeMergeByDistance', {"Geometry": join.outputs[0], "Distance": 1e-5}).outputs[0]


def _rounded(b, radius, rings, sides, offset):
    """A UV sphere whose halves are pushed apart by `offset(position) -> vector`: rounded boxes and
    cylinders (the sphere's poles, equator and quarter meridians land exactly on the flat sides)."""
    sphere = b.node('GeometryNodeMeshUVSphere', {"Segments": sides, "Rings": rings, "Radius": radius})
    position = b.node('GeometryNodeInputPosition').outputs[0]
    return b.node('GeometryNodeSetPosition', {"Geometry": sphere.outputs["Mesh"],
                                              "Offset": offset(position)}).outputs[0]


# ------------------------------------------------------------------------------
# Standard Primitives


def build_geosphere(b):
    radius = b.input("Radius", DIST, 0.5, 0.0, subtype='DISTANCE')
    segments = b.input("Segments", INT, 4, 1, 7)
    hemisphere = b.input("Hemisphere", BOOL, False)
    smooth = b.input("Smooth", BOOL, True)
    ico = b.node('GeometryNodeMeshIcoSphere', {"Radius": radius, "Subdivisions": segments})
    geo = b.store_uv(ico.outputs["Mesh"], ico.outputs["UV Map"])
    _x, _y, z = b.separate(b.node('GeometryNodeInputPosition').outputs[0])
    below = b.node('FunctionNodeCompare', {"A": z, "B": b.math('MULTIPLY', radius, -1e-4)},
                   data_type='FLOAT', operation='LESS_THAN').outputs[0]
    cut = b.node('GeometryNodeDeleteGeometry', {"Geometry": geo, "Selection": b.node(
        'FunctionNodeBooleanMath', {0: below, 1: hemisphere}, operation='AND').outputs[0]}).outputs[0]
    return _smooth(b, cut, smooth)


def build_pyramid(b):
    width = b.input("Width", DIST, 1.0, 0.0, subtype='DISTANCE')
    depth = b.input("Depth", DIST, 1.0, 0.0, subtype='DISTANCE')
    height = b.input("Height", DIST, 1.0, 0.0, subtype='DISTANCE')
    h_segs = b.input("Height Segs", INT, 1, 1, 200)
    # A four-sided cone turned by 45 degrees is a unit square base, then scaled to Width x Depth.
    cone = b.node('GeometryNodeMeshCone', {
        "Vertices": 4, "Side Segments": h_segs, "Radius Top": 0.0, "Radius Bottom": math.sqrt(0.5),
        "Depth": height})
    geo = b.store_uv(cone.outputs["Mesh"], cone.outputs["UV Map"])
    return b.node('GeometryNodeTransform', {
        "Geometry": geo, "Rotation": (0.0, 0.0, math.pi / 4.0),
        "Scale": b.combine(width, depth, 1.0)}).outputs[0]


# The teapot's parts as patch ranges of `teapot_data.PATCHES`: (input, first, last).
_TEAPOT_PARTS = (("Body", 0, 11), ("Body", 28, 31), ("Handle", 12, 15), ("Spout", 16, 19), ("Lid", 20, 27))
_TEAPOT_BODY_RADIUS = 2.0


def build_teapot(b):
    radius = b.input("Radius", DIST, 0.5, 0.0, subtype='DISTANCE')
    segments = b.input("Segments", INT, 4, 1, 64)
    smooth = b.input("Smooth", BOOL, True)
    parts = {name: b.input(name, BOOL, True) for name in ("Body", "Handle", "Spout", "Lid")}
    # The 16 control points of every patch, in patch order.
    index = b.node('GeometryNodeInputIndex').outputs[0]
    controls = [teapot_data.VERTS[k] for patch in teapot_data.PATCHES for k in patch]
    points = b.node('GeometryNodePoints', {
        "Count": len(controls), "Position": _index_switch(b, index, controls, 'VECTOR')}).outputs[0]
    # A grid of Segments x Segments quads per patch, then each vertex moved onto its patch.
    n = b.math('ADD', segments, 1.0)
    grid = b.node('GeometryNodeMeshGrid', {"Size X": 1.0, "Size Y": 1.0, "Vertices X": n, "Vertices Y": n})
    line = b.node('GeometryNodeMeshLine', {"Count": len(teapot_data.PATCHES)}).outputs[0]
    grids = b.node('GeometryNodeInstanceOnPoints', {"Points": line, "Instance": grid.outputs["Mesh"]}).outputs[0]
    mesh = b.node('GeometryNodeRealizeInstances', {"Geometry": grids}).outputs[0]
    per_patch = b.math('MULTIPLY', n, n)
    patch = b.math('FLOOR', b.math('DIVIDE', index, per_patch))
    local = b.math('SUBTRACT', index, b.math('MULTIPLY', patch, per_patch))
    # Grid vertices run along Y first.
    u = b.math('DIVIDE', b.math('FLOOR', b.math('DIVIDE', local, n)), segments)
    v = b.math('DIVIDE', b.math('FLOORED_MODULO', local, n), segments)

    def bernstein(t):
        s = b.math('SUBTRACT', 1.0, t)
        return (b.math('MULTIPLY', b.math('MULTIPLY', s, s), s),
                b.math('MULTIPLY', b.math('MULTIPLY', b.math('MULTIPLY', s, s), t), 3.0),
                b.math('MULTIPLY', b.math('MULTIPLY', b.math('MULTIPLY', t, t), s), 3.0),
                b.math('MULTIPLY', b.math('MULTIPLY', t, t), t))

    bu, bv = bernstein(u), bernstein(v)
    first = b.math('MULTIPLY', patch, 16.0)
    position = b.node('GeometryNodeInputPosition').outputs[0]
    total = None
    for row in range(4):
        for col in range(4):
            sample = b.node('GeometryNodeSampleIndex', {
                "Geometry": points, "Value": position, "Index": b.math('ADD', first, row * 4 + col)},
                data_type='FLOAT_VECTOR', domain='POINT').outputs[0]
            term = _scale(b, sample, b.math('MULTIPLY', bu[row], bv[col]))
            total = term if total is None else b.vmath('ADD', total, term)
    mesh = b.node('GeometryNodeSetPosition', {"Geometry": mesh, "Position": total}).outputs[0]
    mesh = b.store_uv(mesh, b.combine(u, v))
    # Leave out the parts that are off.
    hidden = None
    for name, lo, hi in _TEAPOT_PARTS:
        inside = b.node('FunctionNodeCompare', {"A": patch, "B": (lo + hi) / 2.0, "Epsilon": (hi - lo) / 2.0 + 0.1},
                        data_type='FLOAT', operation='EQUAL').outputs[0]
        off = b.node('FunctionNodeBooleanMath', {0: inside, 1: parts[name]}, operation='NIMPLY').outputs[0]
        hidden = off if hidden is None else b.node('FunctionNodeBooleanMath', {0: hidden, 1: off},
                                                   operation='OR').outputs[0]
    mesh = b.node('GeometryNodeDeleteGeometry', {"Geometry": mesh, "Selection": hidden}, domain='POINT').outputs[0]
    mesh = b.node('GeometryNodeMergeByDistance', {"Geometry": mesh, "Distance": 1e-4}).outputs[0]
    # The patches wind inward.
    mesh = b.node('GeometryNodeFlipFaces', {"Mesh": mesh}).outputs[0]
    scale = b.math('DIVIDE', radius, _TEAPOT_BODY_RADIUS)
    mesh = b.node('GeometryNodeTransform', {"Geometry": mesh, "Scale": b.combine(scale, scale, scale)}).outputs[0]
    return _smooth(b, mesh, smooth)


# ------------------------------------------------------------------------------
# Extended Primitives


def build_hedra(b):
    radius = b.input("Radius", DIST, 0.5, 0.0, subtype='DISTANCE')
    family = b.input("Family", INT, 0, 0, 6)
    b.tree.interface.items_tree["Family"].description = (
        "0 Tetrahedron, 1 Cube, 2 Octahedron, 3 Dodecahedron, 4 Icosahedron, 5 Star1 (small stellated "
        "dodecahedron), 6 Star2 (great stellated dodecahedron)")
    # Max's Axis Scaling: the centers of the triangles (P), squares (Q) and pentagons (R) pushed out.
    axis = [b.input(name, FLOAT, 100.0, 0.0, 1000.0) for name in ("Axis Scaling P", "Axis Scaling Q",
                                                                  "Axis Scaling R")]
    # Tetrahedron: every other corner of a cube; the others are duals (face centers).
    cube = b.node('GeometryNodeMeshCube', {"Size": b.combine(1.0, 1.0, 1.0)}).outputs["Mesh"]
    x, y, z = b.separate(b.node('GeometryNodeInputPosition').outputs[0])
    odd = b.node('FunctionNodeCompare', {"A": b.math('MULTIPLY', b.math('MULTIPLY', x, y), z), "B": 0.0},
                 data_type='FLOAT', operation='LESS_THAN').outputs[0]
    tetra_points = b.node('GeometryNodeDeleteGeometry', {"Geometry": cube, "Selection": odd}).outputs[0]
    tetra = b.node('GeometryNodeConvexHull', {"Geometry": tetra_points}).outputs[0]
    octa = b.node('GeometryNodeDualMesh', {"Mesh": cube}).outputs[0]
    ico = b.node('GeometryNodeMeshIcoSphere', {"Radius": 1.0, "Subdivisions": 1}).outputs["Mesh"]
    dodeca = b.node('GeometryNodeDualMesh', {"Mesh": ico}).outputs[0]
    # Each scaled to a circumradius of 1 before the Radius.
    shapes = [
        (tetra, 2.0 / math.sqrt(3.0)),
        (cube, 2.0 / math.sqrt(3.0)),
        (octa, 2.0),
        (dodeca, 1.0 / 0.7946544723),
        (ico, 1.0),
        (dodeca, 1.0 / 0.7946544723),
        (ico, 1.0),
    ]
    scaled = [b.node('GeometryNodeTransform', {"Geometry": geo, "Scale": (s, s, s)}).outputs[0]
              for geo, s in shapes]
    chosen = _index_switch(b, family, scaled, 'GEOMETRY')
    # Star1: pentagonal spikes on the dodecahedron whose sides are its neighbors' planes (apex at
    # sqrt(5) of the inradius); Star2: triangular spikes on the icosahedron (golden-triangle sides,
    # apex at 3x the inradius).
    sides = b.node('GeometryNodeInputMeshFaceNeighbors').outputs["Vertex Count"]

    def is_family(n):
        return b.node('FunctionNodeCompare', {"A": family, "B": n}, data_type='INT', operation='EQUAL').outputs[0]

    def pick(condition, true, false):
        return b.node('GeometryNodeSwitch', {"Switch": condition, "False": false, "True": true},
                      input_type='FLOAT').outputs[0]

    def sides_are(n):
        return b.node('FunctionNodeCompare', {"A": sides, "B": n}, data_type='INT', operation='EQUAL').outputs[0]
    p, q, r = (b.math('DIVIDE', a, 100.0) for a in axis)
    p = b.math('MULTIPLY', p, pick(is_family(6), 3.0, 1.0))
    r = b.math('MULTIPLY', r, pick(is_family(5), math.sqrt(5.0), 1.0))
    factor = pick(sides_are(3), p, pick(sides_are(4), q, r))
    poke = b.node('FunctionNodeCompare', {"A": b.math('ABSOLUTE', b.math('SUBTRACT', factor, 1.0)), "B": 1e-4},
                  data_type='FLOAT', operation='GREATER_THAN').outputs[0]
    extrude = b.node('GeometryNodeExtrudeMesh', {"Mesh": chosen, "Selection": poke, "Offset Scale": 0.0,
                                                 "Individual": True})
    # Each poked face shrinks to its center, moved out by the factor: a pyramid.
    center = b.node('ShaderNodeVectorMath', {0: b.node('GeometryNodeInputPosition').outputs[0], "Scale": factor},
                    operation='SCALE').outputs['Vector']
    spiked = b.node('GeometryNodeScaleElements', {"Geometry": extrude.outputs["Mesh"],
                                                  "Selection": extrude.outputs["Top"], "Scale": 0.0,
                                                  "Center": center}, domain='FACE').outputs[0]
    spiked = b.node('GeometryNodeMergeByDistance', {"Geometry": spiked, "Distance": 1e-5}).outputs[0]
    # The stars at a radius of 1 to their spikes' tips.
    fit = _index_switch(b, family, [1.0, 1.0, 1.0, 1.0, 1.0, 1.0 / (0.7946544723 * math.sqrt(5.0)),
                                    1.0 / (0.7946544723 * 3.0)], 'FLOAT')
    size = b.math('MULTIPLY', radius, fit)
    return b.node('GeometryNodeTransform', {"Geometry": spiked, "Scale": b.combine(size, size, size)}).outputs[0]


def build_torus_knot(b):
    radius = b.input("Radius", DIST, 0.5, 0.0, subtype='DISTANCE')
    segments = b.input("Segments", INT, 120, 3, 2000)
    p = b.input("P", FLOAT, 2.0, 1.0, 50.0)
    q = b.input("Q", FLOAT, 3.0, 1.0, 50.0)
    section = b.input("Section Radius", DIST, 0.08, 0.0, subtype='DISTANCE')
    sides = b.input("Sides", INT, 12, 3, 200)
    smooth = b.input("Smooth", BOOL, True)
    circle = b.node('GeometryNodeCurvePrimitiveCircle', {"Resolution": segments, "Radius": 1.0}).outputs[0]
    t = b.math('MULTIPLY', b.node('GeometryNodeSplineParameter').outputs["Factor"], 2.0 * math.pi)
    # (p, q) torus knot: around the ring p times, through it q times.
    ring = b.math('ADD', radius, b.math('MULTIPLY', b.math('MULTIPLY', radius, 0.4),
                                       b.math('COSINE', b.math('MULTIPLY', q, t))))
    pt = b.math('MULTIPLY', p, t)
    position = b.combine(b.math('MULTIPLY', ring, b.math('COSINE', pt)),
                         b.math('MULTIPLY', ring, b.math('SINE', pt)),
                         b.math('MULTIPLY', b.math('MULTIPLY', radius, 0.4),
                                b.math('SINE', b.math('MULTIPLY', q, t))))
    path = b.node('GeometryNodeSetPosition', {"Geometry": circle, "Position": position}).outputs[0]
    profile = b.node('GeometryNodeCurvePrimitiveCircle', {"Resolution": sides, "Radius": section}).outputs[0]
    mesh = b.node('GeometryNodeCurveToMesh', {"Curve": path, "Profile Curve": profile}).outputs[0]
    return _smooth(b, mesh, smooth)


def build_chamferbox(b):
    length = b.input("Length", DIST, 1.0, 0.0, subtype='DISTANCE')
    width = b.input("Width", DIST, 1.0, 0.0, subtype='DISTANCE')
    height = b.input("Height", DIST, 1.0, 0.0, subtype='DISTANCE')
    fillet = b.input("Fillet", DIST, 0.1, 0.0, subtype='DISTANCE')
    fillet_segs = b.input("Fillet Segs", INT, 3, 1, 50)
    smooth = b.input("Smooth", BOOL, True)
    f = _clamp_fillet(b, fillet, length, width, height)
    half = b.combine(b.math('SUBTRACT', b.math('MULTIPLY', width, 0.5), f),
                     b.math('SUBTRACT', b.math('MULTIPLY', length, 0.5), f),
                     b.math('SUBTRACT', b.math('MULTIPLY', height, 0.5), f))
    geo = _rounded(b, f, b.math('MULTIPLY', fillet_segs, 2.0), b.math('MULTIPLY', fillet_segs, 4.0),
                   lambda pos: b.vmath('MULTIPLY', b.vmath('SIGN', pos), half))
    return _lift(b, _smooth(b, geo, smooth), b.math('MULTIPLY', height, 0.5))


def _round_cylinder(b, radius, height, cap, sides, cap_segs, squash=None):
    """A cylinder with round caps of height `cap` (OilTank, Capsule, ChamferCyl): a sphere of the
    cap size, split at the equator and around the axis."""
    def offset(pos):
        x, y, z = b.separate(pos)
        xy = b.combine(x, y)
        radial = _scale(b, b.vmath('NORMALIZE', xy), b.math('SUBTRACT', radius, squash or cap))
        lift = b.math('MULTIPLY', b.math('SIGN', z), b.math('SUBTRACT', b.math('MULTIPLY', height, 0.5), cap))
        if squash is not None:
            # OilTank: the dome is flattened to the cap height.
            lift = b.math('ADD', lift, b.math('SUBTRACT', b.math('MULTIPLY', z, b.math('DIVIDE', cap, squash)), z))
        return b.vmath('ADD', radial, b.combine(z=lift))
    size = squash or cap
    geo = _rounded(b, size, b.math('MULTIPLY', cap_segs, 2.0), sides, offset)
    return _lift(b, geo, b.math('MULTIPLY', height, 0.5))


def build_chamfercyl(b):
    radius = b.input("Radius", DIST, 0.5, 0.0, subtype='DISTANCE')
    height = b.input("Height", DIST, 1.0, 0.0, subtype='DISTANCE')
    fillet = b.input("Fillet", DIST, 0.1, 0.0, subtype='DISTANCE')
    fillet_segs = b.input("Fillet Segs", INT, 3, 1, 50)
    sides = b.input("Sides", INT, 24, 3, 500)
    cap_segs = b.input("Cap Segs", INT, 1, 1, 100)
    smooth = b.input("Smooth", BOOL, True)
    quad = b.input("Quad Cap", BOOL, True)
    f = _clamp_fillet(b, fillet, b.math('MULTIPLY', radius, 2.0), height)
    geo = _round_cylinder(b, radius, height, f, sides, fillet_segs)
    step = b.math('DIVIDE', math.pi / 2, fillet_segs)
    side = qc.lathe(b, sides, b.math('ADD', b.math('MULTIPLY', fillet_segs, 2.0), 1.0), lambda k: qc.dome_profile(
        b, k, fillet_segs, 0.0, step, b.math('SUBTRACT', radius, f), f, f, height))
    side = _smooth(b, side, smooth)
    inner = b.math('SUBTRACT', radius, f)
    quads = qc.join_merge(b, side, qc.flat_cap(b, sides, cap_segs, inner, 0.0, False),
                          qc.flat_cap(b, sides, cap_segs, inner, height, True))
    return _quad_switch(b, quad, _smooth(b, geo, smooth), quads)


def _quad_switch(b, quad, geo, quads):
    return b.node('GeometryNodeSwitch', {"Switch": quad, "False": geo, "True": quads}, input_type='GEOMETRY').outputs[0]


def _quad_domes(b, sides, cap_segs, radius, cap, height):
    """Capsule and OilTank with quad poles: domes of `radius` and height `cap` on a straight side."""
    step = b.math('DIVIDE', math.pi / 2, cap_segs)
    pole = qc.pole_rings(b, sides, cap_segs)
    edge = b.math('MULTIPLY', pole, step)
    rings = b.math('SUBTRACT', cap_segs, pole)
    side = qc.lathe(b, sides, b.math('ADD', b.math('MULTIPLY', rings, 2.0), 1.0), lambda k: qc.dome_profile(
        b, k, rings, edge, step, 0.0, radius, cap, height))
    return qc.join_merge(b, side, qc.dome_cap(b, sides, 1, radius, cap, cap, edge, False),
                         qc.dome_cap(b, sides, 1, radius, cap, b.math('SUBTRACT', height, cap), edge, True))


def build_capsule(b):
    radius = b.input("Radius", DIST, 0.5, 0.0, subtype='DISTANCE')
    height = b.input("Height", DIST, 2.0, 0.0, subtype='DISTANCE')
    sides = b.input("Sides", INT, 24, 3, 500)
    cap_segs = b.input("Cap Segs", INT, 6, 1, 100)
    smooth = b.input("Smooth", BOOL, True)
    quad = b.input("Quad Poles", BOOL, True)
    # Max's Height is overall: the caps are inside it.
    r = _clamp_fillet(b, radius, b.math('MULTIPLY', radius, 2.0), height)
    geo = _quad_switch(b, quad, _round_cylinder(b, r, height, r, sides, cap_segs),
                       _quad_domes(b, sides, cap_segs, r, r, height))
    return _smooth(b, geo, smooth)


def build_oiltank(b):
    radius = b.input("Radius", DIST, 0.5, 0.0, subtype='DISTANCE')
    height = b.input("Height", DIST, 2.0, 0.0, subtype='DISTANCE')
    cap_height = b.input("Cap Height", DIST, 0.25, 0.0, subtype='DISTANCE')
    sides = b.input("Sides", INT, 24, 3, 500)
    cap_segs = b.input("Cap Segs", INT, 6, 1, 100)
    smooth = b.input("Smooth", BOOL, True)
    quad = b.input("Quad Poles", BOOL, True)
    cap = _clamp_fillet(b, cap_height, b.math('MULTIPLY', radius, 2.0), height)
    geo = _quad_switch(b, quad, _round_cylinder(b, radius, height, cap, sides, cap_segs, squash=radius),
                       _quad_domes(b, sides, cap_segs, radius, cap, height))
    return _smooth(b, geo, smooth)


def build_spindle(b):
    radius = b.input("Radius", DIST, 0.5, 0.0, subtype='DISTANCE')
    height = b.input("Height", DIST, 2.0, 0.0, subtype='DISTANCE')
    cap_height = b.input("Cap Height", DIST, 0.5, 0.0, subtype='DISTANCE')
    sides = b.input("Sides", INT, 24, 3, 500)
    h_segs = b.input("Height Segs", INT, 1, 1, 200)
    cap_segs = b.input("Cap Segs", INT, 1, 1, 100)
    smooth = b.input("Smooth", BOOL, True)
    quad = b.input("Quad Cap", BOOL, True)
    cap = _clamp_fillet(b, cap_height, height, height)
    body = b.math('MAXIMUM', b.math('SUBTRACT', height, b.math('MULTIPLY', cap, 2.0)), 0.0)
    cylinder = b.node('GeometryNodeMeshCylinder', {"Vertices": sides, "Side Segments": h_segs,
                                                   "Radius": radius, "Depth": body}, fill_type='NONE')
    cyl = _lift(b, cylinder.outputs["Mesh"], b.math('MULTIPLY', height, 0.5))
    # The cone node stands on z = 0 with its tip up: one cap on top, one turned over below.
    cone = b.node('GeometryNodeMeshCone', {"Vertices": sides, "Radius Top": 0.0, "Radius Bottom": radius,
                                           "Depth": cap}, fill_type='NONE').outputs["Mesh"]
    top = _lift(b, cone, b.math('ADD', cap, body))
    bottom = b.node('GeometryNodeTransform', {"Geometry": cone, "Rotation": (math.pi, 0.0, 0.0),
                                              "Translation": b.combine(z=cap)}).outputs[0]
    join = b.node('GeometryNodeJoinGeometry')
    for geo in (bottom, top, cyl):
        b.set(join.inputs[0], geo)
    geo = b.node('GeometryNodeMergeByDistance', {"Geometry": join.outputs[0], "Distance": 1e-5}).outputs[0]
    # Quad caps: the disc on each cone.
    side = qc.lathe(b, sides, h_segs, lambda k: (radius, b.math('ADD', cap, b.math(
        'MULTIPLY', body, b.math('DIVIDE', k, h_segs)))))
    quads = qc.join_merge(b, side, qc.cone_cap(b, sides, cap_segs, radius, cap, 0.0, False),
                          qc.cone_cap(b, sides, cap_segs, radius, cap, height, True))
    return _smooth(b, _quad_switch(b, quad, geo, quads), smooth)


def _quad_prism(b, curve, height, cap_segs):
    """The closed, convex `curve` as walls of quads up to `height` with quad caps."""
    count = b.node('GeometryNodeAttributeDomainSize', {"Geometry": curve}, component='CURVE').outputs["Point Count"]
    loop = b.node('GeometryNodeCurveToMesh', {"Curve": curve}).outputs[0]
    walls = b.node('GeometryNodeExtrudeMesh', {"Mesh": loop, "Offset": b.combine(z=height)}, mode='EDGES').outputs[0]
    # Walls face out, whichever way the curve runs.
    center = b.node('GeometryNodeAttributeStatistic', {"Geometry": curve, "Attribute": b.node(
        'GeometryNodeInputPosition').outputs[0]}, data_type='FLOAT_VECTOR', domain='POINT').outputs["Mean"]
    outward = b.vmath('DOT_PRODUCT', b.node('GeometryNodeInputNormal').outputs[0],
                      b.vmath('SUBTRACT', b.node('GeometryNodeInputPosition').outputs[0], center))
    walls = b.node('GeometryNodeFlipFaces', {"Mesh": walls, "Selection": b.node('FunctionNodeCompare', {
        "A": b.on_faces(outward), "B": 0.0}, data_type='FLOAT', operation='LESS_THAN').outputs[0]}).outputs[0]
    return qc.join_merge(b, walls, qc.polygon_cap(b, count, cap_segs, curve, 0.0, False),
                         qc.polygon_cap(b, count, cap_segs, curve, height, True))


def build_gengon(b):
    radius = b.input("Radius", DIST, 0.5, 0.0, subtype='DISTANCE')
    height = b.input("Height", DIST, 1.0, 0.0, subtype='DISTANCE')
    sides = b.input("Sides", INT, 5, 3, 100)
    fillet = b.input("Fillet", DIST, 0.0, 0.0, subtype='DISTANCE')
    fillet_segs = b.input("Fillet Segs", INT, 1, 1, 50)
    cap_segs = b.input("Cap Segs", INT, 1, 1, 100)
    quad = b.input("Quad Cap", BOOL, True)
    circle = b.node('GeometryNodeCurvePrimitiveCircle', {"Resolution": sides, "Radius": radius}).outputs[0]
    curve = b.node('GeometryNodeFilletCurve', {"Curve": circle, "Radius": fillet, "Limit Radius": True,
                                               "Mode": "Poly", "Count": fillet_segs}).outputs[0]
    return _quad_switch(b, quad, _extrude_fill(b, curve, height), _quad_prism(b, curve, height, cap_segs))


def build_ringwave(b):
    radius = b.input("Radius", DIST, 1.0, 0.0, subtype='DISTANCE')
    ring_width = b.input("Ring Width", DIST, 0.2, 0.0, subtype='DISTANCE')
    height = b.input("Height", DIST, 0.0, 0.0, subtype='DISTANCE')
    segments = b.input("Segments", INT, 200, 3, 5000)
    cycles = b.input("Major Cycles", INT, 6, 0, 500)
    amplitude = b.input("Major Amplitude", DIST, 0.05, subtype='DISTANCE')
    crawl = b.input("Major Crawl Time", FLOAT, 0.0, -10000.0, 10000.0)
    minor_cycles = b.input("Minor Cycles", INT, 0, 0, 500)
    minor_amplitude = b.input("Minor Amplitude", DIST, 0.0, subtype='DISTANCE')
    minor_crawl = b.input("Minor Crawl Time", FLOAT, 0.0, -10000.0, 10000.0)
    inner_cycles = b.input("Inner Cycles", INT, 0, 0, 500)
    inner_amplitude = b.input("Inner Amplitude", DIST, 0.0, subtype='DISTANCE')
    growth = b.input("Growth", INT, 0, 0, 2)
    b.tree.interface.items_tree["Growth"].description = "0 No Growth, 1 Grow and Stay, 2 Cyclic Growth"
    grow_start = b.input("Grow Start", FLOAT, 0.0, -100000.0, 100000.0)
    grow_end = b.input("Grow End", FLOAT, 60.0, -100000.0, 100000.0)
    b.tree.interface.items_tree["Major Crawl Time"].description = (
        "Frames for the waves to travel once around (0: still; negative: the other way)")
    frame = b.node('GeometryNodeInputSceneTime').outputs["Frame"]
    # The ring between Radius - Ring Width and Radius; its outer edge waves.
    inner = b.math('MAXIMUM', b.math('SUBTRACT', radius, ring_width), 0.0)
    middle = b.math('MULTIPLY', b.math('ADD', radius, inner), 0.5)
    path = b.node('GeometryNodeCurvePrimitiveCircle', {"Resolution": segments, "Radius": middle}).outputs[0]
    profile = b.node('GeometryNodeCurvePrimitiveQuadrilateral', {
        "Width": b.math('MAXIMUM', ring_width, 1e-5), "Height": b.math('MAXIMUM', height, 1e-5)}).outputs[0]
    mesh = b.node('GeometryNodeCurveToMesh', {"Curve": path, "Profile Curve": profile}).outputs[0]
    pos = b.node('GeometryNodeInputPosition').outputs[0]
    x, y, _z = b.separate(pos)
    radial = b.vmath('LENGTH', b.combine(x, y))
    angle = b.math('ARCTAN2', y, x)
    outer = b.node('FunctionNodeCompare', {"A": radial, "B": middle},
                   data_type='FLOAT', operation='GREATER_THAN').outputs[0]

    def phase(time):
        # One turn of the wave every `time` frames (0: none).
        moving = b.node('FunctionNodeCompare', {"A": b.math('ABSOLUTE', time), "B": 1e-6},
                        data_type='FLOAT', operation='GREATER_THAN').outputs[0]
        turn = b.math('DIVIDE', b.math('MULTIPLY', frame, 2.0 * math.pi), b.math('MAXIMUM', b.math('ABSOLUTE', time), 1e-6))
        turn = b.math('MULTIPLY', turn, b.math('SIGN', time))
        return b.node('GeometryNodeSwitch', {"Switch": moving, "False": 0.0, "True": turn}, input_type='FLOAT').outputs[0]

    def wave(count, size, time):
        return b.math('MULTIPLY', size, b.math('SINE', b.math('SUBTRACT', b.math('MULTIPLY', count, angle), phase(time))))
    outer_wave = b.math('ADD', wave(cycles, amplitude, crawl), wave(minor_cycles, minor_amplitude, minor_crawl))
    inner_wave = wave(inner_cycles, inner_amplitude, crawl)
    offset = b.node('GeometryNodeSwitch', {"Switch": outer, "False": inner_wave, "True": outer_wave},
                    input_type='FLOAT').outputs[0]
    geo = b.node('GeometryNodeSetPosition', {"Geometry": mesh,
                                             "Offset": _scale(b, b.vmath('NORMALIZE', b.combine(x, y)), offset)}).outputs[0]
    # Growth: the ring grows from nothing between Grow Start and Grow End (once, or over and over).
    span = b.math('MAXIMUM', b.math('SUBTRACT', grow_end, grow_start), 1e-6)
    elapsed = b.math('SUBTRACT', frame, grow_start)
    once = b.math('MINIMUM', b.math('MAXIMUM', b.math('DIVIDE', elapsed, span), 0.0), 1.0)
    cyclic = b.math('DIVIDE', b.math('FLOORED_MODULO', b.math('MAXIMUM', elapsed, 0.0), span), span)
    size = _index_switch(b, growth, [1.0, once, cyclic], 'FLOAT')
    geo = b.node('GeometryNodeTransform', {"Geometry": geo, "Scale": b.combine(size, size, 1.0)}).outputs[0]
    return _lift(b, geo, b.math('MULTIPLY', height, 0.5))


def build_hose(b):
    height = b.input("Height", DIST, 1.0, 0.0, subtype='DISTANCE')
    diameter = b.input("Diameter", DIST, 0.2, 0.0, subtype='DISTANCE')
    sides = b.input("Sides", INT, 16, 3, 200)
    segments = b.input("Segments", INT, 45, 1, 2000)
    starts = b.input("Flex Starts (%)", FLOAT, 10.0, 0.0, 100.0)
    stops = b.input("Flex Stops (%)", FLOAT, 90.0, 0.0, 100.0)
    cycles = b.input("Cycles", INT, 5, 0, 500)
    flex_diameter = b.input("Flex Diameter (%)", FLOAT, -20.0, -50.0, 500.0)
    smooth = b.input("Smooth", BOOL, True)
    # Max's End Point Method "Bound to Object Pivots": the hose runs from the bottom object's pivot
    # to the top one's, leaving each along that object's Z axis (Tension: how far it follows it).
    bound = b.input("Bound to Object Pivots", BOOL, False)
    top_object = b.input("Top Object", 'NodeSocketObject')
    bottom_object = b.input("Bottom Object", 'NodeSocketObject')
    top_tension = b.input("Top Tension", FLOAT, 100.0, 0.0, 1000.0)
    bottom_tension = b.input("Bottom Tension", FLOAT, 100.0, 0.0, 1000.0)
    line = b.node('GeometryNodeCurvePrimitiveLine', {"End": b.combine(z=height)}).outputs[0]
    ends = []
    for obj, tension, sign in ((bottom_object, bottom_tension, 1.0), (top_object, top_tension, 1.0)):
        info = b.node('GeometryNodeObjectInfo', {"Object": obj}, transform_space='RELATIVE')
        axis = b.node('FunctionNodeRotateVector', {"Vector": b.combine(z=sign), "Rotation": info.outputs["Rotation"]}).outputs[0]
        ends.append((info.outputs["Location"], axis, tension))
    (start, start_axis, start_t), (end, end_axis, end_t) = ends
    reach = b.math('MULTIPLY', b.vmath('DISTANCE', start, end), 1.0 / 3.0)

    def handle(point, axis, tension):
        return b.vmath('ADD', point, _scale(b, axis, b.math('MULTIPLY', reach, b.math('DIVIDE', tension, 100.0))))
    bezier = b.node('GeometryNodeCurvePrimitiveBezierSegment', {
        "Resolution": 64, "Start": start, "Start Handle": handle(start, start_axis, start_t),
        "End Handle": handle(end, end_axis, end_t), "End": end}, mode='POSITION').outputs[0]
    line = b.node('GeometryNodeSwitch', {"Switch": bound, "False": line, "True": bezier},
                  input_type='GEOMETRY').outputs[0]
    path = b.node('GeometryNodeResampleCurve', {"Curve": line, "Mode": "Count",
                                                "Count": b.math('ADD', segments, 1.0)}).outputs[0]
    profile = b.node('GeometryNodeCurvePrimitiveCircle', {
        "Resolution": sides, "Radius": b.math('MULTIPLY', diameter, 0.5)}).outputs[0]
    # In the flex section the diameter waves Cycles times.
    u = b.node('GeometryNodeSplineParameter').outputs["Factor"]
    a, c = b.math('DIVIDE', starts, 100.0), b.math('DIVIDE', stops, 100.0)
    local = b.math('DIVIDE', b.math('SUBTRACT', u, a), b.math('MAXIMUM', b.math('SUBTRACT', c, a), 1e-6))
    inside = b.node('FunctionNodeBooleanMath', {
        0: b.node('FunctionNodeCompare', {"A": local, "B": 0.0}, data_type='FLOAT', operation='GREATER_EQUAL').outputs[0],
        1: b.node('FunctionNodeCompare', {"A": local, "B": 1.0}, data_type='FLOAT', operation='LESS_EQUAL').outputs[0]},
        operation='AND').outputs[0]
    bump = b.math('MULTIPLY', 0.5, b.math('SUBTRACT', 1.0, b.math('COSINE', b.math(
        'MULTIPLY', b.math('MULTIPLY', local, cycles), 2.0 * math.pi))))
    flex = b.math('ADD', 1.0, b.math('MULTIPLY', bump, b.math('DIVIDE', flex_diameter, 100.0)))
    scale = b.node('GeometryNodeSwitch', {"Switch": inside, "False": 1.0, "True": flex},
                   input_type='FLOAT').outputs[0]
    mesh = b.node('GeometryNodeCurveToMesh', {"Curve": path, "Profile Curve": profile, "Scale": scale,
                                              "Fill Caps": True}).outputs[0]
    return _smooth(b, mesh, smooth)


def build_l_ext(b):
    side = b.input("Side Length", DIST, 1.0, 0.0, subtype='DISTANCE')
    front = b.input("Front Length", DIST, 1.0, 0.0, subtype='DISTANCE')
    side_w = b.input("Side Width", DIST, 0.2, 0.0, subtype='DISTANCE')
    front_w = b.input("Front Width", DIST, 0.2, 0.0, subtype='DISTANCE')
    height = b.input("Height", DIST, 1.0, 0.0, subtype='DISTANCE')
    sw = _clamp_fillet(b, side_w, b.math('MULTIPLY', front, 2.0), b.math('MULTIPLY', front, 2.0))
    fw = _clamp_fillet(b, front_w, b.math('MULTIPLY', side, 2.0), b.math('MULTIPLY', side, 2.0))
    quad = b.input("Quad Cap", BOOL, True)
    corners = [(0.0, 0.0), (front, 0.0), (front, fw), (sw, fw), (sw, side), (0.0, side)]
    return _quad_switch(b, quad, _prism(b, corners, height),
                        _quad_parts_prism(b, corners, [(0, 1, 2, 3), (0, 3, 4, 5)], height))


def build_c_ext(b):
    back = b.input("Back Length", DIST, 1.0, 0.0, subtype='DISTANCE')
    side = b.input("Side Length", DIST, 1.0, 0.0, subtype='DISTANCE')
    front = b.input("Front Length", DIST, 1.0, 0.0, subtype='DISTANCE')
    back_w = b.input("Back Width", DIST, 0.2, 0.0, subtype='DISTANCE')
    side_w = b.input("Side Width", DIST, 0.2, 0.0, subtype='DISTANCE')
    front_w = b.input("Front Width", DIST, 0.2, 0.0, subtype='DISTANCE')
    height = b.input("Height", DIST, 1.0, 0.0, subtype='DISTANCE')
    # The back runs along Y at x = 0; the side (bottom) and the front (top) run along X.
    corners = [(0.0, 0.0), (side, 0.0), (side, side_w), (back_w, side_w),
               (back_w, b.math('SUBTRACT', back, front_w)), (front, b.math('SUBTRACT', back, front_w)),
               (front, back), (0.0, back)]
    quad = b.input("Quad Cap", BOOL, True)
    return _quad_switch(b, quad, _prism(b, corners, height),
                        _quad_parts_prism(b, corners, [(0, 1, 2, 3), (0, 3, 4, 7), (7, 4, 5, 6)], height))


def build_prism(b):
    side1 = b.input("Side 1 Length", DIST, 1.0, 0.0, subtype='DISTANCE')
    side2 = b.input("Side 2 Length", DIST, 1.0, 0.0, subtype='DISTANCE')
    side3 = b.input("Side 3 Length", DIST, 1.0, 0.0, subtype='DISTANCE')
    height = b.input("Height", DIST, 1.0, 0.0, subtype='DISTANCE')
    # Side 1 along X; the apex from the law of cosines (Side 2 from its end, Side 3 back to 0).
    a = b.math('MAXIMUM', side1, 1e-6)
    x = b.math('DIVIDE', b.math('SUBTRACT', b.math('ADD', b.math('MULTIPLY', a, a), b.math('MULTIPLY', side3, side3)),
                                b.math('MULTIPLY', side2, side2)), b.math('MULTIPLY', a, 2.0))
    y = b.math('SQRT', b.math('MAXIMUM', b.math('SUBTRACT', b.math('MULTIPLY', side3, side3), b.math('MULTIPLY', x, x)),
                              0.0))
    quad = b.input("Quad Cap", BOOL, True)
    curve = _polygon(b, [(0.0, 0.0), (side1, 0.0), (x, y)])
    return _quad_switch(b, quad, _extrude_fill(b, curve, height), _quad_prism(b, curve, height, 1))


BUILDERS = {
    'GEOSPHERE': build_geosphere,
    'PYRAMID': build_pyramid,
    'TEAPOT': build_teapot,
    'HEDRA': build_hedra,
    'TORUS_KNOT': build_torus_knot,
    'CHAMFERBOX': build_chamferbox,
    'CHAMFERCYL': build_chamfercyl,
    'OILTANK': build_oiltank,
    'CAPSULE': build_capsule,
    'SPINDLE': build_spindle,
    'L_EXT': build_l_ext,
    'GENGON': build_gengon,
    'C_EXT': build_c_ext,
    'RINGWAVE': build_ringwave,
    'HOSE': build_hose,
    'PRISM': build_prism,
}
