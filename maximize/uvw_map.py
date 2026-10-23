# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""UVW Map modifier: Planar, Box, Cylindrical and Spherical projection through a gizmo.

The modifier is a Geometry Nodes group. The gizmo is a cube empty parented to the object: move,
rotate and scale it to place the projection, as with Max's UVW Map gizmo. With Real-World Map Size
on, Planar and Box mapping use the real width and length instead of the gizmo size.
"""

import math

import bpy
from bpy.props import EnumProperty
from bpy.types import Operator
from mathutils import Vector

from .nodes import GroupBuilder, find_group, modifier_input

GROUP_NAME = "MX UVW Map"
MODIFIER_NAME = "UVW Map"
MAPPINGS = ("Planar", "Box", "Cylindrical", "Spherical")


def _build(b):
    geometry = b.input("Geometry", 'NodeSocketGeometry')
    mapping = b.input("Mapping", 'NodeSocketMenu')
    gizmo = b.input("Gizmo", 'NodeSocketObject')
    u_tile = b.input("U Tile", 'NodeSocketFloat', 1.0)
    v_tile = b.input("V Tile", 'NodeSocketFloat', 1.0)
    real = b.input("Real-World Map Size", 'NodeSocketBool', False)
    real_w = b.input("Real Width", 'NodeSocketFloat', 1.0, 0.0001, subtype='DISTANCE')
    real_l = b.input("Real Length", 'NodeSocketFloat', 1.0, 0.0001, subtype='DISTANCE')
    channel = b.input("UV Map", 'NodeSocketString', "UVMap")

    # Positions and normals in gizmo space; the gizmo cube spans -1..1.
    info = b.node('GeometryNodeObjectInfo', {"Object": gizmo}, transform_space='RELATIVE')
    inverse = b.node('FunctionNodeInvertMatrix', {"Matrix": info.outputs["Transform"]}).outputs["Matrix"]
    position = b.node('GeometryNodeInputPosition').outputs[0]
    local = b.node('FunctionNodeTransformPoint', {"Vector": position, "Transform": inverse}).outputs[0]
    scaled = b.vmath('MULTIPLY', local, info.outputs["Scale"])
    q = b.node('GeometryNodeSwitch', {"Switch": real, "False": local, "True": scaled},
               input_type='VECTOR').outputs[0]
    qx, qy, qz = b.separate(q)

    normal = b.node('GeometryNodeInputNormal').outputs["Normal"]
    face_normal = b.node('GeometryNodeFieldOnDomain', {"Value": normal},
                         domain='FACE', data_type='FLOAT_VECTOR').outputs[0]
    n_local = b.node('FunctionNodeTransformDirection', {"Direction": face_normal, "Transform": inverse}).outputs[0]
    ax, ay, az = b.separate(b.vmath('ABSOLUTE', n_local))

    def compare_ge(a, c):
        return b.node('FunctionNodeCompare', {"A": a, "B": c},
                      data_type='FLOAT', operation='GREATER_EQUAL').outputs[0]

    x_major = b.node('FunctionNodeBooleanMath', {0: compare_ge(ax, ay), 1: compare_ge(ax, az)},
                     operation='AND').outputs[0]
    y_major = compare_ge(ay, az)

    def switch(cond, if_false, if_true):
        return b.node('GeometryNodeSwitch', {"Switch": cond, "False": if_false, "True": if_true},
                      input_type='VECTOR').outputs[0]

    planar_raw = b.combine(qx, qy)
    box_raw = switch(x_major, switch(y_major, b.combine(qx, qy), b.combine(qx, qz)), b.combine(qy, qz))

    size = b.combine(real_w, real_l, 1.0)

    def normalize(raw):
        unit = b.node('ShaderNodeVectorMath', {0: raw, 1: (0.5, 0.5, 0.5), 2: (0.5, 0.5, 0.5)},
                      operation='MULTIPLY_ADD').outputs[0]
        return switch(real, unit, b.vmath('DIVIDE', raw, size))

    # Angle around the gizmo's Z axis.
    lx, ly, lz = b.separate(local)
    u = b.seam_angle(ly, lx)

    cyl = b.combine(u, b.math('ADD', b.math('MULTIPLY', lz, 0.5), 0.5))
    radius = b.vmath('LENGTH', local)
    cos_polar = b.math('MINIMUM', b.math('MAXIMUM', b.math('DIVIDE', lz, radius), -1.0), 1.0)
    sph = b.combine(u, b.math('SUBTRACT', 1.0, b.math('DIVIDE', b.math('ARCCOSINE', cos_polar), math.pi)))

    menu = b.node('GeometryNodeMenuSwitch', data_type='VECTOR')
    menu.enum_items.clear()
    for name in MAPPINGS:
        menu.enum_items.new(name)
    b.set(menu.inputs["Menu"], mapping)
    b.set(menu.inputs["Planar"], normalize(planar_raw))
    b.set(menu.inputs["Box"], normalize(box_raw))
    b.set(menu.inputs["Cylindrical"], cyl)
    b.set(menu.inputs["Spherical"], sph)

    uv = b.vmath('MULTIPLY', menu.outputs["Output"], b.combine(u_tile, v_tile, 1.0))
    return b.store_uv(geometry, uv, name=channel)


def ensure_group():
    group = find_group(GROUP_NAME)
    if group is None:
        builder = GroupBuilder(GROUP_NAME, 'UVW_MAP')
        geometry_out = builder.output()
        builder.set(geometry_out, _build(builder))
        group = builder.tree
    return group


def uvw_modifier(obj):
    mod = obj.modifiers.get(MODIFIER_NAME) if obj is not None else None
    if mod is not None and mod.type == 'NODES' and mod.node_group is not None and \
            mod.node_group.get("maximize_kind") == 'UVW_MAP':
        return mod
    return None


class MAXIMIZE_OT_uvw_map(Operator):
    """Add a UVW Map modifier with a projection gizmo fitted to the object"""
    bl_idname = "maximize.uvw_map"
    bl_label = "UVW Map"
    bl_options = {'REGISTER', 'UNDO'}

    mapping: EnumProperty(name="Mapping", items=[(m.upper(), m, "") for m in MAPPINGS], default='BOX')

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return context.mode == 'OBJECT' and obj is not None and obj.type == 'MESH'

    def execute(self, context):
        obj = context.active_object
        depsgraph = context.evaluated_depsgraph_get()
        corners = [Vector(c) for c in obj.evaluated_get(depsgraph).bound_box]
        lo = Vector(min(c[i] for c in corners) for i in range(3))
        hi = Vector(max(c[i] for c in corners) for i in range(3))
        half = (hi - lo) * 0.5

        gizmo = bpy.data.objects.new(obj.name + " UVW Gizmo", None)
        gizmo.empty_display_type = 'CUBE'
        gizmo.empty_display_size = 1.0
        for coll in obj.users_collection:
            coll.objects.link(gizmo)
        gizmo.parent = obj
        gizmo.location = (lo + hi) * 0.5
        gizmo.scale = [max(h, 0.001) for h in half]
        gizmo.hide_render = True

        group = ensure_group()
        mod = obj.modifiers.new(MODIFIER_NAME, 'NODES')
        mod.node_group = group
        modifier_input(mod, "Gizmo").value = gizmo
        modifier_input(mod, "Mapping").value = self.mapping.title()
        modifier_input(mod, "Real Width").value = max(half.x * 2.0, 0.001)
        modifier_input(mod, "Real Length").value = max(half.y * 2.0, 0.001)
        obj.update_tag()
        return {'FINISHED'}


classes = (
    MAXIMIZE_OT_uvw_map,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
