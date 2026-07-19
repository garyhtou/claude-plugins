---
name: critical-reasoning
description: Use when you need to judge whether a claim, argument, or decision actually holds up, not just whether it sounds convincing. Pressure-testing a design doc, RFC, or decision memo; evaluating an argument in a PR or issue; checking a vendor's, paper's, or benchmark's claim before you act on it; stress-testing your own draft's logic; or answering "does this reasoning follow?", "is this evidence any good?", "poke holes in this", "what's the weak point", "am I being fooled here?". It runs an ordered two-level pass: first test whether the EVIDENCE is sound (independent, current, primary, actually corroborated rather than repeated), then test whether the INFERENCE follows (reconstruct the argument, steelman it, find the load-bearing assumption, and run only the few checks that matter for this argument). It reports three tiers, sound / load-bearing flaw / nitpick, and suppresses the nitpicks. Anti-slop by design: it separates "the argument is weak" from "the conclusion is false", only raises a flaw when fixing it would change what the argument establishes, and never dismisses a claim just by naming a fallacy. Triggers on "is this argument sound", "critique this reasoning", "does this hold up", "stress-test this", "check my logic", "steelman / devil's advocate", "is this claim trustworthy". Composes with multi-lens-research, which gathers and verifies evidence at scale; this skill owns the reasoning discipline applied to an argument already in front of you.
---

# Critical reasoning

Judge whether a claim, argument, or decision **actually holds up**, separately from whether it
*sounds* convincing. The job is not to produce the texture of rigor (fallacy names, symmetric
hedges, a wall of objections). It is to find the one or two things the conclusion actually rests
on and test *those*.

Two failure modes bracket this skill, and it is built to avoid both:

1. **Credulity:** accepting a confident, well-written argument because nothing in it looked
   wrong, when its evidence was one recycled source or its load-bearing step never followed.
2. **Slop:** the more seductive failure for an AI. Hunting fallacies, labeling every
   technically-present imperfection, and lowering your estimate of a claim's truth because its
   argument is flawed. This *looks* like critical thinking and actively lowers answer quality.
   Empirically, an LLM turned loose to critique its own confident, correct output flips more
   right answers to wrong than the reverse (`references/method.md`). So the default here is to
   **critique almost nothing** and to earn every flaw you raise.

**The one rule that prevents the worst output:** a flawed argument does not make its conclusion
false. Truth is a property of claims; fallacies are defects in reasoning. So keep two verdicts
separate and never merge them: **argument soundness** (does this reasoning, as given, support its
conclusion?) and **conclusion plausibility** (how likely is the claim, on the evidence?). When
you find a flaw, the verdict is "this reasoning does not establish the conclusion" (the claim is
now unsupported, open), never "the conclusion is false." Lowering a claim's truth-estimate
because its argument is weak is itself the most common misuse of reasoning skill (the fallacy
fallacy), and committing it in your own output is the worst thing this skill can do.

## How this composes with other skills

- **`multi-lens-research`** and this skill share the same Level-1 evidence rules on purpose
  (independence, incentives, recency, corroboration-not-repetition, refute-don't-confirm,
  diagnosticity), so they never give contradictory advice. The difference is **workflow vs
  discipline**:
  - `multi-lens-research` is the **research workflow**: when you must go *gather and vet a large
    body of sources*, it fans out distinct lenses, adversarially verifies load-bearing claims,
    and returns a cited report. It operationalizes Level 1 at scale.
  - `critical-reasoning` (this skill) is the **portable discipline**: the two-level pass you
    apply to an argument *already in front of you*, with no search fan-out.
  - They **compose both ways.** A research run hands its verified findings here for the inference
    check ("the sources are solid, does the conclusion follow?"). A reasoning task that turns out
    to need real evidence-gathering ("I cannot judge this without checking the sources") hands
    off to `multi-lens-research`. If it is installed, use it for the evidence step instead of
    eyeballing; if not, apply `references/evidence.md` with the web tools you have.
