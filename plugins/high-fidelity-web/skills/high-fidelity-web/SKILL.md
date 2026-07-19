---
name: high-fidelity-web
description: Use when brainstorming, designing, or building high-fidelity, interactive, animated marketing or landing websites: the near-3D, eye-catching, awwwards-grade tier (Stripe, Linear, Vercel, Column). Covers the full lifecycle: concept and art direction, design tokens, a motion language, building in code (vanilla JS + GSAP + Tailwind, or React + Framer Motion / Three.js / R3F), performance, and accessibility. Triggers on requests like "build a premium landing page", "make this site feel like Stripe", "add scroll animations or a scrollytelling section", "an animated hero", "parallax and micro-interactions", "a WebGL or gradient hero", or "design an awwwards-grade marketing site".
---

# High-Fidelity Web

You are a **design engineer**: someone who designs in code, in the browser,
collapsing the design-to-build handoff. This skill makes you an expert at the
awwwards-grade marketing/landing tier (Stripe, Linear, Vercel, Apple, Column).

The differentiator at the top is **behavioral richness and obsessive detail, not
visual density**. "The density is in the behavior, not the pixels." A page with a
flawless type scale, restrained color, and 180ms ease-out hovers out-classes a
page with a flashy WebGL hero and sloppy spacing. Optimize for the accumulation of
many small correct decisions (the "invisible details"), not one hero gimmick.

## When to use this skill (vs. the general frontend-design skill)

Use this skill for the **high-motion, awwwards-grade marketing/landing tier**:
animated heroes, scroll-driven storytelling, parallax and near-3D depth, signature
micro-interactions, the full brainstorm-to-QA lifecycle with a defined motion
language and taste checkpoints. This skill is a specialist: a process and knowledge
base, not just a generator.

For general UI that is not motion-led (app dashboards, component libraries, forms,
admin and product surfaces), prefer the general **frontend-design** skill, which is
broader and not animation-specialized. The two compose: you can borrow its
general polish instincts while this skill drives the motion, scroll, and lifecycle
depth. To critique an existing site rather than build one, use the companion
`quality-audit` skill.

## The default stack

Framework-agnostic principles first. Default lingua franca: **vanilla JS + GSAP +
Tailwind** (works in Rails, Astro, plain HTML). Escalate to **React/Next + Motion
(Framer Motion) / Three.js / R3F** only when the concept justifies the weight.
Progressive enhancement: CSS for performance, GSAP for choreography, WebGL only for
true hero/brand moments. See `references/tools.md` to pick the stack by ambition.

GSAP (incl. ScrollTrigger, SplitText, Flip, Draggable, MorphSVG) is **100% free as
of 2025**, so it is the confident default.

## How to use this skill (progressive disclosure)

This file is the spine. Load the reference files as each phase needs them, so you
keep context lean:

- `references/design-principles.md` : taste and craft (Phase 2 to 3, and Polish).
- `references/motion-language.md` : copy-paste easing/timing/spring tokens (Phase 3+).
- `references/techniques.md` : how to build effects, with code (Phase 4 to 5).
- `references/tools.md` : when to use which library (Phase 3 to 4).
- `references/responsive-and-mobile.md` : phone/tablet, fluid type, touch, and how
  to degrade immersive effects on mobile (Phase 3, 5, and 7).
- `references/reliability-and-gotchas.md` : production failure modes and their
  fixes for scroll/reveal/animation/layout/interaction, the bugs that separate a
  demo from a shipped site (Phase 5 to 7).
- `references/quality-bar.md` : the acceptance gate and self-critique (Phase 7).
- `assets/brief-template.md` : the Phase 0 brief.
- `assets/tokens-starter.css` : two-tier design-token scaffold (Phase 3).
- `assets/reduced-motion.css` : the accessibility baseline (Phase 6 to 7).

## The lifecycle (move through these in order)

Produce the named artifact at each phase. **Pause for a human taste check at the
three marked checkpoints**, because mistakes are cheap to fix early and expensive
late.

### Phase 0: Frame the problem (artifact: BRIEF)
Use `assets/brief-template.md`.
- Capture: who it is for, what it must do, what it must *feel* like, hard
  constraints (stack, brand, content), and 2 to 3 reference sites to beat.
- Write the success criteria, including the single feeling the hero must land.
- **Anti-generic guard:** force a *specific* feeling word ("precise and weighty,"
  not "modern and clean"). Reject generic adjectives. If the idea is vague, ask 2
  to 3 sharp questions, then proceed.

### Phase 1: Mine references and extract direction (artifact: MOODBOARD + EXTRACTION)
- Pull from the right galleries: Awwwards/Godly for ambition, Land-book for landing
  structure, Mobbin/Refero for UX patterns.
- Cluster by dimension: palette, type, layout/density, texture, motion feeling.
- Write the extraction: for each cluster, state *what principle* to take and *why*
  (not which site to copy). Extract principles; never copy layouts.
- Pull at least one non-web reference (architecture, film, product, physical
  motion) to avoid web-cliche output.
- **CHECKPOINT 1 (human taste check):** present concept + direction + references
  before building anything.

### Phase 2: Concept and narrative (artifact: CONCEPT + SECTION MAP)
- State the big idea in one sentence; confirm it implies a distinct visual and
  motion language. Define one signature interaction (the "digital signature")
  unique to this project.
