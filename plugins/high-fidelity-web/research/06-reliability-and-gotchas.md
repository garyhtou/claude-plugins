# 06. Reliability and Gotchas (the failure modes)

Source material for `references/reliability-and-gotchas.md`. This is the HOW-IT-BREAKS
companion to the techniques doc: the production failure modes for scroll, reveal,
animation, layout, and interaction that separate a polished demo from a shipped
site, with current (2025-2026) recommended fixes and citations. Most of these were
hit while building the "Zoomies" example site; the research below confirms and
generalizes the fixes that shipped.

Grounded in GSAP official docs and forums, MDN, web.dev, WCAG 2.2 Understanding
docs, Floating UI, CSS-Tricks, Josh Comeau, and the Chromium/Chrome developer docs.

---

## Part A. Scroll-driven reveals and pinned scroll

### A.1 Decision rule

- One-shot reveals (fade/slide in once, then done): use IntersectionObserver, or
  native CSS `view()` where you can accept Firefox degradation. Do not reach for
  ScrollTrigger.
- Scrubbing or pinning (progress tied to scroll, sticky scenes, parallax tracking
  the scrollbar): use GSAP ScrollTrigger. This is the one thing IntersectionObserver
  cannot do.

This split is itself the fix for the "invisible until reload" bug: ScrollTrigger
start/end positions are computed once at creation and can go stale; IntersectionObserver
re-evaluates live and cannot.

### A.2 The "invisible until reload" bug

`gsap.from(el, {opacity:0, y:40, scrollTrigger:{...}})` leaves the element invisible
when you scroll down to it, but works if you reload with it already in view. Two
compounding causes:

1. Stale start/end positions. ScrollTrigger caches pixel positions at creation. If
   layout changes after (a pinned section above adds scroll distance, a JS-sized
   element resizes, late web fonts reflow text), the trigger fires at the wrong
   position, often one already passed, so it never plays on the way down.
2. Cached `.from()` start values + `immediateRender`. `.from()` defaults to
   `immediateRender: true`, applying and caching the hidden state immediately; a
   later tween or stale trigger can leave the element stuck hidden.

Fixes in order of preference:
- A. IntersectionObserver for one-shot reveals (most robust): no cached positions,
  re-evaluates live, structurally cannot go stale. Toggle a class, let CSS/GSAP do
  the motion; `unobserve` after the first reveal.
- B. If keeping ScrollTrigger: `ScrollTrigger.refresh()` after layout settles.
  `document.fonts.ready.then(...)` (fonts reflow text), `window` load (late/sized
  images), and `refresh(true)` safe mode (waits ~1 rAF when you mutate the DOM in a
  callback and the size is not painted yet). GSAP auto-refreshes on resize and a few
  times after load but does not know about your AJAX/fonts/JS-sized elements.
- C. Self-healing positions: function-based start/end + `invalidateOnRefresh: true`,
  and `immediateRender: false` (the canonical fix for a `.from()` reveal that stays
  hidden).
- D. Create triggers in DOM order, or set `refreshPriority: 1` on upstream pins, so a
  pin's added scroll distance is accounted for by later triggers.

### A.3 Pinned/scrubbed scenes

Pinning wraps the element in a `pin-spacer` div (fixed size; element goes
`position: fixed`). Gotchas flow from that wrapper:
- pin-spacer breaks `>` child / `:nth-child()` selectors, and a pinned flex/grid
  item is no longer a direct child of its container (flex/grid misbehaves). Fix: pin
  an inner wrapper or the container, not a flex/grid item directly.
- `pinSpacing`: default true reserves space below; false overlaps the next section
  (auto-false inside flex); "margin" switches padding to margin.
- `anticipatePin: 1` pins slightly early so it does not flash/lag on fast scroll.
- `pinReparent: true` physically moves the element (only for certain transformed
  ancestors) and breaks nesting-dependent CSS. Use sparingly.
- `markers: true` to debug where stale start/end land.
- Mobile dynamic viewport (URL bar show/hide) re-fires refresh and can jump a pinned
  scene; degrade to a non-pinned variant via `gsap.matchMedia`.

### A.4 The reload-jumps-into-the-pinned-scene bug

Reload near/at the bottom and you get yanked into a pinned section. Cause: the
browser restores the previous scroll position on reload before ScrollTrigger has
built the pin-spacers, so it restores a tall offset against a not-yet-expanded
document and lands mid-pin. Fix: `history.scrollRestoration = "manual"` set before
ScrollTrigger initializes (ScrollTrigger records scroll memory early), plus
`window.scrollTo(0,0)` on load before building triggers. In SPAs,
`ScrollTrigger.clearScrollMemory("manual")` clears recorded positions so none are
restored after `refresh()`.

