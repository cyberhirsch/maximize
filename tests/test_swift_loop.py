# Run: moritz.exe --factory-startup --enable-event-simulate --python tests/test_swift_loop.py
# (MX_KEYMAP=Max for the Max keymap; Moritz by default. MX_SHOT=<file.png>: a screenshot of the preview.)
# Seb: "swiftloop doesn't do anything yet?" Max's SwiftLoop is a mode started from the Edit Poly
# panel: each click on an edge in the viewport inserts a loop there, until right-click or Esc.
# Shift+click: a flowed loop; Ctrl+click: select the loop; Ctrl+Shift+click: remove it.
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bmesh  # noqa: E402
import bpy  # noqa: E402
from bpy_extras import view3d_utils  # noqa: E402
from maximize.keymaps import activate  # noqa: E402

KEYMAP = os.environ.get("MX_KEYMAP", "Moritz")
failures = []
P = {}


def say(*a): print("MXSWIFT", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", KEYMAP + ":", name, *info)
    if not ok:
        failures.append(name)


def win(): return bpy.context.window_manager.windows[0]
def area(t='VIEW_3D'): return max((a for a in win().screen.areas if a.type == t), key=lambda a: a.width * a.height)
def region(a=None): return [r for r in (a or area()).regions if r.type == 'WINDOW'][-1]
def ev(t, v, x, y, **k): win().event_simulate(type=t, value=v, x=int(x), y=int(y), **k)


def counts():
    bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
    return len(bm.verts), len(bm.edges), len(bm.faces)


def edge_point(index_pick, t=0.5):
    """Screen point on a visible vertical edge of the cube, a fraction t along it."""
    r = region()
    obj = bpy.context.active_object
    bm = bmesh.from_edit_mesh(obj.data)
    mw = obj.matrix_world
    edges = [e for e in bm.edges if abs((e.verts[0].co - e.verts[1].co).normalized().z) > 0.99]
    pts = []
    for e in edges:
        a = view3d_utils.location_3d_to_region_2d(r, r.data, mw @ e.verts[0].co)
        b = view3d_utils.location_3d_to_region_2d(r, r.data, mw @ e.verts[1].co)
        pts.append((a.lerp(b, t), e.index))
    # The front-most edges are the ones with a point nearest the region's bottom-centre.
    pts.sort(key=lambda p: p[0].x)
    co, index = pts[index_pick]
    return r.x + co.x, r.y + co.y


def click(x, y, **mods):
    ev('MOUSEMOVE', 'NOTHING', x, y, **mods)
    ev('LEFTMOUSE', 'PRESS', x, y, **mods)
    ev('LEFTMOUSE', 'RELEASE', x, y, **mods)


def s_setup():
    activate(KEYMAP)
    ev('ESC', 'PRESS', 10, 10)
    ev('ESC', 'RELEASE', 10, 10)
    with bpy.context.temp_override(window=win(), area=area(), region=region()):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.context.tool_settings.mesh_select_mode = (False, True, False)
        bpy.ops.mesh.select_all(action='DESELECT')
    P['before'] = counts()


def s_start():
    # As from the Edit Poly panel: the button sits in the Command Panel, not the viewport.
    props = area('PROPERTIES')
    with bpy.context.temp_override(window=win(), area=props, region=region(props)):
        result = bpy.ops.maximize.swift_loop('INVOKE_DEFAULT')
    say("start", result, [op.bl_idname for op in win().modal_operators])
    P['x'], P['y'] = edge_point(len_edges() // 2)
    ev('MOUSEMOVE', 'NOTHING', P['x'], P['y'])


def len_edges():
    return 4


def s_click1():
    say("modal before click", [op.bl_idname for op in win().modal_operators])
    if os.environ.get("MX_SHOT"):
        # The loop preview under the mouse.
        with bpy.context.temp_override(window=win()):
            bpy.ops.screen.screenshot(filepath=os.environ["MX_SHOT"])
    click(P['x'], P['y'])


def s_after1():
    P['one'] = counts()
    bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
    say("selected after first loop", sum(1 for e in bm.edges if e.select), sum(1 for v in bm.verts if v.select))
    check("a click on an edge inserts a loop", P['one'][2] > P['before'][2], P['before'], "->", P['one'])
    say("modal after click", [op.bl_idname for op in win().modal_operators])
    x, y = edge_point(len_edges() // 2, 0.25)
    click(x, y)


def s_after2():
    P['two'] = counts()
    check("the mode stays: a second click inserts another loop", P['two'][2] > P['one'][2], P['one'], "->", P['two'])
    with bpy.context.temp_override(window=win(), area=area(), region=region()):
        bpy.ops.ed.undo()
    check("one undo per loop", counts() == P['one'], counts())
    # The first loop is selected (Max leaves a new loop selected): Ctrl+click on one of its edges.
    P['lx'], P['ly'] = selected_edge_point()
    click(P['lx'], P['ly'], ctrl=True)


def selected_edge_point():
    r = region()
    obj = bpy.context.active_object
    bm = bmesh.from_edit_mesh(obj.data)
    best = None
    for e in bm.edges:
        if not e.select:
            continue
        co = view3d_utils.location_3d_to_region_2d(r, r.data, obj.matrix_world @ ((e.verts[0].co + e.verts[1].co) / 2))
        d = (co.x + r.x - P['x']) ** 2 + (co.y + r.y - P['y']) ** 2
        if best is None or d < best[0]:
            best = (d, r.x + co.x, r.y + co.y)
    P['loop_len'] = sum(1 for e in bm.edges if e.select)
    return best[1], best[2]


def s_ctrl():
    bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
    sel = sum(1 for e in bm.edges if e.select)
    check("Ctrl+click selects the loop", sel == P['loop_len'] == 4 and counts() == P['one'], sel, P['loop_len'])
    click(P['lx'], P['ly'], ctrl=True, shift=True)


def s_remove():
    check("Ctrl+Shift+click removes the loop", counts() == P['before'], P['before'], "->", counts())
    click(P['x'], P['y'], shift=True)


def s_flow():
    check("Shift+click inserts a loop (flow)", counts()[2] > P['before'][2], counts())
    ev('RIGHTMOUSE', 'PRESS', P['x'], P['y'])
    ev('RIGHTMOUSE', 'RELEASE', P['x'], P['y'])


def s_end_check():
    check("right-click ends the mode", not any("swift" in op.bl_idname.lower()
                                              for op in win().modal_operators),
          [op.bl_idname for op in win().modal_operators])
    say("FAILURES", len(failures), failures)
    bpy.ops.wm.quit_blender()


steps = [s_setup, s_start, s_click1, s_after1, s_after2, s_ctrl, s_remove, s_flow, s_end_check]


def run():
    try:
        steps.pop(0)()
    except Exception as e:
        import traceback
        traceback.print_exc()
        say("ERR", repr(e))
    return 0.6 if steps else None


bpy.app.timers.register(run, first_interval=2.0)
