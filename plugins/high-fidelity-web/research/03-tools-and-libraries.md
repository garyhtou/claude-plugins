# Tools & Libraries Landscape (High-Fidelity Interactive Web)

Research doc #3 for the high-fidelity web skill. This is the opinionated "when to
use what" map of the animation/3D/web tooling landscape.

- **Researched / verified:** 2026-06-19 (facts are fast-moving; re-verify bundle
  sizes, star counts, and versions near any future publish date).
- **House lingua franca:** vanilla JS + GSAP + Tailwind (portable to Rails,
  Astro, plain HTML), escalating to React/Next + Motion (Framer Motion lineage) /
  Three.js / React Three Fiber (R3F) when a project justifies the weight.
- **Bundle sizes** are min+gzip unless stated; treat as orders of magnitude, not
  contract values. Sizes pulled from Bundlephobia's size API where its HTML pages
  403'd.

> **The single biggest 2025 change: GSAP is now 100% free, all plugins
> included.** See the GSAP section below. This removes the old paid-plugin
> licensing friction and is why GSAP is the confident default of the house stack.

---

## 0. TL;DR for the impatient

- **Vanilla / Rails / Astro house stack:** Tailwind v4 (static styling) + GSAP
  (animation, free incl. ScrollTrigger/SplitText/Flip) + Lenis (smooth scroll,
  wired to GSAP ticker) + SplitText for text + native CSS / View Transitions
  where they suffice. Add Three.js or OGL only when the brief needs real 3D.
- **React / Next stack:** keep Tailwind + GSAP (via `@gsap/react` `useGSAP`) for
  scroll/timeline choreography, add Motion (`motion/react`) for declarative
  component, layout, exit, and gesture animation, shadcn/ui for accessible
  primitives, R3F + drei when 3D is React-embedded, next/font + next/image for
  fonts/images.
- **Reach-for-it cheat sheet and accessibility/perf budgets** are in sections 9
  and 10.

---

## 1. Animation engines

### 1.0 Comparison table

| Engine | What it is | Size (min+gzip) | License | Best fit | Maturity (mid-2026) |
|---|---|---|---|---|---|
| **GSAP** | Pro timeline + plugin toolkit | ~27 KB core; +~7 KB ScrollTrigger | GreenSock "No Charge" (free, not OSS) | Vanilla + React (`@gsap/react`) | v3.15, very active (Webflow team) |
| **Motion** (ex Framer Motion) | Hybrid React + vanilla engine on WAAPI | mini ~2.3 KB; full vanilla ~18 KB; `framer-motion` React ~59 KB | MIT (+ optional paid Motion+) | React-first; also vanilla + Vue | v12.40, dominant by usage |
| **anime.js v4** | Lightweight vanilla-first ESM engine | ~38 KB full barrel; far less tree-shaken | MIT | Vanilla-first (no official React adapter) | v4.4.x, active again |
| **WAAPI** | Native `element.animate()` | 0 (native) | Free (native) | Any (raw JS) | Baseline ~96% |
| **CSS + scroll-driven** | `@keyframes` + `animation-timeline` | 0 (native) | Free (native) | Any | Classic CSS universal; scroll-driven NOT Baseline (no Firefox stable) |
| **Theatre.js** | Visual GUI motion editor + runtime | ~31 KB core (studio not shipped) | Apache-2.0 core / AGPL studio | Vanilla, Three.js, R3F | v0.7.2, public dev quiet since 2024 |
| **Velocity.js** | jQuery-era tweening engine | ~15 KB | MIT | Legacy only | Last release 2018. Dead |

### 1.1 GSAP (GreenSock Animation Platform): the powerhouse, now free

**For:** the professional, battle-tested toolkit for complex, timeline-orchestrated
motion. Sequencing many tweens with labels, relative offsets, and staggers, plus a
deep plugin suite: ScrollTrigger (scroll pinning/scrubbing/callbacks), SplitText
(text into lines/words/chars), MorphSVG, DrawSVG, Flip (FLIP layout animation),
Draggable, Observer (unified pointer/scroll/touch), ScrollSmoother, physics.

**Licensing (the headline, verified 2026-06-19).** Webflow acquired GreenSock
(announced 2024-10-15), and GSAP became **100% free for everyone including
commercial use** with the **3.13 release on 2025-04-29**. Every formerly-paid Club
plugin is now in the public npm package and GitHub repo. To directly answer the
brief: ScrollTrigger, Flip, SplitText, Draggable, Observer, and MorphSVG are all
fully free. Confirmed at gsap.com/pricing: "GSAP is now 100% free for all users,
thanks to Webflow's support" and webflow.com/blog/gsap-becomes-free.

**Nuance: free is not the same as open source.** GSAP uses the "Standard 'No
Charge' GreenSock License," not MIT. You may use it freely on any commercial
site/app, but you may not decompile it or use it to build a competing no-code
**visual animation builder** that rivals Webflow (gsap.com/community/standard-license,
verified 2026-06-19). For ordinary product/marketing work this is a non-issue.
Flag it only if the use case is literally "a tool that lets end users build
animations through a visual interface."

**Bundle.** Core ~27 KB gzip (~69 KB min UMD, v3.15). You register only the
plugins you import: ScrollTrigger is the heaviest common one (~7 KB gzip), so a
typical core + ScrollTrigger setup is roughly 30 to 34 KB gzip.

**Framework fit.** Framework-agnostic by design (vanilla, Vue, Angular, Svelte,
Rails-rendered HTML, anything). For React the official `@gsap/react` package
(~0.5 KB gzip) provides the **`useGSAP()`** hook: a drop-in replacement for
`useEffect`/`useLayoutEffect` that auto-reverts every GSAP animation,
ScrollTrigger, Draggable, and SplitText on unmount (critical for React 18 strict
mode double-invocation), supports a `scope` for selector scoping, and
`contextSafe()` for animations created in event handlers. So GSAP is excellent in
vanilla and clean (but imperative) in React: you animate refs rather than express
animation declaratively the way Motion does.

**When to reach for it.** Default of the house stack. Reach for GSAP when you need
the deepest timeline orchestration, scroll pinning/snapping/scrubbing with
callbacks, SVG morphing or text splitting, physics/inertia, FLIP layout
transitions, or guaranteed cross-browser polish on elaborate motion. As of 2025
the cost objection is gone. Reach elsewhere for the smallest possible bundle
(Motion mini, WAAPI), the idiomatic React declarative model (Motion), or pure
native zero-dependency motion (CSS/WAAPI).

### 1.2 Motion (formerly Framer Motion): the React default

**For:** declarative animation in React, plus a small vanilla engine. One npm
package, `motion`, with two surfaces: the framework-agnostic engine at the package
root (`import { animate } from "motion"`, built on WAAPI) and the React API at
`motion/react` (`motion.div`, `AnimatePresence`, layout animations, gestures,
hooks). The React surface is the code that used to be the `framer-motion` package.

**Rebrand.** Framer Motion spun out as the independent open-source project
**Motion in November 2024** at motion.dev. The old `framer-motion` package is
superseded by `motion`; migrating React code is largely a find-and-replace of the
import path. Vue support followed via a separate `motion-v` package (2025).

**Bundle sizes.** The hardware-accelerated `animate` function comes in two flavors
by import path: **mini** (`motion/mini`) ~2.3 to 2.6 KB, animating HTML/SVG via
native WAAPI, and **hybrid/full** (`motion`) ~18 KB, adding independent
transforms, CSS variables, SVG paths, sequences, color/string interpolation, and
WebGL. The React `motion` component surface is heavier (`framer-motion` v12 ~59 KB
gzip full); trim it with `LazyMotion` and the `m` component to under ~5 KB
initial.

**Licensing.** Core is **MIT** and free. **Motion+** is an optional one-time
payment for lifetime updates: premium components (Ticker, Carousel, Cursor,
Typewriter, ScrambleText), an AI kit, tutorials, a visual transition editor, and a
private Discord (confirm price at motion.dev/plus). A separate Motion+ Team annual
per-seat plan exists for teams of 5+.

**Framework fit.** React is first-class and the most mature surface. Vanilla JS is
first-class as of the rebrand. Vue via `motion-v`. The React API uniquely offers
declarative layout animations (`layout` prop), `AnimatePresence` exit animations,
and lifecycle-tied gesture/spring animations.