### A.5 prefers-reduced-motion for scroll scenes

Pinning and scrubbing are the parts that trigger vestibular discomfort, so the
reduced branch should remove them entirely, not just shorten durations. Show
everything in normal flow (optionally one instant IntersectionObserver fade). Use
`gsap.matchMedia()` with `motionOK`/`reduced` conditions so GSAP reverts the
wrong-branch animations automatically when the OS setting changes live. Mirror in
CSS with `@media (prefers-reduced-motion: reduce)`.

### A.6 Native CSS scroll-driven animations (2026)

`animation-timeline: view()` (element entering/exiting viewport) and `scroll()`
(container progress) drive `@keyframes` by scroll with zero JS. Browser owns the
timeline, so no cached positions to go stale (the A.2 bug does not occur) and it
runs off the main thread. Support ~85% (Chrome/Edge 115+, Safari 18/26+); Firefox
still behind a flag, so wrap in `@supports (animation-timeline: view())` with an
IntersectionObserver fallback and `@media (prefers-reduced-motion: no-preference)`.
Use for cosmetic reveals/parallax; keep ScrollTrigger for true pinned/scrubbed
choreography.

---

## Part B. Animation performance and correctness

### B.1 rAF freezes in background tabs and offscreen; pause deliberately

Browsers stop firing `requestAnimationFrame` callbacks in backgrounded/hidden tabs
(and hidden iframes) to save battery; `setTimeout`/`setInterval` are throttled too.
Failure mode: logic that assumes rAF keeps ticking (counting frames, or starting a
transition and expecting it to finish) can freeze mid-state until the user returns.
Offscreen-but-visible content (scrolled out of view) is not covered by tab-visibility
throttling at all and keeps burning CPU/GPU.

Pattern: gate a single loop on both signals (tab `visibilitychange`/`document.hidden`
and element offscreen via IntersectionObserver), and advance by a `performance.now()`
delta, never by frame count, so pause/resume cannot desync. For CSS/WAAPI, the
offscreen equivalent is toggling `animationPlayState`.

Testing/automation implication: rAF-driven animation freezes in backgrounded and
headless/automation contexts, so a CI/automation screenshot of in-progress rAF
motion captures frame 0 or a frozen mid-state, not the settled result. Assert on the
settled/final state (drive to completion, or read computed state directly, or use a
reduced/instant mode).

### B.2 Staggered reveals that move/scale create misleading intermediate states

A stagger animates siblings on a time offset. If the animated property changes size
or position (`scale`, `translateY`, `height`, `width`, `clip`), then every
mid-animation frame has siblings at genuinely different sizes/positions, which reads
as a layout bug (uneven grid rows, a bar chart "not filled," cards with misaligned
tops) even though the settled layout is correct. This is a correctness/perception
issue, not just perf: a paused tab, slow device, reduced motion, or CI screenshot can
surface that misleading frame as the apparent final state (ties to B.1).

Fix: for grids and side-by-side rows, prefer opacity-only reveals (fade in place);
every item occupies its final box from frame zero. If you must move, keep it subtle
and uniform (small uniform `translateY` ~8 to 16px or `scale` >= 0.96, transform
only), never a per-item size/position stagger. Reserve the final box before animating
(hide with `opacity: 0` + transform, not `display:none`/`height:0`).

Tie-in: web.dev restricts animation to `transform`/`opacity` to stay on the
compositor; animating `width`/`height`/`top`/`left`/`margin` triggers layout/paint
(web.dev's demo shows ~50% dropped frames animating `top`/`left` vs ~1% with
`transform`). At 60fps you have ~16.6ms/frame (~10ms after overhead). `will-change`
only reactively, not preemptively.

### B.3 Canvas/WebGL robustness

- Detect availability and fall back: `getContext("webgl2") || getContext("webgl")`
  can return null; show a CSS/static fallback. Honor `prefers-reduced-motion` and
  optionally `deviceMemory`/`hardwareConcurrency`. Probe limits with `getParameter`;
  make extensions optional via `getExtension`.
- Cap devicePixelRatio at ~2 when sizing the drawing buffer and round to integers
  (backing-store cost scales with DPR squared; DPR-3 uncapped = 9x the pixels).
  Non-integer DPR (Windows scaling, zoom) can cause moire; for pixel-perfect output
  use `ResizeObserver` with `device-pixel-content-box`. "Cap at 2 and round" is the
  pragmatic default.
- Pause the render loop offscreen and when hidden (B.1): the biggest battery/thermal
  win for a WebGL hero.
- `preserveDrawingBuffer: false` (default) is faster/lighter; set true only if you
  read pixels after the frame (`toDataURL`/`readPixels`).
