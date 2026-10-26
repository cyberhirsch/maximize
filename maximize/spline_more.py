# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""The rest of Max's Editable Spline Geometry and Selection rollouts:
Refine (Connect, Linear, Closed), Insert, Create Line, Cycle, Hide / Unhide All, Attach Mult.
(Reorient), Cross Section, Area Selection, Select By, Named Selections Copy / Paste, Show Vertex
Numbers (Selected Only), Tangent Copy / Paste, Detach (Same Shp, Reorient, Copy), Explode (To
Splines / Objects), Mirror (Horizontal / Vertical / Both, Copy, About Pivot), Adaptive
interpolation.

Everything works on plain Blender Bezier curves; nothing new is stored but a few settings on the
curve's `maximize_shape`.
"""

import math

import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty
from bpy.types import Operator
from mathutils import Matrix, Vector

from .spline_tools import (
    _PickSpline, _Point, _edit_curves, _insert, _read, _segment, _segment_count, _straight,
    _with_object_mode, _write,
)


# ------------------------------------------------------------------------------
# Refine and Insert


class MAXIMIZE_OT_spline_refine(_PickSpline, Operator):
    """Max's Refine: click on a segment to add a vertex without changing the shape; Connect joins
    the added vertices into a new spline when you finish (Linear: corner vertices; Closed: closed)"""
    bl_idname = "maximize.spline_refine"
    bl_label = "Refine"
    status = "Refine: click on a segment to add a vertex; right-click or Esc to finish"

    connect: BoolProperty(name="Connect", description="Join the added vertices into a new spline")
    linear: BoolProperty(name="Linear", description="The connecting spline gets corner vertices")
    closed: BoolProperty(name="Closed", description="Close the connecting spline")

    def invoke(self, context, event):
        self._added = []
        return super().invoke(context, event)

    def act(self, curve, index, u):
        spline = curve.splines[index]
        if spline.type != 'BEZIER':
            return
        points = _read(spline)
        for p in points:
            p.select = False
        new = _insert(points, spline.use_cyclic_u, [u])
        if len(new) == len(points):
            return
        added = next(p for p in new if p.select)
        self._added.append((curve, added.co.copy()))
        _write(curve, spline, new)

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'} and event.value == 'PRESS' and self.connect:
            groups = {}
            for curve, co in self._added:
                groups.setdefault(curve, []).append(co)
            if groups:
                _with_object_mode(context, lambda _objects: [
                    connect_points(curve, cos, self.linear, self.closed)
                    for curve, cos in groups.items() if len(cos) > 1])
        return super().modal(context, event)


def connect_points(curve, cos, linear, closed):
    """A new spline through `cos`: corner vertices (Linear) or smooth ones."""
    kind = 'VECTOR' if linear else 'AUTO'
    points = [_Point(co, left_type=kind, right_type=kind) for co in cos]
    spline = curve.splines.new('BEZIER')
    spline.bezier_points.add(len(points) - 1)
    for bp, p in zip(spline.bezier_points, points):
        bp.co = p.co
        bp.handle_left_type = bp.handle_right_type = kind
    spline.use_cyclic_u = closed
    return spline


class MAXIMIZE_OT_spline_insert(Operator):
    """Max's Insert: click on a segment to add a vertex, then move it"""
    bl_idname = "maximize.spline_insert"
    bl_label = "Insert"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_CURVE' and context.area is not None and context.area.type == 'VIEW_3D'

    def invoke(self, context, _event):
        context.window_manager.modal_handler_add(self)
        context.workspace.status_text_set("Insert: click on a segment, then move the new vertex")
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'} and event.value == 'PRESS':
            context.workspace.status_text_set(None)
            return {'CANCELLED'}
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            hit = _PickSpline._pick(self, context, event)
            if hit is None:
                return {'RUNNING_MODAL'}
            obj, index, u = hit

            def add(_objects):
                for o in _edit_curves(context):
                    for s in o.data.splines:
                        for bp in s.bezier_points:
                            bp.select_control_point = bp.select_left_handle = bp.select_right_handle = False
                spline = obj.data.splines[index]
                points = _read(spline)
                for p in points:
                    p.select = False
                _write(obj.data, spline, _insert(points, spline.use_cyclic_u, [u]))
            _with_object_mode(context, add)
            context.workspace.status_text_set(None)
            bpy.ops.transform.translate('INVOKE_DEFAULT')
            return {'FINISHED'}
        return {'PASS_THROUGH'}


