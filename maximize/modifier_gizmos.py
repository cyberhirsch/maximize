# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Viewport gizmos for deform modifiers, as Max shows on Bend, Twist, Taper and Stretch: drag the
dial (angle) or the arrow (factor) of the active Simple Deform modifier. FFD stays Blender's
Lattice, which is edited directly.
"""

import bpy
from bpy.types import GizmoGroup
from mathutils import Matrix, Vector

_AXIS = {'X': Vector((1, 0, 0)), 'Y': Vector((0, 1, 0)), 'Z': Vector((0, 0, 1))}


def _deform_modifier(obj):
    if obj is None:
        return None
    mod = obj.modifiers.active
    return mod if mod is not None and mod.type == 'SIMPLE_DEFORM' and mod.show_viewport else None


def _matrix(obj, mod):
    """Gizmo frame: at the modifier's origin (or the object), pointing along the deform axis."""
    base = mod.origin.matrix_world if mod.origin is not None else obj.matrix_world
    axis = _AXIS[mod.deform_axis]
    rot = Vector((0, 0, 1)).rotation_difference(base.to_3x3().normalized() @ axis).to_matrix().to_4x4()
    return Matrix.Translation(base.translation) @ rot


class MAXIMIZE_GGT_deform(GizmoGroup):
    bl_idname = "MAXIMIZE_GGT_deform"
    bl_label = "Deform Modifier Gizmo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and _deform_modifier(context.active_object) is not None

    def setup(self, context):
        self.dial = self.gizmos.new("GIZMO_GT_dial_3d")
        self.dial.draw_options = {'ANGLE_VALUE'}
        self.dial.color = (1.0, 0.55, 0.1)
        self.dial.alpha = 0.6
        self.dial.color_highlight = (1.0, 0.8, 0.3)
        self.dial.alpha_highlight = 1.0
        self.dial.scale_basis = 0.8
        self.arrow = self.gizmos.new("GIZMO_GT_arrow_3d")
        self.arrow.color = (1.0, 0.55, 0.1)
        self.arrow.alpha = 0.6
        self.arrow.color_highlight = (1.0, 0.8, 0.3)
        self.arrow.alpha_highlight = 1.0
        self._bound = None
        self.refresh(context)

    def refresh(self, context):
        obj = context.active_object
        mod = _deform_modifier(obj)
        if mod is None:
            return
        uses_angle = mod.deform_method in {'BEND', 'TWIST'}
        if self._bound != (obj.name, mod.name, uses_angle):
            # `angle` is an angle, `factor` a plain number: one gizmo each.
            if uses_angle:
                self.dial.target_set_prop("offset", mod, "angle")
            else:
                self.arrow.target_set_prop("offset", mod, "factor")
            self._bound = (obj.name, mod.name, uses_angle)
        self.dial.hide = not uses_angle
        self.arrow.hide = uses_angle
        matrix = _matrix(obj, mod)
        self.dial.matrix_basis = matrix
        self.arrow.matrix_basis = matrix

    def draw_prepare(self, context):
        self.refresh(context)


classes = (
    MAXIMIZE_GGT_deform,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
