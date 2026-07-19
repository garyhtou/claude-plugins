---
name: quality-audit
description: Use when auditing, reviewing, or critiquing an EXISTING website against a premium design-engineering quality bar (a design and polish review, not just functional QA). Checks microstates, motion and animation polish, typography, color, hairlines, spacing rhythm, Core Web Vitals (LCP/INP/CLS, Lighthouse), responsiveness, and accessibility, then reports specific prioritized defects with concrete fixes. Triggers on requests like "audit this site", "design review of my landing page", "why does this feel cheap or unpolished", "is this awwwards-grade", "review the animations or motion", or "check this page's performance and accessibility". For building a new high-fidelity site, use the high-fidelity-web skill instead.
---

# Quality Audit

Audit an existing site against the premium, awwwards-grade quality bar and report
specific, actionable defects (not vague impressions). You are a design engineer
doing a critique pass: every finding names a concrete element, the rule it
violates, and the fix.

This is the standalone critique companion to the `high-fidelity-web` skill (which
builds sites from scratch). It reuses that skill's canonical quality-bar content.

## Load the references

The canonical checklists and the seven-step critique live in the sibling skill,
which ships in this same plugin:

- `../high-fidelity-web/references/quality-bar.md` : the acceptance gate and the
  self-critique protocol. **This is the spine of the audit. Load it first.**
- `../high-fidelity-web/references/motion-language.md` : the exact easing,
  duration, spring, and perf values to check motion against.
- `../high-fidelity-web/references/design-principles.md` : the craft context
  (typography, color, depth, anti-patterns) when you need to justify a finding.

(If this skill is ever extracted to stand on its own, copy those reference files in
with it.)

## How to run the audit

1. **Establish the intended feeling.** Ask the user (or infer) the one word the
   site should land. Open it. Does it deliver that word in the first 3 seconds?
2. **Run the seven-step critique** from `quality-bar.md` section 8: feeling test,
   generic test, adversarial QA, microstate audit, unseen-details sweep, numbers
   gate, the Awwwards question.
3. **Walk the checklists** in `quality-bar.md` sections 1 to 7 (visual/interaction,
   spacing/hierarchy, motion polish, Core Web Vitals, responsiveness,
   accessibility, motion/interaction reliability). Inspect the live site: computed
   styles, focus states, reduced-
   motion behavior, and Lighthouse/CWV numbers where you can measure them.
4. **Report findings by severity.** For each: the element, the violated rule, the
   concrete fix (with the correct value from `motion-language.md` where relevant).
   Lead with the few changes that would most raise the perceived quality.

## What good output looks like

- Specific: "The primary CTA has no `:active` state and uses `transition: all
  0.4s ease`; add `scale(0.97)` on press and switch to `transform 150ms
  cubic-bezier(0.23, 1, 0.32, 1)`." Not: "the buttons feel off."
- Prioritized: the highest-leverage fixes first (usually defaulted focus rings,
  `ease-in`/`transition: all`, missing microstates, CWV failures).
- Honest about what you could not measure (e.g. INP without field data).

Avoid em dashes in copy you generate; recast with commas, periods, colons, parentheses, or "to" for ranges. Em dashes read as an AI tell.
