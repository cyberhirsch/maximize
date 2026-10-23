# Run: moritz.exe (or blender.exe) --factory-startup --enable-event-simulate --python tests/test_quad_and_maximize.py
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

import bpy, os
def say(*a): print("MXUI3", " ".join(str(x) for x in a), flush=True)
def win(): return bpy.context.window_manager.windows[0]
def shot(n):
    with bpy.context.temp_override(window=win()):
        bpy.ops.screen.screenshot(filepath=os.path.join(OUT, n + ".png"))
def area(): return next(a for a in win().screen.areas if a.type == 'VIEW_3D')
def regions(): return [r for r in area().regions if r.type == 'WINDOW']
def ev(t, v, x, y, **k): win().event_simulate(type=t, value=v, x=int(x), y=int(y), **k)
def top_region():
    for r in regions():
        if not r.data.is_perspective and r.data.view_rotation.to_euler().x == 0 and abs(r.data.view_matrix[2][2]) > 0.99:
            return r
    return regions()[0]
P = {}
def s0():
    # Enabled after startup, so the Max layout for new files (quad view) has not run yet.
    import maximize.viewport
    maximize.viewport._apply_layout()
    ev('ESC','PRESS',10,10); ev('ESC','RELEASE',10,10)
def s1():
    r = regions()[-1]; P['x'], P['y'] = r.x + r.width*0.5, r.y + r.height*0.5
    say("top region", r.x, r.y, r.width, r.height)
    ev('MOUSEMOVE','NOTHING',P['x'],P['y']); ev('RIGHTMOUSE','PRESS',P['x'],P['y'])
def s2():
    say("mouse", P["x"], P["y"]); shot("01_quad_object"); ev('ESC','PRESS',P['x'],P['y']); ev('ESC','RELEASE',P['x'],P['y'])
def s3():
    r = top_region(); P['x'], P['y'] = r.x + r.width*0.5, r.y + r.height*0.5
    sp = area().spaces.active
    say("before alt+w quad", len(sp.region_quadviews), "persp", sp.region_3d.view_perspective)
    ev('MOUSEMOVE','NOTHING',P['x'],P['y']); ev('W','PRESS',P['x'],P['y'],alt=True); ev('W','RELEASE',P['x'],P['y'],alt=True)
def s4():
    sp = area().spaces.active; r3 = sp.region_3d
    say("after alt+w quad", len(sp.region_quadviews), "persp", r3.view_perspective, "side", r3.is_orthographic_side_view,
        "rot", tuple(round(c,2) for c in r3.view_rotation))
    shot("02_maximized_top")
    r = regions()[-1]
    ev('MOUSEMOVE','NOTHING',r.x+r.width//2,r.y+r.height//2); ev('W','PRESS',r.x+r.width//2,r.y+r.height//2,alt=True); ev('W','RELEASE',r.x+r.width//2,r.y+r.height//2,alt=True)
def s5():
    sp = area().spaces.active
    say("back quad", len(sp.region_quadviews), "main persp", sp.region_3d.view_perspective)
    shot("03_back_to_quad")
    with bpy.context.temp_override(window=win(), area=area(), region=regions()[-1]):
        bpy.ops.object.mode_set(mode='EDIT')
    r = regions()[-1]; P['x'], P['y'] = r.x + r.width*0.5, r.y + r.height*0.5
    ev('MOUSEMOVE','NOTHING',P['x'],P['y']); ev('RIGHTMOUSE','PRESS',P['x'],P['y'])
def s6():
    shot("04_quad_edit"); ev('ESC','PRESS',P['x'],P['y'])
def s7(): bpy.ops.wm.quit_blender()
Q = [s0, s1, s2, s3, s4, s5, s6, s7]
def tick():
    if not Q: return None
    try: Q.pop(0)()
    except Exception as e:
        import traceback; say("ERROR", repr(e)); traceback.print_exc()
    return 1.0
bpy.app.timers.register(tick, first_interval=3.0)
