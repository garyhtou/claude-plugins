# Verifying a 3D model in the browser

A model is only as good as your ability to *see* its flaws. This is the highest-
leverage activity: most rounds are "look from the right angles, find the two worst
tells, fix, rebuild." Build the inspector before you build the model.

## The inspector

Use the standalone [`inspector.html`](../assets/inspector.html) (orbit + scriptable
camera, named views, wireframe, a normals-visualization mode, per-part bounding boxes,
deploy scrubber, pivot-axis markers, node/world-position dump, BVH clip detector). It
loads the GLB in isolation, separate from the app. With an agent browser tool, drive it
via `javascript_tool` (`window.orbit(az, el, dist)`, `setDeploy(t)`, `auditClip()`) and
screenshot via the screenshot tool.

- **Diagnose shading with the normals mode**, not by guessing from the build script. It
  colors each surface by its interpolated normal, so the failure is obvious: hard color
  facets = the part exported flat (the `shade_auto_smooth` headless no-op); a smooth color
  gradient smeared across a panel that should be flat = smooth shading without weighted
  normals (the "putty" look). The fix for the gradient is a Weighted Normal modifier.

- **Use a precise orbit helper, don't fight library cameras.** OrbitControls' `update()`
  overwrites a manual `lookAt` every frame. Set `controls.target` + a camera position on
  a sphere around it (`window.orbit`), so damping never undoes your framing.
- **Query geometry numerically, not just visually.** A quick `Box3` dump of a wheel
  revealed its axle ran along Z (0.86 wide in X, 0.46 in Z). That's how we found the app
  was spinning wheels on the wrong axis. Numbers settle "which axis" faster than eyes.
- **Coordinate conversion is a constant footgun** (Blender Z-up → glTF/three Y-up;
  Blender +Y → three −Z). Don't solve it analytically under pressure. Verify the axis
  empirically in the inspector and set the app to match. See
  [`glb-web-pipeline.md`](glb-web-pipeline.md).

## Different lenses catch different defects

Review the same screenshots through distinct lenses; each finds a different class of
problem:
- **Proportion**: toy slab on huge wheels vs grounded reference ratios.
- **Mechanical plausibility**: does the hinge/mount/linkage make sense?
- **Clipping/intersection**: parts passing through each other (use the clip detector).
- **Material**: enough contrast (metal/painted/anodized/gold) in close proximity?
- **Brand/art-direction**: does it match the intended hardware identity?

## Ingesting a user's screen recording

When the user sends a `.mov` of a bug (e.g. a clip you can't reproduce), extract frames:
```bash
ffmpeg -i clip.mov -vf "fps=5,scale=640:-1" f%03d.jpg     # frames
ffmpeg -i f%03d.jpg -vf "tile=4x5" contact.jpg            # one contact sheet to scan
```
Read the contact sheet to find the moment, then read the key frames full-res. Two
gotchas: (1) macOS names recordings with a **narrow no-break space (U+202F)** before
"PM", so a hand-typed path fails: reference it with a glob (`~/Desktop/*.mov`); (2)
reading a file outside the working directory (like `~/Desktop`) may require the user to
grant access or approve it (it's the user's own file they asked you to read). A single frame pins the exact defect
that an abstract description can't.

## Web-app integration gotchas (cost real time)

- **R3F `<Canvas>` can measure 300×150 (black) until a `resize` event** in headless/
  automation contexts (its ResizeObserver doesn't fire on mount). A defensive post-mount
  `dispatchEvent(new Event('resize'))` is cheap insurance.
- **Scroll-driven sections must align with the scroll library's offset.** drei
  `<ScrollControls>` centers section *i* at `i/(N−1)`. Add a section without re-spacing
  the ranges/keyframes and a section's content shows while the store thinks you're in the
  next one.
- **Lenis / drei smooth scroll ignores programmatic `scrollTop`** and may snap back:
  drive it with real wheel events, and expect a settle/damp delay before `offset` and
  dependent state update.
- **Driving a fold from scroll** is just mapping scroll progress to each joint's `t`. The
  model side is the rig contract (`node, axis, foldRadians`); only the progress source
  differs. With drei: in `useFrame`, read `scroll.offset` (or a section-local 0→1), clamp
  it, and set `node.rotation[axis] = THREE.MathUtils.lerp(from, 0, t)` per joint. With
  GSAP ScrollTrigger: a `scrub`-linked timeline writing the same rotations. Spinners
  (rotors/wheels) ignore scroll: they add `rate * dt` every frame regardless.
- **A fake timed loader that fades via CSS** can look "stuck" to a DOM probe (the element
  persists at opacity 0): check the class, not just presence.

## Process

- **Look first, model second.** Diagnosis (right angles) is most of the work, not
  modeling.
- **Make the loop tight:** one command to build → compress, a hot inspector, scriptable
  camera + scrub. Slow loops kill quality because you stop looking.
- **Decide the product story up front for coherence.** The rover originally had both big
  solar wings *and* a nuclear RTG (contradictory); picking one (solar) made it credible
  and kept the copy honest.
