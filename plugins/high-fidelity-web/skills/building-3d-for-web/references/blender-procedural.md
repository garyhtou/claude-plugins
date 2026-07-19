# Procedural modeling in Blender, headless (`bpy`)

Building via `blender --background --python build.py` (or the pip `bpy` module) is
ideal for hard-surface hardware: parametric, reproducible, diff-able, version-
controlled, and you fix a proportion by changing a number. See the runnable
[`build_scaffold.py`](../assets/build_scaffold.py) for the helper library and the
correct pipeline. This file is the gotcha catalog. (Verified 2026; re-check exact
numbers against your Blender version.)

## Headless `bpy` gotchas

- **`shade_auto_smooth` / `shade_smooth_by_angle` silently no-op in `--background`**
  (bug #117399, unfixed through 5.0-alpha). They now add a "Smooth by Angle" geometry-
  nodes modifier sourced from the bundled ESSENTIALS asset library, which loads
  asynchronously; headless, the operator fires before assets are ready and you get an
  empty node group (silent no-op). Works in GUI, fails headless.
  **Fix:** don't use the operator. Flat-shade boxes (a Bevel modifier gives the
  machined chamfer) and use plain `mesh.shade_smooth()` only for round primitives. If
  you truly need angle-based smoothing, write the `"sharp_edge"` boolean attribute
  yourself, or append the node group synchronously via `bpy.data.libraries.load(...)`.
- **`use_auto_smooth` and `auto_smooth_angle` were removed in 4.1.** Any pre-4.1
  snippet ending in `obj.data.use_auto_smooth = True` crashes on 4.1+/5.x. Also gone in
  4.1: `Mesh.create_normals_split` / `calc_normals_split`; `MeshLoop.normal` is now
  read-only (use `normals_split_custom_set`).
- **Operators need an active + selected object and a valid context.** No screen/area
  exists headless, so context-dependent operators fail `poll()` with `RuntimeError`.
  Set `view_layer.objects.active = o` and `o.select_set(True)`, or use
  `with bpy.context.temp_override(active_object=o, selected_objects=[o]): ...`.
  (The old dict-as-first-arg override is **deprecated since 3.2**, not removed, but
  prefer `temp_override`.)
- **Prefer the data API / `bmesh` over `bpy.ops` headless.** `o.modifiers.new(...)`,
  `mesh.polygons.foreach_set(...)`, `bmesh` mutate data deterministically with no hidden
  UI state; operators "use the context instead" and fail in ways an exception would not.
- **`Material.use_nodes` is a no-op in 5.0** (always returns True; removal planned 6.0).
  `if not mat.use_nodes:` gating branches are dead code on 5.0+.
- **5.0 breaking changes** that bite old scripts: dict access to engine props
  (`scene['cycles']`) removed (use `bl_system_properties_get()`); File Output node
  `file_slots[].path` → `file_output_items[].name`; legacy Action API removed.

**Verify the API in YOUR version, don't trust training data.** A 10-line probe
(`print([i.name for i in bsdf.inputs])`, list operators, check attrs) saves hours.

## Modifiers + the join-drops-modifiers trap

The pipeline is **build → apply modifiers → join → export**, in that order.

- **`bpy.ops.object.join()` keeps ONLY the active object's modifiers** and drops every
  other object's. Your foil Displace and all bevels vanish at join time, and
  `export_apply` can't recover them (the loss is pre-export). **Apply every modifier on
  every object before joining.** Joining collapses N logical objects into one primitive
  per material, a real draw-call win, but only if modifiers are baked first.
- After a destructive op (join/delete), all Python handles to consumed objects are
  **dead**: touching them throws `ReferenceError: StructRNA ... has been removed`.
- **Apply object SCALE before Bevel/Solidify** (`transform_apply(scale=True)`).
  Object-mode scale isn't in mesh data, so non-uniform scale warps bevel width and
  solidify thickness. The `box()` helper applies scale on creation.

