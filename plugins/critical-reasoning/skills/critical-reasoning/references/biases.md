# Level 2: cognitive biases that distort reasoning (replication-filtered)

A bias list is a minefield for a reasoning tool, because much of the pop-psychology "biases"
canon did not survive the **replication crisis** (in the 2015 Reproducibility Project about 36% of
effects replicated by the significance test, 39% by the replication teams' own judgment, and on
the significance metric only about 25% of social-psychology effects replicated versus about 50% of
cognitive ones). `[EXTERNAL]` https://en.wikipedia.org/wiki/Replication_crisis . So this file is
filtered: use the
robust ones, caveat the contested ones, and do not lean on the debunked ones at all. Citing a
biased-out "bias" as science is a hard credibility fail.

The point of a bias check is **not** to accuse an argument of "bias" (that is just a fancier
name-the-fallacy move, and often weaponized: see `references/fallacies.md`, symmetry gate). It is
to ask a sharper question: *is the conclusion being driven by the evidence, or by a predictable
distortion in how the evidence was gathered, weighted, or presented?* The **counter-move matters
more than the label**, so each entry leads to what you actually do.

## Robust: use as-is

### Confirmation bias `[HIGH]`
Seeking, weighting, or interpreting evidence to favor a belief already held; disconfirming data is
never searched for, is explained away, or is held to a higher bar (asymmetric scrutiny). An
argument can look strong purely because the search was one-sided. **Counter-move:** consider the
opposite. "What would I expect to see if this were false, and did anyone look?" Ask what evidence
was *excluded*, not just what was cited. Best-supported debiasing technique there is.
`[EXTERNAL]` Nickerson 1998, https://pages.ucsd.edu/~mckenzie/nickersonConfirmationBias.pdf

### Motivated reasoning `[HIGH]` (distinct from confirmation bias)
Processing information to reach a *desired* conclusion (goal-driven), building justifications for
what you *want* true, versus confirmation bias's more automatic favoring of what you already
*believe*. **Counter-move:** separate the arguer's stake from the argument. "Would this same
evidence convince me if it pointed the other way, or served the other side?" `[EXTERNAL]` Kunda
1990, https://pubmed.ncbi.nlm.nih.gov/2270237/

### Anchoring `[HIGH]` (one of the most robust effects in judgment research)
Estimates are pulled toward an initial reference value, even an irrelevant or random one, because
adjustment away from it is insufficient. Replicated in Many Labs with a *larger* effect than most.
**Counter-move:** generate your own estimate *before* looking at the quoted figure. "Where did
this number come from, and would I reach it independently?" `[EXTERNAL]` Tversky & Kahneman 1974;
Klein et al. 2014 (Many Labs).

### Availability heuristic `[HIGH]`
Judging frequency or probability by how *easily* examples come to mind, so vivid, recent, or
dramatic instances inflate perceived likelihood. (It is the *ease of retrieval*, not the count of
examples, that drives it.) **Counter-move:** ask for base rates and actual frequencies instead of
memorable examples. "How common is this in the full population, not in the cases I can recall?"
`[EXTERNAL]` Tversky & Kahneman 1973; Schwarz et al.

### Framing effects `[HIGH]`
Logically equivalent descriptions of the same facts ("200 saved" vs "400 die", "90% survival" vs
"10% mortality", a chosen denominator) produce different judgments. Survived a targeted challenge:
a higher-powered replication that disambiguated the wording still found a strong effect.
**Counter-move:** restate the claim in the opposite frame and in absolute numbers. If your
reaction flips, the frame, not the fact, was driving you. `[EXTERNAL]` Tversky & Kahneman 1981;
Data Colada #11, https://datacolada.org/11

### Hindsight bias `[HIGH]`
Once an outcome is known, overestimating how predictable it was ("knew it all along"), which makes
a decision or forecast look far more determined than it was and fuels overconfident "lessons
learned". **Counter-move:** reconstruct the information available *before* the outcome; ask what
other outcomes were plausible then. Prefer decision logs over memory. `[EXTERNAL]` Fischhoff 1975.

### Publication bias `[HIGH]` (the seam back to Level 1)
Positive, significant results get published more than null results, so the *published* literature
overstates effects (the file-drawer problem). This is where a bias check hands back to the evidence
layer: even correctly reasoned "the studies show X" can be wrong if the underlying literature is a
biased sample. **Counter-move:** ask "where are the null results?" Prefer preregistered
replications over one splashy study; look for funnel-plot / p-curve checks. `[EXTERNAL]`
https://en.wikipedia.org/wiki/Publication_bias

## Contested: include only with the caveat

### Overconfidence / miscalibration `[MED/HIGH]`
Confidence systematically exceeds accuracy. The specific form cited here, **overprecision**
(90%-confidence intervals that contain the truth far less than 90% of the time), is one of the
more robust overconfidence effects (Moore & Healy 2008 separate overprecision, overestimation,
and overplacement; overprecision replicates well, while overplacement / better-than-average is the
more format-dependent one). **Counter-move:** ask for explicit confidence intervals; "consider the
opposite" reliably reduces overconfidence. Keep this *separate* from Dunning-Kruger below.

### Dunning-Kruger `[LOW / CONTESTED]` (use as the teaching example, not as fact)
The popular claim (the least competent most overestimate their competence) is **mostly a
statistical artifact**: the signature quartile chart falls out of regression to the mean and
autocorrelation *even in random data*. A small residual overplacement effect may survive
under valid methods, and even that is debated. `[EXTERNAL]` Nuhfer et al. 2016/2017; Gignac &
Zajenkowski 2020, "(mostly) a statistical artefact", https://gwern.net/doc/iq/2020-gignac.pdf .
Do **not** present the naive curve as fact. The usable kernel (people are often poorly calibrated
about their own knowledge; seek external calibration) is just overconfidence, above. This bias is
most useful here as a live demonstration that a famous "bias" can itself fail the evidence check.

### Halo effect `[MED]`
A global positive impression of a source (prestige, polish, likeability) contaminates judgment of
its specific, logically independent claims. Real but on a smaller, older evidence base than
anchoring or framing, so do not overclaim precision. **Counter-move:** evaluate the specific claim
on its own evidence. "If a source I disliked said exactly this, would it hold up?" `[EXTERNAL]`
Nisbett & Wilson 1977.

## Do not use as grounded science

**Ego depletion** and **social/behavioral priming** (professor priming, elderly-words-slow-walking)
are the poster children of the replication crisis. Do not cite them in a skill that claims
scientific grounding. `[EXTERNAL]` https://en.wikipedia.org/wiki/Replication_crisis

## Does debiasing even work?

Be honest: awareness alone does almost nothing, and debiasing *reduces* rather than *eliminates*
bias, with effects that vary by task. A few interventions have real support, and they are the
counter-moves worth teaching. `[EXTERNAL]` Larrick 2004, "Debiasing",
https://web.stanford.edu/~knutson/jdm/larrick04.pdf

- **Consider the opposite / consider alternatives** (best-supported). Important limit: ask for a
  *few* strong opposing reasons, not an exhaustive list. Generating too many backfires, because
  when it gets hard to think of more, people take the difficulty as evidence they were right.
- **Outside view / reference-class forecasting:** compare to similar past cases instead of
  reasoning only from inside this one. Fixes base-rate neglect.
- **Frequency framing** for probability problems ("out of 1,000 people..."): durable, beats
  abstract probability.
- **Precommitment / premortem:** decide the criteria before seeing results; "imagine it failed,
  why?"

Present these as disciplines that help, not cures. That honesty is itself part of reasoning well.