class MAXIMIZE_OT_spline_create_line(Operator):
    """Max's Create Line: draw a new spline into this shape"""
    bl_idname = "maximize.spline_create_line"
    bl_label = "Create Line"

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_CURVE'

    def execute(self, context):
        obj = context.edit_object
        bpy.ops.object.mode_set(mode='OBJECT')
        obj.select_set(True)
        context.view_layer.objects.active = obj
        return bpy.ops.maximize.line('INVOKE_DEFAULT', start_new_shape=False)


# ------------------------------------------------------------------------------
# Selection: Cycle, Area Selection, Select By, Named Selections


def _bezier_points(context):
    for obj in _edit_curves(context):
        for si, s in enumerate(obj.data.splines):
            for pi, bp in enumerate(s.bezier_points):
                yield obj, si, pi, bp


def _select(bp, state):
    bp.select_control_point = bp.select_left_handle = bp.select_right_handle = state


class MAXIMIZE_OT_spline_cycle(Operator):
    """Max's Cycle: move the vertex selection to the next vertex of each spline"""
    bl_idname = "maximize.spline_cycle"
    bl_label = "Cycle"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_CURVE'

    def execute(self, context):
        def run(objects):
            for obj in objects:
                for s in obj.data.splines:
                    pts = s.bezier_points
                    chosen = [i for i, bp in enumerate(pts) if bp.select_control_point]
                    if len(chosen) != 1:
                        continue
                    _select(pts[chosen[0]], False)
                    _select(pts[(chosen[0] + 1) % len(pts)], True)
        _with_object_mode(context, run)
        return {'FINISHED'}


class MAXIMIZE_OT_spline_area_select(Operator):
    """Max's Area Selection: also select the vertices within the distance of the selected ones"""
    bl_idname = "maximize.spline_area_select"
    bl_label = "Area Selection"
    bl_options = {'REGISTER', 'UNDO'}

    distance: FloatProperty(name="Area", default=0.1, min=0.0, unit='LENGTH')

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_CURVE'

    def execute(self, context):
        def run(objects):
            for obj in objects:
                pts = [bp for s in obj.data.splines for bp in s.bezier_points]
                seeds = [bp.co.copy() for bp in pts if bp.select_control_point]
                for bp in pts:
                    if any((bp.co - c).length <= self.distance for c in seeds):
                        _select(bp, True)
        _with_object_mode(context, run)
        return {'FINISHED'}


class MAXIMIZE_OT_spline_select_by(Operator):
    """Max's Select By: at vertex level, select every vertex of the segments or splines that have a
    selected vertex"""
    bl_idname = "maximize.spline_select_by"
    bl_label = "Select By"
    bl_options = {'REGISTER', 'UNDO'}

    by: EnumProperty(name="By", items=(('SEGMENT', "Segment", ""), ('SPLINE', "Spline", "")))

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_CURVE'

    def execute(self, context):
        def run(objects):
            for obj in objects:
                for s in obj.data.splines:
                    pts = s.bezier_points
                    chosen = [i for i, bp in enumerate(pts) if bp.select_control_point]
                    if not chosen:
                        continue
                    if self.by == 'SPLINE':
                        for bp in pts:
                            _select(bp, True)
                    else:
                        for i in chosen:
                            for j in (i - 1, i + 1):
                                if 0 <= j < len(pts) or s.use_cyclic_u:
                                    _select(pts[j % len(pts)], True)
        _with_object_mode(context, run)
        return {'FINISHED'}


_named = {}


