# Verification: refute-by-majority, contradictions, and confidence scoring

Gathering is cheap and gullible. This file is how a claim earns the right to carry
weight in the answer. The governing rule: **try to break the claim before you
believe it.**

## What to verify (you cannot verify everything)

Rank claims by **load**: how much the final conclusion depends on the claim being
true. Verify the load-bearing ones hard; spend little on decorative detail.

- **Load-bearing:** the answer flips if this is false. Verify with full rigor.
- **Supporting:** shapes the answer but does not flip it. One corroborating source.
- **Decorative:** color and context. Cite it, do not spend a verification budget.

A claim that is both surprising and load-bearing gets the most scrutiny. Surprising
+ single-source + load-bearing is the classic "confidently wrong" trap.

## The refute-by-majority pattern

For each load-bearing claim, do not ask "is this true?" (you will find confirmation).
Ask "**can I show this is false, stale, or misattributed?**"

- **When the harness has parallel subagents:** spawn a small **odd** number of
  independent skeptics (3 is the default; 5 for the highest stakes). Each is told to
  **refute** the claim and to **default to `refuted: true` when uncertain**. Keep the
  claim as *verified* only if a **majority fail to refute** it. Diversity helps: give
  each skeptic a different attack (one checks the primary source, one checks recency,
  one checks whether the source has a conflict of interest).
- **When you are a single agent:** run the same checks serially as an explicit
  self-refutation pass. Write the claim, then write the best case against it, then
  decide. The discipline is to *actually look* for the counter-evidence, not to
  perform a token doubt and move on.

Attacks that catch the most errors:
- **Primary-source check:** does the cited source actually say this, or is it a
  telephone-game paraphrase? Follow the chain to the origin.
- **Recency check:** is this still true, or was it true three years ago? Look for a
  newer source that supersedes it.
- **Independence check:** are the "multiple sources" actually independent, or do they
  all trace to one press release / one paper / one influential post?
- **Incentive check:** who benefits if this claim is believed? A vendor benchmarking
  its own product is low confidence until an independent source confirms.
- **Base-rate check:** is the claim extraordinary? Extraordinary claims need
  proportionally stronger evidence.

## Handling contradictions (surface, never bury)

When two credible sources disagree, that disagreement **is a finding**. Do not
average them into a false middle and do not silently pick the one that fits the
narrative.

1. **State both** positions with their citations.
2. **Weight** by source quality, independence, recency, and directness (primary over
   secondary). Say how you weighted.
3. **Resolve only if the evidence actually resolves it.** If a primary, recent,
   independent source clearly outweighs a stale secondary one, resolve and say why.
4. **Otherwise mark it contested** and carry that into the synthesis. "Sources
   disagree; here is the split and my lean" is a more honest and more useful answer
   than a fabricated certainty.

## Confidence scoring rubric

Tag every claim that reaches the synthesis. Confidence comes from **independent
corroboration and source quality**, not from repetition.

- **High:** corroborated by 2+ **independent** trustworthy sources, or one primary
  authoritative source (a standard, a spec, an official filing), recent enough to
  still hold. No credible contradiction found after looking.
- **Medium:** a single good source with no independent corroboration yet, or multiple
  sources that are not clearly independent, or a claim with minor unresolved caveats.
- **Low:** single weak/interested source, dated, contested, or only indirectly
  supported. State it as "reported but unverified."
- **Unknown:** could not find a credible source. Report the gap; do not fill it with
  a guess.

**Independence is the crux.** Three articles copying the same press release are one
source at high volume, which is **medium at best**, not high. Trace citations to
their origin before you upgrade confidence.

## No-fabrication rules (hard constraints)

- Never invent a source, a statistic, a quote, or a date. If you do not have it, the
  claim is Unknown.
- Never state an unverified claim in the declarative voice of a fact. Keep the hedge
  attached ("one vendor benchmark reports X, unverified").
- Never upgrade confidence to make the answer look cleaner. An honest "contested" or
  "unknown" is the deliverable working correctly, not a failure.
- Preserve provenance so any claim can be re-checked later by following its citation.

## Handing verified claims to the inference check

Verification tells you a claim's evidence is sound. It does not tell you whether a *conclusion
drawn from* that claim actually follows. Those are different failures: a well-verified fact can be
used in a broken inference (a fallacy, an ignored base rate, a load-bearing assumption). When the
task is to judge an argument built on these findings, hand the verified claims to a
`critical-reasoning` skill (if present) for the Level-2 inference check. It shares these same
evidence rules, so the two never give contradictory advice: this rubric owns "is the evidence
sound", the reasoning skill owns "does the conclusion follow".
