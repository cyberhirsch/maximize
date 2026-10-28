# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""The rest of Max's Edit Poly and Modeling ribbon tools: loops (Grow / Shrink Loop and Ring one step,
Random Loops, Loop and Ring click modes, Build End, Distribute and LoopTools' Center, Straighten,
Circle and Curve), GeoPoly, Generate Topology, To View / To Grid, Previous / Next Modifier, and the
Selection tab (Top / Bottom / Left / Right, Half, By Perspective, By View, Pivot Distance,
By Numeric).
"""

import math
import random

import bmesh
import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty
from bpy.types import Operator
from mathutils import Vector
from mathutils.bvhtree import BVHTree

from .poly_tools import _EditMesh, _edit_meshes, _opposite


# ------------------------------------------------------------------------------
# Helpers


def _mode(context):
    vert, edge, _face = context.tool_settings.mesh_select_mode
    return 'VERT' if vert else 'EDGE' if edge else 'FACE'


def _elements(bm, mode):
    seq = bm.verts if mode == 'VERT' else bm.edges if mode == 'EDGE' else bm.faces
    return [e for e in seq if not e.hide]


def _position(element):
    if isinstance(element, bmesh.types.BMVert):
        return element.co
    if isinstance(element, bmesh.types.BMEdge):
        return (element.verts[0].co + element.verts[1].co) / 2.0
    return element.calc_center_median()


def _normal(element):
    if isinstance(element, bmesh.types.BMEdge):
        n = sum((f.normal for f in element.link_faces), Vector())
        return n.normalized() if n.length > 1e-12 else n
    return element.normal


def _select_only(bm, chosen):
    for seq in (bm.verts, bm.edges, bm.faces):
        for e in seq:
            e.select = False
    for e in chosen:
        e.select_set(True)
    bm.select_flush_mode()


def _view(context):
    """The 3D View's region data: this area's, or the biggest 3D View's (from a panel button)."""
    if context.region_data is not None:
        return context.region_data
    from .vocabulary import view3d_override
    override = view3d_override(context)
    return override["region"].data if override else None


def _eye(rv3d, world, point):
    """Where the viewer looks from, in object space (for an orthographic view, far back along the
    view from `point`)."""
    inverse = world.inverted_safe()
    view_inv = rv3d.view_matrix.inverted()
    if rv3d.is_perspective:
        return inverse @ view_inv.translation
    back = view_inv.to_3x3() @ Vector((0.0, 0.0, 1.0))
    return point + (inverse.to_3x3() @ back).normalized() * 1e4


def _chains(edges):
    """The selected edges as vertex chains: (verts in order, closed). Branching parts are skipped."""
    edges = set(edges)
    links = {}
    for e in edges:
        for v in e.verts:
            links.setdefault(v, []).append(e)
    chains = []
    done = set()
    for start_edge in edges:
        if start_edge in done:
            continue
        # The connected part.
        part = set()
        todo = [start_edge]
        while todo:
            e = todo.pop()
            if e in part:
                continue
            part.add(e)
            for v in e.verts:
                todo.extend(x for x in links[v] if x not in part)
        done |= part
        verts = {v for e in part for v in e.verts}
        if any(len([x for x in links[v] if x in part]) > 2 for v in verts):
            continue
        ends = [v for v in verts if len([x for x in links[v] if x in part]) == 1]
        closed = not ends
        first = ends[0] if ends else next(iter(verts))
        order = [first]
        used = set()
        while True:
            nxt = [x for x in links[order[-1]] if x in part and x not in used]
            if not nxt:
                break
            used.add(nxt[0])
            v = nxt[0].other_vert(order[-1])
            if v is first:
                break
            order.append(v)
        chains.append((order, closed))
    return chains


def _selected_chains(bm):
    return _chains(e for e in bm.edges if e.select and not e.hide)


def _arc_lengths(points, closed):
    lengths = [0.0]
    for a, b in zip(points, points[1:] + ([points[0]] if closed else [])):
        lengths.append(lengths[-1] + (b - a).length)
    return lengths


