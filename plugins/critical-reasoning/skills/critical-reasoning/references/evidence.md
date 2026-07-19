# Level 1: is the evidence sound? (the foundation)

Before you ask whether a conclusion *follows*, ask whether the evidence it rests on is
*trustworthy*. A conclusion that follows perfectly from bad evidence is still unestablished (the
reasoning gives you no reason to believe it, even if it happens to be true), and an inference-only
critique walks straight past that. Level 1 comes first, always.

These rules are deliberately the **same evidence principles** taught by the `multi-lens-research`
skill's verification rubric (independence, incentives, recency, primary-source,
corroboration-not-repetition, refute-don't-confirm, diagnosticity). The two skills must never
give contradictory evidence advice. The difference is scope: that skill *gathers and vets a
large body of sources* as a workflow; this rubric is what you apply to the evidence in an
argument already in front of you. If `multi-lens-research` is available and the evidence needs
real gathering, use it here instead of eyeballing.

## Rank by load first

You cannot verify everything, and trying to is its own kind of slop. Rank each piece of
evidence by **how much the conclusion depends on it**:

- **Load-bearing:** the conclusion flips if this is false. Scrutinize hard.
- **Supporting:** shapes the conclusion but does not flip it. One corroborating check.
- **Decorative:** color and context. Note it, spend nothing.

A claim that is both **surprising and load-bearing** gets the most scrutiny. Surprising +
single-source + load-bearing is the classic confidently-wrong trap.

## The seven checks (in order)

For each load-bearing piece of evidence:

### 1. Origin: primary, or a retelling?

Locate the evidence on a distance-from-the-event axis: **primary** (the raw dataset, the
filing, the eyewitness, the study itself), **secondary** (a report *about* the primary), or
**tertiary** (a summary of summaries). Evidence mutates as it travels. Trace to the
closest-to-source you can reach; a news article's paraphrase of a study is not the study.

### 2. Independence: count origins, not citations

"Multiple sources" is worthless if they all trace to one origin: one press release, one paper,
one influential post. **Repetition is not corroboration.** Three outlets copying the same
release are one source at high volume, medium confidence at best, not three independent
confirmations. Before you count a claim as multiply-supported, trace each "source" to its root;
if they converge, you have one data point wearing several costumes.

The journalism caveat sharpens this: two independent sources confirm that *two people assert*
something, not that the underlying fact is true, because both may share one flawed original
document or one shared incentive. Real corroboration is triangulation across independent source
*types*, not a citation count. **Independence is the crux of confidence.**
`[EXTERNAL]` DataJournalism.org Verification Handbook,
https://datajournalism.com/read/handbook/verification-1 ; Mike Caulfield, SIFT / "trace to
origin", https://hapgood.us/2019/06/19/sift-the-four-moves/

### 3. Incentive: weigh evidence against the producer's interest

Ask "who benefits if I believe this, and did they produce the evidence?" A vendor benchmarking
its own product, a study funded by a party with a stake in the result, a source spinning its own
reputation: all carry a conflict that *lowers* the weight of their evidence (discount and demand
independent replication, do not necessarily zero it). The mirror image is powerful: evidence
*against* the producer's own interest (an "admission against interest", a funder's own study
finding no effect) is unusually credible. `[EXTERNAL]` Industry-funded trials skew favorable is
established in evidence-based-medicine conflict-of-interest literature.

### 4. Recency: is it still true?

Evidence has a shelf life, and it is domain-dependent. A mathematical proof does not stale; a
"fastest model", a price, an API behavior, or a "current best practice" stales in months. Date
every load-bearing claim and ask whether the world it described still holds. Beware **false
recency**: a 2026 article re-citing 2019 data is 2019 evidence. Date the *data*, not the article.

### 5. Prior plausibility: extraordinary claims need extraordinary evidence

Weigh new evidence against how likely the claim was *before* you saw it. A claim that
contradicts a large, well-established body of knowledge starts with low prior odds and needs
correspondingly strong, hard-to-fake, independent evidence to move you. The disciplined
(non-rhetorical) form is Bayesian: an extraordinary claim has a **low prior**; extraordinary
evidence has an **extreme likelihood ratio** (it is far more expected if the claim is true than
if false). `[EXTERNAL]` The Sagan Standard,
https://en.wikipedia.org/wiki/Extraordinary_claims_require_extraordinary_evidence .
**Caveat:** "extraordinary" is undefined and can be abused to dismiss disfavored claims by
fiat. Keep it Bayesian (name the prior and the likelihood ratio) rather than using
"that's extraordinary" as a rhetorical veto.

