# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Quad caps and quad poles for the primitives (Seb, 2026-10-28; Max makes triangle fans).

A cap is a unit disc: an inner grid of quads plus rings out to the rim. The rim has the primitive's
Sides vertices; the grid's border has as many (one more when Sides is odd, so one triangle fits it
in, as Edit Poly's Cap does). Each primitive maps the disc onto its cap: flat (Cylinder), a dome
(Sphere, Capsule, OilTank) or a cone (Spindle). The sides are a lathe: rings of Sides vertices at
the profile's radius and height.

UVs follow Blender's Cylinder node: the sides in the upper half, the caps as two circles below.
"""

import math

TAU = 2.0 * math.pi
UV_RADIUS = 0.225
TOP_UV = (0.25, 0.25)
BOTTOM_UV = (0.75, 0.25)


def _clamp(b, x, lo, hi):
    return b.math('MINIMUM', b.math('MAXIMUM', x, lo), hi)


def _lerp(b, a, c, f):
    return b.math('ADD', a, b.math('MULTIPLY', b.math('SUBTRACT', c, a), f))


def _switch(b, test, if_false, if_true, input_type='FLOAT'):
    return b.node('GeometryNodeSwitch', {"Switch": test, "False": if_false, "True": if_true},
                  input_type=input_type).outputs[0]


def _compare(b, a, c, operation):
    return b.node('FunctionNodeCompare', {"A": a, "B": c}, data_type='FLOAT', operation=operation).outputs[0]


def grid_size(b, sides):
    """(border, columns, rows): the quad grid whose border has `border` vertices, Sides rounded up
    to even."""
    border = b.math('ADD', sides, b.math('FLOORED_MODULO', sides, 2.0))
    columns = b.math('MAXIMUM', b.math('FLOOR', b.math('DIVIDE', border, 4.0)), 1.0)
    rows = b.math('MAXIMUM', b.math('SUBTRACT', b.math('DIVIDE', border, 2.0), columns), 1.0)
    return border, columns, rows


def grid_cells(b, sides):
    """Grid cells from the center to the border: what a quad pole replaces of a sphere's rings."""
    _border, columns, rows = grid_size(b, sides)
    return b.math('CEIL', b.math('MULTIPLY', b.math('MAXIMUM', columns, rows), 0.5))


def _square_to_disc(b, u, v):
    """The square [-1, 1]² onto the unit disc (elliptical grid mapping): the border lands on the
    circle."""
    def axis(a, other):
        return b.math('MULTIPLY', a, b.math('SQRT', b.math('SUBTRACT', 1.0, b.math('MULTIPLY', b.math(
            'MULTIPLY', other, other), 0.5))))
    return axis(u, v), axis(v, u)


def _index_ring(b, count):
    """(ring, i) of a Cylinder node's vertex: ring 0 is the top, i goes around from angle 0."""
    index = b.node('GeometryNodeInputIndex').outputs[0]
    ring = b.math('FLOOR', b.math('DIVIDE', index, count))
    return ring, b.math('SUBTRACT', index, b.math('MULTIPLY', ring, count))


def _border_point(b, i, border, columns, rows):
    """Border vertex `i` of the grid on the unit circle, walked counter-clockwise from the middle of
    the right side."""
    t = b.math('FLOORED_MODULO', b.math('ADD', i, b.math('FLOOR', b.math('MULTIPLY', rows, 0.5))), border)
    x = b.math('ADD', b.math('SUBTRACT', b.math('MULTIPLY', columns, 0.5), _clamp(b, b.math('SUBTRACT', t, rows), 0.0, columns)),
               _clamp(b, b.math('SUBTRACT', t, b.math('ADD', b.math('MULTIPLY', rows, 2.0), columns)), 0.0, columns))
    y = b.math('SUBTRACT', b.math('ADD', b.math('MULTIPLY', rows, -0.5), _clamp(b, t, 0.0, rows)),
               _clamp(b, b.math('SUBTRACT', t, b.math('ADD', rows, columns)), 0.0, rows))
    return _square_to_disc(b, b.math('DIVIDE', x, b.math('MULTIPLY', columns, 0.5)),
                           b.math('DIVIDE', y, b.math('MULTIPLY', rows, 0.5)))


