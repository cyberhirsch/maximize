-- SPDX-FileCopyrightText: 2026 Moritz Authors
-- SPDX-License-Identifier: GPL-2.0-or-later
--
-- Moritz Scene Export for 3ds Max (2018 and later).
-- Writes the scene to a .mxscene file (JSON) that Moritz imports with File > Import >
-- Max Scene (.mxscene): meshes as polygons with UVs, material IDs and smoothing groups, the
-- hierarchy and pivots, layers, hidden and frozen state, wire colors, cameras, lights, and every
-- material with all of its parameters and maps (V-Ray, Corona, Physical, Standard, Multi/Sub),
-- which Moritz converts to its own materials.
--
-- Run: Scripting > Run Script..., pick this file, choose where to save. Exports the selection if
-- there is one, else the whole scene. Modifiers are collapsed into the exported mesh (the scene
-- is not changed).

(
    -- Declared first: the functions below call each other (and themselves).
    local mxEscape, mxStr, mxNum, mxColor, mxPoint3, mxMatrix
    local mxValue, mxParams, mxTexmap, mxMaterialId, mxMesh, mxKind, mxNode

    -- ------------------------------------------------------------------ JSON writing
    fn mxEscape s =
    (
        local out = stringStream ""
        for i = 1 to s.count do
        (
            local c = s[i]
            case c of
            (
                "\"": format "\\\"" to:out
                "\\": format "\\\\" to:out
                "\n": format "\\n" to:out
                "\r": format "\\r" to:out
                "\t": format "\\t" to:out
                default: format "%" c to:out
            )
        )
        out as string
    )

    fn mxStr s = "\"" + (mxEscape (s as string)) + "\""

    fn mxNum v =
    (
        -- Plain decimal, no locale or exponent surprises.
        local s = formattedPrint (v as float) format:".7g"
        if (findString s "nan" != undefined) or (findString s "inf" != undefined) then "0" else s
    )

    fn mxColor c = "[" + (mxNum (c.r / 255.0)) + "," + (mxNum (c.g / 255.0)) + "," + (mxNum (c.b / 255.0)) + "]"

    fn mxPoint3 p = "[" + (mxNum p.x) + "," + (mxNum p.y) + "," + (mxNum p.z) + "]"

    fn mxMatrix tm =
    (
        -- Rows: X, Y, Z axes and translation (Max row-vector convention).
        "[" + (mxPoint3 tm.row1) + "," + (mxPoint3 tm.row2) + "," + (mxPoint3 tm.row3) + "," + (mxPoint3 tm.row4) + "]"
    )

    -- ------------------------------------------------------------------ materials and maps
    local mxMaterials = #()      -- exported materials, index = id
    local mxMaterialJson = #()

    fn mxValue v depth =
    (
        -- A parameter value as JSON, or undefined to skip it.
        case (classOf v) of
        (
            Float: mxNum v
            Integer: (v as string)
            BooleanClass: (if v then "true" else "false")
            Color: mxColor v
            Point3: mxPoint3 v
            String: mxStr v
            default:
            (
                if (superClassOf v) == textureMap and depth < 6 then mxTexmap v (depth + 1)
                else undefined
            )
        )
    )

    fn mxParams obj depth =
    (
        local out = stringStream ""
        format "{" to:out
        local first = true
        for p in (getPropNames obj) do
        (
            local v = undefined
            try (v = getProperty obj p) catch (v = undefined)
            if v != undefined then
            (
                local j = undefined
                try (j = mxValue v depth) catch (j = undefined)
                if j != undefined then
                (
                    if not first then format "," to:out
                    format "%:%" (mxStr (p as string)) j to:out
                    first = false
                )
            )
        )
        format "}" to:out
        out as string
    )

    fn mxTexmap t depth =
    (
        local out = stringStream ""
        format "{\"class\":%,\"name\":%" (mxStr ((classOf t) as string)) (mxStr t.name) to:out
        local file = undefined
        try (file = t.filename) catch ()
        if file == undefined then try (file = t.HDRIMapName) catch ()
        if file != undefined and file != "" then
        (
            local resolved = mapPaths.getFullFilePath file
            if resolved == undefined or resolved == "" then resolved = file
            format ",\"file\":%" (mxStr resolved) to:out
        )
        format ",\"params\":%}" (mxParams t depth) to:out
        out as string
    )

    fn mxMaterialId m =
    (
        -- Export a material once and return its index (0-based), -1 for none.
        if m == undefined then return -1
        local found = findItem mxMaterials m
        if found > 0 then return (found - 1)
        append mxMaterials m
        local index = mxMaterials.count - 1
        append mxMaterialJson ""
        local out = stringStream ""
        format "{\"class\":%,\"name\":%" (mxStr ((classOf m) as string)) (mxStr m.name) to:out
        if (classOf m) == Multimaterial then
        (
            format ",\"sub\":[" to:out
            for i = 1 to m.materialList.count do
            (
                if i > 1 then format "," to:out
                local id = m.materialIDList[i]
                format "{\"id\":%,\"material\":%}" id (mxMaterialId m.materialList[i]) to:out
            )
            format "]" to:out
        )
        format ",\"params\":%}" (mxParams m 0) to:out
        mxMaterialJson[index + 1] = out as string
        index
    )

    -- ------------------------------------------------------------------ geometry
    fn mxMesh obj =
    (
        -- The object's final mesh as polygons, in the node's own space.
        local snap = snapshot obj
        convertToPoly snap
        local inv = inverse obj.transform
        local out = stringStream ""
        local nv = polyop.getNumVerts snap
        local nf = polyop.getNumFaces snap
        format "{\"verts\":[" to:out
        for v = 1 to nv do
        (
            if v > 1 then format "," to:out
            format "%" (mxPoint3 ((polyop.getVert snap v) * inv)) to:out
        )
        format "],\"faces\":[" to:out
        for f = 1 to nf do
        (
            if f > 1 then format "," to:out
            local fv = polyop.getFaceVerts snap f
            format "[" to:out
            for k = 1 to fv.count do
            (
                if k > 1 then format "," to:out
                format "%" (fv[k] - 1) to:out
            )
            format "]" to:out
        )
        format "],\"mat_ids\":[" to:out
        for f = 1 to nf do
        (
            if f > 1 then format "," to:out
            format "%" (polyop.getFaceMatID snap f) to:out
        )
        format "],\"smoothing\":[" to:out
        for f = 1 to nf do
        (
            if f > 1 then format "," to:out
            -- Unsigned, as a plain number (bit 32 makes it negative in MaxScript).
            local sg = polyop.getFaceSmoothGroup snap f
            if sg < 0 then sg = sg + 4294967296.0
            format "%" (formattedPrint (sg as float) format:".0f") to:out
        )
        format "]" to:out
        -- UV channel 1, per face corner.
        if (polyop.getMapSupport snap 1) then
        (
            format ",\"uv_verts\":[" to:out
            local nm = polyop.getNumMapVerts snap 1
            for v = 1 to nm do
            (
                if v > 1 then format "," to:out
                local uv = polyop.getMapVert snap 1 v
                format "[%,%]" (mxNum uv.x) (mxNum uv.y) to:out
            )
            format "],\"uv_faces\":[" to:out
            for f = 1 to nf do
            (
                if f > 1 then format "," to:out
                local mf = polyop.getMapFace snap 1 f
                format "[" to:out
                for k = 1 to mf.count do
                (
                    if k > 1 then format "," to:out
                    format "%" (mf[k] - 1) to:out
                )
                format "]" to:out
            )
            format "]" to:out
        )
        format "}" to:out
        delete snap
        out as string
    )

    fn mxKind obj =
    (
        case (superClassOf obj) of
        (
            camera: "CAMERA"
            light: "LIGHT"
            shape:
            (
                local renderable = false
                try (renderable = obj.render_renderable) catch ()
                if renderable and (canConvertTo obj Editable_Poly) then "MESH" else "SHAPE"
            )
            GeometryClass: (if (canConvertTo obj Editable_Poly) then "MESH" else "EMPTY")
            helper: "EMPTY"
            default: "EMPTY"
        )
    )

    fn mxNode obj =
    (
        local out = stringStream ""
        local kind = mxKind obj
        format "{\"name\":%,\"class\":%,\"kind\":%" (mxStr obj.name) (mxStr ((classOf obj) as string)) (mxStr kind) to:out
        format ",\"parent\":%" (if obj.parent != undefined then mxStr obj.parent.name else "null") to:out
        -- Max allows duplicate names: handles are unique.
        format ",\"handle\":%" obj.inode.handle to:out
        if obj.parent != undefined then format ",\"parent_handle\":%" obj.parent.inode.handle to:out
        format ",\"transform\":%" (mxMatrix obj.transform) to:out
        format ",\"layer\":%" (mxStr obj.layer.name) to:out
        format ",\"hidden\":%,\"frozen\":%" (if obj.isHidden then "true" else "false") (if obj.isFrozen then "true" else "false") to:out
        format ",\"wirecolor\":%" (mxColor obj.wirecolor) to:out
        format ",\"renderable\":%" (if obj.renderable then "true" else "false") to:out
        if kind == "MESH" then
        (
            format ",\"material\":%" (mxMaterialId obj.material) to:out
            format ",\"mesh\":%" (mxMesh obj) to:out
        )
        if kind == "CAMERA" then
        (
            local fov = 45.0
            try (fov = obj.fov) catch ()
            format ",\"fov\":%" (mxNum fov) to:out
            local target = undefined
            local target_handle = undefined
            try (if obj.target != undefined then (target = obj.target.name; target_handle = obj.target.inode.handle)) catch ()
            if target != undefined then format ",\"target\":%" (mxStr target) to:out
            if target_handle != undefined then format ",\"target_handle\":%" target_handle to:out
        )
        if kind == "LIGHT" then
        (
            format ",\"light\":%" (mxParams obj 0) to:out
        )
        format "}" to:out
        out as string
    )

    -- ------------------------------------------------------------------ main
    -- MORITZ_EXPORT_PATH set: no dialog (3dsmaxbatch.exe moritz_export.ms -sceneFile scene.max).
    local path = systemTools.getEnvVariable "MORITZ_EXPORT_PATH"
    if path == undefined or path == "" then
        path = getSaveFileName caption:"Export for Moritz" types:"Max Scene for Moritz (*.mxscene)|*.mxscene|"
    if path != undefined then
    (
        local nodes = if selection.count > 0 then (selection as array) else (objects as array)
        local start = timeStamp()
        local nodeJson = #()
        progressStart "Export for Moritz"
        for i = 1 to nodes.count do
        (
            append nodeJson (mxNode nodes[i])
            if not (progressUpdate (100.0 * i / nodes.count)) then exit
        )
        progressEnd()

        local f = createFile path encoding:#utf8
        format "{\"format\":\"mxscene\",\"version\":1" to:f
        format ",\"max_version\":%" ((maxVersion())[1]) to:f
        format ",\"file\":%" (mxStr (maxFilePath + maxFileName)) to:f
        -- System units in one centimeter (Moritz scales to meters).
        format ",\"units_per_cm\":%" (mxNum (units.decodeValue "1cm")) to:f
        format ",\"system_unit\":%" (mxStr (units.SystemType as string)) to:f
        format ",\"system_scale\":%" (mxNum units.SystemScale) to:f
        format ",\"renderer\":%" (mxStr ((classOf renderers.current) as string)) to:f
        format ",\"nodes\":[" to:f
        for i = 1 to nodeJson.count do
        (
            if i > 1 then format ",\n" to:f
            format "%" nodeJson[i] to:f
        )
        format "],\"materials\":[" to:f
        for i = 1 to mxMaterialJson.count do
        (
            if i > 1 then format ",\n" to:f
            format "%" mxMaterialJson[i] to:f
        )
        format "]}\n" to:f
        close f
        format "Moritz export: % nodes, % materials in % s -> %\n" nodeJson.count mxMaterialJson.count ((timeStamp() - start) / 1000.0) path
    )
)