**When to reach for it.** Default in **React** for component, layout, exit,
gesture, and spring animation. Also reach for the ~2.3 KB vanilla mini when you
want a tiny tree-shakeable hardware-accelerated `animate`. Prefer GSAP for the
deepest timeline/scroll/plugin work; prefer anime.js for lightweight vanilla
outside React. Common real-world pairing: GSAP for scroll choreography + Motion
for component/UI state animation in the same React app.

### 1.3 anime.js v4: the lean free vanilla option

**For:** a lightweight, dependency-free, vanilla-first engine for DOM, CSS, SVG,
and plain JS objects, with built-in timelines, staggering, and (in v4) draggable
and scroll modules.

**v4 rewrite.** v4.0.0 (2024-04-03) was a complete modular, ESM-first rewrite. The
global `anime` object is gone, replaced by named exports
(`import { animate, createTimeline, stagger, svg, utils } from "animejs"`) with
`sideEffects: false` for aggressive tree-shaking. Note the relevant history:
anime.js was effectively unmaintained after v3 (2019), then the original author
returned and drove v4 with a steady cadence since, so the old "is it abandoned?"
concern no longer holds (~70k stars, v4.4.x in 2026).

**Bundle.** Full barrel ~38 KB gzip (worst case, everything imported); a focused
`animate` + a couple utilities ships far less. MIT, no paid tier.

**Framework fit.** Vanilla-first, **no official React adapter** (call `animate()`
inside `useEffect` against a ref). Great for vanilla, Astro, Svelte, web
components; not the idiomatic choice for declarative React.

**When vs GSAP.** anime.js when you want a free MIT lightweight modern-ESM vanilla
engine for the large majority of "animate these elements/SVGs/numbers on a
timeline" needs without a plugin ecosystem. GSAP when you need its powerful
sequencing and plugins (ScrollTrigger, MorphSVG, SplitText, Flip, inertia) and max
polish. Mental model: anime.js is the lean alternative, GSAP is the powerhouse.
Since GSAP is now also free, GSAP often wins on capability unless you specifically
want anime.js's smaller surface and true OSI license.

### 1.4 Web Animations API (WAAPI): the native baseline

**For:** native JS-controlled animation, no library. `Element.animate(keyframes,
options)` returns an `Animation` you can play/pause/reverse/cancel/finish, seek via
`currentTime`, retime via `playbackRate`, and await via the `finished` promise.

**Support:** Baseline widely available (~96%): Chrome/Edge 84+, Firefox 75+,
Safari 13.1+. Treat as universal.

**Can do:** multi-step keyframes with per-keyframe offset/easing, full timing
model (duration/delay/iterations including Infinity/direction/fill), imperative
playback, composite ops, off-main-thread transform/opacity.
**Can't do:** no built-in timeline sequencing/labels/staggers (you chain
`finished` yourself), no SVG morphing, no spring/bounce easings beyond
`cubic-bezier()`/`steps()`, no native scroll trigger (that comes from the separate
ScrollTimeline/ViewTimeline you attach to `Animation.timeline`).

**When to reach for it.** Imperative JS control (play/pause/reverse/scrub, react to
events, await completion) for one or a few elements with standard properties, zero
dependency. Reach for a library for complex timelines, morphing, springs, or a
unified scroll abstraction. Note Motion is built on WAAPI, so "WAAPI vs Motion" is
often "raw API vs ergonomic wrapper over the same engine."

### 1.5 CSS animations + scroll-driven CSS

**Classic CSS** (`@keyframes`, `transition`): mature, ~universal, compositor-
accelerated for transform/opacity. Declarative and ideal for hover states,
loaders, looping decorative motion, simple enter/leave. Limitation: little runtime
control and no native scroll linkage. Default when you don't need JS control.

**Scroll-driven CSS** links progress to scroll: `animation-timeline` with
`scroll()` (scroll container) or `view()` (element entering viewport, the one you
want for reveal-on-enter), plus the JS `ScrollTimeline`/`ViewTimeline` you can
assign to a WAAPI `Animation.timeline`. Runs **off the main thread**, zero bundle.

**Support (mid-2026): NOT Baseline (~85%).** Chromium 115+ (2023), Opera, and
**Safari 26** (2025) support it; **Firefox stable still does not** (only behind
`layout.css.scroll-driven-animations.enabled` / Nightly). That single gap keeps it
"Limited availability." Ship behind `@supports (animation-timeline: scroll())`
with a static fallback, or use a polyfill.

**`@starting-style`** (entry transitions, transition from `display: none` with
`transition-behavior: allow-discrete`): Baseline since Aug 2024, broadly safe in
evergreen by mid-2026.
**`interpolate-size` / `calc-size()`** (animate to `height: auto`): NOT Baseline,
Chromium 129+ only. Progressive enhancement; degrades to a snap.

**When native vs GSAP ScrollTrigger.** Native CSS scroll-driven when the effect is
purely a function of scroll position (parallax, progress bars, reveal-on-enter,
sticky transitions), you want off-main-thread smoothness and zero bundle, and a
Firefox-stable fallback is acceptable. GSAP ScrollTrigger when you need identical
behavior in every browser today including Firefox stable, complex pinning/snapping,
scroll-milestone callbacks, or coordination with canvas/WebGL/React state.

### 1.6 Theatre.js: cinematic / designer-in-the-loop

**For:** a motion-design library with a visual GUI editor. Small runtime
(`@theatre/core`) plus an in-browser keyframing UI (`@theatre/studio`). Author
complex sequenced animation visually (After Effects for the web, wired to live
objects), bake to a JSON state file, play back deterministically. Animates
DOM/CSS/SVG/canvas and especially Three.js / R3F (first-class via `@theatre/r3f`).

**Bundle.** `@theatre/core` ~31 KB gzip (what ships); `@theatre/studio` ~232 KB
but authoring-only and tree-shaken out of production.
**Licensing.** Split: `@theatre/core` is Apache-2.0 (you ship it), `@theatre/studio`
is AGPL-3.0-only (dev-time editor, typically not redistributed).
**Maturity (read carefully).** ~12.5k stars, latest npm v0.7.2 (2024-05-19), last
public commit 2024-04-11. The README says development moved to a private repo
toward 1.0, but no public 1.0 has shipped in ~2 years, so public development is
effectively quiet. Stable and usable, but flag the low public-maintenance signal
as a risk and re-verify at decision time.

**When to reach for it.** Complex sequenced cinematic animation (scroll
narratives, product reveals, intros), Three.js / R3F scenes you want to
art-direct visually (camera moves, transforms), or a designer-in-the-loop
workflow. Not for simple UI micro-interactions (use WAAPI/CSS/GSAP).

### 1.7 Velocity.js: legacy, do not use

`velocity-animate` was a popular jQuery-era accelerated tweening engine (~2014 to
2017). **Last stable release 1.5.2 (2018-07-31), last commit 2020.** WAAPI covers
most of what it offered with zero dependency, and GSAP/Motion/anime.js superseded
it. **Do not use for new work in 2026.** Legacy maintenance only; migrate to WAAPI,
GSAP, Motion, or anime.js.

---

## 2. Smooth scroll

### 2.0 Comparison

| Option | Size (min+gzip) | License | Framework fit | Status |
|---|---|---|---|---|
| **Lenis** | ~5 KB (v1.3.x) | MIT | Vanilla-first; `lenis/react`, `lenis/vue`, `lenis/framer` | Actively maintained, de facto default |
| **Locomotive Scroll** | ~8.6 KB (v5, built on Lenis) | MIT | Vanilla-first; community React wrappers | Stable, lighter maintenance |
| **Native CSS** | 0 KB | Free | Any | scroll-snap universal; scroll-driven anim NOT Firefox-stable |

### 2.1 Lenis (darkroom.engineering, formerly Studio Freight)

**For:** lightweight smooth scroll that **wraps** native scroll rather than
replacing it. Because it rides native scroll, `position: sticky`, anchor links, and
accessibility primitives keep working. One instance supports vertical, horizontal,
and nested scroll, and it is explicitly designed to drive synced scroll scenes
(WebGL, GSAP ScrollTrigger, parallax) off a single loop. ~5 KB gzip, MIT, 14k
stars, actively maintained.

