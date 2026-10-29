# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Max's Camera Map Per Pixel: an image projected onto the scene from a camera, as a material
setup.

A Texture Coordinate node with the camera as its object gives each shading point in the camera's
space; the "MX Camera Map Per Pixel" node group turns that into the image coordinate the camera
sees there (perspective divide, focal length, sensor width, frame aspect and lens shift). Drivers
keep the group's lens inputs in sync with the camera and the render resolution. Everything is
plain shader nodes and drivers, so stock Blender renders it the same.
"""

import bpy
from bpy.props import StringProperty
from bpy.types import Operator

GROUP_NAME = "MX Camera Map Per Pixel"
VERSION = 1


def _socket(tree, name, in_out, socket_type, default=None):
    socket = tree.interface.new_socket(name, in_out=in_out, socket_type=socket_type)
    if default is not None:
        socket.default_value = default
    return socket


def ensure_group():
    group = bpy.data.node_groups.get(GROUP_NAME)
    if group is not None and group.get("maximize_version") == VERSION:
        return group
    if group is not None:
        group.name = GROUP_NAME + " (old)"
    group = bpy.data.node_groups.new(GROUP_NAME, 'ShaderNodeTree')
    group["maximize_version"] = VERSION
    _socket(group, "Vector", 'INPUT', 'NodeSocketVector')
    _socket(group, "Focal Length", 'INPUT', 'NodeSocketFloat', 50.0)
    _socket(group, "Sensor Width", 'INPUT', 'NodeSocketFloat', 36.0)
    _socket(group, "Aspect", 'INPUT', 'NodeSocketFloat', 16.0 / 9.0)
    _socket(group, "Shift X", 'INPUT', 'NodeSocketFloat', 0.0)
    _socket(group, "Shift Y", 'INPUT', 'NodeSocketFloat', 0.0)
    _socket(group, "UV", 'OUTPUT', 'NodeSocketVector')
    _socket(group, "In Front", 'OUTPUT', 'NodeSocketFloat')
    nodes, links = group.nodes, group.links
    gin = nodes.new('NodeGroupInput')
    gout = nodes.new('NodeGroupOutput')
    x = [-600]

    def node(idname, inputs=(), **props):
        n = nodes.new(idname)
        n.location = (x[0], 0)
        x[0] += 160
        for key, value in props.items():
            setattr(n, key, value)
        for i, value in enumerate(inputs):
            if value is None:
                continue
            if isinstance(value, bpy.types.NodeSocket):
                links.new(value, n.inputs[i])
            else:
                n.inputs[i].default_value = value
        return n

    def math(op, a, b=None):
        return node('ShaderNodeMath', (a, b), operation=op).outputs[0]

    xyz = node('ShaderNodeSeparateXYZ', (gin.outputs["Vector"],)).outputs
    # The camera looks down its -Z: divide by the distance in front of it.
    depth = math('MULTIPLY', xyz[2], -1.0)
    scale = math('DIVIDE', gin.outputs["Focal Length"], gin.outputs["Sensor Width"])
    # Lens shift moves the frame, in frame widths: the image moves the other way.
    u = math('SUBTRACT', math('ADD', math('MULTIPLY', math('DIVIDE', xyz[0], depth), scale), 0.5),
             gin.outputs["Shift X"])
    v_scale = math('MULTIPLY', scale, gin.outputs["Aspect"])
    v = math('SUBTRACT', math('ADD', math('MULTIPLY', math('DIVIDE', xyz[1], depth), v_scale), 0.5),
             math('MULTIPLY', gin.outputs["Shift Y"], gin.outputs["Aspect"]))
    uv = node('ShaderNodeCombineXYZ', (u, v, 0.0)).outputs[0]
    links.new(uv, gout.inputs["UV"])
    links.new(math('GREATER_THAN', depth, 0.0), gout.inputs["In Front"])
    gout.location = (x[0], 0)
    return group


def _drive(tree, node, socket, expression, variables):
    """Drive `node`'s input `socket` with `expression` over (name, id type, id, data path)."""
    fcurve = tree.driver_add('nodes["{:s}"].inputs["{:s}"].default_value'.format(node.name, socket))
    driver = fcurve.driver
    driver.type = 'SCRIPTED'
    driver.expression = expression
    for name, id_type, ident, path in variables:
        var = driver.variables.new()
        var.name = name
        var.type = 'SINGLE_PROP'
        var.targets[0].id_type = id_type
        var.targets[0].id = ident
        var.targets[0].data_path = path


