# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Smoothing groups, as in Max: each polygon belongs to some of 32 groups; an edge is smooth where
the polygons on both sides share a group, and hard otherwise.

Stored as the integer face attribute `smoothing_groups` (a bit mask) and turned into Blender's
sharp edges and flat faces whenever the groups change, so rendering, exporting (FBX writes the
sharp edges, which Max reads back as smoothing) and stock Blender all see the result.
"""

import math

import bmesh
import bpy
from bpy.props import FloatProperty, IntProperty
from bpy.types import Operator, Panel

ATTR = "smoothing_groups"


def _layer(bm, create=True):
    layer = bm.faces.layers.int.get(ATTR)
    if layer is None and create:
        layer = bm.faces.layers.int.new(ATTR)
    return layer


def apply_groups(bm, layer):
    """Sharp edges where neighbors share no group; faces without groups are flat."""
    for e in bm.edges:
        faces = e.link_faces
        if len(faces) != 2:
            e.smooth = True
            continue
        a, b = faces[0][layer], faces[1][layer]
        e.smooth = bool(a & b)
    for f in bm.faces:
        f.smooth = f[layer] != 0


def _edit_meshes(context):
    for obj in context.objects_in_mode_unique_data:
        if obj.type == 'MESH':
            yield obj, bmesh.from_edit_mesh(obj.data)


def _update(obj, bm):
    bmesh.update_edit_mesh(obj.data, loop_triangles=True, destructive=False)


class MAXIMIZE_OT_smoothing_group(Operator):
    """Toggle a smoothing group on the selected polygons (Shift: clear the others first)"""
    bl_idname = "maximize.smoothing_group"
    bl_label = "Smoothing Group"
    bl_options = {'REGISTER', 'UNDO'}

    group: IntProperty(name="Group", min=1, max=32, default=1)

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def invoke(self, context, event):
        self.exclusive = event.shift
        return self.execute(context)

    def execute(self, context):
        bit = 1 << (self.group - 1)
        exclusive = getattr(self, "exclusive", False)
        for obj, bm in _edit_meshes(context):
            layer = _layer(bm)
            selected = [f for f in bm.faces if f.select]
            if not selected:
                continue
            on = not all(f[layer] & bit for f in selected)
            for f in selected:
                value = 0 if exclusive else f[layer]
                f[layer] = _signed((value | bit) if on else (value & ~bit))
            apply_groups(bm, layer)
            _update(obj, bm)
        return {'FINISHED'}


def _signed(value):
    """Group 32 is the sign bit of the 32-bit attribute."""
    value &= 0xFFFFFFFF
    return value - (1 << 32) if value & 0x80000000 else value


class MAXIMIZE_OT_smoothing_clear(Operator):
    """Clear All: remove the selected polygons from every smoothing group (faceted)"""
    bl_idname = "maximize.smoothing_clear"
    bl_label = "Clear All"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        for obj, bm in _edit_meshes(context):
            layer = _layer(bm)
            for f in bm.faces:
                if f.select:
                    f[layer] = 0
            apply_groups(bm, layer)
            _update(obj, bm)
        return {'FINISHED'}


class MAXIMIZE_OT_smoothing_select(Operator):
    """Select By SG: select the polygons in a smoothing group"""
    bl_idname = "maximize.smoothing_select"
    bl_label = "Select By SG"
    bl_options = {'REGISTER', 'UNDO'}

    group: IntProperty(name="Group", min=1, max=32, default=1)

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        bit = 1 << (self.group - 1)
        for obj, bm in _edit_meshes(context):
            layer = _layer(bm)
            for f in bm.faces:
                if not f.hide and f[layer] & bit:
                    f.select_set(True)
            bm.select_flush_mode()
            _update(obj, bm)
        return {'FINISHED'}


def _regions(faces, connected):
    """Flood fill: groups of faces joined through edges where `connected(edge)`."""
    seen = set()
    regions = []
    for f in faces:
        if f in seen:
            continue
        region = [f]
        seen.add(f)
        stack = [f]
        while stack:
            face = stack.pop()
            for e in face.edges:
                if not connected(e):
                    continue
                for other in e.link_faces:
                    if other not in seen and other in faces:
                        seen.add(other)
                        region.append(other)
                        stack.append(other)
        regions.append(region)
    return regions


def _assign_regions(faces, layer, connected):
    """One group per region; neighboring regions get different groups (greedy coloring)."""
    region_of = {}
    regions = _regions(faces, connected)
    for i, region in enumerate(regions):
        for f in region:
            region_of[f] = i
    color = {}
    for i, region in enumerate(regions):
        used = set()
        for f in region:
            for e in f.edges:
                for other in e.link_faces:
                    j = region_of.get(other)
                    if j is not None and j != i and j in color:
                        used.add(color[j])
        c = next(c for c in range(32) if c not in used) if len(used) < 32 else 0
        color[i] = c
        for f in region:
            f[layer] = _signed(1 << c)


class MAXIMIZE_OT_smoothing_auto(Operator):
    """Auto Smooth: put the selected polygons into smoothing groups by the angle between them"""
    bl_idname = "maximize.smoothing_auto"
    bl_label = "Auto Smooth"
    bl_options = {'REGISTER', 'UNDO'}

    angle: FloatProperty(name="Angle", default=0.785398, min=0.0, max=3.14159, subtype='ANGLE')

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        for obj, bm in _edit_meshes(context):
            layer = _layer(bm)
            faces = {f for f in bm.faces if f.select} or set(bm.faces)

            def connected(e):
                lf = e.link_faces
                return len(lf) == 2 and lf[0].normal.angle(lf[1].normal, 0.0) <= self.angle

            _assign_regions(faces, layer, connected)
            apply_groups(bm, layer)
            _update(obj, bm)
        return {'FINISHED'}


class MAXIMIZE_OT_smoothing_from_sharp(Operator):
    """Smoothing groups from the mesh's sharp edges (for meshes imported from FBX or made in Blender)"""
    bl_idname = "maximize.smoothing_from_sharp"
    bl_label = "Groups From Sharp Edges"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        for obj, bm in _edit_meshes(context):
            layer = _layer(bm)
            smooth_faces = {f for f in bm.faces if f.smooth}
            _assign_regions(smooth_faces, layer, lambda e: e.smooth)
            for f in bm.faces:
                if not f.smooth:
                    f[layer] = 0
            apply_groups(bm, layer)
            _update(obj, bm)
        return {'FINISHED'}