class MAXIMIZE_OT_spline_named_copy(Operator):
    """Named Selections Copy: remember the selected vertices"""
    bl_idname = "maximize.spline_named_copy"
    bl_label = "Copy"

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_CURVE'

    def execute(self, context):
        def run(objects):
            _named.clear()
            for obj in objects:
                _named[obj.name] = [(si, pi) for si, s in enumerate(obj.data.splines)
                                    for pi, bp in enumerate(s.bezier_points) if bp.select_control_point]
        _with_object_mode(context, run)
        return {'FINISHED'}


class MAXIMIZE_OT_spline_named_paste(Operator):
    """Named Selections Paste: select the remembered vertices again"""
    bl_idname = "maximize.spline_named_paste"
    bl_label = "Paste"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_CURVE' and bool(_named)

    def execute(self, context):
        def run(objects):
            for obj in objects:
                for si, pi in _named.get(obj.name, ()):
                    if si < len(obj.data.splines) and pi < len(obj.data.splines[si].bezier_points):
                        _select(obj.data.splines[si].bezier_points[pi], True)
        _with_object_mode(context, run)
        return {'FINISHED'}


# ------------------------------------------------------------------------------
# Hide / Unhide All, Tangent Copy / Paste


class MAXIMIZE_OT_spline_hide(Operator):
    """Max's Hide / Unhide All (vertex and segment levels)"""
    bl_idname = "maximize.spline_hide"
    bl_label = "Hide"
    bl_options = {'REGISTER', 'UNDO'}

    unhide_all: BoolProperty(name="Unhide All")

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_CURVE'

    def execute(self, context):
        if self.unhide_all:
            return bpy.ops.curve.reveal(select=False)
        return bpy.ops.curve.hide(unselected=False)


_tangent = []


class MAXIMIZE_OT_spline_tangent(Operator):
    """Max's Tangent Copy / Paste: copy the handles of the selected vertex, paste them onto other
    vertices"""
    bl_idname = "maximize.spline_tangent"
    bl_label = "Tangent"
    bl_options = {'REGISTER', 'UNDO'}

    action: EnumProperty(items=(('COPY', "Copy", ""), ('PASTE', "Paste", "")))
    length: BoolProperty(name="Paste Length", default=True, description="Paste the handle length too")

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_CURVE'

    def execute(self, context):
        def run(objects):
            chosen = [bp for obj in objects for s in obj.data.splines for bp in s.bezier_points
                      if bp.select_control_point]
            if self.action == 'COPY':
                if not chosen:
                    return 0
                bp = chosen[0]
                _tangent[:] = [bp.handle_left - bp.co, bp.handle_right - bp.co]
                return 1
            if not _tangent:
                return 0
            left, right = _tangent
            for bp in chosen:
                bp.handle_left_type = bp.handle_right_type = 'FREE'
                if self.length:
                    bp.handle_left, bp.handle_right = bp.co + left, bp.co + right
                else:
                    for side, vec in (("handle_left", left), ("handle_right", right)):
                        old = (getattr(bp, side) - bp.co).length
                        setattr(bp, side, bp.co + vec.normalized() * old)
            return len(chosen)
        if not _with_object_mode(context, run):
            self.report({'WARNING'}, "Select a vertex first" if self.action == 'COPY' else "Copy a tangent first")
            return {'CANCELLED'}
        return {'FINISHED'}


# ------------------------------------------------------------------------------
# Attach Mult. (Reorient), Cross Section


def _curve_objects(self, context):
    edited = context.edit_object or context.active_object
    return [(o.name, o.name, "") for o in context.view_layer.objects
            if o.type == 'CURVE' and o != edited] or [("", "(no shapes)", "")]


def attach(context, target, others, reorient):
    """Join `others` into `target`; Reorient first gives each the target's transform."""
    if reorient:
        for o in others:
            o.matrix_world = target.matrix_world.copy()
    for o in context.view_layer.objects:
        o.select_set(False)
    for o in (target, *others):
        o.select_set(True)
    context.view_layer.objects.active = target
    bpy.ops.object.join()


