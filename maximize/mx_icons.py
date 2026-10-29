# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Moritz's built-in Max icons (MX_...): used where the build has them, else a fallback, so the
add-on still draws in stock Blender and older Moritz builds."""

import bpy

_names = None


def _icon_names():
    global _names
    if _names is None:
        enum = bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items
        _names = frozenset(enum.keys())
    return _names


def has_icon(name):
    """Whether `name` is an icon of this build."""
    return name in _icon_names()


def mx_icon(name, fallback='NONE'):
    """`name` if this build has that icon, else `fallback` (a stock icon or 'NONE')."""
    return name if has_icon(name) else fallback
