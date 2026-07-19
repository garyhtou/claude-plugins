# Reliability and Gotchas

Reference for the `high-fidelity-web` skill. The premium tier lives or dies on
whether the motion actually works: reveals that fire every time, scroll scenes
that do not jump, animations that do not freeze or drain battery, layouts that do
not jitter, interactions that land where you point. This file is the catalog of
failure modes that separate a polished demo from a shipped site, each with the
recommended fix. Most are invisible until QA or a real user hits them, so treat
section 10 as a gate. Load it in Phase 5 to 7 (build, polish, QA).

Many of these were learned the hard way building the example site (Zoomies), and
the fix is noted where it shipped there.

---

## 1. Scroll-driven reveals: pick the right trigger

**Decision rule.** For a one-shot reveal (fade or slide in once, then done), use
**IntersectionObserver** or native CSS **`view()`**. Reserve **GSAP ScrollTrigger**
for what only it can do: scrubbing progress to the scrollbar and pinning sticky
scenes. Using ScrollTrigger for plain reveals is the single most common cause of
the bug below.

### The "invisible until reload" bug

Symptom: `gsap.from(el, {opacity: 0, y: 40, scrollTrigger: {...}})` leaves the
element invisible when you scroll down to it, but it appears fine if you reload
with it already in view. Two compounding causes:

- **Stale start/end positions.** ScrollTrigger computes pixel positions once at
  creation and caches them. If layout changes afterward (a pinned section above
  adds scroll distance, a JS-sized element resizes, web fonts reflow text), the
  trigger fires at the wrong scroll position, often one you have already passed,
  so it never plays on the way down.
- **Cached `.from()` start values + `immediateRender`.** `.from()` defaults to
  `immediateRender: true`, so GSAP applies the hidden state (opacity 0)
  immediately and caches it. A later tween or a mistimed trigger can then leave
  the element stuck hidden with nothing to reveal it.

Fixes, in order of preference:

**A. Use IntersectionObserver for one-shot reveals (most robust).** No cached
positions; it re-evaluates live, so it structurally cannot go stale, even with a
pinned section on the page. Pre-hide, reveal on enter, then stop observing. This
is what the example uses for every one-shot reveal (heatmap, timeline,
leaderboard, rings).

```js
const io = new IntersectionObserver((entries) => {
  for (const e of entries) {
    if (e.isIntersecting) {
      e.target.classList.add("is-visible"); // CSS transition does the motion
      io.unobserve(e.target);               // one-shot
    }
  }
}, { threshold: 0.15, rootMargin: "0px 0px -10% 0px" });
document.querySelectorAll("[data-reveal]").forEach((el) => io.observe(el));
```

```css
[data-reveal] { opacity: 0; transform: translateY(40px);
  transition: opacity .6s, transform .6s; }
[data-reveal].is-visible { opacity: 1; transform: none; }
@media (prefers-reduced-motion: reduce) {
  [data-reveal] { opacity: 1; transform: none; transition: none; }
}
```

To drive GSAP from the observer instead of CSS, pre-hide with
`gsap.set(el, {opacity: 0})` and run `gsap.to(...)` in the `isIntersecting` branch.

**B. If you keep ScrollTrigger for reveals, refresh after layout settles.**
`refresh()` recomputes every trigger against the current DOM. GSAP auto-refreshes
on resize and a few times after load, but it does not know about your fonts,
AJAX, or JS-sized elements.

```js
document.fonts.ready.then(() => ScrollTrigger.refresh());      // fonts reflow text
window.addEventListener("load", () => ScrollTrigger.refresh()); // late/sized images
// After mutating the DOM in a callback (size not painted yet), use safe mode:
ScrollTrigger.refresh(true); // waits ~1 rAF before measuring
```

**C. Self-healing positions.** When start/end depend on measurements, compute them
in functions and add `invalidateOnRefresh: true` so they (and `.from()`'s cached
start values) recompute on every refresh. `immediateRender: false` is the
canonical fix for a `.from()` reveal that stays hidden.

```js
gsap.from(".panel", {
  opacity: 0, y: 60, immediateRender: false,
  scrollTrigger: {
    trigger: ".panel",
    start: () => `top ${window.innerHeight * 0.8}px`,
    invalidateOnRefresh: true,
    toggleActions: "play none none none",
  },
});
```

**D. Create triggers in DOM order**, or give upstream pins `refreshPriority: 1`,
so a pin's added scroll distance is accounted for by later triggers.

