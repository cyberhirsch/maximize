# Run: moritz.exe --factory-startup --enable-event-simulate --python tests/test_tab_toggle.py
# Moritz keymap: Tab toggles Object / Edit Mode both ways, also after the 1-5 levels and with Edit
# Poly. (MX_KEYMAP=Max runs it on the Max keymap, where Tab is Search as in Industry Compatible, so
# it fails there by design until Seb decides otherwise.)
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bpy  # noqa: E402
from maximize.keymaps import activate  # noqa: E402

KEYMAP = os.environ.get("MX_KEYMAP", "Moritz")
failures = []


def say(*a): print("MXTAB", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", KEYMAP + ":", name, *info)
    if not ok:
        failures.append(name)


def win(): return bpy.context.window_manager.windows[0]
def area(): return next(a for a in win().screen.areas if a.type == 'VIEW_3D')
def ev(t, v, x, y, **k): win().event_simulate(type=t, value=v, x=int(x), y=int(y), **k)


P = {}


def key(k, **m):
    ev('MOUSEMOVE', 'NOTHING', P['x'], P['y'])
    ev(k, 'PRESS', P['x'], P['y'], **m)
    ev(k, 'RELEASE', P['x'], P['y'], **m)


def last_op():
    ops = bpy.context.window_manager.operators
    return ops[-1].bl_idname if len(ops) else None


def s_setup():
    activate(KEYMAP)
    r = [r for r in area().regions if r.type == 'WINDOW'][-1]
    P['x'], P['y'] = r.x + r.width * 0.5, r.y + r.height * 0.5
    say("keymap", bpy.context.window_manager.keyconfigs.active.name, "mode", bpy.context.mode,
        "active", bpy.context.active_object and bpy.context.active_object.name)
    ev('ESC', 'PRESS', 10, 10)
    ev('ESC', 'RELEASE', 10, 10)


def s_wait():
    kc = bpy.context.window_manager.keyconfigs.active
    tabs = [(km.name, it.idname, it.active) for km in kc.keymaps for it in km.keymap_items
            if it.type == 'TAB' and not (it.ctrl or it.shift or it.alt)]
    say("keymap now", kc.name, "Tab bound:", tabs)


def s_tab1(): key('TAB')
def c_tab1(): check("Tab: Object -> Edit", bpy.context.mode == 'EDIT_MESH', bpy.context.mode, last_op()); key('TAB')
def c_tab2(): check("Tab: Edit -> Object", bpy.context.mode == 'OBJECT', bpy.context.mode, last_op()); key('TWO')
def c_level(): say("2 ->", bpy.context.mode); key('TAB')
def c_level_tab(): check("Tab after 2 (edge level) -> Object", bpy.context.mode == 'OBJECT', bpy.context.mode, last_op())


def s_edit_poly():
    obj = bpy.context.active_object
    obj.modifiers.new("Bend", 'SIMPLE_DEFORM')
    with bpy.context.temp_override(window=win(), area=area(), region=[r for r in area().regions if r.type == 'WINDOW'][-1]):
        bpy.ops.maximize.edit_poly_add()
    say("edit poly added", [m.name for m in obj.modifiers], bpy.context.mode)
    key('ONE')


def c_ep1(): say("Edit Poly, 1 ->", bpy.context.mode, bpy.context.active_object.name); key('TAB')
def c_ep2(): check("Edit Poly: Tab after 1 -> Object", bpy.context.mode == 'OBJECT', bpy.context.mode, last_op(), bpy.context.active_object.name); key('TAB')
def c_ep3(): check("Edit Poly: Tab -> Edit", bpy.context.mode == 'EDIT_MESH', bpy.context.mode, last_op()); key('TAB')


def c_ep4():
    check("Edit Poly: Tab -> Object again", bpy.context.mode == 'OBJECT', bpy.context.mode, last_op())
    say("FAILURES", len(failures), failures)
    bpy.ops.wm.quit_blender()


steps = [s_setup, s_wait, s_tab1, c_tab1, c_tab2, c_level, c_level_tab, s_edit_poly, c_ep1, c_ep2, c_ep3, c_ep4]


def run():
    try:
        steps.pop(0)()
    except Exception as e:
        say("ERR", repr(e))
    return 0.6 if steps else None


bpy.app.timers.register(run, first_interval=2.0)