**Package rename (common confusion).** `@studio-freight/lenis` is now plain
**`lenis`**, and `@studio-freight/react-lenis` folded into the `lenis/react`
submodule (`<ReactLenis>` + `useLenis`). The old `@studio-freight/*` packages are
deprecated. New code: `npm install lenis`; React from `lenis/react`, Vue from
`lenis/vue`, Framer from `lenis/framer`.

**Canonical GSAP ScrollTrigger wiring** (drive Lenis from GSAP's ticker so both
share one frame loop):

```js
const lenis = new Lenis()
lenis.on('scroll', ScrollTrigger.update)
gsap.ticker.add((time) => { lenis.raf(time * 1000) }) // ticker is seconds, raf wants ms
gsap.ticker.lagSmoothing(0)
```

`lenis.on('scroll', ScrollTrigger.update)` keeps ScrollTrigger synced to Lenis's
virtual position. Driving `lenis.raf` from `gsap.ticker.add` gives one shared loop.
`lagSmoothing(0)` disables GSAP lag compensation, which otherwise fights Lenis's
interpolation. (The older `scrollerProxy` approach exists for custom scroll
containers; the ticker pattern is the current default.)

**Accessibility (document this).** `prefers-reduced-motion` is **not** automatic:
gate the smooth behavior behind a reduced-motion check so opted-out users get
instant native scroll. Keyboard/focus generally keep working because it wraps
native scroll, but test Tab-to-focus scrolling and `#anchor` jumps. Capped to 60fps
on Safari and degraded in low-power mode.

**When to reach for it.** When you need coordinated scroll effects: ScrollTrigger
timelines, WebGL scroll scenes, parallax, or pinning that must stay frame-synced.
Lightest full-featured option. Skip it if CSS scroll-snap or native scroll-driven
animations would do, since any smooth-scroll lib adds accessibility/maintenance
cost for no benefit there.

### 2.2 Locomotive Scroll

**v5 is a rewrite built on top of Lenis** (a thin opinionated wrapper adding
in-viewport detection and a `data-scroll` attribute-driven animation layer). ~8.6
KB gzip, MIT, 8.8k stars, stable but less actively maintained than Lenis (React is
community packages, not official). Use it for the batteries-included declarative
`data-scroll` API when you want scroll-triggered effects without wiring GSAP. If
you already use ScrollTrigger or want the smallest footprint and most control, go
straight to **Lenis** (Locomotive is just Lenis plus a layer you may not need). New
projects increasingly default to Lenis + ScrollTrigger.

### 2.3 Native CSS (the zero-dependency alternative)

**scroll-snap** (`scroll-snap-type`, `scroll-snap-align`): Baseline, safe
everywhere. Use for carousels, full-page section snapping, slide decks. Zero JS.
**Scroll-driven animations:** see 1.5 (not Firefox-stable yet).

**Native is enough when:** section/carousel snapping, or scroll-progress/reveal/
parallax that can degrade gracefully. **You need JS (Lenis) when:** you want the
smoothed/eased scroll motion itself (CSS does not smooth scroll, only animates
along it), orchestrated timelines/pinning/scrubbing via ScrollTrigger, WebGL synced
to scroll, or guaranteed cross-browser behavior including Firefox today. The two
are complementary.

---

## 3. 3D / WebGL

### 3.0 Comparison

| Library | What it is | Size (min+gzip) | License | Framework fit | Maturity |
|---|---|---|---|---|---|
| **Three.js** | The de facto WebGL/WebGPU scene-graph lib | ~178 KB full import (r184) | MIT | Vanilla-first | ~111k stars, monthly releases, very mature |
| **R3F + drei** | React renderer for Three + helpers | R3F thin (~tens KB); weight is Three underneath; drei tree-shakeable | MIT | React only | R3F v9 (React 19), drei v10, mature |
| **OGL** | Minimal WebGL, thin over raw GL | ~33 KB full before tree-shaking | MIT | Vanilla | ~4.5k stars, low-churn, effectively stable |
| **Babylon.js** | Full game engine | ~1.4 MB UMD; far less with ESM tree-shaking | Apache-2.0 | Vanilla-first; React community | ~25k stars, v8, Microsoft-backed |
| **PlayCanvas** | Engine + hosted visual editor | Modular, ~Three order headless | MIT (engine + editor) | Vanilla, React, web components | ~16k stars, strong WebGPU + Gaussian splats |
| **curtains.js** | Shaders on DOM images/video | Lightweight, single-purpose | MIT | Vanilla; React/Vue wrappers | Niche, low activity, verify maintenance |

### 3.1 Three.js: the standard

The default general-purpose 3D library: scene graph over WebGL (increasingly
WebGPU), cameras, lights, materials, geometry, glTF loaders, post-processing. By
far the largest ecosystem (~111k stars vs ~25k Babylon), enormous example corpus,
monthly releases, the lingua franca of web 3D (Spline, R3F, Vanta all sit on it).

**Tree-shaking caveat (the recurring gotcha):** a typical full import is ~178 KB
gzip and Three is **not cleanly tree-shakeable** across all bundlers, so importing
one class can still pull large chunks. Plan for this on conversion-critical landing
pages (lazy-load the 3D, defer below the fold). Vanilla-first, imperative
scene/loop code. **Reach for it** as the default for custom web 3D, especially
when you need full control, the broadest hiring pool, or you are not in React. For
a trivial scene where bytes are paramount, consider OGL.

### 3.2 React Three Fiber (R3F) + drei

Declarative Three.js inside React: R3F is a React **renderer** (like react-dom for
a Three scene graph), you express the scene as JSX and React reconciles it. drei is
the companion helpers (controls, environment, `useGLTF` loaders, text, shaders,
staging). R3F itself is thin; the dominant cost is Three.js underneath, so the
floor is roughly "Three.js + React + R3F glue." drei as a whole is large but
**per-helper tree-shakeable**: import only what you use. R3F v9 targets React 19.

**Use R3F** when the app is already React and the scene has many independent,
stateful pieces that benefit from the component model and hooks. **Use vanilla
Three** when you are not in React, initial load size is critical, or for a simple
static render where R3F's abstraction earns nothing.

### 3.3 OGL: minimal WebGL

Deliberately minimal, thin over raw WebGL (Core/Math/Extras). Tiny (~33 KB gzip
full, far less tree-shaken), so a focused shader effect ships much lighter than
Three. Popular for shader-driven hero sections and creative/award sites. Caveat:
~4.5k stars, no tagged npm releases (consume from main), low ongoing activity,
treat as stable but quiet. **Reach for it** for custom shader work, image/video
effects, or creative coding where you control rendering and bundle size matters and
you don't need a full scene graph/glTF/physics/ecosystem. Otherwise Three.

### 3.4 Babylon.js: full engine

Batteries-included 3D **game engine**: physics, collisions, audio, GUI, animation,
asset pipeline, inspector/editor, WebXR. Far more out of the box than Three, TS-
first, Microsoft-backed, Apache-2.0, ~25k stars, v8, very mature. Heavier floor
(~1.4 MB UMD; tree-shakes down via `@babylonjs/core` ESM). **Choose Babylon** for
games/simulations/configurators/VR-AR or teams that prefer one cohesive engine over
assembling Three plugins. **Choose Three** for max flexibility, smaller simple-scene
bundles, and the bigger community.

### 3.5 PlayCanvas: engine + visual editor

Open-source WebGL2/WebGPU/WebXR engine plus a hosted, real-time collaborative
**visual editor** (game-dev IDE in the browser). Differentiator is the editor and
team collaboration with one-click publish; among the first with full WebGPU
(compute shaders) plus industry-leading 3D Gaussian Splat tooling. Engine + editor
both MIT, ~16k stars. Usable headless via npm, declaratively via `@playcanvas/react`,
or with web components. **Reach for it** when you want a visual editor and team
collaboration for browser games/configurators/interactive 3D, or cutting-edge
WebGPU/splat support. Choose Three/R3F for pure code-first control or embedding 3D
into an existing React codebase.

### 3.6 curtains.js: shaders on DOM media

