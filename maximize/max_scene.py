# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Import a Max scene: File > Import > Max Scene (.mxscene).

.max files are a closed format, so Max writes the scene itself: `max_side/moritz_export.ms` (run
it in Max with Scripting > Run Script) saves a .mxscene file (JSON). This brings in:
- meshes as polygons with UV channel 1, material IDs (Multi/Sub-Object becomes one material slot
  per sub-material) and smoothing groups (as Maximize smoothing groups, see `smoothing.py`);
- the hierarchy and pivots (Max and Blender are both Z up, so transforms carry over as they are),
  scaled from Max's system unit to meters;
- layers as collections, hidden and frozen state, wire colors as object colors;
- cameras (field of view) and lights (as point, spot, area or sun with their color);
- materials converted from V-Ray, Corona, Physical and Standard (`max_materials.py`).
"""

import json
import math
import os

import bmesh
import bpy
from bpy.props import BoolProperty, StringProperty
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper
from mathutils import Matrix

from . import max_materials, smoothing

EXPORTER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "max_side", "moritz_export.ms")


def _matrix(rows, scale):
    """Max's row-vector transform (X, Y, Z axes, translation) as a Blender matrix."""
    m = Matrix(((rows[0][0], rows[1][0], rows[2][0], rows[3][0] * scale),
                (rows[0][1], rows[1][1], rows[2][1], rows[3][1] * scale),
                (rows[0][2], rows[1][2], rows[2][2], rows[3][2] * scale),
                (0.0, 0.0, 0.0, 1.0)))
    return m


def _meters_per_unit(data):
    per_cm = data.get("units_per_cm")
    if per_cm:
        return 0.01 / float(per_cm)
    # Older files: Max's default system unit is the inch.
    return 0.0254


def _mesh(name, md, scale, slot_of_id):
    me = bpy.data.meshes.new(name)
    verts = [(v[0] * scale, v[1] * scale, v[2] * scale) for v in md.get("verts", [])]
    faces = [tuple(f) for f in md.get("faces", [])]
    me.from_pydata(verts, [], faces)
    nf = len(me.polygons)
    if md.get("uv_verts") and md.get("uv_faces") and len(md["uv_faces"]) == nf:
        uv = me.uv_layers.new(name="UVMap")
        uv_verts = md["uv_verts"]
        values = []
        for poly, uf in zip(me.polygons, md["uv_faces"]):
            if len(uf) != poly.loop_total:
                uf = [0] * poly.loop_total
            for k in uf:
                values.extend(uv_verts[k] if k < len(uv_verts) else (0.0, 0.0))
        uv.data.foreach_set("uv", values)
    ids = md.get("mat_ids", [])
    if len(ids) == nf:
        me.polygons.foreach_set("material_index", [slot_of_id(i) for i in ids])
    groups = md.get("smoothing", [])
    if len(groups) == nf:
        bm = bmesh.new()
        bm.from_mesh(me)
        layer = smoothing._layer(bm)
        bm.faces.ensure_lookup_table()
        for f, g in zip(bm.faces, groups):
            g = int(g) & 0xFFFFFFFF
            f[layer] = g - (1 << 32) if g >= (1 << 31) else g
        smoothing.apply_groups(bm, layer)
        bm.to_mesh(me)
        bm.free()
    me.validate(clean_customdata=False)
    return me