class MAXIMIZE_OT_spline_attach_multiple(Operator):
    """Max's Attach Mult.: pick shapes from a list and attach them to this one"""
    bl_idname = "maximize.spline_attach_multiple"
    bl_label = "Attach Mult."
    bl_options = {'REGISTER', 'UNDO'}

    shapes: EnumProperty(name="Shapes", items=_curve_objects, options={'ENUM_FLAG'})
    reorient: BoolProperty(name="Reorient", description="Attached shapes take this shape's position and rotation")

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == 'CURVE' and context.mode in {'OBJECT', 'EDIT_CURVE'}

    def invoke(self, context, _event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        target = context.active_object
        others = [bpy.data.objects[n] for n in self.shapes if n in bpy.data.objects]
        if not others:
            return {'CANCELLED'}
        edit = context.mode == 'EDIT_CURVE'
        if edit:
            bpy.ops.object.mode_set(mode='OBJECT')
        attach(context, target, others, self.reorient)
        if edit:
            bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}


def cross_section(curve, indices, linear=False):
    """Max's Cross Section: splines through the matching vertices of the given splines, in order.
    Returns how many splines were made."""
    splines = [curve.splines[i] for i in indices]
    count = min(len(s.bezier_points) for s in splines)
    made = 0
    for k in range(count):
        cos = [s.bezier_points[k].co.copy() for s in splines]
        connect_points(curve, cos, linear, False)
        made += 1
    return made


class MAXIMIZE_OT_spline_cross_section(Operator):
    """Max's Cross Section: connect the selected splines' vertices with new splines, in order
    (cross sections for a Surface-style cage)"""
    bl_idname = "maximize.spline_cross_section"
    bl_label = "Cross Section"
    bl_options = {'REGISTER', 'UNDO'}

    linear: BoolProperty(name="Linear", description="The new splines get corner vertices")

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_CURVE'

    def execute(self, context):
        def run(objects):
            made = 0
            for obj in objects:
                chosen = [i for i, s in enumerate(obj.data.splines) if s.type == 'BEZIER' and
                          any(bp.select_control_point for bp in s.bezier_points)]
                if len(chosen) > 1:
                    made += cross_section(obj.data, chosen, self.linear)
            return made
        if not _with_object_mode(context, run):
            self.report({'WARNING'}, "Select vertices on two or more splines")
            return {'CANCELLED'}
        return {'FINISHED'}


# ------------------------------------------------------------------------------
# Detach and Explode options, Mirror options


class MAXIMIZE_OT_spline_detach_max(Operator):
    """Max's Detach: the selected segments or splines become a new shape (Same Shp: a new spline in
    this shape; Reorient: the new shape sits at the world origin; Copy: keep the original)"""
    bl_idname = "maximize.spline_detach_max"
    bl_label = "Detach"
    bl_options = {'REGISTER', 'UNDO'}

    same_shape: BoolProperty(name="Same Shp", description="Detach into a new spline of this shape")
    reorient: BoolProperty(name="Reorient", description="The detached shape moves to the world origin")
    copy: BoolProperty(name="Copy", description="Keep the original segments")

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_CURVE'

    def execute(self, context):
        if self.copy:
            bpy.ops.curve.duplicate()
        if self.same_shape:
            return bpy.ops.curve.split() if not self.copy else {'FINISHED'}
        before = set(bpy.data.objects)
        result = bpy.ops.curve.separate()
        if self.reorient:
            for o in set(bpy.data.objects) - before:
                o.matrix_world = Matrix()
        return result


def explode_to_splines(curve):
    """Every segment of every spline becomes its own spline. Returns the new spline count."""
    old = list(curve.splines)
    made = 0
    for spline in old:
        if spline.type != 'BEZIER':
            continue
        points = _read(spline)
        for i in range(_segment_count(points, spline.use_cyclic_u)):
            c = _segment(points, i)
            a, b = points[i], points[(i + 1) % len(points)]
            kind = 'VECTOR' if _straight(c) else 'FREE'
            pair = [_Point(c[0], a.left, c[1], a.left_type, kind),
                    _Point(c[3], c[2], b.right, kind, b.right_type)]
            _write(curve, None, pair, cyclic=False)
            made += 1
        curve.splines.remove(spline)
    return made


