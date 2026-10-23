# Run: moritz.exe (or blender.exe) --factory-startup -b --python tests/test_background.py
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

import bpy, traceback
def check(name, fn):
    try:
        r = fn(); print("MXT OK", name, r if r is not None else "")
    except Exception:
        print("MXT FAIL", name); traceback.print_exc()

import maximize
check("prefs", lambda: bpy.context.preferences.addons["maximize"].preferences.first_run_done)
check("translation", lambda: bpy.app.translations.pgettext_iface("Merge by Distance", "Operator"))
# Keymap preset
def kmtest():
    path = bpy.utils.preset_find("Max", "keyconfig")
    bpy.utils.keyconfig_set(path)
    kc = bpy.context.window_manager.keyconfigs["Max"]
    out = []
    for km_name, key, mods in (("3D View","Z",()),("3D View","MIDDLEMOUSE",("alt",)),("3D View","MIDDLEMOUSE",()),("3D View","T",()),("Object Mode","H",()),("Object Mode","RIGHTMOUSE",()),("Mesh","C",("ctrl","shift")),("Object Mode","ONE",()),("Frames","SLASH",()),("Screen","Y",("ctrl",)),("3D View","S",()),("Object Mode","S",())):
        km = kc.keymaps[km_name]
        hits = [k.idname for k in km.keymap_items if k.type == key and k.ctrl == ("ctrl" in mods) and k.shift == ("shift" in mods) and k.alt == ("alt" in mods)]
        out.append(f"{km_name}:{'+'.join(mods+(key,))}={hits}")
    return "\n  ".join(out)
check("keymap", kmtest)
# Primitives
for kind in ("BOX","SPHERE","CYLINDER","CONE","TUBE","TORUS","PLANE"):
    def f(kind=kind):
        bpy.ops.maximize.add_primitive(kind=kind)
        o = bpy.context.active_object
        dg = bpy.context.evaluated_depsgraph_get()
        e = o.evaluated_get(dg); m = e.to_mesh()
        zs = [v.co.z for v in m.vertices]; xs=[v.co.x for v in m.vertices]
        r = (o.name, len(m.vertices), round(min(zs),3), round(max(zs),3), round(min(xs),3), round(max(xs),3), "UVMap" in m.uv_layers or "UVMap" in m.attributes)
        e.to_mesh_clear(); return r
    check("prim "+kind, f)
# UVW map
def uvw():
    bpy.ops.maximize.add_primitive(kind='BOX')
    o = bpy.context.active_object
    res = []
    for mp in ("PLANAR","BOX","CYLINDRICAL","SPHERICAL"):
        for m in [m for m in o.modifiers if m.name.startswith("UVW")]: o.modifiers.remove(m)
        bpy.ops.maximize.uvw_map(mapping=mp)
        dg = bpy.context.evaluated_depsgraph_get(); e=o.evaluated_get(dg); me=e.to_mesh()
        uv = me.attributes.get("UVMap")
        vals = [tuple(round(x,2) for x in d.vector) for d in uv.data] if uv else None
        res.append((mp, uv.domain if uv else None, min(vals) if vals else None, max(vals) if vals else None))
        e.to_mesh_clear()
    return res
check("uvw", uvw)
# Array / spacing / align / clone / typein (exec)
def arr():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.maximize.add_primitive(kind='SPHERE')
    n = len(bpy.data.objects)
    bpy.ops.maximize.array(count_1d=5, move=(2,0,0), dimension='2D', count_2d=3, clone_type='INSTANCE')
    return len(bpy.data.objects)-n
check("array", arr)
def spacing():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.maximize.add_primitive(kind='BOX'); src = bpy.context.active_object
    bpy.ops.curve.primitive_bezier_circle_add(radius=5)
    crv = bpy.context.active_object; src.select_set(True)
    before = set(bpy.data.objects)
    bpy.ops.maximize.spacing(count=8, follow=True)
    new = sorted(set(bpy.data.objects) - before, key=lambda o: o.name)
    return len(new), [tuple(round(c,2) for c in o.location) for o in new[:3]]
check("spacing", spacing)
def align():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.maximize.add_primitive(kind='BOX'); a = bpy.context.active_object; a.location=(0,0,0)
    bpy.ops.maximize.add_primitive(kind='BOX'); t = bpy.context.active_object; t.location=(5,3,2)
    a.select_set(True)
    bpy.ops.maximize.align_apply(target=t.name, current_point='MIN', target_point='MAX')
    bpy.context.view_layer.update()
    return tuple(round(c,3) for c in a.location)
check("align", align)
def clone():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.maximize.add_primitive(kind='BOX'); o=bpy.context.active_object
    bpy.ops.object.convert(target='MESH')
    bpy.ops.maximize.clone(clone_type='INSTANCE', copies=3)
    c = bpy.context.active_object
    return c.name, c.data == o.data
check("clone", clone)
def typein():
    o = bpy.context.active_object
    bpy.ops.maximize.transform_typein(mode='MOVE', absolute=(1,2,3), offset=(0,0,0))
    a = tuple(o.location)
    bpy.ops.maximize.transform_typein(mode='MOVE', offset=(1,0,0))
    bpy.ops.maximize.transform_typein(mode='SCALE', offset=(200,200,200))
    return a, tuple(o.location), tuple(o.scale)
check("typein", typein)
def resetx():
    o = bpy.context.active_object; o.rotation_euler=(0.5,0,0)
    bpy.ops.maximize.reset_xform(); return tuple(o.rotation_euler), tuple(o.scale)
check("reset_xform", resetx)
def subobj():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.maximize.add_primitive(kind='BOX')
    bpy.ops.maximize.subobject(level='POLYGON')
    m = bpy.context.mode; sm = tuple(bpy.context.tool_settings.mesh_select_mode)
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.maximize.selset_create(name="top")
    bpy.ops.maximize.subobject(level='POLYGON')
    return m, sm, bpy.context.mode, [a.name for a in bpy.context.active_object.data.attributes if a.name.startswith("nss_")]
check("subobject+sets", subobj)
def objsets():
    bpy.ops.maximize.selset_create(name="boxes")
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.maximize.selset_select(name="boxes")
    return len(bpy.context.selected_objects), [s.name for s in bpy.context.scene.maximize_sets]
check("objsets", objsets)
def aliases():
    from maximize.vocabulary import ALIASES
    missing = [t for _i,_l,t,_p,_m,_d in ALIASES if not hasattr(getattr(bpy.ops, t.split(".")[0]), t.split(".")[1])]
    return missing
check("alias targets", aliases)
check("disable", lambda: addon_utils.disable("maximize", default_set=True) or "disabled")
