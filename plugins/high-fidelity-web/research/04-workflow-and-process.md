# 04 - Workflow and Process: How Pros Build High-Fidelity Interactive Sites

Research for the High-Fidelity Interactive Web skill. This document covers the
**workflows, strategies, and processes** that award-winning studios, "design
engineers," and professional designers use to take a vague idea to a polished,
animated, Stripe/Linear/Vercel/Awwwards-caliber site. The goal is to translate
those human workflows into a repeatable sequence an AI coding agent can follow.

Sections 6 (agent-adapted workflow) and 7 (quality bars) are the most
prescriptive, because they directly drive the skill's structure. Read those if
you read nothing else.

---

## 0. TL;DR for the skill author

The professional process is **not** "open Figma, draw pretty pictures, hand off."
The high end of the industry has largely collapsed the design/build handoff into
a single iterative loop driven by a "design engineer" who works in code. The
shape of the work is:

1. **Understand and frame** the specific problem (brief, audience, one big idea).
2. **Mine references** to find a direction, then deliberately depart from them.
3. **Define a language** (visual + motion) as a small system of tokens and rules.
4. **Prototype the risky/expensive parts in code first** (especially motion).
5. **Build component-by-component, in the browser**, iterating tightly.
6. **Polish the unseen details** until it "feels right."
7. **QA like an adversary** and hit hard performance/accessibility bars.

The differentiator at the top is **behavioral richness and obsessive detail**,
not visual density. "The density is in the behavior, not the pixels."
[Mantlr]

---

## 1. The end-to-end process (discovery to QA)

The classic studio pipeline still exists, but the best teams compress it and
loop heavily. Stages and the artifacts each one produces:

### 1.1 Discovery / brief
- **What happens:** Define the problem, audience, goals, constraints, voice, and
  success criteria. The premium-design mindset is to obsess over the *specific*
  case, not the abstract one: "When a user opens this modal from this context,
  how should it feel, and why?" [Mantlr]
- **Artifacts:** A short brief (who it is for, what it must do, what it must feel
  like, constraints, references to beat), a content inventory, and success
  metrics.

### 1.2 Concept and art direction
- **What happens:** Choose a single organizing idea ("the big idea" / "concept")
  and a tone. Define the visual and motion language at a high level before
  pixels. Adrien Vanderpotte frames this as finding a project's "digital
  signature: the singular, reactive behavior that makes a brand feel
  unforgettable." [Codrops/Vanderpotte]
- **Artifacts:** A concept statement (one or two sentences), an art-direction
  note (mood words, the feeling, the metaphor), and a hero idea.

### 1.3 Moodboarding and reference mining
- **What happens:** Collect references that resonate, cluster them, and extract a
  direction. A moodboard "isn't merely a visual collage; it's a strategic
  roadmap" that aligns everyone on tone before prototyping. [Oliinyk; NN/G]
- **Artifacts:** A moodboard (or "cluster" in Cosmos terms) plus a written
  extraction of *what* to take from it (palette, type feeling, motion feeling,
  layout density), explicitly separating "inspiration" from "copy."

### 1.4 Wireframe / structure
- **What happens:** Decide the narrative and section order before visual design.
  Many design engineers skip heavy wireframes (see 5.1), but the *structure* is
  always decided: what story the page tells top to bottom.
- **Artifacts:** A section map / page narrative (hero, build-up, proof,
  resolution, CTA) and a content hierarchy.

### 1.5 Visual design (often still Figma, sometimes code)
- **What happens:** Establish the actual look: type scale, color, spacing,
  grid, key components, the hero composition. At the high end, the designer
  "sketches the start and iterates with a Design Engineer in Figma or code to
  produce the final design." [Vercel]
- **Artifacts:** Key screens or a design-token set, a component inventory, and a
  defined type/color/spacing system.

### 1.6 Motion design / prototyping
- **What happens:** Plan and prototype the motion. Because motion is expensive to
  redo, the rule is to prototype interactions in code, since "animations,
  keyboard controls, and touch are better implemented in code to save the time
  and effort of reimplementing them from a different medium to the web." [Vercel]
  See section 4.
- **Artifacts:** A motion language (easing + timing tokens), a motion board or
  list of choreographed moments, and working code prototypes of the risky parts.