- Handle context loss: listen for `webglcontextlost`/`webglcontextrestored` and
  re-init resources. A well-formed page should only see `OUT_OF_MEMORY` and
  `CONTEXT_LOST`.
- You cannot trust headless/CI screenshots for WebGL output. Headless machines lack a
  real GPU; Chrome historically fell back to SwiftShader (software rendering, looks
  and times differently). As of Chrome ~137 (late 2025) the automatic SwiftShader
  fallback was deprecated/removed (binary size + JIT security), so WebGL context
  creation now fails outright in many headless setups that used to "work." Validate
  on a real GPU; in CI assert that the fallback path renders, not the 3D pixels.
  Docker gotcha: SwiftShader is memory-hungry; default 64MB `/dev/shm` crashes WebGL,
  use `--shm-size=1gb` or `--disable-dev-shm-usage`.

### B.4 CSS/WAAPI off the main thread

Compositor-animatable properties (`transform`, `opacity`, `filter`, `clip-path`)
animated via CSS or the Web Animations API can run off the main thread and stay
smooth even when the main thread is busy. rAF-based JS updates the same properties on
the main thread and is vulnerable to jank when it is blocked. Default: CSS/WAAPI for
property-tween motion; rAF only for genuine per-frame JS (canvas/WebGL, scroll-linked
physics). WAAPI/CSS only stay off-thread while animating compositor-friendly
properties.

---

## Part C. Layout stability and interaction details

### C.1 Preventing layout shift / jitter from dynamic content

CLS target < 0.1. A shift happens whenever a visible element changes position
between two frames without a user-initiated trigger. Universal fix: reserve the space
before the content arrives.
- Reserve space for runtime-changing content (text rewrapping to a different line
  count, count-up numbers, crossfading content): `min-height`, a line cap,
  `aspect-ratio`, or `content-visibility` + `contain-intrinsic-size: auto N` (uses
  your estimate before first render, then remembers the real measured size).
- Tabular numbers: `font-variant-numeric: tabular-nums` for any changing digits
  (counters, clocks, prices). Only works if the font ships `tnum` glyphs; verify with
  the actual font.
- Pitfall: centered content re-centers and jumps. `place-items: center` recomputes
  the center on every inner height change (one-line to three-line swap jumps the
  block). Fix: pin the inner element's height (`min-height` >= tallest state) and
  center within that fixed box.
- Pitfall: shrink-to-content width jumps when centered. An element at `max-content`
  inside a centered container changes width as text changes, and both centered edges
  move. Fix: a stable explicit width, e.g. `width: min(680px, 100%)`.
- Animate `transform`/`opacity` only; layout properties trigger reflow and count
  toward CLS.

### C.2 Tooltip / overlay / popover positioning

- Never render a cursor tooltip directly under the cursor: it covers the target and
  flickers as the pointer enters its own box. Offset above or beside (frameworks
  cluster around ~10 to 16px). System cursor size is not exposed to CSS/JS, so bias
  the offset generous (12 to 16px) and prefer above the pointer (cursors extend
  down-right from the hotspot).
- Always handle viewport collisions: flip to the other side and shift along the edge.
- 2026 toolbox: Floating UI (JS engine, `computePosition` + `offset`/`flip`/`shift`/
  `arrow`/`autoUpdate` middleware, supports virtual reference elements) is the de
  facto standard. Popover API (top layer, light-dismiss, Baseline since Jan 2025)
  handles display/dismiss/stacking but does not position. CSS Anchor Positioning
  (`anchor()`, `position-area`, `position-try-fallbacks`) is newly interoperable
  (Chrome/Edge 125+, Firefox 147+, Safari 26+) for static element-anchored cases; use
  `@supports` + fallback. Naming gotcha: Chrome 125 shipped `inset-area`/
  `position-try-options`, renamed in 129 to `position-area`/`position-try-fallbacks`.
- Cursor-following tooltip: CSS anchor positioning cannot follow a moving point, so
  use Floating UI with a virtual element (0x0 rect at the pointer), middleware order
  `offset` then `flip` then `shift`, `position: fixed`, and coalesce `mousemove` into
  one `requestAnimationFrame` tick. `autoUpdate` is for element-anchored tooltips, not
  cursor-driven ones.

### C.3 Interactive hit-target sizing