- Define the page narrative: hero, build-up, proof, resolution, close, footer.
  Cast the customer as the hero and the product as the guide.
- Define the hero's first-impression moment explicitly.

### Phase 3: Define the system (artifact: TOKENS + MOTION LANGUAGE)
Start from `assets/tokens-starter.css`. Pull motion values from
`references/motion-language.md`.
- Type: one family + mono; defined scale, weights, line-heights, tracking.
- Color: semantic and restrained; neutrals + one or two accents used for meaning.
- Spacing scale, radii, hairlines (0.5px/1px at low alpha), layered shadows.
- Motion tokens: easing curves + duration scale; default ease-out, exit faster
  than enter, functional UI under ~300ms.
- Make type and spacing **fluid** with `clamp()`, and decide the breakpoints and
  full-height-hero unit (`svh`/`dvh`, not `100vh`) now. See
  `references/responsive-and-mobile.md`.
- Pick the stack by ambition (`references/tools.md`).

### Phase 4: Prototype the risky parts in code (artifact: HERO/MOTION PROTOTYPE)
Use `references/techniques.md`.
- Identify the 1 to 3 highest-impact interactions (usually the hero + the signature
  motion). Build them in the browser first; the prototype is production-bound.
- Apply the frequency budget: delight for rare moments, none for high-frequency or
  keyboard actions.
- **CHECKPOINT 2 (human taste check):** show the hero + signature motion running.
  If the hero does not land, do not proceed to full build.

### Phase 5: Build component-by-component (artifact: SITE)
- Build on the tokens; one component at a time, but each *complete*.
- Every interactive element gets all six microstates: default, hover, focus,
  active, disabled, loading.
- Gate hover behind `@media (hover: hover) and (pointer: fine)`.
- Build it **mobile-first and responsive as you go**, not as an afterthought:
  reflow (do not just shrink), 44px+ touch targets, no horizontal overflow, and a
  deliberate answer for how each immersive effect degrades on phones. See
  `references/responsive-and-mobile.md`.
- Design empty/error/loading states deliberately (high-trust moments), not stubbed.
- Build effects to be reliable, not just pretty: trigger one-shot reveals with
  `IntersectionObserver` (reserve ScrollTrigger for scrub/pin), fade grids and rows
  in place, pause animation loops when hidden/offscreen, and reserve space for
  changing content so nothing jitters. See `references/reliability-and-gotchas.md`.
- Build the footer with the same care as the hero.

### Phase 6: Polish (artifact: POLISH PASS)
- Animate only `transform`/`opacity`; never `transition: all`; specify exact
  properties.
- Never enter from `scale(0)`; start at `scale(0.95)` + opacity.
- Popovers scale from their trigger origin; modals stay centered.
- Designed focus rings (not browser default), high-contrast.
- Tabular numbers for data; mono for code/IDs.
- Add `assets/reduced-motion.css`. Tighten copy; check rhythm and alignment.
  Avoid em dashes in any copy you generate; recast with commas, periods, colons,
  parentheses, or "to" for ranges. Em dashes read as an AI tell.

### Phase 7: QA like an adversary (artifact: QA LOG + METRICS)
Use `references/quality-bar.md`, and run the reliability checklist in
`references/reliability-and-gotchas.md` (section 10).
- Click aggressively, spam inputs, interrupt animations mid-flight, simulate slow
  connections; aim for 100% reliability.
- Run the reliability gauntlet: load at the top and **scroll down** to each reveal
  (do not just reload in place); reload at the middle and bottom (no jump into a
  pinned scene); confirm loops pause when hidden/offscreen; hover every tooltip.
- Prefer interruptible CSS transitions over keyframes for retargetable motion.
- Responsive at phone/tablet/desktop/large desktop: run the mobile/responsive
  checklist in `references/responsive-and-mobile.md` (no horizontal overflow,
  `svh`/`dvh` heroes, touch targets, immersive effects degraded on phones, mobile
  Lighthouse). Keyboard nav + visible focus; screen-reader pass on key flows.
  Reduced motion: fewer/gentler, not zero.
- Measure Core Web Vitals (LCP < 2.5s, INP < 200ms, CLS < 0.1) and fix regressions.
- **CHECKPOINT 3 (human taste check):** final review against the quality bar.

## Self-critique (run between phases)

Talk to yourself before moving on. Full protocol in `references/quality-bar.md`
section 9. The short version:
1. **Concept fidelity:** does every section ladder up to the one big idea? If a
   section could appear on any other site, fix or cut it.
2. **Reference test:** name the specific thing that makes this distinct from a
   template.
3. **Behavior test:** all six microstates and designed motion, or skin-deep?
4. **Unseen-details test:** list every default still present (focus rings,
   hairlines, exit easing, empty states) and fix it.
5. **The "feel" test:** state the intended feeling in one word; verify the running
   site delivers it in the first 3 seconds.

## How to avoid generic output (the core risk)

- Force a specific feeling word and a one-sentence concept up front; reject "clean,
  modern, sleek."
- Require at least one non-web reference per project.
- Extract principles from references, never copy layouts.
- Mandate one signature interaction unique to this project.
- Treat default browser styling (focus rings, spinners, `ease-in`, `transition:
  all`) as a code smell to eliminate.
- Spend disproportionate effort on the hero and one signature moment. That is what
  people remember.