---

## 2. Pinned and scrubbed scenes

Pinning wraps the pinned element in a `pin-spacer` div (fixed size, holds the
layout open while the element goes `position: fixed`). Most gotchas flow from that
inserted wrapper.

- **pin-spacer breaks selectors and flex/grid.** The new ancestor breaks `>`
  child and `:nth-child()` selectors, and a pinned flex/grid item is no longer a
  direct child of its container. Fix: pin an inner wrapper or the container, not a
  flex/grid item directly; rewrite affected selectors.
- **`pinSpacing`**: default `true` reserves space below; `false` overlaps the next
  section (auto-false inside flex); `"margin"` switches the padding to margin.
- **`anticipatePin: 1`** pins slightly early so it does not flash/lag on fast
  scroll.
- **`pinReparent`** physically moves the element in the DOM (only needed under
  certain transformed ancestors) and breaks nesting-dependent CSS. Use sparingly.
- **`markers: true`** shows exactly where stale start/end land while debugging.
- **Mobile dynamic viewport** (URL bar show/hide) re-fires refresh and can jump a
  pinned scene; degrade to a non-pinned variant on small screens (section 3).

### The reload-jumps-into-the-pinned-scene bug

Symptom: reload near or at the bottom of the page and you get yanked into a pinned
section. Cause: the browser restores the previous scroll position on reload
*before* ScrollTrigger has built the pin-spacers, so it restores a tall offset
against a not-yet-expanded document and lands you mid-pin. Fix: take scroll
restoration away from the browser, and do it before ScrollTrigger initializes
(ScrollTrigger records scroll memory early). The example ships exactly this.

```js
if ("scrollRestoration" in history) history.scrollRestoration = "manual";
window.addEventListener("load", () => { window.scrollTo(0, 0); /* then build triggers */ });
```

In SPAs/route changes, `ScrollTrigger.clearScrollMemory("manual")` clears the
positions ScrollTrigger recorded so none get restored after a `refresh()`.

---

## 3. prefers-reduced-motion for scroll scenes

Pinning and scrubbing are exactly the parts that trigger vestibular discomfort, so
the reduced-motion branch should **remove them entirely, not just shorten
durations**. Show everything in normal flow (optionally one instant
IntersectionObserver fade). Use `gsap.matchMedia()` so GSAP reverts the
wrong-branch animations automatically when the OS setting changes live.

```js
const mm = gsap.matchMedia();
mm.add({ motionOK: "(prefers-reduced-motion: no-preference)",
         reduced:  "(prefers-reduced-motion: reduce)" }, (ctx) => {
  if (ctx.conditions.motionOK) {
    gsap.timeline({ scrollTrigger: { trigger: ".scene", start: "top top",
      end: "+=2000", pin: true, scrub: 1, anticipatePin: 1, invalidateOnRefresh: true } })
      .from(".scene-a", { autoAlpha: 0, y: 80 })
      .from(".scene-b", { autoAlpha: 0, y: 80 });
  }
  if (ctx.conditions.reduced) {
    gsap.set(".scene-a, .scene-b", { autoAlpha: 1, y: 0, clearProps: "transform" });
  }
});
```

Mirror this in CSS for any non-GSAP transitions with
`@media (prefers-reduced-motion: reduce)`.

---

## 4. Animation lifecycle: pause when not visible

rAF callbacks stop firing in background (hidden) tabs to save battery, and
offscreen-but-visible content (scrolled out of view on a long page) keeps burning
CPU/GPU unless you stop it. Two implications:

- **Pause your loops on both signals**: tab hidden (`visibilitychange` /
  `document.hidden`) and element offscreen (IntersectionObserver). Always advance
  by a `performance.now()` delta, never by frame count, so a pause/resume cannot
  desync time-based state.

```js
let rafId = null, lastT = 0, tabVisible = !document.hidden, onScreen = false;
function frame(now) { const dt = now - lastT; lastT = now; update(dt); render();
  rafId = requestAnimationFrame(frame); }
function start() { if (rafId == null) { lastT = performance.now(); rafId = requestAnimationFrame(frame); } }
function stop() { if (rafId != null) cancelAnimationFrame(rafId); rafId = null; }
const sync = () => (tabVisible && onScreen) ? start() : stop();
document.addEventListener("visibilitychange", () => { tabVisible = !document.hidden; sync(); });
new IntersectionObserver(([e]) => { onScreen = e.isIntersecting; sync(); }, { threshold: 0 }).observe(canvas);
```

  For CSS/WAAPI animations the offscreen equivalent is toggling
  `el.style.animationPlayState = entry.isIntersecting ? "running" : "paused"`.