class MAXIMIZE_OT_spline_explode_max(Operator):
    """Max's Explode: every segment becomes its own spline, or every spline its own object"""
    bl_idname = "maximize.spline_explode_max"
    bl_label = "Explode"
    bl_options = {'REGISTER', 'UNDO'}

    to: EnumProperty(name="To", default='OBJECTS', items=(
        ('SPLINES', "Splines", "Every segment becomes a spline of this shape"),
        ('OBJECTS', "Objects", "Every spline becomes its own shape object")))

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_CURVE'

    def execute(self, context):
        if self.to == 'OBJECTS':
            return bpy.ops.maximize.spline_explode()
        _with_object_mode(context, lambda objects: [explode_to_splines(o.data) for o in objects])
        return {'FINISHED'}


class MAXIMIZE_OT_spline_mirror_max(Operator):
    """Max's Mirror (spline level): Horizontal, Vertical or Both; Copy keeps the originals; About
    Pivot mirrors about the shape's pivot instead of each spline's centre"""
    bl_idname = "maximize.spline_mirror_max"
    bl_label = "Mirror"
    bl_options = {'REGISTER', 'UNDO'}

    axis: EnumProperty(name="Axis", items=(('X', "Horizontal", ""), ('Y', "Vertical", ""), ('BOTH', "Both", "")))
    copy: BoolProperty(name="Copy", description="Mirror a copy and keep the originals")
    about_pivot: BoolProperty(name="About Pivot", description="Mirror about the shape's pivot")

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_CURVE'

    def execute(self, context):
        if self.copy:
            bpy.ops.curve.duplicate()
        constraint = (self.axis in {'X', 'BOTH'}, self.axis in {'Y', 'BOTH'}, False)
        settings = context.scene.tool_settings
        pivot = settings.transform_pivot_point
        try:
            if self.about_pivot:
                bpy.ops.transform.mirror(orient_type='LOCAL', constraint_axis=constraint,
                                         center_override=context.edit_object.matrix_world.translation)
            else:
                settings.transform_pivot_point = 'INDIVIDUAL_ORIGINS'
                bpy.ops.transform.mirror(orient_type='LOCAL', constraint_axis=constraint)
        finally:
            settings.transform_pivot_point = pivot
        return {'FINISHED'}


# ------------------------------------------------------------------------------
# Adaptive interpolation

# Max's Adaptive: as many steps as it takes for about 6 degrees per step on curved segments.
ADAPTIVE_ANGLE = math.radians(6.0)


def adaptive_steps(spline):
    """Steps for the spline's most curved segment (Blender has one resolution per spline)."""
    points = _read(spline)
    best = 0
    for i in range(_segment_count(points, spline.use_cyclic_u)):
        c = _segment(points, i)
        if _straight(c):
            continue
        # Turning of the tangent along the segment, from the control polygon.
        legs = [c[1] - c[0], c[2] - c[1], c[3] - c[2]]
        legs = [v for v in legs if v.length > 1e-9]
        turn = sum(a.angle(b) for a, b in zip(legs, legs[1:]))
        best = max(best, math.ceil(turn / ADAPTIVE_ANGLE))
    return max(1, min(best, 100))


def apply_adaptive(curve):
    for spline in curve.splines:
        if spline.type == 'BEZIER':
            spline.resolution_u = adaptive_steps(spline)


def _adaptive_watch():
    """Keep Adaptive shapes' steps up to date after edits (cheap: only Adaptive shapes)."""
    for curve in bpy.data.curves:
        p = getattr(curve, "maximize_shape", None)
        if p is None or not p.adaptive or curve.is_editmode:
            continue
        for spline in curve.splines:
            if spline.type == 'BEZIER':
                steps = adaptive_steps(spline)
                if spline.resolution_u != steps:
                    spline.resolution_u = steps
    return 0.5


# ------------------------------------------------------------------------------
# Connect Copy: Shift+drag copies of segments get connected to their originals

_last_duplicate = None