def _at_length(points, lengths, closed, s):
    ring = points + ([points[0]] if closed else [])
    for i in range(len(ring) - 1):
        if lengths[i + 1] >= s or i == len(ring) - 2:
            span = lengths[i + 1] - lengths[i]
            t = 0.0 if span < 1e-12 else (s - lengths[i]) / span
            return ring[i].lerp(ring[i + 1], min(max(t, 0.0), 1.0))
    return ring[-1]


def _sides(vert, selected):
    """The two vertices beside `vert` across the selected loop, or None."""
    across = set(filter(None, (_opposite(e, vert) for e in vert.link_edges if e in selected)))
    sides = [e for e in vert.link_edges if e not in selected and e not in across]
    if len(sides) != 2:
        return None
    return sides[0].other_vert(vert), sides[1].other_vert(vert)


def _plane(points):
    """Best-fit plane (center, normal) of points (Newell's normal, falling back to the widest axis)."""
    center = sum(points, Vector()) / len(points)
    normal = Vector()
    for a, b in zip(points, points[1:] + points[:1]):
        normal += (a - center).cross(b - center)
    if normal.length < 1e-12:
        normal = Vector((0.0, 0.0, 1.0))
    return center, normal.normalized()


class _EditMeshUpdate(_EditMesh):
    """Runs `apply(context, obj, bm)` on each mesh in Edit Mode; `apply` returns how much it did."""

    message = "Nothing to do with this selection"

    def execute(self, context):
        done = 0
        for obj in _edit_meshes(context):
            bm = bmesh.from_edit_mesh(obj.data)
            count = self.apply(context, obj, bm)
            if count:
                done += count
                bmesh.update_edit_mesh(obj.data)
        if not done:
            self.report({'WARNING'}, self.message)
            return {'CANCELLED'}
        return {'FINISHED'}


# ------------------------------------------------------------------------------
# Loops: step, random, click modes


class MAXIMIZE_OT_step_loop(_EditMeshUpdate, Operator):
    """Grow or shrink the selected edge loops (or rings) by one edge at each end"""
    bl_idname = "maximize.step_loop"
    bl_label = "Step Loop"
    message = "Select edges first"

    action: EnumProperty(name="Action", items=(('GROW', "Grow", ""), ('SHRINK', "Shrink", "")))
    ring: BoolProperty(name="Ring", description="Along the rings instead of the loops")

    @classmethod
    def description(cls, _context, properties):
        what = "ring" if properties.ring else "loop"
        if properties.action == 'GROW':
            return "Grow the selected edges one step along their {}".format(what)
        return "Shrink the selected edges one step at the ends of their {}".format(what)

    def apply(self, context, obj, bm):
        selected = {e for e in bm.edges if e.select and not e.hide}
        if not selected:
            return 0
        if self.ring:
            def neighbours(e):
                out = []
                for f in e.link_faces:
                    if len(f.verts) == 4:
                        loop = next(l for l in f.loops if l.edge is e)
                        out.append(loop.link_loop_next.link_loop_next.edge)
                return out
        else:
            def neighbours(e):
                return list(filter(None, (_opposite(e, v) for v in e.verts)))
        if self.action == 'GROW':
            change = {n for e in selected for n in neighbours(e) if n not in selected and not n.hide}
            for e in change:
                e.select_set(True)
        else:
            # The ends: edges with a neighbour along the loop / ring that isn't selected.
            change = {e for e in selected if any(n not in selected for n in neighbours(e))
                      or len(neighbours(e)) < 2}
            if change == selected:
                change = set()
            for e in change:
                e.select_set(False)
            # Vertices of kept edges stay selected.
            for e in selected - change:
                e.select_set(True)
        bm.select_flush_mode()
        return len(change)


