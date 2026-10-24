# Run: moritz.exe --factory-startup --enable-event-simulate --python tests/test_region_select.py
# Moritz keymap: Q cycles the region shapes, left-to-right drags select by window, right-to-left by
# crossing; numpad views; hover highlight.
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bpy, bmesh
from mathutils import Vector
from bpy_extras.view3d_utils import location_3d_to_region_2d
def say(*a): print("MXRS", " ".join(str(x) for x in a), flush=True)
def win(): return bpy.context.window_manager.windows[0]
def area(): return next(a for a in win().screen.areas if a.type == 'VIEW_3D')
def region(): return [r for r in area().regions if r.type == 'WINDOW'][-1]
def ev(t, v, x, y, **k): win().event_simulate(type=t, value=v, x=int(x), y=int(y), **k)
def key(k, **m):
    r = region(); x = r.x + r.width // 2; y = r.y + r.height // 2
    ev('MOUSEMOVE', 'NOTHING', x, y); ev(k, 'PRESS', x, y, **m); ev(k, 'RELEASE', x, y, **m)
def px(co):
    r = region(); p = location_3d_to_region_2d(r, r.data, co); return r.x + p.x, r.y + p.y
def drag(a, b, **m):
    (x0, y0), (x1, y1) = px(a), px(b)
    ev('MOUSEMOVE', 'NOTHING', x0, y0); ev('LEFTMOUSE', 'PRESS', x0, y0, **m)
    for i in range(1, 9):
        t = i / 8; ev('MOUSEMOVE', 'NOTHING', x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, **m)
    ev('LEFTMOUSE', 'RELEASE', x1, y1, **m)
def move(co):
    x, y = px(co); ev('MOUSEMOVE', 'NOTHING', x, y); ev('MOUSEMOVE', 'NOTHING', x + 1, y)
def objs(): return sorted(o.name for o in bpy.context.selected_objects)
def tool():
    with bpy.context.temp_override(window=win(), area=area()):
        return bpy.context.workspace.tools.from_space_view3d_mode(bpy.context.mode).idname
def faces():
    bm = bmesh.from_edit_mesh(bpy.context.edit_object.data)
    return sum(f.select for f in bm.faces)
def edges():
    bm = bmesh.from_edit_mesh(bpy.context.edit_object.data)
    return sum(e.select for e in bm.edges)
def s0():
    ev('ESC', 'PRESS', 10, 10); ev('ESC', 'RELEASE', 10, 10)
    a = area()
    if a.spaces.active.region_quadviews:
        with bpy.context.temp_override(window=win(), area=a, region=region()):
            bpy.ops.screen.region_quadview()
    say("keymap", bpy.context.window_manager.keyconfigs.active.name)
    cube = bpy.data.objects["Cube"]
    for name, loc in (("Right", (4, 0, 0)), ("Behind", (0, 6, 0))):
        o = bpy.data.objects.new(name, cube.data); o.location = loc
        bpy.context.collection.objects.link(o)
    for o in bpy.data.objects:
        if o.type != 'MESH':
            o.hide_set(True)
def s1(): key('NUMPAD_1')
def s2():
    r3 = region().data
    say("numpad 1 -> view", r3.view_perspective, tuple(round(x, 2) for x in r3.view_rotation))
    with bpy.context.temp_override(window=win(), area=area(), region=region()):
        bpy.ops.view3d.view_all(center=False)
    key('Q')
def s3():
    say("Q ->", tool()); key('Q')
def s4():
    say("Q again ->", tool())
    with bpy.context.temp_override(window=win(), area=area(), region=region()):
        bpy.ops.wm.tool_set_by_id(name="builtin.select_box")
    bpy.ops.object.select_all(action='DESELECT')
    # Rectangle around the front cube, cutting through the right cube.
    drag(Vector((-1.5, 0, -1.5)), Vector((3.5, 0, 1.5)))
def s5():
    say("window L->R ->", objs(), "(want Behind, Cube)")
    bpy.ops.object.select_all(action='DESELECT')
    drag(Vector((3.5, 0, 1.5)), Vector((-1.5, 0, -1.5)))
def s6():
    say("crossing R->L ->", objs(), "(want Behind, Cube, Right)")
    bpy.ops.object.select_all(action='DESELECT')
    drag(Vector((5.5, 0, 1.5)), Vector((2.5, 0, -1.5)), ctrl=True)
def s7():
    say("ctrl crossing ->", objs(), "(want Right)")
    move(Vector((0, -1, 0.2)))
def s8():
    from maximize import hover
    say("hover object ->", hover.state["key"], "(want OBJECT Cube)")
    for o in bpy.data.objects: o.select_set(o.name == "Cube")
    bpy.context.view_layer.objects.active = bpy.data.objects["Cube"]
    key('FOUR')
def s9():
    say("level", bpy.context.scene.get("maximize_level"))
    bpy.ops.mesh.select_all(action='DESELECT')
    drag(Vector((-1.5, 0, -1.5)), Vector((1.5, 0, 1.5)))
def s10():
    say("poly window ->", faces(), "faces (want 1, the front face)")
    bpy.ops.mesh.select_all(action='DESELECT')
    drag(Vector((0.5, 0, 1.5)), Vector((-0.5, 0, -1.5)))
def s11():
    say("poly crossing through the middle ->", faces(), "faces (want 1: top and bottom are edge-on)")
    key('TWO')
def s12():
    bpy.ops.mesh.select_all(action='DESELECT')
    drag(Vector((-1.5, 0, 0.5)), Vector((1.5, 0, 1.5)))
def s13():
    say("edge window around the top edge ->", edges(), "edges (want 1)")
    move(Vector((0, -1, 0.95)))
def s14():
    from maximize import hover
    say("hover edge ->", hover.state["key"])
    bpy.ops.wm.quit_blender()
steps = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14]
def run():
    try: steps.pop(0)()
    except Exception:
        import traceback; say("ERR", traceback.format_exc())
    return 0.6 if steps else None
bpy.app.timers.register(run, first_interval=2.0)
