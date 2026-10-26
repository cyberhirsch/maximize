# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Editable (parametric) shapes, as Max's Shapes panel: Rectangle with corner radius, Circle,
Ellipse, Arc, NGon, Star, Helix and Donut.

A shape is a curve object made of real Bezier splines with the vertices and handles Max gives the
same shape (measured in 3ds Max 2026, see moritz/docs/splines_max_design.md in the Moritz repo).
Its parameters live on the curve data and rebuild the splines when they change, so the shape
stays editable until it is converted. Pressing 1 (Convert to Editable Spline) keeps the splines
as they are. The Rendering settings (Enable In Renderer / Viewport, cross section) are Max's,
see `spline_render.py`. The splines are plain Blender data: stock Blender shows the shape, it
only can't edit the parameters.
"""

import math

import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, PointerProperty
from bpy.types import PropertyGroup
from mathutils import Matrix, Vector

SHAPE_KINDS = (
    ('RECTANGLE', "Rectangle", "", 'MESH_PLANE', 20),
    ('CIRCLE', "Circle", "", 'MESH_CIRCLE', 21),
    ('ELLIPSE', "Ellipse", "", 'MESH_CIRCLE', 22),
    ('ARC', "Arc", "", 'SPHERECURVE', 23),
    ('NGON', "NGon", "", 'SEQ_CHROMA_SCOPE', 24),
    ('STAR', "Star", "", 'SOLO_OFF', 25),
    ('HELIX', "Helix", "", 'FORCE_VORTEX', 26),
    ('DONUT', "Donut", "", 'MESH_TORUS', 27),
    ('EGG', "Egg", "", 'MESH_UVSPHERE', 28),
)
SHAPES = {kind[0] for kind in SHAPE_KINDS}

SHAPE_STEPS = {
    'RECTANGLE': ('RECT',),
    'ELLIPSE': ('RECT',),
    'CIRCLE': ('RADIUS',),
    'ARC': ('RADIUS',),
    'NGON': ('RADIUS',),
    'STAR': ('RADIUS', 'RADIUS2'),
    'HELIX': ('RADIUS', 'HEIGHT', 'RADIUS2'),
    'DONUT': ('RADIUS', 'RADIUS2'),
    'EGG': ('RADIUS',),
}

# Max's handle length for a quarter circle, per unit radius. Fillets use it too, per unit of
# tangent distance.
CIRCLE_HANDLE = 0.5517861843
# Helix vertices per turn.
HELIX_KNOTS_PER_TURN = 40


# ------------------------------------------------------------------------------
# Spline math. A knot is (position, left handle, right handle, Blender handle type); a spline is
# (cyclic, [knots]).


def arc_handle(angle):
    """Handle length, per unit radius, of one Bezier segment spanning `angle` radians of a circle.
    Max picks the length at which the mean distance from the centre of the samples at t = 0, 0.1,
    ..., 0.9 equals the radius. This matches Max's arcs to 1e-6 (4/3 tan(angle/4), the usual
    choice, differs by up to 0.3 %)."""
    angle = round(angle, 9)
    cached = _ARC_HANDLES.get(angle)
    if cached is not None:
        return cached
    s, c = math.sin(angle), math.cos(angle)
    lo, hi = 0.0, 1.5
    for _ in range(60):
        h = (lo + hi) / 2.0
        p0, p1, p2, p3 = (1.0, 0.0), (1.0, h), (c + s * h, s - c * h), (c, s)
        mean = 0.0
        for i in range(10):
            t = i / 10.0
            u = 1.0 - t
            a, b, cc, d = u * u * u, 3 * u * u * t, 3 * u * t * t, t * t * t
            mean += math.hypot(a * p0[0] + b * p1[0] + cc * p2[0] + d * p3[0],
                               a * p0[1] + b * p1[1] + cc * p2[1] + d * p3[1])
        if mean / 10.0 > 1.0:
            hi = h
        else:
            lo = h
    _ARC_HANDLES[angle] = h
    return h


_ARC_HANDLES = {}


def _ellipse_arc(rx, ry, start, sweep, segments):
    """Smooth knots along an ellipse from `start` over `sweep` radians, open ends included."""
    k = arc_handle(abs(sweep) / segments) * (1.0 if sweep >= 0 else -1.0)
    knots = []
    for i in range(segments + 1):
        a = start + sweep * i / segments
        co = Vector((rx * math.cos(a), ry * math.sin(a), 0.0))
        tangent = Vector((-rx * math.sin(a), ry * math.cos(a), 0.0)) * k
        knots.append((co, co - tangent, co + tangent, 'ALIGNED'))
    return knots


def _ellipse(rx, ry):
    return (True, _ellipse_arc(rx, ry, 0.0, 2.0 * math.pi, 4)[:4])


def _direction(a, b):
    d = b - a
    return d.normalized() if d.length > 1e-12 else Vector()


def _polygon(corners, fillets, corner_handles, fillet_type):
    """A closed polygon; corner i is rounded with tangent distance fillets[i]. Unrounded corners
    get handles at 1/3 of their sides (`corner_handles` 'THIRD', Max's Bezier Corner) or none
    ('ZERO')."""
    n = len(corners)
    points = []   # (position, towards previous, towards next, rounded)
    for i, c in enumerate(corners):
        prev, nxt = corners[i - 1], corners[(i + 1) % n]
        d = min(fillets[i], (c - prev).length / 2.0, (nxt - c).length / 2.0)
        if d > 1e-9:
            to_prev, to_next = _direction(c, prev), _direction(c, nxt)
            p_in, p_out = c + to_prev * d, c + to_next * d
            h = CIRCLE_HANDLE * d
            points.append((p_in, p_in + to_prev * h, p_in - to_prev * h, True))
            points.append((p_out, p_out - to_next * h, p_out + to_next * h, True))
        else:
            points.append((c, None, None, False))
    knots = []
    m = len(points)
    for i, (co, left, right, rounded) in enumerate(points):
        if rounded:
            knots.append((co, left, right, fillet_type))
        elif corner_handles == 'THIRD':
            prev, nxt = points[i - 1][0], points[(i + 1) % m][0]
            knots.append((co, co + (prev - co) / 3.0, co + (nxt - co) / 3.0, 'FREE'))
        else:
            knots.append((co, co.copy(), co.copy(), 'FREE'))
    return (True, knots)


def _star(r1, r2, n, distortion, fillet1, fillet2):
    """Max's star: Radius 2 points at 0, 360/n, ..., turned by Distortion; Radius 1 points
    between them. A fillet's vertices lie at the fillet radius from the point, along the sides.
    With Distortion, Max aims the fillets of a Radius 2 point at the previous Radius 1 point
    unturned and at the next one turned twice, and those of a Radius 1 point at the unturned
    Radius 2 points (so filleted sides of a distorted star curve)."""
    def at(r, a):
        return Vector((r * math.cos(a), r * math.sin(a), 0.0))

    step = math.pi / n
    knots = []
    for i in range(2 * n):
        a = step * i
        if i % 2 == 0:
            corner, f = at(r2, a + distortion), fillet2
            prev, nxt = at(r1, a - step), at(r1, a + step + 2.0 * distortion)
        else:
            corner, f = at(r1, a), fillet1
            prev, nxt = at(r2, a - step), at(r2, a + step)
        if f <= 1e-9:
            knots.append((corner, corner.copy(), corner.copy(), 'FREE'))
            continue
        to_prev, to_next = _direction(corner, prev), _direction(corner, nxt)
        p_in, p_out = corner + to_prev * f, corner + to_next * f
        h = CIRCLE_HANDLE * f
        knots.append((p_in, p_in + to_prev * h, p_in - to_prev * h, 'ALIGNED'))
        knots.append((p_out, p_out - to_next * h, p_out + to_next * h, 'ALIGNED'))
    return (True, knots)


def _arc(center, radius, start, sweep, segments):
    return [(co + center, left + center, right + center, t)
            for co, left, right, t in _ellipse_arc(radius, radius, start, sweep, segments)]


def _egg_spline(half_width, offset, angle):
    """Max's egg: circular arcs, measured in Max 2026 (in units of half the width w): the bottom a
    half circle of radius w around (0, -0.3w), the sides arcs of radius 3w around (-+2w, -0.3w)
    up to 36.87 degrees, the top an arc of radius w/2 around (0, 1.2w). The outline is the same arcs
    `offset` further out. Max's knots: bottom 2, each side 3, top 3; `angle` turns the egg."""
    s = half_width
    rise = math.atan2(1.8, 2.4)
    arcs = (
        (Vector((0, -0.3 * s, 0)), s + offset, math.pi, math.pi, 2),
        (Vector((-2 * s, -0.3 * s, 0)), 3 * s + offset, 0.0, rise, 3),
        (Vector((0, 1.2 * s, 0)), 0.5 * s + offset, rise, math.pi - 2 * rise, 3),
        (Vector((2 * s, -0.3 * s, 0)), 3 * s + offset, math.pi - rise, rise, 3),
    )
    knots = []
    for center, radius, start, sweep, segments in arcs:
        arc = _arc(center, radius, start, sweep, segments)
        if knots:
            # The joint takes its left handle from the arc before it.
            co, left, _right, t = knots.pop()
            arc[0] = (arc[0][0], left, arc[0][2], t)
        knots += arc
    # The last arc ends on the first knot: its left handle goes there.
    co, left, _right, _t = knots.pop()
    first = knots[0]
    knots[0] = (first[0], left, first[2], first[3])
    if angle:
        rot = Matrix.Rotation(angle, 3, 'Z')
        knots = [(rot @ co, rot @ left, rot @ right, t) for co, left, right, t in knots]
    return (True, knots)


def _helix(r1, r2, height, turns, bias, clockwise):
    """Max's helix: 40 corner vertices per turn, the radius linear along it; Bias packs the turns
    towards the top (> 0) or the bottom (< 0)."""
    segments = max(1, math.ceil(turns * HELIX_KNOTS_PER_TURN - 1e-6))
    power = 1.0 + 9.0 * abs(bias)
    sign = -1.0 if clockwise else 1.0
    positions = []
    for i in range(segments + 1):
        u = i / segments
        if bias > 0.0:
            z = 1.0 - (1.0 - u) ** power
        elif bias < 0.0:
            z = u ** power
        else:
            z = u
        a = sign * turns * 2.0 * math.pi * u
        r = r1 + (r2 - r1) * u
        positions.append(Vector((r * math.cos(a), r * math.sin(a), height * z)))
    knots = []
    for i, co in enumerate(positions):
        prev = positions[i - 1] if i > 0 else co
        nxt = positions[i + 1] if i < segments else co
        # Blender points the outer handle of an end vertex away from the spline; Max leaves it on
        # the vertex.
        knots.append((co, co + (prev - co) / 3.0, co + (nxt - co) / 3.0,
                      'FREE' if i in (0, segments) else 'VECTOR'))
    return (False, knots)


def build_splines(p):
    """The splines of a shape from its parameters (a MaximizeShape)."""
    kind = p.kind
    if kind == 'CIRCLE':
        return [_ellipse(p.radius, p.radius)]
    if kind == 'ELLIPSE':
        return [_ellipse(p.width / 2.0, p.length / 2.0)]
    if kind == 'DONUT':
        return [_ellipse(p.radius1, p.radius1), _ellipse(p.radius2, p.radius2)]
    if kind == 'RECTANGLE':
        w, l = p.width / 2.0, p.length / 2.0
        corners = [Vector((w, l, 0)), Vector((-w, l, 0)), Vector((-w, -l, 0)), Vector((w, -l, 0))]
        return [_polygon(corners, [p.corner_radius] * 4, 'THIRD', 'FREE')]
    if kind == 'NGON':
        n = p.sides
        radius = p.radius / math.cos(math.pi / n) if p.scribe == 'INSCRIBED' else p.radius
        if p.circular:
            return [(True, _ellipse_arc(radius, radius, 0.0, 2.0 * math.pi, n)[:n])]
        corners = [Vector((radius * math.cos(2 * math.pi * i / n), radius * math.sin(2 * math.pi * i / n), 0))
                   for i in range(n)]
        d = p.corner_radius * math.tan(math.pi / n)
        return [_polygon(corners, [d] * n, 'THIRD', 'ALIGNED')]
    if kind == 'STAR':
        return [_star(p.radius1, p.radius2, p.points, p.distortion, p.fillet1, p.fillet2)]
    if kind == 'ARC':
        start = p.angle_from
        sweep = (p.angle_to - p.angle_from) % (2.0 * math.pi) or 2.0 * math.pi
        knots = _ellipse_arc(p.radius, p.radius, start, sweep, 3)
        if p.reverse:
            knots = [(co, right, left, t) for co, left, right, t in reversed(knots)]
        first, last = knots[0], knots[-1]
        knots[0] = (first[0], first[0].copy(), first[2], 'FREE')
        knots[-1] = (last[0], last[1], last[0].copy(), 'FREE')
        if p.pie:
            centre = Vector()
            knots.append((centre, centre.copy(), centre.copy(), 'FREE'))
        return [(p.pie, knots)]
    if kind == 'EGG':
        splines = [_egg_spline(p.width / 2.0, 0.0, p.egg_angle)]
        if p.outline:
            splines.append(_egg_spline(p.width / 2.0, p.egg_thickness, p.egg_angle))
        return splines
    if kind == 'HELIX':
        return [_helix(p.radius1, p.radius2, p.height, p.turns, p.bias, p.direction == 'CW')]
    return []


def rebuild(curve):
    """Write the shape's splines and render settings into its curve data."""
    from . import spline_render
    p = curve.maximize_shape
    spline_render.sync(curve)
    if p.kind == 'NONE':
        return
    curve.splines.clear()
    curve.dimensions = '3D'
    # Max's Steps are the points between two vertices; Blender's resolution counts the segments.
    curve.resolution_u = p.steps + 1
    curve.render_resolution_u = 0
    if hasattr(curve, "use_optimize"):
        # Moritz core: straight segments get no Steps points. Stock Blender lacks it.
        curve.use_optimize = p.optimize
    for cyclic, knots in build_splines(p):
        spline = curve.splines.new('BEZIER')
        spline.bezier_points.add(len(knots) - 1)
        for bp, (co, left, right, handle_type) in zip(spline.bezier_points, knots):
            bp.co = co
            bp.handle_left_type = bp.handle_right_type = 'FREE'
            bp.handle_left = left
            bp.handle_right = right
            if handle_type != 'FREE':
                bp.handle_left_type = bp.handle_right_type = handle_type
        spline.use_cyclic_u = cyclic
        spline.use_smooth = True
    if p.adaptive:
        from .spline_more import apply_adaptive
        apply_adaptive(curve)
    curve.update_tag()


def _update(self, _context):
    rebuild(self.id_data)


def _length(name, default, description=""):
    return FloatProperty(name=name, default=default, min=0.0, unit='LENGTH', update=_update,
                         description=description)


def _angle(name, default):
    return FloatProperty(name=name, default=math.radians(default), subtype='ANGLE', unit='ROTATION', update=_update)


def _update_adaptive(self, context):
    curve = self.id_data
    _update(self, context)
    if self.adaptive:
        from .spline_more import apply_adaptive
        apply_adaptive(curve)
    else:
        for spline in curve.splines:
            spline.resolution_u = curve.resolution_u


def _lock_aspect(self):
    if self.rect_aspect_lock and self.rect_width > 0:
        self.rect_locked_aspect = self.rect_length / self.rect_width


_rect_guard = []


def _update_rect(self, context, changed):
    """Lock Aspect: Length and Width move together."""
    if self.rect_aspect_lock and self.rect_locked_aspect > 0 and not _rect_guard:
        _rect_guard.append(True)
        try:
            if changed == "rect_length":
                self.rect_width = self.rect_length / self.rect_locked_aspect
            else:
                self.rect_length = self.rect_width * self.rect_locked_aspect
        finally:
            _rect_guard.clear()
    _update(self, context)


class MaximizeShape(PropertyGroup):
    kind: EnumProperty(name="Shape", items=(('NONE', "None", "Not a parametric shape"),) +
                       tuple(k[:3] for k in SHAPE_KINDS), default='NONE')
    length: _length("Length", 1.0)
    width: _length("Width", 1.0)
    corner_radius: _length("Corner Radius", 0.0)
    radius: _length("Radius", 0.5)
    radius1: _length("Radius 1", 0.5)
    radius2: _length("Radius 2", 0.25)
    angle_from: _angle("From", 45.0)
    angle_to: _angle("To", 135.0)
    pie: BoolProperty(name="Pie Slice", update=_update)
    reverse: BoolProperty(name="Reverse", update=_update)
    scribe: EnumProperty(name="Radius", default='INSCRIBED', update=_update, items=(
        ('INSCRIBED', "Inscribed", "The radius circle touches the sides"),
        ('CIRCUMSCRIBED', "Circumscribed", "The radius circle runs through the corners")))
    sides: IntProperty(name="Sides", default=6, min=3, max=100, update=_update)
    circular: BoolProperty(name="Circular", update=_update)
    points: IntProperty(name="Points", default=6, min=3, max=100, update=_update)
    distortion: _angle("Distortion", 0.0)
    fillet1: _length("Fillet Radius 1", 0.0)
    fillet2: _length("Fillet Radius 2", 0.0)
    height: FloatProperty(name="Height", default=1.0, unit='LENGTH', update=_update)
    turns: FloatProperty(name="Turns", default=3.0, min=0.0, soft_max=100.0, update=_update)
    bias: FloatProperty(name="Bias", default=0.0, min=-1.0, max=1.0, update=_update)
    direction: EnumProperty(name="Direction", default='CW', update=_update, items=(
        ('CW', "CW", "Clockwise seen from above"), ('CCW', "CCW", "Counter-clockwise seen from above")))
    steps: IntProperty(name="Steps", default=6, min=0, max=100, update=_update,
                       description="Points drawn between two vertices")
    optimize: BoolProperty(name="Optimize", default=True, update=_update,
                           description="Straight segments get no Steps points")
    adaptive: BoolProperty(name="Adaptive", update=lambda self, ctx: _update_adaptive(self, ctx),
                           description="Steps follow the curvature, about 6 degrees per step (Steps and "
                                       "Optimize are ignored); one count per spline")
    show_vertex_numbers: BoolProperty(name="Show Vertex Numbers", description="Number the vertices of each spline")
    show_selected_segments: BoolProperty(name="Show Selected Segs", default=True,
                                         description="Draw selected segments in red, as Max does")
    vertex_numbers_selected: BoolProperty(name="Selected Only", description="Number only the selected vertices")
    # Egg: Max ties the length to the width (length = 1.5 width).
    egg_length: FloatProperty(name="Length", min=0.0, unit='LENGTH', update=_update,
                              get=lambda self: self.width * 1.5,
                              set=lambda self, value: setattr(self, "width", value / 1.5))
    egg_thickness: _length("Thickness", 0.05, "Distance of the egg's outline")
    egg_angle: _angle("Angle", 0.0)
    outline: BoolProperty(name="Outline", default=True, update=_update,
                          description="A second egg around the first")
    # Rendering (spline_render.py); kept after Convert to Editable Spline.
    render_renderer: BoolProperty(name="Enable In Renderer", update=_update,
                                  description="Render the spline as a mesh with the cross section below")
    render_viewport: BoolProperty(name="Enable In Viewport", update=_update,
                                  description="Show the spline as that mesh in the viewport")
    render_mode: EnumProperty(name="Cross Section", default='RADIAL', update=_update, items=(
        ('RADIAL', "Radial", "Round cross section"), ('RECTANGULAR', "Rectangular", "Rectangular cross section")))
    thickness: _length("Thickness", 0.01, "Diameter of the round cross section")
    thickness_sides: IntProperty(name="Sides", default=12, min=3, max=100, update=_update,
                                 description="Sides of the round cross section")
    render_angle: _angle("Angle", 0.0)
    rect_length: FloatProperty(name="Length", default=0.06, min=0.0, unit='LENGTH',
                               update=lambda self, ctx: _update_rect(self, ctx, "rect_length"),
                               description="Height of the rectangular cross section")
    rect_width: FloatProperty(name="Width", default=0.02, min=0.0, unit='LENGTH',
                              update=lambda self, ctx: _update_rect(self, ctx, "rect_width"),
                              description="Width of the rectangular cross section")
    rect_aspect: FloatProperty(name="Aspect", min=0.0, description="Length divided by Width",
                               get=lambda self: self.rect_length / self.rect_width if self.rect_width else 0.0,
                               set=lambda self, value: setattr(self, "rect_width", self.rect_length / value)
                               if value > 0 else None)
    rect_aspect_lock: BoolProperty(name="Lock Aspect", update=lambda self, ctx: _lock_aspect(self),
                                   description="Changing Length or Width keeps the aspect")
    rect_locked_aspect: FloatProperty(options={'HIDDEN'})
    # Use Viewport Settings: the viewport mesh can be thinner or coarser than the rendered one.
    use_viewport_settings: BoolProperty(name="Use Viewport Settings", update=_update,
                                        description="The viewport uses its own thickness and sides")
    render_settings_target: EnumProperty(name="Settings", default='RENDERER', items=(
        ('VIEWPORT', "Viewport", "Edit the viewport's settings"),
        ('RENDERER', "Renderer", "Edit the renderer's settings")))
    viewport_thickness: _length("Thickness", 0.01, "Diameter of the round cross section in the viewport")
    viewport_sides: IntProperty(name="Sides", default=12, min=3, max=100, update=_update,
                                description="Sides of the round cross section in the viewport")
    viewport_rect_length: _length("Length", 0.06, "Height of the rectangular cross section in the viewport")
    viewport_rect_width: _length("Width", 0.02, "Width of the rectangular cross section in the viewport")
    rect_angle: _angle("Angle", 0.0)
    auto_smooth: BoolProperty(name="Auto Smooth", default=True, update=_update,
                              description="Smooth the mesh, keeping edges sharper than the threshold")
    smooth_threshold: _angle("Threshold", 40.0)
    mapping: BoolProperty(name="Generate Mapping Coords", update=_update,
                          description="UVs: U along the spline (in length), V around the cross section")
    twist_correction: BoolProperty(name="Twist Correction", default=True, update=_update,
                                   description="The cross section follows the spline with the least twist")
    cap: BoolProperty(name="Cap", default=True, update=_update, description="Close the ends of open splines")
    quad_cap: BoolProperty(name="Quad Cap", update=_update, description="Flat caps made of quad rings")
    cap_segments: IntProperty(name="Segments", default=4, min=1, max=100, update=_update,
                              description="Rings of a quad or sphere cap")
    cap_sphere: BoolProperty(name="Sphere", update=_update, description="Round caps")
    # Geometry: End Point Auto-Welding.
    auto_weld: BoolProperty(name="Automatic Welding",
                            description="A spline end moved within the threshold of another end welds to it")
    weld_threshold: FloatProperty(name="Threshold Dist", default=0.15, min=0.0, unit='LENGTH',
                                  description="How close an end must come to another to weld")


# Parameters per shape, in Max's order: (UI label, property).
PARAMETERS = {
    'RECTANGLE': (("Length", "length"), ("Width", "width"), ("Corner Radius", "corner_radius")),
    'CIRCLE': (("Radius", "radius"),),
    'ELLIPSE': (("Length", "length"), ("Width", "width")),
    'ARC': (("Radius", "radius"), ("From", "angle_from"), ("To", "angle_to"), ("Pie Slice", "pie"),
            ("Reverse", "reverse")),
    'NGON': (("Radius", "radius"), ("Inscribed", "scribe"), ("Sides", "sides"),
             ("Corner Radius", "corner_radius"), ("Circular", "circular")),
    'STAR': (("Radius 1", "radius1"), ("Radius 2", "radius2"), ("Points", "points"),
             ("Distortion", "distortion"), ("Fillet Radius 1", "fillet1"), ("Fillet Radius 2", "fillet2")),
    'HELIX': (("Radius 1", "radius1"), ("Radius 2", "radius2"), ("Height", "height"), ("Turns", "turns"),
              ("Bias", "bias"), ("Direction", "direction")),
    'DONUT': (("Radius 1", "radius1"), ("Radius 2", "radius2")),
    'EGG': (("Length", "egg_length"), ("Width", "width"), ("Thickness", "egg_thickness"),
            ("Angle", "egg_angle"), ("Outline", "outline")),
}
COMMON = (("Steps", "steps"), ("Optimize", "optimize"), ("Enable In Renderer", "render_renderer"),
          ("Enable In Viewport", "render_viewport"), ("Thickness", "thickness"),
          ("Thickness Sides", "thickness_sides"))
# Max's defaults per shape where they differ from the property defaults.
DEFAULTS = {
    'ELLIPSE': {"width": 0.6},
    'DONUT': {"radius2": 0.35},
    'HELIX': {"radius2": 0.5},
    'EGG': {"width": 0.4},
}


class _Input:
    """One shape parameter, read and written through `value` like a modifier input."""

    def __init__(self, shape, prop):
        self._shape, self._prop = shape, prop

    @property
    def value(self):
        return getattr(self._shape, self._prop)

    @value.setter
    def value(self, value):
        setattr(self._shape, self._prop, value)


def shape_kind(obj):
    if obj is None or obj.type != 'CURVE':
        return None
    kind = obj.data.maximize_shape.kind
    return None if kind == 'NONE' else kind


def shape_input(obj, name):
    """The shape parameter with that UI name; raises KeyError if the shape has none."""
    kind = shape_kind(obj)
    for label, prop in PARAMETERS.get(kind, ()) + COMMON:
        if label == name:
            return _Input(obj.data.maximize_shape, prop)
    raise KeyError(name)


def draw_shape_parameters(layout, obj):
    shape = obj.data.maximize_shape
    col = layout.column(align=True)
    for label, prop in PARAMETERS[shape.kind]:
        if prop == 'scribe':
            col.row(align=True).prop(shape, prop, expand=True)
        else:
            col.prop(shape, prop, text=label)
    layout.label(text="Interpolation")
    col = layout.column(align=True)
    col.prop(shape, "steps")
    if hasattr(obj.data, "use_optimize"):
        col.prop(shape, "optimize")
    col.prop(shape, "adaptive")
    layout.label(text="Rendering")
    from . import spline_render
    spline_render.draw(layout, obj)


def create_shape(context, kind, name):
    """A new shape object with Max's defaults; not linked, selected or placed yet."""
    curve = bpy.data.curves.new(name, 'CURVE')
    shape = curve.maximize_shape
    for prop, value in DEFAULTS.get(kind, {}).items():
        setattr(shape, prop, value)
    shape.kind = kind
    rebuild(curve)
    return bpy.data.objects.new(name, curve)


# ------------------------------------------------------------------------------
# Convert to Editable Spline


_HANDLE_TYPES = ('FREE', 'AUTO', 'VECTOR', 'ALIGNED')


def _attr(curves, name, default):
    attr = curves.attributes.get(name)
    if attr is None:
        return lambda i: default
    data = attr.data
    key = "vector" if attr.data_type == 'FLOAT_VECTOR' else "value"
    return lambda i: getattr(data[i], key)


def curve_from_geometry(curves, name):
    """Legacy curve data (Blender's editable spline) from evaluated curves geometry: Bezier
    splines keep their handles, poly curves become Bezier splines with vector handles."""
    data = bpy.data.curves.new(name, 'CURVE')
    data.dimensions = '3D'
    if curves is None:
        return data
    position = _attr(curves, "position", (0.0, 0.0, 0.0))
    left = _attr(curves, "handle_left", None)
    right = _attr(curves, "handle_right", None)
    left_type = _attr(curves, "handle_type_left", 0)
    right_type = _attr(curves, "handle_type_right", 0)
    tilt = _attr(curves, "tilt", 0.0)
    radius = _attr(curves, "radius", 1.0)
    curve_type = _attr(curves, "curve_type", 0)
    cyclic = _attr(curves, "cyclic", False)
    for ci, c in enumerate(curves.curves):
        first, count = c.first_point_index, c.points_length
        spline = data.splines.new('BEZIER')
        spline.bezier_points.add(count - 1)
        bezier = curve_type(ci) == 2 and left(first) is not None
        for k, bp in enumerate(spline.bezier_points):
            i = first + k
            bp.co = position(i)
            bp.tilt = tilt(i)
            bp.radius = radius(i)
            if bezier:
                bp.handle_left_type = bp.handle_right_type = 'FREE'
                bp.handle_left = left(i)
                bp.handle_right = right(i)
                bp.handle_left_type = _HANDLE_TYPES[left_type(i) % 4]
                bp.handle_right_type = _HANDLE_TYPES[right_type(i) % 4]
            else:
                # Poly curves (polygons, arcs, stars) become Bezier splines with vector handles,
                # so Fillet and the handle tools work on them.
                bp.handle_left_type = bp.handle_right_type = 'VECTOR'
        spline.use_cyclic_u = bool(cyclic(ci))
    return data


def to_editable_spline(context, obj):
    """Make a shape an editable spline: the parameters go, the splines stay. Returns the object.
    Shapes saved by earlier versions (a Geometry Nodes poly curve) are rebuilt as a curve
    object with the same name, transform and materials."""
    if shape_kind(obj) is not None:
        obj.data.maximize_shape.kind = 'NONE'
        return obj
    obj.update_tag()
    depsgraph = context.evaluated_depsgraph_get()
    depsgraph.update()
    # Keep the geometry set alive while its curves are read.
    geometry = obj.evaluated_get(depsgraph).evaluated_geometry()
    name = obj.name
    data = curve_from_geometry(geometry.curves, name)
    new = bpy.data.objects.new(name + ".spline", data)
    for coll in obj.users_collection:
        coll.objects.link(new)
    new.matrix_world = obj.matrix_world
    for mat in obj.data.materials:
        data.materials.append(mat)
    old_data = obj.data
    bpy.data.objects.remove(obj)
    if old_data is not None and old_data.users == 0:
        (bpy.data.meshes if isinstance(old_data, bpy.types.Mesh) else bpy.data.curves).remove(old_data)
    new.name = name
    data.name = name
    new.select_set(True)
    context.view_layer.objects.active = new
    return new


def register():
    bpy.utils.register_class(MaximizeShape)
    bpy.types.Curve.maximize_shape = PointerProperty(type=MaximizeShape)


def unregister():
    del bpy.types.Curve.maximize_shape
    bpy.utils.unregister_class(MaximizeShape)