class _Importer:
    def __init__(self, context, path, convert_materials=True):
        self.context = context
        self.path = path
        with open(path, encoding="utf-8-sig") as f:
            self.data = json.load(f)
        if self.data.get("format") != "mxscene":
            raise ValueError("not a .mxscene file")
        self.scale = _meters_per_unit(self.data)
        self.convert_materials = convert_materials
        self.search_dirs = [os.path.dirname(path)]
        if self.data.get("file"):
            self.search_dirs.append(os.path.dirname(self.data["file"]))
        self.materials = {}
        self.collections = {}
        self.objects = {}
        self.by_name = {}

    def material(self, index):
        """Blender materials for an exported material: one, or one per sub-material."""
        if index in self.materials:
            return self.materials[index]
        mats = self.data.get("materials", [])
        if index < 0 or index >= len(mats):
            return []
        md = mats[index]
        if md.get("class", "").lower() == "multimaterial":
            self.materials[index] = []
            result = []
            for sub in md.get("sub", []):
                subs = self.material(sub.get("material", -1))
                result.append((int(sub.get("id", len(result) + 1)), subs[0][1] if subs else None))
        else:
            mat = bpy.data.materials.new(md.get("name") or "Material")
            if self.convert_materials:
                max_materials.convert(mat, md, self.search_dirs)
            result = [(None, mat)]
        self.materials[index] = result
        return result

    def collection(self, layer):
        if layer in self.collections:
            return self.collections[layer]
        root = self.context.collection
        if not layer or layer == "0":
            coll = root
        else:
            coll = bpy.data.collections.new(layer)
            root.children.link(coll)
        self.collections[layer] = coll
        return coll

    def node(self, nd):
        name = nd.get("name", "Object")
        kind = nd.get("kind", "EMPTY")
        data = None
        mats = []
        if kind == "MESH" and nd.get("mesh"):
            mats = self.material(nd.get("material", -1))
            ids = [i for i, _m in mats]
            if ids and ids[0] is not None:
                # Multi/Sub: Max wraps material IDs around the sub-material count.
                order = sorted(set(ids))

                def slot_of_id(mid):
                    if mid in order:
                        return order.index(mid)
                    return (mid - 1) % len(order)
                mats = [next(m for i, m in mats if i == mid) for mid in order]
            else:
                def slot_of_id(_mid):
                    return 0
                mats = [m for _i, m in mats]
            data = _mesh(name, nd["mesh"], self.scale, slot_of_id)
            for m in mats:
                data.materials.append(m)
        elif kind == "CAMERA":
            data = bpy.data.cameras.new(name)
            data.lens_unit = 'FOV'
            data.angle = math.radians(float(nd.get("fov", 45.0)))
            data.clip_end = max(data.clip_end, 1000.0)
        elif kind == "LIGHT":
            data = self._light(name, nd.get("light", {}), nd.get("class", ""))
        ob = bpy.data.objects.new(name, data)
        self.collection(nd.get("layer")).objects.link(ob)
        ob.matrix_world = _matrix(nd["transform"], self.scale)
        wc = nd.get("wirecolor")
        if wc:
            ob.color = tuple(wc[:3]) + (1.0,)
        if nd.get("frozen"):
            ob.hide_select = True
        if nd.get("hidden"):
            ob.hide_set(True)
        if not nd.get("renderable", True):
            ob.hide_render = True
        ob["max_class"] = nd.get("class", "")
        # Max allows duplicate names: nodes are found by their handle when the file has them.
        self.objects[nd.get("handle", len(self.objects))] = (ob, nd)
        self.by_name.setdefault(name, ob)
        return ob

    def _light(self, name, params, cls):
        p = {k.lower(): v for k, v in params.items()}
        c = cls.lower()
        if "sun" in c or "direct" in c or (c == "vraysun"):
            light = bpy.data.lights.new(name, 'SUN')
            light.energy = 3.0
        elif "spot" in c:
            light = bpy.data.lights.new(name, 'SPOT')
            if "falloff" in p:
                light.spot_size = math.radians(float(p["falloff"]))
        elif c in ("vraylight", "coronalight") and p.get("type", 0) in (0, 1):
            light = bpy.data.lights.new(name, 'AREA')
            # Plane or disc, half sizes in Max.
            w = float(p.get("size0", p.get("width", 50.0))) * self.scale
            h = float(p.get("size1", p.get("height", 50.0))) * self.scale
            light.size, light.size_y = max(w * 2, 1e-3), max(h * 2, 1e-3)
            light.shape = 'RECTANGLE'
            light.energy = 100.0
        else:
            light = bpy.data.lights.new(name, 'POINT')
            light.energy = 100.0
        color = p.get("color") or p.get("rgb") or p.get("rgbfilter")
        if isinstance(color, list):
            light.color = color[:3]
        light["max_class"] = cls
        return light

    def _find(self, nd, key):
        """The object `nd` refers to by `<key>_handle`, else by the name in `<key>`."""
        handle = nd.get(key + "_handle")
        if handle is not None and handle in self.objects:
            return self.objects[handle][0]
        name = nd.get(key)
        return self.by_name.get(name) if name else None

    def run(self):
        nodes = self.data.get("nodes", [])
        for nd in nodes:
            self.node(nd)
        # Parent after all exist, keeping the world transforms.
        for ob, nd in self.objects.values():
            parent = self._find(nd, "parent")
            if parent is not None and parent != ob:
                world = ob.matrix_world.copy()
                ob.parent = parent
                ob.matrix_world = world
        # Target cameras and lights look at their target.
        for ob, nd in self.objects.values():
            target = self._find(nd, "target")
            if target is not None and target != ob and ob.type in ('CAMERA', 'LIGHT'):
                con = ob.constraints.new('TRACK_TO')
                con.target = target
        return [ob for ob, _nd in self.objects.values()]


def import_mxscene(context, path, convert_materials=True):
    return _Importer(context, path, convert_materials).run()


class MAXIMIZE_OT_import_mxscene(Operator, ImportHelper):
    """Import a scene saved from 3ds Max with the Moritz exporter script (moritz_export.ms)"""
    bl_idname = "maximize.import_mxscene"
    bl_label = "Import Max Scene"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    filename_ext = ".mxscene"
    filter_glob: StringProperty(default="*.mxscene", options={'HIDDEN'})
    convert_materials: BoolProperty(
        name="Convert Materials",
        description="Convert V-Ray, Corona, Physical and Standard materials to Principled BSDF",
        default=True,
    )

    def execute(self, context):
        try:
            objects = import_mxscene(context, self.filepath, self.convert_materials)
        except (OSError, ValueError, KeyError) as ex:
            self.report({'ERROR'}, "Max Scene import failed: {}".format(ex))
            return {'CANCELLED'}
        for o in context.selected_objects:
            o.select_set(False)
        for o in objects:
            if o.visible_get():
                o.select_set(True)
        self.report({'INFO'}, "Imported {} objects".format(len(objects)))
        return {'FINISHED'}


class MAXIMIZE_OT_max_exporter_show(Operator):
    """Show the 3ds Max exporter script that writes .mxscene files (run it in Max)"""
    bl_idname = "maximize.max_exporter_show"
    bl_label = "Show Max Exporter Script"

    def execute(self, context):
        bpy.ops.wm.path_open(filepath=os.path.dirname(EXPORTER))
        return {'FINISHED'}


def _menu_import(self, _context):
    self.layout.operator(MAXIMIZE_OT_import_mxscene.bl_idname, text="Max Scene (.mxscene)")


_classes = (MAXIMIZE_OT_import_mxscene, MAXIMIZE_OT_max_exporter_show)


def register():
    for cls in _classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_file_import.append(_menu_import)


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(_menu_import)
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
