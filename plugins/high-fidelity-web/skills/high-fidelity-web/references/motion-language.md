# Motion Language (copy-paste cheat sheet)

Reference for the `high-fidelity-web` skill. The fast, copy-pasteable motion
tokens: easing curves, durations, springs, stagger, and the non-negotiable perf
rules. Grab this in Phase 3 (define the motion system) and keep it open while you
build. For the reasoning behind every value, see `design-principles.md` section 2.

The spine of this is Emil Kowalski's design-engineering practice (Linear, ex
Vercel; creator of Sonner and Vaul) plus Rauno Freiberg's interaction-detail work.

---

## Easing: pick by what the element is doing

| Situation | Easing |
|---|---|
| Entering / exiting element | **ease-out** (starts fast, feels responsive) |
| Moving / morphing on screen | **ease-in-out** |
| Hover / color change | **ease** |
| Constant motion (marquee, spinner) | **linear** |
| Anything in functional UI | **never `ease-in`** (sluggish start) |

Do not ship the bare CSS keywords as final values; they lack strength. Use tuned
cubic-beziers:

```css
--ease-out-strong:    cubic-bezier(0.23, 1, 0.32, 1);     /* default UI workhorse */
--ease-in-out-strong: cubic-bezier(0.77, 0, 0.175, 1);    /* on-screen movement */
--ease-drawer:        cubic-bezier(0.32, 0.72, 0, 1);     /* iOS-like sheet/drawer */
```

## Duration: keep functional UI under ~300ms

| Element | Duration |
|---|---|
| Button / press feedback | 100 to 160ms |
| Tooltips, small popovers | 125 to 200ms |
| Dropdowns, selects, menus | 150 to 250ms |
| Modals, drawers, sheets | 200 to 500ms (more travel justifies longer) |

- **Functional UI ceiling: ~300ms.** A 180ms transition feels more responsive
  than a 400ms one.
- **Exit faster than enter.**
- **Asymmetric timing:** slow where the user decides (a 2s hold-to-confirm), fast
  where the system responds (~200ms snap-back).
- **Macro/marketing reveals** (hero entrances, scroll scenes) may run 400 to
  800ms+ because they are rare and emphasize elegance. The ~300ms rule is for
  functional UI, not cinematic page moments.

## Springs (for anything interruptible or gestural)

Springs carry velocity instead of restarting, so they feel physical. Use for drag,
sheets, anything the user can grab mid-flight.

```js
// Apple-style, recommended:
{ type: "spring", duration: 0.5, bounce: 0.2 }
// Classic physics form:
{ mass: 1, stiffness: 100, damping: 10 }
```

Keep **bounce subtle: 0.1 to 0.3.** Higher reads as cartoonish.

## Stagger

- **30 to 80ms between items.** Longer feels laborious.
- Stagger is decorative: **never block interaction** while it plays (the user must
  be able to click item 5 before item 12 finishes entering).
- Cap total orchestration time. If 30 items each add 60ms, the last starts ~1.8s
  in, which feels broken. Cap the number that stagger, or shrink per-item delay as
  count grows.

## Frequency budget (whether to animate at all)

Decide by how often the action happens:

| Frequency | Treatment |
|---|---|
| 100+/day (shortcuts, command menu, core nav) | **No animation.** |
| Tens/day (hover, nav) | Minimal, fast, or none. |
| Occasional (modals, toasts, tab switches) | Standard tuned animation. |
| Rare / first-run (onboarding, success, celebration) | Room for delight. |

Never animate keyboard-initiated actions. Delight is a rare reward, not a constant.

## Non-negotiable performance rules

- **Animate only `transform` and `opacity`** (and `filter` with care). Never
  `width`, `height`, `top`, `left`, `margin`, `padding`: those trigger layout and
  jank below 60fps.
- **Never `transition: all`.** Name the exact properties.
- **Never enter from `scale(0)`.** Start at `scale(0.95)` + `opacity: 0`. Same for
  exits.
- **Press feedback:** `scale(0.97)` on `:active`, ~160ms ease-out.
- **Origin-aware popovers:** set `transform-origin` to the trigger so the popover
  grows out of its button. Modals stay centered.
- **Prefer CSS / Web Animations API** over rAF JS on a busy main thread (CSS runs
  off the main thread and stays smooth).
- **Framer Motion caveat:** shorthand props (`x`, `y`, `scale`) animate on the
  main thread; pass the full transform string to stay GPU-accelerated.

## Always

- Honor `prefers-reduced-motion`: remove movement/position/parallax, keep gentle
  opacity/color transitions that aid comprehension. (See `assets/reduced-motion.css`.)
- Gate hover behind `@media (hover: hover) and (pointer: fine)`.
- One subtle parallax effect per page, maximum.
- Make motion interruptible and retargetable (transitions over keyframes where the
  user can interrupt).

## The meta-rule

Change defaults on purpose. Accumulate many small correct details. Spend delight
rarely. Cut any motion that does not communicate state, preserve spatial
continuity, explain/reveal, or reward a rare moment.