class MAXIMIZE_OT_random_loops(_EditMesh, Operator):
    """Random Loops: select whole loops at random, from the rings of the selected edges"""
    bl_idname = "maximize.random_loops"
    bl_label = "Random Loops"

    percent: FloatProperty(name="Percent", default=50.0, min=0.0, max=100.0, subtype='PERCENTAGE')
    seed: IntProperty(name="Seed", default=0, min=0)

    def execute(self, context):
        if not any(e.select for obj in _edit_meshes(context) for e in bmesh.from_edit_mesh(obj.data).edges):
            self.report({'WARNING'}, "Select edges first")
            return {'CANCELLED'}
        bpy.ops.mesh.select_edge_ring_multi()
        rng = random.Random(self.seed)
        for obj in _edit_meshes(context):
            bm = bmesh.from_edit_mesh(obj.data)
            ring = [e for e in bm.edges if e.select]
            keep = {e for e in ring if rng.random() * 100.0 < self.percent}
            _select_only(bm, keep)
            bmesh.update_edit_mesh(obj.data)
        bpy.ops.mesh.select_edge_loop_multi()
        return {'FINISHED'}


CLICK_MODES = (
    ('NONE', "Normal", "Clicks pick single sub-objects"),
    ('LOOP', "Loop Mode", "A click picks the whole loop"),
    ('RING', "Ring Mode", "A click picks the whole ring"),
)


class MAXIMIZE_OT_loop_mode_pick(Operator):
    """Loop / Ring mode: a click picks the whole loop or ring under the mouse"""
    bl_idname = "maximize.loop_mode_pick"
    bl_label = "Pick Loop"
    bl_options = {'INTERNAL'}

    extend: BoolProperty(options={'SKIP_SAVE'})
    deselect: BoolProperty(options={'SKIP_SAVE'})

    @classmethod
    def poll(cls, context):
        if context.mode != 'EDIT_MESH' or context.window_manager.maximize_click_mode == 'NONE':
            return False
        from .selection import current_level
        return current_level(context) in {'VERTEX', 'EDGE', 'POLYGON'}

    def invoke(self, context, _event):
        ring = context.window_manager.maximize_click_mode == 'RING'
        pick = bpy.ops.mesh.edgering_select if ring else bpy.ops.mesh.loop_select
        result = pick('INVOKE_DEFAULT', extend=self.extend, deselect=self.deselect)
        return {'FINISHED'} if 'FINISHED' in result else {'PASS_THROUGH'}


# ------------------------------------------------------------------------------
# Loops: Build End, Distribute, Center, Straighten, Circle, Curve


class MAXIMIZE_OT_build_end(_EditMeshUpdate, Operator):
    """Build End: the two edge loops through the selected edge's quads end there, in a U-turn.
    Pick the two vertices of the edge, first where the loops come from"""
    bl_idname = "maximize.build_end"
    bl_label = "Build End"
    message = "Select the two vertices of an edge between two quads (or the edge)"

    def apply(self, context, obj, bm):
        verts = [e for e in bm.select_history if isinstance(e, bmesh.types.BMVert)]
        edge = None
        if len(verts) >= 2:
            edge = bm.edges.get(verts[-2:])
            start, end = verts[-2], verts[-1]
        if edge is None:
            chosen = [e for e in bm.edges if e.select and not e.hide]
            if len(chosen) != 1:
                return 0
            edge = chosen[0]
            start, end = edge.verts
        faces = list(edge.link_faces)
        if len(faces) != 2 or any(len(f.verts) != 4 for f in faces):
            return 0

        def beside(face, vert, other):
            return next(v for v in face.verts if v is not vert and v is not other and
                        bm.edges.get((v, vert)) is not None)
        a, b = faces
        p0, q0 = beside(a, start, end), beside(a, end, start)
        p2, q2 = beside(b, start, end), beside(b, end, start)
        normal = (a.normal + b.normal).normalized()
        middle = bm.verts.new((start.co + end.co) / 2.0)
        bmesh.ops.delete(bm, geom=[edge], context='EDGES')
        made = []
        for quad in ((p0, start, middle, q0), (start, p2, q2, middle), (q0, middle, q2, end)):
            face = bm.faces.new(quad)
            face.normal_update()
            if face.normal.dot(normal) < 0.0:
                face.normal_flip()
            made.append(face)
        for f in bm.faces:
            f.select = False
        for f in made:
            f.select_set(True)
        bm.select_flush_mode()
        return 1