Narrow use case: turn existing DOM images/videos/canvases into WebGL textured
planes you animate with shaders, positioned/sized via CSS (shader hover effects,
image/video transitions, "WebGL on top of HTML" heroes). Small, single-purpose,
CSS-driven, MIT, React/Vue wrappers. **Status caveat:** niche, low ongoing
activity, verify last commit before adopting. Many teams now do the same DOM-image-
shader effect with OGL or a small Three plane to stay on a more active base.
**Reach for it** specifically when the job is "shaders on DOM images/video with
CSS-driven layout." For anything broader (real scene, models, physics), use
Three/OGL.

### 3.7 No-code / 3D-asset tools

| Tool | What it is | Runtime cost | Pricing | Fit |
|---|---|---|---|---|
| **Spline** | 3D design tool, export to web/React | `@splinetool/react-spline` ~27 KB + `@splinetool/runtime` (Three-based) + scene asset, so real cost is much higher | Free (watermarked); Starter ~$12/mo, Pro ~$20/mo, Enterprise | React component + vanilla runtime |
| **Rive** | Interactive vector + state machines + data binding | Small JS runtime + shared `rive.wasm` (load once) + `.riv` file (10 to 15x smaller than Lottie JSON) | Free tier; paid per-editor seats | `@rive-app/canvas`/`-webgl`/`-lite`, `@rive-app/react-canvas` |
| **Lottie** | After Effects export (Bodymovin) | `lottie-web` ~75 KB gzip; dotLottie players vary; `.json` can be 1 MB+ | Free OSS players; LottieFiles SaaS paid tiers | `lottie-web`, `lottie-react`, dotLottie players |
| **Three.js Journey** | The standard learning course (Bruno Simon) | n/a | ~$95 one-time, lifetime | Teaches vanilla Three + R3F |

**Spline:** designer-authored interactive 3D handed to a React/web app without
hand-writing Three. Best for hero scenes/product showcases; budget for the runtime
weight and lazy-load/defer the embed. Raw Three/R3F instead for full control,
smaller bundles, or data-driven 3D.

**Rive:** interactive vector animation with **state machines** and **data binding**
(properties bound to live data, respond to input/state at runtime). Strong for UI
micro-interactions, animated icons, onboarding. `.riv` files are ~10 to 15x smaller
than equivalent Lottie JSON, and rendering goes through Canvas/WebGL via WASM
(bypassing layout) for better perf. First instance must fetch/init WASM, so
**preload it for above-the-fold** animations. **Rive vs Lottie:** Rive for
interactivity, smaller files, better runtime perf; Lottie for an existing After
Effects workflow, purely decorative animation, or widest platform/tooling
compatibility.

**Lottie:** render After Effects animations exported as JSON via the Bodymovin
plugin. `lottie-web` ~75 KB gzip; the newer **dotLottie** players are WASM-backed,
ship a compressed `.lottie`, and can render on a Web Worker via OffscreenCanvas.
Both player JS and the (possibly 1 MB+) JSON count, so minify/optimize, prefer
`.lottie`, and lazy-load. Players are OSS/free. **Reach for it** when a motion
designer already works in After Effects and the animation is decorative/non-
interactive, or for max cross-platform compatibility. Rive instead for
interactivity, smaller files, or higher runtime perf.

**Three.js Journey (~$95):** the recognized standard paid course for learning
Three.js (Bruno Simon), covering vanilla Three and R3F. Cite it as the learning
resource.

---

## 4. Helpers

### 4.0 Comparison

| Library | Size (min+gzip) | License | Fit | Status |
|---|---|---|---|---|
| **SplitType** | ~4.2 KB | ISC (free) | vanilla (React via ref) | Stale (no release since 2023) |
| **GSAP SplitText** | ~3.6 KB (+core optional) | GreenSock no-charge (free) | vanilla + `@gsap/react` | Very active |
| **Tempus** | ~1.9 KB | MIT | vanilla | Active (prerelease) |
| **matter.js** | ~25 KB | MIT | vanilla (React via ref) | Stagnant but stable |
| **tsParticles** | ~54 KB full; slim ~44 KB; engine ~21 KB | MIT | many official wrappers incl. React | Very active |
| **Vanta.js** | ~2.6 KB loader + heavy engine (three ~178 KB / trimmed ~45 KB) | MIT | vanilla (React via ref) | Stale but stable |
| **atropos** | ~2.5 KB | MIT | vanilla + React + Web Component | Actively maintained |
| **vanilla-tilt** | ~2.6 KB | MIT | vanilla (React via ref) | Mature, quiet |
| **hover-effect** | ~130 KB (bundles three + gsap) | MIT | vanilla | Stale |
| **Embla Carousel** | core ~6.9 KB; React ~7.3 KB | MIT | vanilla, React, Vue, Svelte, Solid | Active |
| **Swiper** | ~20 KB full (tree-shakeable) | MIT | vanilla, `swiper/react`, `swiper/vue`, `swiper/element` | Very active |

### 4.1 SplitType vs GSAP SplitText (text splitting)

**SplitType** wraps each line/word/char in a DOM element so you can animate with
any library. ~4.2 KB gzip, zero deps, animation-agnostic. **License is ISC, not
MIT** (declared only in package.json, no LICENSE file). Does NOT handle masking,
aria, or re-split on resize. **Stale:** no release/commits since late 2023.
Vanilla-first; in React call it in an effect against a ref.

**GSAP SplitText** is GreenSock's splitter (chars/words/lines), **free as of 2025**
(rewrite landed in GSAP 3.13, 2025-04-29). ~3.6 KB plugin (can run without loading
gsap core, so a pure split is ~3.6 KB). Advantages over SplitType: built-in
**masking** (clip wrapper for one-line reveals), **accessibility** (auto
`aria-label` on parent, `aria-hidden` on children so screen readers read the
original text), and **responsive resize** (`autoSplit` re-splits on font load/width
change with an `onSplit()` callback). **License is GreenSock's no-charge license,
not OSI**, but free incl. commercial.

**When which.** SplitType for the smallest possible dep when you only need raw
splitting, you are not on GSAP, and you handle masking/aria/resize yourself.
SplitText when you already use GSAP (marginal ~3.6 KB) or need the production
extras out of the box. Since SplitText became free and is actively maintained while
SplitType is stale, **SplitText is now the stronger default for serious projects.**

### 4.2 Lenis + GSAP wiring and rAF centralization (Tempus)

Lenis + ScrollTrigger wiring is in section 2.1. **Tempus** (darkroom, ~1.9 KB,
MIT) is a centralized requestAnimationFrame loop manager: register callbacks via
`Tempus.add(cb, { priority, fps })` and it runs them all from one rAF loop with
ordering and per-callback FPS throttling. Why it matters: many independent rAF
loops (smooth scroll + WebGL + parallax + marquee + component animations) cause
read-then-write layout thrash, redundant scheduling, and no single place to
throttle or pause on tab-hide. One shared loop fans out in deterministic priority
order, computes `time`/`deltaTime` once, and lets you throttle/pause globally.
Pair with Lenis by registering it in the global loop instead of giving Lenis its
own rAF:

```js
Tempus.add((time) => { lenis.raf(time) }, 0)
```

Use the unscoped `tempus` package (the scoped `@darkroom.engineering/tempus` is
frozen). Note: if you already drive Lenis from GSAP's ticker (section 2.1), that
ticker is itself your centralized loop and you may not need Tempus too. Pick one
shared loop owner.

### 4.3 matter.js (2D physics)

2D rigid-body physics (gravity, collisions, constraints, compound bodies) with a
built-in renderer and runner. The easiest web physics engine to start with: pure
JS, zero deps, ~25 KB gzip, MIT, ~18k stars (most-starred JS 2D physics).
**Stagnant but stable:** no release since 2024-06 but ~405k weekly downloads,
battle-tested. Vanilla-first; React via ref + effect. **Alternatives:** planck.js
(Box2D port, ~46 KB) for Box2D-grade accuracy; Rapier (`@dimforge/rapier2d`, Rust
to WASM+SIMD) for raw performance/determinism at the cost of a WASM artifact and
async init. Rule of thumb: matter.js for ease/small bundle, planck for Box2D
fidelity, Rapier for performance.

### 4.4 tsParticles (particles)

