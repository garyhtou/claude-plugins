# Responsive and Mobile

Reference for the `high-fidelity-web` skill. Most traffic is mobile, yet the
awwwards-grade tier is where responsive gets neglected: heavy heroes, WebGL,
parallax, and scroll scenes are easy to ship desktop-only and leave broken or
janky on phones. Treat phone, tablet, and large desktop as first-class. Load this
in Phase 3 (define the system) and Phase 5 to 7 (build, polish, QA).

## 1. Mindset: mobile-first, content-driven, fluid

- **Mobile-first.** Write the base styles for the smallest screen, then add
  complexity at wider breakpoints with `min-width` queries. It is easier to add
  than to claw back, and it keeps the mobile payload lean.
- **Breakpoints follow content, not devices.** Do not target "iPhone" or "iPad"
  widths. Resize the browser and add a breakpoint wherever the layout starts to
  look wrong. Practical ranges to think in: phone (up to ~640px), large phone /
  small tablet (~640 to 860), tablet (~860 to 1024), desktop (1024+), large
  (1280/1440+). Adjust to the design.
- **Fluid over stepped.** Prefer `clamp()` for type and spacing so values scale
  continuously and you need far fewer breakpoints. `font-size: clamp(2rem, 5vw,
  4.4rem)` is one line that replaces three media queries. Always set a sane min
  and max so it never gets too small or too large.
- **Container queries for components.** When a component (card, panel, nav) must
  adapt to the space it sits in rather than the viewport, use container queries
  (`container-type: inline-size` + `@container`). Baseline across modern browsers
  in 2026. They make components truly portable across layouts.

## 2. The mobile viewport (the parts that bite)

- **Dynamic viewport units.** `100vh` is wrong on mobile: it ignores the
  expanding/collapsing browser UI, so full-height heroes get cut off or jump. Use
  `svh` (small: UI shown), `lvh` (large: UI hidden), and `dvh` (dynamic: current).
  A full-height hero is usually `min-height: 100svh` (safe) or `100dvh` (follows
  the bar, but can cause reflow on scroll, test it). Provide a `vh` fallback for
  old browsers.
- **Safe areas (notches, home indicators).** Add `<meta name="viewport"
  content="width=device-width, initial-scale=1, viewport-fit=cover">` and pad with
  `env(safe-area-inset-*)` so content and fixed bars clear the notch and the home
  indicator. Example: `padding-bottom: max(1rem, env(safe-area-inset-bottom))`.
- **Prevent horizontal overflow.** A single element wider than the viewport
  creates a horizontal scroll and shifts everything. Causes and fixes:
  - Flex/grid children default to `min-width: auto` and refuse to shrink below
    their content. Add `min-width: 0` (or `min-inline-size: 0`) to the shrinking
    child so long text and wide grids can compress.
  - Grids that auto-create columns from many items (a heatmap, a calendar) can
    force a min width. Pin them with `grid-template-columns: repeat(N, 1fr)` or
    `grid-auto-columns: 1fr` so the columns share the available width.
  - Use `overflow-x: clip` on a wrapper for genuinely oversized decorative layers
    (a full-bleed canvas, an off-screen glow) instead of letting them scroll.
  - QA tip: in DevTools, run a quick scan for any element whose right edge exceeds
    the viewport width, that is your culprit.

## 3. Touch and pointers

- **Gate hover behind capability, not width.** `@media (hover: hover) and
  (pointer: fine)` for anything that depends on a real cursor (magnetic buttons,
  tilt, custom cursors, hover reveals). On touch, hover states stick and look
  broken. Never hide essential content or actions behind hover only.
- **Touch targets.** Minimum 44x44px (Apple HIG) / 24x24px with spacing (WCAG
  2.5.8), comfortably 48px. Space tappable items so fat fingers do not mis-hit.
- **Gestures.** Replace hover-driven interactions with tap, swipe, or always-on
  variants on touch. Make drag and swipe interruptible and velocity-aware (a quick
  flick should work even if the distance threshold was not met). Do not hijack the
  browser's own gestures (back-swipe, pull-to-refresh) unless the design truly
  needs it, and then test it hard.
- **No sticky :active glow.** Tap highlight and lingering active states read as
  broken on mobile; design press feedback that resolves quickly.

## 4. Adapting the immersive parts (the hard, high-fidelity-specific part)

This section is about degrading effects on small/low-power screens. For the
non-mobile-specific ways these same effects break (scroll reveals not firing, the
reload-into-pin jump, rAF loops freezing offscreen, WebGL failing in headless),
see `reliability-and-gotchas.md`.

Premium effects must degrade deliberately on phones, not run at full weight:

- **WebGL / shaders / particle fields.** These are GPU and battery heavy on phones
  and often run on software GL in low-power contexts. Strategy: cap DPR at ~1.5 to
  2; reduce particle counts and canvas resolution on small/low-power devices; pause
  rendering when offscreen and when the tab is hidden; and provide a lighter static
  or CSS fallback. Consider `navigator.hardwareConcurrency` / `deviceMemory` /
  `prefers-reduced-motion` / Save-Data as signals to scale down or skip.
- **Scroll-jacking and pinned scroll scenes.** Pinned, scrubbed, or
  scroll-hijacked sections are the most fragile on touch (momentum scrolling,
  address-bar resize, variable refresh). Prefer native scroll. If you pin, test on
  real devices, keep the scene short, and offer a simpler stacked layout under
  reduced motion or on small screens.