def _rotate(b, x, y, angle):
    c, s = b.math('COSINE', angle), b.math('SINE', angle)
    return (b.math('SUBTRACT', b.math('MULTIPLY', x, c), b.math('MULTIPLY', y, s)),
            b.math('ADD', b.math('MULTIPLY', x, s), b.math('MULTIPLY', y, c)))


def disc(b, sides, rings, uv_center, mirror=False):
    """The unit quad disc in the XY plane, facing up, with UVs in the circle at `uv_center`."""
    border, columns, rows = grid_size(b, sides)
    cells = b.math('MULTIPLY', b.math('MAXIMUM', columns, rows), 0.5)
    inner = b.math('DIVIDE', cells, b.math('ADD', cells, rings))

    # Turn the grid so its border vertices sit, on average, at the angles of the rim vertices they
    # connect to (an odd Sides drifts by one vertex over the round).
    first = _border_point(b, 0.0, border, columns, rows)
    drift = b.math('MULTIPLY', math.pi, b.math('MULTIPLY', b.math('SUBTRACT', border, 1.0), b.math(
        'SUBTRACT', b.math('DIVIDE', 1.0, sides), b.math('DIVIDE', 1.0, border))))
    turn = b.math('SUBTRACT', drift, b.math('ARCTAN2', first[1], first[0]))
    grid = b.node('GeometryNodeMeshGrid', {"Size X": 2.0, "Size Y": 2.0, "Vertices X": b.math('ADD', columns, 1.0),
                                           "Vertices Y": b.math('ADD', rows, 1.0)}).outputs["Mesh"]
    gx, gy, _gz = b.separate(b.node('GeometryNodeInputPosition').outputs[0])
    dx, dy = _square_to_disc(b, gx, gy)
    rx, ry = _rotate(b, dx, dy, turn)
    grid = b.node('GeometryNodeSetPosition', {
        "Geometry": grid, "Position": b.combine(b.math('MULTIPLY', rx, inner), b.math('MULTIPLY', ry, inner))}).outputs[0]

    # The rings: vertex i goes from the grid border (walked counter-clockwise from the right side)
    # to the rim at angle i / Sides, the last one of an odd Sides doubling the first.
    strip = b.node('GeometryNodeMeshCylinder', {"Vertices": border, "Side Segments": rings},
                   fill_type='NONE').outputs["Mesh"]
    ring, i = _index_ring(b, border)
    f = b.math('DIVIDE', ring, rings)
    ix, iy = _border_point(b, i, border, columns, rows)
    angle_in = b.math('ADD', b.math('ARCTAN2', iy, ix), turn)
    angle_out = b.math('MULTIPLY', b.math('FLOORED_MODULO', i, sides), b.math('DIVIDE', TAU, sides))
    delta = b.math('SUBTRACT', angle_out, angle_in)
    delta = b.math('ARCTAN2', b.math('SINE', delta), b.math('COSINE', delta))
    angle = b.math('ADD', angle_in, b.math('MULTIPLY', delta, f))
    radius = _lerp(b, inner, 1.0, f)
    strip = b.node('GeometryNodeSetPosition', {"Geometry": strip, "Position": b.combine(
        b.math('MULTIPLY', radius, b.math('COSINE', angle)), b.math('MULTIPLY', radius, b.math('SINE', angle)))}).outputs[0]

    join = b.node('GeometryNodeJoinGeometry')
    for geo in (strip, grid):
        b.set(join.inputs[0], geo)
    geo = b.node('GeometryNodeMergeByDistance', {"Geometry": join.outputs[0], "Distance": 1e-5}).outputs[0]
    _nx, _ny, nz = b.separate(b.node('GeometryNodeInputNormal').outputs[0])
    geo = b.node('GeometryNodeFlipFaces', {"Mesh": geo, "Selection": _compare(b, nz, 0.0, 'LESS_THAN')}).outputs[0]
    px, py, _pz = b.separate(b.node('GeometryNodeInputPosition').outputs[0])
    u = b.math('MULTIPLY', px, -UV_RADIUS if mirror else UV_RADIUS)
    return b.store_uv(geo, b.combine(b.math('ADD', u, uv_center[0]),
                                     b.math('ADD', b.math('MULTIPLY', py, UV_RADIUS), uv_center[1])))


