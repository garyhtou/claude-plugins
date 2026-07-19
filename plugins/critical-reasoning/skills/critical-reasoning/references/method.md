# The method in full: structure, schemes, cruxes, and constructive moves

`SKILL.md` has the five-step spine. This file is the depth behind it: the frameworks that make
each step a real procedure rather than a vibe, and the evidence for why the skill is tuned to
critique sparingly. Every framework here is a published one, cited, so the method is not invented.

## Why the default is "critique almost nothing"

The tempting design (turn a model loose to find flaws in reasoning) is net-negative by default,
and the evidence is strong enough that it sets the skill's whole posture.

- Intrinsic self-correction, with no external feedback, **degrades** reasoning: the model cannot
  reliably tell sound from flawed reasoning in its own output, so revision flips about as many
  correct answers to wrong as the reverse, for no net gain and often a net loss. The paper reports
  GPT-4's GSM8K accuracy *dropping* across successive self-correction rounds rather than rising.
  `[EXTERNAL]` Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet*, ICLR 2024,
  https://arxiv.org/abs/2310.01798 (abstract: "at times, their performance even degrades after
  self-correction")
- Stress-tested generate-criticize-improve loops confirm it: on tasks a model already did well,
  a critic "primed to find errors invented them", and accuracy collapsed. The rule that survives:
  **critique is for debugging, not polishing.** `[EXTERNAL]` Snorkel AI, "The Self-Critique
  Paradox", https://snorkel.ai/blog/the-self-critique-paradox-why-ai-verification-fails-where-its-needed-most/
- Self-correction reliably helps only with an **external signal** (a source, a test, a tool, a
  second independent derivation). `[EXTERNAL]` CRITIC and the broader self-correction literature.

Design consequences, baked into the gates: engage the full pass only when stakes are real or you
are genuinely uncertain; prefer an external check over introspection; and treat "the argument
holds" as the expected, correct output most of the time. A skill that critiques everything is
worse than no skill.

## Step 1 depth: Toulmin reconstruction

Decompose the argument into its parts before testing it. Toulmin's six (the first three are
load-bearing): `[EXTERNAL]` Purdue OWL,
https://owl.purdue.edu/owl/general_writing/academic_writing/historical_perspectives_on_argumentation/toulmin_argument.html

- **Claim:** the conclusion to be accepted.
- **Grounds:** the evidence it starts from.
- **Warrant:** the inferential license from grounds to claim, usually *unstated*. Grounds are one
  riverbank, the claim is the far bank, the warrant is the bridge. Most bad arguments fail at the
  bridge, and because it is implicit, you have to *say it out loud* to test it. Surfacing the
  warrant is the highest-value move in reconstruction.
- **Backing:** support for the warrant itself.
- **Qualifier:** how strongly the claim is asserted ("probably", "in most cases"). The built-in
  calibration slot.
- **Rebuttal:** the conditions under which the claim would not hold. The built-in humility slot.

Caveat: Toulmin is a *diagnostic layout*, not a decision procedure; the lines between grounds,
warrant, and backing are fuzzy and analysts label the same sentence differently. Use it to force
the implicit inference into the open, not to litigate categories.

## Step 4 depth: argumentation schemes and their critical questions

This is the published **antidote to a fallacy glossary**, and the most important idea in the
method. Instead of a flat list of ~50 named errors with binary verdicts, Walton's model says:
first identify what *type* of argument you face, and each type comes bundled with a short list of
**critical questions** that test exactly that type. The argument's shape *selects* the few checks
worth running. An argument is treated as presumptively acceptable until a specific critical
question is left unanswered, and that is what shifts the burden of proof. `[EXTERNAL]` Walton,
Reed & Macagno, *Argumentation Schemes* (Cambridge, 2008);
https://www.reasoninglab.com/patterns-of-argument/argumentation-schemes/waltons-argumentation-schemes/

Common types and their critical questions (keep to the handful that fit; do not recite):

- **Appeal to expert opinion.** Is E genuinely an expert *in this field*? Do other experts agree?
  Is the assertion backed by evidence? Is E trustworthy and unbiased? Did E actually say it? Is
  it inside E's field?
- **Argument from analogy.** Are the two cases alike in the *relevant* respects? Are there
  relevant *disanalogies* that break the mapping? Is there a better-fitting comparison case?
- **Cause to effect.** Is there a plausible mechanism, not just correlation? Could a third factor
  cause both? Could the causation run the other way? Do other known causes intervene?
- **Argument from sign.** Does the indicator reliably track the thing, or are there common false
  positives? What is the base rate of the indicator without the thing?
- **Argument from popularity / practice.** Is what is popular actually a guide to what is true or
  right here, or only to what is common? Are the "many" independent or a herd?
- **Argument from consequences / slippery slope.** Are the predicted consequences real and
  probable, with each causal link independently supported? Or asserted as inevitable on a weak
  chain?

Caveats to hold: a scheme's critical-question list is never provably complete (the argument stays
"open to further questioning"), and whether an unanswered question *defeats* the argument or only
*shifts the burden* is debated. And the full taxonomy runs to 60+ schemes: use the *idea* (type,
then its few questions), not the whole catalog.

## Step 4 depth: find the load-bearing assumption (the crux)

Not all premises hold up the conclusion; some are load-bearing and most are not. The crux is the
one premise or warrant that, if it fell, collapses the conclusion. Finding it is what lets you run
two or three checks instead of twenty.

