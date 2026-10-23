# Run: moritz.exe (or blender.exe) --factory-startup --enable-event-simulate --python tests/test_level_keys.py
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

import bpy
def say(*a): print("MXNUM", " ".join(str(x) for x in a), flush=True)
def win(): return bpy.context.window_manager.windows[0]
def area(): return next(a for a in win().screen.areas if a.type == 'VIEW_3D')
def ev(t, v, x, y, **k): win().event_simulate(type=t, value=v, x=int(x), y=int(y), **k)
P = {}
import maximize.selection as sel
def key(k, **m):
    ev('MOUSEMOVE','NOTHING',P['x'],P['y']); ev(k,'PRESS',P['x'],P['y'],**m); ev(k,'RELEASE',P['x'],P['y'],**m)
def s0():
    kc = bpy.context.window_manager.keyconfigs.user
    for it in kc.keymaps["Object Mode"].keymap_items:
        if it.type == 'ONE': say("user item", it.idname, it.active, it.value, it.any, it.ctrl, it.shift, it.alt, it.oskey, it.key_modifier, it.repeat)
    r = [r for r in area().regions if r.type == 'WINDOW'][-1]; P['x'], P['y'] = r.x + r.width*0.5, r.y + r.height*0.5
    ev('ESC','PRESS',10,10); ev('ESC','RELEASE',10,10)
def s0b():
    key('ONE')
def s1(): say("1 ->", bpy.context.mode); key('TWO')
def s1b(): say("2 ->", bpy.context.mode); key('TWO')
def s1c(): say("2 again ->", bpy.context.mode); key('K')
def s2(): say("K ->", [o.bl_idname for o in bpy.context.window_manager.operators][-2:]); bpy.ops.wm.quit_blender()
steps = [s0, s0b, s1, s1b, s1c, s2]
def run():
    try: steps.pop(0)()
    except Exception as e: say("ERR", repr(e))
    return 0.6 if steps else None
bpy.app.timers.register(run, first_interval=2.0)