class _LoopShape(_EditMeshUpdate):
    """Reshapes each selected chain of edges with `shape(points, closed) -> points` (or None)."""
    message = "Select a loop or a chain of edges"

    auto_loop: BoolProperty(name="Auto Loop", description="Work on the whole loops of the selected edges")

    def execute(self, context):
        if self.auto_loop:
            bpy.ops.mesh.select_edge_loop_multi()
        return super().execute(context)

    def apply(self, context, obj, bm):
        done = 0
        for verts, closed in _selected_chains(bm):
            if len(verts) < 3:
                continue
            points = self.shape([v.co.copy() for v in verts], closed)
            if points is None:
                continue
            for v, co in zip(verts, points):
                v.co = co
            done += 1
        return done


class MAXIMIZE_OT_distribute(_LoopShape, Operator):
    """Distribute: space the vertices of the selected loops evenly along them"""
    bl_idname = "maximize.distribute"
    bl_label = "Distribute"

    def shape(self, points, closed):
        lengths = _arc_lengths(points, closed)
        total = lengths[-1]
        count = len(points) if closed else len(points) - 1
        return [_at_length(points, lengths, closed, total * i / count) for i in range(len(points))]


class MAXIMIZE_OT_loop_straighten(_LoopShape, Operator):
    """Straighten: put the vertices of the selected chains on the line between their ends"""
    bl_idname = "maximize.loop_straighten"
    bl_label = "Straighten"

    def shape(self, points, closed):
        if closed:
            return None
        a, b = points[0], points[-1]
        ab = b - a
        if ab.length_squared < 1e-12:
            return None
        return [a + ab * ((p - a).dot(ab) / ab.length_squared) for p in points]


class MAXIMIZE_OT_loop_circle(_LoopShape, Operator):
    """Circle: make the selected loops round, in their own plane"""
    bl_idname = "maximize.loop_circle"
    bl_label = "Circle"

    def shape(self, points, closed):
        center, normal = _plane(points)
        flat = [p - normal * (p - center).dot(normal) for p in points]
        radius = sum((p - center).length for p in flat) / len(flat)
        out = []
        for p in flat:
            d = p - center
            out.append(center + d.normalized() * radius if d.length > 1e-12 else p)
        return out


