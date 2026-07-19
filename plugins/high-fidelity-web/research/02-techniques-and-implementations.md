# 02. Techniques and Implementations

How the impressive interactions on Stripe / Linear / Vercel / Apple / Column / Awwwards "Site of the Day" sites are actually built. This is the HOW companion to the design-principles doc. It is organized by technique, each with **How it works**, **Tools / APIs / properties**, and **Gotchas / perf**.

Primary context is **vanilla JS + GSAP + Tailwind** (Rails-friendly, framework-agnostic). React / R3F equivalents are noted inline.

Research grounded in Codrops, GSAP docs, MDN, web.dev, CSS-Tricks, olivierlarose.com, Maxime Heckel, and library showcases. Sources with URLs are at the bottom; key claims are inline-cited.

> One firsthand caveat: a few flagship Codrops articles (Magnetic Buttons, WebGL displacement) are promo shells that link to GitHub/demos for the real shader/JS. The load-bearing patterns below were reconstructed from tutorials that ship full code (olivierlarose, GSAP docs) plus the libraries' public APIs, so magnetic-button / cursor snippets are verbatim while the deepest shader internals are described conceptually plus the public constructor API.

---

## Table of contents

1. [Scroll animation](#1-scroll-animation)
2. [Smooth scroll](#2-smooth-scroll)
3. [WebGL / near-3D heroes](#3-webgl--near-3d-heroes)
4. [Page and element transitions](#4-page-and-element-transitions)
5. [Micro-interaction techniques](#5-micro-interaction-techniques)
6. [Performance techniques](#6-performance-techniques)
7. [Anatomy of famous effects](#7-anatomy-of-famous-effects)
8. [Library usage by high-fidelity sites](#8-library-usage-by-high-fidelity-sites)
9. [Sources](#sources)

---

## 1. Scroll animation

### 1.1 GSAP ScrollTrigger (the workhorse)

**How it works.** ScrollTrigger links a tween or timeline to a scroll position. You give it a `trigger` element and `start` / `end` positions (expressed as `"element-edge viewport-edge"`, e.g. `"top center"`). As the scrollbar moves between start and end, ScrollTrigger either fires the animation (`toggleActions`) or ties the animation's playhead directly to scroll progress (`scrub`). With `pin: true` it fixes the trigger in place for the duration of the scroll, so the user keeps scrolling but the section stays put while the animation plays. ([gsap.com/docs/v3/Plugins/ScrollTrigger](https://gsap.com/docs/v3/Plugins/ScrollTrigger/))

**Tools / APIs / properties.**

- `trigger`, `start`, `end`, `markers: true` (dev-only visual guides).
- `scrub: true` (playhead snaps to scroll) or `scrub: 1` (1-second catch-up lag, feels smoother / more cinematic).
- `pin: true`, `pinSpacing` (whether to add padding so following content does not jump), `anticipatePin`.
- `toggleActions: "play pause resume reverse"` (4 states: onEnter, onLeave, onEnterBack, onLeaveBack) for non-scrubbed reveals.
- `snap` (to progress values, labels, or a function), e.g. `snap: 1 / (sections.length - 1)`.
- `gsap.matchMedia()` / `ScrollTrigger.matchMedia()` for responsive setup that auto-reverts at breakpoints.
- `ScrollTrigger.normalizeScroll(true)` to take over native scrolling (fixes mobile address-bar resize jank and synchronizes touch).
- `ScrollTrigger.refresh()` after layout changes (fonts load, images sized, route change).

**Basic scrubbed reveal:**

```javascript
gsap.registerPlugin(ScrollTrigger);

gsap.to(".panel", {
  yPercent: -100,
  ease: "none",
  scrollTrigger: {
    trigger: ".panel",
    start: "top top",
    end: "bottom top",
    scrub: true,
  },
});
```

**Pinned scene (a "scene" is a pinned trigger with its own timeline):**

```javascript
const tl = gsap.timeline({
  scrollTrigger: {
    trigger: ".showcase",
    start: "top top",
    end: "+=2000",      // scene lasts 2000px of scroll
    pin: true,
    scrub: 1,
  },
});
tl.from(".headline", { opacity: 0, y: 50 })
  .from(".product", { scale: 0.8 }, "<")   // "<" = start at same time as previous
  .to(".product", { rotate: 15 });
```

**Horizontal scroll section (the Awwwards staple).** Vertical scroll is translated into horizontal motion: pin a container, then `x`-translate a wide inner track by its overflow width, driven by scrub. ([gsap.com/docs/v3/Plugins/ScrollTrigger](https://gsap.com/docs/v3/Plugins/ScrollTrigger/))

```javascript
const track = document.querySelector(".track");
const panels = gsap.utils.toArray(".track .panel");

gsap.to(track, {
  x: () => -(track.scrollWidth - window.innerWidth),
  ease: "none",
  scrollTrigger: {
    trigger: ".horizontal",
    pin: true,
    scrub: 1,
    end: () => "+=" + (track.scrollWidth - window.innerWidth),
    invalidateOnRefresh: true,   // recompute the function-based values on resize
  },
});
```

Key detail: use **function-based values** (`() => ...`) for `x` and `end` plus `invalidateOnRefresh: true` so widths recompute on resize instead of caching a stale pixel value.

**React equivalent.** `@gsap/react`'s `useGSAP(() => {...}, { scope: ref })` hook handles cleanup (`ctx.revert()`) automatically on unmount, which solves the #1 React + GSAP footgun (orphaned ScrollTriggers across re-renders).

**Gotchas / perf.**

- Pin works by wrapping the trigger in a `pin-spacer`; if your CSS targets direct-child selectors or relies on exact DOM order, the inserted spacer can break it.
- Always call `ScrollTrigger.refresh()` after async content changes height, and prefer `invalidateOnRefresh` for function-based values.
- `scrub: true` is exact; `scrub: <number>` adds smoothing lag (nicer feel, but the animation can lag behind a fast flick).
- Animate `transform`/`opacity` only inside scrubbed tweens (see Perf section) so each frame stays on the compositor.

### 1.2 Native scroll-linked CSS (scroll-driven animations)

**How it works.** The browser drives a regular CSS `@keyframes` animation off a **scroll timeline** instead of a time clock, entirely off the main thread. Two timeline kinds: `scroll()` tracks how far a scroll container has scrolled (0% to 100%); `view()` tracks an element's visibility as it enters and exits the scrollport (great for reveals). ([MDN scroll-driven animations](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations); [Josh Comeau](https://www.joshwcomeau.com/animation/scroll-driven-animations/))

**Tools / APIs / properties.**

- `animation-timeline: scroll(root block)` or `animation-timeline: view()`.
- Named timelines: `scroll-timeline-name` / `view-timeline-name` declared on the scroller, referenced by name on the animated element; `timeline-scope` lets a name reach across the DOM (escape the direct-ancestor restriction).
- `animation-range: entry 0% cover 50%` etc. View-timeline named ranges: `entry`, `exit`, `contain`, `cover`.

**Reveal on enter, no JS:**

```css
@keyframes reveal {
  from { opacity: 0; transform: translateY(40px); }
  to   { opacity: 1; transform: translateY(0); }
}
.card {
  animation: reveal linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;   /* play as it enters */
}
```

**Progress bar tied to page scroll:**

```css
@keyframes grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }
.progress {
  transform-origin: left;
  animation: grow linear both;
  animation-timeline: scroll(root block);
}
```

**Browser support (2026):** Chromium (Chrome/Edge/Opera) since ~115, Safari since 18, Firefox partial / behind a flag. Treat it as progressive enhancement: gate with `@supports (animation-timeline: view())` and fall back to IntersectionObserver or the scroll-timeline polyfill. ([MDN animation-timeline](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation-timeline); [dev.to 2026 guide](https://dev.to/nickbenksim/creating-complex-scroll-driven-animations-with-pure-css-in-2026-17l))

**Gotchas / perf.** Compositor-driven, so it is the most performant option for simple reveals/parallax and frees the main thread. But it cannot pin, cannot snap, and orchestration across many elements is clumsy versus a GSAP timeline. Rule of thumb: native CSS for simple per-element reveals and scrollbars; GSAP ScrollTrigger when you need pinning, scrubbed multi-step timelines, snapping, or cross-browser certainty.

### 1.3 IntersectionObserver reveals

**How it works.** Register a callback that fires when a target crosses a visibility `threshold` relative to the viewport (optionally inset by `rootMargin`). On first intersection, add a class (CSS transition does the motion) and `unobserve` so it never re-runs.

```javascript
const io = new IntersectionObserver((entries) => {
  for (const entry of entries) {
    if (entry.isIntersecting) {
      entry.target.classList.add("is-visible");
      io.unobserve(entry.target);   // reveal once, then stop watching
    }
  }
}, { threshold: 0.2, rootMargin: "0px 0px -10% 0px" });

document.querySelectorAll("[data-reveal]").forEach((el) => io.observe(el));
```

**Gotchas / perf.** Far cheaper than `scroll` listeners (no per-frame work). `rootMargin` with a negative bottom value delays the trigger until the element is comfortably in view. Unobserve after reveal to avoid leaks. Pair with `prefers-reduced-motion` by skipping the transition.

### 1.4 Parallax math

**How it works.** Move a layer by an amount **proportional to scroll progress**, scaled by a depth factor: nearer layers move more, distant layers less (or opposite for foreground/background). The core formula is `translateY = scrollProgress * range * depthFactor`.

With ScrollTrigger this is just a scrubbed tween where the travel distance encodes depth:

```javascript
gsap.utils.toArray("[data-speed]").forEach((el) => {
  const speed = parseFloat(el.dataset.speed);   // e.g. 0.2 slow, 0.8 fast
  gsap.to(el, {
    yPercent: -100 * speed,
    ease: "none",
    scrollTrigger: { trigger: el.parentElement, scrub: true, start: "top bottom", end: "bottom top" },
  });
});
```

Native CSS version: drive `translateY` from a `scroll()` timeline with a different `animation-range` per layer. **Gotcha:** always parallax with `transform: translate`, never `background-position` or `top`, to stay compositor-only and avoid layout/CLS.

---

## 2. Smooth scroll

### 2.1 Lenis (the current standard)

**How it works.** Lenis (by darkroom.engineering) intercepts wheel/touch input, maintains a **virtual target scroll position**, and each animation frame lerps the actual position toward that target, then applies it (via `window.scrollTo` or a transform). The result is a weighted, eased "glide" instead of the OS's stepwise scroll. Crucially it is designed to **sync with**, not replace, other rAF-driven systems (GSAP, WebGL). ([github.com/darkroomengineering/lenis](https://github.com/darkroomengineering/lenis))

**Tools / APIs / properties.**

- Config: `lerp` (0 to 1 smoothing factor; lower = smoother/slower catch-up), `duration` + `easing` (alternative to lerp), `smoothWheel`, `syncTouch` (smooth on touch, off by default since native momentum is usually better), `wheelMultiplier`, `orientation`, `gestureOrientation`, `infinite`.
- Methods/events: `lenis.raf(time)` (advance one frame), `lenis.on('scroll', cb)`, `lenis.scrollTo(target, opts)`, `lenis.stop()` / `lenis.start()`.

**Canonical GSAP ScrollTrigger integration** (the exact pattern you see across high-fidelity sites):

```javascript
const lenis = new Lenis();

// 1. ScrollTrigger updates on every Lenis scroll event
lenis.on('scroll', ScrollTrigger.update);

// 2. Drive Lenis from GSAP's single ticker (one rAF loop for everything)
gsap.ticker.add((time) => {
  lenis.raf(time * 1000);   // gsap ticker is in seconds, lenis wants ms
});

// 3. Disable GSAP's lag smoothing so scroll + tweens stay in lockstep
gsap.ticker.lagSmoothing(0);
```

Folding Lenis into `gsap.ticker` (rather than a separate `requestAnimationFrame`) guarantees one synchronized frame loop, which is why ScrollTrigger pins and scrubs feel glued to the smooth scroll. ([github.com/darkroomengineering/lenis](https://github.com/darkroomengineering/lenis))

**React equivalent.** `lenis/react` (formerly `@studio-freight/react-lenis`) exposes a `<ReactLenis root>` wrapper and `useLenis()` hook; combine with `useGSAP`.

**Locomotive Scroll** is the older smooth-scroll lib; v5 is now built on top of Lenis, so Lenis is effectively the engine either way.

**Gotchas / perf, and when NOT to hijack scroll.**

- Hijacked scroll breaks native affordances: anchor `#hash` jumps, keyboard `PageDown`/`Space`, focus scrolling, and find-in-page can land in the wrong place. Use `lenis.scrollTo()` for in-page links and test keyboard nav.
- Disable or neutralize under `prefers-reduced-motion` (instantiate with `lerp: 1` / `smooth: false`, or skip Lenis entirely): smooth scrolling is itself a motion concern, not just keyframes. ([Smashing, Respecting Motion Preferences](https://www.smashingmagazine.com/2021/10/respecting-users-motion-preferences/))
- On mobile, native momentum often beats `syncTouch`; leave touch smoothing off unless the design truly needs it.
- Virtual-scroll tradeoff: you own the scroll position now, so anything that measures `scrollTop` or expects native scroll restoration needs to go through Lenis. Always weigh whether the "feel" is worth giving up native behavior.

---

## 3. WebGL / near-3D heroes

### 3.1 Three.js core (for a hero scene)

**How it works.** A Three.js scene is: a `Scene` (container), a `Camera` (usually `PerspectiveCamera` or, for flat full-screen effects, `OrthographicCamera`), a `WebGLRenderer` bound to a `<canvas>`, and `Mesh`es (a `Geometry` plus a `Material`). For shader heroes the material is a `ShaderMaterial` (or `RawShaderMaterial`) with custom GLSL **vertex** and **fragment** shaders and `uniforms` (values passed from JS into the shader, e.g. `uTime`, `uMouse`, `uResolution`). A `requestAnimationFrame` loop bumps `uTime` and calls `renderer.render(scene, camera)` each frame.

```javascript
const scene = new THREE.Scene();
const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));   // cap DPR (perf)

const geometry = new THREE.PlaneGeometry(2, 2, 128, 128);       // subdivided plane
const material = new THREE.ShaderMaterial({
  uniforms: { uTime: { value: 0 }, uMouse: { value: new THREE.Vector2() } },
  vertexShader, fragmentShader,
});
scene.add(new THREE.Mesh(geometry, material));

const clock = new THREE.Clock();
function tick() {
  material.uniforms.uTime.value = clock.getElapsedTime();
  renderer.render(scene, camera);
  requestAnimationFrame(tick);
}
tick();
```

- **Vertex shader** runs per vertex; it positions geometry (this is where you displace a plane to make a waving gradient mesh).
- **Fragment shader** runs per pixel; it decides color (this is where you mix gradient colors, apply noise, distortion, RGB shift).

**React equivalent (R3F + drei).** `@react-three/fiber` maps the whole Three.js API to JSX components and gives you the `useFrame((state) => {...})` render-loop hook and `useThree()` for renderer/camera. drei's `shaderMaterial(uniforms, vertex, fragment)` helper generates a self-contained material component; you update uniforms via a `ref` inside `useFrame`. ([drei shaderMaterial docs](https://drei.docs.pmnd.rs/shaders/shader-material); [Maxime Heckel, Study of Shaders](https://blog.maximeheckel.com/posts/the-study-of-shaders-with-react-three-fiber/))

```jsx
const ColorMaterial = shaderMaterial({ uTime: 0 }, vertexShader, fragmentShader);
extend({ ColorMaterial });
function Hero() {
  const ref = useRef();
  useFrame((_, delta) => (ref.current.uTime += delta));
  return <mesh><planeGeometry args={[2, 2, 128, 128]} /><colorMaterial ref={ref} /></mesh>;
}
```

**OGL** is a lighter-weight (no scene-graph overhead) alternative to Three.js for single-effect heroes where you do not need Three's full feature set; smaller bundle, closer to raw WebGL.

### 3.2 Shader-based hero effects

- **Animated gradient mesh (Stripe-style).** A subdivided plane whose vertices are displaced (in the vertex shader) by layered **Simplex/Perlin noise** sampled over `uTime`, with colors blended in the fragment shader. Full anatomy in [section 7.1](#71-stripe-style-animated-gradient-hero).
- **Distortion / displacement.** Offset each fragment's texture-lookup UV by a value read from a grayscale displacement map, scaled by a `uProgress` uniform: `vec2 uv2 = uv + displacement.r * intensity * uProgress;`. Drives liquid hover reveals and crossfades.
- **Particles / GPGPU.** Thousands of points rendered as a `Points` object; for huge counts you store positions in a texture and update them with a simulation shader (GPGPU/FBO ping-pong) so the GPU moves the particles, not the CPU.

### 3.3 Image-to-WebGL

**How it works.** Take a DOM `<img>`, upload it as a GL texture, and render it on a plane so you can apply shader effects (distortion, RGB shift, scroll-velocity warp). **curtains.js** is the friendly wrapper: it positions WebGL planes exactly over their DOM `<img>` elements and syncs them on scroll/resize, so you keep accessible HTML and layer WebGL on top. GSAP then tweens a single `uProgress` uniform 0 to 1 for hover/transition reveals. ([CSS-Tricks, curtains.js](https://css-tricks.com/creating-webgl-effects-with-curtainsjs/))

**Displacement crossfade (concept).** Feed two textures plus a displacement map; the fragment shader distorts each toward the other and `mix()`es by progress: `mix(texture(img1, uvA), texture(img2, uvB), uProgress)`. Codrops' canonical three-step recipe: distort using the displacement texture, crossfade the two images, then reverse the displacement. ([Codrops, WebGL distortion hover](https://tympanus.net/codrops/2018/04/10/webgl-distortion-hover-effects/))

### 3.4 When WebGL is worth it, and performance budgets

**When to reach for it:** brand/hero moments that genuinely need organic motion, depth, fluid distortion, or particle volume that CSS/SVG cannot fake (the Stripe gradient, immersive Active Theory-style scenes). **When NOT to:** simple gradients (a CSS `conic-gradient` + slow `@keyframes` or an animated SVG is far cheaper), basic reveals, anything where the payoff is marginal versus shipping a renderer.

**Performance budgets / rules:**

- Cap pixel ratio: `renderer.setPixelRatio(Math.min(devicePixelRatio, 2))` (Retina at full DPR is 4x the fragments).
- Watch **draw calls** and keep geometry/material counts low; merge where possible.
- Keep **texture sizes** modest and power-of-two; compress.
- **Lazy-load** the renderer: dynamic `import('three')` on first intersection so it stays out of the initial bundle and off the LCP critical path.
- Pause the rAF loop when the canvas is offscreen (IntersectionObserver) or the tab is hidden.
- Always ship a **CSS fallback** for no-WebGL contexts and for `prefers-reduced-motion`.

---

## 4. Page and element transitions

### 4.1 View Transitions API (native)

**How it works.** Wrap a DOM change in `document.startViewTransition(callback)`. The browser snapshots the old state, runs your callback to produce the new state, then cross-fades (by default) between old and new snapshots. Elements tagged with `view-transition-name` are snapshotted **independently** and animate from their old to new position/size, giving morph / shared-element transitions for free. ([MDN View Transition API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API))

```javascript
document.startViewTransition(() => {
  updateDOM();   // swap content / change route view
});
```

```css
.hero-image { view-transition-name: hero; }   /* this element morphs across the change */
```

The transition exposes a pseudo-element tree you can target with CSS animations:

```
::view-transition
└── ::view-transition-group(name)
    └── ::view-transition-image-pair(name)
        ├── ::view-transition-old(name)   /* outgoing snapshot */
        └── ::view-transition-new(name)   /* incoming snapshot */
```

```css
::view-transition-old(hero) { animation: 300ms ease-out both fade-out; }
::view-transition-new(hero) { animation: 300ms ease-in  both fade-in; }
```

**Same-document (SPA)** uses `startViewTransition()`. **Cross-document (MPA, plain multi-page sites)** opts in with an at-rule, no JS:

```css
@view-transition { navigation: auto; }
```

and exposes `pageswap` / `pagereveal` events on the two documents for fine control. ([MDN View Transition API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API))

**Browser support (2026):** `startViewTransition` and `view-transition-name` in Chromium 111+ and (per MDN) expanding; cross-document `@view-transition` in Chromium 125+; Firefox support still limited as of late 2025. Treat as progressive enhancement.

**Reduced motion:**

```css
@media (prefers-reduced-motion: reduce) { ::view-transition-group(*) { animation: none; } }
```

or call `transition.skipTransition()` in JS.

**Gotchas / perf.** A `view-transition-name` must be **unique** per transition (two elements sharing a name throws). The old/new snapshots are flat images during the transition, so very large morphing regions can look soft. It pauses interaction briefly during the snapshot. Astro's view transitions and the Next.js App Router both wrap this API for route transitions.

### 4.2 FLIP technique and GSAP Flip

**How it works.** FLIP = **First, Last, Invert, Play**. Record an element's **First** position/size, make your DOM change (it jumps to its **Last** position), compute the delta and apply an inverse transform so it **looks** unmoved (**Invert**), then animate the transform back to zero (**Play**). Because the whole motion is a `transform`, it is compositor-cheap even when the underlying change was a layout change (reflow, reparenting, grid reorder). ([gsap.com/docs/v3/Plugins/Flip](https://gsap.com/docs/v3/Plugins/Flip/))

**GSAP Flip plugin** automates all four steps:

```javascript
gsap.registerPlugin(Flip);

const state = Flip.getState(".items");   // FIRST: capture position/size
container.classList.toggle("grid-to-list");   // make any layout change
Flip.from(state, {                       // LAST/INVERT/PLAY animated for you
  duration: 0.6,
  ease: "power2.inOut",
  absolute: true,        // position:absolute during the flip (prevents reflow mid-anim)
  nested: true,          // avoid compounding offsets on nested flipped elements
  stagger: 0.05,
});
```

- `Flip.getState(targets, { props: "backgroundColor,borderRadius" })` can also capture non-geometric props to animate.
- **Shared-element transitions:** give the "same" element in two different DOM trees a matching `data-flip-id`; Flip morphs the source into the destination. This is the classic thumbnail-to-detail expand.
- Helpers: `Flip.fit(a, b)` (resize one element to match another), `Flip.batch()`, `Flip.makeAbsolute()`.

GSAP Flip is the cross-browser, fully-controllable cousin of the native View Transitions API. View Transitions is lighter (no JS, native) but less controllable and less supported; Flip works everywhere GSAP does and gives you eases, stagger, and timeline control.

### 4.3 Route transitions in SPAs

- **barba.js** (historical) intercepted link clicks, fetched the next page, and ran enter/leave animations while swapping a container. Still seen on vanilla/jQuery-era creative sites; largely superseded by native View Transitions and framework routers.
- **Next.js (App Router):** native View Transitions support plus `framer-motion` / `motion` `AnimatePresence` for enter/exit of route segments.
- **Framer Motion (`motion`):** `AnimatePresence` keeps exiting components mounted long enough to animate out; `layout` and `layoutId` props implement automatic FLIP / shared-element transitions declaratively (the React analogue of GSAP Flip's `data-flip-id`).
- **Astro:** `<ViewTransitions />` wraps the native API for MPA-style route transitions with almost no code.

### 4.4 Text reveal / split-text animations

**How it works.** Split a text node into per-line, per-word, or per-char wrapper elements, then animate them with a `stagger`. The signature "lines rising from behind a mask" look wraps each line in an `overflow: hidden` (or `clip`) container and animates the inner text from `yPercent: 100` to `0`, so each line slides up out of an invisible mask. ([gsap.com/docs/v3/Plugins/SplitText](https://gsap.com/docs/v3/Plugins/SplitText/); [Codrops, 7 GSAP tips](https://tympanus.net/codrops/2025/09/03/7-must-know-gsap-animation-tips-for-creative-developers/))

**GSAP SplitText** (now free in GSAP 3.13+, with **built-in masking**):

```javascript
gsap.registerPlugin(SplitText);

const split = SplitText.create(".headline", { type: "lines", mask: "lines" });
gsap.from(split.lines, {
  yPercent: 100,        // slide up from behind the mask
  opacity: 0,
  duration: 0.8,
  ease: "power3.out",
  stagger: 0.1,         // 100ms cascade between lines
});
```

- `type`: `"chars"`, `"words"`, `"lines"`, or combos. `mask: "lines"` (3.13+) auto-wraps each unit in an `overflow:hidden` clip element; before 3.13 you nested wrappers by hand.
- Typical stagger: `0.02` (20ms) for chars (snappy but readable), `0.1` for lines.
- **Always `split.revert()` on cleanup** (and re-split on resize / after fonts load), or line breaks go stale.

**Vanilla alternative: SplitType** (`new SplitType(el, { types: "lines,words,chars" })`) gives you the same per-unit wrappers without GSAP, then animate with GSAP or CSS.

**clip-path / mask reveals** (no splitting): animate `clip-path: inset(...)` or a `mask` gradient to wipe text/elements into view. Compositor-friendly and great for image and block reveals.

---

## 5. Micro-interaction techniques

### 5.1 Magnetic buttons

**How it works.** On `mousemove`, read the element's bounding box, compute the cursor's offset from its center, multiply by a strength factor, and translate the element toward the cursor with `transform`. On `mouseleave`, animate back to origin (an elastic ease sells the snap-back). ([olivierlarose, magnetic button](https://blog.olivierlarose.com/tutorials/magnetic-button))

```javascript
const xTo = gsap.quickTo(el, "x", { duration: 1, ease: "elastic.out(1, 0.3)" });
const yTo = gsap.quickTo(el, "y", { duration: 1, ease: "elastic.out(1, 0.3)" });

el.addEventListener("mousemove", (e) => {
  const { left, top, width, height } = el.getBoundingClientRect();
  const x = e.clientX - (left + width / 2);
  const y = e.clientY - (top + height / 2);
  xTo(x * 0.4);   // 0.4 = strength: drift toward, not all the way to, the cursor
  yTo(y * 0.4);
});
el.addEventListener("mouseleave", () => { xTo(0); yTo(0); });
```

For a larger magnetic "field," attach the listener to an invisible wrapper and move the inner button. Layer parallax by moving the label/shadow at different strengths. **Perf:** use `gsap.quickTo` (reuses one tween) rather than a fresh `gsap.to()` per `mousemove`; disable on touch and under reduced-motion.

### 5.2 Custom cursors

**How it works.** A `position: fixed; pointer-events: none` div follows the pointer, lerped toward the target each frame for a trailing feel. On hover targets, scale it up; `mix-blend-mode: difference` inverts whatever is beneath it. ([olivierlarose, blend-mode cursor](https://blog.olivierlarose.com/tutorials/blend-mode-cursor))

```javascript
gsap.set(".cursor", { xPercent: -50, yPercent: -50 });   // center on pointer
const xTo = gsap.quickTo(".cursor", "x", { duration: 0.4, ease: "power3" });
const yTo = gsap.quickTo(".cursor", "y", { duration: 0.4, ease: "power3" });
window.addEventListener("mousemove", (e) => { xTo(e.clientX); yTo(e.clientY); });
```

```css
.cursor { position: fixed; top: 0; left: 0; width: 30px; height: 30px;
  border-radius: 50%; background: #fff; pointer-events: none;
  mix-blend-mode: difference; }
```

GSAP's tween `duration`/`ease` supplies the trailing lerp for you. On `mouseenter` of `[data-cursor-hover]`, tween `scale` up (e.g. 13x). **Perf:** `mix-blend-mode` is GPU-heavier and can force a layer; keep `pointer-events: none`; restore the native cursor under reduced-motion / touch.

### 5.3 Hover distortion on images (three tiers)

- **CSS-only (hover.css style):** `transform`/`filter` transitions (scale, skew, grayscale to color). Cheapest, compositor-friendly, no JS. Good default.
- **WebGL displacement (Codrops hover-effect.js):** feed two textures + a grayscale displacement map; the fragment shader offsets UVs by the displacement scaled by a `dispFactor` uniform tweened 0 to 1. Liquid reveal. ([Codrops](https://tympanus.net/codrops/2018/04/10/webgl-distortion-hover-effects/))

```javascript
new hoverEffect({
  parent: document.querySelector('.tile'),
  image1: 'a.jpg', image2: 'b.jpg', displacementImage: 'disp.png',
});
```

- **RGB shift / chromatic aberration:** sample the red channel at a slightly offset UV from green/blue, often driven by mouse velocity. curtains.js is the lighter wrapper. **Perf:** lazy-load three/Curtains, small power-of-two displacement maps, CSS fallback.

### 5.4 Marquees / infinite loops

- **CSS-only seamless loop:** duplicate the content inline, translate the track `-50%`. Because copy 2 is identical, the wrap is invisible. Compositor-only, but fixed speed and not draggable.

```css
.track { display: flex; width: max-content; animation: marquee 20s linear infinite; }
@keyframes marquee { to { transform: translateX(-50%); } }
.track:hover { animation-play-state: paused; }
```

- **GSAP `horizontalLoop()` helper (robust):** animates a group along x in a seamless, responsive, optionally draggable loop. It converts to **`xPercent`** so it survives resize, wraps the playhead with `modifiers: { time: gsap.utils.wrap(0, tl.duration()) }`, and returns a timeline with `next()` / `previous()` / `toIndex()` so the same marquee doubles as a slider. ([GSAP seamlessLoop helper](https://gsap.com/docs/v3/HelperFunctions/helpers/seamlessLoop/)) **Perf:** animate `xPercent`/`transform`, never `left`/`margin` (CLS); pause offscreen.

### 5.5 Sticky / gooey effects

**How it works.** Chain two SVG filter primitives: `feGaussianBlur` blurs sibling blobs so their edges bleed together, then `feColorMatrix` thresholds the **alpha** with a steep multiplier to snap the overlap back into crisp merged shapes. Apply the filter to the **parent** of the blobs. ([CSS-Tricks, gooey effect](https://css-tricks.com/gooey-effect/))

```html
<svg style="position:absolute;width:0;height:0"><defs>
  <filter id="goo">
    <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur"/>
    <feColorMatrix in="blur" mode="matrix"
      values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -7"/>
  </filter>
</defs></svg>
```

The last row `0 0 0 18 -7` is the trick: `18` sharpens, `-7` sets the merge threshold. **Perf:** SVG filters are expensive and force layers; keep them on small regions and isolate just the blob layer (they blur everything in the container, text included).

### 5.6 Number tickers / count-up

- **GSAP value-object tween (flexible):** animate a proxy and write text in `onUpdate`; `snap` rounds.

```javascript
const obj = { val: 0 };
gsap.to(obj, { val: 12500, duration: 3, ease: "power1.out", snap: { val: 1 },
  onUpdate: () => el.textContent = Math.round(obj.val).toLocaleString() });   // 12,500
```

- **Odometer-style rolling digits:** each digit is a vertical `0..9` strip in an `overflow:hidden` window; translate by `-digit * 10%`. Reads mechanical. HubSpot's Odometer packages this.

**Perf:** only run when in view (IntersectionObserver); use `font-variant-numeric: tabular-nums` so width does not jitter (avoids CLS); in React write to a ref, not state, per frame.

---

## 6. Performance techniques

### 6.1 Compositor-only animation (transform + opacity)

The render pipeline is **style → layout → paint → composite**. Animating `transform` and `opacity` can run entirely at the **composite** stage on the GPU, skipping layout and paint. web.dev's rule: avoid animating any property that triggers layout or paint. ([web.dev animations guide](https://web.dev/articles/animations-guide))

- Move with `translate()`, not `top`/`left`/`margin`.
- Resize with `scale()`, not `width`/`height`.
- Fade with `opacity`.

### 6.2 will-change (use sparingly)

`will-change: transform` hints the browser to promote an element to its own compositor layer ahead of time. Use it only for elements that genuinely change often, ideally added via JS right before the animation and removed after. Over-applying creates many layers, eating GPU memory and sometimes hurting perf. Legacy force-promote: `transform: translateZ(0)`.

```javascript
el.addEventListener("mouseenter", () => el.style.willChange = "transform");
el.addEventListener("mouseleave", () => el.style.willChange = "auto");
```

### 6.3 Avoid layout thrash (read-all then write-all)

Interleaving DOM reads (`getBoundingClientRect`, `offsetWidth`, `scrollTop`) with writes forces repeated synchronous reflows. Batch: do all reads, then all writes (the FastDOM pattern: reads in one rAF phase, writes in the next). GSAP largely sidesteps this by batching all tweens into one ticker flush.

### 6.4 requestAnimationFrame and gsap.ticker

Drive per-frame work through `requestAnimationFrame` so it syncs to refresh and pauses on hidden tabs. With GSAP, everything runs on a single `gsap.ticker`; prefer `gsap.ticker.add(fn)` over a separate rAF when mixing with GSAP. Use `gsap.quickTo()` / `gsap.quickSetter()` for high-frequency updates (mousemove, scroll): they skip per-call parsing overhead and reuse one tween instead of allocating a new `gsap.to()` each event.

### 6.5 Lazy-load heavy assets

- Images/iframes: native `loading="lazy"`.
- Sections/components: IntersectionObserver to init near-viewport.
- Heavy libs (three.js, shaders): **dynamic `import()`** on demand to keep them out of the initial bundle.

```javascript
const io = new IntersectionObserver(async ([entry]) => {
  if (!entry.isIntersecting) return;
  const THREE = await import("three");
  initScene(THREE);
  io.disconnect();
});
```

### 6.6 prefers-reduced-motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: .001ms !important; animation-iteration-count: 1 !important;
    transition-duration: .001ms !important; scroll-behavior: auto !important;
  }
}
```

`gsap.matchMedia()` is the idiomatic GSAP approach: animations/ScrollTriggers built inside a matching block auto-revert when the query stops matching, giving clean teardown for both reduced-motion and breakpoints.

```javascript
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  gsap.to(".hero", { x: 200, scrollTrigger: ".hero" });   // only built when motion is OK
});
```

Disable smooth scroll under reduced-motion (Lenis `lerp: 1` / `smooth: false`, or skip it).

### 6.7 Core Web Vitals impact

- **CLS:** `transform`-based motion does not shift layout (CLS-safe); animating `margin`/`width`/`top` causes shift. web.dev: animating layout-affecting properties roughly doubles the rate of poor CLS. Reserve space with `aspect-ratio`, `contain-intrinsic-size`, `tabular-nums`.
- **LCP:** do not let heavy animation JS init block or delay the largest element; lazy-load offscreen WebGL.
- **INP / long tasks:** good INP is ≤ 200ms. Per-frame JS and big synchronous handlers create long tasks that delay input; keep animation on the compositor (CSS transitions/animations keep running even while JS is busy, protecting responsiveness). ([web.dev animations guide](https://web.dev/articles/animations-guide))
- **`content-visibility: auto`:** skips render of offscreen content until near-viewport (web.dev measured ~7x render-time drop in their demo). Pair with `contain-intrinsic-size` so collapsed sections do not cause scrollbar jumps/CLS. ([web.dev content-visibility](https://web.dev/articles/content-visibility))

```css
.section { content-visibility: auto; contain-intrinsic-size: 0 1000px; }
```

---

## 7. Anatomy of famous effects

### 7.1 Stripe-style animated gradient hero

The single most-recreated effect. Stripe did NOT use Three.js: they wrote a tiny custom WebGL layer they call **minigl** plus a `Gradient` class (~10KB, ~800 lines). The open-source `whatamesh` reproduces it; Codrops has a Three.js recreation. ([Kevin Hufnagl](https://kevinhufnagl.com/how-to-stripe-website-gradient-effect/); [bram.us](https://www.bram.us/2021/10/13/how-to-create-the-stripe-website-gradient-effect/); [Codrops lava-lamp gradient](https://tympanus.net/codrops/2022/09/26/how-to-recreate-stripes-lava-lamp-gradient-with-three-js/))

**Step by step:**

1. **A full-viewport `<canvas>`** holds a single large `PlaneGeometry` heavily subdivided into a grid of vertices (the more segments, the smoother the wave).
2. **Vertex shader displaces the mesh.** Each vertex's `z` (or `y`) is offset by layered **Simplex noise** (Fractal Brownian Motion: several octaves of noise summed at different frequencies/amplitudes) sampled over a `uTime` uniform. This is what makes the surface undulate like a lava lamp.
3. **Fragment shader paints the colors.** 3 to 4 gradient color stops (defined as CSS custom properties like `--gradientColorZero`) are blended across the mesh using **blend modes** (multiply / screen / overlay) implemented in-shader, so colors interact rather than just cross-fade. Noise drives where each color dominates.
4. **The animation loop** increments `uTime` each frame and re-renders, so the noise field flows continuously. Init is a one-liner: `new Gradient().initGradient('#gradient-canvas')`.
5. **The famous diagonal edge is a CSS trick, not geometry:** the canvas is a plain rectangle, but its container uses `transform: skewY(-12deg); overflow: hidden`.
6. **Perf pattern worth copying:** Stripe attaches a scroll observer that **pauses the WebGL loop when the canvas scrolls offscreen.**

**CSS-only approximation (when WebGL is overkill):** animate a `conic-gradient` / blurred radial-gradient blobs with slow `@keyframes` and a `filter: blur()`. Much cheaper, less organic.

### 7.2 Apple-style sticky scroll product showcase (canvas image sequence)

Apple's product pages "scrub a video" that is actually a **sequence of pre-rendered images drawn to a canvas, indexed by scroll position.** ([CSS-Tricks](https://css-tricks.com/lets-make-one-of-those-fancy-scrolling-animations-used-on-apple-product-pages/); [GSAP imageSequenceScrub helper](https://gsap.com/docs/v3/HelperFunctions/helpers/imageSequenceScrub/))

**Step by step:**

1. **Export ~100 to 300 numbered frames** (PNG/JPG/WebP) and **preload them into an array** of `Image` objects so no frame fetches mid-scroll.
2. **Draw to a `<canvas>`** with `ctx.drawImage(images[frame], 0, 0)`.
3. **Drive a frame index with GSAP ScrollTrigger scrub.** Tween a `{ frame: 0 }` object to the last index with `ease: "none"`; on each `onUpdate`, round and draw that frame. `pin` the canvas so the user scrolls through the whole sequence in place.

```javascript
const frames = { frame: 0 };
const images = urls.map((u) => { const i = new Image(); i.src = u; return i; });
const ctx = canvas.getContext("2d");
const render = () => ctx.drawImage(images[Math.round(frames.frame)], 0, 0);
images[0].onload = render;

gsap.to(frames, {
  frame: images.length - 1,
  ease: "none",
  onUpdate: render,
  scrollTrigger: { trigger: ".showcase", start: "top top", end: "+=3000", pin: true, scrub: true },
});
```

GSAP ships this as the `imageSequenceScrub` helper. **Perf:** WebP frames + preload; cap frame count; size the canvas to display resolution; this is heavy on memory (every frame decoded), so it suits one hero, not many.

The closely-related **sticky scroll showcase** (text scrolls past a pinned visual that swaps as you reach each step) uses `position: sticky` (or ScrollTrigger `pin`) on the visual, plus IntersectionObserver / ScrollTrigger callbacks that swap the active image/state per text block. ([Codrops, sticky sections](https://tympanus.net/codrops/2024/01/31/on-scroll-animation-ideas-for-sticky-sections/))

### 7.3 Text-mask line reveal (Linear/agency style)

The "lines rise into view from behind an invisible edge" headline.

**Step by step:**

1. **Split the heading into lines** with SplitText (`type: "lines"`). Each line becomes its own element.
2. **Mask each line:** wrap it in an `overflow: hidden` clip box (SplitText 3.13+ does this with `mask: "lines"`). The box is exactly one line tall, so anything below it is clipped.
3. **Animate the inner line from `yPercent: 100` to `0`** with a per-line `stagger` (~0.1s) and a strong ease-out (`power3.out` / `expo.out`). Each line slides up out of its mask, one after another.
4. **Trigger on scroll** by attaching a ScrollTrigger (`start: "top 80%"`, `toggleActions: "play none none reverse"`) so it fires when the heading enters the viewport.
5. **Cleanup:** `split.revert()` and re-split on resize / after web fonts load, or line breaks (and thus masks) go stale.

(Code in [section 4.4](#44-text-reveal--split-text-animations).)

---

## 8. Library usage by high-fidelity sites

Per the brief, this cites published writeups and library showcases, not live inspection.

- **GSAP is the near-default for award sites.** GSAP's own positioning lists Apple, Google, EA, Disney as users and claims "the majority of Awwwards-winning projects since 2020," ~11M+ sites. The "Made With GSAP" and `gsap.com/showcase` galleries aggregate top-agency work, and GSAP shipped a **native Webflow integration** (SplitText, Staggers, ScrollTrigger in the visual canvas) in 2025, entrenching the Webflow + GSAP stack. If an Awwwards-caliber site has scroll-driven or timeline animation, GSAP is the safe bet. ([GSAP showcase](https://gsap.com/showcase/))
- **Lenis (darkroom.engineering) is the smooth-scroll standard.** Writeups note it "quietly runs on roughly half of the Awwwards homepage" and on Rockstar's GTA VI teaser. It is built to sync (not fight) the browser, driving WebGL scroll scenes, ScrollTrigger, and parallax off one loop. ([Lenis repo](https://github.com/darkroomengineering/lenis); [Lenis showcase](https://lenis.darkroom.engineering/showcase))
- **Stripe = bespoke WebGL.** Custom `minigl` + `Gradient` class with in-shader Simplex-noise FBM and blend modes, not an off-the-shelf lib (see 7.1).
- **Common stack patterns:**
  - **GSAP + Lenis + Three.js (or R3F):** the dominant Awwwards/creative-studio stack for scroll-driven WebGL (darkroom.engineering, Active Theory-style work). Lenis for smooth scroll, GSAP/ScrollTrigger for timelines, Three/R3F for the GL layer, all on one rAF tick.
  - **Webflow + GSAP:** low-code agency sites, now first-party via the 2025 integration.
  - **Next.js + Framer Motion (`motion`):** the React/product-site default (Linear/Vercel-style marketing); declarative spring/gesture/layout animation, often plus Lenis's React package.
  - **Framer (the builder):** used directly for high-polish marketing sites; Lenis available as a Framer package.
  - **Bespoke WebGL (custom shaders):** reserved for hero/brand moments where library overhead does not fit (Stripe gradient, Igloo Inc / Active Theory immersive scenes); typically lazy-loaded and viewport-gated.

**Takeaway for the skill:** the portable, Rails-friendly default that covers ~80% of "awwwards-grade" output is **GSAP (+ ScrollTrigger, SplitText, Flip) + Lenis + Tailwind**, escalating to **Three.js / R3F** only for true WebGL hero moments and to **Framer Motion** when the project is already React.

---

## Sources

URLs actually read or fetched during this research. Inline citations above point to the relevant one.

Scroll and smooth scroll:
- GSAP ScrollTrigger docs: https://gsap.com/docs/v3/Plugins/ScrollTrigger/
- GSAP seamlessLoop / horizontalLoop helper: https://gsap.com/docs/v3/HelperFunctions/helpers/seamlessLoop/
- GSAP imageSequenceScrub helper: https://gsap.com/docs/v3/HelperFunctions/helpers/imageSequenceScrub/
- Lenis (darkroom.engineering) repo + GSAP integration: https://github.com/darkroomengineering/lenis
- Lenis showcase: https://lenis.darkroom.engineering/showcase
- MDN, CSS scroll-driven animations: https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations
- MDN, animation-timeline: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation-timeline
- Josh W. Comeau, Scroll-Driven Animations: https://www.joshwcomeau.com/animation/scroll-driven-animations/
- dev.to, Complex scroll-driven animations with pure CSS in 2026: https://dev.to/nickbenksim/creating-complex-scroll-driven-animations-with-pure-css-in-2026-17l

WebGL / 3D:
- Codrops, Recreate Stripe's lava lamp gradient with Three.js: https://tympanus.net/codrops/2022/09/26/how-to-recreate-stripes-lava-lamp-gradient-with-three-js/
- Codrops, WebGL distortion hover effects: https://tympanus.net/codrops/2018/04/10/webgl-distortion-hover-effects/
- CSS-Tricks, WebGL effects with curtains.js: https://css-tricks.com/creating-webgl-effects-with-curtainsjs/
- drei shaderMaterial docs: https://drei.docs.pmnd.rs/shaders/shader-material
- Maxime Heckel, The Study of Shaders with React Three Fiber: https://blog.maximeheckel.com/posts/the-study-of-shaders-with-react-three-fiber/

Transitions / text:
- MDN, View Transition API: https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API
- GSAP Flip plugin docs: https://gsap.com/docs/v3/Plugins/Flip/
- GSAP SplitText docs: https://gsap.com/docs/v3/Plugins/SplitText/
- Codrops, 7 must-know GSAP tips: https://tympanus.net/codrops/2025/09/03/7-must-know-gsap-animation-tips-for-creative-developers/

Micro-interactions / perf / anatomy:
- olivierlarose, Magnetic Button: https://blog.olivierlarose.com/tutorials/magnetic-button
- olivierlarose, Blend Mode Cursor: https://blog.olivierlarose.com/tutorials/blend-mode-cursor
- GSAP gsap.quickTo() docs: https://gsap.com/docs/v3/GSAP/gsap.quickTo()/
- GSAP gsap.matchMedia() docs: https://gsap.com/docs/v3/GSAP/gsap.matchMedia()/
- CSS-Tricks, The Gooey Effect: https://css-tricks.com/gooey-effect/
- web.dev, Animations guide: https://web.dev/articles/animations-guide
- web.dev, content-visibility: https://web.dev/articles/content-visibility
- Smashing, Respecting Users' Motion Preferences: https://www.smashingmagazine.com/2021/10/respecting-users-motion-preferences/
- CSS-Tricks, Apple-style scroll canvas animations: https://css-tricks.com/lets-make-one-of-those-fancy-scrolling-animations-used-on-apple-product-pages/
- Codrops, On-scroll animation ideas for sticky sections: https://tympanus.net/codrops/2024/01/31/on-scroll-animation-ideas-for-sticky-sections/
- Kevin Hufnagl, Stripe gradient effect: https://kevinhufnagl.com/how-to-stripe-website-gradient-effect/
- bram.us, How to create the Stripe gradient effect: https://www.bram.us/2021/10/13/how-to-create-the-stripe-website-gradient-effect/

Library usage:
- GSAP showcase: https://gsap.com/showcase/
- Made With GSAP: https://madewithgsap.com/showcase
