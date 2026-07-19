# Quality Bar and Self-Critique

Reference for the `high-fidelity-web` skill (Phase 7) and the canonical source for
the standalone `quality-audit` skill. This is the acceptance gate: the checklists
pros use to decide whether something is "good enough," plus how to run a design
critique on yourself.

> If you are auditing an existing site, run the seven-step critique in section 8
> first (it tells you where to look), then check each relevant checklist below.

---

## 1. The reproducible quality-bar checklist (visual + interaction)

From the premium-UI teardown of Stripe / Linear / Vercel:

- [ ] **Microstates:** every interactive element has default, hover, focus,
  active, disabled, loading.
- [ ] **Focus rings:** designed, visible, high-contrast; never browser default.
- [ ] **Hairlines:** 0.5px or 1px at low alpha, deliberately placed (not 1px solid
  gray everywhere).
- [ ] **Empty/error states:** designed, not stubbed; treated as high-trust moments.
- [ ] **Numerals:** tabular numbers for data; monospace for code/IDs.
- [ ] **Typography:** one family + mono; systemic scale/weight/spacing; no mixed
  display fonts.
- [ ] **Color:** restrained, used for meaning not decoration.
- [ ] **Motion:** curves and durations defined and applied consistently; exit
  faster than enter; under ~300ms for functional UI; only `transform`/`opacity`
  animated.
- [ ] **Loading:** intentional (staggered, with motion), not a generic spinner.

## 2. Spacing, hierarchy, rhythm

- [ ] Consistent spacing scale; no arbitrary one-off margins.
- [ ] Clear visual hierarchy: one primary action per view; secondary actions
  visually subordinate.
- [ ] Alignment and optical balance (squint test: does the eye land where
  intended).
- [ ] Generous, deliberate whitespace; density is in behavior, not crowding.

## 3. Motion polish (amateur vs. pro giveaways)

Common violations and their fixes:

| Issue | Fix |
|---|---|
| `transition: all` | Specify exact properties |
| `scale(0)` entry | Start from `scale(0.95)` with opacity |
| `ease-in` on UI | Switch to `ease-out` or a custom curve |
| Animation on keyboard action | Remove entirely |
| Duration > 300ms (functional UI) | Reduce to 150 to 250ms |
| Hover without media query | Gate behind `@media (hover: hover) and (pointer: fine)` |
| Same enter/exit speed | Make exit faster |

- [ ] Button press: `transform: scale(0.97)` on `:active` (range 0.95 to 0.98).
- [ ] Motion is interruptible and retargetable (transitions over keyframes where
  it matters).

## 4. Performance (Core Web Vitals)

- [ ] **LCP < 2.5s.** Preload the LCP element; WebP/AVIF; CDN static assets;
  server response under ~200ms.
- [ ] **INP < 200ms.** Keep the main thread free; avoid janky handlers.
- [ ] **CLS < 0.1.** Reserve space for media; avoid layout-shifting injects.
- [ ] **60fps animation.** Animate only `transform`/`opacity` (skip layout/paint,
  run on GPU). Framer Motion shorthand (`x`, `y`, `scale`) is not
  hardware-accelerated by default; pass the full transform string.
- [ ] Inline critical CSS; lazy-load below-the-fold and heavy WebGL.
- [ ] Measure with Lighthouse / PageSpeed Insights / DevTools. (Roughly half of
  sites fail CWV, so passing is itself a differentiator.)

## 5. Responsiveness

Run the full checklist in `responsive-and-mobile.md` section 8. The essentials:

- [ ] Verified at phone, tablet, desktop, and large desktop widths.
- [ ] No horizontal overflow at any width; full-height heroes use `svh`/`dvh`.
- [ ] Touch targets >= 44px; hover effects gated for touch.
- [ ] Immersive effects (WebGL, particles, parallax, pinned scroll) degrade or fall
  back on phones; nothing janks or drains battery.
- [ ] Layout, type scale, and motion adapt sensibly (do not just shrink).

## 6. Accessibility

- [ ] **Reduced motion:** fewer and gentler animations, not zero; keep
  opacity/color transitions that aid comprehension.
- [ ] Keyboard operable; logical focus order; visible focus.
- [ ] Semantic HTML; ARIA only where needed; alt text.
- [ ] Color contrast meets WCAG 2.2; do not rely on color alone for meaning.
- [ ] Screen-reader pass on primary flows.

## 7. Motion and interaction reliability

The bugs that only surface when you actually use the site: scroll down to a reveal,
reload mid-page, leave the tab, point at a tooltip. Full catalog and fixes in
`reliability-and-gotchas.md`; the gate:

- [ ] **Reveals fire on scroll-down,** not just on reload-in-view. One-shot reveals
  use `IntersectionObserver` / CSS `view()`, not a stale-prone ScrollTrigger.
- [ ] **No reload-into-pin jump:** reloading at mid-page and at the bottom stays put
  (`history.scrollRestoration = "manual"`).
- [ ] **Loops pause when hidden/offscreen** (rAF/canvas/WebGL); nothing freezes
  mid-state or drains battery.
- [ ] **Grid/row reveals fade in place** (no per-item size/position stagger that
  reads as a layout bug mid-animation).
- [ ] **No content jitter:** reserved space, `tabular-nums`, stable
  centered/shrink-to-content widths.
- [ ] **Tooltips clear the cursor** and flip/shift to stay inside the viewport.
- [ ] **Hit targets >= 24px (44 for touch);** dense interactive grids have
  contiguous hit tiles (no dead `gap`).
- [ ] **Pinned/scrubbed scenes** have a static reduced-motion branch and degrade on
  mobile.

## 8. How to give yourself a design critique (run this to audit)

1. **State the intended feeling in one word.** Open the running site. Does it
   deliver that word in the first 3 seconds (the hero / first impression)?
2. **Run the generic test.** Could this section live on any other brand's site? If
   yes, it lacks concept fidelity. Make it specific or cut it.
3. **Adversarial QA.** Spam clicks, interrupt animations mid-flight, throttle the
   network, tab through everything. Anything that breaks fails the bar.
4. **Microstate audit.** Pick three interactive elements at random; confirm all six
   states exist and feel designed.
5. **Unseen-details sweep.** Hairlines, focus rings, exit easing, stagger timing,
   empty states, copy rhythm. List every default still present and fix it.
6. **Numbers gate.** Run Lighthouse; confirm LCP/INP/CLS pass and animations hold
   60fps.
7. **The Awwwards question.** "Would this earn a second look from a jury?" If you
   cannot name the specific thing that makes it distinctive, it is not done.

## 9. Between-phase self-critique protocol (for the build flow)

Run this as you move between build phases, talking to yourself:

1. **Concept fidelity:** does every section ladder up to the one big idea? If a
   section could appear on any other site, it is generic. Fix or cut it.
2. **Reference test:** "Would this earn a second look on Awwwards/Godly, or is it a
   safe template?" Name the specific thing that makes it distinct.
3. **Behavior test:** does each interactive element have all six microstates and
   designed motion, or is the polish only skin-deep? "Density is in the behavior."
4. **Unseen-details test:** hairlines, focus rings, empty states, exit easing,
   stagger, copy. List what is still defaulted and fix it.
5. **The "feel" test:** describe the intended feeling in one word; verify the
   running site delivers it. If you cannot, the motion language is wrong.

---

Sources for this reference are consolidated in the skill's other reference files
(`design-principles.md`, `techniques.md`): primarily the Mantlr premium-UI
teardown, Emil Kowalski's design-engineering skill and "Animations on the Web"
course, Rauno Freiberg's "Invisible Details," and the Core Web Vitals guides.
