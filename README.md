# claude-plugins

**Claude Code plugins that make Claude build like a senior specialist, not a generic assistant.** Free, open, and grounded in real craft. Add the marketplace once, install what you want.

Here is a site one of these plugins built, start to finish (this is example output, not this repo's own page):

[![Zoomies, an awwwards-grade animated site built with the high-fidelity-web plugin](https://zoomies.garytou.dev/preview/hero.png)](https://zoomies.garytou.dev/)

<sub>☝️ **[Zoomies](https://zoomies.garytou.dev/)**, a "Strava for cats" demo built end to end by the **high-fidelity-web** plugin in this repo. More demos, and the plugins themselves, below.</sub>

## Install

```
/plugin marketplace add garyhtou/claude-plugins
/plugin install high-fidelity-web@garyhtou
/plugin install rails-testing@garyhtou
```

Run `/plugin` to confirm the skills are available.

- **Update to the latest:** `/plugin marketplace update garyhtou` then `/reload-plugins` (installed plugins do not auto-update on push).
- **Manage or remove:** open the interactive `/plugin` menu to enable, disable, or uninstall a plugin, or remove the marketplace entirely.

## Plugins at a glance

| Plugin | Skills it ships | Reach for it when |
| --- | --- | --- |
| **high-fidelity-web** | `high-fidelity-web`, `quality-audit`, `building-3d-for-web` | You want an awwwards-grade animated marketing/landing site: the full brainstorm-to-QA build, a standalone polish audit of an existing page, or believable web 3D (procedural Blender to glTF/GLB to Three.js/R3F). |
| **rails-testing** | `rails-testing` | You want senior-level Rails tests in RSpec or Minitest: behavior-first, non-flaky, N+1/performance-guarded, with a disciplined mocking policy. Composes with `test-driven-development`. |
| **multi-lens-research** | `multi-lens-research` | You need research you can trust, not just plausible-sounding: literature reviews, vendor/tech comparisons, "state of the art" scans, due diligence. Researches from distinct lenses (incl. a contrarian one), verifies load-bearing claims, and reports verified vs. contested vs. unknown with citations. |
| **critical-reasoning** | `critical-reasoning` | You want to know whether a claim, argument, or decision actually holds up: pressure-test a design doc/RFC/PR argument, vet a vendor or benchmark claim, poke holes in your own draft. Tests evidence, then inference, and reports sound / load-bearing flaw / nitpick without the fallacy-labeling slop. |

**For coding agents:** each skill auto-triggers from its `description` when your request matches, so you rarely name a skill, just describe the task ("build a premium landing hero", "write a request spec for checkout", "why does this feel cheap"). Every `SKILL.md` stays lean and loads its heavier `references/` only when a step needs them (progressive disclosure), so the context cost is paid on demand.

---

## high-fidelity-web

**Turn Claude into a design engineer for awwwards-grade, animated marketing and landing sites: the Stripe / Linear / Vercel / Column tier.**

Most AI-built sites look templated: default easing, muddy shadows, untuned type, no microstates, one flashy gimmick over sloppy spacing. This plugin encodes what actually separates premium from generic, so Claude designs (and critiques) like a senior design engineer instead.

- **The full lifecycle, not snippets.** Concept and art direction, design tokens, a real motion language, in-browser prototyping, component build with complete microstate coverage, polish, and adversarial QA, pausing at human taste checkpoints.
- **Concrete craft, not vibes.** Exact easing curves, duration scales, spring params, hairline alphas, and Core Web Vitals targets. Grounded in published work by named practitioners (Emil Kowalski, Rauno Freiberg, the Vercel design-engineering team, GSAP/Codrops), cited in every reference file.
- **A reliability playbook.** The production failure modes that separate a demo from a shipped site: scroll-reveal triggers that fire every time, pinned-scroll bugs, animation lifecycle, layout stability, and hit targets.
- **Framework-agnostic.** Default stack is vanilla JS + GSAP + Tailwind (works in Rails, Astro, plain HTML); escalates to React/Next + Motion or Three.js only when the concept earns it.

It ships **three skills**:

- **`high-fidelity-web`** drives the full brainstorm-to-QA build: brainstorm a concept, define a design-token and motion system, prototype the hero in code, build component-by-component with all six microstates, then polish and QA against a premium bar.
- **`quality-audit`** points at an *existing* site and reports specific, prioritized defects (microstates, motion polish, Core Web Vitals, accessibility) with concrete fixes.
- **`building-3d-for-web`** builds a believable hard-surface 3D model for a WebGL hero, procedural Blender (headless `bpy`) to optimized GLB (Draco) to Three.js / R3F. It carries the hard-won craft (hard-surface realism, the headless Blender gotchas, the GLB pipeline, articulated rigging, a programmatic clip detector) plus ready-to-adapt assets: a Blender build scaffold, a Draco compressor, and a model inspector.

### See it in action

The plugin built a complete example site, **Zoomies ("Strava for cats")**: a fictional product carried with a real, premium aesthetic, the opposite of generic AI output. It is deployed live and the code is open.

### **[Open the live demo &rarr;](https://zoomies.garytou.dev/)** &middot; [Source: garyhtou/zoomies](https://github.com/garyhtou/zoomies)

[![The Zoomies dashboard: count-up stat tiles, an interactive zoomies heatmap, and a category-colored hourly timeline](https://zoomies.garytou.dev/preview/dashboard.png)](https://zoomies.garytou.dev/)

[![The Zoomies leaderboard: cats ranked by weekly zoomie score, with animated bars and count-up scores](https://zoomies.garytou.dev/preview/leaderboard.png)](https://zoomies.garytou.dev/)

Every effect is meaningful, not decorative: a cursor-chasing hero trail that visualizes the exact thing the product sells, animated activity rings, an interactive heatmap with a real data story, a scroll-scrubbed "day in the life," cursor-reactive 3D tilt cards, and full reduced-motion support.

### And in actual 3D

The `building-3d-for-web` skill produced **VANTA Prospector**, a scroll-driven WebGL hero for a fictional autonomous planetary rover: a procedurally-sculpted Blender rover (a ~190 KB Draco GLB) that you orbit, inspect subsystem by subsystem as it deploys its mast, solar wings, and instrument arm, then drive across a procedural surface. No box-of-primitives "toy" look, a real machined spacecraft.

### **[Open the live demo &rarr;](https://vanta.garytou.dev)** &middot; [Source: garyhtou/vanta](https://github.com/garyhtou/vanta)

[![VANTA Prospector: a hyper-real solar exploration rover floating in near-black space beside the headline "The Prospector"](https://vanta.garytou.dev/og.png)](https://vanta.garytou.dev)

### Use it

- **To build:** describe what you want, for example "build a premium landing page for X that feels precise and weighty." The `high-fidelity-web` skill triggers and walks the lifecycle, pausing at three human taste checkpoints.
- **To audit:** "audit this landing page's polish" or "why does this feel cheap." The `quality-audit` skill reports defects with fixes.
- **To build a 3D hero:** "build a 3D rover/drone/device for the hero," or "this exported GLB shades wrong / clips when it animates / is too big." The `building-3d-for-web` skill triggers.

**When to use this vs. the built-in `frontend-design` skill:** reach for this plugin for the high-motion, awwwards-grade marketing/landing tier (animated heroes, scroll-driven storytelling, parallax, signature interactions) and its full brainstorm-to-QA lifecycle. For general UI that is not motion-led (dashboards, component libraries, product surfaces), the broader `frontend-design` skill fits better. They compose well.

---

## rails-testing

**Turn Claude into a senior Rails test engineer for both RSpec and Minitest: tests that check behavior, run green for the right reasons, don't go flaky, and don't silently go slow.**

Most AI-written Rails tests over-mock, assert on internals, and pass while the real thing is broken (then break on every refactor). This plugin encodes what separates a test that protects you from one that just inflates the coverage number.

- **Framework-aware from the first line.** Auto-detects RSpec (`.rspec` / `spec/` / `rspec-rails`) vs Minitest (`test/test_helper.rb`), then adapts commands and idioms, and reads a neighboring test to match local conventions. **Minitest + fixtures is first-class, not a footnote**, the gap every other Rails testing skill leaves open.
- **Opinionated judgment, not just syntax.** Sandi Metz's testing rules encoded as an explicit mocking/assertion policy (assert incoming, mock only outgoing commands, ignore private and outgoing queries); a classicist "real objects + test DB" default; request specs over controller specs; system specs kept few. Grounded in named practitioners (Sandi Metz, Ian Cooper, Martin Fowler, DHH, Kent C. Dodds, thoughtbot), cited in the reference files.
- **A flaky-test playbook.** The failure modes that quietly rot a suite: time, ordering, unseeded randomness (Faker doesn't honor the global seed), network, leaked global state, DB order without `ORDER BY`, `sleep` in system specs. Detection with `--seed` / `--bisect`, a prevention checklist, and the reason blind retries hide flakiness.
- **Performance regressions, caught in CI.** Assert deterministic query counts, never flaky wall-clock time, and catch N+1s with the scale-invariance pattern (query count doesn't grow with record count) rather than brittle magic numbers. Covers `n_plus_one_control`, `db-query-matchers`, Rails 7.2's built-in query assertions, `prosopite`/`bullet`, and `strict_loading` as a broad tripwire.
- **Composes, doesn't duplicate.** It defers to the `test-driven-development` skill for the red-green loop and supplies the Rails *how*. An implementer under `subagent-driven-development` can load it for the test mechanics.

It ships **one framework-aware skill** (`rails-testing`) with a lean SKILL.md plus six on-demand references: `rspec.md`, `minitest.md`, `test-data.md` (factory_bot + fixtures + determinism), `philosophy.md` (the cited "why"), `reliability.md` (flaky tests, HTTP/VCR, jobs, coverage, CI, PII), and `performance.md` (N+1 / query-count regression tests, `strict_loading`).

### Use it

- **To write tests:** "write a request spec for the checkout endpoint," "test this model," or just "add tests" to Rails code. It detects the framework and writes behavior-first tests.
- **To fix flakiness:** "this spec is flaky" or "this test fails intermittently in CI." It walks the root-cause checklist and reproduces with the seed.
- **To review:** "review these tests." It hunts over-mocking, mystery guests, non-determinism, and specs that test the framework instead of your code.
- **To catch slowness:** "make sure this endpoint doesn't N+1" or "add a query-count guard." It asserts query counts (not flaky wall-clock time) and the N+1-doesn't-scale-with-records pattern.

---

## multi-lens-research

**Turn Claude into a rigorous researcher instead of a fast one: research from distinct lenses, adversarially verify the claims the answer rests on, and report what is verified, what is contested, and what is unknown, with citations.**

The default failure mode of AI research is to fire a few near-identical searches, read the first page, and report the consensus with confidence. The first page of any query is a monoculture, and nothing ever looked for the disconfirming evidence, so the answer is fast and sometimes confidently wrong. This plugin encodes the discipline that prevents that.

- **Distinct lenses, not repeated searches.** It researches from an academic lens, a technical lens, an applied/case-study lens, a news/recency lens, and a dedicated **contrarian lens** whose only job is to build the case against the emerging answer. Different angles surface what the monoculture hides.
- **Verify before believing.** Load-bearing claims are adversarially checked (refute, don't confirm); contradictions between sources are surfaced, never silently reconciled.
- **Anti-confirmation-bias rounds.** One pass is a draft. It runs follow-up rounds aimed at the weakest and most contested claims, weighted toward disconfirming evidence, and loops until the research converges.
- **Honest output.** The report separates verified from contested from unknown, tags each finding with a confidence level earned by independent corroboration (not repetition), and cites everything.

It runs as a **parallel subagent fan-out** when the harness supports it (one agent per lens, then per-claim verification), or a **single-agent sequential loop** when it does not, same method either way. It ships **one skill** (`multi-lens-research`) with a lean SKILL.md plus four on-demand references (`lenses.md`, `verification.md`, `orchestration.md`, `synthesis.md`) and a report template. It owns research rigor and source diversity, and composes with a `deep-research` or web-search skill that owns the raw fetching.

### Use it

- **To research:** "research X thoroughly," "compare A vs B," "what's the state of the art in Y," "landscape scan of Z," or any due-diligence ask where being confidently wrong is expensive.
- **To fact-check at scale:** "is it true that…" or "find the strongest case for and against." It verifies load-bearing claims and reports confidence earned by corroboration.

---

## critical-reasoning

**Turn Claude into a disciplined critical reasoner instead of a fallacy labeler: test whether the evidence is sound, then whether the conclusion follows, and report what holds, what genuinely breaks, and what is just a nitpick.**

Two failure modes show up whenever an AI evaluates an argument. **Credulity:** accepting a confident, well-written argument because nothing in it looked wrong, when its evidence was one recycled source or its key step never actually followed. And the more seductive one, **slop:** hunting fallacies, slapping Latin labels on things, flagging every technically-present imperfection, and dismissing conclusions because their arguments are flawed. Slop *looks* like critical thinking and measurably lowers answer quality, so this plugin's default is to critique almost nothing and to earn every flaw it raises.

- **Evidence first (Level 1), then inference (Level 2).** A conclusion that follows perfectly from bad evidence is still unsupported, so it checks independence, incentives, recency, primary-source, base rates, and corroboration-vs-repetition *before* touching the logic. Three outlets copying one press release are one source, not three.
- **A method, not a glossary.** It reconstructs the argument (claim / grounds / warrant), steelmans it, names its *type* (which selects the few critical questions that fit), finds the one load-bearing assumption, and runs only the two or three checks aimed at that joint, so it never recites a fallacy taxonomy.
- **Anti-slop hard gates.** It keeps two verdicts separate (a weak *argument* never makes a *conclusion* false), applies a change-the-conclusion bar so nitpicks are suppressed, refuses to let a fallacy name stand as a dismissal, and scrutinizes the favored side as hard as the opposed one.
- **Honest grounding.** The fallacy and bias catalogs are filtered: contested fallacies carry their legitimate forms (citing real expert consensus is not a fallacy), and biases are replication-filtered (anchoring and framing in, ego-depletion and the naive Dunning-Kruger curve out).

It ships **one skill** (`critical-reasoning`) with the five-step method plus four references (`method.md`, `evidence.md`, `fallacies.md`, `biases.md`) and an analysis template. It owns the reasoning discipline applied to an argument already in front of you, and composes with `multi-lens-research`: that skill gathers and verifies sources at scale, this one is the portable two-level pass you apply to an argument you already have.

### Use it

- **To pressure-test:** "does this reasoning hold up," "poke holes in this," "stress-test this design doc / RFC / decision memo," "what am I missing," or "check my logic" on your own draft.
- **To vet a claim:** "is this evidence any good," "should I trust this vendor's / paper's / benchmark's claim before acting on it." It reports sound / load-bearing flaw / nitpick and suppresses the nitpicks.

---

More plugins land here over time. Add the marketplace once and you get them as they ship.

## Repository layout

```
claude-plugins/
├── .claude-plugin/marketplace.json   the marketplace manifest (lists every plugin)
├── plugins/
│   ├── high-fidelity-web/            design-engineering plugin: 3 skills + cited research
│   ├── rails-testing/                Rails testing plugin: 1 framework-aware skill
│   ├── multi-lens-research/          rigorous research plugin: 1 skill + lens/verify references
│   └── critical-reasoning/           argument-evaluation plugin: 1 skill + method/evidence references
└── README.md                         you are here
```

Each plugin has its own README with a deeper tour, an install snippet, and a "what is inside" map of its skills and references.

## License

MIT, see [LICENSE](./LICENSE). Free to use, fork, and adapt.

Built by Gary Tou. The craft content is grounded in published work by Emil Kowalski, Rauno Freiberg, the Vercel design-engineering team, GSAP/Codrops, Sandi Metz, Martin Fowler, thoughtbot, Evil Martians, and others; full citations live in each plugin's reference files.
