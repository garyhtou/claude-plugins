---
name: multi-lens-research
description: Use when a question needs real research depth and the answer must be trustworthy, not just plausible: literature reviews, technology and vendor comparisons, due diligence, "what is the current state of X," landscape scans, or any claim that will be acted on. It runs research as distinct lenses (academic, technical, applied, news, and a dedicated contrarian lens) instead of several identical searches, so it does not converge on first-page consensus; then it adversarially verifies load-bearing claims, runs anti-confirmation-bias follow-up rounds, and synthesizes a cited report that separates verified from contested from unknown. Triggers on "deep dive," "research X thoroughly," "compare A vs B," "is it true that," "state of the art," "landscape / market scan," "due diligence," "find the strongest case for and against," or any ask where being confidently wrong is expensive. Owns research rigor and source diversity; composes with a deep-research or web-search skill that owns raw fetching.
---

# Multi-lens research

Most AI research fails the same way: it fires a few near-identical searches, reads
the first page of results, and reports the consensus back with confidence. That is
fast and often wrong, because the first page of any query is a monoculture (the
same few sources cite each other) and nothing ever looked for the disconfirming
evidence. This skill exists to prevent that.

The method is three commitments:

1. **Diversity over volume.** Research from **distinct lenses** (angles that look at
   different source types and ask different questions), not N copies of one query.
   A dedicated **contrarian lens** whose only job is to build the case *against* the
   emerging answer is non-negotiable.
2. **Verify before you believe.** A claim does not enter the synthesis because it
   appeared. Load-bearing claims get **adversarially checked**; contradictions
   between sources are surfaced, never silently reconciled.
3. **Say what you do not know.** The output separates **verified**, **contested**,
   and **unknown**, with confidence and citations. Never launder a plausible guess
   into a stated fact.

## How this composes with other skills

- **A `deep-research` / `web-search` / fetch skill** (if present) owns the raw
  mechanics: issuing searches, fetching pages, extracting text. This skill owns the
  *rigor*: how many angles, which ones, how claims are verified, when to stop, and
  what the report must contain. If such a skill is active, use it for retrieval and
  layer this method on top. If not, use whatever web search and fetch tools you have.
- **Subagent / workflow orchestration** (if the harness has it) is how you run the
  lenses in parallel. See `references/orchestration.md`. Without it, run the
  sequential fallback in the same file. The method is identical; only the wiring
  differs.
- This skill is about **finding and vetting truth**, not writing final prose. If a
  separate writing/voice skill is active, hand it the synthesized, cited findings.

## Step 1: Frame the question and decompose

Do not start searching until the question is sharp. Vague questions produce vague
monoculture answers.

- **Restate the real question** in one sentence. If the user's ask is
  underspecified ("research electric cars"), pin down scope, audience, decision, and
  timeframe before spending a search budget. One or two clarifying questions here
  save an entire wasted round.
- **Name the decision it feeds.** "Which database for a write-heavy 10k-TPS service"
  is researchable; "tell me about databases" is not. The decision sets the bar for
  what counts as enough.
- **Decompose into sub-questions.** Break the question into the 3 to 7 independent
  things that must each be true for a confident answer. These become the targets the
  lenses divide up.
- **State the thesis, if there is one (thesis-driven mode).** If the user already
  believes something ("X is faster than Y"), write the thesis down explicitly and
  treat the job as *testing* it, not confirming it. This is what makes the
  contrarian lens and the later rounds bite.

## Step 2: Assign the lenses (the core move)

Run **distinct lenses**, each looking at different source types and asking a
different question, so they do not all land on the same first page. Default to the
**standard set of five**; escalate to the **deep set** for high-stakes or wide
topics.

**Standard set (5 lenses):**

| Lens | What it hunts | Goes to |
| --- | --- | --- |
| **Academic / primary** | The authoritative definition, mechanism, and evidence | Papers, standards, specs, official docs, primary sources |
| **Technical / practitioner** | How it actually works and performs in practice | Source code, engineering blogs, benchmarks, issue trackers, docs |
| **Applied / case-study** | Who uses it, what happened, at what scale | Case studies, postmortems, real deployments, reviews, forums |
| **News / recency** | The current state and what changed lately | Recent news, release notes, changelogs, dated announcements |
| **Contrarian / skeptic** | The strongest case *against* the emerging answer | Criticism, failure reports, "X considered harmful," competitor claims, known limitations |

**Deep set (add for high-stakes or broad topics):** **Historical / evolution** (how
it got here, what was tried and abandoned), **Adjacent / analogy** (how neighboring
fields solved the same problem), **Data / quantitative** (numbers, benchmarks,
market size, measured tradeoffs).

Rules that make the lenses work:

- **Each lens is blind to the others during gathering.** The point is independent
  coverage. If they share notes mid-gather they re-converge, which defeats the
  exercise. They merge only at synthesis.
- **The contrarian lens is mandatory and adversarial.** Its prompt is not "find
  balance," it is "assume the likely answer is wrong; find the best evidence it is."
  A homogeneous swarm silently skips this; a named agent cannot.