### 1.7 Build
- **What happens:** Implement component-by-component, in the browser, with the
  prototype becoming the production code. Studios optimize for *iteration time*:
  "the more you can do in less time, the better the project will be because this
  allows for more time to improve and iterate upon the details." [Active Theory]
- **Artifacts:** The real site, built on the token system and motion language.

### 1.8 Polish
- **What happens:** Refine the details that no one consciously notices but
  everyone feels. "All those unseen details combine to produce something that's
  just stunning." [Emil Kowalski skill] Rauno describes being "lost in polishing
  that one silly edge case that no one might ever notice." [Rauno/Spaces]
- **Artifacts:** Microstate coverage, refined easing, hairlines, focus rings,
  empty/error states, copy tightening.

### 1.9 QA / performance / accessibility
- **What happens:** Test adversarially and measure. Rauno "tests interactions
  like a QA engineer by clicking aggressively, spamming inputs, and simulating
  slow connections, aiming for 100% reliability." [Rauno/Spaces] Then verify Core
  Web Vitals and accessibility. See section 7.
- **Artifacts:** A QA pass log, Lighthouse/CWV numbers, responsive checks, and a
  reduced-motion / keyboard / screen-reader pass.

---

## 2. Reference mining and inspiration

Pros do not pull "inspiration" randomly. They mine, cluster, and extract a
*direction*, then deliberately depart from it so the output is not generic.

### 2.1 The canonical galleries and what each is for

| Source | Best for | Notes |
|---|---|---|
| **Awwwards** (awwwards.com) | Award-grade interactive/animated sites, motion, WebGL | The benchmark for "is this top tier"; study Site of the Day winners |
| **Godly** (godly.website) | Curated high-end visual + motion web design | Tight curation, strong for hero/section ideas |
| **Refero** (refero.design) | Real product UI flows, screenshots searchable | Good for UX patterns, not just visuals |
| **Land-book** (land-book.com) | Landing pages and homepages, updated daily | Full screenshots; great for landing-page structure [Land-book] |
| **Httpster** | Fresh, often bold/experimental sites | Less filtered, good for breaking out of safe defaults |
| **SiteInspire** (siteinspire.com) | Highly curated, filterable by type/style/tech | Quality-first; filter by style/subject/technology [portalZINE] |
| **Mobbin** (mobbin.com) | 300k+ searchable real app screens and flows | Best for interaction/flow patterns across real products [Mobbin] |
| **Footer.design** | Footers specifically | The most-neglected section; steal structure here |
| **Cosmos** (cosmos.so) | AI-curated visual discovery, "Clusters" not boards | Ad-free, filters out AI slop; build moodboards as clusters [Creative Bloq] |
| **Savee** (savee.com) | Designer-curated visual references, collections | "Build a sharper eye without ads or clutter" [Savee] |
| **Dribbble** | Quick visual sparks | **Limit:** often non-functional "design fiction"; do not copy layouts wholesale. Pros explicitly recommend leaving Dribbble/Behance for real-product sources [UX Planet] |

Rule of thumb the field uses: **Mobbin/Refero for UX research (real products),
Awwwards/Godly for visual ambition, Land-book/Lapa Ninja for landing-page
structure.** [portalZINE]

### 2.2 How pros build a moodboard and extract direction
1. **Collect broadly, then cut hard.** Gather a mix of images, type, color,
   texture, and motion clips that resonate; collecting is "the most fundamental
   step." [search synthesis] Then ruthlessly remove anything off-tone.
2. **Cluster by dimension.** Separate palette, typography, layout/density,
   texture/material, and *motion feeling* into their own groups (Cosmos
   "clusters" formalize this). [Creative Bloq]
3. **Write the extraction.** A moodboard is only useful if you state *what you
   are taking and why*: "this palette's restraint," "this type's confidence,"
   "this motion's weight." This is the "strategic roadmap," not the collage.
   [Oliinyk]
4. **Go outside the web.** The strongest references come from architecture, film,
   typography, product, and physical motion, not from other websites. Vanderpotte
   studies "real-world movement" rather than copying sites. Rauno "time travels
   backwards in the industry, or even away from it." [Codrops; Rauno/Spaces]
5. **Inspiration vs. copy.** "Start by copying things that inspire you" is how
   you *learn* (Rauno), but the deliverable must transform references into a
   distinct direction. Copying a layout = generic; extracting a principle =
   direction.

---

## 3. Art direction and concept

