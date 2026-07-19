# Design Principles & Visual/Motion Language for High-Fidelity Web

Reference material for an agent that builds awwwards-grade, animated marketing/landing sites (the Stripe / Linear / Vercel / Apple / Column tier). This file is the "taste and craft" knowledge base: what separates premium from template, with concrete numbers, easing values, and rules an agent can follow directly.

---

## 0. The mental model

Premium feel is not one big move. It is the **accumulation of many small correct decisions** that individually go unnoticed and collectively read as "expensive." Rauno Freiberg (Vercel) calls these the "invisible details": the timing of an animation, the physics of a gesture, the origin a popover grows from, the 0.5px hairline at low alpha. None of them announce themselves. Their absence is what makes a site feel generic. (Source: Freiberg, "Invisible Details of Interaction Design.")

The corollary: an agent should optimize for **correctness of small details at scale**, not for one hero gimmick. A page with a flawless type scale, optically-aligned icons, restrained color, and 180ms ease-out hovers will out-class a page with a flashy WebGL hero and sloppy spacing.

---

## 1. What separates high fidelity from generic AI/template design

### 1.1 The generic "tells" (avoid these)

These are the signatures that make a site read as template or default-AI output:

- **Default everything**: browser-default `ease` easing, default focus rings, default `box-shadow` presets, untuned border-radius. Defaults are the tell. Every value should look chosen. (Freiberg; Mantlr on Stripe/Linear/Vercel.)
- **Even, mechanical spacing** with no rhythm or grouping. Template layouts space everything the same; premium layouts use intentional proximity (related things close, unrelated things far).
- **Too many colors used decoratively.** Generic sites color things to look "designed." Premium sites use color almost entirely for **meaning** (red = danger, green = success, brand hue = primary action) and keep the rest near-neutral. (Mantlr.)
- **A single off-the-shelf font at one or two weights**, with no attention to tracking, optical size, or hierarchy.
- **Sloppy optical alignment**: icons centered by bounding box instead of by visual weight, text baselines not aligned, a "+" that is mathematically centered but looks low.
- **Heavy, muddy shadows** (the default `0 4px 6px rgba(0,0,0,0.1)` look) instead of layered, tuned elevation.
- **Gradients that band** (visible stepping) and have no grain, so they look like a CSS default rather than a designed surface.

### 1.2 The craft signals (build these in)

**Spacing, rhythm, and a spatial system.** Use a consistent spacing scale (a 4px or 8px base grid is the standard). Premium teams emphasize **interaction density over visual density**: layouts can be sparse and roomy, but every interactive element is fully wired (hover, focus, active, disabled, loading) and responsive. (Mantlr.) Whitespace is a feature, not empty space. Group with proximity; separate with space, not always with lines.

**Optical alignment over mathematical alignment.** Align by what the eye sees, not what the box says. Nudge a play triangle right of geometric center; nudge a glyph so its visual mass sits centered; align text by baseline and cap height, not bounding box. This is one of the highest-leverage "invisible" craft moves. (Freiberg.)

**Hairlines and separators.** Use thin lines at **0.5px or 1px at low alpha** (for example `rgba(255,255,255,0.08)` on dark, `rgba(0,0,0,0.06)` on light), deliberately placed, not default 1px solid gray borders everywhere. (Mantlr.) On dark UIs, a subtle top highlight border (lighter alpha on the top edge) plus a darker bottom simulates a light source and adds realism.

**Typographic detail.** See section 6. The short version: one type family at 4 to 6 sizes max, a consistent modular scale, tuned tracking (tighter on large display, looser on small caps/labels), and optical-size awareness on variable fonts. (Mantlr; Design Shack.)

**Intentional color.** Pick a tight neutral ramp plus one brand hue plus semantic colors. Stripe: neutrals plus measured indigo. Linear: cool grays plus brand indigo. Vercel: near-monochrome plus context color. (Mantlr.)

**Grain, noise, and gradients done well.** Modern premium surfaces add subtle film grain or noise over gradients to kill banding and add a tactile, organic feel. The best dark-mode gradients are "nearly imperceptible: they add depth without being obvious." (DesignRush; Colorhero.) Ambient color orbs (deep purple, neon blue, hot pink) blurred behind glass UI create depth without flatness ("dark glassmorphism").