**Modifier stack order** (top→bottom) and why:
`Mirror → Array → Boolean → Solidify → Bevel → Subdivision → Weighted Normal`.
Mirror/Array before Bevel (bevel the full geometry); Boolean before Subdivision (cut
first, smooth after); **Weighted Normal LAST** (it reads the final geometry's faces).

**Applying headlessly:** `bpy.ops.object.modifier_apply(modifier=name)` (needs active
object + OBJECT mode), or the depsgraph route exporters use: `eval =
obj.evaluated_get(bpy.context.evaluated_depsgraph_get()); me = eval.to_mesh()`. For
glTF you often skip manual apply: `export_scene.gltf(..., export_apply=True)` bakes
the stack on export. Apply manually only when you need to edit/join the baked result.

## The "machined, not toy" modifier recipe

(See [`realism.md`](realism.md) for *why*; this is the Blender mechanism.)
- **Bevel modifier** on every box: Limit Method = **Angle** (~30-40°), **1-2 segments**
  for a CNC chamfer (3-4 = softer plastic), **Clamp Overlap** on. Use edge bevel-
  *weights* (Limit Method = Weight) when functionally different same-angle edges should
  bevel differently.
- **Weighted Normal modifier (last), `keep_sharp=True`**: rewrites normals weighted by
  face area so large flat panels stay dead-flat and only the chamfer carries the
  highlight. Bevel + Weighted Normal is *the* machined-metal shading recipe. (In 4.1+,
  custom-normal display needs Shade Smooth active, since Auto Smooth is gone.)

## Reproducible headless runs

- **pip `bpy` pins an EXACT Python** (`Requires-Python == 3.X.*`, no range): 4.0→3.10,
  4.1-4.5/5.0→**3.11**, 5.1→**3.13** (the 3.13 jump is at 5.1, not 5.0). Wrong
  interpreter → "No matching distribution found". Pin with uv/pyenv.
- pip `bpy` always boots `--factory-startup`, no GUI, **add-ons not auto-registered**
  (the glTF exporter ships in-tree, so it works). Prefer it for CI mesh-gen; use the
  full `blender --background` app when you need add-ons, GPU render, or a specific patch.
- **CLI flags:** `--background -b`, `--factory-startup` (keep dev prefs out of CI),
  `--python-exit-code 1` (**without it a Python traceback can still exit 0 and CI passes
  silently**), `-noaudio`. Isolate with `BLENDER_USER_RESOURCES`.
- **Pin the Blender version:** minor versions change exporter behavior. For long-lived
  CI pin an LTS (4.5 LTS → 2027). And note GLB export is **not byte-reproducible**
  (see [`glb-web-pipeline.md`](glb-web-pipeline.md)). Don't gate CI on byte-identical.

## Geometry Nodes from script (and the procedural ceiling)

- Build trees: `bpy.data.node_groups.new("N", 'GeometryNodeTree')`,
  `tree.nodes.new("GeometryNodeXxx")`, `tree.links.new(out, in)`.
- **Interface sockets changed in 4.0:** `node_group.inputs.new()`/`outputs.new()` were
  removed → use `tree.interface.new_socket(name=..., in_out='INPUT', socket_type=
  'NodeSocketFloat')`.
- Assign: `mod = obj.modifiers.new("N","NODES"); mod.node_group = tree`. **Don't
  hardcode input identifiers** like `"Input_2"` (version-dependent, now often
  `"Socket_2"`). Resolve at runtime via `tree.interface.items_tree`.
- For export, **Realize Instances + apply to plain mesh** (universally exportable);
  the exporter's experimental geometry-nodes-instances option needs childless meshes
  under one parent.
- **The ceiling:** GN/scripting excels at systematic parametric hard-surface structure;
  it struggles with bespoke organic forms (creatures, faces, hand-sculpted asymmetry).
  That's Sculpt Mode territory, which is interactive (brush judgment) with no real
  headless path. For hardware, procedural is excellent.

## Do-NOT-trust list (outdated / myth)

- "Tick **Auto Smooth** in mesh data properties": removed in 4.1.
- "Dict-override was **removed** in 4.x": deprecated since 3.2, still works.
- "`material.use_nodes` is a meaningful toggle": no-op in 5.0.
- "`node_group.inputs.new()`": removed in 4.0; use `interface.new_socket()`.
- "bpy 5.0 needs Python 3.13": 5.0 needs 3.11; 3.13 starts at 5.1.
- "`shade_auto_smooth` works headless": silent no-op (#117399).
- "GLB export is byte-reproducible": it is not.