Highly customizable particles, confetti, fireworks, animated backgrounds. Modern
successor to the unmaintained particles.js (frozen at 2015). Modular: full
`tsparticles` ~54 KB, `@tsparticles/slim` ~44 KB, `@tsparticles/engine` ~21 KB,
import only what you need. MIT, ~8.9k stars, very active. Official `@tsparticles/react`
wrapper (thin, the engine holds the weight). **Reach for it** for configurable
particle/confetti/background effects (especially in React). For confetti only,
`canvas-confetti` is lighter.

### 4.5 Vanta.js (WebGL backgrounds)

Drops an animated, mouse-reactive 3D/2D background canvas behind any element. Thin
wrapper (~2.6 KB) that renders nothing itself: each effect (Waves, Birds, Fog,
Net, Globe...) needs a heavy engine you supply (**three.js** for most, **p5.js**
for a couple), and that engine is the real cost (~45 KB trimmed three up to ~180 KB
full three). Vanta declares no dependencies, so **pin a compatible three/p5
version** yourself. **Stale but stable:** last publish 2022, ~28k weekly downloads,
not archived. **Reach for it** when you want a polished mouse-reactive 3D
background fast with near-zero graphics code, a preset is close enough, and the
page can absorb the engine (lazy-load below the fold). Roll your own three for
custom shaders/scenes or if you already ship three. Use plain CSS (gradients,
`@property`, conic/radial, scroll-driven) when the effect can be 2D.

### 4.6 Hover / tilt effects

- **atropos (~2.5 KB, MIT):** 3D parallax tilt-on-hover with layered depth, touch-
  friendly, zero deps, first-class `atropos/react` and `atropos/element` builds,
  most recently maintained. **Best default for 2026.**
- **vanilla-tilt (~2.6 KB, MIT):** smooth 3D tilt on mouse move/device orientation,
  glare and gyroscope options, most-starred. Mature but quiet, vanilla API (React
  via ref). Edge to atropos unless you want its specific glare/orientation features.
- **hover-effect (~130 KB, MIT):** WebGL image displacement "liquid reveal" between
  two images via a displacement map. The only one that does this, but bundles old
  three + gsap and is stale. Reach for it only when you specifically need that
  displacement reveal (cheaper if you already bundle three, watch version
  conflicts).

### 4.7 Embla vs Swiper (carousels)

**Embla** is lightweight, dependency-free, framework-agnostic, **headless/unstyled**:
ships the motion engine (swipe physics, snapping) and a reactive/imperative API but
no UI (you build buttons/dots/styling). Official vanilla/React/Vue/Svelte/Solid
wrappers, official plugins (autoplay, auto-scroll, fade, class-names, accessibility).
core ~6.9 KB, React ~7.3 KB, MIT.

**Swiper** is feature-rich, modular, **batteries-included**: built-in
navigation/pagination/scrollbar, many effects (fade, cube, coverflow, flip, cards,
creative), virtual slides, lazy loading, RTL. Tree-shakeable (~20 KB full). MIT
(stayed MIT, no paid tier). **Correction to a common assumption:** `swiper/react`
and `swiper/vue` are NOT deprecated (verified 2026-06-19, still official and
shipping in v12.x). v9 removed the Angular/Svelte/Solid components and points those
to `swiper/element` (web component), but React/Vue were retained.

**When which.** **Embla** for full control over markup/styling/accessibility, a
minimal bundle (~3x smaller out of the box), and composing your own UI (ideal for
design-system carousels). **Swiper** for a batteries-included slider with built-in
nav/pagination and a large effect catalog out of the box (best when speed-to-ship
and prebuilt features beat bundle size or UI control). For web-component or Angular
use, `swiper/element` is the turnkey option.

---

## 5. Design-to-code / asset tools

Covered above where they sit naturally: **Spline, Rive, Lottie** in section 3.7
(they emit 3D/vector/AE runtime assets); **shadcn/ui** in section 6 (React
component generator). Quick context on the reference **builders**:

- **Framer** (framer.com): no-code/low-code visual website builder. Its animations
  are powered by **Motion** (the same library that is the React escalation target),
  so Framer motion patterns translate cleanly to hand-coded Motion. Freemium ($0,
  ~$10/mo, ~$30/mo, Enterprise). Use for inspiration, rapid client prototypes, or
  quick marketing pages; build by hand for custom GSAP/ScrollTrigger choreography
  or codebase integration.
- **Webflow** (webflow.com): mature visual builder generating real HTML/CSS/JS.
  **Webflow acquired GSAP (announced 2024-10-15) and made it 100% free on
  2025-04-30**, which is the bigger takeaway for a code-first team than building in
  Webflow. Reach for Webflow itself for CMS-driven client deliverables a
  non-developer must maintain.
- **Unicorn Studio** (unicorn.studio): no-code WebGL effects tool (shaders,
  scroll/hover-driven effects, animated backgrounds) output as a code embed.
  Freemium ($0 watermarked, ~$20/mo or ~$168/yr Legend for commercial/unwatermarked).
  Use to prototype/reference a specific shader/WebGL effect you would otherwise
  hand-build in three; build by hand when the effect must be perf-tuned, app-state-
  integrated, or free of an external embed/watermark.

---

## 6. Supporting tooling

### 6.1 Tailwind CSS (and coexisting with GSAP)

**Current: v4.x** (the Rust "Oxide" rewrite, v4.0 shipped 2025-01-22). Headline
changes: **CSS-first config** (`tailwind.config.js` replaced by an `@theme`
directive, design tokens become real CSS custom properties, so you can read and
animate them at runtime), a one-line `@import "tailwindcss";`, and large build
speedups (full builds several x faster, no-op incremental rebuilds in microseconds).
MIT and free; Tailwind Plus is an optional ~$299 one-time license for prebuilt
components/templates. Framework-agnostic, so it carries unchanged from the vanilla
house stack to React/Next. Production CSS is typically single-digit to low-tens of
KB (JIT generates only used classes).

**The key coexistence rule with GSAP/Motion.** Division of labor: **Tailwind owns
the static resting state and structure; GSAP/Motion owns the animation.** The
pitfall: Tailwind `transition`, `transition-*`, and `animate-*` classes **fight**
GSAP/Motion, which animate by writing inline styles. If the same element carries a
Tailwind transition/animate class, the CSS transition competes with per-frame
inline updates, producing stutter or double-easing (Motion's own docs call this
out). So:

- Do **not** put Tailwind `transition*` / `animate-*` classes on any element
  GSAP/Motion animates. Let the JS library be the single source of truth for
  timing and easing.
- Keep Tailwind transitions only for purely CSS-driven interactions JS is not
  touching (a button hover, a menu fade), and never target the same property on
  the same element from both.
- GSAP leaves inline styles after animating; use `clearProps` or `gsap.set()`
  deliberately if you want Tailwind classes to retake control.
- **Arbitrary values** (`w-[347px]`, `translate-x-[12.5%]`, `top-[calc(100%_-_2rem)]`)
  let you hit exact specs and set precise animation start states in markup, so GSAP
  code only describes motion, not geometry. The JIT engine generates these on
  demand, so unused values cost nothing. Caveat: JIT relies on static analysis, so
  avoid fully runtime-dynamic class strings (use literal class names, a safelist,
  or set animated values via inline styles GSAP writes anyway).

### 6.2 shadcn/ui

Not a component library: a CLI (`npx shadcn`) **copies component source into your
repo**, where you own and edit it. Each component is built on the matching Radix UI
primitive (accessible behavior: focus management, ARIA, keyboard nav) and styled
with Tailwind. Supplies the accessible interactive primitives you don't want to
hand-roll (dialogs, dropdowns, popovers, sheets, tooltips, accordions, tabs), and
because you own the source you can drop GSAP/Motion directly in and hook animations
to Radix's `data-state="open"` attributes. **React only** (Radix is React-only; the
Astro path is via React islands). MIT, very mature (~117k stars). **Reach for it**
on a React stack already using Tailwind when you need accessible primitives fast
and want to animate the source. Not for the vanilla baseline, or if you want
Vue/Svelte/Angular.

### 6.3 Fonts

- **Variable fonts** (one file, axes `wght`/`wdth`/`ital`/`slnt`/`opsz` plus custom
  like `GRAD`): declare a range in `@font-face` and drive values with CSS or
  `font-variation-settings`. You can **animate along an axis** (weight, slant,
  grade) in GSAP/Motion instead of cross-fading discrete files. Usually beats
  shipping multiple static cuts as soon as a design uses 2+ weights. Always serve
  WOFF2 and subset (full Inter variable ~330 KB drops to ~75 KB Latin-only). Most
  popular variable fonts (Inter, Roboto Flex, Recursive) are OFL/free. **Default
  for high-fidelity marketing sites.**
