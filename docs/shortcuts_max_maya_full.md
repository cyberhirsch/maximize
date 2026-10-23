# 3ds Max and Maya default shortcuts: complete reference

Companion to `shortcuts.md` for the Moritz keymap work. This file stands on its own: it repeats every 3ds Max and Maya binding from `shortcuts.md` and adds the editor- and tool-specific tables that the first pass skipped.

- **Compiled:** 2026-10-23
- **3ds Max:** 2026 (primary), checked against 2027.
- **Maya:** 2026 (primary), checked against 2027.
- **Method:** the Autodesk Help table-of-contents files (`help.autodesk.com/view/3DSMAX/2026/ENU/data/toctree.json`, `help.autodesk.com/view/MAYAUL/2026/ENU/data/toctree.json` and `help.autodesk.com/view/MAXDEV/2026/ENU/data/toctree.json`) list every page in the Max, Maya (including Bifrost, LookdevX and USD) and MAXScript help. All 10,962 Max and Maya pages listed there (raw CloudHelp HTML) were downloaded and searched for key names (Ctrl+, Shift+, Alt+, "Keyboard shortcut:", "Hotkey:", "Default key", "press X"). Every hit page was read, and its bindings are listed below with that page as the source.
- **2026 vs 2027:** the 2027 versions of every dedicated shortcut page were downloaded from the 2027 TOC (Max 2027 moved to `.../2027/ENU/3dsMax-Basics/files/<folder>/GUID-....html` paths) and diffed against 2026. **3ds Max:** no binding differs. **Maya:** no binding differs. 2027 adds a Walk Tool table to "Tool and action hotkeys" / "All Maya Hotkeys" and rewords some playback descriptions (marked below).

### Legend

- **—** = the official docs list the action but give no default key.
- **†** = not from an official Autodesk page for this version (secondary source). No table row below needs it: every binding in the tables comes from Autodesk Help 2026/2027. The two † items from `shortcuts.md` (Maya 2014-only keys) appear only in the closing section.
- **LMB / MMB / RMB** = left / middle / right mouse button. **[hold]** = hold the key while doing something else. `A / B` in one cell = two shortcuts in the order of the action text.
- **Override** = 3ds Max context shortcuts (Editable Poly, Unwrap, Track View and others) only work while the **Keyboard Shortcut Override Toggle** is on, which is the default.
- **Conflict** notes mark places where two official Autodesk pages give different keys for the same action. The main shortcut tables are the more reliable source; the feature pages are often older.

### Sources

3ds Max 2026 (Autodesk Help, raw CloudHelp HTML):

- Keyboard Shortcut Tables (main reference; Main UI, Edit, Schematic View, Track View, UVW Unwrap, Material Editor/SME, Biped, Hair Styling, Particle Flow, SteeringWheels/ViewCube/Walkthrough, Misc): https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Basics/files/GUID-A73E1B09-7BFE-4A22-8153-1D3D2237B8E9.htm
- Same page, 2027 (identical): https://help.autodesk.com/cloudhelp/2027/ENU/3dsMax-Basics/files/keyboard_shortcuts/GUID-A73E1B09-7BFE-4A22-8153-1D3D2237B8E9.html
- Keyboard Shortcuts (overview): https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Basics/files/GUID-AA36F53A-96A9-49A9-B66E-58A13AA788F9.htm
- Default Hotkey Maps (images only, not parsed): https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Basics/files/GUID-6D38579A-C018-47F6-AC57-2578CF903F2D.htm
- Keyboard Shortcut Override Toggle: https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Basics/files/GUID-C14C1D13-0E8E-4471-9671-077FDFB156C8.htm
- Hotkey Editor: https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Basics/files/GUID-236F4053-D509-4133-A709-5DF8554EB8D3.htm
- Additional Keyboard Commands: https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Basics/files/GUID-0CE50884-27AC-4528-89DA-DCB3C77D2411.htm
- Interaction Mode Preferences (Maya-mode differences): https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Customizing/files/GUID-9DF0E9DB-F68E-448D-BB9E-C75CA85B6E70.htm
- Mouse Panel: https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Customizing/files/GUID-75E03BAB-0D94-43E0-B281-3AE3299BD2B9.htm
- Zoom / Orbit / Pan View / Select Object / Shift+Clone / Track Bar: https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Basics/files/GUID-CCD2C70B-52B4-4BF0-A5C0-74ECC591ACDD.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Basics/files/GUID-6DA741AB-9941-4957-903A-4B998C1C65E7.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Basics/files/GUID-802A4CCA-1695-4D91-BC30-9A4C0DAEEE5F.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Basics/files/GUID-6CEB9419-A182-430C-9C6C-FEE5799324E0.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Basics/files/GUID-03F84C88-6EEC-42A4-BCB9-C487243E7B99.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Basics/files/GUID-A55E4702-263E-4768-9964-5866698784DA.htm
- Setting Viewport Layout (view keys incl. B): https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Basics/files/GUID-26518D1C-3F68-4D77-AAD1-3A78F0948B5C.htm
- Viewport's General Menu: https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Basics/files/GUID-6C424DA3-B0AA-406A-9DD5-D111CB680366.htm
- Point-Of-View Viewport Label Menu: https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Basics/files/GUID-F86CB637-685E-4874-82C5-CFACB8486D35.htm
- Active Viewport: Preferences Tab / Filter Tab: https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Basics/files/GUID-9AD2FCC5-0DB0-4F5F-A4A1-59C0ED4F7A01.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Basics/files/GUID-032D8548-DCE7-48D7-9A42-9E827EF7149B.htm
- Special Controls (spinners): https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Basics/files/GUID-FD2F49B2-B86F-445B-AE4B-03F020671485.htm
- Snap Options / Snap Working Pivot: https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Basics/files/GUID-47E8B8FB-6A32-44DA-AFF1-6D959B1E45F9.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Animation/files/GUID-CE2E524E-1AA0-4AC6-91E1-5A0047B3F059.htm
- Additional Quad Menus: https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Basics/files/GUID-B913CA16-7AA0-4477-85F8-38BC9519AE75.htm
- Using Walkthrough Navigation: https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Basics/files/GUID-5B06CB73-DEA7-465E-9C6F-B8E7D454A7FB.htm
- Editable Poly (Vertex) / Chamfer caddy / Editable Spline (Segment) / Edit Spline: https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Modeling/files/GUID-047B00EC-D4E3-4D05-8FB7-220795D13874.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Modeling/files/GUID-FB852041-9E26-4F4A-9E17-154CD4CB504A.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Modeling/files/GUID-E7E1EBFF-5371-4835-8B7C-A34FEE225F15.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Modifiers/files/GUID-56489D31-EB66-413C-B30E-EC5193D20519.htm
- Graphite Freeform: Paint Deform / PolyDraw (Add Geometry & Optimize, Drag & Conform, Create Geometry) / Edit Panel / Shift, Conform, UV Tweak options: https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Modeling/files/GUID-CA6D812A-C92B-4037-8810-E0257C6B61AE.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Modeling/files/GUID-3861007B-2549-4770-8E6F-AACC65DF50AE.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Modeling/files/GUID-96452030-B2E8-404A-AF0E-4EB70EB44EE6.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Modeling/files/GUID-9FDF41F1-C576-4888-B183-78706E5EAEC0.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Modeling/files/GUID-6DFFC234-217F-494D-A76E-D62158E91C98.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Modeling/files/GUID-69783BDB-645B-48E5-BF48-6989613B464E.htm
- NURBS: Display Controls / Surface Approximation / Surface CV sub-objects / Sub-Object Selection: https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Modeling/files/GUID-AF520FBC-EDC5-4D6F-A05B-D8CF2530455A.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Modeling/files/GUID-A66E61B1-8B69-4A61-A7AF-40C8927DA00E.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Modeling/files/GUID-3BFAD865-B647-4447-B7A2-0FA5FE47D886.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Modeling/files/GUID-AC4156BE-3110-4105-8FF2-F6279E16FD5A.htm
- Edit Normals Modifier Reference: https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Modifiers/files/GUID-82722323-100B-4711-A01D-8A87EB53DD96.htm
- Unwrap UVW Shortcuts (UV Editor) / Edit UVWs Dialog Toolbars: https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Modifiers/files/GUID-86034121-F9ED-487C-A49F-45299FF7BFE1.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Modifiers/files/GUID-C65A1B09-3670-4E7E-BCFC-13E10C831817.htm
- Skin Modifier Reference / Parameters Rollout / Weight Table: https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Modifiers/files/GUID-058A01D0-263D-48C0-9BF1-ABFEC2359F86.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Modifiers/files/GUID-0D847E14-366A-4629-A87A-D24CAF591226.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Modifiers/files/GUID-9DE90E0E-C0E1-4E30-B4EC-BC4169917B28.htm
- Slate Material Editor: Toolbar / Select / View / Edit / Tools / Options menus / Navigation Buttons / Named Views / Selecting, Moving, Laying Out Nodes / Navigating: https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Lighting-Shading/files/GUID-14FB4E2C-0F6F-4C13-8EDE-BAEEECA67117.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Lighting-Shading/files/GUID-C8BB54F7-06D2-4680-BB06-C7FB0C33A020.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Lighting-Shading/files/GUID-A2F64022-28E4-4CEA-B004-FD4D4546C7C9.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Lighting-Shading/files/GUID-26505115-1469-41BD-AD99-F97B9B97976B.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Lighting-Shading/files/GUID-91C03DEF-08BC-4B41-9DC8-E958B8CEE82A.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Lighting-Shading/files/GUID-A8B9DB8C-1B38-44B6-BED1-40F1D09921EC.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Lighting-Shading/files/GUID-87AB3A91-B15A-451A-AF67-3585826D3B5F.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Lighting-Shading/files/GUID-776219E5-68B1-4C5E-BFBD-16677B219243.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Lighting-Shading/files/GUID-0EF7EBB0-31DC-4602-9E74-67BABB4E8F6F.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Lighting-Shading/files/GUID-B3AA923F-0A2E-4D2C-9A11-7CE8A3DF4C6E.htm
- Using the Keyboard to Navigate the Material/Map List: https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Lighting-Shading/files/GUID-280C32DC-2C34-4207-BF36-6E0512C3A6CC.htm
- Viewport Canvas: https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Lighting-Shading/files/GUID-F5518487-A253-44F0-A8D9-9CB537A8F392.htm
- RAM Player Keyboard Shortcuts / To Zoom and Pan in the Rendered Frame Window / About ActiveShade: https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Rendering/files/GUID-492C97E4-E588-4B8B-A978-21E9FEA7C83F.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Rendering/files/GUID-15B2D9F0-22BA-49EE-9EF4-947668BD4B7F.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Rendering/files/GUID-DDD521BE-16A3-4E43-AE40-6B38E588C13A.htm
- Baking to Texture: https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Rendering/files/GUID-B67A2495-89E4-464A-8913-35C957E950EB.htm
- Biped Keyboard Shortcuts / Setting Keys for Feet and Hands / Previewing Biped Motion / Creating Footsteps Manually / Copying and Pasting Postures: https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Character-Animation/files/GUID-4C4D93FC-05AB-4A2D-A291-B3B682D98B66.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Character-Animation/files/GUID-4AAD5905-A21A-4AC2-AB6C-6765D79F00F4.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Character-Animation/files/GUID-1084BECD-FD13-4898-A853-56C8DE78360A.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Character-Animation/files/GUID-9DCC165A-AEAF-451F-8C43-1BF7092723B9.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Character-Animation/files/GUID-40250A36-E2F9-41A7-8D49-5A0B700C0152.htm
- Populate: Define Idle Areas Panel: https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Character-Animation/files/GUID-136A2671-6432-49B0-A253-925DB2500346.htm
- Physique Shortcuts / Crowd Shortcuts (Archive book): https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Archive/files/GUID-1717C210-FA2E-4E99-ACDF-C6E029016AC3.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Archive/files/GUID-21BC3067-D6B5-4D62-BBB1-D1770278D3F4.htm
- Particle Flow Keyboard Shortcuts / Data View Hotkeys: https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Simulation-Effects/files/GUID-65881096-36F7-4970-8250-6AE3A77166A8.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Simulation-Effects/files/GUID-8B0604AD-7C79-4EC6-97EA-424850544A31.htm
- Styling Rollout (Hair And Fur): https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Simulation-Effects/files/GUID-E7442225-7A7F-46AF-B4CC-D326F6755E16.htm
- Track View: Pan / Zoom Key Window / Quad Menus / Hierarchy: https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Animation/files/GUID-8C676182-0B91-46A3-AEFF-D598BC17D01D.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Animation/files/GUID-BD4B7491-D7DF-4531-A97E-BCE6A6B17FBC.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Animation/files/GUID-4DFE3869-A0FE-4AEE-836C-59B774215151.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Animation/files/GUID-414977F3-56B6-479B-94CE-3442B744CADF.htm
- Camera Tracker: Movie Window: https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Animation/files/GUID-7ACA788D-6EAF-46FB-91E8-E4F2E24D92A8.htm
- Scene Explorer / Scene Explorer Toolbars / Panning and Zooming the Track Window (State Sets): https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Manage-Scenes/files/GUID-2569461E-C859-4D54-BAFF-C8BD078B53AC.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Manage-Scenes/files/GUID-12DA4CA4-95D4-4B06-8AFC-B3F3E9AD55D1.htm , https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Manage-Scenes/files/GUID-E1E625AB-195B-4A65-A98D-26C23EDC53F4.htm
- Save Incremental (+): https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Manage-Scenes/files/GUID-F7489795-9716-4FA1-AA24-F731A0C1CE00.htm
- Retopology Tools for 3ds Max: https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Retopology/files/GUID-57B77A00-5300-47CB-99E1-22B9C536B060.html
- MAXScript: Scripting Editor - Keyboard Shortcuts (2026 and 2027 identical): https://help.autodesk.com/cloudhelp/2026/ENU/MAXScript-Help/files/MAXScript-Introduction/The-MAXScript-Editor/GUID-B79B2059-FEAA-4939-8C83-7A04A53FBCE7.html
- MAXScript: Listener Commands / The Scripting Listener Window: https://help.autodesk.com/cloudhelp/2026/ENU/MAXScript-Help/files/MAXScript-Introduction/Accessing-MAXScript/GUID-8079981C-344A-47C2-B5CB-4D03B6B68FDC.html , https://help.autodesk.com/cloudhelp/2026/ENU/MAXScript-Help/files/MAXScript-Introduction/Accessing-MAXScript/GUID-81403EB7-94F8-4EAA-8026-1A495343AE06.html

Maya 2026 (Autodesk Help, raw CloudHelp HTML):