- **Do not trust mid-flight rAF state in backgrounded tabs or CI.** A backgrounded
  or headless browser freezes rAF at whatever frame it was on, so a screenshot of
  an in-progress rAF animation captures a frozen or frame-0 state, not the settled
  result. Assert on the settled/final state instead. (This bit us repeatedly
  capturing the example: animations froze in the automation tab; reduced-motion
  captures and direct state reads were the reliable check.)

Prefer **CSS/WAAPI** for transform/opacity tweens: they can run on the compositor,
off the main thread, so they stay smooth even when the main thread is busy.
Reserve rAF for true per-frame JS (canvas/WebGL, scroll-linked physics).

---

## 5. Reveal staggers: a correctness problem, not just polish

A stagger animates siblings on a time offset. If the animated property changes
**size or position** (`scale`, `translateY`, `height`, `width`), then at every
mid-animation frame the siblings are genuinely different sizes or at different
positions, which reads as a layout bug even though the settled layout is correct:

- a grid looks like it has uneven rows or misaligned card tops,
- a bar chart staggering height looks half-empty or "not filled,"
- a row of cards has tops that do not line up until the last one lands.

This is worse than cosmetic: a slow device, a paused tab, reduced motion, or a CI
screenshot can catch and surface that misleading frame as the apparent final state
(see section 4).

**Fix: for grids and side-by-side rows, fade in place (opacity only).** Every item
holds its final box from frame zero, so no frame looks broken. If you must add
motion, keep it subtle and uniform (a small uniform `translateY`, or `scale` no
smaller than ~0.96, transform only), never a per-item size/position stagger.
Reserve the final box up front (hide with `opacity: 0`, not `display: none` or
`height: 0`, which causes layout shift). We hit all three symptoms above on the
example dashboard; opacity-only reveals fixed them.

---

## 6. Canvas and WebGL robustness

- **Detect and fall back.** `canvas.getContext("webgl2") || getContext("webgl")`
  can return null; show a CSS/static fallback. Honor `prefers-reduced-motion` and
  optionally `deviceMemory`/`hardwareConcurrency` to choose the fallback on
  low-power devices. Probe limits with `getParameter`; make extensions optional
  via `getExtension`.
- **Cap devicePixelRatio at ~2** when sizing the drawing buffer, and round to
  integers; backing-store cost scales with DPR squared.

```js
const dpr = Math.min(window.devicePixelRatio || 1, 2);
canvas.width = Math.round(cssW * dpr); canvas.height = Math.round(cssH * dpr);
canvas.style.width = cssW + "px"; canvas.style.height = cssH + "px";
```

- **Pause the render loop offscreen and when the tab is hidden** (section 4). A
  WebGL hero is the single biggest battery/thermal cost on the page.
- **`preserveDrawingBuffer: false`** (the default) is faster and lighter; set it
  true only if you read pixels after the frame (`toDataURL` / `readPixels`).
- **Handle context loss**: listen for `webglcontextlost` / `webglcontextrestored`
  and re-init resources.
- **You cannot trust headless/CI screenshots for WebGL output.** Headless machines
  have no real GPU; Chrome historically fell back to SwiftShader (software
  rendering, which looks and times differently), and **as of Chrome 137 (late
  2025) that automatic fallback was removed**, so WebGL context creation now fails
  outright in many headless setups that used to "work." Validate WebGL visuals on
  a real GPU; in CI, assert that the fallback path renders, not the 3D pixels.

---

## 7. Layout stability (no jitter)

Beyond images, awwwards-tier instability comes from content that changes at
runtime. The universal fix is to reserve the space before the content arrives.

- **Reserve space for changing content.** Text that rewraps to a different line
  count, count-up numbers, crossfading content: give the container a stable size
  (`min-height`, a line cap, `aspect-ratio`, or `content-visibility` +
  `contain-intrinsic-size: auto N` for deferred sections).
- **Tabular numbers for any changing digits.** `font-variant-numeric:
  tabular-nums` stops counters, clocks, and prices from shifting horizontally as
  digit widths change. It only works if the font ships `tnum` glyphs; verify with
  your actual font.