### 3.1 Choosing the big idea
A "concept" is a single organizing thought that every design decision can ladder
up to. The premium teams derive it from the *specific* situation, not a generic
template. The test: can you state it in one sentence, and does it imply a
distinct visual and motion language? Vanderpotte's "digital signature" is the
purest version: one reactive behavior that makes the brand unforgettable.
[Codrops]

### 3.2 Defining a visual and motion language
- **Visual:** one type family (plus mono where needed), a restrained palette used
  for *meaning* not decoration, a spacing scale, and a grid. Premium products
  show "surprising color restraint" (Stripe's dashboard is "mostly neutrals plus
  measured indigo"). Typography is the brand anchor: one family, systemic scale,
  weight, and spacing, "no mixing display fonts." [Mantlr]
- **Motion:** a small set of easing curves and durations applied consistently
  (see section 4). "Motion curves should be designed, not defaulted." [Mantlr]

### 3.3 Tone and the hero / first impression
The hero is the opening line of a novel: it sets tone, evokes emotion, and gives
a reason to keep scrolling. [site123/storytelling] It should carry the concept
immediately. The first impression is where the "big idea" either lands or does
not.

### 3.4 Narrative structure of a landing page
A reliable spine, drawn from storytelling/StoryBrand frameworks:
1. **Hero / opening scene:** the promise, the tone, the one big idea, primary CTA.
2. **Build-up:** the problem and the product as the solution; show, do not tell.
3. **Proof:** features, demos, social proof, logos, testimonials, data.
4. **Resolution:** the transformation / outcome the user gets.
5. **Close:** a confident final CTA and a designed footer.

Key narrative principle: **cast the customer as the hero and the product as the
guide**, which keeps the page empowering rather than self-promotional. [Umbrex;
Alitu/StoryBrand] Visual + motion choices should support the narrative, not fight
it.

---

## 4. Motion choreography planning

Motion is the single biggest differentiator and the most expensive thing to redo,
so it gets planned deliberately.

### 4.1 Plan motion before (and while) building
- **Vocal / gestural prototyping.** Before code, communicate motion intent with
  "whooshes, clicks, and snaps," hand gestures, and mouth sounds to convey the
  "feel" of an animation "before the first line of code is even written."
  [Vanderpotte]
- **Motion boards / reference clips.** Collect short video references of the
  feeling you want (easing weight, snappiness, settle).
- **Prototype the risky parts in code, not in design tools.** Code prototypes
  become production, so "animations, keyboard controls, and touch are better
  implemented in code." [Vercel] After Effects/Principle/Figma prototypes are
  useful for *communication*, but the source of truth is the browser.
- **Embrace mess in R&D.** "The best interactions usually come from a weird
  experiment." Keep a personal library of experimental effects to draw from.
  [Vanderpotte]

### 4.2 Define an easing and timing system (a motion language)
This is the most copy-pasteable part of the skill. From the Emil Kowalski design
engineering rules: [Emil Kowalski skill]

**Easing selection:**
- Entering / exiting element: **ease-out** (starts fast, feels responsive).
- Moving / morphing on screen: **ease-in-out**.
- Hover / color change: **ease**.
- Constant motion: **linear**.
- **Never use ease-in for UI** (starts slow, feels sluggish).

**Recommended custom curves:**
- Strong ease-out: `cubic-bezier(0.23, 1, 0.32, 1)`
- Strong ease-in-out: `cubic-bezier(0.77, 0, 0.175, 1)`
- iOS-like drawer: `cubic-bezier(0.32, 0.72, 0, 1)`

**Timing (durations):**
| Element | Duration |
|---|---|
| Button press feedback | 100 to 160ms |
| Tooltips, small popovers | 125 to 200ms |
| Dropdowns, selects | 150 to 250ms |
| Modals, drawers | 200 to 500ms |

Master rule: **UI animations should stay under ~300ms.** Exit should be faster
than enter.

**Springs** feel more natural than duration-based motion because they simulate
physics and settle on physical parameters rather than a fixed duration. [Emil
Kowalski course]

### 4.3 Choreography patterns
- **Single progress driver.** A common award-site pattern: drive a whole scene
  from one progress number between 0 and 1, tweened by a GSAP timeline with a
  custom ease, and feed that number into shaders/uniforms so the GPU stays
  stateless while GSAP "owns the motion curve." [Codrops/GSAP]
- **Stagger.** Delay between items 30 to 80ms; stagger is decorative and "never
  block interaction while stagger animations are playing." [Emil Kowalski skill]
- **Frequency budget for delight.** Animate based on how often an action happens:
  100+ times/day (shortcuts) = no animation ever; tens/day (hover, nav) = minimal;
  occasional (modals, toasts) = standard; rare/first-time (onboarding,
  celebrations) = room for delight. Never animate keyboard-initiated actions.
  [Emil Kowalski skill]

---

## 5. The design-engineer workflow

The "design engineer" is the role this skill should emulate: someone who designs
*in code, in the browser*, collapsing the handoff.

### 5.1 Design in code / in the browser
- The handoff is eliminated: "a Designer sketches the start and iterates with a
  Design Engineer in Figma or code to produce the final design." [Vercel]
- Rauno skips wireframes/mockups and treats **code as the design material**: like
  prototyping a chair out of physical materials to reveal strengths and limits,
  "with software, the material is code." His advice: "Work with the material...
  the materials you need to master are HTML, CSS, and JavaScript." [Rauno/Spaces]
- The reason: interactions (animation, keyboard, touch, gesture) cannot be
  faithfully evaluated in static tools. You have to feel them running.

### 5.2 Build a design system + tokens first
- Establish tokens before components: type scale, spacing scale, color (semantic,
  not decorative), radii, shadows/hairlines, easing curves, durations. These
  become the shared vocabulary so everything stays consistent. [Mantlr; Vercel]
- Many teams pair a component registry (e.g. shadcn/ui) with design tokens to get
  fast, consistent prototyping. [Vercel]

### 5.3 Component-by-component, with full microstate coverage
- Build one component at a time, but build it *completely*. Premium UI requires
  **six distinct microstates** per interactive element: default, hover, focus,
  active, disabled, loading. "The density is in the behavior, not the pixels."
  [Mantlr]

### 5.4 The iteration loop and progressive enhancement
- **Iterate to greatness.** Balance shipping speed with quality, avoiding
  perfectionism that blocks delivery. [Vercel] Optimize iteration time so there
  is room to refine details. [Active Theory]
- **Progressive enhancement.** Start with CSS for performance, escalate to GSAP
  for choreography, and to Three.js/OGL/WebGL only when the concept justifies the
  weight. "A tool is only as good as the problem it solves." [Vanderpotte] (This
  matches the skill's stated default of vanilla JS + GSAP + Tailwind, escalating
  to React/Motion/R3F.)

### 5.5 Taste, and how it is developed and applied
- **Taste is trained, not innate.** "Good taste is not personal preference. It is
  a trained instinct." [Emil Kowalski skill]
- **How to train it:** copy things that inspire you (then say thank you), study
  cross-disciplinary and historical work, and notice what creators you respect
  are excited about. [Rauno/Spaces] Build useless R&D constantly; "those small,
  'useless' chunks of R&D code... are often the things that will define your
  professional work a year from now." [Vanderpotte]
- **How to apply it:** obsess over the specific case, design every microstate,
  and refine the unseen details until it feels right.

---

## 6. Adapting this for an AI agent (MOST IMPORTANT)

Translate the human workflow into an explicit, phased sequence with checklists,
self-critique gates, and human-taste checkpoints. The agent should move through
these phases in order, producing the listed artifact at each gate, and **pause
for a human taste check at the marked checkpoints**.

### Phase 0 - Frame the problem (artifact: BRIEF)
- [ ] Capture: who it is for, what it must do, what it must *feel* like, hard
  constraints (stack, brand, content), and 2 to 3 reference sites to beat.
- [ ] Write the success criteria, including the single feeling the hero must land.
- [ ] If the idea is vague, ask 2 to 3 sharp clarifying questions, then proceed.
- **Anti-generic guard:** force a *specific* feeling word (e.g. "precise and
  weighty," not "modern and clean"). Reject generic adjectives.

### Phase 1 - Mine references and extract direction (artifact: MOODBOARD + EXTRACTION)
- [ ] Pull references from the right galleries for the job (Awwwards/Godly for
  ambition, Land-book for landing structure, Mobbin/Refero for UX patterns).
- [ ] Cluster by dimension: palette, type, layout/density, texture/material,
  motion feeling.
- [ ] Write the extraction: for each cluster, state *what principle* to take and
  *why* (not which site to copy).
- [ ] Pull at least one non-web reference (architecture, film, product, physical
  motion) to avoid web-cliché output.
- **CHECKPOINT (human taste check #1):** present the concept + direction +
  references before building anything. Cheap to redo here, expensive later.

### Phase 2 - Concept and narrative (artifact: CONCEPT + SECTION MAP)
- [ ] State the big idea in one sentence; confirm it implies a distinct visual
  and motion language.
- [ ] Define the page narrative: hero, build-up, proof, resolution, close,
  footer. Customer is the hero; product is the guide.
- [ ] Define the hero's first-impression moment explicitly.

### Phase 3 - Define the system (artifact: TOKENS + MOTION LANGUAGE)
- [ ] Type: one family + mono; a defined scale, weights, line-heights, tracking.
- [ ] Color: semantic, restrained; neutrals + one or two accents used for meaning.
- [ ] Spacing scale, radii, hairlines (0.5px/1px at low alpha), shadows.
- [ ] Motion tokens: easing curves (use the cubic-beziers in 4.2) + duration
  scale; default ease-out, exit faster than enter, under ~300ms.
- [ ] Pick the stack by ambition: CSS/Tailwind + GSAP by default; escalate to
  React/Motion/Three.js/R3F only if the concept demands it.

### Phase 4 - Prototype the risky parts in code (artifact: MOTION/HERO PROTOTYPE)
- [ ] Identify the 1 to 3 highest-risk or highest-impact interactions (usually
  the hero and the signature motion).
- [ ] Build them in the browser first; the prototype is production-bound.
- [ ] Apply the frequency budget: more delight for rare moments, none for
  high-frequency/keyboard actions.
- **CHECKPOINT (human taste check #2):** show the hero + signature motion running.
  If the hero does not land, do not proceed to full build.

### Phase 5 - Build component-by-component (artifact: SITE)
- [ ] Build on tokens; one component at a time but each *complete*.
- [ ] Every interactive element gets all six microstates: default, hover, focus,
  active, disabled, loading.
- [ ] Gate hover behind `@media (hover: hover) and (pointer: fine)`.
- [ ] Design empty/error/loading states deliberately (they are high-trust
  moments), not stubbed.
- [ ] Build the footer with the same care as the hero.

### Phase 6 - Polish (artifact: POLISH PASS)
- [ ] Animate only `transform` and `opacity`; never `transition: all`; specify
  exact properties.
- [ ] Never enter from `scale(0)`; start at `scale(0.9)`+ with opacity.
- [ ] Popovers scale from their trigger origin; modals stay centered.
- [ ] Designed focus rings (not browser default), high-contrast.
- [ ] Tabular numbers for data, mono for code/IDs.
- [ ] Tighten copy; remove filler; check rhythm and alignment.

### Phase 7 - QA like an adversary (artifact: QA LOG + METRICS)
- [ ] Click aggressively, spam inputs, interrupt animations mid-flight, simulate
  slow connections; aim for 100% reliability. [Rauno]
- [ ] CSS transitions (interruptible) over keyframes (restart from zero) for
  retargetable motion.
- [ ] Responsive: phone, tablet, desktop, large desktop.
- [ ] Reduced motion: fewer/gentler animations, not zero (keep opacity/color).
- [ ] Keyboard nav + visible focus order; screen-reader pass on key flows.
- [ ] Measure Core Web Vitals (see section 7) and fix regressions.
- **CHECKPOINT (human taste check #3):** final review against the quality bar.

### Self-critique protocol (run between phases, agent talks to itself)
1. **Concept fidelity:** does every section ladder up to the one big idea? If a
   section could appear on any other site, it is generic. Fix or cut it.
2. **Reference test:** "Would this earn a second look on Awwwards/Godly, or is it
   a safe template?" Name the specific thing that makes it distinct.
3. **Behavior test:** does each interactive element have all six microstates and
   designed motion, or is the polish only skin-deep? "Density is in the behavior."
4. **Unseen-details test:** hairlines, focus rings, empty states, exit easing,
   stagger, copy. List what is still defaulted and fix it.
5. **The "feel" test:** describe the intended feeling in one word; verify the
   running site delivers it. If you cannot, the motion language is wrong.

### How the agent avoids generic output (the core risk)
- Force a *specific* feeling word and a concept sentence up front; reject generic
  adjectives ("clean, modern, sleek").
- Require at least one non-web reference per project.
- Extract *principles* from references, never copy layouts.
- Mandate a signature interaction (the "digital signature") that is unique to
  this project.
- Treat default browser styling (focus rings, spinners, ease-in, `transition:
  all`) as a code smell to be eliminated.
- Spend disproportionate effort on the hero and one signature moment; that is
  what people remember.

---

## 7. Quality bars and critique

Heuristics and checklists pros use to decide if something is "good enough," and
how to give yourself a design critique. Use this as the skill's acceptance gate.

### 7.1 The reproducible quality-bar checklist (visual + interaction)
From the premium-UI teardown of Stripe/Linear/Vercel: [Mantlr; Emil Kowalski skill]
- [ ] **Microstates:** every interactive element has default, hover, focus,
  active, disabled, loading.
- [ ] **Focus rings:** designed, visible, high-contrast; never browser default.
- [ ] **Hairlines:** 0.5px or 1px at low alpha, deliberately placed.
- [ ] **Empty/error states:** designed, not stubbed; treated as high-trust
  moments.
- [ ] **Numerals:** tabular numbers for data; monospace for code/IDs.
- [ ] **Typography:** one family + mono; systemic scale/weight/spacing; no mixed
  display fonts.
- [ ] **Color:** restrained, used for meaning not decoration.
- [ ] **Motion:** curves and durations defined and applied consistently; exit
  faster than enter; under ~300ms for UI; only `transform`/`opacity` animated.
- [ ] **Loading:** intentional (staggered, with motion), not a generic spinner.

### 7.2 Spacing, hierarchy, rhythm
- [ ] Consistent spacing scale; no arbitrary one-off margins.
- [ ] Clear visual hierarchy: one primary action per view; secondary actions
  visually subordinate.
- [ ] Alignment and optical balance check (squint test: does the eye land where
  intended).
- [ ] Generous, deliberate whitespace; density is in behavior, not crowding.

### 7.3 Motion polish (the giveaways of amateur vs. pro)
Common violations and fixes: [Emil Kowalski skill]
| Issue | Fix |
|---|---|
| `transition: all` | Specify exact properties |
| `scale(0)` entry | Start from `scale(0.95)` with opacity |
| `ease-in` on UI | Switch to `ease-out` or a custom curve |
| Animation on keyboard action | Remove entirely |
| Duration > 300ms (UI) | Reduce to 150 to 250ms |
| Hover without media query | Gate behind `@media (hover: hover) and (pointer: fine)` |
| Same enter/exit speed | Make exit faster |
- [ ] Button press: `transform: scale(0.97)` on `:active` (range 0.95 to 0.98).
- [ ] Motion is interruptible and retargetable (transitions over keyframes where
  it matters).

### 7.4 Performance (Core Web Vitals)
Targets and tactics: [Core Web Vitals guides]
- [ ] **LCP < 2.5s** (good). Preload the LCP element; use WebP/AVIF; CDN static
  assets; server response under ~200ms.
- [ ] **INP < 200ms** (good). Keep the main thread free; avoid janky handlers.
- [ ] **CLS < 0.1** (good). Reserve space for media; avoid layout-shifting
  injects.
- [ ] **60fps animation.** Animate only `transform`/`opacity` (skip layout/paint,
  run on GPU). Note: Framer Motion shorthand (`x`, `y`, `scale`) is *not*
  hardware-accelerated by default. [Emil Kowalski skill]
- [ ] Inline critical CSS; lazy-load below-the-fold and heavy WebGL.
- [ ] Measure with Lighthouse / PageSpeed Insights / DevTools. (47% of sites fail
  CWV, so passing is itself a differentiator.) [CWV guides]

### 7.5 Responsiveness
- [ ] Verified at phone, tablet, desktop, and large desktop widths.
- [ ] Touch targets adequate; hover effects gated for touch.
- [ ] Layout, type scale, and motion adapt sensibly (do not just shrink).

### 7.6 Accessibility
- [ ] **Reduced motion:** fewer and gentler animations, not zero; keep
  opacity/color transitions. [Emil Kowalski skill]
- [ ] Keyboard operable; logical focus order; visible focus.
- [ ] Semantic HTML; ARIA only where needed; alt text.
- [ ] Color contrast meets WCAG 2.2; do not rely on color alone for meaning.
- [ ] Screen-reader pass on primary flows.

### 7.7 How to give yourself a design critique
1. **State the intended feeling in one word.** Open the running site. Does it
   deliver that word in the first 3 seconds (the hero/first impression)? [Mantlr;
   storytelling]
2. **Run the generic test.** Could this section live on any other brand's site?
   If yes, it lacks concept fidelity. Make it specific or cut it.
3. **Adversarial QA.** Spam clicks, interrupt animations, throttle the network,
   tab through everything. Anything that breaks fails the bar. [Rauno]
4. **Microstate audit.** Pick three interactive elements at random; confirm all
   six states exist and feel designed.
5. **Unseen-details sweep.** Hairlines, focus rings, exit easing, stagger timing,
   empty states, copy rhythm. List every default still present and fix it.
6. **Numbers gate.** Run Lighthouse; confirm LCP/INP/CLS pass and animations hold
   60fps.
7. **The Awwwards question.** "Would this earn a second look from a jury?" If you
   cannot name the specific thing that makes it distinctive, it is not done.

---

## Sources

Primary sources actually read for this document:

- Vercel, "Design Engineering at Vercel: What we do and how we do it" -
  https://vercel.com/blog/design-engineering-at-vercel
- Emil Kowalski, design engineering skill (SKILL.md), emilkowalski/skills repo -
  https://github.com/emilkowalski/skills/blob/main/skills/emil-design-eng/SKILL.md
- Codrops, "Whooshes, Snaps and Shaders: Adrien Vanderpotte and the Feeling of
  the Interface" -
  https://tympanus.net/codrops/2026/05/27/whooshes-snaps-and-shaders-adrien-vanderpotte-and-the-feeling-of-the-interface/
- Codrops, "From Shader Uniforms to Clip-Path Wipes: How GSAP Drives My
  Portfolio" -
  https://tympanus.net/codrops/2026/05/06/from-shader-uniforms-to-clip-path-wipes-how-gsap-drives-my-portfolio/
- Mantlr, "How Stripe, Linear, and Vercel Ship Premium UI" -
  https://mantlr.com/blog/stripe-linear-vercel-premium-ui
- Spaces / Lovers Magazine, "Interview with Rauno Freiberg, Design Engineer at
  Vercel" - https://spaces.is/loversmagazine/interviews/rauno-freiberg
- Communication Arts, feature on Active Theory -
  https://www.commarts.com/features/active-theory
- NN/G, "Mood Boards in UX: How and Why to Use Them" -
  https://www.nngroup.com/articles/mood-boards/
- Taras Oliinyk, "The Art and Science Behind Moodboard Design" -
  https://oliinykkdesign.medium.com/the-art-and-science-behind-moodboard-design-a8cab507b6f0
- portalZINE, "Top 15 UI/UX Design Inspiration Websites" -
  https://portalzine.de/top-15-ui-ux-design-inspiration-websites-in-2025/
- Land-book - https://land-book.com/ ; Mobbin - https://mobbin.com/ ;
  Cosmos - https://www.cosmos.so/ ; Savee - https://savee.com/
- Creative Bloq, "How to use Cosmos" -
  https://www.creativebloq.com/design/social-media/how-to-use-cosmos-a-beginners-guide-to-the-social-media-platform-made-for-creatives
- UX Planet, "Stop using Dribbble & Behance... Use these websites instead" -
  https://uxplanet.org/stop-using-dribbble-behance-to-find-design-inspiration-use-these-15-websites-instead-b3a200c82776
- Umbrex, "Hero's Journey Storytelling Structure (for brands)" -
  https://umbrex.com/resources/frameworks/marketing-frameworks/heros-journey-storytelling-structure-for-brands/
- Alitu, "How to Use the StoryBrand Framework... Landing Page" -
  https://alitu.com/creator/content-creation/storybrand-framework/
- site123, "The Art of Storytelling in Landing Page Design" -
  https://www.site123.com/learn/the-art-of-storytelling-in-landing-page-design
- senorit.de, "Core Web Vitals 2026: INP, LCP, CLS Optimization Guide" -
  https://senorit.de/en/blog/core-web-vitals-2026
- corewebvitals.io, "What Are the Core Web Vitals?" -
  https://www.corewebvitals.io/core-web-vitals
- Emil Kowalski, "Animations on the Web" course overview (easing, springs,
  timing, taste) - https://udcourse.com/product/animations-on-the-web/
