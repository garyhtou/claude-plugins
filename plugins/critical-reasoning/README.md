# critical-reasoning

A Claude Code plugin that makes the agent reason **rigorously** about a claim, argument, or
decision, instead of pattern-matching fallacy names onto it. It tests whether the evidence is
sound, then whether the conclusion follows, and reports what holds, what genuinely breaks, and
what is just a nitpick.

## Why install

Two failure modes show up whenever an AI evaluates an argument, and this plugin is built to
avoid both:

- **Credulity:** accepting a confident, well-written argument because nothing in it looked
  wrong, when its evidence was one recycled source or its key step never actually followed.
- **Slop:** the more seductive failure. Hunting fallacies, slapping Latin labels on things,
  flagging every technically-present imperfection, and dismissing conclusions because their
  arguments are flawed. This *looks* like critical thinking and measurably lowers answer
  quality. Turned loose on its own confident, correct output, an LLM flips more right answers to
  wrong than the reverse (Huang et al., "LLMs Cannot Self-Correct Reasoning Yet", ICLR 2024). So
  this plugin's default is to **critique almost nothing**, and to earn every flaw it raises.

What it encodes instead:

- **Evidence first (Level 1), then inference (Level 2).** A conclusion that follows perfectly
  from bad evidence is still unsupported, so it checks independence, incentives, recency,
  primary-source, base rates, and corroboration-vs-repetition *before* touching the logic. Three
  outlets copying one press release are one source, not three.
- **A method, not a glossary.** It reconstructs the argument (claim / grounds / warrant),
  steelmans it, names its *type* (which selects the few critical questions that fit), finds the
  one load-bearing assumption, and runs only the two or three checks aimed at that joint. The
  argument's shape tells it which checks matter, so it never recites a fallacy taxonomy.
- **Anti-slop hard gates.** It keeps two verdicts separate (a weak *argument* never makes a
  *conclusion* false), applies a change-the-conclusion bar so nitpicks are suppressed, refuses to
  let a fallacy name stand as a dismissal, scrutinizes the favored side as hard as the opposed
  one, and defers to the evidence on what is actually true.
- **Honest grounding.** The fallacy and bias catalogs are filtered: contested fallacies carry
  their legitimate forms (citing real expert consensus is not a fallacy), and biases are
  replication-filtered (anchoring and framing in, ego-depletion and the naive Dunning-Kruger
  curve out), because a reasoning tool that cites debunked science has failed its own test.

## When it triggers

Pressure-testing a design doc, RFC, or decision memo; evaluating an argument in a PR or issue;
checking a vendor's, paper's, or benchmark's claim before acting on it; stress-testing your own
draft's logic; or any "does this reasoning hold up?", "is this evidence any good?", "poke holes
in this", "what am I missing?". It owns the reasoning discipline applied to an argument already
in front of you, and composes with `multi-lens-research`, which gathers and verifies the evidence
at scale.

## How it composes with multi-lens-research

The two share the same Level-1 evidence rules on purpose, so they never contradict each other.
The difference is **discipline vs workflow**: `multi-lens-research` is what you run when you must
go gather and vet a large body of sources (lens fan-out, adversarial verification, cited report);
`critical-reasoning` is the portable two-level pass you apply to an argument you already have.
They hand off both ways: a research run passes its verified findings here for the inference check,
and a reasoning task that turns out to need real evidence-gathering hands off to
`multi-lens-research`.

## What is inside

- **`critical-reasoning`** skill: the five-step method (reconstruct, steelman, test the evidence,
  test the inference, grade in three tiers) plus four reference files and a template.
  - `references/method.md`: the full process, Toulmin reconstruction, Walton's argumentation
    schemes and critical questions (the anti-glossary engine), crux-finding, the constructive
    moves, and the evidence for critiquing sparingly.
  - `references/evidence.md`: the Level-1 evidence rubric, aligned with `multi-lens-research`.
  - `references/fallacies.md`: the high-yield fallacy set, when each breaks a conclusion vs when
    it is a nitpick, and the legitimate forms of the contested ones.
  - `references/biases.md`: the replication-filtered cognitive biases, each with its counter-move.
  - `assets/analysis-template.md`: a fill-in template for a full two-level analysis.

## Install

```
/plugin marketplace add garyhtou/claude-plugins
/plugin install critical-reasoning@garyhtou
```

Built with Claude Code.
