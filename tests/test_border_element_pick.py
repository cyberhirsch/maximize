# Run: moritz.exe (or blender.exe) --factory-startup --enable-event-simulate --python tests/test_border_element_pick.py
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

import bpy, bmesh
from bpy_extras.view3d_utils import location_3d_to_region_2d
def say(*a): print("MXPK", " ".join(str(x) for x in a), flush=True)
def win(): return bpy.context.window_manager.windows[0]
def area(): return next(a for a in win().screen.areas if a.type == 'VIEW_3D')
def region(): return [r for r in area().regions if r.type == 'WINDOW'][-1]
def ev(t, v, x, y, **k): win().event_simulate(type=t, value=v, x=int(x), y=int(y), **k)
def key(k, x=None, y=None):
    r = region(); x = x or r.x + r.width//2; y = y or r.y + r.height//2
    ev('MOUSEMOVE','NOTHING',x,y); ev(k,'PRESS',x,y); ev(k,'RELEASE',x,y)
def click(co, **m):
    r = region(); p = location_3d_to_region_2d(r, r.data, co)
    x, y = r.x + p.x, r.y + p.y
    ev('MOUSEMOVE','NOTHING',x,y); ev('LEFTMOUSE','PRESS',x,y,**m); ev('LEFTMOUSE','RELEASE',x,y,**m)
def sel():
    bm = bmesh.from_edit_mesh(bpy.context.edit_object.data)
    return (sum(v.select for v in bm.verts), sum(e.select for e in bm.edges), sum(f.select for f in bm.faces))
C = {}
def s0():
    ev('ESC','PRESS',10,10); ev('ESC','RELEASE',10,10)
    a = area(); r = region()
    if a.spaces.active.region_quadviews:
        with bpy.context.temp_override(window=win(), area=a, region=r): bpy.ops.screen.region_quadview()
    # Two separate elements: the cube with its top face removed, and a second cube.
    cube = bpy.data.objects["Cube"]
    me = cube.data; bm = bmesh.new(); bm.from_mesh(me)
    top = [f for f in bm.faces if f.calc_center_median().z > 0.9]
    bmesh.ops.delete(bm, geom=top, context='FACES_ONLY')
    bmesh.ops.create_cube(bm, size=1.0, matrix=__import__("mathutils").Matrix.Translation((0, 3, 0)))
    bm.to_mesh(me); bm.free()
    bpy.context.view_layer.objects.active = cube
    with bpy.context.temp_override(window=win(), area=a, region=region()):
        bpy.ops.view3d.view_selected()
def s1(): key('THREE')
def s2():
    say("level 3 mode", bpy.context.mode, bpy.context.scene.get("maximize_level"))
    bpy.ops.mesh.select_all(action='DESELECT')
    click(__import__("mathutils").Vector((1, 0, 1)))   # top border edge (open)
def s3():
    say("border click ->", sel(), "(want 4 verts, 4 edges)")
    bpy.ops.mesh.select_all(action='DESELECT')
    click(__import__("mathutils").Vector((1, 1, 0)))   # side edge, not a border
def s4():
    say("inner edge click ->", sel(), "(want nothing)")
    key('FIVE')
def s5():
    say("level 5", bpy.context.scene.get("maximize_level"))
    bpy.ops.mesh.select_all(action='DESELECT')
    click(__import__("mathutils").Vector((1, 0, 0)))   # side face of the open cube
def s6():
    say("element click ->", sel(), "(want 8 verts, 5 faces)")
    click(__import__("mathutils").Vector((0, 3, 0.5)), ctrl=True)  # top of second cube
def s7():
    say("ctrl element click ->", sel(), "(want 16 verts, 11 faces)")
    click(__import__("mathutils").Vector((1, 0, 0)), alt=True)
def s8():
    say("alt element click ->", sel(), "(want 8 verts, 6 faces)")
    key('TWO')
def s9():
    bpy.ops.mesh.select_all(action='DESELECT')
    click(__import__("mathutils").Vector((1, 1, 0)))
def s10():
    say("edge level click ->", sel(), "(want 2 verts, 1 edge)"); bpy.ops.wm.quit_blender()
steps = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]
def run():
    try: steps.pop(0)()
    except Exception as e:
        import traceback; say("ERR", traceback.format_exc())
    return 0.6 if steps else None
bpy.app.timers.register(run, first_interval=2.0)