def connect_copies(curve, delta):
    """Straight splines from each selected vertex (the copies) back to the unselected vertex it was
    copied from, `delta` (local) away. Returns how many were made."""
    originals = [bp.co.copy() for s in curve.splines for bp in s.bezier_points if not bp.select_control_point]
    copies = [bp.co.copy() for s in curve.splines for bp in s.bezier_points if bp.select_control_point]
    made = 0
    for co in copies:
        source = co - delta
        if any((o - source).length < 1e-4 for o in originals):
            connect_points(curve, [source, co], True, False)
            made += 1
    return made


def _connect_copy_watch():
    global _last_duplicate
    wm = bpy.context.window_manager
    ops = wm.operators if wm else ()
    if not ops or ops[-1].bl_idname != "CURVE_OT_duplicate_move":
        return 0.2
    op = ops[-1]
    if op.as_pointer() == _last_duplicate:
        return 0.2
    _last_duplicate = op.as_pointer()
    obj = bpy.context.view_layer.objects.active if bpy.context.view_layer else None
    if obj is None or obj.type != 'CURVE' or obj.mode != 'EDIT' or not obj.data.maximize_shape.connect_copy:
        return 0.2
    move = next((m for m in getattr(op, "macros", {}).values() if m.bl_idname == "TRANSFORM_OT_translate"), None)
    if move is None:
        return 0.2
    delta = obj.matrix_world.inverted_safe().to_3x3() @ Vector(move.properties.value)
    window = wm.windows[0] if wm.windows else None
    if window is None or delta.length < 1e-9:
        return 0.2
    with bpy.context.temp_override(window=window):
        if _with_object_mode(bpy.context, lambda objects: connect_copies(obj.data, delta)):
            bpy.ops.ed.undo_push(message="Connect Copy")
    return 0.2


# ------------------------------------------------------------------------------
# Section as a plane object: move it, the cut shows live, Create Shape makes the shape

SECTION_TAG = "maximize_section"
_section_cache = {}


def _section_targets(context, plane):
    return [o for o in context.view_layer.objects if o.type == 'MESH' and o != plane and
            not o.get(SECTION_TAG) and o.visible_get()]


def _section_frame(plane):
    mw = plane.matrix_world
    return mw.translation.copy(), (mw.to_3x3() @ Vector((0.0, 0.0, 1.0))).normalized()


class MAXIMIZE_OT_section_plane(Operator):
    """Max's Section: a plane object at the 3D cursor; move or rotate it and the cut shows in
    yellow; Create Shape turns the cut into a shape"""
    bl_idname = "maximize.section_plane"
    bl_label = "Section Plane"
    bl_options = {'REGISTER', 'UNDO'}

    size: FloatProperty(name="Size", default=2.0, min=0.0, unit='LENGTH')

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        import bmesh
        mesh = bpy.data.meshes.new("Section")
        bm = bmesh.new()
        bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=self.size / 2.0)
        bm.to_mesh(mesh)
        bm.free()
        plane = bpy.data.objects.new("Section", mesh)
        plane[SECTION_TAG] = True
        plane.display_type = 'WIRE'
        plane.hide_render = True
        plane.visible_shadow = False
        context.collection.objects.link(plane)
        plane.matrix_world = context.scene.cursor.matrix
        for o in context.selected_objects:
            o.select_set(False)
        plane.select_set(True)
        context.view_layer.objects.active = plane
        return {'FINISHED'}


class MAXIMIZE_OT_section_create_shape(Operator):
    """Max's Section > Create Shape: the cut of the section plane through the visible meshes"""
    bl_idname = "maximize.section_create_shape"
    bl_label = "Create Shape"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return context.mode == 'OBJECT' and obj is not None and bool(obj.get(SECTION_TAG))

    def execute(self, context):
        from .spline_tools import section_curve
        plane = context.active_object
        origin, normal = _section_frame(plane)
        obj = section_curve(context, _section_targets(context, plane), origin, normal)
        if obj is None:
            self.report({'WARNING'}, "The section cuts nothing")
            return {'CANCELLED'}
        return {'FINISHED'}


def _section_dirty(*_args):
    _section_cache.clear()


