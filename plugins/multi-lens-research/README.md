# multi-lens-research

A Claude Code plugin that turns the agent into a **rigorous researcher** instead of a
fast one. It researches a question from distinct lenses, adversarially verifies the
claims the answer rests on, and reports what is verified, what is contested, and what
is unknown, with citations.

## Why install

The default failure mode of AI research is to fire a few near-identical searches, read
the first page, and report the consensus with confidence. The first page of any query
is a monoculture, and nothing ever looked for the disconfirming evidence, so the
answer is fast and sometimes confidently wrong.

This plugin encodes the discipline that prevents that:

- **Distinct lenses, not repeated searches.** It researches from an academic lens, a
  technical lens, an applied/case-study lens, a news/recency lens, and a dedicated
  **contrarian lens** whose only job is to build the case against the emerging answer.
  Different angles surface what the monoculture hides.
- **Verify before believing.** Load-bearing claims are adversarially checked (refute,
  do not confirm); contradictions between sources are surfaced, never silently
  reconciled.
- **Anti-confirmation-bias rounds.** One pass is a draft. It runs follow-up rounds
  aimed at the weakest and most contested claims, weighted toward disconfirming
  evidence, and loops until the research converges.
- **Honest output.** The report separates verified from contested from unknown, tags
  each finding with a confidence level earned by independent corroboration (not
  repetition), and cites everything so any claim can be checked.

It runs as a **parallel subagent fan-out** when the harness supports it (one agent per
lens, then per-claim verification), or a **single-agent sequential loop** when it does
not. Same method either way.

## When it triggers

Literature reviews, technology and vendor comparisons, "state of the art" scans,
landscape and market research, due diligence, and any question where being confidently
wrong is expensive. It owns research rigor and source diversity, and composes with a
`deep-research` or web-search skill that owns the raw fetching.

## What is inside

- **`multi-lens-research`** skill: the method (frame, assign lenses, gather with
  provenance, adversarially verify, anti-bias rounds, synthesize) plus four reference
  files (the lens catalog and prompt templates, the verification and confidence
  rubric, the orchestration patterns, and the synthesis contract) and a report
  template.

## Install

```
/plugin marketplace add garyhtou/claude-plugins
/plugin install multi-lens-research@garyhtou
```

Built with Claude Code.
