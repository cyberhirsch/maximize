# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Max materials to Principled BSDF: V-Ray (VRayMtl, VRayLightMtl), Corona (CoronaPhysicalMtl,
CoronaLegacyMtl / CoronaMtl, CoronaLightMtl), Physical Material, Standard, Multi/Sub-Object
(handled by the importer: one slot per sub-material).

Input is the material as written by `max_side/moritz_export.ms`: `class`, `name` and `params`,
all of the material's parameters by their MaxScript names (compared lower-case). Maps are dicts
with `class`, `params` and, for bitmaps, `file`. Unknown materials get their diffuse-looking
color, unknown maps the first bitmap found inside them, so nothing comes in as plain white
without a reason. What a converter could not map is listed in the material's custom property
`max_unconverted`.
"""

import os

import bpy

# Parameters by role, per material class (lower case). A role maps to a Principled input.
VRAY = {
    "base_color": ("diffuse", "texmap_diffuse"),
    "roughness": ("reflection_glossiness", "texmap_reflectionglossiness"),
    "metallic": ("reflection_metalness", "texmap_metalness"),
    "ior": ("reflection_ior", None),
    "specular_color": ("reflection", "texmap_reflection"),
    "transmission_color": ("refraction", "texmap_refraction"),
    "transmission_roughness": ("refraction_glossiness", None),
    "transmission_ior": ("refraction_ior", None),
    "opacity": (None, "texmap_opacity"),
    "bump": (None, "texmap_bump"),
    "bump_amount": ("texmap_bump_multiplier", None),
    "emission_color": ("selfillumination", "texmap_self_illumination"),
    "emission_strength": ("selfillumination_multiplier", None),
    "coat": ("coat_amount", None),
    "coat_roughness": ("coat_glossiness", None),
    "coat_ior": ("coat_ior", None),
    "sheen_color": ("sheen_color", None),
    "sheen_roughness": ("sheen_glossiness", None),
}

CORONA_PHYSICAL = {
    "base_color": ("basecolor", "basetexmap"),
    "base_level": ("baselevel", None),
    "roughness": ("baseroughness", "baseroughnesstexmap"),
    "metallic": ("metalnessmode", "metalnesstexmap"),
    "ior": ("baseior", None),
    "transmission": ("refractionamount", "refractionamounttexmap"),
    "opacity": ("opacitylevel", "opacitytexmap"),
    "bump": (None, "basebumptexmap"),
    "bump_amount": ("basebumpmapamount", None),
    "emission_color": ("selfillumcolor", "selfillumtexmap"),
    "emission_strength": ("selfillumlevel", None),
    "coat": ("clearcoatamount", None),
    "coat_roughness": ("clearcoatroughness", None),
    "coat_ior": ("clearcoatior", None),
    "sheen": ("sheenamount", None),
    "sheen_color": ("sheencolor", None),
    "sheen_roughness": ("sheenroughness", None),
    "subsurface": ("sssamount", None),
}

CORONA_LEGACY = {
    "base_color": ("colordiffuse", "texmapdiffuse"),
    "base_level": ("leveldiffuse", None),
    "specular_color": ("colorreflect", "texmapreflect"),
    "specular_level": ("levelreflect", None),
    "roughness": ("reflectglossiness", "texmapreflectglossiness"),
    "ior": ("fresnelior", None),
    "transmission_color": ("colorrefract", "texmaprefract"),
    "transmission_level": ("levelrefract", None),
    "transmission_ior": ("ior", None),
    "opacity": ("levelopacity", "texmapopacity"),
    "bump": (None, "texmapbump"),
    "bump_amount": ("mapamountbump", None),
    "emission_color": ("colorselfillum", "texmapselfillum"),
    "emission_strength": ("levelselfillum", None),
}

PHYSICAL = {
    "base_color": ("base_color", "base_color_map"),
    "base_level": ("base_weight", None),
    "roughness": ("roughness", "roughness_map"),
    "metallic": ("metalness", "metalness_map"),
    "ior": ("trans_ior", None),
    "transmission": ("transparency", "transparency_map"),
    "opacity": (None, "cutout_map"),
    "bump": (None, "bump_map"),
    "bump_amount": ("bump_map_amt", None),
    "emission_color": ("emit_color", "emit_color_map"),
    "emission_strength": ("emission", None),
    "coat": ("coating", None),
    "coat_roughness": ("coat_roughness", None),
    "coat_ior": ("coat_ior", None),
    "sheen": ("sheen", None),
    "sheen_color": ("sheen_color", None),
    "sheen_roughness": ("sheen_roughness", None),
    "subsurface": ("scattering", None),
}

STANDARD = {
    "base_color": ("diffuse", "diffusemap"),
    "opacity": ("opacity", "opacitymap"),
    "bump": (None, "bumpmap"),
    "bump_amount": ("bumpmapamount", None),
    "roughness": ("glossiness", "glossinessmap"),
    "specular_level": ("specularlevel", None),
    "emission_color": ("selfillumcolor", "selfillummap"),
}

TABLES = {
    "vraymtl": VRAY,
    "coronaphysicalmtl": CORONA_PHYSICAL,
    "coronalegacymtl": CORONA_LEGACY,
    "coronamtl": CORONA_LEGACY,
    "physicalmaterial": PHYSICAL,
    "physical_material": PHYSICAL,
    "standardmaterial": STANDARD,
    "standard": STANDARD,
}

LIGHT_MATERIALS = {
    "vraylightmtl": ("color", "multiplier", "texmap"),
    "coronalightmtl": ("color", "intensity", "texmap"),
}

BITMAP_KEYS = ("file", "filename", "hdrimapname")
NORMAL_MAPS = {"vraynormalmap", "coronanormal", "normal_bump", "normalbump"}


def _lower(params):
    return {k.lower(): v for k, v in (params or {}).items()}


def _value(params, key):
    return None if key is None else params.get(key)


def _is_map(v):
    return isinstance(v, dict) and "class" in v


def bitmap_file(texmap, depth=0):
    """The image file of a map: its own, else the first one inside it (color correction etc.)."""
    if not _is_map(texmap) or depth > 6:
        return None
    if texmap.get("file"):
        return texmap["file"]
    params = _lower(texmap.get("params"))
    for key in BITMAP_KEYS:
        if isinstance(params.get(key), str) and params[key]:
            return params[key]
    for v in params.values():
        found = bitmap_file(v, depth + 1)
        if found:
            return found
    return None


def _normal_map(texmap):
    return _is_map(texmap) and texmap["class"].lower() in NORMAL_MAPS


class _Builder:
    def __init__(self, mat, search_dirs):
        self.mat = mat
        mat.use_nodes = True
        self.nt = mat.node_tree
        self.bsdf = next(n for n in self.nt.nodes if n.type == 'BSDF_PRINCIPLED')
        self.out = next(n for n in self.nt.nodes if n.type == 'OUTPUT_MATERIAL')
        self.search_dirs = search_dirs
        self.unconverted = []
        self.y = 300

    def image(self, texmap, non_color=False):
        path = bitmap_file(texmap)
        if not path:
            if _is_map(texmap):
                self.unconverted.append(texmap["class"])
            return None
        node = self.nt.nodes.new('ShaderNodeTexImage')
        node.location = (-700, self.y)
        self.y -= 280
        node.image = self._load(path)
        if node.image and non_color:
            node.image.colorspace_settings.is_data = True
        node.label = os.path.basename(path)
        return node

    def _load(self, path):
        candidates = [path] + [os.path.join(d, os.path.basename(path)) for d in self.search_dirs]
        for p in candidates:
            if os.path.isfile(p):
                return bpy.data.images.load(p, check_existing=True)
        # Keep the reference so relinking (File > External Data) can find it later.
        img = bpy.data.images.new(os.path.basename(path) or "missing", 8, 8)
        img.source = 'FILE'
        img.filepath = path
        return img

    def link(self, node, socket, output="Color"):
        self.nt.links.new(node.outputs[output], self.bsdf.inputs[socket])

    def set(self, socket, value):
        inp = self.bsdf.inputs[socket]
        if isinstance(value, (list, tuple)):
            value = tuple(value[:3])
            if len(inp.default_value) == 4:
                value = value + (1.0,)
        inp.default_value = value

    def color_or_map(self, socket, color, texmap, non_color=False):
        if color is not None:
            self.set(socket, color)
        node = self.image(texmap, non_color) if texmap is not None else None
        if node:
            self.link(node, socket)
        return node

    def bump(self, texmap, amount):
        if texmap is None:
            return
        normal = _normal_map(texmap)
        node = self.image(texmap, non_color=True)
        if node is None:
            return
        if normal:
            nm = self.nt.nodes.new('ShaderNodeNormalMap')
            nm.location = (-350, node.location.y)
            self.nt.links.new(node.outputs["Color"], nm.inputs["Color"])
            self.nt.links.new(nm.outputs["Normal"], self.bsdf.inputs["Normal"])
        else:
            bp = self.nt.nodes.new('ShaderNodeBump')
            bp.location = (-350, node.location.y)
            bp.inputs["Strength"].default_value = min(max(float(amount or 1.0), 0.0), 1.0)
            self.nt.links.new(node.outputs["Color"], bp.inputs["Height"])
            self.nt.links.new(bp.outputs["Normal"], self.bsdf.inputs["Normal"])


def _gray(c):
    return sum(c[:3]) / 3.0 if isinstance(c, (list, tuple)) else float(c)


def _scale(c, level):
    if isinstance(c, (list, tuple)) and level is not None:
        return [x * float(level) for x in c[:3]]
    return c


def convert(mat, data, search_dirs=()):
    """Fill the Blender material `mat` from the exported Max material `data`."""
    cls = data.get("class", "").lower()
    params = _lower(data.get("params"))
    mat["max_class"] = data.get("class", "")
    b = _Builder(mat, list(search_dirs))

    if cls in LIGHT_MATERIALS:
        color_key, strength_key, map_key = LIGHT_MATERIALS[cls]
        color = params.get(color_key, [1, 1, 1])
        b.set("Base Color", (0, 0, 0))
        b.color_or_map("Emission Color", color, params.get(map_key))
        b.set("Emission Strength", float(params.get(strength_key, 1.0)))
        mat.diffuse_color = tuple(color[:3]) + (1.0,)
        return mat

    table = TABLES.get(cls)
    if table is None:
        # Unknown class: anything that looks like a diffuse color or map.
        b.unconverted.append(data.get("class", ""))
        for key, v in params.items():
            if "diffuse" in key or "basecolor" in key or key == "color":
                if isinstance(v, list):
                    b.set("Base Color", v)
                elif _is_map(v):
                    b.color_or_map("Base Color", None, v)
                break
        mat["max_unconverted"] = ", ".join(sorted(set(b.unconverted)))
        return mat

    def get(role):
        value_key, map_key = table.get(role, (None, None))
        return _value(params, value_key), _value(params, map_key)

    color, cmap = get("base_color")
    level, _ = get("base_level")
    if color is not None:
        color = _scale(color, level)
    b.color_or_map("Base Color", color, cmap)
    if isinstance(color, list):
        mat.diffuse_color = tuple(color[:3]) + (1.0,)

    # Roughness: V-Ray and Corona legacy give glossiness unless told otherwise.
    rough, rmap = get("roughness")
    glossy = cls == "vraymtl" and not params.get("brdf_useroughness", False)
    glossy = glossy or cls in ("coronalegacymtl", "coronamtl", "standardmaterial", "standard")
    if cls == "coronaphysicalmtl":
        glossy = int(params.get("roughnessmode", 0)) == 1
    if cls in ("physicalmaterial", "physical_material"):
        glossy = bool(params.get("roughness_inv", False))
    if rough is not None:
        r = float(rough)
        if cls in ("standardmaterial", "standard"):
            r = r / 100.0
        r = min(max(1.0 - r if glossy else r, 0.0), 1.0)
        b.set("Roughness", r)
    if rmap is not None:
        node = b.image(rmap, non_color=True)
        if node:
            if glossy:
                inv = b.nt.nodes.new('ShaderNodeInvert')
                inv.location = (-350, node.location.y)
                b.nt.links.new(node.outputs["Color"], inv.inputs["Color"])
                b.nt.links.new(inv.outputs["Color"], b.bsdf.inputs["Roughness"])
            else:
                b.link(node, "Roughness")

    metal, mmap = get("metallic")
    if metal is not None:
        b.set("Metallic", min(max(float(metal), 0.0), 1.0))
    if mmap is not None:
        node = b.image(mmap, non_color=True)
        if node:
            b.link(node, "Metallic")

    ior, _ = get("ior")
    if ior is not None and float(ior) > 1.0:
        b.set("IOR", float(ior))
    if cls == "vraymtl" and not params.get("reflection_fresnel", True):
        # No Fresnel: a mirror-like constant reflection; roughly a high IOR.
        b.set("IOR", 10.0)

    spec, smap = get("specular_color")
    slevel, _ = get("specular_level")
    if spec is not None:
        amount = _gray(_scale(spec, slevel))
        if cls in ("standardmaterial", "standard"):
            amount = float(slevel or 0) / 100.0
        b.set("Specular IOR Level", min(max(amount, 0.0), 1.0))
        if "Specular Tint" in b.bsdf.inputs and isinstance(spec, list) and max(spec) > 0:
            peak = max(spec[:3])
            b.set("Specular Tint", [c / peak for c in spec[:3]])
    elif slevel is not None and cls in ("standardmaterial", "standard"):
        b.set("Specular IOR Level", min(max(float(slevel) / 100.0, 0.0), 1.0))

    trans, tmap = get("transmission")
    tcolor, _ = get("transmission_color")
    tlevel, _ = get("transmission_level")
    weight = None
    if trans is not None:
        weight = float(trans)
    elif tcolor is not None:
        weight = _gray(_scale(tcolor, tlevel))
    if weight:
        b.set("Transmission Weight", min(max(weight, 0.0), 1.0))
        tior, _ = get("transmission_ior")
        if tior is not None and float(tior) > 1.0:
            b.set("IOR", float(tior))
        troughness, _ = get("transmission_roughness")
        if troughness is not None and cls == "vraymtl":
            # Principled has one roughness; glass usually wants the refraction one.
            if weight > 0.5:
                b.set("Roughness", min(max(1.0 - float(troughness), 0.0), 1.0))
    if tmap is not None:
        node = b.image(tmap, non_color=True)
        if node:
            b.link(node, "Transmission Weight")

    opacity, omap = get("opacity")
    if opacity is not None:
        o = float(opacity)
        if cls in ("standardmaterial", "standard"):
            o = o / 100.0
        b.set("Alpha", min(max(o, 0.0), 1.0))
    if omap is not None:
        node = b.image(omap, non_color=True)
        if node:
            b.link(node, "Alpha")
    if opacity is not None and float(opacity) < (100.0 if cls in ("standardmaterial", "standard") else 1.0) \
            or omap is not None:
        if hasattr(mat, "surface_render_method"):
            mat.surface_render_method = 'DITHERED'

    _, bump = get("bump")
    amount, _ = get("bump_amount")
    if bump is not None:
        # V-Ray's multiplier and Standard's amount are in percent-like units.
        a = float(amount) if amount is not None else 1.0
        if cls in ("vraymtl", "standardmaterial", "standard") and a > 1.0:
            a = a / 100.0
        b.bump(bump, a)

    ecolor, emap = get("emission_color")
    estrength, _ = get("emission_strength")
    if ecolor is not None and _gray(ecolor) > 0 or emap is not None:
        b.color_or_map("Emission Color", ecolor, emap)
        b.set("Emission Strength", float(estrength) if estrength is not None else 1.0)
    elif estrength is not None and cls in ("physicalmaterial", "physical_material") and float(estrength) > 0:
        b.set("Emission Strength", float(estrength))

    coat, _ = get("coat")
    if coat is not None and float(coat) > 0:
        b.set("Coat Weight", min(float(coat), 1.0))
        croughness, _ = get("coat_roughness")
        if croughness is not None:
            r = float(croughness)
            b.set("Coat Roughness", 1.0 - r if cls == "vraymtl" else r)
        cior, _ = get("coat_ior")
        if cior is not None and float(cior) > 1.0:
            b.set("Coat IOR", float(cior))

    sheen, _ = get("sheen")
    scolor, _ = get("sheen_color")
    if (sheen is not None and float(sheen) > 0) or (scolor is not None and _gray(scolor) > 0):
        b.set("Sheen Weight", float(sheen) if sheen is not None else 1.0)
        if scolor is not None:
            b.set("Sheen Tint", scolor)
        sroughness, _ = get("sheen_roughness")
        if sroughness is not None:
            r = float(sroughness)
            b.set("Sheen Roughness", 1.0 - r if cls == "vraymtl" else r)

    sss, _ = get("subsurface")
    if sss is not None and float(sss) > 0:
        b.set("Subsurface Weight", min(float(sss), 1.0))

    if b.unconverted:
        mat["max_unconverted"] = ", ".join(sorted(set(b.unconverted)))
    return mat