- **Centered content re-centers and jumps.** `place-items: center` recomputes the
  center on every height change of the inner content, so a one-line to three-line
  state swap makes the whole block jump. Fix: pin the inner element's height
  (`min-height` at least the tallest state) and center *within* that fixed box, so
  the center never moves.
- **Shrink-to-content width jumps when centered.** An element sized to
  `max-content` inside a centered container changes width as its text changes, and
  because it is centered, both edges move. Fix: give it a stable explicit width
  like `width: min(680px, 100%)` (fixed up to a cap, fluid below). We hit both of
  these in the example's scrubbed day scene; stable inner dimensions fixed the
  jump.
- **Animate transform/opacity only.** Layout properties (`top`, `left`, `width`,
  `height`, `margin`) trigger reflow and count toward CLS; transforms cannot shift
  other elements.

---

## 8. Interaction details

### Tooltips and cursor-following overlays

- **Never render a tooltip directly under the cursor.** It covers what you are
  pointing at and flickers as the pointer enters its own box. Offset it above or
  beside the pointer, biased generous (12 to 16px), since cursors extend
  down-right from their hotspot and enlarged-cursor users need clearance. The
  example's heatmap/timeline/leaderboard tooltips render fully above the cursor
  (`transform: translate(-50%, -100%)` plus a gap).
- **Handle viewport collisions.** The tooltip must flip to the other side and
  shift along the edge so it never clips off-screen.
- **Tooling (2026).** For a cursor-following tooltip, use Floating UI with a
  virtual element (a 0x0 rect at the pointer) and `offset` then `flip` then
  `shift` middleware (order matters); coalesce `mousemove` into one
  `requestAnimationFrame` tick. For element-anchored popovers, prefer the native
  stack: the Popover API (top layer, light-dismiss, Baseline since Jan 2025) plus
  CSS Anchor Positioning with `position-try-fallbacks`, behind `@supports`, with a
  Floating UI fallback for older browsers.

```js
import { computePosition, offset, flip, shift } from "@floating-ui/dom";
const virtual = (x, y) => ({ getBoundingClientRect: () =>
  ({ width: 0, height: 0, x, y, top: y, left: x, right: x, bottom: y }) });
let raf = null;
target.addEventListener("mousemove", ({ clientX, clientY }) => {
  if (raf) return;
  raf = requestAnimationFrame(() => { raf = null;
    computePosition(virtual(clientX, clientY), tip,
      { placement: "top", middleware: [offset(14), flip(), shift({ padding: 8 })] })
      .then(({ x, y }) => Object.assign(tip.style, { left: `${x}px`, top: `${y}px` }));
  });
});
```

### Hit-target sizing

- **Two bars, do not conflate them.** WCAG 2.5.8 Target Size (Minimum) is 24x24
  CSS px (the accessibility floor); Apple HIG recommends 44pt (the touch-comfort
  target). Use 24 as the floor, 44 for touch.
- **The hit target is the interactive area, not the visual.** A 16px icon is fine
  if its clickable box is at least 24px (44 for touch). Expand with transparent
  padding (`content-box`); do not enlarge the graphic.
- **A grid/flex `gap` is dead, unhittable space.** For a dense grid of small
  interactive cells (a heatmap, a color picker, a calendar), `gap` creates gutters
  where clicks fall through and hover targets are smaller than they look. Fix: set
  `gap: 0`, recreate the visual spacing with transparent padding, and paint the
  visual only inside the content box with `background-clip: content-box`. The whole
  contiguous tile is the hit target while the visible swatch stays small. This is
  how the example heatmap gets large, contiguous hover targets at a compact visual
  size.

```css
.grid { display: grid; grid-template-columns: repeat(12, 1fr); gap: 0; }
.cell { padding: 4px;                 /* becomes the visual gap, stays hittable */
  background-clip: content-box;       /* paint swatch only in the content box */
  background-color: var(--swatch); cursor: pointer; min-width: 24px; min-height: 24px; }
```

---

## 9. Native CSS scroll-driven animations (2026 status)

`animation-timeline: view()` (element entering/exiting the viewport) and
`scroll()` (container progress) drive `@keyframes` by scroll position with zero JS.
Because the browser owns the timeline, there are no cached positions to go stale
(the section-1 bug does not occur) and it runs off the main thread. Support is
~85% (Chrome/Edge 115+, Safari 18/26+); Firefox is still behind a flag, so wrap in
`@supports (animation-timeline: view())` with an IntersectionObserver fallback, and
in `@media (prefers-reduced-motion: no-preference)`. Use it for cosmetic reveals
and parallax today; keep GSAP ScrollTrigger for true pinned/scrubbed scenes with
coordinated choreography or callback logic.