def _draw_sections():
    context = bpy.context
    if context.mode != 'OBJECT':
        return
    planes = [o for o in context.view_layer.objects if o.get(SECTION_TAG) and o.visible_get()]
    if not planes:
        return
    from .spline_tools import section_loops
    lines = []
    for plane in planes:
        key = (plane.name, tuple(map(tuple, plane.matrix_world)))
        cached = _section_cache.get(key)
        if cached is None:
            origin, normal = _section_frame(plane)
            cached = []
            for points, closed in section_loops(context, _section_targets(context, plane), origin, normal):
                ring = points + points[:1] if closed else points
                for a, b in zip(ring, ring[1:]):
                    cached += [a, b]
            _section_cache[key] = cached
        lines += cached
    if not lines:
        return
    import gpu
    from gpu_extras.batch import batch_for_shader
    shader = gpu.shader.from_builtin('POLYLINE_UNIFORM_COLOR')
    shader.uniform_float("viewportSize", (context.region.width, context.region.height))
    shader.uniform_float("lineWidth", 2.0)
    shader.uniform_float("color", (1.0, 0.9, 0.1, 1.0))
    batch_for_shader(shader, 'LINES', {"pos": lines}).draw(shader)


# ------------------------------------------------------------------------------
# Show Selected Segs

_segments_handle = None


def selected_segment_lines(obj):
    """World-space line pairs along the segments whose two ends are selected."""
    from .spline_tools import _polyline
    mw = obj.matrix_world
    lines = []
    for spline in obj.data.splines:
        if spline.type != 'BEZIER':
            continue
        points = _read(spline)
        poly = _polyline(points, spline.use_cyclic_u)
        n = len(points)
        for (u0, a), (u1, b) in zip(poly, poly[1:]):
            i = int(u0)
            if points[i % n].select and points[(i + 1) % n].select:
                lines += [mw @ a, mw @ b]
    return lines


def _draw_selected_segments():
    context = bpy.context
    obj = context.edit_object
    if obj is None or obj.type != 'CURVE' or not obj.data.maximize_shape.show_selected_segments:
        return
    lines = selected_segment_lines(obj)
    if not lines:
        return
    import gpu
    from gpu_extras.batch import batch_for_shader
    shader = gpu.shader.from_builtin('POLYLINE_UNIFORM_COLOR')
    shader.uniform_float("viewportSize", (context.region.width, context.region.height))
    shader.uniform_float("lineWidth", 2.5)
    shader.uniform_float("color", (1.0, 0.1, 0.1, 1.0))
    gpu.state.blend_set('ALPHA')
    batch_for_shader(shader, 'LINES', {"pos": lines}).draw(shader)
    gpu.state.blend_set('NONE')


# ------------------------------------------------------------------------------
# Show Vertex Numbers

_numbers_handle = None
_sections_handle = None


def _draw_vertex_numbers():
    context = bpy.context
    obj = context.edit_object
    if obj is None or obj.type != 'CURVE':
        return
    p = obj.data.maximize_shape
    if not p.show_vertex_numbers:
        return
    import blf
    from bpy_extras import view3d_utils
    region, rv3d = context.region, context.region_data
    mw = obj.matrix_world
    font = 0
    blf.size(font, 12)
    blf.color(font, 1.0, 1.0, 0.6, 1.0)
    for spline in obj.data.splines:
        for i, bp in enumerate(spline.bezier_points):
            if p.vertex_numbers_selected and not bp.select_control_point:
                continue
            at = view3d_utils.location_3d_to_region_2d(region, rv3d, mw @ bp.co)
            if at is not None:
                blf.position(font, at.x + 6, at.y + 6, 0)
                blf.draw(font, str(i + 1))