### 6. Data quality: interrogate the sample, not just the source

A source can be authoritative, current, and independent, and its underlying *data* still lie:

- **Selection bias:** was the sample drawn in a way that skews the result (self-selected
  respondents, cherry-picked benchmarks, a non-representative population)?
- **Survivorship bias:** are you seeing only the survivors ("three dropouts got rich" ignores
  the vast invisible pool who dropped out and did not)?
- **Sample size and power:** is N enough to support the claim, or is an anecdote dressed as a
  trend?
- **The denominator:** a raw count with no base rate is not evidence of a rate.

Evidence-based medicine formalizes this as **evidence hierarchies**: study designs ranked by how
well they control bias (systematic reviews of trials at the top, mechanism-based reasoning and
single expert opinion at the bottom). `[EXTERNAL]` OCEBM Levels of Evidence,
https://www.cebm.ox.ac.uk/resources/levels-of-evidence/ocebm-levels-of-evidence . **Caveat:**
the CEBM itself warns the hierarchy is a *prior* on data quality, not an automatic verdict. A
well-run cohort study can beat a flawed trial; GRADE exists precisely to up/down-grade evidence
for quality, consistency, and directness. Use the hierarchy to set expectations, then judge.

### 7. Verify laterally, and disconfirm

- **Lateral, not vertical.** Do not judge a source by staring harder at the source (its slick
  design, its "About" page, its own claims about itself). Leave it and check what the rest of
  the record says about it. Lateral reading is how professional fact-checkers work, and it is
  faster *and* more accurate than deep-diving the page. `[EXTERNAL]` SIFT / the Four Moves
  (Stop, Investigate the source, Find better coverage, Trace to origin), Caulfield,
  https://hapgood.us/2019/06/19/sift-the-four-moves/
- **Disconfirm, don't confirm.** The default move (pick the favorite explanation, hunt for
  support) bakes in confirmation bias. Instead, hold the plausible hypotheses at once and prize
  **diagnostic** evidence: evidence that discriminates *between* hypotheses. Evidence equally
  consistent with every explanation has near-zero value even when it "feels" supportive. The
  surviving explanation is the one hardest to *rule out*, not the one with the most
  confirmations piled on. `[EXTERNAL]` Analysis of Competing Hypotheses (ACH), Richards Heuer,
  *Psychology of Intelligence Analysis* (CIA, 1999),
  https://en.wikipedia.org/wiki/Analysis_of_competing_hypotheses . **Caveat:** ACH's measured
  bias-reduction in practice is modest (RAND RR-1408); the *principle* (consider all
  hypotheses, seek disconfirmation, prize diagnosticity) is not in dispute. Treat it as
  disciplined scaffolding, not a guarantee.

## Confidence follows corroboration, not repetition

When you report how much to trust the evidence:

- **High:** corroborated by 2+ *independent* trustworthy sources, or one primary authoritative
  source (a standard, a spec, an official filing), recent enough to hold, no credible
  contradiction found after looking.
- **Medium:** a single good source with no independent corroboration yet, or multiple sources
  not clearly independent, or minor unresolved caveats.
- **Low:** single weak or interested source, dated, contested, or only indirectly supported.
  State it as "reported but unverified".
- **Unknown:** no credible source located. Report the gap; do not fill it with a guess.

## When evidence fails, stop here

If the load-bearing evidence fails these checks, that is your finding: **the argument is
unsupported at the evidence layer**, and you do not need to reach the inference check to say so.
Report *which* check it failed (recycled one source, stale, interested, wrong denominator) and
what it would take to fix. This is the failure an inference-only critique misses, and catching
it is half of what this skill is for.

When two load-bearing sources genuinely disagree, do not average them into a false middle or
silently pick one. Surface both, weight by independence, recency, and primary-over-secondary, and
mark the point contested if the evidence does not actually resolve it. (For multi-source synthesis
at scale this is the `multi-lens-research` verification rubric's job; here it is the single-argument
version.)

## A caution on checklists

Named rubrics (CRAAP, evidence hierarchies) are useful *prompts*, not verdicts. The CRAAP test
in particular is criticized as a "vertical" checklist that keeps you *on* an untrustworthy page,
where experts do worse than lateral reading against networked misinformation. `[EXTERNAL]`
"Rethinking CRAAP", https://crln.acrl.org/index.php/crlnews/article/view/24195/32005 . Use the
criteria as questions to ask, then verify laterally and disconfirm. The checks above are the
questions; independence and disconfirmation are the ones that do the work.