```css
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    [data-reveal] { animation: reveal linear both;
      animation-timeline: view(); animation-range: entry 0% cover 35%; }
  }
}
@keyframes reveal { from { opacity: 0; transform: translateY(40px); } to { opacity: 1; transform: none; } }
```

---

## 10. Reliability QA checklist (add to Phase 7)

- [ ] Every scroll reveal fires reliably: **load at the top and scroll down** to
  each one (do not just reload in place). Prefer IntersectionObserver / CSS
  `view()` for one-shot reveals.
- [ ] Reload at the middle and bottom of the page: no jump into a pinned scene
  (`history.scrollRestoration = "manual"`).
- [ ] Pinned/scrubbed scenes have a static, un-pinned reduced-motion branch
  (`gsap.matchMedia`), tested on a real mobile device.
- [ ] rAF / canvas / WebGL loops pause when the tab is hidden and when offscreen;
  nothing drains battery or freezes mid-state.
- [ ] Grid/row reveals fade in place: no per-item size/position stagger that looks
  like a layout bug mid-animation.
- [ ] WebGL detects and falls back; DPR capped; validated on a real GPU, not a
  headless screenshot.
- [ ] No layout jitter from changing content: reserved space, tabular-nums, stable
  centered/shrink-to-content dimensions. CLS < 0.1.
- [ ] Tooltips render clear of the cursor and flip/shift inside the viewport.
- [ ] Interactive targets at least 24px (44 for touch); dense interactive grids
  have contiguous hit tiles (no dead gap).

---

## Sources

Scroll, reveals, pinning, reduced motion:
- GSAP docs: ScrollTrigger, `ScrollTrigger.refresh()`, `gsap.matchMedia()`, and
  "ScrollTrigger tips and mistakes" - https://gsap.com/docs/v3/Plugins/ScrollTrigger/ ;
  https://gsap.com/resources/st-mistakes/ ; https://gsap.com/docs/v3/GSAP/gsap.matchMedia()/
- MDN, History.scrollRestoration - https://developer.mozilla.org/en-US/docs/Web/API/History/scrollRestoration
- MDN, CSS scroll-driven animations; caniuse `animation-timeline` -
  https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations ;
  https://caniuse.com/mdn-css_properties_animation-timeline_scroll
- CSS-Tricks, "An Overview of Scroll Technologies"; Josh W. Comeau,
  "Scroll-Driven Animations" - https://css-tricks.com/an-overview-of-scroll-technologies/ ;
  https://www.joshwcomeau.com/animation/scroll-driven-animations/

Animation performance and correctness:
- MDN, requestAnimationFrame; Page Visibility API; CSS and JavaScript animation
  performance - https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame ;
  https://developer.mozilla.org/en-US/docs/Web/API/Page_Visibility_API ;
  https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/CSS_JavaScript_animation_performance
- MDN, WebGL best practices - https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices
- web.dev, "High-performance CSS animations" - https://web.dev/articles/animations-guide
- Chrome for Developers / Chromium, SwiftShader and the Chrome 137 removal of the
  automatic WebGL software fallback -
  https://developer.chrome.com/blog/swiftshader-brings-software-3d-rendering-to-chrome ;
  https://issues.chromium.org/issues/40277080

Layout stability and interaction:
- web.dev, Cumulative Layout Shift and Optimize CLS - https://web.dev/articles/cls ;
  https://web.dev/articles/optimize-cls
- MDN, `contain-intrinsic-size`, `content-visibility`, `font-variant-numeric`,
  `background-clip`, Popover API, CSS anchor positioning -
  https://developer.mozilla.org/en-US/docs/Web/CSS/contain-intrinsic-size ;
  https://developer.mozilla.org/en-US/docs/Web/CSS/background-clip ;
  https://developer.mozilla.org/en-US/docs/Web/API/Popover_API
- W3C WAI, Understanding SC 2.5.8 Target Size (Minimum); Apple HIG (44pt) -
  https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- Floating UI docs (virtual elements, flip, shift, tooltip) - https://floating-ui.com/docs/tutorial
