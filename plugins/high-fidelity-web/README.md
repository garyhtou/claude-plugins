# high-fidelity-web

A Claude Code plugin that turns the agent into a **design engineer** for
high-fidelity, interactive, animated marketing and landing sites: the near-3D,
eye-catching, awwwards-grade tier you see on Stripe, Linear, Vercel, and Column.

## Why install

Most AI-built sites look templated: default easing, muddy shadows, untuned type,
no microstates. This plugin encodes what actually separates premium from generic,
so Claude builds (and critiques) like a senior design engineer instead.

- **The full lifecycle, not just snippets.** It walks concept, design tokens, a
  real motion language, in-browser prototyping, component build with complete
  microstate coverage, polish, and adversarial QA, pausing at human taste
  checkpoints.
- **Framework-agnostic.** Default stack is vanilla JS + GSAP + Tailwind (works in
  Rails, Astro, plain HTML), escalating to React/Next + Motion / Three.js / R3F
  only when the concept earns it. The principles port to any stack.
- **Grounded in named practitioners.** The craft content is sourced from published
  work by Emil Kowalski (Linear), Rauno Freiberg (Vercel), the Vercel
  design-engineering team, and GSAP/Codrops, with citations in every reference
  file. Concrete values, not vibes: exact easing curves, durations, spring params,
  Core Web Vitals targets.
- **Two ways in.** Build a new site, or point the audit skill at an existing one.

It packages three skills:

- **`high-fidelity-web`** : the full build lifecycle. Brainstorm a concept, define
  a design-token and motion system, prototype the hero in code, build
  component-by-component with all six microstates, then polish and QA against a
  premium bar.
- **`quality-audit`** : a standalone critique pass. Point it at an *existing* site
  and it reports specific, prioritized defects (microstates, motion polish, Core
  Web Vitals, accessibility) with concrete fixes.
- **`building-3d-for-web`** : build a believable hard-surface 3D model for a WebGL
  hero or product piece, procedural Blender (headless `bpy`) to optimized glTF/GLB
  (Draco) to Three.js/R3F. Covers hard-surface realism, the headless `bpy` gotchas,
  the GLB pipeline, articulated rigging, and a programmatic clip detector, with a
  Blender build scaffold, a Draco compressor, and a model inspector as assets.

**When to use this vs. the general `frontend-design` skill:** reach for this plugin
for the high-motion, awwwards-grade marketing/landing tier (animated heroes,
scroll-driven storytelling, parallax, signature interactions) and its full
brainstorm-to-QA lifecycle. For general UI that is not motion-led (dashboards,
component libraries, product surfaces), the broader built-in `frontend-design` skill
is the better fit. They compose well.

## Demo

The example site, **Zoomies ("Strava for cats")**, is built with this plugin's
principles. It lives in its own repo and is deployed live. It is real code you can
open and read, not a mockup. The stills below are calm frames; the rings, charts,
bars, trail, and reveals are all in motion in the browser.

### [Live site &rarr;](https://zoomies.garytou.dev/) &middot; [Source: garyhtou/zoomies](https://github.com/garyhtou/zoomies)

A full fictional product, profile included (`BRAND.md`: identity, ICP, tone of voice,
features, color system). The point is to show the plugin carrying an absurd premise
with a real, premium product aesthetic, the opposite of generic AI output.

The hero is **immersive but on-concept**: a glowing **zoomie trail** races and wanders
across it like a tracked sprint and chases your cursor (the cat chasing you). It
visualizes the exact thing Zoomies sells, so the artistry adds meaning instead of
decoration. The rest stays **restrained for clarity**: animated **activity rings**, a
real-looking **dashboard centerpiece** (an interactive zoomies heatmap, a category
day-timeline, count-up stat tiles), a **scroll-scrubbed "a day in the life"** section
(a pinned scene where the sun arcs across the sky and each moment of Mochi's day
crossfades in as you scroll), an **animated leaderboard**, **cursor-reactive 3D tilt
cards**, big count-up metrics, and full reduced-motion support. It is **responsive**
(mobile-first, no horizontal overflow, immersive effects degrade on phones). Color is
used for meaning (lime = zoomies, blue = rest, amber = hunt), not decoration.

