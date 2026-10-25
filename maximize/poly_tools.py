# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Edit Poly tools Blender has under another shape: Material IDs (Set ID, Select ID with Clear
Selection), Make Planar X / Y / Z and Create Shape (edges to a spline).

Max's material IDs are Blender's material slots, counted from 1. Nothing new is stored.
"""

import bmesh
import bpy
from bpy.props import BoolProperty, EnumProperty, IntProperty
from bpy.types import Operator, Panel


def _edit_meshes(context):
    return [o for o in context.objects_in_mode_unique_data if o.type == 'MESH']


class _EditMesh:
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'


class MAXIMIZE_OT_set_material_id(_EditMesh, Operator):
    """Max's Set ID: give the selected polygons a material ID (material slot, from 1)"""
    bl_idname = "maximize.set_material_id"
    bl_label = "Set ID"

    material_id: IntProperty(name="ID", default=1, min=1, max=32767)

    def execute(self, context):
        count = 0
        for obj in _edit_meshes(context):
            bm = bmesh.from_edit_mesh(obj.data)
            for face in bm.faces:
                if face.select:
                    face.material_index = self.material_id - 1
                    count += 1
            bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)
        if not count:
            self.report({'WARNING'}, "Select polygons first")
            return {'CANCELLED'}
        return {'FINISHED'}


class MAXIMIZE_OT_select_material_id(_EditMesh, Operator):
    """Max's Select ID: select the polygons with a material ID"""
    bl_idname = "maximize.select_material_id"
    bl_label = "Select ID"

    material_id: IntProperty(name="ID", default=1, min=1, max=32767)
    clear: BoolProperty(name="Clear Selection", default=True,
                        description="Deselect everything else first (off: add to the selection)")

    def execute(self, context):
        for obj in _edit_meshes(context):
            bm = bmesh.from_edit_mesh(obj.data)
            if self.clear:
                for seq in (bm.verts, bm.edges, bm.faces):
                    for elem in seq:
                        elem.select = False
            for face in bm.faces:
                if face.material_index == self.material_id - 1:
                    face.select = True
            bm.select_flush_mode()
            bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)
        return {'FINISHED'}


class MAXIMIZE_OT_make_planar_axis(_EditMesh, Operator):
    """Max's Make Planar X / Y / Z: flatten the selection along an object axis, about its center"""
    bl_idname = "maximize.make_planar_axis"
    bl_label = "Make Planar Axis"

    axis: EnumProperty(name="Axis", items=(('X', "X", ""), ('Y', "Y", ""), ('Z', "Z", "")))

    def execute(self, context):
        settings = context.scene.tool_settings
        pivot = settings.transform_pivot_point
        settings.transform_pivot_point = 'MEDIAN_POINT'
        try:
            i = "XYZ".index(self.axis)
            value = [1.0, 1.0, 1.0]
            value[i] = 0.0
            bpy.ops.transform.resize(value=value, orient_type='LOCAL',
                                     constraint_axis=tuple(k == i for k in range(3)))
        finally:
            settings.transform_pivot_point = pivot
        return {'FINISHED'}


class MAXIMIZE_OT_create_shape(_EditMesh, Operator):
    """Max's Create Shape: make a spline object from the selected edges"""
    bl_idname = "maximize.create_shape"
    bl_label = "Create Shape"

    smooth: BoolProperty(name="Smooth", description="Smooth vertices instead of Linear (corners)")

    def execute(self, context):
        source = context.edit_object
        bm = bmesh.from_edit_mesh(source.data)
        edges = [e for e in bm.edges if e.select]
        if not edges:
            self.report({'WARNING'}, "Select edges first")
            return {'CANCELLED'}
        index = {}
        verts = []
        for e in edges:
            for v in e.verts:
                if v.index not in index:
                    index[v.index] = len(verts)
                    verts.append(v.co.copy())
        mesh = bpy.data.meshes.new(source.name + " Shape")
        mesh.from_pydata(verts, [(index[e.verts[0].index], index[e.verts[1].index]) for e in edges], [])
        shape = bpy.data.objects.new(mesh.name, mesh)
        shape.matrix_world = source.matrix_world
        for coll in source.users_collection:
            coll.objects.link(shape)
        bpy.ops.object.mode_set(mode='OBJECT')
        try:
            with context.temp_override(active_object=shape, object=shape, selected_objects=[shape],
                                       selected_editable_objects=[shape]):
                bpy.ops.object.convert(target='CURVE')
            curve = shape.data
            for spline in curve.splines:
                if spline.type != 'BEZIER':
                    spline.type = 'BEZIER'
                kind = 'AUTO' if self.smooth else 'VECTOR'
                for bp in spline.bezier_points:
                    bp.handle_left_type = bp.handle_right_type = kind
        finally:
            bpy.ops.object.mode_set(mode='EDIT')
        self.report({'INFO'}, "Created {:s}".format(shape.name))
        return {'FINISHED'}


class MAXIMIZE_PT_material_ids(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Max"
    bl_label = "Polygon: Material IDs"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH' and context.tool_settings.mesh_select_mode[2]

    def draw(self, context):
        draw_material_ids(self.layout, context)


def draw_material_ids(layout, context):
    wm = context.window_manager
    row = layout.row(align=True)
    row.operator("maximize.set_material_id").material_id = wm.maximize_material_id
    row.prop(wm, "maximize_material_id", text="")
    row = layout.row(align=True)
    op = row.operator("maximize.select_material_id")
    op.material_id = wm.maximize_material_id
    op.clear = wm.maximize_material_clear
    row.prop(wm, "maximize_material_clear", text="Clear Selection")


classes = (
    MAXIMIZE_OT_set_material_id,
    MAXIMIZE_OT_select_material_id,
    MAXIMIZE_OT_make_planar_axis,
    MAXIMIZE_OT_create_shape,
    MAXIMIZE_PT_material_ids,
)


def register():
    bpy.types.WindowManager.maximize_material_id = IntProperty(name="ID", default=1, min=1, max=32767)
    bpy.types.WindowManager.maximize_material_clear = BoolProperty(name="Clear Selection", default=True)
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.WindowManager.maximize_material_clear
    del bpy.types.WindowManager.maximize_material_id