- **Fontsource** (`@fontsource/*` static, `@fontsource-variable/*` variable):
  1500+ OSS typefaces self-hosted via npm. Why self-host vs the Google CDN:
  privacy/GDPR (no third-party IP transfer), perf (no extra DNS/TLS), version
  locking, offline/PWA bundling. Free, mature, needs a bundler (Vite/Webpack/Astro).
  **Default for self-hosting on the vanilla/Vite/Astro tier; on Next use next/font.**
- **Loading strategy:** `font-display: swap` for headings/body (FOUT then swap),
  `optional` for decorative, `block` for brand glyphs. **Preload** the one or two
  above-the-fold critical fonts with `<link rel="preload" as="font" type="font/woff2"
  crossorigin>` (crossorigin mandatory even same-origin). The real CLS fix is
  **metric-override descriptors** (`size-adjust`, `ascent-override`,
  `descent-override`, `line-gap-override`) on a local fallback `@font-face` so the
  swap doesn't reflow. Tooling: Capsize / Fontaine (Vite/Webpack plugins) for the
  vanilla tier; **next/font** does all of this automatically inside Next (self-hosts
  Google fonts at build time so the browser sends no request to Google,
  `adjustFontFallback` defaults on for zero-CLS, `display` defaults to `swap`,
  variable fonts first-class, expose a CSS variable and wire into the Tailwind
  theme).

### 6.4 Image / video optimization

**Image decision rules:** AVIF first, WebP fallback, JPEG last via `<picture>`
(AVIF ~50% smaller than JPEG, ~20 to 30% smaller than WebP; encodes slower, so
encode once and cache). The LCP/hero image: `fetchpriority="high"`, eager (never
`lazy`), and do NOT add `decoding="async"` to it (async decode can defer the very
paint you are prioritizing). Below the fold: `loading="lazy"` + `decoding="async"`.
Always set width/height (or `aspect-ratio`) and pair `srcset` (w descriptors) with
`sizes`. Placeholders: **ThumbHash** (under ~100 bytes, supports transparency) for
blur, dominant color for the minimum. The `<picture>` fallback chain requires an
inner `<img>` or non-matching browsers render nothing.

**Tooling:** **sharp** (libvips, Apache-2.0, the fastest mainstream Node library,
~4 to 5x ImageMagick; engine behind Astro's and Next's optimizers) for any build/
server "source to AVIF + WebP + multiple widths + ThumbHash" pipeline (the right
primitive for the vanilla house stack). **Squoosh** (squoosh.app) for manual one-
off compression tuning, but its CLI is unmaintained so don't automate on it.
**next/image** automates format negotiation, responsive srcset, lazy loading, CLS
prevention, blur-up (`placeholder="blur"`); set `priority` on the hero. **Astro
`<Image>`/`<Picture>`** optimize via sharp (`<Picture>` emits a real multi-format
`<picture>`).

**Hero video:** `muted autoplay loop playsinline poster="..."`, WebM (VP9/AV1)
source before MP4 (H.264) fallback. `muted` is mandatory for autoplay, `playsinline`
stops iOS fullscreen, `poster` shows an optimized still immediately and is the
static fallback. Keep under ~4 MB desktop / ~2 MB mobile, 10 to 30s loops, lazy-load
below-the-fold video behind an Intersection Observer. Under
`prefers-reduced-motion: reduce`, do not autoplay: show the poster (see 10.4).

### 6.5 View Transitions API

Native animated transitions between two UI states (the browser captures
before/after snapshots and crossfades or morphs). Two cases: **same-document (SPA)**
via `document.startViewTransition(callback)`, and **cross-document (MPA)** for real
same-origin multi-page navigations with no JS router (the headline for marketing
sites: SPA-feeling page transitions on a static/server-rendered site). Cross-
document opts in via CSS on both pages:

```css
@view-transition { navigation: auto; }
```

Assign `view-transition-name` to an element (hero, heading) so the browser morphs
it between states, then style via `::view-transition-*` pseudo-elements.

**Support (verified 2026-06-19):** same-document is **Baseline newly available**
(since Firefox 144 shipped, ~Oct 2025): Chrome/Edge 111+, Safari 18+, Firefox 144+.
Production-ready. **Cross-document (MPA) is NOT yet Baseline:** Chrome/Edge 126+ and
Safari 18.2+, but **Firefox does not support cross-document yet**. So an MPA
transition will not animate in Firefox today. Same-origin only. **Fallback is built
in:** unsupported browsers just navigate/update with no animation, no polyfill
needed in the general case.

**Framework fit:** **Astro** ships first-class support via `<ClientRouter />`
(formerly `<ViewTransitions />`): drop it in a shared layout for SPA-like animated
MPA transitions, with `transition:*` directives and a `fallback` prop (`animate`
default, `swap`, `none`) that can animate even where the native API is absent
(including Firefox today). **Next.js/React** have an experimental `<ViewTransition>`
(not production-recommended yet).