class MAXIMIZE_OT_loop_curve(_LoopShape, Operator):
    """Curve: smooth the selected chains into an even curve (open chains keep their ends)"""
    bl_idname = "maximize.loop_curve"
    bl_label = "Curve"

    def shape(self, points, closed):
        lengths = _arc_lengths(points, closed)
        total = lengths[-1]
        if total < 1e-12:
            return None
        if closed:
            # A smooth closed curve: the loop's first harmonics around its length.
            n = len(points)
            harmonics = min(3, (n - 1) // 2)
            angles = [2.0 * math.pi * lengths[i] / total for i in range(n)]
            coeffs = []
            for k in range(harmonics + 1):
                c = sum((p * math.cos(k * t) for p, t in zip(points, angles)), Vector()) * (2.0 / n)
                s = sum((p * math.sin(k * t) for p, t in zip(points, angles)), Vector()) * (2.0 / n)
                coeffs.append((c, s))
            out = []
            for t in angles:
                p = coeffs[0][0] / 2.0
                for k in range(1, harmonics + 1):
                    p = p + coeffs[k][0] * math.cos(k * t) + coeffs[k][1] * math.sin(k * t)
                out.append(p)
            return out
        # Open: the least-squares cubic Bezier through the two ends.
        p0, p3 = points[0], points[-1]
        ts = [l / total for l in lengths[:len(points)]]
        c11 = c12 = c22 = 0.0
        x1 = Vector()
        x2 = Vector()
        for p, t in zip(points, ts):
            b0, b1, b2, b3 = (1 - t) ** 3, 3 * t * (1 - t) ** 2, 3 * t * t * (1 - t), t ** 3
            c11 += b1 * b1
            c12 += b1 * b2
            c22 += b2 * b2
            rest = p - p0 * b0 - p3 * b3
            x1 += rest * b1
            x2 += rest * b2
        det = c11 * c22 - c12 * c12
        if abs(det) < 1e-12:
            return None
        h1 = (x1 * c22 - x2 * c12) / det
        h2 = (x2 * c11 - x1 * c12) / det
        return [p0 * (1 - t) ** 3 + h1 * 3 * t * (1 - t) ** 2 + h2 * 3 * t * t * (1 - t) + p3 * t ** 3 for t in ts]


class MAXIMIZE_OT_center_loop(_EditMeshUpdate, Operator):
    """Center: move the selected loops to the middle between the loops beside them"""
    bl_idname = "maximize.center_loop"
    bl_label = "Center"
    message = "Select edge loops between other loops"

    auto_loop: BoolProperty(name="Auto Loop", description="Work on the whole loops of the selected edges")

    def execute(self, context):
        if self.auto_loop:
            bpy.ops.mesh.select_edge_loop_multi()
        return super().execute(context)

    def apply(self, context, obj, bm):
        selected = {e for e in bm.edges if e.select and not e.hide}
        verts = {v for e in selected for v in e.verts}
        targets = []
        for v in verts:
            sides = _sides(v, selected)
            if sides is not None:
                targets.append((v, (sides[0].co + sides[1].co) / 2.0))
        for v, co in targets:
            v.co = co
        return len(targets)


# ------------------------------------------------------------------------------
# Polygons: GeoPoly, Generate Topology


class MAXIMIZE_OT_geopoly(_EditMeshUpdate, Operator):
    """GeoPoly: make each selected polygon a regular polygon, in its plane and at its size"""
    bl_idname = "maximize.geopoly"
    bl_label = "GeoPoly"
    message = "Select polygons first"

    def apply(self, context, obj, bm):
        faces = [f for f in bm.faces if f.select and not f.hide]
        sums = {}
        for f in faces:
            verts = list(f.verts)
            n = len(verts)
            center = f.calc_center_median()
            normal = f.normal
            radius = sum((v.co - center).length for v in verts) / n
            u = verts[0].co - center
            u -= normal * u.dot(normal)
            if u.length < 1e-12:
                continue
            u.normalize()
            w = normal.cross(u)
            for i, v in enumerate(verts):
                angle = 2.0 * math.pi * i / n
                co = center + (u * math.cos(angle) + w * math.sin(angle)) * radius
                total, count = sums.get(v, (Vector(), 0))
                sums[v] = (total + co, count + 1)
        for v, (total, count) in sums.items():
            v.co = total / count
        return len(faces)


class MAXIMIZE_OT_generate_topology(_EditMeshUpdate, Operator):
    """Generate Topology: replace the selected polygons (all, with none selected) with a pattern"""
    bl_idname = "maximize.generate_topology"
    bl_label = "Generate Topology"
    message = "No polygons"

    pattern: EnumProperty(name="Pattern", items=(
        ('QUADS', "Quads", "Each polygon split into quads"),
        ('DIAMOND', "Diamonds", "Quads turned 45 degrees"),
        ('FAN', "Fan", "Triangles around each polygon's center"),
        ('TRIANGLES', "Triangles", "Each polygon split into triangles"),
        ('INSET', "Inset", "A smaller copy of each polygon inside it"),
    ))
    thickness: FloatProperty(name="Inset", default=0.1, min=0.0, subtype='DISTANCE')

    def apply(self, context, obj, bm):
        faces = [f for f in bm.faces if f.select and not f.hide] or [f for f in bm.faces if not f.hide]
        if not faces:
            return 0
        if self.pattern == 'QUADS':
            edges = list({e for f in faces for e in f.edges})
            bmesh.ops.subdivide_edges(bm, edges=edges, cuts=1, use_grid_fill=True)
        elif self.pattern == 'DIAMOND':
            inner = [e for e in {e for f in faces for e in f.edges}
                     if len(e.link_faces) == 2 and all(f in faces for f in e.link_faces)]
            bmesh.ops.poke(bm, faces=faces)
            bmesh.ops.dissolve_edges(bm, edges=[e for e in inner if e.is_valid], use_verts=False)
        elif self.pattern == 'FAN':
            bmesh.ops.poke(bm, faces=faces)
        elif self.pattern == 'TRIANGLES':
            bmesh.ops.triangulate(bm, faces=faces)
        else:
            bmesh.ops.inset_individual(bm, faces=faces, thickness=self.thickness)
        return len(faces)


# ------------------------------------------------------------------------------
# Align: To View, To Grid


class MAXIMIZE_OT_align_to(_EditMeshUpdate, Operator):
    """Flatten the selection onto a plane facing the view (To View) or onto the home grid (To Grid)"""
    bl_idname = "maximize.align_to"
    bl_label = "Align"
    message = "Select sub-objects first"

    target: EnumProperty(name="Target", items=(('VIEW', "To View", "A plane facing the view, through the "
                                                "selection's center"),
                                               ('GRID', "To Grid", "The home grid (world Z = 0)")))

    @classmethod
    def description(cls, _context, properties):
        return ("To View: flatten the selection onto a plane facing the view" if properties.target == 'VIEW'
                else "To Grid: flatten the selection onto the home grid")

    def apply(self, context, obj, bm):
        verts = [v for v in bm.verts if v.select and not v.hide]
        if not verts:
            return 0
        world = obj.matrix_world
        points = [world @ v.co for v in verts]
        if self.target == 'GRID':
            origin, normal = Vector(), Vector((0.0, 0.0, 1.0))
        else:
            rv3d = _view(context)
            if rv3d is None:
                return 0
            normal = (rv3d.view_matrix.inverted().to_3x3() @ Vector((0.0, 0.0, 1.0))).normalized()
            origin = sum(points, Vector()) / len(points)
        inverse = world.inverted_safe()
        for v, p in zip(verts, points):
            v.co = inverse @ (p - normal * (p - origin).dot(normal))
        return len(verts)


# ------------------------------------------------------------------------------
# Modifier stack: Previous / Next


def _stack_entries(obj):
    """The modifiers as the stack shows them (the base's own hidden modifier left out)."""
    hidden = None
    hook = getattr(bpy.types.DATA_PT_modifiers, "moritz_base_entry", None)
    if hook is not None:
        hidden = hook(obj)[0]
    return [m for m in obj.modifiers if m != hidden]


class MAXIMIZE_OT_modifier_step(Operator):
    """Go to the previous (below) or next (above) entry of the modifier stack"""
    bl_idname = "maximize.modifier_step"
    bl_label = "Modifier"
    bl_options = {'REGISTER', 'UNDO'}

    direction: EnumProperty(name="Direction", items=(('PREVIOUS', "Previous", "The entry below"),
                                                     ('NEXT', "Next", "The entry above")))

    @classmethod
    def description(cls, _context, properties):
        return ("Previous Modifier: the entry below in the stack" if properties.direction == 'PREVIOUS'
                else "Next Modifier: the entry above in the stack")

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj is not None and len(obj.modifiers) > 0

    def execute(self, context):
        obj = context.object
        entries = _stack_entries(obj)
        active = obj.modifiers.active
        # -1 is the base object, below the first modifier.
        index = entries.index(active) if active in entries else -1
        index += -1 if self.direction == 'PREVIOUS' else 1
        if index < -1 or index >= len(entries):
            return {'CANCELLED'}
        name = entries[index].name if index >= 0 else ""
        select = getattr(bpy.ops.object, "moritz_modifier_select", None)
        if select is not None and select.poll():
            return select(modifier=name)
        if index >= 0:
            obj.modifiers.active = entries[index]
        return {'FINISHED'}


# ------------------------------------------------------------------------------
# Selection tab


class MAXIMIZE_OT_select_side(_EditMeshUpdate, Operator):
    """Keep the part of the selection (or of the mesh, with nothing selected) at one side of the view"""
    bl_idname = "maximize.select_side"
    bl_label = "Select Side"
    message = "Nothing on that side"

    side: EnumProperty(name="Side", items=(('TOP', "Top", ""), ('BOTTOM', "Bottom", ""),
                                           ('LEFT', "Left", ""), ('RIGHT', "Right", "")))
    amount: FloatProperty(name="Amount", default=50.0, min=1.0, max=100.0, subtype='PERCENTAGE',
                          description="How much of the selection's extent, from that side")

    @classmethod
    def description(cls, _context, properties):
        return "{}: keep the {} part of the selection, as seen in the view".format(
            properties.side.title(), properties.side.lower())

    def apply(self, context, obj, bm):
        rv3d = _view(context)
        if rv3d is None:
            return 0
        mode = _mode(context)
        elements = [e for e in _elements(bm, mode) if e.select] or _elements(bm, mode)
        if not elements:
            return 0
        to_view = rv3d.view_matrix @ obj.matrix_world
        axis = 1 if self.side in {'TOP', 'BOTTOM'} else 0
        sign = 1.0 if self.side in {'TOP', 'RIGHT'} else -1.0
        values = [(to_view @ _position(e))[axis] * sign for e in elements]
        hi, lo = max(values), min(values)
        limit = hi - (hi - lo) * self.amount / 100.0 - 1e-6 * max(1.0, hi - lo)
        chosen = [e for e, value in zip(elements, values) if value >= limit]
        _select_only(bm, chosen)
        return len(chosen)


class MAXIMIZE_OT_select_half(_EditMeshUpdate, Operator):
    """Half: keep the half of the selection on one side of its center, along an axis"""
    bl_idname = "maximize.select_half"
    bl_label = "Half"
    message = "Select sub-objects first"

    axis: EnumProperty(name="Axis", items=(('X', "X", ""), ('Y', "Y", ""), ('Z', "Z", "")), default='X')
    invert: BoolProperty(name="Invert", description="The other half")

    def apply(self, context, obj, bm):
        elements = [e for e in _elements(bm, _mode(context)) if e.select]
        if not elements:
            return 0
        i = "XYZ".index(self.axis)
        values = [_position(e)[i] for e in elements]
        middle = (max(values) + min(values)) / 2.0
        chosen = [e for e, value in zip(elements, values) if (value < middle) == self.invert]
        _select_only(bm, chosen)
        return len(chosen) or 1


class MAXIMIZE_OT_select_pivot_distance(_EditMeshUpdate, Operator):
    """Pivot Distance: select the sub-objects within a distance of the object's pivot"""
    bl_idname = "maximize.select_pivot_distance"
    bl_label = "Pivot Distance"
    message = "Nothing at that distance"

    distance: FloatProperty(name="Distance", default=1.0, min=0.0, subtype='DISTANCE')
    beyond: BoolProperty(name="Beyond", description="Those farther away instead")

    def apply(self, context, obj, bm):
        scale = obj.matrix_world.to_3x3()
        chosen = [e for e in _elements(bm, _mode(context))
                  if ((scale @ _position(e)).length > self.distance) == self.beyond]
        _select_only(bm, chosen)
        return len(chosen)


class MAXIMIZE_OT_select_numeric(_EditMeshUpdate, Operator):
    """By Numeric: select vertices by how many edges they have, or polygons by how many sides"""
    bl_idname = "maximize.select_numeric"
    bl_label = "By Numeric"
    message = "None match"

    count: IntProperty(name="Count", default=4, min=0)
    compare: EnumProperty(name="Compare", items=(('EQUAL', "Equal", ""), ('LESS', "Less Than", ""),
                                                 ('GREATER', "Greater Than", "")))

    def apply(self, context, obj, bm):
        mode = _mode(context)
        if mode == 'EDGE':
            mode = 'FACE'
        elements = _elements(bm, mode)

        def number(e):
            return len(e.link_edges) if mode == 'VERT' else len(e.verts)
        test = {'EQUAL': lambda n: n == self.count, 'LESS': lambda n: n < self.count,
                'GREATER': lambda n: n > self.count}[self.compare]
        chosen = [e for e in elements if test(number(e))]
        _select_only(bm, chosen)
        return len(chosen)


class MAXIMIZE_OT_select_perspective(_EditMeshUpdate, Operator):
    """By Perspective: select the sub-objects that face the view, within an angle"""
    bl_idname = "maximize.select_perspective"
    bl_label = "By Perspective"
    message = "Nothing faces the view"

    angle: FloatProperty(name="Angle", default=math.radians(45.0), min=0.0, max=math.pi, subtype='ANGLE')

    def apply(self, context, obj, bm):
        rv3d = _view(context)
        if rv3d is None:
            return 0
        limit = math.cos(self.angle)
        chosen = []
        for e in _elements(bm, _mode(context)):
            p = _position(e)
            to_eye = _eye(rv3d, obj.matrix_world, p) - p
            n = _normal(e)
            if n.length > 1e-12 and to_eye.length > 1e-12 and n.normalized().dot(to_eye.normalized()) >= limit:
                chosen.append(e)
        _select_only(bm, chosen)
        return len(chosen)


class MAXIMIZE_OT_select_by_view(_EditMeshUpdate, Operator):
    """By View: select the sub-objects you can see (nothing in front of them)"""
    bl_idname = "maximize.select_by_view"
    bl_label = "By View"
    message = "Nothing visible"

    def apply(self, context, obj, bm):
        rv3d = _view(context)
        if rv3d is None:
            return 0
        bm.faces.ensure_lookup_table()
        tree = BVHTree.FromBMesh(bm)
        chosen = []
        for e in _elements(bm, _mode(context)):
            p = _position(e)
            eye = _eye(rv3d, obj.matrix_world, p)
            d = p - eye
            length = d.length
            if length < 1e-9:
                continue
            if isinstance(e, bmesh.types.BMFace) and e.normal.dot(d) > -1e-6 * length:
                # Facing away, or seen edge-on.
                continue
            hit = tree.ray_cast(eye, d / length, length)
            if hit[0] is None or hit[3] >= length - 1e-3 or _owns(e, bm.faces[hit[2]]):
                chosen.append(e)
        _select_only(bm, chosen)
        return len(chosen)


def _owns(element, face):
    if isinstance(element, bmesh.types.BMFace):
        return element is face
    verts = [element] if isinstance(element, bmesh.types.BMVert) else list(element.verts)
    return all(v in face.verts for v in verts)


classes = (
    MAXIMIZE_OT_step_loop,
    MAXIMIZE_OT_random_loops,
    MAXIMIZE_OT_loop_mode_pick,
    MAXIMIZE_OT_build_end,
    MAXIMIZE_OT_distribute,
    MAXIMIZE_OT_loop_straighten,
    MAXIMIZE_OT_loop_circle,
    MAXIMIZE_OT_loop_curve,
    MAXIMIZE_OT_center_loop,
    MAXIMIZE_OT_geopoly,
    MAXIMIZE_OT_generate_topology,
    MAXIMIZE_OT_align_to,
    MAXIMIZE_OT_modifier_step,
    MAXIMIZE_OT_select_side,
    MAXIMIZE_OT_select_half,
    MAXIMIZE_OT_select_pivot_distance,
    MAXIMIZE_OT_select_numeric,
    MAXIMIZE_OT_select_perspective,
    MAXIMIZE_OT_select_by_view,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.WindowManager.maximize_click_mode = EnumProperty(
        name="Click Mode", items=CLICK_MODES, default='NONE',
        description="Loop / Ring mode: a click picks the whole loop or ring")


def unregister():
    del bpy.types.WindowManager.maximize_click_mode
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