- **Give each lens the decomposed sub-questions plus its angle**, not the raw user
  prompt. See `references/lenses.md` for per-lens prompt templates, example queries,
  and how to add domain-specific lenses (legal, security, clinical, financial).

## Step 3: Gather claims with provenance

Each lens returns **claims**, not raw text dumps. A claim is: the assertion, the
**source (URL or citation)**, and a **confidence tag** (high / medium / low) based
on source quality and independent corroboration.

- **No source, no claim.** An assertion with no citation is a lead to verify, not a
  finding. Never state it as fact.
- **Capture the source verbatim** (URL, title, date) so the synthesis can cite and a
  later round can re-check. Preserve dates; recency and staleness both matter.
- **Do not fabricate.** If a lens finds nothing solid, that absence is itself a
  result ("no primary source located for X"), not a cue to invent one.

## Step 4: Adversarially verify the load-bearing claims

This is the quality gate that separates this skill from generic research. Before a
claim can carry weight in the answer, try to break it.

- **Rank claims by how much the conclusion leans on them.** You cannot verify
  everything; verify what the decision rests on.
- **Refute, do not confirm.** For each load-bearing claim, actively look for
  evidence it is false, outdated, or misattributed. When the harness supports
  parallel subagents, spawn independent skeptics (a small odd number) each told to
  refute, and keep the claim only if it survives a majority. Default to "not
  verified" when uncertain. See `references/verification.md`.
- **Surface contradictions, never bury them.** If two sources disagree, that is a
  finding: report both, weight by source quality and recency, and mark it contested.
  Do not average them into a false middle or silently pick one.
- **Tag the result:** verified (independently corroborated from a trustworthy
  source), contested (real disagreement), or unverified (single/weak source, could
  not corroborate).

## Step 5: Run anti-confirmation-bias follow-up rounds

One pass is a draft, not an answer. After round 1, deliberately attack the weak spots.

- **Target the weak and the contested.** Identify the claims with the thinnest
  support and the open contradictions, and run a focused round aimed at exactly
  those, weighted toward the **disconfirming** side.
- **Fill the gaps the decomposition exposed.** Any sub-question still unanswered gets
  its own targeted search.
- **Escalate a lens if it came back thin.** If the contrarian lens found little,
  push it harder before concluding "no real objections exist" (that conclusion is
  usually wrong on the first try).
- **Stop on a real signal, not a fixed count.** Stop when a round surfaces nothing
  materially new (converged), when the load-bearing claims are all verified or
  explicitly marked contested/unknown, or when you hit the search budget. If you
  stop on budget, say so and name what is still unverified. Do not stop just because
  round 1 produced a tidy narrative.

## Step 6: Synthesize a cited, honestly-hedged report

The deliverable is not "what the internet says." It is a decision-grade answer that
shows its work. Structure (full contract in `references/synthesis.md`, template in
`assets/report-template.md`):

- **Answer / bottom line** first, with an explicit **overall confidence**.
- **Key findings**, each with citation(s) and a confidence tag.
- **Contested / uncertain**: where good sources disagree, and how you weighted them.
- **What we could not determine**: the honest unknowns. Their presence is a feature.
- **Sources**: the citations, so every claim is traceable.

Confidence is earned by **independent corroboration**, not by how many times the same
source was requoted. Three pages copying one press release is one source.

## Scale to the stakes

Match effort to the cost of being wrong. A quick factual check does not need eight
parallel agents; a vendor decision or a due-diligence memo does.

- **Quick check:** standard 5 lenses (or fewer), single verify pass, one round.
- **Thorough / high-stakes:** deep set (8 lenses), 3-way adversarial verify on
  load-bearing claims, loop rounds until dry, explicit contested/unknown sections.

Announce the level you chose and why, so the reader knows the depth behind the answer.

## Anti-patterns (what this skill refuses to do)

- **N identical searches.** The failure this whole skill prevents. Different lenses,
  or it is not multi-lens research.
- **First-page consensus as truth.** The top results are a monoculture; treat them as
  a starting point to verify and challenge, not the answer.
- **Plausible-but-unverified stated as fact.** The single most damaging research
  error. Tag confidence; keep unverified claims labeled.
- **Silent reconciliation.** Two sources disagree and the report picks one with no
  note. Surface the disagreement instead.
- **One-and-done.** Stopping at round 1 because the narrative looks clean. Clean
  round-1 narratives are exactly where the confirmation bias hides.
- **No citations.** An unsourced synthesis cannot be checked, so it cannot be trusted.

## Reference files (load as needed)

- `references/lenses.md`: the full lens catalog, per-lens prompt templates and
  example queries, and how to design domain-specific lenses.
- `references/verification.md`: adversarial verification, the refute-by-majority
  pattern, contradiction handling, and the confidence-scoring rubric.
- `references/orchestration.md`: the parallel subagent/workflow fan-out pattern
  (with pseudocode) and the single-agent sequential fallback; dedupe, budgets, and
  loop-until-dry.
- `references/synthesis.md`: the output contract, the cited-report structure, and
  the no-fabrication / provenance rules.

## Prose style

Write plainly and cite specifically. Avoid em dashes in any prose you generate;
recast with commas, periods, colons, parentheses, or "to" for ranges. Em dashes read
as an AI tell.