**When to reach for it:** SPA-like page transitions on an MPA/static/server-rendered
site without a JS router (the vanilla + Tailwind sweet spot), or shared-element
transitions (a persisting hero/logo) that are painful to hand-roll, where degrading
to instant navigation is acceptable. Same-document is safe now; cross-document
ships as progressive enhancement (don't promise Firefox the animation, or use
Astro's `fallback: animate`). GSAP/Motion instead for complex, interruptible,
scroll-driven, or physics-based motion beyond snapshot crossfade/morph. They are
complementary: View Transitions own state-to-state morphs, GSAP owns scroll-coupled
choreography.

---

## 7. Recommended default toolkit: vanilla / Rails / Astro ("house stack")

The portable default. Everything here works in a Rails ERB view, an Astro `.astro`
file, or a plain HTML page, because none of it requires a React render tree.

| Layer | Pick | Why |
|---|---|---|
| Styling / layout | **Tailwind v4** | Utility-first, framework-agnostic, CSS-first tokens you can animate. Owns the static resting state. |
| Animation engine | **GSAP** (core + ScrollTrigger; add SplitText/Flip/MorphSVG as needed) | Now 100% free incl. all plugins. Deepest timeline + scroll choreography, cross-browser, framework-agnostic. ~30 KB gzip core+ScrollTrigger. |
| Text splitting | **GSAP SplitText** | Free, maintained, built-in masking + aria + resize. (SplitType only if you want the ~4 KB OSI-licensed standalone and not GSAP.) |
| Smooth scroll | **Lenis**, wired to `gsap.ticker` | ~5 KB, wraps native scroll (sticky/anchors/a11y keep working), frame-synced with ScrollTrigger. Gate behind `prefers-reduced-motion`. Only add it when you actually need coordinated scroll effects. |
| rAF loop | **GSAP ticker** (or Tempus if many independent loops) | One shared loop owner; avoid multiple competing rAF loops. |
| Native-first effects | **CSS scroll-snap, CSS scroll-driven (with `@supports` fallback), View Transitions** | Zero bundle. Use before reaching for JS where they suffice. |
| 3D (only when briefed) | **Three.js**, or **OGL** for a lean shader effect | Lazy-load/defer; Three is ~178 KB gzip and not cleanly tree-shaken. |
| 3D/vector assets | **Rive** (interactive), **Lottie** (decorative AE), **Spline** (designer 3D) | Pick by interactivity and existing workflow. Preload Rive WASM; lazy-load Spline. |
| Carousels | **Embla** (headless) or **Swiper** (batteries-included) | Embla for design-system control + small bundle; Swiper for speed-to-ship with built-in UI/effects. |
| Particles / tilt | **tsParticles**, **atropos** | Active, small, framework-agnostic. |
| Fonts | **Variable fonts via Fontsource** + `swap` + preload + Fontaine fallback | Self-host, zero-CLS, animatable axes. |
| Images / video | **sharp** pipeline to AVIF+WebP+widths+ThumbHash; hero video muted/autoplay/poster | Astro `<Image>` if on Astro. |

**Astro note:** Astro adds first-class View Transitions (`<ClientRouter />`) and an
`<Image>`/`<Picture>` pipeline (sharp) for free, so on Astro lean on those before
adding JS. React islands let you selectively pull in the React-tier tools below.

---

## 8. Recommended toolkit when React / Next is in play

Keep the house stack's GSAP + Tailwind, **add** the React-idiomatic pieces. Don't
replace GSAP with Motion: use both for what each is best at.

| Layer | Pick | Why |
|---|---|---|
| Styling | **Tailwind v4** (+ optional **shadcn/ui** for accessible primitives) | Same tokens as the vanilla tier; shadcn gives you owned, animatable Radix-based dialogs/menus/etc. |
| Scroll + timeline choreography | **GSAP via `@gsap/react` `useGSAP`** | `useGSAP` auto-reverts on unmount (handles strict-mode double-invoke), `scope` for selector scoping, `contextSafe` for event handlers. |
| Component / UI / layout / exit / gesture animation | **Motion (`motion/react`)** | Declarative `motion.div`, `AnimatePresence` exit, `layout` animations, gestures, springs. Use `LazyMotion` + `m` to trim bundle. mini (~2.3 KB) for tiny standalone animates. |
| Smooth scroll | **Lenis via `lenis/react`** (`<ReactLenis>` + `useLenis`) | Same engine, React bindings. Still gate `prefers-reduced-motion`. |
| 3D | **R3F + drei** (Three underneath) | Declarative scene graph when 3D is React-embedded and stateful. Import drei helpers individually. Theatre.js (`@theatre/r3f`) if you want visual keyframing. |
| 3D/vector assets | **Spline** (`@splinetool/react-spline`), **Rive** (`@rive-app/react-canvas`), **Lottie** (`lottie-react` / dotLottie React) | Lazy-load Spline; preload Rive WASM. |
| Carousels | **Embla** (`embla-carousel-react`) or **Swiper** (`swiper/react`, not deprecated) | Same tradeoff as the vanilla tier. |
| Fonts | **next/font** | Self-hosts Google fonts at build, auto zero-CLS fallback, variable-font first-class, exposes a CSS var for Tailwind. |
| Images | **next/image** | Format negotiation, srcset, lazy, blur-up, `priority` on hero. |
| Page transitions | **View Transitions** (native same-document is Baseline) or Motion route transitions | Next's `<ViewTransition>` is still experimental; Motion `AnimatePresence` is the production-stable route-transition path in Next today. |

**Escalation trigger (when React earns its weight):** rich app-state-driven UI,
many independent stateful animated components, layout/exit choreography that the
declarative model makes tractable, or 3D that needs to read app state. If the site
is mostly content with bounded interactivity, stay on the vanilla tier: it ships
less JS.

---

## 9. Decision tree / cheat-sheet: "want effect X, reach for Y"

- **Scroll-triggered reveal / pin / scrub / parallax (cross-browser, today)** ->
  **GSAP ScrollTrigger** (+ Lenis for smoothed scroll).
- **Pure scroll-position effect, OK with a Firefox-stable static fallback** ->
  **native CSS scroll-driven** (`animation-timeline`) behind `@supports`.
- **Smoothed/eased scrolling itself** -> **Lenis** (wired to `gsap.ticker`),
  gated by `prefers-reduced-motion`. Not native CSS (it doesn't smooth scroll).
- **Animated headline / text reveal (lines/words/chars, masking, a11y)** ->
  **GSAP SplitText** (free). SplitType only if you want the standalone ~4 KB dep.
- **SVG path morph / draw-on** -> **GSAP MorphSVG / DrawSVG** (now free).
- **FLIP layout animation (element moves between states)** -> **GSAP Flip**
  (vanilla) or **Motion `layout`** (React).
- **Component enter/exit on mount/unmount (React)** -> **Motion `AnimatePresence`**.
- **Gesture/drag/hover spring UI (React)** -> **Motion** gestures.
- **Tiniest possible JS animate** -> **Motion mini (~2.3 KB)** or **raw WAAPI**.
- **Lightweight vanilla engine, no React, true OSI license** -> **anime.js v4**.
- **Cinematic sequenced animation with a visual keyframe editor** -> **Theatre.js**
  (mind the 1.0 uncertainty); for 3D, `@theatre/r3f`.
- **Custom 3D scene** -> **Three.js** (vanilla) / **R3F + drei** (React).
- **Lean shader-only hero effect** -> **OGL** (or a small Three plane).
- **Full game engine (physics/GUI/audio/VR)** -> **Babylon.js**.
- **Visual 3D editor + team collaboration + WebGPU/splats** -> **PlayCanvas**.
- **Shaders on DOM images/video** -> **curtains.js** (verify maintenance) or OGL.
- **Designer-authored interactive 3D into the page** -> **Spline** (lazy-load).
- **Interactive, data-bound UI animation, small files** -> **Rive** (preload WASM).
- **After Effects export, decorative** -> **Lottie** (prefer dotLottie, lazy-load).
- **Animated mouse-reactive 3D background, fast, preset is fine** -> **Vanta.js**
  (lazy-load; mind the heavy engine), or roll your own Three for control.
- **Particles / confetti / fireworks** -> **tsParticles** (confetti-only:
  `canvas-confetti`).
- **3D tilt-on-hover** -> **atropos** (vanilla/React/web component).
- **WebGL image-to-image "liquid" displacement reveal** -> **hover-effect** (only
  if you need exactly that; it's heavy and stale).
- **2D physics (falling/draggable objects, playful UI)** -> **matter.js**
  (Box2D fidelity: planck; performance/determinism: Rapier).
- **Carousel/slider** -> **Embla** (headless, small, design-system) or **Swiper**
  (batteries-included, built-in nav/effects).
- **SPA-like page transitions without a JS router** -> **View Transitions API**
  (same-document Baseline; cross-document not Firefox-stable; Astro `<ClientRouter />`
  for a polyfilled fallback). React route transitions today: **Motion
  `AnimatePresence`**.
- **Hover/loader/looping decorative micro-motion, no JS control needed** ->
  **plain CSS** (`@keyframes`/`transition`, `@starting-style` for entry).

---

## 10. Accessibility & performance notes (per category)

### 10.1 prefers-reduced-motion (applies to everything that moves)

- A mature, universally supported media feature. Under `reduce`, disable or
  drastically tame nonessential motion: skip autoplay, replace big movement with a
  fade or instant state, and **do not run smooth scroll** (Lenis is not automatic,
  gate it).
- Important WCAG nuance: `prefers-reduced-motion` helps with **2.3.3 (Animation
  from Interactions)** but does NOT by itself satisfy **2.2.2 (Pause, Stop, Hide)**.
  Anything auto-playing/looping more than ~5s (hero video, looping marquee, animated
  background) also needs an explicit pause/stop control regardless of the query.
- Pattern: wrap GSAP/Motion timelines and Lenis init in a
  `window.matchMedia('(prefers-reduced-motion: reduce)')` check, and mirror it in
  CSS via `@media (prefers-reduced-motion: reduce)`. GSAP's `gsap.matchMedia()` is
  built for exactly this (define reduced-motion variants declaratively).
- Respect keyboard focus and in-page anchors when using smooth scroll: test
  Tab-to-focus scrolling and `#anchor` jumps; smoothing can desync focus from the
  viewport.

### 10.2 SSR / hydration concerns (React/Next tier)

- GSAP, Three, and the DOM-measuring helpers touch `window`/`document`, so run
  them in `useGSAP`/`useEffect` (client only), never during render. `@gsap/react`
  `useGSAP` is the safe React entry (auto-revert handles strict-mode
  double-invocation).
- ScrollTrigger and Lenis measure layout: initialize after hydration and call
  `ScrollTrigger.refresh()` after fonts/images load to avoid stale trigger
  positions. Reserve image/video boxes (width/height or `aspect-ratio`) so late
  layout shifts don't break trigger math or CLS.
- View Transitions: same-document is safe; Next's `<ViewTransition>` is still
  experimental, so prefer Motion `AnimatePresence` for production route transitions.
  shadcn/Radix render server-side fine but their open/close animations are
  client-driven.
- 3D and heavy effects should be dynamically imported / client-only and ideally
  below-the-fold, so they don't block hydration or the LCP.

### 10.3 Bundle budgets

- **House stack baseline is cheap:** Tailwind (single-digit to low-tens of KB CSS)
  + GSAP core+ScrollTrigger (~30 to 34 KB gzip) + Lenis (~5 KB) + SplitText
  (~3.6 KB). That full motion baseline is roughly ~45 KB gzip of JS, before any 3D.
- **The expensive line items are 3D and asset runtimes:** Three.js ~178 KB gzip
  (and not cleanly tree-shaken), Vanta's three engine ~45 to 180 KB, Lottie
  `lottie-web` ~75 KB plus a possibly 1 MB+ JSON, Spline's runtime + scene. Treat
  any of these as a deliberate, lazy-loaded, below-the-fold decision, never an
  always-shipped dependency on a landing page.
- **React tier additions:** `framer-motion` full ~59 KB gzip (trim with
  `LazyMotion` + `m`), R3F is thin but Three underneath is the real weight, shadcn
  ships only the components you add.
- Rule of thumb for a conversion-critical marketing page: keep the critical-path JS
  for above-the-fold motion in the tens of KB, defer everything 3D/asset-heavy, and
  prefer native (CSS scroll-driven, View Transitions, scroll-snap) where it
  suffices to spend zero bytes.

### 10.4 Native-vs-library perf

- CSS animations, scroll-driven CSS, and WAAPI run **off the main thread** for
  transform/opacity and cost zero bundle, so prefer them when they cover the effect
  (and ship a fallback for scroll-driven where Firefox stable lacks it).
- GSAP/Motion run on the main thread but animate transform/opacity to stay
  compositor-friendly; animate `transform`/`opacity`, not layout-triggering
  properties (`top`/`left`/`width`/`height`), and use `will-change` sparingly.
- Centralize rAF (one GSAP ticker or Tempus) so smooth scroll + WebGL + parallax +
  component animations don't each schedule competing loops and thrash layout.
- Rive/Canvas-WASM rendering bypasses the layout engine and outperforms Lottie for
  heavy/interactive content; preload its WASM for above-the-fold use.
- Hero video: cap size (~4 MB desktop / ~2 MB mobile), poster as the LCP-friendly
  still, lazy-load below-the-fold video, and gate autoplay on reduced-motion.

---

## 11. Corrections to common assumptions (flagged during research)

1. **GSAP is free but not OSI open source.** Free incl. commercial via GreenSock's
   "Standard No Charge" license, with a no-compete clause against building a rival
   visual animation builder and no decompiling. (2025-04-29, GSAP 3.13.)
2. **Motion is no longer React-only.** Older comparisons calling Framer Motion
   "React-only, no vanilla version" are outdated: the `motion` package ships a
   first-class vanilla engine (motion.dev) as of the Nov 2024 rebrand.
3. **Swiper's React/Vue components are NOT deprecated** (verified 2026-06-19). v9
   removed the Angular/Svelte/Solid components (pointing them to `swiper/element`);
   React and Vue were retained and are still shipping.
4. **SplitType's license is ISC, not MIT** (declared only in package.json, no
   LICENSE file). Permissive and free, but not MIT.
5. **anime.js is actively maintained again** (v4 rewrite, 2024 onward). The old
   "abandoned after v3 (2019)" concern no longer holds.
6. **Native scroll-driven CSS is broadly but NOT universally available** (no
   Firefox stable as of mid-2026). Ship behind `@supports` with a fallback.
7. **Cross-document View Transitions are not Firefox-stable yet.** Same-document is
   Baseline; cross-document works in Chromium + Safari 18.2+ only.

---

## Sources

GSAP licensing / bundle:
- https://webflow.com/blog/gsap-becomes-free
- https://gsap.com/pricing/
- https://gsap.com/community/standard-license/
- https://gsap.com/blog/3-13/
- https://gsap.com/resources/React/
- https://bundlephobia.com/package/gsap , https://bundlephobia.com/package/@gsap/react
- https://css-tricks.com/gsap-is-now-completely-free-even-for-commercial-use/

Motion / Framer Motion:
- https://motion.dev/ , https://motion.dev/docs/animate , https://motion.dev/plus
- https://motion.dev/blog/framer-motion-is-now-independent-introducing-motion
- https://motion.dev/docs/react-tailwind , https://motion.dev/docs/react-reduce-bundle-size
- https://github.com/motiondivision/motion
- https://lab.good-fella.com/blog/gsap-vs-framer-motion-vs-react-spring

anime.js / WAAPI / CSS / Theatre / Velocity:
- https://github.com/juliangarnier/anime , https://github.com/juliangarnier/anime/releases/tag/v4.0.0
- https://animejs.com/ , https://bundlephobia.com/package/animejs
- https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API , https://caniuse.com/web-animation
- https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_scroll-driven_animations
- https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline
- https://developer.mozilla.org/en-US/docs/Web/CSS/@starting-style
- https://connect.mozilla.org/t5/ideas/implement-css-scroll-driven-animations-animation-timeline/idi-p/116931
- https://github.com/theatre-js/theatre , https://bundlephobia.com/package/@theatre/core
- https://github.com/julianshapiro/velocity

Smooth scroll:
- https://github.com/darkroomengineering/lenis , https://github.com/darkroomengineering/lenis/discussions/140
- https://www.npmjs.com/package/lenis
- https://github.com/locomotivemtl/locomotive-scroll , https://scroll.locomotive.ca/docs/

3D / WebGL / assets:
- https://github.com/mrdoob/three.js/releases/tag/r184 , https://en.wikipedia.org/wiki/Three.js
- https://github.com/pmndrs/react-three-fiber , https://bundlephobia.com/package/@react-three/drei
- https://github.com/oframe/ogl , https://oframe.github.io/ogl/
- https://blog.logrocket.com/three-js-vs-babylon-js/ , https://playcanvas.com/ , https://github.com/playcanvas/engine
- https://www.curtainsjs.com/ , https://github.com/martinlaxenaire/curtainsjs
- https://github.com/splinetool/react-spline , https://bundlephobia.com/package/@splinetool/react-spline
- https://help.rive.app/runtimes/overview/web-js/preloading-wasm , https://www.callstack.com/blog/lottie-vs-rive-optimizing-mobile-app-animation
- https://www.npmjs.com/package/lottie-web , https://dotlottie.io/intro/
- https://threejs-journey.com/

Helpers:
- https://github.com/lukePeavey/SplitType , https://bundlephobia.com/package/split-type
- https://gsap.com/docs/v3/Plugins/SplitText/
- https://github.com/darkroomengineering/tempus
- https://github.com/liabru/matter-js , https://rapier.rs/
- https://github.com/tsparticles/tsparticles , https://particles.js.org/
- https://github.com/tengbao/vanta
- https://github.com/nolimits4web/atropos , https://github.com/micku7zu/vanilla-tilt.js , https://github.com/robin-dela/hover-effect
- https://github.com/davidjerleke/embla-carousel
- https://github.com/nolimits4web/swiper , https://raw.githubusercontent.com/nolimits4web/swiper/master/CHANGELOG.md

Supporting tooling:
- https://tailwindcss.com/blog/tailwindcss-v4 , https://endoflife.date/tailwind-css , https://tailwindcss.com/blog/tailwind-plus
- https://ui.shadcn.com/docs , https://ui.shadcn.com/docs/installation , https://github.com/shadcn-ui/ui
- https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_fonts/Variable_fonts_guide
- https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display
- https://fontsource.org/docs/getting-started/introduction , https://nextjs.org/docs/app/api-reference/components/font
- https://developer.chrome.com/blog/framework-tools-font-fallback/
- https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Formats/Image_types
- https://web.dev/learn/design/responsive-images , https://web.dev/learn/performance/video-performance
- https://addyosmani.com/blog/fetch-priority/ , https://github.com/lovell/sharp
- https://nextjs.org/docs/app/api-reference/components/image , https://docs.astro.build/en/guides/images/
- https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API
- https://web.dev/blog/same-document-view-transitions-are-now-baseline-newly-available
- https://caniuse.com/view-transitions , https://developer.chrome.com/docs/web-platform/view-transitions/cross-document
- https://docs.astro.build/en/guides/view-transitions/ , https://nextjs.org/docs/app/guides/view-transitions
- https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- https://www.framer.com/pricing/ , https://www.unicorn.studio/docs/pricing/