**Depth and layering.** Real elevation hierarchy: background plane, content plane, floating plane, overlay plane, each with its own shadow/blur treatment. See section 4.

**Lighting.** Treat the UI as if lit from a consistent direction (usually top). Top edges catch a highlight, bottom edges sit in shadow, insets reverse this. Consistent implied light is what makes glass, buttons, and cards read as physical objects rather than flat rectangles.

### 1.3 Rule of thumb for the agent

> If a value could have been the framework default, change it on purpose or confirm it is genuinely right. Defaults are how a site reads as generic.

---

## 2. Motion design principles

The single most cited expert here is **Emil Kowalski** (design engineer at Linear, ex-Vercel; creator of Sonner, Vaul, and the "Animations on the Web" course). His framework is the spine of this section. (Sources: Kowalski, "Great Animations"; emilkowalski/skills SKILL.md.)

### 2.1 Easing: the most important variable

- **Default to ease-out for UI.** It "starts fast and slows down at the end, which gives the impression of a quick response." This is the workhorse for almost every enter/hover/press. (Kowalski.)
- **Never use ease-in for UI.** It delays the initial movement, which makes the interface feel sluggish and unresponsive. (Kowalski.) Ease-in is acceptable only for exits where something is leaving the screen.
- **Avoid the built-in CSS keywords as final values.** `ease`, `ease-in-out`, and friends "lack strength." Use tuned cubic-beziers instead. (Kowalski.)
- **Workhorse cubic-bezier values** (from Kowalski's skill):
  - Strong ease-out for UI interactions: `cubic-bezier(0.23, 1, 0.32, 1)`
  - Strong ease-in-out for on-screen movement: `cubic-bezier(0.77, 0, 0.175, 1)`
  - iOS-like drawer/sheet curve: `cubic-bezier(0.32, 0.72, 0, 1)`
- **Springs for anything interruptible or gestural** (drag, sheets, things the user can grab mid-flight). Springs carry velocity instead of restarting, which feels physical.
  - Apple-style, recommended: `{ type: "spring", duration: 0.5, bounce: 0.2 }`
  - Classic physics form: `{ mass: 1, stiffness: 100, damping: 10 }`
  - Keep bounce subtle: **0.1 to 0.3.** Higher reads as cartoonish.

### 2.2 Duration: norms in milliseconds

Keep UI motion **under 300ms** as a default ceiling; a 180ms transition feels more responsive than a 400ms one. (Kowalski.)

| Element | Duration |
|---|---|
| Button / press feedback | 100 to 160ms |
| Tooltips, small popovers | 125 to 200ms |
| Dropdowns, selects, menus | 150 to 250ms |
| Modals, drawers, sheets | 200 to 500ms (larger travel justifies longer) |

Macro/marketing reveals (hero entrances, large scroll scenes) can run longer (400 to 800ms+) because they are rare and emphasize elegance over snappiness. The "under 300ms" rule is for **functional** UI, not cinematic page moments.

**Asymmetric timing.** Make the deliberate part slow and the system response fast. A hold-to-confirm might fill over ~2s linear, but the release/cancel snaps back in ~200ms ease-out. Slow where the user decides; fast where the system responds. (Kowalski.)

### 2.3 When NOT to animate (the defining principle)

Emil's signature contribution is restraint: "the goal is not to animate for animation's sake, it's to build great user interfaces." Decide by **frequency**:

- **100+ times/day** (keyboard shortcuts, command menu, core navigation): **no animation.** Removing motion from high-frequency keyboard actions makes the tool feel dramatically faster despite identical execution speed. (Freiberg, Kowalski.)
- **Tens of times/day** (hovers): minimal, fast, or none.
- **Occasional** (modals, toasts, tab switches): standard tuned animation.
- **Rare** (onboarding, success/celebration, first-run): room for delight.

Valid reasons to animate at all: spatial continuity (a toast slides from where it lives), state indication (a morphing icon), feature explanation (marketing), input feedback (press), and preventing a jarring instant change. If a motion does none of these, cut it.

### 2.4 The 12 principles of animation, applied to UI

Disney's 12 principles (Thomas and Johnston, "The Illusion of Life") map onto interface motion. The recurring caution: aim for **believability, not Looney Tunes.** (Sources: IxDF; Interface Wiki; Pluralsight.)

- **Squash & stretch**: subtle scale on press/release makes elements feel tactile and alive. A button at `scale(0.97)` on `:active` is squash done tastefully. Overdo it and pro software looks cartoonish.
- **Anticipation**: a tiny pre-movement that primes the user for what is about to happen. Hover states are anticipation: they preview the click. A drawer can pull back a hair before sliding out.
- **Follow-through & overlap**: elements do not all stop at once. A sheet settles, its content arrives a beat later. This is where gentle spring overshoot lives.
- **Staging**: direct attention to one thing at a time; do not animate everything simultaneously.
- **Slow in / slow out (easing)**: covered above. This is the most directly transferable principle.
- **Arcs**: natural motion curves rather than dead-straight linear paths (especially for larger, more organic movements).
- **Secondary action**: a supporting motion that reinforces the main one (an icon rotating as a panel opens).
- **Timing**: tune per interaction type, per the duration table.
- **Exaggeration**: in UI, this means just enough emphasis to be felt, not seen as a stunt.
- **Appeal**: the overall cohesion that makes motion feel crafted.

### 2.5 Staggering and choreography (orchestrating many elements)

- **Stagger delay: 30 to 80ms between items.** Longer feels slow and laborious. (Kowalski.)
- Stagger is **decorative**: never block interaction while a stagger plays. The user must be able to click item 5 before item 12 has finished entering.
- Choreograph by hierarchy: the primary element leads, supporting elements follow with offset and slightly different (usually shorter) durations. This creates the "everything moves together but not in lockstep" feel.
- For list/grid reveals, cap total orchestration time. If 30 items each add 60ms, the last one starts ~1.8s in, which feels broken. Either cap the number that stagger, or shrink the per-item delay as count grows.

### 2.6 Continuity and shared-element motion

When the same conceptual object exists in two states (a card that expands into a detail view, a thumbnail that becomes a hero), animate it as **one continuous object** rather than fading one out and another in. This shared-element/morph continuity is a hallmark of high-end motion. Apple's app-launch animations originate from the exact source (icon, Dynamic Island, App Switcher) to preserve the object's identity. (Freiberg.)

---

## 3. Scroll-driven storytelling (scrollytelling)

Scrollytelling uses scroll position as the primary input to control narrative progression: reveal content, trigger animations, and pace attention as the user scrolls, turning passive reading into active, self-paced participation. (Sources: UI-Deploy scrollytelling guide; Lovable scrolling patterns; Motion.dev scroll docs.)

### 3.1 The two fundamental mechanisms (know the difference)

- **Scroll-linked (scrubbed)**: animation progress is tied 1:1 to scroll position. Scroll up and it reverses; the user "owns" the playhead. Use for parallax, progress indicators, pinned scenes where an element morphs as you scroll through it. Best implemented with the native CSS `scroll-timeline` / `animation-timeline` where supported, or GSAP ScrollTrigger with `scrub: true`, or Motion's `useScroll`.
- **Scroll-triggered (one-shot)**: an animation fires once when an element crosses a threshold and then plays on its own clock (ease-out, ~300 to 600ms). Use for reveal-on-enter (text, cards, images fading/sliding up). Best implemented with `IntersectionObserver` (or Scrollama.js, a light wrapper around it).

Rule of thumb: **trigger for reveals, link for scenes.** Reveals should not be scrubbed (scrubbing a fade as the user scrolls feels mushy and laggy). Cinematic transformations should be scrubbed so the user controls the pace.

### 3.2 Section-by-section structure of a great landing page

A premium landing page is a paced narrative, not a stack of equal blocks. A reliable arc:

1. **Hero**: the one-line promise plus the single strongest visual. Big editorial type, immediate brand. Minimal motion beyond a confident entrance and maybe a subtle ambient/mouse-reactive background.
2. **Proof / logos**: quiet trust band, low contrast, often a slow marquee.
3. **The core "scene" / product demo**: the centerpiece. Often a **pinned (sticky) section** where the product visual stays fixed while captions or steps advance with scroll. This is where scrubbed scroll-linked motion earns its keep.
4. **Feature reveals**: alternating layout, each feature entering on scroll-trigger. Vary the rhythm; do not animate every feature identically.
5. **Depth / philosophy beat**: a slower, more atmospheric section (large quote, ambient gradient) to give the eye a rest and the story a breath.
6. **CTA**: confident, high-contrast, calm. Do not gimmick the conversion moment.

### 3.3 Pacing rules

- **Sticky/pinned scenes** create a focal point: one element stays anchored while context changes around it. This is the strongest scrollytelling device. Give each pinned scene enough scroll distance to read (a common heuristic is 100vh to 300vh of pin length per scene depending on how much happens).
- **Stagger text reveals** to pace attention: paragraphs or lines enter as they hit the viewport rather than all at once. (Maglr.)
- **One narrative idea per scene.** If a scene tries to say three things, split it.
- **Do not animate above the fold on load and below the fold on scroll with the same effect**; the hero earns a bespoke entrance, the rest share a quieter reveal language.

### 3.4 Parallax for depth (use sparingly)

Parallax (background and foreground moving at different speeds) creates a 3D-like sense of depth and guides attention. **But**: "an entire page of competing parallax layers feels gimmicky and disorienting," and parallax can trigger vestibular issues (dizziness, nausea, migraine). Guidance: **limit to one subtle parallax effect per page maximum**, keep speed deltas small, and always honor reduced-motion. (UXPin; Maglr; Justinmind.)

---

## 4. Depth & near-3D feel without literal 3D

You can get the premium "almost three-dimensional" feel using only CSS/JS layering, not WebGL. The illusion comes from **differential motion, consistent light, and layered blur**.

### 4.1 Layered parallax and perspective

- Stack elements on distinct depth planes and move them at different rates with cursor or scroll. Assigning speed multipliers per layer (for example background 0.75x, foreground 1.5 to 2x) yields convincing pseudo-3D depth "without heavy WebGL overhead." (FreeFrontend; ArpaTech.)
- **Mouse-reactive parallax**: layers shift/tilt as the cursor moves, which makes a static hero feel alive and responsive. Map cursor delta to small translate/rotate values on each layer (closer layers move more). Keep the max offset small (a few px to a couple dozen px) so it reads as subtle depth, not a funhouse.
- **CSS 3D transforms** (`perspective`, `rotateX/Y`, `translateZ`) on cards give real perspective tilt (the "tilt card" effect) without any 3D engine. Keep tilt angles modest (roughly 4 to 12 degrees) and add a moving specular highlight for realism.

### 4.2 Shadows, elevation, and light

- Build a **shadow elevation scale** (resting, hover, floating, modal) rather than one shadow. Higher elevation = larger, softer, more spread shadow plus often a lift in position.
- **Layer multiple shadows** for realism: a tight, darker contact shadow plus a wider, softer ambient shadow reads far more real than a single blur. (This mirrors how real objects cast both.)
- Use **consistent implied light direction.** Darker color on lower layers reinforces depth. (CreativeBloq.) Top highlight + bottom shadow on raised elements; reverse for insets.

### 4.3 Glass, blur, and gradient depth

- **Glassmorphism / backdrop-blur**: a translucent panel with `backdrop-filter: blur()` over a colorful or moving background separates planes and signals "floating above." On dark UIs, pair with ambient color orbs behind the glass ("dark glassmorphism"). (Medium, MustBeWebCode.)
- **Ambient gradient orbs**: large, heavily-blurred radial color blobs drifting slowly behind content create atmosphere and depth. Keep them low-saturation and slow.
- **Grain over gradients** kills banding and adds a tactile surface, which paradoxically reads as more "physical" and higher-end. (DesignRush.)

### 4.4 Mouse-reactive and magnetic micro-effects

- **Magnetic elements**: buttons/links that gently translate toward the cursor as it approaches, then snap back on exit. Keep pull radius and max offset small; ease back with a spring. This is a signature awwwards micro-delight.
- **Custom cursors / cursor followers**: a trailing dot or a cursor that grows over interactive targets. Powerful but easy to overdo; must never hurt usability or hide the real pointer affordance.
- **Spotlight / glow-follows-cursor** on cards (a radial highlight tracking the mouse over a card grid) is a cheap, high-impact depth/lighting effect.

Gate all of these behind `@media (hover: hover) and (pointer: fine)` so touch devices do not get broken pseudo-hover states. (Kowalski.)

---

## 5. Micro-interactions & feedback

Micro-interactions are where "expensive" is most felt per byte. The standard is that **every interactive element has six fully-designed states**: default, hover, focus (keyboard), active (pressed), disabled, loading. (Mantlr.)

### 5.1 Concrete patterns (from Kowalski's skill)

- **Press feedback**: `transform: scale(0.97)` on `:active`, `transition: transform 160ms ease-out`. Instant tactile confirmation the input registered.
- **Never animate from `scale(0)`.** Nothing in reality vanishes to nothing. Enter from `scale(0.95)` + `opacity: 0` instead. Same for exits.
- **Origin-aware popovers**: set `transform-origin` to the trigger location so the popover grows out of its button. Exception: modals stay centered.
- **Tooltip delay logic**: the first tooltip in a group delays (to prevent accidental triggers); once one is open, adjacent tooltips appear instantly with no animation. This is a classic "invisible detail."
- **Blur to mask imperfect crossfades**: a subtle `filter: blur(2px)` during a state crossfade blends the two states so the eye reads it as a smooth morph (keep under ~20px).
- **clip-path reveals**: animate `clip-path: inset(...)` for wipes, hold-to-delete fills, and comparison sliders without extra DOM.

### 5.2 Hover states

- Make hovers **fast** (100 to 200ms) and reversible. The hover is anticipation for the click, so it should preview the action (lift, brighten, reveal an arrow).
- Hovers fire tens of times a day, so keep them cheap and never block.
- Avoid hover effects that shift layout (they cause neighbor jank and reflow). Animate `transform`/`opacity`/`filter`, not size or position-in-flow.

### 5.3 What "delight" means and where to spend it

Delight is a **rare reward**, not a constant. Spend it where interactions are infrequent and emotionally meaningful: a successful submission, completing onboarding, a celebratory state, a first-run moment. Do not spend delight on things users do dozens or hundreds of times a day; there, delight becomes friction. (Kowalski's frequency framework.)

### 5.4 Gesture/drag feel (for interactive demos and mobile)

- **Velocity-based dismissal**: track `velocity = |dragDistance| / elapsedTime`; dismiss on a fast flick (threshold around 0.11) even if the distance threshold was not met. Quick flicks should work. (Kowalski.)
- **Interruptible**: the user can grab and redirect mid-animation; never force completion. (Freiberg: "flipping a page in a book is interruptible.")
- **Lightweight vs destructive**: lightweight overlays can trigger partway through a swipe; destructive actions require explicit completion to avoid accidents.

---

## 6. Typography & color for premium feel

### 6.1 Typography

- **One family, 4 to 6 sizes max.** Discipline reads as confidence. (Mantlr.) The reference families: Linear uses Inter (Rasmus Andersson), Vercel uses Geist (with Basement Studio), Stripe uses Söhne (Klim Type Foundry). The lesson is not the specific font but the commitment to one well-made family used consistently.
- **A modular type scale.** Pick a base body size, step headings by a fixed ratio so H6 to H1 feel related. Ratios: ~1.2 to 1.25 for restrained, readable hierarchy; up to **1.333 to 1.618** for dramatic, marketing-grade contrast between body and display. (Design.dev; Design Shack.) Marketing hero type can step up an extra notch beyond the in-app scale.
- **Large editorial type as the hero.** Oversized, high-contrast display type conveys confidence and instantly reads premium. Body base is often **18px or larger** on modern marketing sites. (Design Shack.)
- **Tracking (letter-spacing) by size**: tighten large display type (negative tracking, roughly -0.01em to -0.04em) so big headlines feel set, not loose; slightly loosen small caps and all-caps labels (positive tracking) for legibility. This per-size tuning is a strong craft tell.
- **Variable fonts**: ship one file, get many weights/widths/optical sizes, and enable smooth weight/width transitions without multiple downloads. Use the optical-size axis so small text and display text are each tuned. (Studio Ubique; Bluetext.)
- **Line length and leading**: target ~60 to 75 characters per line for body; tighten leading on large headings (they need less), open it on body.
- **Numbers**: use tabular figures for anything that aligns in columns or animates (counters, prices, stats) so digits do not jitter.

### 6.2 Color

- **Use color for meaning, not decoration.** Build a tight neutral ramp (often 9 to 12 steps from near-black to near-white), add one brand hue, add semantic colors (danger/success/warning/info). Keep most of the surface near-neutral so the brand color and semantics carry weight. (Mantlr.)
- **Dark mode**: avoid pure `#000` for large surfaces; use a very dark neutral (slightly blue or warm) so elevation and shadows can read. Dark surfaces feel premium, focused, and reduce eye strain, and they save power on OLED. Use deep, slightly-shifted hues for gradients (purples, blues, muted tones) that transition subtly. (Colorhero; DesignRush.) On dark, raise text contrast carefully and use lighter alphas (not solid grays) for secondary text and borders so the surface stays cohesive.
- **Gradients done well**: keep them **subtle and nearly imperceptible** for surfaces ("add depth without being obvious"); reserve vivid mesh/multi-stop gradients for intentional accents (a hero, a CTA glow, a logomark). Add grain/noise to defeat banding. Layer gradients with blend modes and masks for richness rather than one flat ramp. (DesignRush; Colorhero.)
- **Contrast and accessibility**: maintain WCAG contrast for text (4.5:1 body, 3:1 large). Premium does not mean low-contrast/illegible; it means controlled contrast where it counts.

---

## 7. Restraint, performance perception, and accessibility

### 7.1 The 60fps non-negotiable

If motion does not run at **60fps, every other principle is moot.** (Kowalski.) Concretely:

- **Only animate `transform` and `opacity`** (and `filter` with care). They are compositor/GPU-friendly. Never animate `width`, `height`, `top`, `left`, `margin`, `padding`: those trigger layout recalculation for the element and all children, which janks. (Kowalski.)
- **CSS / Web Animations API beat JS on a busy main thread.** When the page is loading or running heavy scripts, CSS animations run off the main thread and stay smooth while `requestAnimationFrame`-driven JS animations drop frames. Prefer CSS or the Web Animations API (`element.animate([...], { duration, easing, fill: 'forwards' })`) for hardware acceleration. (Kowalski.)
- **Framer Motion caveat**: shorthand props (`x`, `y`, `scale`) animate on the main thread; pass the full transform string (`transform: "translateX(100px)"`) to stay GPU-accelerated. (Kowalski.)
- **`@starting-style`** enables CSS-only enter animations (no JS "mounted" hack):
  ```css
  .toast {
    opacity: 1; transform: translateY(0);
    transition: opacity 400ms ease, transform 400ms ease;
    @starting-style { opacity: 0; transform: translateY(100%); }
  }
  ```

### 7.2 Perceived performance

- **Removing animation can feel faster** than adding it, especially on high-frequency actions. Snappy beats smooth for things users do constantly. (Freiberg, Kowalski.)
- Loading should feel **under ~100ms perceived** or be intentionally, calmly staggered (skeletons, optimistic UI). (Mantlr.)
- **Optimistic UI**: respond instantly to the user's action and reconcile with the server after. The interface should never feel like it is waiting on the network for feedback.

### 7.3 Accessibility (mandatory, not optional)

- **`prefers-reduced-motion`**: honor it everywhere. The correct behavior is usually not "remove all animation" but "remove movement/position/parallax and keep opacity and color transitions that aid comprehension." (Kowalski.)
  ```css
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
  }
  ```
  Then selectively re-enable gentle opacity fades where they help.
- **Gate hover effects** behind `@media (hover: hover) and (pointer: fine)` so touch devices do not get stuck pseudo-hover states. (Kowalski.)
- **Keyboard and focus**: visible, well-designed focus states (not the default ring, but not removed either). Focus is one of the six required states.
- **Parallax and vestibular safety**: parallax can cause dizziness/nausea/migraine; cap it (one subtle effect per page) and disable under reduced-motion. (Maglr.)

### 7.4 The impressive/gimmicky line

Ask of every effect: does it (a) communicate state, (b) preserve spatial continuity, (c) reveal/explain, or (d) reward a rare moment? If yes, keep it. If it exists only to be seen, cut it. Restraint is the premium signal; a calm, fast, correct interface out-classes a busy one.

---

## 8. Anti-patterns (what makes interactive sites feel cheap, dated, or annoying)

- **Scroll-jacking**: hijacking the native scroll to force a pace or a horizontal section the user did not ask for. Breaks expectations, hurts accessibility, and feels broken on trackpads/keyboards. Use scrubbed scroll-*linked* effects that still respect native scroll, not scroll *hijacking*.
- **Parallax everywhere**: "an entire page of competing parallax layers feels gimmicky and disorienting." (UXPin.) One subtle layer, max.
- **Animating high-frequency actions**: putting transitions on keyboard shortcuts, command menus, or core nav makes the whole product feel slow. (Kowalski, Freiberg.)
- **Slow animations**: anything functional over ~300ms feels laggy. Slow exits and slow modals are a common tell. (Kowalski.)
- **Using `ease-in` or default `ease`**: sluggish starts and weak curves read as unpolished. (Kowalski.)
- **Animating layout properties** (`width`/`height`/`top`/`left`/`margin`): janks below 60fps and shifts neighbors. (Kowalski.)
- **`scale(0)` enters/exits**: things popping from/to literal nothing look cheap; start/end at `scale(0.95)`. (Kowalski.)
- **Default heavy shadows and default borders**: the `0 4px 6px rgba(0,0,0,.1)` look plus 1px solid gray everywhere is the template signature.
- **Banding gradients with no grain**, and vivid decorative gradients on every surface.
- **Too many fonts / too many weights / untuned tracking**, and decorative (meaningless) color.
- **Custom cursors and magnetic effects that hurt usability** (hiding the real pointer, making targets harder to hit, lagging behind input).
- **Reveal-on-scroll on everything**, so the page cannot be read without waiting for content to fade in; and re-triggering reveals every time an element re-enters the viewport.
- **Ignoring `prefers-reduced-motion`** and ignoring touch (broken hover on tap).
- **Stagger delays too long** (content trickles in over seconds) or blocking interaction during a stagger. (Kowalski: 30 to 80ms, non-blocking.)
- **Autoplay everything**: looping background video at high bitrate, sound, motion that never rests. Premium sites give the eye places to rest.

---

## Quick-reference cheat sheet (for the agent)

- Default UI easing: `cubic-bezier(0.23, 1, 0.32, 1)` (strong ease-out). Never `ease-in` for UI.
- Drawer/sheet easing: `cubic-bezier(0.32, 0.72, 0, 1)`. Movement across screen: `cubic-bezier(0.77, 0, 0.175, 1)`.
- Springs: `{ duration: 0.5, bounce: 0.2 }`, bounce in 0.1 to 0.3, for anything draggable/interruptible.
- Durations: press 100 to 160ms, tooltip 125 to 200ms, dropdown 150 to 250ms, modal 200 to 500ms. Functional UI ceiling ~300ms. Macro/marketing reveals 400 to 800ms+.
- Stagger: 30 to 80ms, non-blocking, capped total.
- Animate only `transform`/`opacity` (and `filter` carefully). Target 60fps. Prefer CSS / Web Animations API.
- Press feedback: `scale(0.97)` on `:active`, 160ms ease-out. Enter from `scale(0.95)` + `opacity:0`, never `scale(0)`.
- Six states per interactive element: default, hover, focus, active, disabled, loading.
- Hairlines at 0.5 to 1px low alpha. Layered shadows (contact + ambient). Consistent top-light.
- Type: one family, 4 to 6 sizes, modular scale (1.2 to 1.25 restrained, up to ~1.618 for marketing), tighten display tracking, variable fonts with optical size, body 18px+.
- Color: tight neutral ramp + 1 brand hue + semantics; color for meaning. Dark mode not pure black; subtle gradients with grain.
- Depth without 3D: layered/mouse parallax (small offsets, gated to fine pointer), backdrop-blur glass, ambient blurred gradient orbs, CSS 3D tilt (4 to 12 deg).
- Always: `prefers-reduced-motion`, `@media (hover: hover) and (pointer: fine)`, optimistic UI, one subtle parallax max.
- The meta-rule: change defaults on purpose; accumulate many small correct details; spend delight rarely; cut motion that does not communicate, preserve continuity, explain, or reward.

---

## Sources

Read and used directly:

- Emil Kowalski, "Great Animations" (rules: ease-out, under 300ms, 60fps, transform/opacity only, interruptibility, reduced-motion). https://emilkowal.ski/ui/great-animations
- Emil Kowalski, design-eng SKILL.md (cubic-bezier values, duration table, spring settings, stagger 30 to 80ms, scale(0.97) press, @starting-style, clip-path, velocity dismissal, Framer Motion GPU caveat, hover gating). https://github.com/emilkowalski/skills/blob/main/skills/emil-design-eng/SKILL.md
- Rauno Freiberg, "Invisible Details of Interaction Design" (timing/physics, interruptibility, origin-aware motion, perceived performance via removing animation, optical detail, Fitts's law). https://every.to/p/invisible-details-of-interaction-design
- Mantlr, "How Stripe, Linear, and Vercel Ship Premium UI" (one family 4 to 6 sizes, color for meaning, six interactive states, interaction density, 0.5 to 1px low-alpha hairlines, sub-100ms perceived loading). https://mantlr.com/blog/stripe-linear-vercel-premium-ui
- UI-Deploy, "Complete Scrollytelling Guide (2025)" (scroll-as-input, scrubbed vs triggered, pinned sections, GSAP ScrollTrigger / Scrollama). https://ui-deploy.com/blog/complete-scrollytelling-guide-how-to-create-interactive-web-narratives-2025
- Lovable, "Scrolling Designs: 8 Patterns and When to Use Each (2026)" (sticky/pinned focal points, pattern selection). https://lovable.dev/guides/scrolling-designs-patterns-when-to-use
- Maglr, "8 scroll animations every digital storyteller should know" (staggered text reveals, parallax cautions, reduced-motion). https://www.maglr.com/blog/scroll-animations
- UXPin, "Creative Website Scrolling Patterns (2026)" (parallax-everywhere is gimmicky; scroll-jacking cautions). https://www.uxpin.com/studio/blog/4-types-creative-website-scrolling-patterns/
- Interaction Design Foundation, "UI Animation: Apply Disney's 12 Principles to UI" (squash/stretch, anticipation, follow-through, believability not Looney Tunes). https://www.interaction-design.org/literature/article/ui-animation-how-to-apply-disney-s-12-principles-of-animation-to-ui-design
- Pluralsight, "Understanding the 12 Principles of Animation." https://www.pluralsight.com/resources/blog/software-development/understanding-12-principles-animation
- DesignRush, "Gradient Design: Trends & Tips" (grain/noise gradients, layering, blend modes, masking). https://www.designrush.com/agency/graphic-design/trends/gradient-design
- Colorhero, "Dark Mode Color Palettes for Modern Websites (2025)" (dark mode premium feel, near-imperceptible gradients, deep hues). https://colorhero.io/blog/dark-mode-color-palettes-2025
- Medium (MustBeWebCode), "Dark Glassmorphism" (ambient color orbs behind glass, backdrop-blur depth). https://medium.com/@developer_89726/dark-glassmorphism-the-aesthetic-that-will-define-ui-in-2026-93aa4153088f
- Design Shack, "Design Trend: Large Typography Scales" (oversized display type, 18px+ body, cohesion). https://designshack.net/articles/trends/large-typography-scales/
- Design.dev, "Web Typography Guide: Fonts & Hierarchy" (modular scale ratios, hierarchy). https://design.dev/guides/typography-web-design/
- Studio Ubique, "Typography in web design: 7 Key Choices for 2025" (variable fonts, performance). https://www.studioubique.com/typography-in-web-design/
- Bluetext, "Typography Trends in Web Design" (variable fonts, editorial type for impact). https://bluetext.com/blog/typography-trends-in-web-design-choosing-fonts-for-impact/
- FreeFrontend, "JavaScript Mouse Interactions" and "JavaScript Scroll Effects" (mouse-reactive parallax, layer speed multipliers, cursor effects). https://freefrontend.com/javascript-mouse-interaction/ , https://freefrontend.com/javascript-scroll-effects/
- ArpaTech, "Add 3D Parallax Effect to 2D Images with Depth Map" (pseudo-3D layering without WebGL). https://www.arpatech.com/blog/3d-parallax-effect-2d-images-depth-map/
- Creative Bloq, "Create a mouse-controlled parallax background effect" (per-layer speeds, darker lower layers for depth). https://www.creativebloq.com/how-to/create-a-mouse-controlled-parallax-background-effect
- Justinmind, "Parallax effect website design: best practices and examples" (depth, attention guidance, layering). https://www.justinmind.com/blog/parallax-effect-websites/
- Motion.dev, "React scroll animations: scroll-linked & parallax" (useScroll, scroll-linked vs trigger). https://motion.dev/docs/react-scroll-animations

Background/reference (consulted via search summaries):

- Lobehub / Shyft / vercel-labs open-agents skill listings summarizing Emil Kowalski animation practice.
- Adobe, NYFA, Animaker explainers of the 12 principles of animation.
- SitePoint, "7 Performance Tips for Jank-free JavaScript Animations" (jank definition, GPU properties).