[![Zoomies hero: a glowing zoomie-trail path weaving across a dark hero, headline "Every nap, hunt, and 3am zoomie. Tracked.", with an activity-rings product card showing Mochi napping](https://zoomies.garytou.dev/preview/hero.png)](https://zoomies.garytou.dev/)

![Zoomies dashboard: stat tiles, an interactive zoomies heatmap with hot 3am and evening columns, and a category-colored day timeline](https://zoomies.garytou.dev/preview/dashboard.png)

![Zoomies "a day in the life": a color-coded timeline of six moments, from a 6:30am breakfast sprint to the 3:02am zoomie, each with a stat and a deadpan caption](https://zoomies.garytou.dev/preview/day.png)

## What is inside

```
high-fidelity-web/
├── .claude-plugin/
│   └── plugin.json          plugin manifest
├── skills/
│   ├── high-fidelity-web/
│   │   ├── SKILL.md          the lifecycle spine (always loaded)
│   │   ├── references/       loaded on demand: design-principles, motion-language,
│   │   │                     techniques, tools, responsive-and-mobile,
│   │   │                     reliability-and-gotchas, quality-bar
│   │   └── assets/           brief-template.md, tokens-starter.css, reduced-motion.css
│   ├── quality-audit/
│   │   └── SKILL.md          the standalone audit skill (reuses quality-bar.md)
│   └── building-3d-for-web/
│       ├── SKILL.md          the 3D pipeline spine + gotcha quick-reference
│       ├── references/       realism, blender-procedural, glb-web-pipeline,
│       │                     rigging-and-clips, verifying-in-browser
│       └── assets/           build_scaffold.py, compress.mjs, inspector.html
└── research/                the underlying, fully-cited research the skills distill
```

The example site (Zoomies) lives in its own repo, [garyhtou/zoomies](https://github.com/garyhtou/zoomies),
and is deployed at [zoomies.garytou.dev](https://zoomies.garytou.dev/).

The `references/` files are the distilled, instructional versions the skills load
at runtime; `research/` holds the longer-form research and sources they were built
from, kept here so the plugin is self-contained.

Built on progressive disclosure: each `SKILL.md` stays lean and points to the
heavier reference files, which the agent reads only when a phase needs them.

## Install

This plugin lives in the `garyhtou/claude-plugins` marketplace. Add the marketplace
once, then install the plugin:

```
/plugin marketplace add garyhtou/claude-plugins
/plugin install high-fidelity-web@garyhtou
/plugin
```

The last command should list the `high-fidelity-web`, `quality-audit`, and
`building-3d-for-web` skills.

To pick up edits, run `/plugin marketplace update garyhtou` then `/reload-plugins`
(installed plugins do not auto-update on push). During development you can point the
marketplace at a local checkout path instead of the GitHub slug.

## Use

- **To build a site:** describe what you want ("build a premium landing page for X
  that feels precise and weighty"). The `high-fidelity-web` skill triggers and
  walks the lifecycle, pausing at three human taste checkpoints.
- **To audit a site:** "audit this landing page's polish" or "why does this feel
  cheap." The `quality-audit` skill triggers and reports defects with fixes.

## Maintaining and releasing this plugin

Marketplace-level mechanics (how to add a plugin, how users add the marketplace)
live in the marketplace README at the repo root. Plugin-specific release hygiene:

- **Versioning:** bump `version` in `.claude-plugin/plugin.json` on every released
  change (patch for fixes/copy, minor for new references/skills, major for breaking
  restructures). Tag releases in git (`git tag high-fidelity-web-v0.2.0`) so a
  marketplace entry can pin a ref if you ever split this into its own repo.
- **License:** `plugin.json` declares `MIT`, and the repo-root `LICENSE` covers
  this plugin while it lives in this monorepo. If you ever split it into its own
  repo, add a matching `LICENSE` file there. Confirm the license is what you want
  (it governs reuse).
- **Fresh facts:** the references cite fast-moving facts (bundle sizes, GSAP
  licensing, browser support). Re-verify near a release; `references/tools.md`
  carries a "current as of" date.
- **Before publishing, sanity-check:** both skills install and appear in `/plugin`
  from a clean clone (not just your dev copy); the trigger descriptions invoke the
  right skill (build vs audit) on realistic prompts; no em dashes in generated copy,
  and no secrets/private data are bundled.
- **Discoverability when public:** set GitHub repo topics (claude-code,
  claude-plugin, claude-skill, gsap, web-animation, landing-page, awwwards,
  motion-design, design-engineering, frontend), add visual demos to this README,
  and consider listing the marketplace in community "awesome-claude" directories. For AI
  agents, the skill `description` fields are what drive auto-invocation, so keep
  them trigger-phrase-rich.

## Credit

Built with AI (Claude) under the guidance of Gary Tou. The craft content is
grounded in published work by Emil Kowalski, Rauno Freiberg, the Vercel
design-engineering team, GSAP/Codrops, and others; full citations live in each
reference file's Sources section and in `research/`.
