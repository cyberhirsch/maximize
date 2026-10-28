# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Small helper for building Geometry Nodes groups from Python."""

import math

import bpy

# Bump when a group's node layout changes, so files get the new version of the group.
VERSION = 5


def modifier_input(mod, name):
    """The input of a Geometry Nodes modifier with that socket name; read and write its `value`."""
    for item in mod.node_group.interface.items_tree:
        if item.item_type == 'SOCKET' and item.in_out == 'INPUT' and item.name == name:
            return getattr(mod.properties.inputs, item.identifier)
    raise KeyError(name)


def draw_modifier_inputs(layout, mod, names=None):
    col = layout.column(align=True)
    for item in mod.node_group.interface.items_tree:
        # Geometry and object lists (BlobMesh's Blob Objects) have their own UI.
        if item.item_type != 'SOCKET' or item.in_out != 'INPUT' or                 item.socket_type in {'NodeSocketGeometry', 'NodeSocketCollection'}:
            continue
        if names is None or item.name in names:
            col.prop(getattr(mod.properties.inputs, item.identifier), "value", text=item.name)


def find_group(name):
    group = bpy.data.node_groups.get(name)
    if group is not None and group.get("maximize_version") == VERSION:
        return group
    if group is not None:
        # Made by an earlier version: what uses it keeps it, and the name is free for the new one.
        group.name = "{} v{}".format(name, group.get("maximize_version", 0))
    return None


class GroupBuilder:
    def __init__(self, name, kind):
        self.tree = bpy.data.node_groups.new(name, 'GeometryNodeTree')
        self.tree["maximize_version"] = VERSION
        self.tree["maximize_kind"] = kind
        self.nodes = self.tree.nodes
        self.group_in = self.nodes.new('NodeGroupInput')
        self.group_out = self.nodes.new('NodeGroupOutput')
        self.group_in.location = (-900, 0)
        self.group_out.location = (900, 0)
        self._x = -600

    def input(self, name, socket_type, default=None, min_value=None, max_value=None, subtype=None):
        """Add a group input; returns the matching output socket of the Group Input node."""
        socket = self.tree.interface.new_socket(name, in_out='INPUT', socket_type=socket_type)
        if subtype is not None:
            socket.subtype = subtype
        if default is not None:
            socket.default_value = default
        if min_value is not None:
            socket.min_value = min_value
        if max_value is not None:
            socket.max_value = max_value
        return self.group_in.outputs[socket.identifier]

    def output(self, name="Geometry", socket_type='NodeSocketGeometry'):
        socket = self.tree.interface.new_socket(name, in_out='OUTPUT', socket_type=socket_type)
        return self.group_out.inputs[socket.identifier]

    def node(self, idname, inputs=None, **props):
        """Add a node; `inputs` maps socket names or indices to values or sockets."""
        node = self.nodes.new(idname)
        node.location = (self._x, 0)
        self._x += 40
        for key, value in props.items():
            if hasattr(node, key):
                setattr(node, key, value)
            else:
                # Newer Blender versions turned some node options into menu sockets.
                node.inputs[key.replace("_", " ").title()].default_value = value.replace("_", " ").title()
        for key, value in (inputs or {}).items():
            self.set(node.inputs[key], value)
        return node

    def set(self, socket, value):
        if isinstance(value, bpy.types.NodeSocket):
            self.tree.links.new(value, socket)
        else:
            socket.default_value = value

    def math(self, operation, a, b=None):
        inputs = {0: a}
        if b is not None:
            inputs[1] = b
        return self.node('ShaderNodeMath', inputs, operation=operation).outputs[0]

    def vmath(self, operation, a, b=None):
        inputs = {0: a}
        if b is not None:
            inputs[1] = b
        node = self.node('ShaderNodeVectorMath', inputs, operation=operation)
        return node.outputs['Value' if operation in {'LENGTH', 'DOT_PRODUCT', 'DISTANCE'} else 'Vector']

    def combine(self, x=0.0, y=0.0, z=0.0):
        return self.node('ShaderNodeCombineXYZ', {"X": x, "Y": y, "Z": z}).outputs[0]

    def separate(self, vector):
        return self.node('ShaderNodeSeparateXYZ', {"Vector": vector}).outputs

    def on_faces(self, value, data_type='FLOAT'):
        """The value averaged over each face."""
        return self.node('GeometryNodeFieldOnDomain', {"Value": value}, domain='FACE', data_type=data_type).outputs[0]

    def seam_angle(self, y, x):
        """Angle of (x, y) as 0..1. Each corner is unwrapped relative to its face's center, so faces
        that cross the seam don't stretch across the whole map."""
        def angle(yy, xx):
            return self.math('ADD', self.math('DIVIDE', self.math('ARCTAN2', yy, xx), 2.0 * math.pi), 0.5)

        center = angle(self.on_faces(y), self.on_faces(x))
        delta = self.math('SUBTRACT', angle(y, x), center)
        return self.math('ADD', center, self.math('SUBTRACT', delta, self.math('ROUND', delta)))

    def store_uv(self, geometry, uv, name="UVMap"):
        return self.node('GeometryNodeStoreNamedAttribute',
                         {"Geometry": geometry, "Name": name, "Value": uv},
                         data_type='FLOAT2', domain='CORNER').outputs[0]