def _pole_gap(b, sides, rings):
    """How far the disc's vertex nearest the center is from it: 0 unless the grid has an odd number
    of columns or rows. Domes and cones put those vertices at the pole's height, so the height stays
    exact (a small flat top)."""
    _border, columns, rows = grid_size(b, sides)
    cells = b.math('MULTIPLY', b.math('MAXIMUM', columns, rows), 0.5)
    inner = b.math('DIVIDE', cells, b.math('ADD', cells, rings))
    u = b.math('DIVIDE', b.math('FLOORED_MODULO', columns, 2.0), columns)
    v = b.math('DIVIDE', b.math('FLOORED_MODULO', rows, 2.0), rows)
    du, dv = _square_to_disc(b, u, v)
    return b.math('MULTIPLY', inner, b.math('SQRT', b.math('ADD', b.math('MULTIPLY', du, du), b.math('MULTIPLY', dv, dv))))


def _from_pole(b, s, gap):
    """The disc radius `s` with the pole gap closed: 0 at the vertices nearest the center."""
    return b.math('DIVIDE', b.math('MAXIMUM', b.math('SUBTRACT', s, gap), 0.0),
                  b.math('MAXIMUM', b.math('SUBTRACT', 1.0, gap), 1e-6))


def _map(b, geo, position, flip):
    geo = b.node('GeometryNodeSetPosition', {"Geometry": geo, "Position": position}).outputs[0]
    return b.node('GeometryNodeFlipFaces', {"Mesh": geo}).outputs[0] if flip else geo


def _disc_xy(b):
    x, y, _z = b.separate(b.node('GeometryNodeInputPosition').outputs[0])
    return x, y, b.math('SQRT', b.math('ADD', b.math('MULTIPLY', x, x), b.math('MULTIPLY', y, y)))


def flat_cap(b, sides, rings, radius, z, top):
    """A flat cap of `radius` at height `z`, facing up (`top`) or down."""
    geo = disc(b, sides, rings, TOP_UV if top else BOTTOM_UV, mirror=not top)
    x, y, _s = _disc_xy(b)
    return _map(b, geo, b.combine(b.math('MULTIPLY', x, radius), b.math('MULTIPLY', y, radius), z), not top)


def dome_cap(b, sides, rings, radius, height, center, edge, top):
    """A quad pole: the disc on a dome of `radius` and `height` around `center` (an ellipsoid when
    they differ), out to `edge` radians from the pole."""
    geo = disc(b, sides, rings, TOP_UV if top else BOTTOM_UV, mirror=not top)
    x, y, s = _disc_xy(b)
    polar = b.math('MULTIPLY', s, edge)
    out = b.math('DIVIDE', b.math('MULTIPLY', radius, b.math('SINE', polar)), b.math('MAXIMUM', s, 1e-9))
    z = b.math('MULTIPLY', height, b.math('COSINE', b.math('MULTIPLY', _from_pole(b, s, _pole_gap(b, sides, rings)), edge)))
    z = b.math('ADD', center, z if top else b.math('MULTIPLY', z, -1.0))
    return _map(b, geo, b.combine(b.math('MULTIPLY', x, out), b.math('MULTIPLY', y, out), z), not top)


def cone_cap(b, sides, rings, radius, height, apex, top):
    """The disc on a cone of `radius` and `height` with its apex at `apex` (pointing up when
    `top`)."""
    geo = disc(b, sides, rings, TOP_UV if top else BOTTOM_UV, mirror=not top)
    x, y, s = _disc_xy(b)
    drop = b.math('MULTIPLY', height, _from_pole(b, s, _pole_gap(b, sides, rings)))
    z = b.math('SUBTRACT', apex, drop) if top else b.math('ADD', apex, drop)
    return _map(b, geo, b.combine(b.math('MULTIPLY', x, radius), b.math('MULTIPLY', y, radius), z), not top)