- All Maya Hotkeys: https://help.autodesk.com/cloudhelp/2026/ENU/Maya-KeyboardShortcuts/files/GUID-30CACC9D-8FBE-4B85-8A8F-C5ADF32DDD4E.htm
- All Maya Hotkeys 2027 (adds Walk Tool): https://help.autodesk.com/cloudhelp/2027/ENU/Maya-KeyboardShortcuts/files/GUID-30CACC9D-8FBE-4B85-8A8F-C5ADF32DDD4E.htm
- Category pages: Animation, Camera, Display, Edit operation, File operation, Interface, Modeling, Modeling Toolkit, Paint operation, Rendering, Sculpting tool, Selection, Snapping, Tool and action, Transformation, UV Editor, View hotkeys, Marking Menus: https://help.autodesk.com/cloudhelp/2026/ENU/Maya-KeyboardShortcuts/files/GUID-0639ADA0-EBE5-4703-A874-92C80E4A0516.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-KeyboardShortcuts/files/GUID-0DF7D2C9-1633-411F-BCA3-93302BE20676.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-KeyboardShortcuts/files/GUID-3A9207E3-6A7F-4C95-A5F3-6D5269F8F018.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-KeyboardShortcuts/files/GUID-FA8B2362-4397-43B0-8C92-1DE7D606FFF5.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-KeyboardShortcuts/files/GUID-4A6B0D91-7886-4CE0-A1C3-C6BA5166BBB2.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-KeyboardShortcuts/files/GUID-F5379746-7A11-48C0-AFBA-D4B333D3B63A.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-KeyboardShortcuts/files/GUID-0B937D23-49D1-47D4-9B81-3356BA7FD815.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-KeyboardShortcuts/files/GUID-DAD42E62-3E23-4A00-93E9-4F4A193F3057.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-KeyboardShortcuts/files/GUID-5688C9F5-A20B-4415-8479-4AA9E49EA416.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-KeyboardShortcuts/files/GUID-802C6C51-2427-41E9-A69A-70ECEA4822EA.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-KeyboardShortcuts/files/GUID-C53434C7-0A0D-4DF8-BB9A-BF60DE751987.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-KeyboardShortcuts/files/GUID-03CE3BF0-E4E9-4495-81A0-CE06FFA5C973.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-KeyboardShortcuts/files/GUID-6B53E985-7407-4763-B5A2-A64E92745341.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-KeyboardShortcuts/files/GUID-8370FB55-6BE6-4571-872B-F8291A187EC0.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-KeyboardShortcuts/files/GUID-25CEBBA0-3779-41DF-B944-CA7AD6FB76F0.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-KeyboardShortcuts/files/GUID-0AFB7E06-7F51-4D4D-A3DD-E0221CDF73AB.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Basics/files/GUID-8D330D02-98DC-441F-872E-4648BC23DCFF.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Basics/files/GUID-8BA1A3AA-4C44-4779-8B22-0AAE3627E8EB.htm
- Node Editor and Hypershade Hotkeys / Node Editor marking menus / Zooming in the Node Editor: https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Basics/files/GUID-8E175070-AB7C-41A2-B0D7-85E842F83C4E.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Basics/files/GUID-B99E6112-CECD-4F1A-8520-265C1407E904.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Basics/files/GUID-EBC629FE-0075-42BF-816F-9DEFFD17D6FC.htm
- Hypershade: Create and connect nodes / View menu: https://help.autodesk.com/cloudhelp/2026/ENU/Maya-LightingShading/files/GUID-F90898A6-55E7-47EA-8542-8A9FD9CBC561.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-LightingShading/files/GUID-DBE3FA18-FC27-4768-8E69-8C0D28E3EB53.htm
- Tumble, track, dolly, roll, or zoom the camera / Camera Tools menu / Dolly Tool options / Walk through the scene: https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Basics/files/GUID-941480C1-9BDA-4DB3-8EA8-113A0D6FAF1F.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Basics/files/GUID-DDE25A30-0D59-4F92-8150-98DD12EF39DE.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Basics/files/GUID-A2851E8C-A4EE-4546-B383-27D9CB530AB8.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Basics/files/GUID-8700421A-4CAC-4936-BA2C-BC400FAE5CAE.htm
- Select menu / Display menu / Panel menu: View / Panel menu: Show / Show or hide components / Show Options / Search: https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Basics/files/GUID-D1BBC051-0EE7-4A91-B4FF-2A369764EC8B.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Basics/files/GUID-0657DA41-332E-4F3C-BDAE-4A9AD8CA2553.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Basics/files/GUID-6C1FACC3-8B01-45CB-8458-581DFAFC2A2F.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Basics/files/GUID-A15B3808-D3C4-482F-98DD-BC7F45E13A36.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Basics/files/GUID-EBB179AA-9F3A-4386-8D25-B22881E27CD0.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Basics/files/GUID-635B5352-D075-40F7-A23B-ACE219A14194.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Basics/files/GUID-A41539AD-F566-4F3D-8671-FE6237BB3C2B.htm
- Change the pivot point / Move objects / Scale objects: https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Basics/files/GUID-150B390E-840B-4FE3-B8E9-8DEBCE7CEC97.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Basics/files/GUID-ABF1A141-7860-4234-889B-00278F20B9A3.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Basics/files/GUID-09D0E733-74DF-44E2-937A-C857001E45B2.htm
- Outliner / Attribute Editor: https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Basics/files/GUID-4B9A9A3A-83C5-445A-95D5-64104BC47406.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Basics/files/GUID-67A58D31-4722-4769-B3E6-1A35B5B53BED.htm
- Playback Controls / Time Slider: https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Basics/files/GUID-277ADCBF-6277-4B32-81E0-AEB6D081153F.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Basics/files/GUID-827ED8CD-C6AA-4495-8B5E-2FC98C8D49EE.htm
- Graph Editor / Graph Editor Tangents, Keys, Select menus / Curve Sculpting: https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Animation/files/GUID-6D38EAEA-6032-471E-BD0E-54A74D4443C0.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Animation/files/GUID-43A4FE2C-4863-4EA6-B6AE-6D2B6757F6C7.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Animation/files/GUID-C51CDB66-E4C8-45C7-9F77-BC43343B2559.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Animation/files/GUID-6ADB00F9-FDCB-44F6-A31C-2A240CB78186.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Animation/files/GUID-CC09AB35-363D-4154-9F15-99286CA5A261.htm
- Dope Sheet Editor / Edit, View, Channels menus / toolbar: https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Animation/files/GUID-266E7597-25F5-44B7-96AF-FFB248AE4802.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Animation/files/GUID-7461A3E5-F181-4A85-9AAA-D537E1FC9399.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Animation/files/GUID-BCBE5E7E-19A3-47BD-9511-131DBE8BD26F.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Animation/files/GUID-94288D17-9A2B-44FB-8FD3-53FAD77B0BB1.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Animation/files/GUID-231A20E8-5EBD-476D-88BC-704901A5E682.htm
- Time Slider Bookmark menu / Animation controls menu / Time Slider Bookmarks: https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Animation/files/GUID-1B4F8DB8-8DAF-4BD1-AC21-D27DB043998F.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Animation/files/GUID-4A45C257-9E4D-4C63-A181-B2F94EA0C8B4.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Animation/files/GUID-E15891DF-BC48-43B4-BD03-08918CD4D0C0.htm
- Time Editor: toolbar / Current Time Marker / Edit animation; Trax: time warps: https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Animation/files/GUID-6137119F-CEDF-4998-BF76-C946722C9EE8.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Animation/files/GUID-6E47AC53-AD96-4824-BB4A-7C5556444EB1.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Animation/files/GUID-86B70295-2A93-458C-9D3E-F153EB048E5B.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Animation/files/GUID-49F66888-EE6D-4755-BD7C-60435EE7703E.htm
- Camera Sequencer: https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Animation/files/GUID-FDCA1426-D7FE-41A5-9563-5628C736BCCC.htm
- Blue Pencil / Blue Pencil Marking menu / Transform mode: https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Animation/files/GUID-67EA4E70-9FF6-491B-8874-7D89C269B2A3.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Animation/files/GUID-56B1204A-49AE-4605-AEEE-93323E5462D9.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Animation/files/GUID-18E6A540-99AC-438D-9A60-378160D3629C.htm
- Multi-Cut Tool hotkeys / Quad Draw Tool hotkeys / Quad Draw marking menu / Relax with Quad Draw: https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Modeling/files/GUID-21E402B5-1ABF-4DD3-A9CE-8B7957F6DF2B.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Modeling/files/GUID-ED28E6BC-6141-491C-8C1B-2AE6FC813284.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Modeling/files/GUID-6DF18DAC-20F8-4D3E-BE66-3330FBE095D2.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Modeling/files/GUID-171B1A46-C616-4D92-83D8-C6440A51264C.htm
- Extrude / Edit Mesh menu / Target Weld / Connect Tool / In-View Editor / Smooth Mesh / Subdiv proxy overview: https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Modeling/files/GUID-77FF95F8-13E8-48A6-BF82-84078E1F4FD3.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Modeling/files/GUID-8FF5F5FC-2065-438A-AFC8-65A17FA7842F.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Modeling/files/GUID-F1BFED46-9277-4B01-93A8-37946E110007.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Modeling/files/GUID-86D1DC81-4016-4508-9AAF-956D9F8DF6A4.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Modeling/files/GUID-C9C88AA3-CE61-4389-9A19-B6456427EBA2.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Modeling/files/GUID-FF35F773-1FC0-4EBA-A64C-6199375F489A.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Modeling/files/GUID-196DCBDA-4A3D-4D48-904F-D38D8267E07E.htm
- UV Editor overview / UV Editor marking menus / 3D Cut and Sew UV Tool / Select edge rings, loops, shells in the UV Editor / Separate and attach UVs / UV menu / Symmetrize, Smear, Pinch, Pin UV tools: https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Modeling/files/GUID-73BF7546-3BF2-44F3-9192-15A024CEC173.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Modeling/files/GUID-D60FE3EC-401D-4E83-B309-D53D9ED9BD14.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Modeling/files/GUID-4BDF2BD4-1238-478E-8F37-9043E31345F3.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Modeling/files/GUID-6815200E-5E22-49E3-A91D-83E0EEE098D5.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Modeling/files/GUID-954B5123-F4A6-4E3E-9966-642BBA85D2FE.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Modeling/files/GUID-C4E40AB6-17AB-4FC6-8D53-AFBD96D9B322.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Modeling/files/GUID-578193DB-7EE7-4C60-A26F-9187DF8614A3.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Modeling/files/GUID-3100AC8D-C82C-4F17-A556-39760FEE91AC.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Modeling/files/GUID-E5C5B3FF-F703-45C3-8DEF-A3DCFD14C079.htm
- Sculpting Tools / Sculpting Tool settings: https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Modeling/files/GUID-820F611F-3380-4D33-AC69-EEC62A59109B.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Modeling/files/GUID-219AB505-A82B-4213-A5CF-3342CBC0C04E.htm
- XGen interactive grooming tool hotkeys / brush settings: https://help.autodesk.com/cloudhelp/2026/ENU/Maya-CharEffEnvBuild/files/GUID-4033B20E-7277-48FA-906A-77F1275B2648.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-CharEffEnvBuild/files/GUID-1C209948-292E-47A2-BC8D-2711F5592AD0.htm
- Use Artisan hotkeys / Artisan marking menus / Prepare to use Paint Effects: https://help.autodesk.com/cloudhelp/2026/ENU/Maya-CharEffEnvBuild/files/GUID-D3E0C098-C385-43F0-A125-525847301EB6.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-CharEffEnvBuild/files/GUID-F0967154-7346-40D1-8F55-6476BBE68D5E.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-CharEffEnvBuild/files/GUID-3834424D-6421-48CA-9DD5-196AB8E92236.htm
- Joint Tool marking menus / Shape Editor: https://help.autodesk.com/cloudhelp/2026/ENU/Maya-CharacterAnimation/files/GUID-D403B411-A712-4900-A93B-E44C670760B0.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-CharacterAnimation/files/GUID-3C92402C-B24E-4874-AC8D-EADF976A19DC.htm
- Script Editor menus and hotkeys / Edit text in an animation expression: https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Scripting/files/GUID-B66020CC-1BBE-4EA1-B1DE-A288B044DD80.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Scripting/files/GUID-A43C30D3-9663-46ED-9768-35F1F162DB9B.htm
- Render View toolbar: https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Rendering/files/GUID-83161023-275E-4E57-A0D8-9C9E255944AE.htm
- FCheck: Display keys / Image adjustment keys / Animation playback control keys / Save images: https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Rendering/files/GUID-89701014-0F19-4BAD-9A9A-FD8496219D65.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Rendering/files/GUID-1F89279F-9B7C-4CCB-93EE-1FECF13B5923.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Rendering/files/GUID-B71C6746-A950-4CB4-8335-AE580655FC96.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Rendering/files/GUID-C51712D0-D809-428D-AB14-EBF7D951B435.htm
- Profiler / Navigation in the Profiler: https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Customizing/files/GUID-3423BE20-0F03-422D-A05A-A1757C7B0A70.htm , https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Customizing/files/GUID-543B5734-8271-4EFE-BBE7-B05FE2D4D2BD.htm
- MASH Placer: https://help.autodesk.com/cloudhelp/2026/ENU/Maya-MotionGraphics/files/GUID-3911D170-2524-42AF-BF37-682C76F7657B.htm
- LookdevX Graph Editor: Keyboard Shortcuts: https://help.autodesk.com/cloudhelp/2026/ENU/LookdevX/files/LookdevX_for_Maya/Exploring_the_UI_of_LookdevX_Graph_Editor/GUID-15F719F9-C3E1-4D00-B10C-790BA9317791.html
- Bifrost Graph Editor: Build and modify graphs / Add a node / Annotate (backdrops, sticky notes) / Connect ports / Set values / Pause graph / Create a compound: https://help.autodesk.com/cloudhelp/2026/ENU/Bifrost-Common/files/Bifrost_Common_build_a_graph_html.html , https://help.autodesk.com/cloudhelp/2026/ENU/Bifrost-Common/files/build-a-graph/Bifrost_Common_build_a_graph_add_a_node_html.html , https://help.autodesk.com/cloudhelp/2026/ENU/Bifrost-Common/files/build-a-graph/Bifrost_Common_build_a_graph_annotate_and_organize_html.html , https://help.autodesk.com/cloudhelp/2026/ENU/Bifrost-Common/files/build-a-graph/Bifrost_Common_build_a_graph_connect_ports_html.html , https://help.autodesk.com/cloudhelp/2026/ENU/Bifrost-Common/files/build-a-graph/Bifrost_Common_build_a_graph_set_value_html.html , https://help.autodesk.com/cloudhelp/2026/ENU/Bifrost-Common/files/build-a-graph/Bifrost_Common_build_a_graph_pause_graph_html.html , https://help.autodesk.com/cloudhelp/2026/ENU/Bifrost-Common/files/build-a-graph/create-and-edit-compounds/Bifrost_Common_build_a_graph_create_and_edit_compounds_create_a_compound_html.html
- Interface overview (pane zoom): https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Basics/files/GUID-F4FCE554-1FA5-447A-8835-63EB43D2690B.htm

`www.autodesk.com/shortcuts/maya` (HTTP 403 in the first pass) and the friendly `help.autodesk.com/view/...?guid=` pages were not needed: everything above is the raw CloudHelp HTML.

---

## 3ds Max — complete

All tables are for 3ds Max 2026; the 2027 pages give the same keys. "KST" = the Keyboard Shortcut Tables page.

### Main UI (global)
Source: KST, Main UI Hotkeys
Every row of the Main UI table, in the table's order. The Notes column holds the table's Category.