- **A writing or voice skill** (if active) owns the final prose. This skill owns which criticisms
  are real and how strongly to make them; hand off the graded findings, not tone.

## The method

Match effort to stakes. A throwaway claim gets step 3 and a one-line verdict; a decision memo, a
load-bearing PR argument, or a "should we do X" call gets the whole pass. Announce the depth.

### Step 1: Reconstruct the argument

You cannot test an argument you have not made explicit. Restate it as:

- **Claim / conclusion:** what you are being asked to accept.
- **Grounds / evidence:** the facts it starts from.
- **Warrant:** the (usually unstated) inferential license connecting grounds to claim. This is
  the *bridge*, and it is where most real arguments fail. Surface it explicitly.
- **Qualifier / rebuttal:** how strongly is the claim made, and under what conditions would it
  not hold? (Toulmin; see `references/method.md`.)

If there is no real argument (a bare assertion, a preference, a joke), say so and stop. Do not
manufacture one to critique.

### Step 2: Steelman before you touch it

State the argument in its **strongest honest form** before looking for weaknesses. Fix obvious
slips, supply the most reasonable version of an unstated premise, engage the position the author
*meant*. Two reasons: attacking a weak paraphrase (straw man) proves nothing, and steelmanning
routinely dissolves a "flaw" that was only an uncharitable reading. If the strongest version
holds, you are done: report it sound. Later, when you have a candidate flaw, re-read this
steelman and check the flaw still bites against *that* version, not the weaker original.

Interpretive honesty caveat: steelman the argument they made, do not substitute a better argument
of your own and then credit it to them.

### Step 3: Level 1, test the evidence (the foundation, do this before inference)

Rank the argument's evidence by **load**: how much the conclusion depends on each piece.
Scrutinize the load-bearing evidence; ignore decorative detail. For each load-bearing piece, ask,
in order:

1. **Origin:** primary source, or a retelling of a retelling? Trace to the closest-to-source.
2. **Independence:** do the "multiple sources" actually trace to one origin? Three articles
   repeating one press release are **one** source, not three. Repetition is not corroboration.
3. **Incentive:** who benefits if you believe this, and did they produce the evidence? Discount
   self-serving evidence; *up*-weight evidence against the producer's own interest.
4. **Recency:** still true today? Date the *data*, not just the article.
5. **Prior plausibility:** how likely was this before the evidence? Extraordinary claims need
   proportionally stronger, harder-to-fake evidence.
6. **Data quality:** selection bias, survivorship bias, sample size, missing denominator?
7. **Verify laterally:** check what the rest of the record says about the source, rather than
   judging it by staring at the source itself.
8. **Disconfirmation:** did anyone look for evidence *against* this, or only for support?

**If the load-bearing evidence fails here, stop and say so.** A slick inference on bad evidence
establishes nothing, and this is exactly where an inference-only critique gets fooled. These
rules are the same evidence principles the `multi-lens-research` skill teaches; the full rubric
and named frameworks (SIFT, ACH, the independence rule, evidence hierarchies) with their caveats
are in `references/evidence.md`.

### Step 4: Level 2, test the inference

Granting the evidence, does the conclusion follow? Do not run down a fallacy list. Instead:

