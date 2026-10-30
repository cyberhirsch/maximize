# Run: moritz.exe --factory-startup --enable-event-simulate --python tests/test_suzanne.py
# Teapot and Suzanne are two Standard Primitives buttons (Seb): Suzanne is Blender's monkey as a
# plain mesh, drag-created from the center, named Suzanne001, scale 1 with the size in the mesh.
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bpy  # noqa: E402

failures = []


def say(*a): print("MXSZ", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", name, *info)
    if not ok:
        failures.append(name)


def win(): return bpy.context.window_manager.windows[0]
def area(): return next(a for a in win().screen.areas if a.type == 'VIEW_3D')
def region(): return [r for r in area().regions if r.type == 'WINDOW'][-1]
def ev(t, v, x, y, **k): win().event_simulate(type=t, value=v, x=int(x), y=int(y), **k)


def s_script():
    from maximize import primitives
    check("Suzanne right after Teapot in the Add menu",
          primitives.STANDARD_PRIMITIVES.index('TEAPOT') >= 0 and hasattr(bpy.ops.maximize, "add_suzanne"))
    bpy.ops.maximize.add_suzanne()
    obj = bpy.data.objects.get("Suzanne001")
    check("script: Suzanne001", obj is not None and len(obj.data.vertices) == 507,
          obj and len(obj.data.vertices))
    teapot_icon = next(k[3] for k in primitives.KINDS if k[0] == 'TEAPOT')
    check("Teapot no longer borrows the monkey icon where the build has its own",
          teapot_icon == 'MX_CR_TEAPOT' or 'MX_CR_TEAPOT' not in
          bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items.keys(), teapot_icon)
    ev('ESC', 'PRESS', 10, 10)
    ev('ESC', 'RELEASE', 10, 10)


def s_start():
    r = region()
    with bpy.context.temp_override(window=win(), area=area(), region=r):
        bpy.ops.maximize.add_suzanne('INVOKE_DEFAULT')
    cx, cy = r.x + r.width * 0.5, r.y + r.height * 0.5
    ev('MOUSEMOVE', 'NOTHING', cx, cy)
    ev('LEFTMOUSE', 'PRESS', cx, cy)
    for i in range(1, 6):
        ev('MOUSEMOVE', 'NOTHING', cx + i * 30, cy)
    ev('LEFTMOUSE', 'RELEASE', cx + 150, cy)
    ev('RIGHTMOUSE', 'PRESS', cx + 150, cy)
    ev('RIGHTMOUSE', 'RELEASE', cx + 150, cy)


def s_check():
    obj = bpy.data.objects.get("Suzanne002")
    check("drag: Suzanne002", obj is not None)
    if obj is not None:
        width = max(v.co.x for v in obj.data.vertices) - min(v.co.x for v in obj.data.vertices)
        check("scale 1, size in the mesh", tuple(obj.scale) == (1.0, 1.0, 1.0) and abs(width - 2.734) > 0.01,
              tuple(obj.scale), round(width, 3))
    say("FAILURES", len(failures), failures)
    bpy.ops.wm.quit_blender()


steps = [s_script, s_start, s_check]


def run():
    try:
        steps.pop(0)()
    except Exception as e:
        say("ERR", repr(e))
    return 0.8 if steps else None


bpy.app.timers.register(run, first_interval=2.0)
