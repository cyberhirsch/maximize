# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Max's Compound Objects. BlobMesh: metaball blobs on the vertices of other objects, merged into
one mesh, as a Geometry Nodes group like the primitives in `primitives.py`.

Max's BlobMesh parameters (Size, Tension, Evaluation Coarseness Render / Viewport, Off in
Viewport, Blob Objects) plus what Max lacks (from tyFlow's tyMesher): Mesh Volume (mesh the
objects' volume instead of blobs on their vertices), Resample Faces, Variation, Smoothing and
Adaptive.
"""

import bpy
from bpy.types import Operator

DIST = 'NodeSocketFloat'
INT = 'NodeSocketInt'
BOOL = 'NodeSocketBool'
FLOAT = 'NodeSocketFloat'

COMPOUND_KINDS = (
    ('BLOBMESH', "BlobMesh", "", 'META_BALL', 60),
)
COMPOUND_OBJECTS = ('BLOBMESH',)
BLOB_OBJECTS = "Blob Objects"


def build_blobmesh(b):
    objects = b.input(BLOB_OBJECTS, 'NodeSocketCollection')
    size = b.input("Size", DIST, 0.2, 0.001, subtype='DISTANCE')
    tension = b.input("Tension", FLOAT, 1.0, 0.0, 1.0)
    render = b.input("Render Coarseness", DIST, 0.03, 0.001, subtype='DISTANCE')
    viewport = b.input("Viewport Coarseness", DIST, 0.06, 0.001, subtype='DISTANCE')
    off_viewport = b.input("Off in Viewport", BOOL, False)
    volume = b.input("Mesh Volume", BOOL, False)
    resample = b.input("Resample Faces", FLOAT, 0.0, 0.0)
    variation = b.input("Variation %", FLOAT, 0.0, 0.0, 100.0)
    seed = b.input("Seed", INT, 0)
    smoothing = b.input("Smoothing", INT, 0, 0, 10)
    adaptive = b.input("Adaptive", FLOAT, 0.0, 0.0, 1.0)
    descriptions = {
        "Tension": "Lower values blend nearby blobs into each other",
        "Render Coarseness": "Voxel size at render time; smaller is finer",
        "Viewport Coarseness": "Voxel size in the viewport",
        "Mesh Volume": "Mesh the objects' volume instead of blobs on their vertices",
        "Resample Faces": "Extra blobs per square unit spread over the faces, for sparse meshes",
        "Variation %": "Random variation of the blob sizes",
        "Smoothing": "Smooths the surface between blobs",
        "Adaptive": "Fewer polygons on flat areas",
    }
    for name, text in descriptions.items():
        b.tree.interface.items_tree[name].description = text

    # The blob objects where they are in the world, relative to the BlobMesh.
    info = b.node('GeometryNodeCollectionInfo', {"Collection": objects}, transform_space='RELATIVE')
    mesh = b.node('GeometryNodeRealizeInstances', {"Geometry": info.outputs[0]}).outputs[0]
    is_viewport = b.node('GeometryNodeIsViewport').outputs[0]
    voxel = b.node('GeometryNodeSwitch', {"Switch": is_viewport, "False": render, "True": viewport},
                   input_type='FLOAT').outputs[0]
    # Blobs on the vertices, and on points spread over the faces.
    verts = b.node('GeometryNodeMeshToPoints', {"Mesh": mesh}, mode='VERTICES').outputs[0]
    spread = b.node('GeometryNodeDistributePointsOnFaces', {
        "Mesh": mesh, "Density": resample, "Seed": seed}).outputs[0]
    points = b.node('GeometryNodeJoinGeometry')
    for geo in (verts, spread):
        b.set(points.inputs[0], geo)
    # Max's Size is the blob's diameter.
    random = b.node('FunctionNodeRandomValue', {"Min": 0.0, "Max": 1.0, "Seed": seed},
                    data_type='FLOAT').outputs["Value"]
    shrink = b.math('SUBTRACT', 1.0, b.math('MULTIPLY', random, b.math('DIVIDE', variation, 100.0)))
    radius = b.math('MULTIPLY', b.math('MULTIPLY', size, 0.5), shrink)
    blobs = b.node('GeometryNodePointsToSDFGrid', {
        "Points": points.outputs[0], "Radius": radius, "Voxel Size": voxel}).outputs[0]
    # Tension: lower values fillet the creases between blobs.
    blend = b.math('ROUND', b.math('MULTIPLY', b.math('SUBTRACT', 1.0, tension), 10.0))
    blobs = b.node('GeometryNodeSDFGridFillet', {"Grid": blobs, "Iterations": blend}).outputs[0]
    solid = b.node('GeometryNodeMeshToSDFGrid', {"Mesh": mesh, "Voxel Size": voxel}).outputs[0]
    meshes = []
    for grid in (blobs, solid):
        grid = b.node('GeometryNodeSDFGridMean', {"Grid": grid, "Width": 1, "Iterations": smoothing}).outputs[0]
        meshes.append(b.node('GeometryNodeGridToMesh', {"Grid": grid, "Threshold": 0.0, "Adaptivity": adaptive}).outputs[0])
    result = b.node('GeometryNodeSwitch', {"Switch": volume, "False": meshes[0], "True": meshes[1]},
                    input_type='GEOMETRY').outputs[0]
    result = b.node('GeometryNodeSetShadeSmooth', {"Mesh": result}).outputs[0]
    hidden = b.node('FunctionNodeBooleanMath', {0: off_viewport, 1: is_viewport}, operation='AND').outputs[0]
    return b.node('GeometryNodeSwitch', {"Switch": hidden, "False": result}, input_type='GEOMETRY').outputs[0]


BUILDERS = {
    'BLOBMESH': build_blobmesh,
}


def blob_collection(obj):
    """The collection holding a BlobMesh's Blob Objects, made on first use."""
    from .nodes import modifier_input
    from .primitives import primitive_modifier
    mod = primitive_modifier(obj)
    entry = modifier_input(mod, BLOB_OBJECTS)
    if entry.value is None:
        entry.value = bpy.data.collections.new(obj.name + " " + BLOB_OBJECTS)
    return entry.value


def is_blobmesh(obj):
    from .primitives import primitive_modifier
    mod = primitive_modifier(obj)
    return mod is not None and mod.node_group.get("maximize_kind") == 'BLOBMESH'


def add_blob_objects(blobmesh, objects):
    """Add objects to a BlobMesh's Blob Objects, as Max's Add button does; returns how many."""
    collection = blob_collection(blobmesh)
    added = 0
    for obj in objects:
        if obj is blobmesh or obj.type != 'MESH' or obj.name in collection.objects:
            continue
        collection.objects.link(obj)
        added += 1
    blobmesh.update_tag()
    return added


class MAXIMIZE_OT_blob_objects_add(Operator):
    """Add the other selected objects to the BlobMesh's Blob Objects"""
    bl_idname = "maximize.blob_objects_add"
    bl_label = "Add"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return is_blobmesh(context.active_object)

    def execute(self, context):
        added = add_blob_objects(context.active_object, context.selected_objects)
        self.report({'INFO'}, "{:d} added".format(added))
        return {'FINISHED'}


class MAXIMIZE_OT_blob_objects_remove(Operator):
    """Remove an object from the BlobMesh's Blob Objects"""
    bl_idname = "maximize.blob_objects_remove"
    bl_label = "Remove"
    bl_options = {'REGISTER', 'UNDO'}

    name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return is_blobmesh(context.active_object)

    def execute(self, context):
        collection = blob_collection(context.active_object)
        obj = collection.objects.get(self.name)
        if obj is None:
            return {'CANCELLED'}
        collection.objects.unlink(obj)
        context.active_object.update_tag()
        return {'FINISHED'}


def draw_blob_objects(layout, obj):
    """Max's Blob Objects list with Add / Remove."""
    from .nodes import modifier_input
    from .primitives import primitive_modifier
    box = layout.box()
    box.label(text=BLOB_OBJECTS)
    collection = modifier_input(primitive_modifier(obj), BLOB_OBJECTS).value
    for member in (collection.objects if collection is not None else ()):
        row = box.row(align=True)
        row.label(text=member.name, icon='OBJECT_DATA')
        row.operator("maximize.blob_objects_remove", text="", icon='X').name = member.name
    box.operator("maximize.blob_objects_add", text="Add Selected", icon='ADD')


classes = (
    MAXIMIZE_OT_blob_objects_add,
    MAXIMIZE_OT_blob_objects_remove,
)