- Two thresholds, do not conflate: WCAG 2.5.8 Target Size (Minimum), Level AA, is
  24x24 CSS px (with a spacing exception: a 24px circle centered on the target must
  not intersect another's). Apple HIG recommends 44x44 pt. Use 24 as the a11y floor,
  44 for touch comfort.
- The hit target is the interactive area, not the visible graphic. A 16px icon is
  fine if its clickable box is >= 24 (>= 44 for touch). Expand with transparent
  padding (`content-box`), do not enlarge the visual.
- The `gap` gotcha: a CSS grid/flex `gap` is dead, unhittable space. For a dense grid
  of small interactive cells (color picker, calendar heatmap, seat map), set `gap: 0`,
  recreate the visual spacing with transparent padding, and paint the visual only
  inside the content box with `background-clip: content-box`. The whole contiguous
  tile is hittable; the visual swatch stays small. (Note: `background-clip: content-box`
  clips background only; if the visual is a child element or `::before`, size/center
  that child inside the padded box instead.)

---

## Sources

GSAP:
- ScrollTrigger - https://gsap.com/docs/v3/Plugins/ScrollTrigger/
- ScrollTrigger.refresh() - https://gsap.com/docs/v3/Plugins/ScrollTrigger/static.refresh()/
- gsap.matchMedia() - https://gsap.com/docs/v3/GSAP/gsap.matchMedia()/
- ScrollTrigger tips and mistakes - https://gsap.com/resources/st-mistakes/
- Forums: .from() only triggers when scrolling up - https://gsap.com/community/forums/topic/38219-from-in-scrolltrigger-only-triggers-when-scrolling-up/
- Forums: ScrollTrigger vs IntersectionObserver - https://gsap.com/community/forums/topic/32694-scrolltrigger-vs-intersectionobeserver/
- Forums: matchMedia + prefers-reduced-motion - https://gsap.com/community/forums/topic/27141-scrolltriggermatchmedia-and-prefers-reduced-motion/
- Forums: ignore history.scrollRestoration manual - https://gsap.com/community/forums/topic/34601-scrolltrigger-ignore-historyscrollrestoration-manual/
- Forums: why display:flex breaks pinning - https://gsap.com/community/forums/topic/39261-why-display-flex-breaks-the-scrolltrigger-pinning-and-how-to-avoid/
- GitHub #461 (existing spacer element) - https://github.com/greensock/GSAP/issues/461

MDN:
- requestAnimationFrame - https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame
- Page Visibility API - https://developer.mozilla.org/en-US/docs/Web/API/Page_Visibility_API
- CSS and JavaScript animation performance - https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/CSS_JavaScript_animation_performance
- WebGL best practices - https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices
- Scroll-driven animations; animation-timeline - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations
- History.scrollRestoration - https://developer.mozilla.org/en-US/docs/Web/API/History/scrollRestoration
- contain-intrinsic-size; content-visibility; font-variant-numeric; background-clip - https://developer.mozilla.org/en-US/docs/Web/CSS/contain-intrinsic-size
- Popover API; position-try-fallbacks; @position-try - https://developer.mozilla.org/en-US/docs/Web/API/Popover_API

web.dev:
- High-performance CSS animations - https://web.dev/articles/animations-guide
- Animations and performance - https://web.dev/articles/animations-and-performance
- Cumulative Layout Shift; Optimize CLS - https://web.dev/articles/cls ; https://web.dev/articles/optimize-cls
- content-visibility - https://web.dev/articles/content-visibility
- Anchor positioning (Learn CSS) - https://web.dev/learn/css/anchor-positioning

Chrome/Chromium:
- SwiftShader brings software 3D rendering to Chrome - https://developer.chrome.com/blog/swiftshader-brings-software-3d-rendering-to-chrome
- Remove SwiftShader as a WebGL fallback unless explicitly requested - https://issues.chromium.org/issues/40277080
- Using Chromium with SwiftShader - https://chromium.googlesource.com/chromium/src/+/main/docs/gpu/swiftshader.md

Other:
- caniuse: animation-timeline scroll() - https://caniuse.com/mdn-css_properties_animation-timeline_scroll
- CSS-Tricks: An Overview of Scroll Technologies - https://css-tricks.com/an-overview-of-scroll-technologies/
- Josh W. Comeau: Scroll-Driven Animations - https://www.joshwcomeau.com/animation/scroll-driven-animations/
- Motion.dev: Web Animation Performance Tier List - https://motion.dev/magazine/web-animation-performance-tier-list
- Emil Kowalski: 7 practical animation tips - https://emilkowal.ski/ui/7-practical-animation-tips
- W3C WAI: Understanding SC 2.5.8 Target Size (Minimum) - https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- Floating UI: tutorial, virtual elements, flip, tooltip - https://floating-ui.com/docs/tutorial
- dev.to: GSAP ScrollTrigger pin nearly broke my portfolio - https://dev.to/xuanhai0913/gsap-scrolltrigger-pin-true-nearly-broke-my-portfolio-heres-what-i-learned-28i7
- dev.to: complex scroll-driven CSS in 2026 - https://dev.to/nickbenksim/creating-complex-scroll-driven-animations-with-pure-css-in-2026-17l