def draw_geometry_extras(layout, context, obj):
    """The Max buttons this module adds to the Editable Spline Geometry and Selection rollouts."""
    p = obj.data.maximize_shape
    box = layout.box()
    box.label(text="Selection")
    row = box.row(align=True)
    row.prop(p, "show_selected_segments")
    row.prop(p, "segment_end")
    row = box.row(align=True)
    row.prop(p, "show_vertex_numbers")
    sub = row.row(align=True)
    sub.active = p.show_vertex_numbers
    sub.prop(p, "vertex_numbers_selected")
    row = box.row(align=True)
    row.operator("maximize.spline_cycle")
    row.operator("maximize.spline_area_select")
    row.operator_menu_enum("maximize.spline_select_by", "by", text="Select By")
    row = box.row(align=True)
    row.label(text="Named Selections:")
    row.operator("maximize.spline_named_copy")
    row.operator("maximize.spline_named_paste")
    box = layout.box()
    box.label(text="Geometry (more)")
    grid = box.grid_flow(columns=2, even_columns=True, align=True)
    grid.operator("maximize.spline_create_line")
    grid.operator("maximize.spline_insert")
    grid.operator("maximize.spline_refine")
    grid.operator("maximize.spline_refine", text="Refine Connect").connect = True
    grid.operator("maximize.spline_cross_section")
    grid.operator("maximize.spline_attach_multiple")
    grid.operator("maximize.spline_hide", text="Hide").unhide_all = False
    grid.operator("maximize.spline_hide", text="Unhide All").unhide_all = True
    grid.operator("maximize.spline_tangent", text="Tangent Copy").action = 'COPY'
    grid.operator("maximize.spline_tangent", text="Tangent Paste").action = 'PASTE'
    grid.operator_menu_enum("maximize.spline_mirror_max", "axis", text="Mirror")
    grid.operator_menu_enum("maximize.spline_explode_max", "to", text="Explode")
    grid.operator("maximize.spline_detach_max", text="Detach...")
    box.prop(p, "connect_copy")


classes = (
    MAXIMIZE_OT_spline_refine,
    MAXIMIZE_OT_spline_insert,
    MAXIMIZE_OT_spline_create_line,
    MAXIMIZE_OT_spline_cycle,
    MAXIMIZE_OT_spline_area_select,
    MAXIMIZE_OT_spline_select_by,
    MAXIMIZE_OT_spline_named_copy,
    MAXIMIZE_OT_spline_named_paste,
    MAXIMIZE_OT_spline_hide,
    MAXIMIZE_OT_spline_tangent,
    MAXIMIZE_OT_spline_attach_multiple,
    MAXIMIZE_OT_spline_cross_section,
    MAXIMIZE_OT_spline_detach_max,
    MAXIMIZE_OT_spline_explode_max,
    MAXIMIZE_OT_spline_mirror_max,
    MAXIMIZE_OT_section_plane,
    MAXIMIZE_OT_section_create_shape,
)


def register():
    global _numbers_handle, _segments_handle
    for cls in classes:
        bpy.utils.register_class(cls)
    if not bpy.app.background:
        _numbers_handle = bpy.types.SpaceView3D.draw_handler_add(_draw_vertex_numbers, (), 'WINDOW', 'POST_PIXEL')
        _segments_handle = bpy.types.SpaceView3D.draw_handler_add(_draw_selected_segments, (), 'WINDOW', 'POST_VIEW')
    bpy.app.timers.register(_adaptive_watch, persistent=True)
    bpy.app.timers.register(_connect_copy_watch, persistent=True)
    bpy.app.handlers.depsgraph_update_post.append(_section_dirty)
    global _sections_handle
    if not bpy.app.background:
        _sections_handle = bpy.types.SpaceView3D.draw_handler_add(_draw_sections, (), 'WINDOW', 'POST_VIEW')


def unregister():
    global _numbers_handle, _segments_handle
    if _segments_handle is not None:
        bpy.types.SpaceView3D.draw_handler_remove(_segments_handle, 'WINDOW')
        _segments_handle = None
    global _sections_handle
    if _sections_handle is not None:
        bpy.types.SpaceView3D.draw_handler_remove(_sections_handle, 'WINDOW')
        _sections_handle = None
    if _section_dirty in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(_section_dirty)
    for timer in (_adaptive_watch, _connect_copy_watch):
        if bpy.app.timers.is_registered(timer):
            bpy.app.timers.unregister(timer)
    if _numbers_handle is not None:
        bpy.types.SpaceView3D.draw_handler_remove(_numbers_handle, 'WINDOW')
        _numbers_handle = None
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