First, though, the argument's **structure** decides what "load-bearing" means, and getting this
wrong makes the change-the-conclusion bar misfire in both directions:

- **Conjunctive** (the conclusion needs A *and* B *and* C, e.g. "the migration works if the
  dual-write holds and the backfill finishes and the cutover is atomic"): every link is necessary,
  so the crux is the **weakest necessary link**. Test that one; do not flag all of them (that is a
  justified-looking wall).
- **Cumulative** (no single premise is load-bearing; the aggregate carries it, e.g. "acquire them:
  the tech is ahead, the team is strong, the price is cheap, the fit is good"): no single reason
  flipping changes the conclusion, so a per-reason change-the-conclusion bar would suppress *every*
  weakness and greenlight a weak aggregate. Judge the **sum**: does the combined weight clear the
  bar, and are the reasons actually independent or double-counting one thing?
- **Graded** (a recommendation with a confidence, "do X, 70%"): a flaw counts if it drives a
  **material** shift in the confidence or the decision (turns "confident go" into "coin flip"),
  and you must state that shift rather than rounding "still X" to unchanged.
- **Single-crux:** the remaining, common case, where one premise or warrant carries it. The tools
  below (sensitivity, double crux) are for this case.

- **Sensitivity test:** "which single input, if wrong, flips the conclusion?" That input is where
  your scrutiny goes. `[EXTERNAL]` Key Assumptions Check, CIA *Tradecraft Primer*,
  https://www.cia.gov/resources/csi/static/Tradecraft-Primer-apr09.pdf
- **Premise-level vs inference-level:** name *which* you are contesting. Either you dispute a
  stated input ("that statistic is wrong", a Level-1 evidence problem) or you grant the inputs
  and dispute that they *support* the conclusion ("even if true, that does not follow", a warrant
  problem). Conflating the two is how people argue past each other.
- **Double crux (for a disagreement):** find a statement B such that if B flipped, each side would
  change its conclusion, then argue only about B. Most debates fail by arguing everything except
  the thing that actually matters. `[EXTERNAL]`
  https://www.lesswrong.com/posts/exa5kmvopeRyfJgCy/double-crux-a-strategy-for-mutual-understanding .
  Caveat: real disagreements often have several partial cruxes; use "find the load-bearing
  assumption" as the durable idea and double-crux as one technique.

## The constructive moves (reasoning is not only detection)

Good reasoning builds as much as it breaks. These are the moves worth making, and several are
cheap universal checks that need no fallacy at all.

- **Steelman, and steelman solitaire.** State the strongest honest version first (principle of
  charity; Rapoport's rules: re-express the position so well the author says "I wish I'd put it
  that way", note agreements, say what you learned, *then* rebut). Solo version: argue with
  yourself in a nested outline (position, strongest counter, strongest counter-counter), killing
  weak branches fast. It removes the social pressure to defend and often changes your own mind.
  `[EXTERNAL]` Dennett, *Intuition Pumps*; Charity Entrepreneurship, "steelman solitaire". Honesty
  caveat: steelman the argument they *made*, do not swap in a better one of your own and credit it
  to them.
- **"What would change my mind?"** Before defending a claim, name the observation that would make
  you abandon it. If nothing could, the belief is not tracking evidence. The single best one-line
  reasoning prompt.
- **Diagnosticity over fit.** Do not ask "is this evidence consistent with my view?" (almost
  everything is). Ask "is it *more expected under my hypothesis than under the alternative*?"
  Evidence that fits every hypothesis equally has near-zero value. `[EXTERNAL]` Analysis of
  Competing Hypotheses, Heuer.
- **Qualitative Bayesian updating.** Posterior scales with prior times likelihood ratio: how
  plausible was the claim *before* this evidence, and how much *more expected* is the evidence if
  the claim is true than if false? Keep it qualitative (direction and rough magnitude). Putting
  invented numbers on it is false precision, and garbage priors give garbage posteriors. Use it to
  force consideration of base rates and alternatives, not as theater.
- **Generate at least two hypotheses and try to disconfirm.** A cheap structural guard against
  tunnel vision: the moment you have only one explanation, you will find confirmations for it.

## A note on transfer and humility

Generic critical-thinking skill transfers poorly across domains; competence is heavily
domain-knowledge-dependent (judging a history claim needs source rules, a clinical claim needs
trial literacy). `[EXTERNAL]` Halpern, teaching CT for transfer; education-research transfer
findings. The honest consequence, and gate 8: when judging the claim needs domain knowledge you do
not have, say so and say what would settle it, rather than applying a generic template with false
confidence. "I cannot assess the domain claim, here is what would" beats a confident domain-blind
verdict.

## Sources

Toulmin, *The Uses of Argument* (1958); Purdue OWL Toulmin page. Walton, Reed & Macagno,
*Argumentation Schemes* (Cambridge 2008); Reasoning Lab scheme catalog; Walton & Godden on
critical questions. Heuer, *Psychology of Intelligence Analysis* (CIA 1999) and the CIA
*Tradecraft Primer* (2009). LessWrong on double crux and cruxes. Dennett, *Intuition Pumps and
Other Tools for Thinking* (2013). Huang et al., ICLR 2024; Snorkel AI self-critique writeup. RAND
RR-1408 on the thin empirical base for structured analytic techniques. All public.