| Shortcut | Action | Notes |
|---|---|---|
| Shift+T | Asset Tracking Toggle | Asset Tracking System |
| Alt+A | Align | Edit |
| Ctrl+V | Clone | Edit |
| Del | Delete Objects | Edit |
| Ctrl+Alt+F | Fetch | Edit |
| Ctrl+H | Hold | Edit |
| Alt+N | Normal Align | Edit |
| Ctrl+Y | Redo Scene Operation | Edit |
| F12 | Transform Type-In Dialog Toggle | Edit |
| Ctrl+Z | Undo Scene Operation | Edit |
| Alt+Shift+E | Extrude Face (Poly) | Editable Polygon Object |
| Ctrl+PgUp, Ctrl+Up | Grow Selection (Poly) | Editable Polygon Object |
| Alt+Shift+X | Ignore Backfacing Toggle (Poly) | Editable Polygon Object |
| Alt+L | Select Sub-object Loop | Editable Polygon Object |
| Alt+R | Select Sub-object Ring | Editable Polygon Object |
| Ctrl+PgDown, Ctrl+Down | Shrink Selection (Poly) | Editable Polygon Object |
| Shift+B | Soft Selection Toggle (Poly) | Editable Polygon Object |
| Alt+Shift+1 | Refine (Spline) | Editable Spline Object |
| Ctrl+N | New Scene | File |
| Ctrl+O | Open File | File |
| Ctrl+S | Save File | File |
| Ctrl+Shift+S | Save File As | File |
| Ctrl+Alt+S | Save Incremental (+) | File |
| Ctrl+U | Group Attach | Groups |
| Ctrl+C, Alt+Shift+C | Create Camera (Physical) From View | Lights and Cameras |
| Ctrl+Alt+Shift+C | Create Camera (Standard) From View | Lights and Cameras |
| F11 | MAXScript Listener | MAX Script |
| Alt+\` | Show End Result | Modifier Stack |
| 1 | Sub-Object Level 1 | Modifier Stack |
| 2 | Sub-Object Level 2 | Modifier Stack |
| 3 | Sub-Object Level 3 | Modifier Stack |
| 4 | Sub-Object Level 4 | Modifier Stack |
| 5 | Sub-object Level 5 | Modifier Stack |
| Alt+Shift+3 | Circle Loops | PolyTools |
| Alt+Shift+4 | Geo Poly | PolyTools |
| Alt+3 | Insert Loop | PolyTools |
| Alt+4 | PolyShift Move | PolyTools |
| Alt+2 | Set Flow | PolyTools |
| Alt+5 | Spin Edge | PolyTools |
| Alt+Shift+2 | Straighten Loops | PolyTools |
| Alt+1 | Swift Loop | PolyTools |
| Alt+G | Geometry Selection Visibility Toggle | Projection Modifier |
| Alt+RMB | Animation [Alt+RMB] | Quad Menu Sets |
| Ctrl+Alt+Shift+RMB | Custom [Shift+Ctrl+Alt+RMB] | Quad Menu Sets |
| Ctrl+Shift+RMB | Custom [Shift+Ctrl+RMB] | Quad Menu Sets |
| Ctrl+Alt+RMB | Lighting \| Render [Ctrl+Alt+RMB] quad menu | Quad Menu Sets |
| Space | Lock | Quad Menu Sets |
| Ctrl+RMB | Modeling [Ctrl+RMB] | Quad Menu Sets |
| Shift+RMB | Snap [Shift+RMB] | Quad Menu Sets |
| V | Viewports | Quad Menu Sets |
| J | Windows | Quad Menu Sets |
| 9 | Advanced Lighting Panel | Render |
| Shift+V | Create Animated Sequence File... | Render |
| 8 | Environment Dialog Toggle | Render |
| Shift+Q, Shift+F9 | Render | Render |
| F9 | Render Last | Render |
| F10 | Render SetUp... | Render |
| Ctrl+A | Select All | Selection |
| PgUp | Select Ancestor | Selection |
| H | Select By Name | Selection |
| PgDown | Select Child | Selection |
| Shift+PgDown | Select Children | Selection |
| Ctrl+I | Select Invert | Selection |
| Ctrl+D | Select None | Selection |
| Ctrl+Shift+A | Select Similar | Selection |
| Ctrl+Shift+N | Selection Lock Toggle | Selection |
| Q | Smart Select | Selection |
| N | Auto Key Mode Toggle | Set Key Tools |
| K | Set Keys | Set Key Tools |
| A | Angle Snap Toggle | Snaps |
| Alt+S | Cycle Active Snap Type | Snaps |
| Alt+F3 | Enable Axis Constraints in Snaps Toggle | Snaps |
| S | Snaps Toggle | Snaps |
| , | Backup Time One Unit | Time |
| . | Forward Time One Unit | Time |
| End | Go to End Frame | Time |
| Home | Go to Start Frame | Time |
| / | Play Animation | Time |
| Insert | Affect Pivot Only Mode Toggle | Tools |
| Alt+Shift+5 | Center Point Cycle | Tools |
| Ctrl+F | Cycle Selection Method | Tools |
| Alt+X | Display as See-Through Toggle | Tools |
| Alt+H | Hide Selection | Tools |
| Alt+I | Hide Unselected | Tools |
| Alt+Q | Isolate Selection | Tools |
| Ctrl+Alt+Q | Isolate Selection Toggle | Tools |
| Ctrl+Alt+Shift+X | Keyboard Shortcut Override Toggle | Tools |
| — | Lock User Interface Toggle | Tools; listed in the table with an empty Hotkey cell |
| M | Material Editor Toggle | Tools |
| Alt+W | Maximize Viewport Toggle | Tools |
| I | Pan Viewport | Tools |
| Shift+A | Quick Align | Tools |
| Ctrl+E | Scale Cycle | Tools |
| W | Select and Move | Tools |
| E | Select and Rotate | Tools |
| — | Show Main Toolbar Toggle | Tools; listed in the table with an empty Hotkey cell |
| 7 | Show Statistics Toggle | Tools |
| Y | Smart Place | Tools |
| R | Smart Scale | Tools |
| \ | Sound Toggle | Tools |
| Shift+I | Spacing Tool | Tools |
| Ctrl+B | Sub-object Selection Toggle | Tools |
| F8 | Transform Gizmo Plane Constraint Cycle | Tools |
| - | Transform Gizmo Size Down | Tools |
| = | Transform Gizmo Size Up | Tools |
| F5 | Transform Gizmo X Constraint | Tools |
| F6 | Transform Gizmo Y Constraint | Tools |
| F7 | Transform Gizmo Z Constraint | Tools |
| Alt+U | Unhide All | Tools |
| Ctrl+L | Viewport Lighting Illuminate with Default / Scene Lights Toggle | Tools |
| Shift+F | Viewport Safe Frames Toggle | Tools |
| F2 | Viewport Selection Shade Selected Faces Toggle | Tools |
| Shift+J | Viewport Selection Show Selection Bracket Toggle | Tools |
| Num2 | Virtual Viewport Pan Down | Tools |
| Num4 | Virtual Viewport Pan Left | Tools |
| Num6 | Virtual Viewport Pan Right | Tools |
| Num8 | Virtual Viewport Pan Up | Tools |
| Num/ | Virtual Viewport Toggle | Tools |
| Num+ | Virtual Viewport Zoom In | Tools |
| Num- | Virtual Viewport Zoom Out | Tools |
| Shift+O | Window / Crossing Toggle | Tools |
| Ctrl+Alt+Z | Zoom Extents | Tools |
| Shift+Ctrl+Z | Zoom Extents All | Tools |
| Z | Zoom Extents Selected | Tools |
| Ctrl+Alt+Shift+Z | Zoom In 2X | Tools |
| Alt+Z | Zoom Mode | Tools |
| Ctrl+W | Zoom Region Mode | Tools |
| [, Ctrl+= | Zoom Viewport In | Tools |
| ], Ctrl+- | Zoom Viewport Out | Tools |
| Ctrl+1 | Add/Edit Parameters... (TV) | Track View |
| X | Launch Global Search | User Interface |
| Shift+F3 | High Quality | Viewport Lighting and Shadows |
| O | Adaptive Degradation Toggle | Views |
| C | Camera View | Views |
| Ctrl+Shift+D | Disable Viewport | Views |
| Ctrl+Alt+X | Expert Mode Toggle | Views |
| F | Front View | Views |
| Shift+C | Hide Cameras Toggle | Views |
| Shift+G | Hide Geometry Toggle | Views |
| G | Hide Grids Toggle | Views |
| Shift+H | Hide Helpers Toggle | Views |
| Shift+L | Hide Lights Toggle | Views |
| Shift+P | Hide Particle Systems Toggle | Views |
| Shift+S | Hide Shapes Toggle | Views |
| Shift+W | Hide Space Warps Toggle | Views |
| Alt+Home | Home View | Views |
| L | Left View | Views |
| Ctrl+R | Orbit View Mode | Views |
| U | Orthographic User View | Views |
| Ctrl+P | Pan View | Views |
| P | Perspective User View | Views |
| Shift+Y | Redo Viewport Operation | Views |
| \` | Redraw All Views | Views |
| Alt+J | Selection/Preview Highlights Toggle | Views |
| Ctrl+\` | Show Floating Dialogs | Views |
| Shift+4 | Spot/Directional Light View | Views |
| T | Top View | Views |
| Shift+Z | Undo Viewport Operation | Views |
| Alt+Shift+Ctrl+B | Update Background Image | Views |
| F4 | View Edged Faces Toggle | Views |
| Alt+B | Viewport Background | Views |
| Up | WalkThrough View Mode | Views |
| F3 | Wireframe / Smooth+Highlights Toggle | Views |

### Main UI: additional bindings documented on feature pages
Source: feature pages listed in Sources

| Shortcut | Action | Notes |
|---|---|---|
| B | Bottom view | Setting Viewport Layout. Not in KST. |
| — | Right view / Shape view | Setting Viewport Layout: "none", use the POV viewport label menu. |
| $ (Shift+4) | Light viewport | Light pages say "$"; KST lists Spot/Directional Light View as Shift+4. |
| Ctrl+Space | Presentation Mode (floating viewport full screen, borderless) | Viewport's General Menu; General Viewport Concepts. Not in KST. |
| D | Disable Viewport | Viewport's General Menu. Conflict: KST gives Ctrl+Shift+D. |
| J | Selection Brackets (viewport preference) | Active Viewport: Preferences Tab. Conflict: KST gives Shift+J for the selection-bracket toggle. |
| Shift+K | Toggle the viewport filter | Active Viewport: Filter Tab. |
| Ctrl+Alt+O | Reopen the most recently closed Scene Explorer | Scene Explorer. |
| Ctrl+Shift+\` | Place Working Pivot | Snap Working Pivot. |
| Ctrl+\` | Quick Pivot (place Working Pivot) | Snap Working Pivot. Conflict: KST gives Ctrl+\` to Show Floating Dialogs. |
| Alt+Shift+S | Selection Pivot (Working Pivot to selection average) | Snap Working Pivot. |
| Alt+Shift [hold] then S repeatedly | Cycle through available snap and preview points | Snap Options. |
| Alt+S repeatedly | Choose the Snap Override type | Snap Override (same key as Cycle Active Snap Type). |
| 0 | Bake to Texture (via quad menu) | Baking to Texture page: "Hotkey: 0 > Quad menu > Bake to Texture". Not in KST. |
| Ctrl+N (in a numeric field) | Numerical Expression Evaluator | Special Controls. |
| Ctrl [hold] while dragging a spinner | Change the value faster | Special Controls. |
| Alt [hold] while dragging a spinner | Change the value slower | Special Controls. |
| RMB on spinner arrows | Reset field to its minimum | Special Controls. |
| Alt+RMB on spinner arrows | Remove the animation key at the current frame | Special Controls. |
| Ctrl+Shift+RMB on spinner arrows | Remove all animation on the parameter | Special Controls. |
| Shift+RMB on spinner arrows | Set a key (Set Key mode) | Special Controls; Using Set Key Mode. |
| Ctrl+drag / Alt+drag a modifier | Instance / move a modifier to another object or stack position | Using the Modify Panel; Editing the Stack. Shift+drag moves a modifier. |
| Ctrl+Alt+S | Save Incremental (+) | Save Incremental page, same as KST. |
| — | Keyable Property Toggle; Clear Set Key Mode Buffer; Create Position/Rotation Lock Key | Additional Keyboard Commands: "Default key: None". |
| — | Select Sibling - Next / Previous; Paint Selection Size Up / Down; Position To Zero; Key Filters; Show Keyable | Feature pages say these have no default key. |

### Viewport navigation: mouse (3ds Max interaction mode, the default)
Source: Zoom, Orbit, Pan View, Mouse Panel, Track Bar and related pages

| Shortcut | Action | Notes |
|---|---|---|
| MMB drag | Pan | Pan View; Mouse Panel |
| Alt+MMB drag | Orbit | Orbit page |
| Ctrl+Alt+MMB drag | Zoom | Zoom page |
| Wheel | Zoom in / out | Zoom page |
| Ctrl / Alt [hold] while zooming | Zoom faster / slower | Zoom page (first pass) |
| Shift / Ctrl [hold] while panning | Constrain pan to one axis / pan faster | Pan View (first pass) |
| Esc or RMB | Exit a navigation mode | first pass |
| Ctrl+click / Alt+click | Add to / remove from selection | Basics of Selecting Objects |
| Ctrl+Alt [hold], move over sub-objects, click a selected one | Deselect all highlighted sub-objects | Polygon Modeling Panel / Selection Rollout |
| Shift+drag with Move / Rotate / Scale | Shift+Clone | Using Shift+Clone |
| Ctrl+Alt+LMB / RMB / MMB drag on the track bar | Set active time segment start / end / move both | Track Bar |
| Ctrl+Alt+MMB / RMB drag over the track-bar time ruler | Pan / zoom the track window (State Sets) | Panning and Zooming the Track Window |
| Windows key [hold] + click | Switch viewports while one is maximized | Configuring Viewports |

### Viewport navigation: Maya interaction mode (option)
Source: Interaction Mode Preferences; Undo View Change; Maximize Viewport Toggle
The docs list only these differences. The full Maya-mode hotkey set is selectable in the Hotkey Editor but is not tabulated in the help.

| Shortcut | Action | Notes |
|---|---|---|
| Alt+LMB drag | Orbit (not in Camera or orthographic viewports) |  |
| Alt+MMB drag | Pan |  |
| Alt+RMB drag | Zoom (not in Camera viewports) |  |
| Alt+Home | Default Perspective view |  |
| Shift+click / Ctrl+click | Toggle / subtract selection |  |
| Space | Maximize Viewport Toggle (3ds Max mode: Alt+W) |  |
| F | Zoom Extents Selected (3ds Max mode: Z) |  |
| A | Zoom Extents All (3ds Max mode: Shift+Ctrl+Z) |  |
| Alt+Z / Alt+Y | Undo / Redo Viewport Operation (3ds Max mode: Shift+Z / Shift+Y) |  |
| Alt+V | Play Animation (3ds Max mode: /) |  |
| S | Set Key (3ds Max mode: K) |  |
| Ctrl+G | Group (3ds Max mode: none) |  |
| G | Editable Poly Repeat Last Operation (3ds Max mode: ;) |  |

### Quad menus
Source: KST (Quad Menu Sets) and Additional Quad Menus

| Shortcut | Action | Notes |
|---|---|---|
| RMB | Default quad menu |  |
| Shift+RMB | Snap quad menu | KST |
| Alt+RMB | Animation quad menu | KST; not available in Maya mode (Alt+RMB zooms) |
| Ctrl+RMB | Modeling quad menu | KST |
| Ctrl+Alt+RMB | Lighting \| Render quad menu | KST |
| Ctrl+Shift+RMB | Custom quad menu | KST |
| Ctrl+Alt+Shift+RMB | Custom quad menu | KST |
| V | Viewports quad menu | KST |
| J | "Windows" quad menu set | KST |
| Space | Lock (Quad Menu Sets) | KST |
| Alt+RMB in Track View Controller window | Alternate Track View quad / hierarchy navigation menu | Track View Quad Menus; Hierarchy Right-Click Menu |

### Edit Normals modifier
Source: KST, Edit Hotkeys + feature pages

| Shortcut | Action | Notes |
|---|---|---|
| Shift+R | Break Normals | KST, Edit Hotkeys |
| Ctrl+C | Copy Normal | KST, Edit Hotkeys |
| 3 | Edge Level | KST, Edit Hotkeys |
| 4 | Face Level | KST, Edit Hotkeys |
| E | Make Explicit | KST, Edit Hotkeys |
| 1 | Normal Level | KST, Edit Hotkeys |
| 5 | Object Level | KST, Edit Hotkeys |
| Ctrl+V | Paste Normal | KST, Edit Hotkeys |
| R | Reset Normals | KST, Edit Hotkeys |
| S | Specify Normals | KST, Edit Hotkeys |
| U | Unify Normals | KST, Edit Hotkeys |
| 2 | Vertex Level | KST, Edit Hotkeys |
| Ctrl+0 / Ctrl+1 / Ctrl+2 / Ctrl+3 / Ctrl+4 | Object / Normal / Vertex / Edge / Face level | Edit Normals Modifier Reference. Conflict: KST gives 5 / 1 / 2 / 3 / 4. |

### Edit Poly modifier
Source: KST, Edit Hotkeys + feature pages

| Shortcut | Action | Notes |
|---|---|---|
| Alt+Shift+D | Attach | KST, Edit Hotkeys |
| Ctrl+Shift+B | Bevel Mode | KST, Edit Hotkeys |
| Shift+R | Break | KST, Edit Hotkeys |
| Alt+P | Cap | KST, Edit Hotkeys |
| Ctrl+Shift+C | Chamfer Mode | KST, Edit Hotkeys |
| Ctrl+Alt+C | Collapse | KST, Edit Hotkeys |
| Shift+Ctrl+E | Connect | KST, Edit Hotkeys |
| Shift+X | Constrain to Edges | KST, Edit Hotkeys |
| Alt+C | Cut | KST, Edit Hotkeys |
| Ctrl+Alt+D | Detach | KST, Edit Hotkeys |
| B | Edit Soft Selection Mode | KST, Edit Hotkeys |
| Ctrl+Alt+Shift+E | Extrude along Spline Mode | KST, Edit Hotkeys |
| Shift+E | Extrude Mode | KST, Edit Hotkeys |
| Ctrl+PgUp, Ctrl+Up | Grow Selection | KST, Edit Hotkeys |
| Alt+H | Hide | KST, Edit Hotkeys |
| Alt+I | Hide Unselected | KST, Edit Hotkeys |
| Alt+Shift+X | Ignore Backfacing in Selections | KST, Edit Hotkeys |
| Alt+M | Make Planar | KST, Edit Hotkeys |
| Ctrl+M | MeshSmooth | KST, Edit Hotkeys |
| Shift+Ctrl+Q | Quickslice Mode | KST, Edit Hotkeys |
| ; | Repeat Last Operation | KST, Edit Hotkeys |
| Ctrl+PgDown, Ctrl+Down | Shrink Selection | KST, Edit Hotkeys |
| Shift+Ctrl+W | Target Weld Mode | KST, Edit Hotkeys |
| Alt+U | Unhide All | KST, Edit Hotkeys |
| Shift+B | Use Soft Selection | KST, Edit Hotkeys |
| Shift+Drag | Extrude Polygon (Move tool selected) | KST, Edit Hotkeys |
| Ctrl+Shift+Drag | Clone Polygon (Move tool selected) | KST, Edit Hotkeys |
| Shift+Drag | Inset Polygon (Scale tool selected) | KST, Edit Hotkeys |
| Shift+Ctrl+B [hold] | Temporarily activate Bevel (press/release override) | Hotkey Editor |

### Edit Mesh / Editable Mesh
Source: KST, Edit Hotkeys + feature pages

| Shortcut | Action | Notes |
|---|---|---|
| Alt+Shift+D | Attach Mode | KST, Edit Hotkeys |
| Ctrl+Shift+B | Bevel Mode | KST, Edit Hotkeys |
| Shift+R | Break Vertices | KST, Edit Hotkeys |
| Ctrl+Shift+C | Chamfer Mode | KST, Edit Hotkeys |
| Ctrl+Alt+C | Collapse | KST, Edit Hotkeys |
| Alt+C | Cut Mode | KST, Edit Hotkeys |
| Ctrl+Alt+D | Detach | KST, Edit Hotkeys |
| Ctrl+T | Edge Turn | KST, Edit Hotkeys |
| B | Edit Soft Selection | KST, Edit Hotkeys |
| Shift+E | Extrude Mode | KST, Edit Hotkeys |
| Alt+H | Hide Selected | KST, Edit Hotkeys |
| Alt+Shift+X | Ignore Backfacing in Selections | KST, Edit Hotkeys |
| Shift+B | Soft Selection | KST, Edit Hotkeys |
| Alt+U | Unhide All | KST, Edit Hotkeys |
| Alt+Shift+W | Weld Selected | KST, Edit Hotkeys |
| Shift+Ctrl+W | Weld Target Mode | KST, Edit Hotkeys |
| Alt+C | Toggle Cut mode | Cut and Slice (Editable Mesh) |

### Editable Poly
Source: KST, Edit Hotkeys + feature pages

| Shortcut | Action | Notes |
|---|---|---|
| Alt+Shift+D | Attach | KST, Edit Hotkeys |
| Ctrl+Shift+B | Bevel Mode | KST, Edit Hotkeys |
| Shift+R | Break | KST, Edit Hotkeys |
| Alt+P | Cap | KST, Edit Hotkeys |
| Ctrl+Shift+C | Chamfer Mode | KST, Edit Hotkeys |
| Ctrl+Alt+C | Collapse | KST, Edit Hotkeys |
| Shift+Ctrl+E | Connect | KST, Edit Hotkeys |
| Shift+X | Constrain to Edges | KST, Edit Hotkeys |
| Alt+C | Cut | KST, Edit Hotkeys |
| Ctrl+Alt+D | Detach | KST, Edit Hotkeys |
| B | Edit Soft Selection Mode | KST, Edit Hotkeys |
| Ctrl+Alt+Shift+E | Extrude along Spline Mode | KST, Edit Hotkeys |
| Shift+E | Extrude Mode | KST, Edit Hotkeys |
| Ctrl+PgUp, Ctrl+Up | Grow Selection | KST, Edit Hotkeys |
| Alt+H | Hide | KST, Edit Hotkeys |
| Alt+I | Hide Unselected | KST, Edit Hotkeys |
| Alt+Shift+X | Ignore Backfacing in Selections | KST, Edit Hotkeys |
| Ctrl+M | MeshSmooth | KST, Edit Hotkeys |
| Shift+Ctrl+Q | Quickslice Mode | KST, Edit Hotkeys |
| ; | Repeat Last Operation | KST, Edit Hotkeys |
| Ctrl+PgDown, Ctrl+Down | Shrink Selection | KST, Edit Hotkeys |
| Shift+Ctrl+W | Target Weld Mode | KST, Edit Hotkeys |
| Alt+U | Unhide All | KST, Edit Hotkeys |
| Shift+B | Use Soft Selection | KST, Edit Hotkeys |
| Backspace | Remove (vertices; combines polygons, no hole) | Editable Poly (Vertex); Vertices Panel |
| Ctrl+Backspace (Ctrl+Remove) | Remove edges and delete the extra vertices | Editable Poly (Edge); Edges Panel |
| Ctrl+Enter | Apply and Continue in a caddy (Chamfer, Extrude Along Spline, MeshSmooth and others) | Chamfer Vertices/Edges/Borders; caddy pages |
| Shift+click a tool button | Open that tool's settings caddy | Polygons/Edges/Vertices panels |
| Shift+click another sub-object in the same loop / ring | Select the loop / ring | Modify Selection Panel; Selection Rollout |
| Ctrl+click spinner arrow / Alt+click spinner arrow | Grow / shrink a loop or ring selection in one direction | Selection Rollout |
| Ctrl+click the Polygon button | Convert the selection to polygons | Selection Rollout |
| Shift+Ctrl+B [hold] | Temporarily activate Bevel (press/release override) | Hotkey Editor: bold actions are press/release overrides |

### Soft selection in other modifiers and objects
Source: KST, Edit Hotkeys
Soft Selection Rollout: for Editable Poly the Edit Soft Selection Mode key must be set by the user; Edit Poly has B (table above).

| Shortcut | Action | Notes |
|---|---|---|
| B | Edit Soft Selection | Edit Mesh |
| B | Edit Soft Selection | Edit Patch |
| B | Edit Soft Selection | Edit Spline |
| B | Edit Soft Selection | HSDS |
| B | Edit Soft Selection | Mesh Select |
| B | Edit Soft Selection Mode | MeshSmooth |
| B | Edit Soft Selection | Patch Select |
| B | Edit Soft Selection Mode | Poly Select |
| B | Edit Soft Selection | Projection Modifier |
| B | Edit Soft Selection | Vol. Select |

### PolyTools / Graphite main-UI modeling keys
Source: KST (PolyTools) and Graphite Edit Panel

| Shortcut | Action | Notes |
|---|---|---|
| Alt+1 | Swift Loop | KST, PolyTools |
| Alt+2 | Set Flow | KST |
| Alt+3 | Insert Loop | KST |
| Alt+4 | PolyShift Move | KST |
| Alt+5 | Spin Edge | KST |
| Alt+Shift+2 | Straighten Loops | KST |
| Alt+Shift+3 | Circle Loops | KST |
| Alt+Shift+4 | Geo Poly | KST |
| Shift+click (SwiftLoop) | Insert an edge loop that follows surface flow | Edit Panel |
| Ctrl+click (SwiftLoop) | Select an edge loop and switch to Edge level | Edit Panel |
| Alt+drag (SwiftLoop) | Slide a selected edge loop | Edit Panel |
| Ctrl+Alt+drag (SwiftLoop) | Slide and straighten the loop | Edit Panel |
| Ctrl+Shift+click (SwiftLoop) | Remove an edge loop | Edit Panel |
| Shift+drag (Paint Connect) | Paint connections at edge midpoints | Edit Panel |
| Ctrl+drag (Paint Connect) | Select and connect vertices | Edit Panel |
| Alt+click (Paint Connect) | Remove a vertex | Edit Panel |
| Ctrl+Shift+click (Paint Connect) | Remove an edge loop | Edit Panel |
| Ctrl+Alt+click (Paint Connect) | Remove an edge | Edit Panel |
| Shift+Alt+drag (Paint Connect) | Paint a double connection (two parallel edges) | Edit Panel |
| Alt+paint (Tweak UVs) | Revert to untweaked UVs | Edit Panel |

### Graphite Freeform: Paint Deform brushes
Source: Paint Deform Panel and Freeform options panels

| Shortcut | Action | Notes |
|---|---|---|
| Ctrl+Shift+drag | Resize the brush (all Paint Deform brushes) | Paint Deform Panel; Paint Options Panel |
| Shift+Alt+drag | Change brush strength (all brushes) |  |
| Ctrl [hold] | Revert to the previous saved state (Push/Pull, Relax/Soften, Smudge, Flatten, Pinch/Spread, Noise, Exaggerate) |  |
| Shift [hold] | Relax the mesh (Push/Pull, Smudge, Flatten, Pinch/Spread, Noise, Exaggerate, Constrain to Spline) |  |
| Alt+drag (Push/Pull) | Push vertices inward |  |
| Alt+drag (Relax/Soften) | Relax without shrinking |  |
| Alt+drag (Smudge) | Move vertices horizontally only |  |
| Alt+drag (Pinch/Spread) | Spread vertices apart |  |
| Alt+drag (Noise) | Concave noise |  |
| Alt+drag (Exaggerate) | Invert the exaggeration |  |
| Ctrl+drag vertically (Shift tool) | Change Falloff radius | Paint Deform Panel; Shift Options Panel |
| Shift+drag vertically (Shift tool) | Change Full Strength radius |  |
| Shift+Alt+drag vertically (Shift tool) | Change Strength % |  |
| Shift+drag / Ctrl+drag / Shift+Alt+drag | Full Strength / Falloff / Strength % (Conform and UV Tweak options) | Conform Options Panel; UV Tweak Options Panel |

### Graphite Freeform: PolyDraw tools
Source: PolyDraw pages
Alt-based PolyDraw and Paint Deform modifiers do not work in Maya interaction mode (Alt orbits).

| Shortcut | Action | Notes |
|---|---|---|
| click | Step Build: place vertices | Add Geometry and Optimize Tools |
| Shift+drag | Step Build: fill gaps between free vertices with quads |  |
| Ctrl+click | Step Build: delete a polygon (keeps vertices) |  |
| Alt+click | Step Build: remove a vertex |  |
| Ctrl+Alt+click | Step Build: remove an edge |  |
| Ctrl+Shift+click | Step Build: place/select vertices, auto-build a polygon every four |  |
| Shift+Alt+move, click | Step Build: select vertices by hovering, click to build a polygon |  |
| Ctrl+Shift+Alt+drag | Step Build: move a vertex on grid/surface |  |
| drag a border vertex | Extend: create a polygon |  |
| Shift+drag a border edge | Extend: create a polygon |  |
| Ctrl+Shift+drag an edge | Extend: extend the whole loop |  |
| Ctrl+Alt+drag between two edges | Extend: create a polygon |  |
| Ctrl+click | Extend: delete a polygon and its isolated vertices |  |
| Ctrl+Shift+Alt+drag | Extend: move a vertex |  |
| Alt+drag / Alt+Shift+drag | Extend: create a polygon in screen space from a vertex / edge |  |
| click edges | Optimize: collapse edges |  |
| Shift+drag | Optimize: target-weld vertices along the stroke |  |
| Ctrl+drag | Optimize: connect vertices with edges |  |
| Alt+click | Optimize: remove a vertex |  |
| Shift+Ctrl+click | Optimize: remove an edge loop |  |
| Shift+Alt+click | Optimize: remove an edge ring |  |
| Ctrl+Alt+click | Optimize: remove an edge |  |
| Shift+Ctrl+Alt+drag | Optimize: move a vertex |  |
| Shift+drag / Ctrl+drag | Drag: move edges / polygons | Drag and Conform Tools |
| Shift+Ctrl+drag / Shift+Ctrl+Alt+drag | Drag: move edge loops / elements |  |
| Alt / Alt+Shift / Alt+Ctrl + drag | Drag: move vertices / edges / polygons in screen space |  |
| Ctrl+click / Ctrl+Shift+Alt+drag | Shapes: delete / move a polygon | Create Geometry Tools |
| Shift+drag / Ctrl+click | Topology: continue from nearest endpoint / delete a line |  |
| Ctrl+click / Ctrl+Shift+Alt+drag | Splines: delete / move the closest spline |  |
| Shift+drag | Strips: start from the closest existing edge |  |
| Alt [hold] while drawing | Strips: add a polygon to an open edge |  |
| drag / Shift+drag | Branches: from the nearest polygon / from all selected polygons |  |
| Ctrl+click / Shift+Alt+click | Branches: select a polygon / add or remove polygons |  |
| Ctrl+Shift+drag | Brush size (most Freeform brushes) | Paint Options Panel |

### Editable Spline / Edit Spline
Source: KST + spline pages

| Shortcut | Action | Notes |
|---|---|---|
| Alt+Shift+1 | Refine (Spline) | KST, Main UI |
| B | Edit Soft Selection (Edit Spline) | KST, Edit Hotkeys |
| Shift+LMB drag a vertex (Move/Rotate/Scale) | Extrude the spline from the vertex | Editable Spline (Segment); Edit Spline Modifier |
| Shift+LMB drag a segment | Extrude a segment | Edit Spline Modifier |
| Ctrl+Shift+LMB drag a segment | Clone a segment | Editable Spline (Segment); Edit Spline Modifier |
| Shift+click a Bezier handle | Break the tangent (move handles independently) | Editable Spline |

### Schematic View
Source: KST, Schematic View Hotkeys

| Shortcut | Action | Notes |
|---|---|---|
| B | Add Bookmark |  |
| D | Display Floater |  |
| Alt+F | Filters |  |
| Alt+A | Free All |  |
| Alt+S | Free Selected |  |
| Alt+H | Hide Selected |  |
| Ctrl+I | Invert Selected Nodes |  |
| Alt+C | Move Children |  |
| Right | Next Bookmark |  |
| Left | Previous Bookmark |  |
| Ctrl+U | Refresh View |  |
| F2 | Rename Object |  |
| Ctrl+A | Select All Nodes |  |
| Shift+PgDown | Select Children |  |
| Ctrl+D | Select None |  |
| G | Show Grid |  |
| Shift+S | Toggle Shrink |  |
| C | Use Connect Tool |  |
| Ctrl+P | Use Pan Tool |  |
| Q | Use Select Tool |  |
| Ctrl+W | Use Zoom Region Tool |  |
| Alt+Z | Use Zoom Tool |  |
| Ctrl+Alt+Z | Zoom Extents |  |
| Z | Zoom Selected Extents |  |
| H | Select objects by name | Using Schematic View |
| Ctrl+click | Add to selection | Selecting with Schematic View |

### Track View (Curve Editor and Dope Sheet)
Source: KST, Track View Hotkeys
Biped adds Alt+A / Alt+S / Alt+D for footstep selection in Track View (Biped table).

| Shortcut | Action | Notes |
|---|---|---|
| K | Add/Remove Keys |  |
| Ctrl+E | Apply Ease Curve |  |
| Ctrl+M | Apply Multiplier Curve |  |
| C | Assign Controller |  |
| Ctrl+C | Copy Controller |  |
| O | Expand Object Toggle |  |
| Enter, T | Expand Track Toggle |  |
| Alt+F | Filters |  |
| Ctrl+Alt+Z | Frame Horizontal Extents |  |
| Ctrl+Alt+Shift+Z | Frame Horizontal Extents Keys |  |
| Ctrl+L | Lock Selection |  |
| L | Lock Tangents Toggle |  |
| U | Make Controller Unique |  |
| Down | Move Highlight Down |  |
| Up | Move Highlight Up |  |
| M | Move Keys |  |
| Left | Nudge Keys Left |  |
| Right | Nudge Keys Right |  |
| Ctrl+P | Pan |  |
| Ctrl+V | Paste Controller |  |
| Ctrl+Left | Retime Move Left |  |
| Ctrl+Right | Retime Move Right |  |
| Ctrl+Down | Scroll Down |  |
| Ctrl+Up | Scroll Up |  |
| Ctrl+A | Select All |  |
| Shift+PgDown | Select Children |  |
| Ctrl+I | Select Invert |  |
| Ctrl+D | Select None |  |
| S | Snap Frames |  |
| Alt+Z | Zoom |  |
| Ctrl+W | Zoom Region |  |
| Ctrl+1 | Add/Edit Parameters... (TV) | KST, Main UI (Track View category) |
| MMB drag (Alt+MMB in Maya mode) | Pan the key window | Pan (Track View) |
| Ctrl+Alt+MMB drag (Alt+RMB in Maya mode) | Zoom the key window | Pan (Track View); Zoom Track View Key Window |
| Alt+RMB | Alternate menu: expand/collapse tracks | Track View Quad Menus; Hierarchy Alt+Right-Click Menu |
| Ctrl+click | Highlight non-contiguous keys (Move Keys) | Move Keys |

### Unwrap UVW / Edit UVWs editor (main table)
Source: KST, UVW Unwrap Hotkeys

| Shortcut | Action | Notes |
|---|---|---|
| Shift+H | Align Horizontal |  |
| Shift+E | Align to Edge |  |
| Shift+V | Align Vertical |  |
| Shift+R | Break Selected Vertices |  |
| Ctrl+C | Copy |  |
| Shift+C | Cylindrical Mapping |  |
| Ctrl+Alt+D | Detach Edge Verts |  |
| Shift+P | Edge Selection to Pelt Seam Add |  |
| Ctrl+Shift+P | Edge Selection to Pelt Seam Replace |  |
| Ctrl+E | Edit UVW's |  |
| Alt+F | Filter Selected Polygons |  |
| Ctrl+Shift+S | Flatten by Smoothing Group |  |
| Q | Freeform Mode |  |
| Ctrl+F | Freeze Selected |  |
| G | Grid Visible |  |
| Ctrl+PgUp | Grow |  |
| Alt+H | Hide Selected |  |
| Alt+Shift+X | Ignore Back Polygons |  |
| Ctrl+L | Lock selected vertices |  |
| Shift+A | Pack |  |
| Ctrl+P | Pan |  |
| Ctrl+V | Paste |  |
| Enter | Planar map faces/patches |  |
| Shift+Q | Quick Planar Map |  |
| Shift+X | Relax |  |
| Alt+R | Relax Brush Type Cycle |  |
| Ctrl+Right | Rotate -90 |  |
| Ctrl+Left | Rotate +90 |  |
| Shift+M | Show Map |  |
| Ctrl+PgDn | Shrink |  |
| Alt+E | Show Seams In Viewport |  |
| S | Snap |  |
| Shift+B | Soft Selection |  |
| Shift+S | Stitch |  |
| Shift+F | Straighten Edges |  |
| Ctrl+PgDown, Ctrl+Down | Texture Vertex Contract Selection |  |
| Ctrl+PgUp, Ctrl+Up | Texture Vertex Expand Selection |  |
| W | Texture Vertex Move Mode |  |
| E | Texture Vertex Rotate Mode |  |
| R | Texture Vertex Scale Mode |  |
| Alt+Shift+W | Texture Vertex Weld Selected |  |
| Shift+Ctrl+W | Texture VertexTarget Weld |  |
| 4 | TV Element Mode |  |
| Alt+L | TV Loop Select |  |
| Alt+R | TV Ring Select |  |
| Ctrl+Q | Unfold3D Peel |  |
| Ctrl+Shift+F | Unfreeze All |  |
| Alt+U | Unhide All |  |
| O | Unwrap Options |  |
| U | Update Map |  |
| Alt+4 | UV Paint Movement |  |
| Alt+Z | Zoom |  |
| Ctrl+Alt+Z | Zoom Extents |  |
| Z | Zoom Extents Selected |  |
| Ctrl+W | Zoom Region |  |
| Shift+Space | Zoom To Gizmo |  |

### Unwrap UVW: rows with a key on the "Unwrap UVW Shortcuts" page
Source: Unwrap UVW Shortcuts page
This page is older than KST and disagrees with it in places. Conflicts: Break Selected Vertices Ctrl+B (KST Shift+R); Weld Selected Ctrl+W (KST Alt+Shift+W); Target Weld Ctrl+T (KST Shift+Ctrl+W); Zoom Extents Alt+Ctrl+X (KST Ctrl+Alt+Z); Expand Geom. Polygons Alt+F (same key as Filter Selected Polygons). Prefer KST.

| Shortcut | Action | Notes |
|---|---|---|
| Ctrl+B | Break Selected Vertices | Breaks selected vertices so no texture polygon shares them; the same as breaking a vertex in Edit Mesh. |
| Ctrl+Alt+D | Detach Edge Vertices | Detaches the selected vertices into a separate element. |
| Ctrl+E | Edit UVWs | Opens the Edit UVWs dialog. |
| Alt+F | Expand Geom. Polygons | Grows the polygon selection in the viewport. |
| Alt+F | Filter Selected Polygons | When on, only polygons that are selected in the viewport will be displayed in the Edit UVWs dialog. |
| Q | Freeform Mode | Toggles freeform editing tool in the Edit UVWs dialog. |
| Ctrl+F | Freeze Selected | Locks the current selection so you cannot select it anymore. |
| Alt+Shift+Ctrl+F | Get Polygon Selection From Stack | Copies the polygon selection from the modifier stack to the polygon selection that Unwrap UVW uses. |
| Alt+Shift+Ctrl+P | Get Selection From Polygons | Transfers the polygon selection in the viewport to the selection in the Edit UVWs dialog. |
| Alt+H | Hide Selected | Hides the current selection in the Edit UVWs dialog. |
| Alt+Shift+Ctrl+L | Load UVW | Lets you load a .uvw file onto a mesh. The mesh must have similar topology as the source. |
| Ctrl+L | Lock Selected Vertices | Locks the selection so you cannot add to or remove from it. |
| Alt+Shift+Ctrl+N | Mirror Horizontal | Mirrors the current selection along the U axis. |
| Alt+Shift+Ctrl+M | Mirror Vertical | Mirrors the current selection along the V axis. |
| Alt+Shift+Ctrl+J | Move Horizontal |  |
| Alt+Shift+Ctrl+K | Move Vertical |  |
| Ctrl+P | Pan |  |
| Enter | Planar Map Faces/Patches | Applies a planar map to the current selection. |
| Alt+R | Relax Brush Type Cycle | While held, toggles from UV Paint to the Relax brush. |
| Alt+E | Show Seams in Viewport | Toggles display of cluster seams in the viewport. Works only when Edit UVWs dialog has focus. |
| S | Snap | Toggles snapping. |
| Ctrl+Down Arrow, Ctrl+Page Down | Texture Vertex Contract Selection | Shrinks the selection in the Edit UVWs dialog. |
| Ctrl+Up Arrow, Ctrl+Page Up | Texture Vertex Expand Selection | Grows the selection in the Edit UVWs dialog. |
| W | Texture Vertex Move Mode | Moves vertices in editor. |
| E | Texture Vertex Rotate Mode | Rotates vertices in editor. |
| R | Texture Vertex Scale Mode | Scales vertices in editor. |
| Ctrl+W | Texture Vertex Weld Selected | Welds selected vertices in editor. |
| Ctrl+T | Texture Vertex Target Weld | Target-welds selected vertices in editor. |
| Alt+U | Unhide All | Unhides all hidden elements. |
| O (letter) | Unwrap Options |  |
| U | Update Map | Updates map in editor. |
| Alt+4 | UV Paint Movement |  |
| Alt+Z | Zoom |  |
| Alt+Ctrl+X | Zoom Extents |  |
| Z | Zoom Extents Selected |  |
| Ctrl+W | Zoom Region |  |
| Shift+spacebar | Zoom to Gizmo |  |
| Ctrl+Alt [hold] while transforming | Transform from the click point instead of the selection centre | Edit UVWs Dialog Toolbars |
| Ctrl+drag / Alt+drag (Freeform rotate) | Rotate in 5° / 1° steps | Edit UVWs Dialog Toolbars |
| Ctrl+select outside the gizmo | Expand the Freeform gizmo to the whole selection | Edit UVWs Dialog Toolbars |

### Compact Material Editor
Source: KST, Material Editor and SME Hotkeys

| Shortcut | Action | Notes |
|---|---|---|
| A | Assign Material to Selection | KST |
| O | Get Material | KST |
| Left | Go Backward to Sibling | KST |
| Right | Go Forward to Sibling | KST |
| Up | Go to Parent | KST |
| F9 | Make Preview | KST |
| M | Open Material Editor (last used mode) | KST Main UI; Material Editor |
| double-click a sample slot | Magnify the sample slot | Sample Slot Right-Click Menu |

### Slate Material Editor (SME)
Source: KST + Slate menu pages
All Slate keys require the Keyboard Shortcut Override Toggle.

| Shortcut | Action | Notes |
|---|---|---|
| A | Assign Material to Selection | KST |
| Del | Delete Selected | KST |
| H | Hide Unused Nodeslots | KST |
| L | Lay Out All | KST |
| C | Lay Out Children | KST |
| O | Material/Map Browser | KST |
| Alt+C | Move Children | KST |
| N | Navigator | KST |
| Alt+P | Pan to Selected | KST |
| Ctrl+P | Pan Tool | KST |
| P | Parameter Editor | KST |
| F2 | Rename | KST |
| Ctrl+A | Select All | KST |
| Shift+PgDown | Select Children | KST |
| Ctrl+I | Select Invert | KST |
| Ctrl+D | Select None | KST |
| Q | Select Tool | KST |
| Ctrl+T | Select Tree | KST |
| G | Show Grid | KST |
| U | Update Selected Previews | KST |
| Ctrl+Alt+Z | Zoom Extents | KST |
| Z | Zoom Extents Selected | KST |
| Ctrl+W | Zoom Region Tool | KST |
| Alt+Z | Zoom Tool | KST |
| S | Select Tool | Slate Toolbar; Select menu. Conflict: KST gives Q. |
| Ctrl+Q | Select All | Slate Select menu. Conflict: KST gives Ctrl+A. |
| Alt+U | Auto Update Selected Previews (toggle) | Slate Edit menu |
| Ctrl+Tab | Cycle named Views | Creating and Managing Named Views |
| Ctrl+click / Alt+click | Add / remove a node from the selection | Selecting, Moving, and Laying Out Nodes |
| Shift+drag a node | Clone the node |  |
| Ctrl+Shift+drag a node | Clone the node with its children |  |
| Ctrl+Alt+drag a node | Move with children (temporary) | Slate Toolbar; Options menu |
| Ctrl+Alt+MMB drag | Zoom the active View | Navigating the Slate Material Editor Active View (also ShaderFX work area) |
| Up / Down | Material/Map Browser: move through the list | Using the Keyboard to Navigate the Material/Map List |
| Left / Right | Material/Map Browser: collapse / expand a group |  |
| Enter | Material/Map Browser: add the material/map to the View, or toggle a group |  |

### Rendering, ActiveShade and frame windows
Source: KST + rendering pages

| Shortcut | Action | Notes |
|---|---|---|
| Shift+Q or Shift+F9 | Render (uses active Render flyout mode: Production or ActiveShade) | KST; About ActiveShade; Render Flyout |
| F9 | Render Last | KST |
| F10 | Render Setup | KST |
| 8 | Environment dialog | KST |
| 9 | Advanced Lighting panel | KST |
| Shift+V | Create Animated Sequence File | KST |
| Esc | Stop radiosity processing (legacy) | Radiosity Processing Parameters Rollout (Archive) |
| D | Draw Region | ActiveShade (KST Misc) |
| P | Initialize | ActiveShade (KST Misc) |
| F9 | Render | ActiveShade (KST Misc) |
| Q | Select Object | ActiveShade (KST Misc) |
| U | Update | ActiveShade (KST Misc) |
| Ctrl+click / Ctrl+RMB | Rendered Frame Window: zoom in / out | To Zoom and Pan in the Rendered Frame Window |
| Shift+drag | Rendered Frame Window: pan |  |
| Wheel / MMB drag | Rendered Frame Window: zoom (when not zoomed in) / pan |  |

### RAM Player
Source: RAM Player Keyboard Shortcuts

| Shortcut | Action | Notes |
|---|---|---|
| Home | Go To Start Frame |  |
| End | Go To End Frame |  |
| Left | Go To Previous Frame |  |
| Right | Go To Next Frame |  |
| Up | Playback Reverse |  |
| Down | Playback Forward |  |
| Esc or Ctrl+C | Stop Playback |  |
| Space | Toggle Playback or Stop |  |
| A | Toggle Channel A On/Off |  |
| B | Toggle Channel B On/Off |  |
| Ctrl+A | Open File in Channel A |  |
| Ctrl+B | Open File in Channel B |  |
| Alt+A | Open Last Rendered Image in Channel A |  |
| Alt+B | Open Last Rendered Image in Channel B |  |
| RMB drag or Ctrl+LMB drag | Scrub animation |  |

### Video Post (legacy)
Source: KST, Misc Hotkeys

| Shortcut | Action | Notes |
|---|---|---|
| F9 | Execute Sequence | KST Misc |
| Ctrl+Shift+N | New Sequence | KST Misc |
| Ctrl+P | Pan | KST Misc |
| Ctrl+Alt+Z | Zoom Extents | KST Misc |
| Ctrl+W | Zoom Region | KST Misc |

### Biped / character studio
Source: KST, Biped Hotkeys + Biped pages
The Biped page lists about 50 more Biped actions with no default key (Figure Mode, Footstep Mode, Mixer Mode, Layer commands, Bend Links ...).

| Shortcut | Action | Notes |
|---|---|---|
| Ctrl+C | Copy/Paste - Copy | KST |
| Ctrl+V | Copy/Paste - Paste | KST |
| Ctrl+Shift+V | Copy/Paste - Paste Opposite | KST |
| Alt+Ctrl+F | Fix Graphs | KST |
| Alt+M | Move All - Collapse | KST |
| Alt+K | Reset All Limb Keys | KST |
| Alt+Ctrl+E | Scale In Transform | KST |
| Alt+R | Set Animation Range | KST |
| K | Set Key | KST |
| Alt+T | Trackbar - Toggle Biped Keys | KST |
| Alt+D | TV Select end of footsteps | KST |
| Alt+S | TV Select entire foostep | KST |
| Alt+A | TV Select start of foosteps | KST |
| V | Play Biped (toggle Biped playback) | Biped Keyboard Shortcuts page; Previewing Biped Motion. Not in KST. |
| 0 (zero) | Set Key (Key Info rollout) | Setting Keys for Feet and Hands. Not in KST. |
| Q | Toggle left/right footstep while creating footsteps | Creating Footsteps Manually; Footstep Creation Rollout |
| Alt+C / Alt+V / Alt+B | Copy / paste posture commands | Copying and Pasting Postures and Poses (names not given beside the keys) |

### Physique (legacy, Archive book)
Source: KST + Physique Shortcuts

| Shortcut | Action | Notes |
|---|---|---|
| Ctrl+C | Copy Envelope | KST Misc |
| Del | Delete | KST Misc |
| PgDown | Next | KST Misc |
| Ctrl+V | Paste Envelope | KST Misc |
| PgUp | Previous | KST Misc |
| Ctrl+E | Reset Envelopes | KST Misc |
| Ctrl+D | Delete | Physique Shortcuts page. Conflict: KST gives Del. |
| I / Shift+I | Next / Previous Selection Level | Physique Shortcuts page |

### Crowd (legacy)
Source: KST + Crowd Shortcuts

| Shortcut | Action | Notes |
|---|---|---|
| S, F9 | Solve | KST Misc |
| — | Step Solve | Crowd Shortcuts page |

### Populate
Source: Define Idle Areas Panel (Populate)

| Shortcut | Action | Notes |
|---|---|---|
| Ctrl+Shift+drag | Resize the Modify Idle Areas brush | Define Idle Areas Panel |
| Ctrl+drag | Orient a new seat toward the cursor |  |

### Hair and Fur styling
Source: KST, Hair Styling Hotkeys

| Shortcut | Action | Notes |
|---|---|---|
| Shift+Ctrl+A | Attenuate | KST |
| Ctrl+B | Brush | KST |
| Shift+Ctrl+4 | Brush Clump | KST |
| Shift+Ctrl+3 | Brush Puff | KST |
| Shift+Ctrl+5 | Brush Rotate | KST |
| Shift+Ctrl+6 | Brush Scale | KST |
| Shift+Ctrl+2 | Brush Stand | KST |
| Shift+Ctrl+1 | Brush Translate | KST |
| Ctrl+M | Clump | KST |
| Alt+C | Cut | KST |
| Ctrl+PgUp, Ctrl+Up | Expand Selection | KST |
| Ctrl+2 | Guide | KST |
| Alt+H | Hide Selected | KST |
| Alt+Shift+X | Ignore Back | KST |
| Ctrl+I | Invert Selection | KST |
| Ctrl+L | Lock | KST |
| Shift+Ctrl+= | Merge Hairgroups | KST |
| Shift+Ctrl+P | Pop Selected | KST |
| Shift+Ctrl+Z | Pop Zerosized | KST |
| Ctrl+P | Puff | KST |
| Shift+Ctrl+M | Recomb | KST |
| Shift+Ctrl+T | Reset Rest | KST |
| Ctrl+4 | Root | KST |
| E | Rotate | KST |
| Shift+Ctrl+R | Rotate Selection | KST |
| R | Scale | KST |
| Q | Select | KST |
| Alt+U | Show Hidden | KST |
| Shift+Ctrl+F | Soft Falloff | KST |
| Shift+Ctrl+- | Split Hairgroups | KST |
| Ctrl+N | Stand | KST |
| Ctrl+1 | Tip | KST |
| Shift+Ctrl+C | Toggle Collisions | KST |
| Shift+Ctrl+I | Toggle Hairs | KST |
| Ctrl+T | Translate | KST |
| Ctrl+Z | Undo | KST |
| Ctrl+Shift+L | Unlock | KST |
| Ctrl+3 | Verts | KST |
| Ctrl+Shift+drag | Resize the styling brush | Styling Rollout; Quad Menu for Hair Styling |

### Particle Flow / Particle View
Source: KST + Particle Flow Keyboard Shortcuts

| Shortcut | Action | Notes |
|---|---|---|
| Alt+Ctrl+P | Clean Up Particle Flow | KST |
| Ctrl+C | Copy Selected In Particle View | KST |
| Alt+Ctrl+M | Open PFlow Preset Manager dialog | KST |
| 6 | Particle View Toggle | KST |
| Ctrl+V | Paste In Particle View | KST |
| Alt+Ctrl+C | Repair PFlow Cache System | KST |
| Alt+Ctrl+R | Reset Particle View | KST |
| Ctrl+A | Select All In Particle View | KST |
| Shift+; | Selected Particle Emission Toggle | KST |
| Alt+Ctrl+L | Synchronize Particle Flow Layers | KST |
| ; (semicolon) | Particle Emission Toggle (all particle systems) | Particle Flow Keyboard Shortcuts page. Not in KST. |

### Particle Flow Data View
Source: KST, Particle Flow Tools; Data View Hotkeys page (same keys)

| Shortcut | Action | Notes |
|---|---|---|
| Ctrl+C | Copy Selected In Data View | KST; Data View Hotkeys |
| Ctrl+X | Cut Selected In Data View | KST; Data View Hotkeys |
| S | Move Selected Down In Data View | KST; Data View Hotkeys |
| Shift+S | Move Selected Down x10 In Data View | KST; Data View Hotkeys |
| A | Move Selected Left In Data View | KST; Data View Hotkeys |
| Shift+A | Move Selected Left x10 In Data View | KST; Data View Hotkeys |
| D | Move Selected Right In Data View | KST; Data View Hotkeys |
| Shift+D | Move Selected Right x10 In Data View | KST; Data View Hotkeys |
| W | Move Selected Up In Data View | KST; Data View Hotkeys |
| Shift+W | Move Selected Up x10 In Data View | KST; Data View Hotkeys |
| Ctrl+V | Paste In Data View | KST; Data View Hotkeys |
| F2 | Rename Suboperator In Data View | KST; Data View Hotkeys |
| Ctrl+A | Select All In Data View | KST; Data View Hotkeys |
| Ctrl+D | Select None In Data View | KST; Data View Hotkeys |

### SteeringWheels and ViewCube
Source: KST

| Shortcut | Action | Notes |
|---|---|---|
| Shift+Ctrl+, | Decrease Walk Speed | KST |
| Shift+Ctrl+. | Increase Walk Speed | KST |
| Shift+W | Toggle SteeringWheels | KST |
| Shift+Ctrl+J | Tour Building Wheel | KST |
| Alt+Ctrl+H | Home | KST |
| Alt+Ctrl+V | Toggle ViewCube Visibility | KST |

### WalkThrough navigation
Source: KST + Using Walkthrough Navigation

| Shortcut | Action | Notes |
|---|---|---|
| Q | Accelerate Toggle | KST |
| S, Down | Back | KST |
| Z | Decelerate Toggle | KST |
| [ | Decrease Step Size | KST |
| C, Shift+Down | Down | KST |
| W, Up Arrow | Forward | KST |
| ] | Increase Step Size | KST |
| A, Left Arrow | Left | KST |
| Shift+Space | Level | KST |
| Space | Lock Vertical Rotation | KST |
| Alt+[ | Reset Step Size | KST |
| D, Right Arrow | Right | KST |
| E, Shift+Up Arrow | Up | KST |
| Up | Enter WalkThrough View Mode | KST, Main UI |
| — | Increase / Decrease Rotation Sensitivity; Invert Vertical Rotation; Lock Horizontal Rotation | Using Walkthrough Navigation: no default key |

### FFD modifiers
Source: KST, Misc Hotkeys

| Shortcut | Action | Notes |
|---|---|---|
| Alt+Shift+C | Switch To Control Point Level | KST Misc |
| Alt+Shift+L | Switch To Lattice Level | KST Misc |
| Alt+Shift+S | Switch To Set Volume Level | KST Misc |
| Alt+Shift+T | Switch To Top Level | KST Misc |

### NURBS
Source: KST + NURBS pages
Ctrl+L (Lock 2D Selection in KST) is also documented as the local Display Lattice toggle on the Display Controls page.

| Shortcut | Action | Notes |
|---|---|---|
| Alt+N | CV Constrained Normal Move | KST Misc |
| Alt+U | CV Constrained U Move | KST Misc |
| Alt+V | CV Constrained V Move | KST Misc |
| Shift+Ctrl+C | Display Curves | KST Misc |
| Alt+L | Display Shaded Lattice | KST Misc |
| Ctrl+L | Lock 2D Selection | KST Misc |
| Ctrl+Right | Select Next in U | KST Misc |
| Ctrl+Up | Select Next in V | KST Misc |
| Ctrl+Left | Select Previous in U | KST Misc |
| Ctrl+Down | Select Previous in V | KST Misc |
| H | Select Sub-Object By Name | KST Misc |
| Alt+1 | Set Tessellation Preset 1 | KST Misc |
| Alt+2 | Set Tessellation Preset 2 | KST Misc |
| Alt+3 | Set Tessellation Preset 3 | KST Misc |
| Shift+B | Soft Selection | KST Misc |
| Alt+Shift+Z | Switch To Curve CV Level | KST Misc |
| Alt+Shift+C | Switch To Curve Level | KST Misc |
| Alt+Shift+I | Switch To Imports Level | KST Misc |
| Alt+Shift+P | Switch To Point Level | KST Misc |
| Alt+Shift+V | Switch To Surface CV Level | KST Misc |
| Alt+Shift+S | Switch To Surface Level | KST Misc |
| Alt+Shift+T | Switch To Top Level | KST Misc |
| Ctrl+H | Select Sub-Objects dialog, only items under the cursor | NURBS Sub-Object Selection |
| Ctrl+Shift+S | Display Surfaces toggle | Display Controls for NURBS Models |
| Ctrl+D | Display Dependents toggle |  |
| Ctrl+Shift+T | Display Surface Trims toggle |  |
| Ctrl+X | Transform Degrade toggle (also during a transform) |  |
| Ctrl+T | NURBS Creation Toolbox toggle | Display Controls; Creating Curve Sub-Objects |
| Delete | Delete the selected point / CV / curve / surface sub-object | Editing Point/CV/Curve/Surface Sub-Objects |
| Ctrl+click, release, drag | Set height while creating a Point/CV curve point | Point Curve; CV Curve |

### Reaction Manager
Source: KST, Misc Hotkeys

| Shortcut | Action | Notes |
|---|---|---|
| Ctrl+I | Set Max Influence | KST Misc |
| Alt+I | Set Min Influence | KST Misc |

### Skin modifier and Weight Table
Source: KST + Skin pages

| Shortcut | Action | Notes |
|---|---|---|
| Ctrl+C | Copy | KST Misc (WeightTable) |
| Ctrl+V | Paste | KST Misc (WeightTable) |
| Ctrl+A | Select All | KST Misc (WeightTable) |
| Ctrl+I | Select Invert | KST Misc (WeightTable) |
| Ctrl+D | Select None | KST Misc (WeightTable) |
| B | Toggle Paint mode | KST Misc (PaintWeight) |
| B (while painting) | Switch between Painting and selecting a bone in the viewport | Skin Modifier Reference |
| Alt+Shift+drag | Adjust paint-weights brush strength | Parameters Rollout (Skin Modifier) |
| Ctrl+RMB in a cell | Enter a weight of 1.0 | Weight Table (Skin Modifier) |
| — | Select Vertices By Bone | Parameters Rollout: must be assigned by the user |

### Projection modifier
Source: KST + Projection modifier page

| Shortcut | Action | Notes |
|---|---|---|
| Alt+G | Geometry Selection Visibility Toggle | KST Main UI |
| B | Edit Soft Selection | KST Edit Hotkeys |
| Enter | Add a named sub-object selection set (Reference Geometry rollout) | Reference Geometry Rollout (Projection Modifier) |

### Viewport Canvas (texture painting)
Source: Viewport Canvas

| Shortcut | Action | Notes |
|---|---|---|
| Shift [hold] | Temporary Erase | Viewport Canvas |
| Ctrl [hold] | Sample colour from the surface (single pixel) |  |
| Space [hold] + click | Straight line from the last painted point |  |
| Ctrl+Shift+drag vertically | Brush radius |  |
| Alt+Shift+drag vertically | Brush opacity |  |
| Ctrl+Alt+drag vertically | Brush hardness |  |
| Alt+click | Clone tool: set the clone source point |  |
| RMB | Exit the tool and save paint to the bitmap |  |

### Scene Explorer
Source: Scene Explorer pages

| Shortcut | Action | Notes |
|---|---|---|
| Ctrl+Alt+O | Reopen the most recently closed Scene Explorer | Scene Explorer |
| Ctrl+click the arrow of a node | Expand / collapse the whole branch | Scene Explorer Menus; Right-Click Menus |
| Alt+click a toolbar filter button | Solo that filter (Alt+click again to restore) | Scene Explorer Toolbars |
| Shift+click / Ctrl+click | Range / toggle selection in the list | To Work with Scene Explorer |
| H | Select From Scene (Select By Name) dialog | KST |

### Camera Tracker utility: Movie window
Source: Camera Tracker: Movie Window

| Shortcut | Action | Notes |
|---|---|---|
| I | Zoom in on the selected gizmo (×2) | Camera Tracker: Movie Window |
| O | Zoom out (×2) |  |
| R | Reset zoom to 100% |  |
| Tab | Select the next numbered gizmo |  |
| 1–9, 0 | Select gizmo 1–10 (0 = 10) |  |
| Arrow keys | Nudge the selected gizmo |  |

### Asset Tracking, Retopology, misc
Source: feature pages

| Shortcut | Action | Notes |
|---|---|---|
| Shift+T | Asset Tracking dialog toggle | KST; Asset Tracking Dialog |
| 7 | Show poly count (Show Statistics) | Retopology Tools for 3ds Max; KST |
| Y (in a ribbon tooltip) | Play the tooltip video | The Ribbon; Ribbon Controls |
| Ctrl+drag / Alt+drag a toolbar button | Copy / move the button to a custom toolbar | Toolbars Panel (Customize) |

### MAXScript Scripting Editor (by feature area)
Source: Scripting Editor - Keyboard Shortcuts (MAXScript Help 2026; 2027 identical)

| Shortcut | Action | Notes |
|---|---|---|
| F1 | Help File | Help |
| Ctrl+N | New File | File Operations |
| Ctrl+O | Open File | File Operations |
| Ctrl+Shift+O | Open Selected Filename | File Operations |
| Ctrl+R | Revert File to last saved version | File Operations |
| Ctrl+W | Close File | File Operations |
| Ctrl+S | Save File | File Operations |
| Ctrl+Shift+S | Save File As | File Operations |
| Ctrl+Shift+P | Save As Copy | File Operations |
| Ctrl+P | Print File | File Operations |
| Ctrl+Tab, F6, Ctrl+PgDn | Cycle through files currently open in tabs | File Operations |
| Ctrl+Shift+Tab, Shift+F6, Ctrl+PgUp | Cycle backwards through tabs | File Operations |
| Ctrl+E | Evaluate All | Script Evaluation |
| Shift+ENTER, NumPad Enter | Evaluate Line/Selection | Script Evaluation |
| Ctrl+Z | Undo | Editing Operations |
| Ctrl+Y | Redo | Editing Operations |
| Ctrl+X | Cut | Editing Operations |
| Ctrl+C | Copy | Editing Operations |
| Ctrl+V | Paste | Editing Operations |
| Ctrl+Shift+D | Duplicate | Editing Operations |
| Ctrl+A | Select All | Editing Operations |
| Ctrl+L | Line cut | Editing Operations |
| Ctrl+Shift+T | Line copy | Editing Operations |
| Ctrl+Shift+L | Line delete | Editing Operations |
| Ctrl+T | Line transpose with previous | Editing Operations |
| Del | Delete | Deleting Text |
| Ctrl+D | Delete All in Listener | Deleting Text |
| Ctrl+Alt+D | Delete All in Editor | Deleting Text |
| Ctrl+BackSpace | Delete to start of word | Deleting Text |
| Ctrl+Delete | Delete to end of word | Deleting Text |
| Ctrl+Shift+BackSpace | Delete to start of line | Deleting Text |
| Ctrl+Shift+Delete | Delete to end of line | Deleting Text |
| Alt+F2 | Select to next bookmark | Selecting Text |
| Ctrl+Shift+Home | Extend selection to start of document | Selecting Text |
| Alt+Shift+Home | Extend selection to start of display line | Selecting Text |
| Ctrl+Shift+End | Extend selection to end of document | Selecting Text |
| Alt+Shift+End | Extend selection to end of display line | Selecting Text |
| Ctrl+Up | Scroll up | Navigation |
| Ctrl+Down | Scroll down | Navigation |
| Ctrl+[ | Previous paragraph. Shift extends selection | Navigation |
| Ctrl+] | Next paragraph. Shift extends selection | Navigation |
| Ctrl+Left | Previous word. Shift extends selection | Navigation |
| Ctrl+Right | Next word. Shift extends selection | Navigation |
| Ctrl+/ | Previous word part. Shift extends selection | Navigation |
| Ctrl+\ | Next word part. Shift extends selection | Navigation |
| Tab | Indent block | Indenting Text |
| Shift+Tab | De-indent block | Indenting Text |
| Ctrl+Shift+I | Change Indentation Settings | Indenting Text |
| Ctrl+B | Match Bracket | Bracket Balancer |
| Ctrl+Shift+B | Select to Bracket | Bracket Balancer |
| Ctrl+ENTER | Complete Word | Auto-Complete |
| Ctrl+Shift+A | Expand Abbreviation | Auto-Complete |
| Ctrl+Shift+R | Insert Abbreviation | Auto-Complete |
| Ctrl+Q | Block Comment or Uncomment | Commenting |
| Ctrl+Shift+C | Box Comment | Commenting |
| Ctrl+Shift+Q | Stream Comment | Commenting |
| Ctrl+Shift+U | Make Selection Uppercase | Upper/Lower Case |
| Ctrl+U | Make Selection Lowercase | Upper/Lower Case |
| Ctrl+F | Find | Search |
| F3 | Find Next | Search |
| Shift+F3 | Find Previous | Search |
| Ctrl+F3 | Find selection | Search |
| Ctrl+Shift+F3 | Find selection backwards | Search |
| Ctrl+H | Replace | Search |
| Ctrl+G | Go To.../ Find Again In Listener | Go To / Bookmarks |
| Ctrl+Home | Go to start of document | Go To / Bookmarks |
| Alt+Home | Go to start of display line | Go To / Bookmarks |
| Ctrl+End | Go to end of document | Go To / Bookmarks |
| Alt+End | Go to end of display line | Go To / Bookmarks |
| F2 | Next Bookmark | Go To / Bookmarks |
| Shift+F2 | Previous Bookmark | Go To / Bookmarks |
| Ctrl+F2 | Toggle Bookmark | Go To / Bookmarks |
| F11 | Full Screen | View |
| Ctrl+Shift+8 | Show Whitespaces | View |
| Ctrl+Shift+9 | Show End Of Line Characters | View |
| Ctrl+Numpad* | Expand or contract a fold point | View |
| Ctrl+Numpad+ | Magnify text size | Font Controls |
| Ctrl+Numpad- | Reduce text size | Font Controls |
| Ctrl+Numpad/ | Restore text size to normal | Font Controls |
| Ctrl+F11 | Toggle Monospaced Font | Font Controls |
| Shift+F11 | Switch to Text (No Syntax Coloring) | Font Controls |
| F4 | Next Message | Output Pane Controls |
| Shift+F4 | Previous Message | Output Pane Controls |
| Shift+F5 | Clear Output | Output Pane Controls |
| Ctrl+F6 | Switch to/from Output pane | Output Pane Controls |
| Ctrl+F5 | Add File | Source Control |
| Ctrl+Shift+F5 | Remove File | Source Control |
| Shift+F5 | Check In | Source Control |
| F5 | CheckOut | Source Control |

### MAXScript Scripting Editor and Listener: extra keys from the alphabetical table
Source: same page, second (alphabetical) table: rows not already in the table above, plus Listener-only rows
The page prints "Ctrl+|" for Word part left; it is probably Ctrl+\ (the feature table says Ctrl+\).

| Shortcut | Action | Notes |
|---|---|---|
| Numpad Enter | Evaluate Line / Selection | Editor and Listener |
| F6 | Cycle Tabs | Editor only |
| Ctrl+B | Select To Brace | Listener only |
| Ctrl+D | Delete All | Listener only |
| Ctrl+G | Find Again | Listener only |
| Ctrl+H | Replace | Listener only |
| Ctrl+R | Run Script | Listener only |
| Ctrl+Ins | Copy | Editor and Listener |
| Ctrl+Del | Delete word right | Editor and Listener |
| Ctrl+Back | Delete word left | Editor and Listener |
| Ctrl+Enter | Complete Word | Editor only |
| Ctrl+\|Word part left | Editor and Listener |  |
| Ctrl+Tab | Cycle Tabs | Editor only |
| Ctrl+PgDn | Cycle Tabs | Editor only |
| Ctrl+PgUp | Cycle Tabs Backwards | Editor only |
| Ctrl+Shift+Left | Word left extend | Editor and Listener |
| Ctrl+Shift+Right | Work right extend | Editor and Listener |
| Ctrl+Shift+Del | Delete line right | Editor and Listener |
| Ctrl+Shift+Back | Delete line left | Editor and Listener |
| Ctrl+Shift+/ | Word part right extend | Editor and Listener |
| Ctrl+Shift+\|Word part left extend | Editor and Listener |  |
| Ctrl+Shift+[ | Paragraph up extend | Editor and Listener |
| Ctrl+Shift+] | Paragraph down extend | Editor and Listener |
| Ctrl+Shift+Tab | Cycle Tabs Backwards | Editor only |
| Shift+Down | Line extend down | Editor and Listener |
| Shift+Up | Line extend up | Editor and Listener |
| Shift+Left | Character extend left | Editor and Listener |
| Shift+Right | Character extend right | Editor and Listener |
| Shift+Ins | Paste | Editor and Listener |
| Shift+Home | Line begin extend | Editor and Listener |
| Shift+End | Line end extend | Editor and Listener |
| Shift+Page Down | Page down extend | Editor and Listener |
| Shift+Page Up | Page up extend | Editor and Listener |
| Shift+Enter | Evaluate line/selection | Editor and Listener |
| Shift+F6 | Cycle Tabs Backwards | Editor only |
| Alt+Backspace | Undo | Editor and Listener |
| Alt+Mouse Drag | Window Select | Editor and Listener |
| Alt+Shift+Down | Line down rectangle extend | Editor and Listener |
| Alt+Shift+Up | Line up rectangle extend | Editor and Listener |
| Alt+Shift+Left | Character left rectangle extend | Editor and Listener |
| Alt+Shift+Right | Character right rectangle extend | Editor and Listener |
| Alt+Shift+Page Down | Page down rectangle extend | Editor and Listener |
| Alt+Shift+Page Up | Page up rectangle extend | Editor and Listener |
| Alt+Shift+Arrows | Window Select | Editor and Listener |

### MAXScript Listener
Source: Listener Commands

| Shortcut | Action | Notes |
|---|---|---|
| F11 | Open / close MAXScript Listener | KST; The Scripting Listener Window |
| Shift+Enter or Num Enter | Evaluate the line / selection (Python mode: always) | Listener Commands |
| Enter | New line inside existing text (no evaluation of selection) | Listener Commands |
| Ctrl+S / Ctrl+N / Ctrl+O / Ctrl+R | Save As / New Script / Open Script / Run Script | Listener Commands |
| Ctrl+Z | Undo (one level; removes last command output) |  |
| Ctrl+X / Ctrl+C / Ctrl+V / Ctrl+A | Cut / Copy / Paste / Select All |  |
| Ctrl+F / Ctrl+G / Ctrl+H | Find / Find Next / Replace |  |
| Ctrl+B | Select the text inside the current brackets |  |
| Ctrl+D | Delete all in Listener | Scripting Editor - Keyboard Shortcuts |

---

## Maya — complete

All tables are for Maya 2026 unless marked 2027. Keys are written as in the docs: letters are lower case unless the docs write Shift. On macOS, Ctrl = Control, Alt = Option and the Windows key = Command, except where the File/Edit rows say "Ctrl (Cmd)".

### Viewport and global: Tool Operations
Source: All Maya Hotkeys (2026)

| Shortcut | Action | Notes |
|---|---|---|
| Return | Complete current tool |  |
| Insert | Enter tool Edit mode |  |
| q | Select Tool, or with left mouse button for Selection Mask marking menu |  |
| w | Move Tool, or with left mouse button for Move Tool marking menu |  |
| e | Rotate Tool, or with left mouse button for Rotate Tool marking menu |  |
| r | Scale Tool, or with left mouse button for Scale Tool marking menu |  |
| Ctrl + t | Show universal manipulator tool |  |
| t | Show manipulator tool |  |
| y | Selects the last used tool that is not one of Select, Move, Rotate, or Scale |  |
| j | (Hold + drag) Move, Rotate, Scale Tool Snapping |  |
| =, + | Increase manipulator size |  |
| - | Decrease manipulator size |  |
| d | With left mouse button move pivot (Move Tool) |  |
| Insert | Switches between move pivot and move object (Move Tool) |  |
| Tab | Cycle through In-View editor values |  |
| Shift + Tab | Reverse-cycle through In-view Editor values. |  |
| Ctrl + Middle-drag (with the Move Tool) | Move components along their normals (Component Mode only) |  |
| Ctrl + Middle-drag (with the Rotate Tool) | Rotate components along their local X axes (Component Mode only) |  |
| Ctrl + Middle-drag (with the Scale Tool) | Scale components along their local YZ axes (Component Mode only) |  |

### Viewport and global: Action Operations
Source: All Maya Hotkeys (2026)

| Shortcut | Action | Notes |
|---|---|---|
| Ctrl + z | Undo |  |
| Ctrl + y | Redo |  |
| g | Repeat last action |  |
| F8 | Switch between object/component selection mode |  |
| p | Parent |  |
| Shift + P | Unparent |  |
| s | Set key |  |
| Shift + w | Key the selected object position |  |
| Shift + e | Key the selected object rotation |  |
| Shift + r | Key the selected object scale |  |

### Viewport and global: Hotbox Display
Source: All Maya Hotkeys (2026)

| Shortcut | Action | Notes |
|---|---|---|
| space | (When pressed down) Show the hotbox |  |
| Alt + m | Default Hotbox Style (Zones and Menu Rows) |  |

### Viewport and global: Displaying Objects (Show, Hide)
Source: All Maya Hotkeys (2026)

| Shortcut | Action | Notes |
|---|---|---|
| Ctrl + h | Display > Hide > Hide Selection |  |
| Shift + h | Display > Show > Show Selection |  |
| Ctrl+Shift + h | Display > Show > Show Last Hidden |  |
| Alt + h | Display > Hide > Hide Unselected Objects |  |
| Ctrl + 1 | Show > Isolate Select > View Selected (in the panel menus) |  |
| Alt + A | Cycle rig display mode: shows joints, controls, and character |  |

### Viewport and global: Display Settings
Source: All Maya Hotkeys (2026)

| Shortcut | Action | Notes |
|---|---|---|
| 4 | Shading > Wireframe |  |
| 5 | Shaded display |  |
| 6 | Shaded and Textured display |  |
| 7 | Lighting > Use All Lights |  |
| 0 | Default quality display setting |  |
| 1 | Rough quality display setting |  |
| 2 | Medium quality display setting |  |
| 3 | Smooth quality display setting |  |

### Viewport and global: File Operations
Source: All Maya Hotkeys (2026)

| Shortcut | Action | Notes |
|---|---|---|
| Ctrl (Cmd) + n | File > New Scene |  |
| Ctrl (Cmd) + o | File > Open Scene |  |
| Ctrl (Cmd) + s | File > Save Scene |  |
| Ctrl (Cmd) + Shift + s | File > Save Scene As |  |
| Ctrl (Cmd) + q | File > Exit |  |
| Ctrl + r | Create file reference |  |

### Viewport and global: Animation Operations
Source: All Maya Hotkeys (2026)

| Shortcut | Action | Notes |
|---|---|---|
| s | Set key |  |
| Shift + e | Set key for Rotate |  |
| Shift + r | Set key for Scale |  |
| Shift + w | Set key for Translate |  |
| Alt + i | Insert Keys (on any curve(s) inside or outside the Graph Editor that correspond to the position of the Current Time Indicator). Note: If the window focus is outside the Graph Editor, this hotkey inserts a key on all curves. If you are within the Graph Editor this hotkey sets a key on the selected curve. |  |
| Ctrl + Shift + e r w | Inserts a key on a specific channel: E for Rotation, R for Scaling, and W for translation, at the position of the Current Time Indicator. |  |
| i | With middle mouse button lets you insert a key anywhere on a selected curve, regardless of the position of the Current Time Indicator. |  |
| Shift + s | With left mouse button for Keyframe marking menu (or swipe left) |  |
| Shift + s | With middle mouse button for Tangent marking menu (or swipe right) |  |
| Alt + v | Play animation (Press v again to turn animation off) |  |
| Alt + j | Toggle Multicolor Feedback |  |
| Alt + 1 | Toggle NURBs curves visibility |  |
| Alt + 2 | Toggle Polygon mesh visibility |  |
| Alt + 4 | Toggle Image Plane visibility |  |
| Alt + 5 | Switch between Wireframe and Shaded view |  |
| Ctrl + 1 | Switches between joints, controls, and character visibility |  |
| Alt + t | Opens the Create Bookmark window. |  |
| Alt + Shift + t | Creates a bookmark for the selected time range. (Bookmarks created this way have no name and a random color associated with it. Modify this in the Bookmark Manager.) |  |
| \| (vertical bar) | Frame Bookmark: sets the playback range to the start and end of the current bookmark. (If multiple bookmarks overlap, the bookmark on top, the newest-created, is selected.) |  |
| : (colon) | Frame Previous Bookmark: sets the Range Slider on the bookmark before the bookmark at the current time. |  |
| " (quotation mark) | Frame Next Bookmark: sets the Range Slider on the bookmark after the bookmark at the current time. |  |
| Alt + \ (backslash) | Unframe Bookmark: sets the playback range to the animation range. |  |
| ' (apostrophe) | Bookmark selection step forward |  |
| ; (semicolon) | Bookmark selection step backward |  |
| Ctrl + drag | Reposition bookmark on the Time Slider. |  |
| Ctrl + drag left or right edge | Resize the bookmark on the Time Slider. |  |
| Ctrl + double-click | Selects the bookmark and the frames associated with it so you can move them together |  |

### Viewport and global: Playback Control
Source: All Maya Hotkeys (2026)
2027 rewords: Ctrl+Alt+. / , "Selects the next / previous key" (2026: "...in the Graph Editor without opening it"); adds tips about Loop Play Range while stepping.

| Shortcut | Action | Notes |
|---|---|---|
| Alt + . (period) | Move forward one frame in time |  |
| Alt + , (comma) | Move backward one frame in time |  |
| . (period) | Go to Next key |  |
| , (comma) | Go to Previous key |  |
| Ctrl + Alt + . (period) | Selects the Next key in the Graph Editor without opening it. |  |
| Ctrl + Alt + , (comma) | Selects the Previous key in the Graph Editor without opening it. |  |
| Alt + v | toggles playback on or off |  |
| Alt+Shift + v | Go to Min Frame (normally 0) |  |
| k | With middle mouse button for virtual Time Slider mode (press and hold and scrub timeline) |  |

### Viewport and global: Tumble, Track, or Dolly
Source: All Maya Hotkeys (2026)

| Shortcut | Action | Notes |
|---|---|---|
| Alt + Left mouse button | Tumble Tool (press and release) |  |
| Alt + Middle mouse button | Track Tool (press and release) |  |
| Alt + Right mouse button | Dolly Tool (press and release) |  |

### Viewport and global: 2D Pan/Zoom
Source: All Maya Hotkeys (2026)

| Shortcut | Action | Notes |
|---|---|---|
| \ + Middle mouse button | 2D Pan tool |  |
| \ + Right mouse button | 2D Zoom tool |  |
| \ | Enable/disable 2D Pan/Zoom. |  |

### Viewport and global: Painting Operations
Source: All Maya Hotkeys (2026)

| Shortcut | Action | Notes |
|---|---|---|
| Alt + f | Flood with the current value |  |
| Alt + a | Turn Show Wireframe on or off |  |
| Alt + c | Turn Color Feedback on or off |  |
| Alt + r | Toggle Reflection on or off |  |
| u | With left mouse button for Artisan Paint Operation marking menu |  |
| b | Modify upper brush radius (press and release) (Drag left or right for Blue Pencil stroke size) |  |
| Shift + B | Modify lower brush radius (press and release) |  |
| m | Modify maximum displacement (Sculpt Surfaces and Sculpt Polygons Tool) (Drag left or right for Blue Pencil opacity) |  |
| n | Modify paint value |  |
| / | Switch to pick color mode (press and release) |  |
| o | With left mouse button for the Poly Brush Tool marking menu |  |
| o | With middle mouse button for Poly UV Tool marking menu |  |

### Viewport and global: Snapping Operations
Source: All Maya Hotkeys (2026)

| Shortcut | Action | Notes |
|---|---|---|
| c | Snap to curves (press and release) |  |
| x | Snap to grids (press and release) |  |
| v | Snap to points (press and release) |  |
| j | Move, Rotate, Scale Tool snapping (press and release) |  |
| Shift + j | Move, Rotate, Scale Tool relative snapping (press and release) |  |

### Viewport and global: Selecting Objects and Components
Source: All Maya Hotkeys (2026)

| Shortcut | Action | Notes |
|---|---|---|
| F8 | Select > Object/Component (Switch between object and component editing) |  |
| F9 | Select > Vertex |  |
| F10 | Select > Edge |  |
| F11 | Select > Face |  |
| F12 | Select > UV |  |
| Ctrl + i | Select next intermediate object |  |
| Alt + F9 | Select > Vertex Face |  |
| < | Shrink polygon selection region |  |
| > | Grow polygon selection region |  |

### Viewport and global: Selecting Menus
Source: All Maya Hotkeys (2026)

| Shortcut | Action | Notes |
|---|---|---|
| Ctrl + m | Show/hide main menu bar |  |
| Shift + M | Show/hide panel menu bar |  |
| Ctrl+Shift + M | Show/hide panel toolbar |  |
| h | With Left mouse button for Menu Set marking menu |  |
| F2 | Show Modeling menu set |  |
| F3 | Show Rigging menu set |  |
| F4 | Show Animation menu set |  |
| F6 | Show Rendering menu set |  |

### Viewport and global: Edit Operations
Source: All Maya Hotkeys (2026)

| Shortcut | Action | Notes |
|---|---|---|
| Ctrl (Cmd) + z | Edit > Undo |  |
| Ctrl (Cmd) + y | Edit > Redo |  |
| g | Edit > Repeat |  |
| Shift + G | Repeat command at mouse position |  |
| Ctrl + d | Edit > Duplicate |  |
| Shift + Drag any transform manipulator | Edit > Duplicate |  |
| Ctrl+Shift + D | Edit > Duplicate Special |  |
| Shift + D | Edit > Duplicate with Transform |  |
| Ctrl + g | Edit > Group |  |
| p | Edit > Parent |  |
| Shift + P | Edit > Unparent |  |
| Ctrl (Cmd) + x | Edit > Cut |  |
| Ctrl (Cmd) + c | Edit > Copy |  |
| Ctrl (Cmd) + v | Edit > Paste |  |

### Viewport and global: Rendering
Source: All Maya Hotkeys (2026)

| Shortcut | Action | Notes |
|---|---|---|
| Ctrl + Left arrow | Render view next image |  |
| Ctrl + Right arrow | Render view previous image |  |
| Ctrl + P | Open the Color Chooser in a modal window. When opened using this hotkey rather than from a swatch, you can save colors to the Color History or use the Eyedropper to select or inspect colors on screen. You can also load, save, and edit palettes. However, you cannot set color attributes on scene objects. |  |

### Viewport and global: Window and View Operations
Source: All Maya Hotkeys (2026)

| Shortcut | Action | Notes |
|---|---|---|
| Alt + Middle mouse | Pan in the Outliner |  |
| Alt + Ctrl + Middle mouse | Fast pan in the Outliner |  |
| Alt + Middle mouse | Pan in the Attribute Editor |  |
| Ctrl + a | Switches between Attribute Editor or Channel Box–displays the Attribute Editor if neither is shown |  |
| a | Frame All in active panel, or with left mouse button for History Operations marking menu |  |
| Shift + A | Frame All in all views |  |
| f | Frame Selected in active panel |  |
| Shift + F | Frame Selected in all views |  |
| space | (When tapped) Switch between the active window in multi-pane display and single pane display |  |
| Ctrl + space | Switch between the standard view and full-screen view of the current panels |  |
| ] (Right square bracket) | Redo view change |  |
| [ (Left square bracket) | Undo view change |  |
| Alt + b | Switch between a gradient, black, dark gray, or light gray background color. |  |
| Shift + { (Left brace bracket) | View previous layout |  |
| Shift + } (Right brace bracket) | View next layout |  |
| F1 | Help > Maya Help |  |

### Viewport and global: Moving Selected Objects
Source: All Maya Hotkeys (2026)

| Shortcut | Action | Notes |
|---|---|---|
| Alt + Up | Move up one pixel |  |
| Alt + Down | Move down one pixel |  |
| Alt + Left | Move left one pixel |  |
| Alt + Right | Move right one pixel |  |

### Viewport and global: Pick Walk
Source: All Maya Hotkeys (2026)
Arrow keys walk the hierarchy (object selected) or around components (component selected).

| Shortcut | Action | Notes |
|---|---|---|
| Up | Walk up current |  |
| Down | Walk down current |  |
| Left | Walk left in current |  |
| Right | Walk right in current |  |

### Viewport and global: Modeling Operations
Source: All Maya Hotkeys (2026)

| Shortcut | Action | Notes |
|---|---|---|
| 1 | Default polygon mesh display (no smoothing) |  |
| 2 | Cage + smooth polygon mesh display |  |
| 3 | Smooth polygon mesh display |  |
| Ctrl + F9 | Convert polygon selection to Vertices |  |
| Ctrl + F10 | Convert polygon selection to Edges |  |
| Ctrl + F11 | Covert polygon selection to Faces |  |
| Ctrl + F12 | Covert polygon selection to UVs |  |
| Ctrl + \` | Proxy > Subdiv Proxy Displays original mesh (proxy) and a smoothed version of the original. |  |
| Ctrl+Shift + \` | Proxy > Subdiv Proxy > Displays Subdiv Proxy options window |  |
| \` | Toggles the display between the original (proxy) and the smoothed mesh. |  |
| ~ | Displays both the original (proxy) and the smoothed mesh. |  |
| Alt + \` | Modify > Convert > NURBS to Subdiv, Polygons to Subdiv |  |
| Alt+Shift + ~ | Displays option window for Modify > Convert > NURBS to Subdiv > or Polygons to Subdiv > (depending on whether NURBS or Polygons are selected). |  |
| Page Up | Increases Division Levels for Smooth Mesh Preview or Subdiv Proxy. |  |
| Page Down | Decreases Division Levels for Smooth Mesh Preview or Subdiv Proxy. |  |
| l | Lock/unlock length of curve (press and hold) |  |
| Ctrl+Shift + Drag transform manipulator | Slide selected component along edge. You can also middle-drag anywhere on the screen. |  |
| Shift + Drag transform manipulator | Extrude currently selected component (Component Mode only). |  |
| Ctrl + Middle-drag | Move components along their normals (Move Tool only) |  |
| Ctrl + Middle-drag | Rotate component groups along their local X axes (Rotate Tool only) |  |
| Ctrl + Middle-drag | Scale component groups along their local YZ axes (Scale Tool only) |  |
| Ctrl+Shift + Q | Activate Quad Draw Tool. |  |
| Ctrl+Shift + X | Activate Multi-Cut Tool. |  |

### Time Editor (Animation hotkeys page)
Source: Animation hotkeys (2026)

| Shortcut | Action | Notes |
|---|---|---|
| q | Toggle Time Editor Mute on or off |  |
| m | Toggle Time Editor Track mute on or off |  |
| n | Toggle Solo Track on or off |  |
| Ctrl + e | Export selected |  |
| i | Import animation clip |  |
| Shift + i | Import audio clip |  |
| l | Create Additive layer |  |
| Shift + L | Create Override layer |  |
| o | Add animation from scene selection |  |
| p | Add pose from scene selection |  |
| a | Frame all |  |
| f | Frame selection |  |
| w | Split clip at current frame |  |
| g | Trim clip before |  |
| h | Trim clip after |  |
| Shift + G | Scale clip start to current frame |  |
| Shift + H | Scale clip end to current frame |  |
| e | Trim clip |  |
| r | Scale clip |  |
| t | Loop clip |  |
| y | Hold clip |  |
| Ctrl + g | Group clips |  |
| Ctrl+Shift + G | Ungroup clips |  |

### Graph Editor (Animation hotkeys page)
Source: Animation hotkeys (2026)

| Shortcut | Action | Notes |
|---|---|---|
| Alt + z | Undo view change |  |
| Alt + y | Redo view change |  |
| t | Center current time |  |
| Alt + / (forward slash) | Snap Time Marker to selected key |  |
| 1 | Switch to Absolute view |  |
| 2 | Switch to Stacked view |  |
| 3 | Switch to Normalized view |  |
| h | Lock Curve channel |  |
| j | Unlock Curve channel |  |
| d | Auto Tangents |  |
| Shift + 9 | Move selected key(s) left |  |
| Shift + 0 | Move selected key(s) right |  |
| Ctrl + Alt + , (comma) | Select the previous key |  |
| Ctrl + Alt + . (period) | Select the next key |  |
| Shift + | Switches to the Smooth Tool while using other Curve Sculpting tools. Hold Shift while middle-dragging to adjust size or strength. |  |
| MMB Drag left or right | Changes the Graph Editor Curve sculpting tools brush size. |  |
| Ctrl + Middle-drag left or right | Changes the Graph Editor Curve sculpting tools brush size starting at zero. |  |
| MMB Drag up or down | Changes the Graph Editor Curve sculpting tools brush strength. |  |
| Ctrl + Middle-drag up or down | Changes the Graph Editor Curve sculpting tools brush strength starting at zero. |  |

### Time Slider (Interface hotkeys page)
Source: Interface hotkeys (2026)
The Time Slider Bookmarks page gives Shift+| , Shift+; and Shift+: for Frame / Frame Previous / Frame Next Bookmark, and the Animation controls menu page gives "," for Frame Next Bookmark. The hotkey tables give | , : and " (no Shift). Prefer the hotkey tables.

| Shortcut | Action | Notes |
|---|---|---|
| s | Sets a key on the Time Slider |  |
| Shift + Drag | Select a range of key ticks on the Time Slider |  |
| Shift+Alt + Drag | Select range of key ticks on the Time Slider but does not update the animation as you drag |  |
| Ctrl + Drag the icon in the center of the selection of keys | Copy and move the selected key ticks on the Time Slider |  |
| Ctrl + Drag the arrow icons on either side of the key selection. | Scale the highlighted blue selection of keys on the Time Slider |  |
| MMB Drag | Cut and move the highlighted blue selection of keys on the Time Slider |  |
| Alt + T | Create a Time Slider bookmark on the Time Slider |  |
| Alt+Shift + T | Quick Create Bookmark (doesn't open the Create Time Slider Bookmark window) |  |
| ' (apostrophe) | Set the current time to the start of the following bookmark |  |
| ; (semicolon) | Set the current time to the start of the preceding bookmark |  |
| \| (vertical bar) | Set the playback range to the start and end of the current bookmark. (If multiple bookmarks overlap, the bookmark on top, the newest-created, is selected) |  |
| : (colon) | Set the Range Slider on the bookmark before the bookmark at the current time |  |
| " (quotation mark) | Set the Range Slider on the bookmark after the bookmark at the current time |  |
| Alt + \ (backslash) | Sets the playback range to the animation range |  |

### Tool and action page extras
Source: Tool and action hotkeys (2026)

| Shortcut | Action | Notes |
|---|---|---|
| Ctrl + a | Attribute Editor | Tool and action hotkeys: "Attribute Editor" section |
| x / c / v | Snap to grids / curves / points | Tool and action hotkeys: "Snap To Operations" |

### Walk Tool (new table in 2027)
Source: Tool and action hotkeys / All Maya Hotkeys 2027
The Walk Tool itself exists in 2026; the table was added to the hotkey pages in 2027.

| Shortcut | Action | Notes |
|---|---|---|
| Drag the cursor | Look around the scene |  |
| Left-click | Select a normal speed |  |
| Middle-click | Select a slow speed |  |
| Right-click | Select a fast speed See also Control Walk Tool speed. |  |
| S or Down arrow | Move backward |  |
| W or Up arrow | Move forward |  |
| A or Left arrow | Strafe left |  |
| D or Right arrow | Strafe right |  |
| Q or / (forward slash) | Move up |  |
| E or ' (apostrophe) | Move down |  |
| (W + A/D) or (Up + Left/Right arrow) | Move diagonally upward |  |
| (S + A/D) or (Down + Left/Right arrow) | Move diagonally downward See also Control direction of Walk Tool movement. |  |
| Ctrl | Crouch | Hold = crouch until released; tap = crouch until Ctrl is pressed again |
| Scroll the mouse wheel up. | Zoom in |  |
| Scroll the mouse wheel down. | Zoom out |  |
| Alt + x | Enter / exit walk mode | Walk through the scene; Camera Tools menu (2026 docs too) |

### View hotkeys page extras
Source: View hotkeys

| Shortcut | Action | Notes |
|---|---|---|
| Alt + LMB + MMB drag | Dolly | View hotkeys |
| Shift + Space | Zoom-in display of the view under the pointer (collapses other docked panes); again to restore | View hotkeys; Interface overview |
| Ctrl + Space | Full-screen display of the view under the pointer (also hides Status Line, Shelf, Time Slider) | View hotkeys; Interface overview |
| Alt + b | Cycle viewport background: standard light grey, dark grey, black (All Maya Hotkeys adds gradient) | View hotkeys |

### Viewport: additional bindings from menu and feature pages
Source: menu and feature pages listed in Sources

| Shortcut | Action | Notes |
|---|---|---|
| Ctrl + Shift + a | Select > All | Select menu |
| Alt + d | Select > Deselect All | Select menu; Shape Editor |
| Ctrl + Shift + i | Select > Inverse | Select menu |
| Shift + . (>) | Select > Grow | Select menu (same key as > in the hotkey tables) |
| Ctrl + f | Frame Selection with Children (active panel) | Panel menu: View; Display menu; Frame all or selected |
| Ctrl + Shift + f | Frame Selection with Children in All Views | same pages |
| Ctrl + f | Open / cycle the Search field (menus, tools, commands, objects) | Search for menus, tools, commands, or objects. Conflict with Frame Selection with Children. |
| Ctrl + click / Ctrl + Enter in Search | Run a command without closing Search | Search page |
| h | Toggle visibility of selected objects / components | Display menu; Show or hide objects/components; Outliner |
| Ctrl + Alt + h | Show all hidden components (also Shift + h) | Show or hide components; Show Options |
| Ctrl + Delete or Ctrl + Backspace | Quickly delete components | Edit Mesh menu |
| Shift + \` | Display both original and converted subdiv / proxy and smooth mesh | Subdiv proxy overview; NURBS to Subdiv options (hotkey tables list ~ for this) |
| Alt + Shift + \` | Option window for NURBS/Polygons to Subdiv | NURBS to Subdiv options (hotkey tables write Alt+Shift+~) |
| Alt + 3 | Toggle Displacement Preview on selected polygon objects | Smooth Mesh |
| Ctrl + Alt + drag box | Box dolly (left→right in, right→left out) | Tumble, track, dolly...; Dolly Tool options |
| Shift [hold] while tumbling / tracking | Constrain camera movement | Camera Tools menu |
| Alt + z / Alt + y | Undo / redo camera view change (Graph Editor and views) | Tumble, track, dolly page; Animation hotkeys (Graph Editor) |
| Shift + MMB drag (no handle selected) | Move / scale in the drag direction | Move objects and components; Scale objects |
| Ctrl + click a manipulator axis / box | Activate the corresponding plane handle | Move / Scale pages |
| Shift + click (pivot mode) | Place the pivot at the cursor / snap to a component | Change the pivot point |
| Ctrl + click (pivot mode) | Snap pivot axis orientation to a component | Change the pivot point |
| Ctrl + Shift + click (pivot mode) | Aim the pivot at the cursor | Change the pivot point |
| c or v [hold] + MMB drag (pivot mode) | Snap the pivot to another object's edges / vertices | Change the pivot point |
| Alt + MMB / Ctrl + Alt + MMB drag | Pan / fast pan the Attribute Editor | Attribute Editor |
| Ctrl + a twice | Attribute Editor, then Channel Control Editor | Channel Control Editor |

### Graph Editor (feature pages, beyond the hotkey table)
Source: Graph Editor pages

| Shortcut | Action | Notes |
|---|---|---|
| Alt + MMB drag | Pan | Graph Editor |
| Alt + drag or Alt + RMB drag | Zoom (centred on the pointer) |  |
| Alt + Shift + RMB drag | Zoom horizontally |  |
| f | Frame the selected curve |  |
| a | Frame all | Dope Sheet/Graph Editor shared |
| k [hold] + drag | Scrub in the graph view (releases the cursor lock) |  |
| [ / ] | Previous / next view |  |
| Shift + s + LMB, swipe left / MMB, swipe right | Keyframe Tangent marking menu: keys / tangents | Keyframe Tangent Marking Menu |
| i + MMB on a curve | Insert a key anywhere on the selected curve |  |
| Alt + i | Insert Keys Tool | Graph Editor Keys menu |
| Alt + / | Snap Time to Selection | Graph Editor Select menu |
| d | Tangents > Auto | Graph Editor Tangents menu |
| Shift + MMB drag | Move keys in time only | Graph Editor |
| Alt [hold] while repositioning a selection box | Move a region of keys |  |
| MMB drag in empty space | Move selected keys |  |
| Ctrl + m / Shift + m | Show / hide the Graph Editor menu bar | Graph Editor menus |
| Ctrl + c / Ctrl + v | Copy / paste keys | Copy and paste keys in the Graph Editor |
| Ctrl + MMB drag | Curve Sculpting: start brush radius / strength at zero | Sculpt curves with the Graph Editor Curve Sculpting tools |

### Dope Sheet
Source: Dope Sheet pages

| Shortcut | Action | Notes |
|---|---|---|
| q / w / r | Select Tool / Move Keys Tool / Scale Keys Tool | Dope Sheet toolbar; Edit menu |
| Ctrl + z / Ctrl + y | Undo / Redo | Dope Sheet Edit menu |
| Ctrl + x / Ctrl + c / Ctrl + v | Cut / Copy / Paste keys |  |
| Delete | Delete keys |  |
| a / f | Frame All / Frame Selection | Dope Sheet View menu |
| g | Frame Playback Range |  |
| t | Center Current Time |  |
| h / j | Lock / unlock channel | Dope Sheet Editor; Channels menu |
| Alt + MMB drag | Pan | Dope Sheet Editor |
| Shift + double-click a selected key | Enter one value for all selected keys | Edit keys using the Dope Sheet |
| f (in the Dope Sheet outliner) | Find the node of the selected object | Dope Sheet Outliner contextual menu |

### Time Slider and playback (feature pages)
Source: Playback Controls; Time Slider

| Shortcut | Action | Notes |
|---|---|---|
| Alt + , | Step back one frame | Playback Controls |
| , | Step back one key |  |
| Alt + v | Play forwards |  |
| . | Step forward one key |  |
| Alt + . | Step forward one frame |  |
| Esc | Stop playback (also stops Play Backwards) |  |
| Shift + drag | Select / move a range of keys | Time Slider |
| Ctrl + drag | Copy keys | Time Slider |
| Shift + Alt + drag | Move keys without updating the viewport | Time Slider |
| — | Play Backwards, Go To Start, Go To End | Playback Controls: no default key |

### Time Editor and Trax (feature pages)
Source: Time Editor / Trax pages
Trax has no other documented default keys.

| Shortcut | Action | Notes |
|---|---|---|
| k [hold] + drag | Scrub the Time Editor Current Time Marker (otherwise locked) | Time Editor Current Time Marker |
| 1 | Split the selected clip at the Current Time Marker | Edit animation in the Time Editor. Conflict: the Animation hotkeys table gives w for Split clip. |
| Ctrl + g / Ctrl + Shift + g | Group / ungroup clips | Time Editor toolbar and menu bar |
| f | Frame the time warp curve (Time Editor and Trax) | Create and edit time warps in Trax / Time Editor |

### Camera Sequencer
Source: Camera Sequencer

| Shortcut | Action | Notes |
|---|---|---|
| Alt + MMB drag | Scroll the shot view | Camera Sequencer |
| Delete | Delete the selected shot |  |
| Shift + click | Select multiple shots |  |

### Node Editor and Hypershade
Source: Node Editor and Hypershade Hotkeys + related pages

| Shortcut | Action | Notes |
|---|---|---|
| 1, 2, 3, 4 | View modes: simple, connected, full, custom attribute view | Node Editor and Hypershade |
| 5 | Cycle node name / node type / no title |  |
| = / - | Zoom in / out |  |
| Delete / Backspace | Remove nodes from the scene |  |
| Tab | Create node |  |
| , | Select connected upstream nodes |  |
| . | Select connected downstream nodes |  |
| / | Select upstream and downstream nodes |  |
| Ctrl + l | Remove selected nodes from the graph |  |
| Ctrl + / | Remove unselected nodes from the graph |  |
| Ctrl + , | Remove upstream nodes (incl. selected) from the graph |  |
| Ctrl + . | Remove downstream nodes (incl. selected) from the graph |  |
| Shift + , (<) | Regraph upstream nodes |  |
| Shift + . (>) | Regraph downstream nodes |  |
| Shift + / (?) | Regraph upstream and downstream |  |
| s | Toggle attribute search field in the node (Node Editor only) |  |
| Shift + c | Sync Node Editor / viewport selection (Node Editor only) | also Node Editor marking menus |
| v | Toggle selection swatch size (Node Editor only) |  |
| Left / Right | Pickwalk sibling nodes (Node Editor only) |  |
| Up / Down | Pickwalk parent / child nodes (Node Editor only) |  |
| p | Pin / unpin (Node Editor only) |  |
| l | Lay out the graph (Node Editor only) |  |
| @ | Solo the selected node (Hypershade only) |  |
| # | Remove soloing (Hypershade only) |  |
| ! | Solo the last soloed node/attribute (Hypershade only) |  |
| Ctrl + Alt + LMB drag left→right / right→left | Marquee zoom in / out | Zooming in and out of the Node Editor |
| Alt + RMB drag | Zoom at the pointer |  |
| Ctrl + MMB drag a node onto another | Connect with the default connection | Create and connect nodes in the Hypershade |
| Shift + Alt + drag across wires | Delete connections |  |
| Alt + RMB drag / Alt + drag in Browser tabs | Dolly to flip through swatch sizes | Hypershade View menu; Browser |
| RMB | Node / connection / empty-space marking menus | Node Editor and Hypershade Marking Menus |

### UV Editor (UV Editor hotkeys page)
Source: UV Editor hotkeys (2026)

| Shortcut | Action | Notes |
|---|---|---|
| 4 | Wireframe mode |  |
| 5 | Shaded mode. See UV Editor View menu. |  |
| 6 | Display texture image |  |
| 7 | Toggle UV Distortion display. See Identify a UV distortion. |  |
| Ctrl + Shift + A | Select all active components |  |
| Ctrl + Shift + I | Invert current selection |  |
| Ctrl + < or > | Shrink or grow selection |  |
| Ctrl + C | Copies last selected face |  |
| Ctrl + V | Pastes last face added to clipboard |  |
| Ctrl + L | Lay out the current selection. See Layout UV shells. |  |
| Ctrl + U | Unfold the current selection. See Unfold a UV mesh. |  |
| Ctrl + Shift + X | Create a UV Shell from the current selection |  |
| Ctrl + Shift + Drag | When a transform tool is active, this constrains movement to edges. |  |
| Shift + X | Cut currently selected edges. See Separate and attach UV shells. |  |
| Shift + S | Sew currently selected edges. See Separate and attach UV shells. |  |
| Q, W, E, R | Activate Select, Translate, Rotate, or Scale Tool respectively |  |
| A | Frame all UV shells for the selected object. |  |
| F | Frame all selected components / shells. |  |
| Ctrl + Up, Down | Increase / Decrease resolution of checker map (when Checker Map is enabled). |  |

### UV Editor and UV Toolkit (feature pages)
Source: UV pages

| Shortcut | Action | Notes |
|---|---|---|
| Shift + RMB | UV Editor component marking menu | UV Editor marking menus |
| Ctrl + RMB | UV Editor selection / convert marking menu |  |
| Shift + click a UV Toolkit button | Open that tool's options | UV Editor overview |
| RMB on Normalize | Scale each face to fill 0–1 space | UV Editor overview |
| Alt + MMB / Alt + RMB drag | Track / dolly the UV Editor view | Dolly or track within the UV Editor |
| double-click / Shift + double-click | Select a loop / partial loop | Select component loops in the UV Editor |
| Ctrl + double-click | Deselect a full / partial loop |  |
| Shift + double-click a parallel edge | Select a full / partial edge ring | Select edge rings in the UV Editor |
| Ctrl + double-click a parallel edge | Deselect a full / partial edge ring |  |
| Ctrl + double-click a vertex / face / UV | Deselect all connected components | Select UV shells |
| Shift + x / Shift + s | Cut / Sew (Cut and Sew) | Separate and attach UVs |
| drag / Shift + drag (3D Cut and Sew) | Cut UVs / cut along an edge loop | 3D Cut and Sew UV Tool |
| click / double-click | Cut UV edge / edge loop |  |
| Shift + double-click | Cut an edge loop between two edges |  |
| Tab [hold] | UV Edge Loop selection constraint |  |
| Ctrl + click / Ctrl + double-click | Sew UV edge / edge loop |  |
| Ctrl + Shift + drag / Ctrl + Shift + double-click | Sew along an edge loop / between two edges |  |
| x | Cut highlighted edges (Face mask: create UV shell) |  |
| s | Sew highlighted edges (UV Shell mask: sew shell borders) |  |
| d / Shift + d | Unfold shell and lay out / unfold only |  |
| Ctrl + Shift + s | Warning: toggles the Keyframe Tangent marking menu off | UV menu |
| b + drag or MMB drag left/right | Brush size (Smear, Pinch, Pin, Symmetrize and other UV brushes) | Smear / Pinch / Pin / Symmetrize UV Tool |
| m + drag or MMB drag up/down | Brush strength |  |
| Ctrl [hold] | Inverse brush operation (Smear, Pinch, Pin) |  |
| Ctrl + MMB drag | Symmetrize: move the line of symmetry | Symmetrize UV Tool |
| Ctrl + drag | Symmetrize: mirror the whole shell under the brush |  |

### Modeling Toolkit
Source: Modeling Toolkit hotkeys

| Shortcut | Action | Notes |
|---|---|---|
| Ctrl + Tab | Multi-component selection mode | Modeling Toolkit hotkeys |
| F9 / F10 / F11 | Vertex / Edge / Face selection mode |  |
| Ctrl + click a selection-mode icon | Switch component modes |  |
| \` | Tweak mode |  |
| b | Soft selection mode |  |
| d | Custom pivot editing mode |  |
| x / c / v | Snap to grid intersections / curves / CV, vertex, pivot |  |
| click an edge (Connect) | Insert an edge loop |  |
| Shift + click a component | Insert connecting edges between components |  |
| Ctrl + click a component | Remove components from the selection |  |
| drag / MMB drag (Target Weld) | Merge components / merge to centre |  |

### Multi-Cut Tool
Source: Multi-Cut Tool hotkeys

| Shortcut | Action | Notes |
|---|---|---|
| click / drag | Drop a new point or move an existing one | Multi-Cut Tool hotkeys |
| Ctrl + click (no points yet) | Insert an edge loop |  |
| Ctrl + MMB click (no points yet) | Insert an edge loop snapped to the middle |  |
| Ctrl + Shift + click (no points yet) | Insert an edge loop snapped to Snap Step % |  |
| Ctrl + drag / Ctrl + Shift + drag | Preview the edge loop | Insert an edge loop with the Multi-Cut Tool |
| Shift + click an edge (points placed) | Snap the cut point to Snap Step % increments |  |
| Shift + drag over an edge | Set Snap Step % interactively |  |
| Ctrl + Shift + click (points placed) | Constrain to perpendicular angles |  |
| x [hold] + click / v [hold] + click | Snap slice point to grid / to other points |  |
| drag from off the mesh | Slice faces |  |
| MMB drag anywhere | Quick slice faces |  |
| Backspace / Delete | Undo last point or delete highlighted edge |  |
| z / Shift + z | Undo / redo any action |  |
| MMB drag a slice plane | Reposition the slice plane |  |
| RMB / Enter | Complete the cut or slice |  |
| Esc | Cancel |  |
| Ctrl + Shift + RMB | Multi-Cut marking menu |  |
| Ctrl + Shift + x | Activate Multi-Cut | All Maya Hotkeys |

### Quad Draw Tool
Source: Quad Draw Tool hotkeys

| Shortcut | Action | Notes |
|---|---|---|
| click the reference surface or grid | Drop dots | Quad Draw Tool hotkeys |
| drag or MMB drag | Tweak components |  |
| Shift + drag | On mesh: relax vertices. Off mesh: create quads or triangles |  |
| Shift + MMB drag | Relax a selection of vertices (right relaxes, left undoes) | also Relax vertices with Quad Draw |
| Ctrl + click | Insert an edge loop |  |
| Ctrl + MMB click | Insert an edge loop snapped to face centres |  |
| Ctrl + Shift + click | Delete components |  |
| Ctrl + Shift + MMB drag | Move an edge loop |  |
| Tab + drag | On mesh: extend an edge. Off mesh: create quad strips |  |
| Tab + MMB drag | On mesh: extend an edge loop. Off mesh: resize quad strips |  |
| y | Reactivate the Quad Draw Tool |  |
| Ctrl + Shift + RMB | Quad Draw marking menu | Quad Draw tool marking menu |
| Ctrl + Shift + q | Activate Quad Draw | All Maya Hotkeys |

### Other modeling tools (feature pages)
Source: Modeling feature pages

| Shortcut | Action | Notes |
|---|---|---|
| Ctrl + e | Extrude | Extrude; All Maya Hotkeys |
| Ctrl + Shift + RMB | Tool / In-View Editor marking menu (Extrude, Connect, transform tools) | Extrude; Connect Tool; Edit Mesh menu |
| Ctrl + Tab / Ctrl + Shift + Tab | Cycle In-View Editor attributes | In-View Editor; Extrude (the two pages give opposite directions) |
| Ctrl / Ctrl + Shift / Shift [hold] while dragging an In-View Editor attribute | Slow down / speed up the value change | In-View Editor |
| t | Show manipulator (needed before the In-View Editor shows) | In-View Editor |
| y | Reactivate Target Weld / Connect Tool (last tool) | Target Weld; Connect Tool |
| Shift + RMB on a tangent handle / anchor | Break / smooth Bezier tangents | Break/Smooth tangents |
| Ctrl + drag a tangent | Bezier Curve Tool: break tangent |  |
| Ctrl + RMB on a curve | Select first / last / all CVs | Select curve CVs |

### Sculpting tools
Source: Sculpting tool hotkeys (KeyboardShortcuts and Modeling books, same page)
The table header changed from "Windows" (2026) to "Windows and Linux" (2027). Keys unchanged.

| Shortcut | Action | Notes |
|---|---|---|
| b + drag or MMB drag left/right | Adjust brush size | Sculpting tool hotkeys |
| b + MMB drag or Ctrl + MMB drag left/right | Adjust brush size from 0 |  |
| m + drag or MMB drag up/down | Adjust brush strength |  |
| m + MMB drag or Ctrl + MMB drag up/down | Adjust brush strength from 0 |  |
| Ctrl [hold] | Invert (Grab tool: Averaged Normal) |  |
| Ctrl + Shift + i | Invert Frozen |  |
| Shift + u | Unfreeze All |  |
| Shift [hold] | Temporary Smooth |  |
| Ctrl + Shift [hold] | Temporary Relax |  |
| Ctrl + Shift + drag a menu item to the shelf | Add a sculpting tool to the shelf |  |
| f | Frame the mesh area under the cursor |  |
| Alt + drag (with Tumble pivot options on) | Tumble around the last stroke |  |
| Ctrl + RMB or Shift + RMB | Sculpting Tools marking menu (a sculpting tool must be active) |  |
| Ctrl + 1 … Ctrl + 9, Ctrl + 0 | Sculpt, Smooth, Relax, Grab, Pinch, Flatten, Foamy, Spray, Repeat, Freeze |  |

### Painting: Artisan, Paint Effects, weights
Source: Paint operation hotkeys; Use Artisan hotkeys
Paint Effects panel key 8 appeared only in the 2014 list (first pass, †); it is not in the 2026 docs.

| Shortcut | Action | Notes |
|---|---|---|
| Alt + f | Flood with the current value | Paint operation hotkeys; Use Artisan hotkeys |
| Alt + a | Show Wireframe on/off |  |
| Alt + c | Color Feedback on/off |  |
| Alt + r | Reflection on/off |  |
| u + LMB | Artisan Paint Operation marking menu | also Use Artisan marking menus |
| b + drag | Upper brush radius (Blue Pencil: stroke size) |  |
| Shift + b + drag | Lower brush radius |  |
| m + drag | Maximum displacement (Sculpt Surfaces/Polygons) or Paint Effects Surface Offset (Blue Pencil: opacity) |  |
| n + drag | Paint value |  |
| / [hold] | Pick colour / set / attribute value |  |
| o + LMB / o + MMB | Poly Brush / Poly UV Tool marking menus |  |
| b / B / m + drag, release | Paint Effects brush size, lower radius, surface offset | Prepare to use Paint Effects |
| Alt + c | Color Feedback when painting jiggle / cluster / skin weights | Paint jiggle deformer weights |

### XGen interactive grooming
Source: XGen interactive grooming tool hotkeys

| Shortcut | Action | Notes |
|---|---|---|
| B + drag or middle mouse button (MMB)-drag left/right | Adjust brush size | The tool cursor resizes larger and smaller as you drag. |
| B + MMB-drag left/right or Ctrl + MMB-drag left/right | Adjust brush size from 0 | The tool cursor resizes larger and smaller as you drag. |
| M + drag or MMB-drag up/down | Adjust brush strength | The brush strength indicator lengthens or shortens as you drag. |
| M + MMB-drag up/down or Ctrl + MMB-drag up/down | Adjust brush strength from 0 | The brush strength indicator lengthens or shortens as you drag. |
| Ctrl + Shift + I | Invert frozen | Reverses the frozen and unfrozen CVs and hairs. Frozen areas display in blue. |
| Ctrl | Decrease hair density | The Density brush's Paint Operation switches from increasing to decreasing hair density. |
| Ctrl | Remove a placed hair | The Place brush removes the hairs it added. |
| Ctrl | Reduce hair length | The Length brush decreases the hair length by the set Increment value. |
| Shift | Smooth hair while lengthening | The Length brush's Operation switches from Scale to Smooth. |
| Ctrl | Reduce hair width | The width brush decreases the hair width by the set Increment value. |
| Ctrl | Unfreeze frozen hairs | When using the Freeze brush, the strokes unfreeze previously frozen hair CVs. |
| Shift | Change how the Freeze brush applies freezing | Switches between freezing and smoothing operations when using the Freeze brush. |
| Ctrl | Deselect hairs | Switches from selecting hairs to deselecting them when using the Select brush. |
| N | Switch the tool's Selection Mode | If the current tool has a Select Mode setting, the tool toggles between Floating and Locked Selection Mode. |
| N | Switch the tool's Brush Mode | If the current tool has a Brush Mode setting, the tool toggles between Global and Local Brush Mode. |
| N | Switch the Density brush's Paint Operation | Switches between the Density brush's Paint Operation settings, such as Set and Smooth. |
| N | Switch to a different Falloff Type | Toggles between the Screen and Volume Falloff Type when using the Comb and Grab brushes. |
| N | Switch to a different Cut mode | Toggles between the Screen and Volume Cut mode when using the Cut brush. |
| N | Change the way hairs get parted | Toggles between the Along Stroke and Away from Center modes when using the Part brush. |
| N | Change how the Select brush selects hairs | Switches between the Screen, Volume and Surface selection types when using the Select brush. |
| Ctrl + 1 | Switch to Density brush | Activates the Density brush. (Another interactive grooming tool must already be selected.) |
| Ctrl + 2 | Switch to Comb brush | Activates the Comb brush. (Another interactive grooming tool must already be selected.) |
| Ctrl + 3 | Switch to Grab brush | Activates the Grab brush. (Another interactive grooming tool must already be selected.) |
| Ctrl + 5 | Switch to Twist brush | Activates the Twist brush. (Another interactive grooming tool must already be selected.) |
| Ctrl + 6 | Switch to Smooth brush | Activates the Smooth brush. (Another interactive grooming tool must already be selected.) |
| Ctrl + 7 | Switch to Noise brush | Activates the Noise brush. (Another interactive grooming tool must already be selected.) |
| Ctrl + 8 | Switch to Clump brush | Activates the Clump brush. (Another interactive grooming tool must already be selected.) |
| Ctrl + 9 | Switch to Part brush | Activates the Part brush. (Another interactive grooming tool must already be selected.) |
| Ctrl + 0 | Switch to Freeze brush | Activates the Freeze brush. (Another interactive grooming tool must already be selected.) |
| Shift + Ctrl [hold] while grooming | Toggle (common brush setting, see page) | Interactive grooming common brush settings |
| Shift + MMB | Density / Length / Width brush: secondary adjustment | Density and Place / Length and Width Brush Settings |

### Outliner
Source: Outliner pages

| Shortcut | Action | Notes |
|---|---|---|
| Alt + MMB drag | Pan | Outliner; Interface hotkeys |
| Ctrl + Alt + MMB drag | Fast pan |  |
| Shift + click / Ctrl + click | Add to selection / toggle |  |
| Shift + click +/- | Expand / collapse all levels |  |
| MMB drag onto a node | Parent |  |
| p / Shift + p | Parent / unparent |  |
| f | Find the node of the object selected in the view | Outliner; USD data in the Outliner |
| Enter | Rename the selected node |  |
| h | Hide / show the node in view panels |  |
| Ctrl + h | Hide / unhide a USD prim in the viewport | USD contextual menu in the Outliner |
| Ctrl + c / Ctrl + v / Ctrl + x / Ctrl + g | Copy / paste / cut / group USD prims | Work with prims in the Outliner |

### Script Editor and Expression Editor
Source: Script Editor pages
The Script Editor page says Undo, Redo, Cut, Copy, Paste and Select All have "their associated hotkeys" but does not list them.

| Shortcut | Action | Notes |
|---|---|---|
| Ctrl + t | New tab | Script Editor menus and hotkeys |
| Ctrl + Tab / Ctrl + Shift + Tab | Next / previous tab |  |
| Ctrl + w | Delete tab |  |
| Ctrl + Space | Show command / object path completion (when Tooltip Help is off) |  |
| Num Enter | Execute |  |
| Ctrl + c / Ctrl + x / Ctrl + v | Expression Editor: copy / cut / paste (Cmd on macOS) | Edit text in an animation expression |
| Ctrl + a | Expression Editor: select all (Windows) |  |
| Ctrl + k / Ctrl + d / Ctrl + a / Ctrl + e | Expression Editor (Linux only): delete to end of line / delete next char / line start / line end |  |

### Render View
Source: Rendering hotkeys; Render View toolbar

| Shortcut | Action | Notes |
|---|---|---|
| Ctrl + Left / Ctrl + Right | Render View: next / previous image (as written in the docs) | Rendering hotkeys |
| Ctrl + p | Color Chooser (modal) | Rendering hotkeys |
| Ctrl + - / Ctrl + = | Exposure: decrease / increase (fine) | Render View toolbar |
| Ctrl + Alt + - / Ctrl + Alt + = | Exposure: decrease / increase (coarse) |  |
| Ctrl + ; / Ctrl + ' | Gamma: decrease / increase (fine) |  |
| Ctrl + Alt + ; / Ctrl + Alt + ' | Gamma: decrease / increase (coarse) |  |
| Ctrl + MMB drag in a numeric box | Drag the value |  |
| Alt + MMB / Alt + RMB | Track / zoom (same as other view panels) | Render a single frame |

### FCheck (legacy image viewer; Windows/Linux only since Maya 2020)
Source: Display keys / Image adjustment keys / Animation playback control keys / Save images in FCheck.

| Shortcut | Action | Notes |
|---|---|---|
| a / r / g / b | Display alpha / red / green / blue channel | Display keys |
| c | Display RGB combined |  |
| f | Single / double buffer |  |
| k | Kodak Cineon correction |  |
| m | Display mask |  |
| p | Print luminance, gamma, saturation |  |
| x | Display the negative |  |
| (modifier shown as image) + x | Reverse the mask | key image not readable |
| z | Z-depth in grey levels |  |
| (modifier shown as image) + z | Logarithm of Z-depth | key image not readable |
| F5 | Cross-hair cursor / tracking |  |
| F6 | Display all tracking points |  |
| (modifier shown as image) + F6 | Write a composer curve | key image not readable |
| F8 | Luminance curve on/off |  |
| F12 | Image tile borders |  |
| Num0 / Num. | Zoom in / out |  |
| Num1–Num9 | Scroll the image (Shift+Alt+number: faster) |  |
| d | Reset luminance, gamma, saturation | Image adjustment keys |
| i / n | Inverted bump / normal bump |  |
| l / Shift + l | Luminance / toggle lines and points |  |
| u | Update / reload image |  |
| w / Shift + w | Save image / save entire animation | also Save images or sequences from FCheck |
| F11 | Allow overwriting images |  |
| = / Shift + = / Alt + = | Luminance +1% / +10% / +50% |  |
| - / Shift + - / Alt + - | Luminance −1% / −10% / −50% |  |
| Ctrl + = or Ctrl + - | Restore luminance |  |
| ] / Shift + ] / Alt + ] | Gamma +1% / +10% / +50% |  |
| [ / Shift + [ / Alt + [ | Gamma −1% / −10% / −50% |  |
| Ctrl + ] or Ctrl + [ | Restore gamma |  |
| / / Shift + / / Alt + / | Offset +1% / +10% / +50% |  |
| \ / Shift + \ / Alt + \ | Offset −1% / −10% / −50% |  |
| Ctrl + \ or Ctrl + / | Restore offset |  |
| ' / Shift + ' / Alt + ' | Saturation +1% / +10% / +50% | docs print a typographic quote |
| ; / Shift + ; / Alt + ; | Saturation −1% / −10% / −50% |  |
| Ctrl + ' or Ctrl + ; | Restore saturation |  |
| F1 / F2 / F3 / F4 | Red / green / blue / RGB channel control |  |
| Shift + F1 / F2 / F3 | Cyan / magenta / yellow channel control |  |
| Num/ / Num* | Less / more colour in the bump image |  |
| Ctrl + Num/ / Ctrl + Num* | Reset colour to 0 / 100% |  |
| (key shown as image) | Reset all FCheck Info window options | key image not readable |
| , / . | Play backwards / forwards continuously | Animation playback control keys |
| Space | Pause / resume |  |
| Shift + , / Shift + . | Set current frame as start / end |  |
| Alt + , / Alt + . | Play backwards / forwards once |  |
| - / + | Slower / faster playback |  |
| Right / Left | Next / previous frame (paused) |  |
| Ctrl + Right / Ctrl + Left | Last / first frame |  |
| s | Swing (forwards and backwards) |  |
| t | Real-time playback (skip frames) |  |

### Marking menus: how to open them
Source: Marking Menus page and editor marking-menu pages

| Shortcut | Action | Notes |
|---|---|---|
| RMB on an object | Object / component-mode marking menu | Marking Menus |
| Shift + RMB | Polygon tools / component-specific / UV / UV shell / NURBS curve marking menus (context-dependent); Create Polygon menu with nothing selected |  |
| Ctrl + RMB | Convert Selection marking menu |  |
| Ctrl + Shift + RMB | Transform-tool settings marking menu (also Quad Draw, Multi-Cut, Joint Tool, In-View Editor) | Marking Menus; Joint Tool marking menus |
| q / w / e / r + LMB | Select / Move / Rotate / Scale tool marking menus |  |
| a + LMB | Input / Output (history) marking menu |  |
| h + LMB | Menu Set marking menu | Interface hotkeys |
| Shift + s + LMB / MMB | Keyframe / Tangent marking menu | Animation hotkeys |
| u + LMB | Artisan paint operation marking menu |  |
| o + LMB / o + MMB | Poly Brush / Poly UV Tool marking menus |  |
| Shift + RMB or Ctrl + RMB (sculpt tool active) | Sculpting tools marking menu |  |
| Shift + RMB in the Hypergraph | Hypergraph marking menu | Hypergraph marking menu |
| RMB in Hypershade / Node Editor / Script Editor / UV Editor / Profiler | Editor marking menus | respective marking-menu pages |
| Space [hold] | Hotbox | All Maya Hotkeys |

### Blue Pencil
Source: Blue Pencil pages

| Shortcut | Action | Notes |
|---|---|---|
| Ctrl + RMB | Blue Pencil marking menu | Blue Pencil; Blue Pencil Marking menu |
| Ctrl + Shift + RMB | Blue Pencil marking menu (variant wording on the same page) | Blue Pencil Marking menu |
| Shift + drag (Transform mode) | Spin the selected area | Modify drawings with Blue Pencil Transform mode |
| Shift + MMB drag (Transform mode) | Freely resize the selected area |  |
| Shift + click / Shift + drag on the Time Slider | Select / move Blue Pencil frames | Work with Blue Pencil frames |
| b + drag / m + drag | Stroke size / opacity | Paint operation hotkeys |

### Bifrost Graph Editor
Source: Bifrost Graph Editor pages (Bifrost-Common book in the Maya 2026 TOC)

| Shortcut | Action | Notes |
|---|---|---|
| MMB drag, Alt + MMB drag or arrow keys | Pan | Build and modify graphs |
| Alt + RMB drag or wheel | Zoom |  |
| f / a | Frame selected / all |  |
| Shift + click / Ctrl + click / Ctrl + Shift + click | Toggle / deselect / add node |  |
| l | Auto-arrange selected nodes (or the whole graph) |  |
| Tab | Tab menu: add a node | Add a node |
| t | Show node types above names | Add a node |
| Ctrl + c / Ctrl + v | Copy / paste nodes (also between sessions) |  |
| Shift + b | Create a backdrop | Annotate and organize nodes |
| Shift + s | Create a sticky note |  |
| Alt + Shift + drag across wires | Break connections (also removes watchpoints) | Connect and disconnect ports; Diagnose and debug |
| Alt + drag a node onto a wire | Insert the node into the connection | Menu reference |
| Shift + drag / Ctrl + drag / Ctrl + Shift + drag | Value field: 10× / 1/10 / 1/100 speed | Set input values on ports |
| Ctrl + . | Pause / resume graph compilation and execution | Pause graph; Open a scene without running graphs |
| Ctrl + g | Make Compound | Create a compound |

### LookdevX Graph Editor
Source: LookdevX for Maya: Keyboard Shortcuts

| Shortcut | Action | Notes |
|---|---|---|
| Ctrl + c / Ctrl + v / Ctrl + x | Copy / Paste / Cut | LookdevX Keyboard Shortcuts |
| Ctrl + d / Ctrl + Shift + d | Duplicate / Duplicate with Connections |  |
| Tab | Create a node |  |
| Enter | Rename a node |  |
| Del | Delete a node |  |
| t | Show node types |  |
| Shift + x | Clear Solo from all |  |
| Ctrl [hover] | Auto-expand port group |  |
| Ctrl + a | Select all in graph |  |
| f / a | Frame selection / all |  |
| 1 / 2 / 3 | Collapse / partially collapse / expand selected |  |
| Shift + b | Create backdrop |  |
| l | Auto layout selected |  |
| g | Show grid |  |
| v | Toggle node swatch preview |  |

### MASH Placer, Shape Editor, Profiler
Source: MASH, Shape Editor and Profiler pages

| Shortcut | Action | Notes |
|---|---|---|
| m [hold] + drag | Placer: place, rotate and scale a point precisely | Placer |
| Shift + drag / Ctrl + drag | Placer: scale points up / down |  |
| j [hold] + drag | Placer: align points to the stroke |  |
| b + drag / n + drag | Placer: brush size / strength |  |
| Alt + click the circle | Shape Editor: solo a target | Shape Editor |
| Ctrl + g / Alt + d / Ctrl + d | Shape Editor: group / deselect all / duplicate target |  |
| Ctrl + r | Profiler: toggle recording | Profiler |
| Shift + Alt + RMB drag up/down / left/right | Profiler: zoom vertically / horizontally | Profiler; Navigation in the Profiler |
| f / a | Profiler: frame selected / all blocks |  |
| Ctrl + c | Profiler: copy event name and DG node | Interpret your Profiler graph results |

---

## Not found / unverifiable

| App | Editor / table | Status |
|---|---|---|
| 3ds Max | Default Hotkey Maps | Keyboard images only (Main UI, Schematic, Track View, Material Editor/SME, Edit Normals, Unwrap, "retired and changed hotkeys"). Not parsed; the text tables cover the same groups. |
| 3ds Max | Maya interaction-mode keyset | The Hotkey Editor can load a "Maya Default" keyset, but the help only lists nine differing keys (table above). The full Maya-mode set is not documented. |
| 3ds Max | Lock User Interface Toggle, Show Main Toolbar Toggle | Listed in the Main UI table with an empty Hotkey cell. |
| 3ds Max | CAT (Character Animation Toolkit), Motion Mixer, Animation Layers, Max Creation Graph, Arnold for 3ds Max, USD Explorer, Civil View, State Sets | No default keyboard shortcuts found in any page. Only list-selection modifiers (Ctrl/Shift+click) are documented. |
| 3ds Max | Graphite ribbon panels (other than PolyTools Alt+1–5, Alt+Shift+1–4 and Freeform tools above) | The ribbon keys are the Edit Poly / Editable Poly context keys. "Customizing the Ribbon" offers 20 user-assignable panel shortcuts with no defaults. |
| 3ds Max | Rendered Frame Window / Frame Buffer toolbar buttons | Only the zoom/pan mouse controls are documented; no buttons have keys. |
| 3ds Max | Particle Flow tyFlow, other plug-ins | Skipped (not default). |
| 3ds Max | Biped: ~50 actions on the Biped Keyboard Shortcuts page | Listed with no default key. |
| 3ds Max | Unwrap UVW Shortcuts page | Older page; five keys conflict with KST (noted in the table). |
| 3ds Max | Copy/paste posture Alt+C / Alt+V / Alt+B | Keys are given without saying which is Copy Posture, Paste Posture or Paste Posture Opposite. |
| Maya | Arnold RenderView | Not in the Maya 2026 help TOC (Arnold docs are a separate site). Not checked. |
| Maya | nCloth, nHair, Fluids, Bifrost legacy | No editor-specific default keys documented; pages only mention display keys 4/5/6. |
| Maya | Trax Editor | Only "f" (frame time warp curve) is documented. |
| Maya | Paint Effects panel | Key 8 is only in the 2014 list (†, first pass). Not in 2026/2027. |
| Maya | z / Shift + z undo / redo | In the 2014 list only (†, first pass). 2026/2027 give Ctrl + z / Ctrl + y globally; z / Shift + z exist only inside the Multi-Cut Tool. |
| Maya | Script Editor Undo/Redo/Cut/Copy/Paste/Select All | The page says they have hotkeys but does not list them. |
| Maya | FCheck rows with image keys | Three modifier keys and one key are drawn as images; the text does not say which keys they are. |
| Maya | Mac-specific hotkeys | "Hotkeys in Maya for MacOS" and "Interface preferences" give Command/Option mappings; not repeated here beyond the legend. |
| Maya | Hypergraph, ShaderFX, Profiler, Script Editor, UV Editor marking menus | Documented menu contents, no extra keys beyond the RMB / Shift+RMB invocations listed. |
| Both | www.autodesk.com/shortcuts/maya, Autodesk shortcut PDFs | Not used (403 in the first pass). Everything comes from the help. |