def add_camera_map(material, camera, scene, image=None):
    """Add the Camera Map Per Pixel nodes to `material`: an Image Texture projected from `camera`,
    linked to the Base Color when the material has a Principled BSDF. Returns the image node."""
    material.use_nodes = True
    tree = material.node_tree
    coords = tree.nodes.new('ShaderNodeTexCoord')
    coords.object = camera
    coords.location = (-900, 300)
    mapping = tree.nodes.new('ShaderNodeGroup')
    mapping.node_tree = ensure_group()
    mapping.name = mapping.label = "Camera Map Per Pixel"
    mapping.location = (-700, 300)
    tree.links.new(coords.outputs["Object"], mapping.inputs["Vector"])
    texture = tree.nodes.new('ShaderNodeTexImage')
    texture.location = (-480, 300)
    texture.extension = 'CLIP'
    texture.image = image
    tree.links.new(mapping.outputs["UV"], texture.inputs["Vector"])
    cam = camera.data
    _drive(tree, mapping, "Focal Length", "lens", [("lens", 'CAMERA', cam, "lens")])
    _drive(tree, mapping, "Sensor Width", "sensor", [("sensor", 'CAMERA', cam, "sensor_width")])
    _drive(tree, mapping, "Shift X", "shift", [("shift", 'CAMERA', cam, "shift_x")])
    _drive(tree, mapping, "Shift Y", "shift", [("shift", 'CAMERA', cam, "shift_y")])
    _drive(tree, mapping, "Aspect", "(x * px) / (y * py)", [
        ("x", 'SCENE', scene, "render.resolution_x"), ("y", 'SCENE', scene, "render.resolution_y"),
        ("px", 'SCENE', scene, "render.pixel_aspect_x"), ("py", 'SCENE', scene, "render.pixel_aspect_y")])
    bsdf = next((n for n in tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if bsdf is not None and not bsdf.inputs["Base Color"].is_linked:
        tree.links.new(texture.outputs["Color"], bsdf.inputs["Base Color"])
    return texture


class MAXIMIZE_OT_camera_map_per_pixel(Operator):
    """Project an image onto the active object's material from a camera (Max's Camera Map Per
    Pixel)"""
    bl_idname = "maximize.camera_map_per_pixel"
    bl_label = "Camera Map Per Pixel"
    bl_options = {'REGISTER', 'UNDO'}

    camera: StringProperty(name="Camera", description="The camera to project from (the scene camera if empty)")
    filepath: StringProperty(subtype='FILE_PATH', options={'SKIP_SAVE'})

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj is not None and obj.type in {'MESH', 'CURVE', 'FONT', 'SURFACE', 'META'}

    def invoke(self, context, _event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        scene = context.scene
        camera = scene.objects.get(self.camera) if self.camera else scene.camera
        if camera is None or camera.type != 'CAMERA':
            self.report({'WARNING'}, "No camera to project from")
            return {'CANCELLED'}
        obj = context.object
        material = obj.active_material
        if material is None:
            material = bpy.data.materials.new(obj.name + " Camera Map")
            obj.data.materials.append(material)
        image = bpy.data.images.load(self.filepath, check_existing=True) if self.filepath else None
        add_camera_map(material, camera, scene, image)
        return {'FINISHED'}


def _draw_menu(self, _context):
    self.layout.operator(MAXIMIZE_OT_camera_map_per_pixel.bl_idname)


classes = (MAXIMIZE_OT_camera_map_per_pixel,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    menu = getattr(bpy.types, "NODE_MT_category_shader_texture", None)
    if menu is not None:
        menu.append(_draw_menu)


def unregister():
    menu = getattr(bpy.types, "NODE_MT_category_shader_texture", None)
    if menu is not None:
        menu.remove(_draw_menu)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