def selection_groups(context):
    """Bit masks: (groups all selected polygons have, groups some have)."""
    all_mask, any_mask, found = 0xFFFFFFFF, 0, False
    for obj in context.objects_in_mode_unique_data:
        if obj.type != 'MESH':
            continue
        bm = bmesh.from_edit_mesh(obj.data)
        layer = _layer(bm, create=False)
        for f in bm.faces:
            if f.select:
                value = (f[layer] & 0xFFFFFFFF) if layer is not None else 0
                all_mask &= value
                any_mask |= value
                found = True
    return (all_mask if found else 0), any_mask


class MAXIMIZE_PT_smoothing(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Max"
    bl_label = "Polygon: Smoothing Groups"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        # Moritz has no Max sidebar tab: this is in the Command Panel there.
        if hasattr(bpy.types, "PROPERTIES_PT_create"):
            return False
        return context.mode == 'EDIT_MESH' and context.tool_settings.mesh_select_mode[2]

    def draw(self, context):
        draw_smoothing_groups(self.layout, context)


def draw_smoothing_groups(layout, context):
    """Max's Polygon: Smoothing Groups: the 32 groups, then Max's ribbon Smooth / Smooth 30 / Hard."""
    all_mask, any_mask = selection_groups(context)
    grid = layout.grid_flow(row_major=True, columns=8, even_columns=True, align=True)
    for group in range(1, 33):
        bit = 1 << (group - 1)
        depress = bool(all_mask & bit)
        text = str(group) if not (any_mask & bit and not depress) else str(group) + "·"
        grid.operator("maximize.smoothing_group", text=text, depress=depress).group = group
    row = layout.row(align=True)
    row.operator("maximize.smoothing_clear")
    row.operator("maximize.smoothing_auto")
    layout.operator("maximize.smoothing_from_sharp")
    # Max's ribbon: Smooth (one group across), Smooth 30 (Auto Smooth at 30 degrees), Hard (none).
    from .mx_icons import mx_icon
    row = layout.row(align=True)
    row.operator("maximize.smoothing_auto", text="Smooth", icon=mx_icon('MX_PR_SMOOTH')).angle = math.pi
    row.operator("maximize.smoothing_auto", text="Smooth 30",
                 icon=mx_icon('MX_PR_SMOOTH_30')).angle = math.radians(30.0)
    row.operator("maximize.smoothing_clear", text="Hard", icon=mx_icon('MX_PR_HARD'))


classes = (
    MAXIMIZE_OT_smoothing_group,
    MAXIMIZE_OT_smoothing_clear,
    MAXIMIZE_OT_smoothing_select,
    MAXIMIZE_OT_smoothing_auto,
    MAXIMIZE_OT_smoothing_from_sharp,
    MAXIMIZE_PT_smoothing,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