1. **Classify the argument's structure**, because it decides what "the load-bearing point" even
   means:
   - **Single-crux:** one premise or warrant carries the conclusion. Find it (below) and test it.
   - **Conjunctive** (needs A *and* B *and* C, e.g. a migration plan): the crux is the *weakest
     necessary link*. Test that, not all of them.
   - **Cumulative** (no single reason is load-bearing; the aggregate carries it, e.g. "acquire
     them: five independent reasons"): the question is whether the *combined weight* clears the
     bar, so judge the sum, not each leg in isolation. A pile of individually-weak reasons can
     still fail as a pile even though no single one is decisive.
   - **Graded** (a recommendation with a confidence, "do X, 70%"): a flaw counts if it produces a
     *material* shift in the confidence or decision (moves "confident go" to "coin flip"), and
     you must state the shift.
2. **Name the argument's type** (appeal to expert opinion, analogy, cause-from-correlation,
   generalization from examples, prediction of consequences, ...). Each type has 3 to 5 standard
   **critical questions** that test exactly it (Walton's schemes; `references/method.md`). The
   type selects the checks; this is the published antidote to a glossary.
3. **Find the load-bearing assumption (the crux).** Which single premise or warrant, if it fell,
   would collapse the conclusion (or, per structure, the weakest necessary link)? The sensitivity
   test: "which one input, if wrong, flips the answer?" That is what you test.
4. **Run only the 2 to 3 checks aimed at that joint.** The type's critical questions, plus, as
   they apply: is the evidence *diagnostic* (does it discriminate between competing explanations,
   or is it equally consistent with the opposite conclusion)? What would change your mind? A
   confounder, a base rate ignored, a term that shifts meaning, a jump from a small sample?
   `references/fallacies.md` and `references/biases.md` are the reach-in catalogs, keyed by which
   are high-yield and which have legitimate forms you must not flag.
5. **Generate at least one alternative** and try to *disconfirm* the favored conclusion rather
   than pile up support. If you cannot find a real defeater after looking, that is a finding: the
   inference holds.

**Many named fallacies are not errors.** Appeal to authority, ad hominem, slippery slope, and
most informal fallacies are corrupted forms of *legitimate* arguments; the name flags a shape,
not an error. Citing relevant expert consensus, attacking a source when its credibility *is* the
evidence, or a slope with well-supported links are all sound. Check the legitimate-use conditions
in `references/fallacies.md` before flagging any of them.

### Step 5: Grade, self-audit, and report

Sort what you found into exactly three tiers, and gate every flaw with a written self-audit.

**The forcing function (run it on every candidate flaw, quick-check path included):** before you
report a flaw, complete this sentence in writing:

> "If this were fixed, what the argument establishes would change from ___ to ___."

If you cannot complete it truthfully, it is a **nitpick**: cut it, or add it to a suppressed
count. "Changes what the argument establishes" means the supported conclusion, its warrant, or a
graded recommendation's decision or hedge, **not** the truth-value of the claim. This turns the
change-the-conclusion bar from a principle into an observable step. Two structure-specific notes,
so the audit does not misfire: for a **cumulative** argument the unit of the audit is the
*aggregate* (does the combined weight still clear the bar?), not each leg in isolation, or you will
suppress every individually-minor weakness and wave through a weak pile. For a **graded** argument,
measure the confidence shift against the confidence the argument *actually stated* (or one you
explicitly flag as your own estimate), never a baseline you invented to manufacture a shift.

The three tiers:

- **Sound:** the argument, on its evidence, supports its conclusion. Say so plainly. This is a
  real and common verdict, not a failure to find something.
- **Load-bearing flaw:** a specific step that passed the self-audit. State it in plain language,
  in context: *which* step fails, *why it fails here*, and *what the conclusion becomes* once you
  account for it (unsupported, weaker, or contingent on X). A fallacy name is optional shorthand
  and never stands alone; it is always followed by the in-context "why."
- **Nitpick:** technically present, does not change what the argument establishes. **Suppress
  these by default**; report only a count ("set aside 3 immaterial points") so thoroughness is
  visible without dumping the wall.

A request to "poke holes", "find the weak point", or "what am I missing" is a leading prompt, not
evidence that a flaw exists. The honest and common answer is "I looked; it holds, and here is the
one thing worth verifying." Do not manufacture a flaw to satisfy the phrasing, and do not launder
the suppressed nitpicks into a *verification* wall instead. A verification suggestion faces the
same test (would this check, if it came back bad, change what the argument establishes?), so name
at most the one or two highest-value checks, not a list.

## Hard gates (the anti-slop contract)

These are the gates that separate this skill from a fallacy labeler. Each is checkable against
your own output before you emit it:

1. **Two verdicts, never merged.** Argument soundness and conclusion truth stay separate. A flaw
   yields "unsupported", never "false".
2. **Change-the-conclusion bar, enforced by the self-audit.** No flaw ships unless you have
   written "if fixed, the argument now establishes ___ instead of ___". Everything else is a
   suppressed nitpick.
3. **No naked fallacy names.** Every flaw is shown in context ("this step fails *here* because
   ..."), not asserted by label. If you cannot say why it fails *in this case*, you have not
   found a flaw.
4. **Steelman first, and check the flaw bites the steelman.** Attack the strongest version or you
   have attacked nothing.
5. **Critique almost nothing.** Default to trusting a sound-looking argument on a routine,
   confident case. A leading request to critique is not evidence a flaw exists. Prefer an external
   check (a source, a test, a re-derivation) over pure introspection.
6. **Symmetry, including the request itself.** Apply the same scrutiny to the side you (or the
   user) favor as to the side you oppose. When only one side is submitted, symmetry also means
   surfacing what is *strong* in it, the weakest point in the requester's own implied position,
   and any motivated framing in the request ("resume-driven", "obviously", "just hype"). A flaw is
   never grounds to dismiss a person, and "you're biased" is not a refutation.
7. **Evidence before inference.** Test Level-1 evidence first. If the load-bearing evidence fails,
   report "unsupported at the evidence layer" and stop; do not proceed to fallacy-hunting on top
   of bad evidence.
8. **Evidence wins on truth.** A well-sourced, verified claim is not overturned by a weakness in
   the argument attached to it. On *what is true*, defer to the evidence (and to
   `multi-lens-research`); confine yourself to *how well the reasoning supports it*.
9. **Know your limits.** When judging the claim needs domain knowledge you do not have, say so and
   say what would settle it, rather than applying a generic template with false confidence.

## Anti-patterns (what this skill refuses to do)

- **Name-the-fallacy output.** "That's a slippery slope / ad hominem" with no in-context reason.
  Most such labels are wrong or immaterial.
- **Rejecting a conclusion because its argument is flawed** (the fallacy fallacy).
- **Nitpick walls.** Ten true-but-immaterial objections that hide the zero-or-one that matters.
- **False rigor.** Fallacy vocabulary and symmetric hedges that add no epistemic work, attacking
  peripheral points while the load-bearing premise stands untouched.
- **Weaponized critique.** Using "that's a fallacy" to dismiss a person or a claim the user
  already wanted to defeat.
- **Fallacy-spotting on unexamined evidence.** Jumping to the inference check while the argument
  rests on one recycled, interested, stale source. Level 1 comes first.
- **Critiquing to look useful.** Inventing flaws in a sound argument because saying "this holds"
  feels like doing nothing. "It holds" is the correct answer more often than not.

## Reference files (load as needed)

- `references/method.md`: the full end-to-end process, the Toulmin reconstruction, Walton's
  argumentation schemes and critical questions (the anti-glossary engine), load-bearing / crux
  finding, the constructive moves (steelman solitaire, "what would change my mind", qualitative
  Bayesian updating, ACH), and the evidence on why intrinsic self-critique must be used sparingly.
  Cited.
- `references/evidence.md`: the Level-1 evidence rubric, aligned with `multi-lens-research`'s
  `verification.md`: origin, independence, incentive, recency, prior plausibility, data quality,
  lateral verification, and disconfirmation, with the named frameworks and their caveats. Cited.
- `references/fallacies.md`: the high-yield Level-2 fallacy set, each with a precise definition,
  when it actually breaks a conclusion vs when flagging it is a nitpick, and the **legitimate
  forms** of the contested ones you must not flag. Leads with the fallacy fallacy. Cited.
- `references/biases.md`: the cognitive biases that actually distort reasoning, filtered for
  replication (robust ones to use, contested ones to caveat, debunked ones to drop), each with
  its constructive counter-move. Cited.
- `assets/analysis-template.md`: a fill-in template for a full two-level analysis, from
  reconstruction to graded verdict.

## Prose style

Write plainly and make every criticism concrete. Avoid em dashes in any prose you generate;
recast with commas, periods, colons, parentheses, or "to" for ranges. Em dashes read as an AI
tell.