def polygon_cap(b, sides, rings, curve, z, top):
    """A flat cap filling the closed, convex `curve` (its points are the rim) at height `z`."""
    geo = disc(b, sides, rings, TOP_UV if top else BOTTOM_UV, mirror=not top)
    x, y, s = _disc_xy(b)
    position = b.node('GeometryNodeInputPosition').outputs[0]
    center = b.node('GeometryNodeAttributeStatistic', {"Geometry": curve, "Attribute": position},
                    data_type='FLOAT_VECTOR', domain='POINT').outputs["Mean"]
    turn = b.math('FLOORED_MODULO', b.math('DIVIDE', b.math('ARCTAN2', y, x), TAU), 1.0)
    along = b.math('MULTIPLY', turn, sides)
    first = b.math('FLOOR', b.math('ADD', along, 1e-4))
    weight = _clamp(b, b.math('SUBTRACT', along, first), 0.0, 1.0)

    def corner(index):
        return b.node('GeometryNodeSampleIndex', {"Geometry": curve, "Value": position,
                                                  "Index": b.math('FLOORED_MODULO', index, sides)},
                      data_type='FLOAT_VECTOR', domain='POINT').outputs[0]
    a = corner(first)
    rim = b.vmath('ADD', a, b.node('ShaderNodeVectorMath', {
        "Vector": b.vmath('SUBTRACT', corner(b.math('ADD', first, 1.0)), a), "Scale": weight},
        operation='SCALE').outputs["Vector"])
    offset = b.node('ShaderNodeVectorMath', {"Vector": b.vmath('SUBTRACT', rim, center), "Scale": s},
                    operation='SCALE').outputs["Vector"]
    px, py, _pz = b.separate(b.vmath('ADD', center, offset))
    geo = _map(b, geo, b.combine(px, py, z), False)
    # The curve may run either way round: face up, then down for the bottom.
    _nx, _ny, nz = b.separate(b.node('GeometryNodeInputNormal').outputs[0])
    geo = b.node('GeometryNodeFlipFaces', {"Mesh": geo, "Selection": _compare(
        b, nz, 0.0, 'LESS_THAN' if top else 'GREATER_THAN')}).outputs[0]
    return geo


def lathe(b, sides, segments, profile):
    """The sides: `segments` + 1 rings of `sides` vertices; `profile(k)` gives ring k's (radius,
    height), k = 0 at the bottom."""
    cylinder = b.node('GeometryNodeMeshCylinder', {"Vertices": sides, "Side Segments": segments}, fill_type='NONE')
    u, v, _w = b.separate(cylinder.outputs["UV Map"])
    geo = b.store_uv(cylinder.outputs["Mesh"], b.combine(u, b.math('ADD', b.math('MULTIPLY', v, 0.5), 0.5)))
    ring, i = _index_ring(b, sides)
    radius, z = profile(b.math('SUBTRACT', segments, ring))
    angle = b.math('MULTIPLY', i, b.math('DIVIDE', TAU, sides))
    return b.node('GeometryNodeSetPosition', {"Geometry": geo, "Position": b.combine(
        b.math('MULTIPLY', radius, b.math('COSINE', angle)), b.math('MULTIPLY', radius, b.math('SINE', angle)), z)}).outputs[0]


def dome_profile(b, k, rings, edge, step, offset, radius, height, total):
    """Two domes joined by a straight side: ring k (from the bottom) of `rings` per dome, starting
    `edge` radians from the pole in steps of `step`; the dome's radius is `offset` + `radius` · sin,
    its height `height`, `total` the overall height."""
    bottom = b.math('ADD', edge, b.math('MULTIPLY', k, step))
    top = b.math('SUBTRACT', math.pi / 2, b.math('MULTIPLY', b.math('SUBTRACT', k, b.math('ADD', rings, 1.0)), step))
    is_top = _compare(b, k, b.math('ADD', rings, 0.5), 'GREATER_THAN')
    polar = _switch(b, is_top, bottom, top)
    r = b.math('ADD', offset, b.math('MULTIPLY', radius, b.math('SINE', polar)))
    lift = b.math('MULTIPLY', height, b.math('COSINE', polar))
    z = _switch(b, is_top, b.math('SUBTRACT', height, lift),
                b.math('ADD', b.math('SUBTRACT', total, height), lift))
    return r, z


def join_merge(b, *geos):
    join = b.node('GeometryNodeJoinGeometry')
    for geo in geos:
        b.set(join.inputs[0], geo)
    return b.node('GeometryNodeMergeByDistance', {"Geometry": join.outputs[0], "Distance": 1e-5}).outputs[0]


def pole_rings(b, sides, available):
    """Rings a quad pole replaces: the grid's cells plus one, at most `available`."""
    return b.math('MAXIMUM', b.math('MINIMUM', b.math('ADD', grid_cells(b, sides), 1.0), available), 1.0)