- **Parallax.** Cut to one subtle effect at most, and disable under reduced motion;
  parallax is a common motion-sickness trigger and is jankier on mobile.
- **Smooth-scroll libraries (Lenis).** Reconsider on touch: native momentum is
  usually better. If kept, test inertia and disable under reduced motion.
- **The rule:** every signature interaction needs an answer to "what does this do
  on a phone." Lighter, native, or off are all valid; broken is not.

## 5. Layout adaptation

- **Reflow, do not just shrink.** Multi-column grids become single columns; side
  nav becomes a top bar or a sheet/hamburger; wide data tables become stacked
  cards or horizontally scrollable regions with a sticky first column. Do not ship
  a desktop layout zoomed out.
- **Nav.** Collapse secondary links behind a menu on small screens, keep the
  primary CTA visible. Make the menu keyboard and screen-reader accessible.
- **Type scale.** Display type that sings at 5rem on desktop is oppressive at
  360px. Use `clamp()` and let headlines breathe; tighten tracking less on small
  sizes.
- **Spacing.** Reduce section padding and gaps on mobile so content is not buried
  under whitespace; fluid space tokens (`clamp()`) handle this.

## 6. Performance on mobile (where it matters most)

Phones have weaker CPUs/GPUs, less memory, and metered, higher-latency networks.

- **Responsive images.** `srcset` + `sizes`, or `<picture>` with modern formats
  (AVIF/WebP), so phones download phone-sized assets. This is usually the single
  biggest mobile win.
- **Ship less.** Code-split and lazy-load heavy libraries (Three.js, big animation
  bundles) with dynamic `import()` and only on capable/large viewports. Defer
  below-the-fold work. `content-visibility: auto` to skip offscreen render.
- **60fps on weaker GPUs.** Animate only `transform`/`opacity`; be stingier with
  `backdrop-filter`, large `blur()`, and many simultaneous compositor layers on
  mobile (they are disproportionately expensive there). Cap DPR for canvas.
- **Honor Save-Data and reduced-motion.** Skip autoplay video, heavy fetches, and
  big animations when the user or device asks for less.
- **Core Web Vitals are measured on mobile.** Field data and Lighthouse default to
  a throttled mobile profile, so mobile LCP/INP/CLS are what you are graded on.

## 7. Accessibility overlaps (not optional)

- **Reflow (WCAG 1.4.10):** content must work at 320px CSS width and at 400% zoom
  without horizontal scrolling for a column of content.
- **Text spacing and zoom:** do not break layouts when users bump line-height,
  letter-spacing, or zoom; avoid fixed heights on text containers.
- **Target size (WCAG 2.5.8):** 24x24px minimum, ideally 44px+.
- **Orientation:** support both portrait and landscape; do not lock orientation
  without cause.

## 8. Mobile/responsive QA checklist (add to Phase 7)

- [ ] Verified at ~360 to 400px (phone), ~768px (tablet portrait), ~1024px
  (tablet landscape / small laptop), and a large desktop width.
- [ ] No horizontal overflow at any width (no element exceeds the viewport).
- [ ] Full-height heroes use `svh`/`dvh`, not `100vh`; nothing is cut by the mobile
  address bar.
- [ ] Safe-area insets respected on notched devices; `viewport-fit=cover` set.
- [ ] Hover-only affordances have touch equivalents; hover gated to fine pointers.
- [ ] Touch targets >= 44px with adequate spacing.
- [ ] WebGL/particles/parallax scale down or fall back on phones; nothing janks or
  drains battery; offscreen and hidden-tab rendering paused.
- [ ] Pinned/scrubbed scroll scenes tested on a real device (or a simpler layout
  served on small screens / reduced motion).
- [ ] Responsive images shipped; heavy libs not loaded on small viewports.
- [ ] Reduced motion and Save-Data honored.
- [ ] Mobile Lighthouse passes LCP < 2.5s, INP < 200ms, CLS < 0.1.
- [ ] Works at 400% zoom and 320px width (WCAG reflow).

## Sources

- web.dev, "Responsive web design basics" and "Learn Responsive Design" -
  https://web.dev/articles/responsive-web-design-basics ;
  https://web.dev/learn/design
- MDN, "Using container queries" -
  https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries
- MDN, viewport units incl. `svh`/`lvh`/`dvh` -
  https://developer.mozilla.org/en-US/docs/Web/CSS/length#viewport-percentage_lengths
- MDN, `env()` and safe-area insets -
  https://developer.mozilla.org/en-US/docs/Web/CSS/env
- MDN, `@media` `hover` and `pointer` features -
  https://developer.mozilla.org/en-US/docs/Web/CSS/@media/hover
- web.dev, `content-visibility` -
  https://web.dev/articles/content-visibility
- web.dev / MDN, responsive images (`srcset`, `sizes`, `<picture>`) -
  https://developer.mozilla.org/en-US/docs/Web/HTML/Responsive_images
- Josh W. Comeau, "The sad state of fluid typography" and clamp() patterns -
  https://www.joshwcomeau.com/css/fluid-typography/
- Apple Human Interface Guidelines, touch target sizing (44pt) ;
  WCAG 2.2 Success Criteria 1.4.10 Reflow, 2.5.8 Target Size, 1.4.4 Resize Text -
  https://www.w3.org/WAI/WCAG22/Understanding/
