# Level 2: fallacies, the high-yield set (and when they are not errors)

This is a reach-in catalog, not a checklist to run top to bottom. The method (`SKILL.md`,
step 4) is: name the argument's *type*, find the load-bearing joint, and run only the two or
three checks that test *that*. You come here to get a specific check right, not to pattern-match
labels onto prose. A named fallacy is at most shorthand for an in-context explanation you still
have to give.

## Read this first: naming a fallacy is not a refutation

**The fallacy fallacy** (argument from fallacy, *argumentum ad logicam*): inferring that a
conclusion is **false** because an argument for it is fallacious. This is itself an error, and
it is the single most likely way a reasoning tool misfires. Truth is a property of *claims*;
fallacies are defects in *reasoning*. A bad argument for P leaves P's truth exactly where it
was, and true claims are supported by weak arguments constantly.
`[EXTERNAL]` https://en.wikipedia.org/wiki/Argument_from_fallacy ;
https://effectiviology.com/fallacy-fallacy/

So the verdict when you find a fallacy is always **"this reasoning does not establish the
conclusion"** (the claim is now unsupported, open), never **"the conclusion is false."** Keep
argument-soundness and conclusion-truth as two separate verdicts, and never lower your estimate
of a claim's truth just because its argument is weak.

**Most informal fallacies are not automatic errors.** This is the mainstream position in
informal-logic and argumentation theory, not a fringe take. Named informal fallacies are largely
*corrupted forms of legitimate argument types*, defeasible and context-dependent: the same shape
is reasonable in one context and fallacious in another. `[EXTERNAL]` Walton, "The Contextuality
of Fallacies", https://informallogic.ca/index.php/informal_logic/article/view/464 ; Hamblin
(1970) on the "debased, worn-out and dogmatic" textbook treatment; SEP, Fallacies,
https://plato.stanford.edu/entries/fallacies/ . Practical consequence: for every fallacy tagged
**CONTESTED** below, check the legitimate-use conditions *before* flagging. Flagging a legitimate
form is itself a reasoning error, and the noisier half of slop.

## The high-yield informal fallacies

Ordered by how often they actually flip real-world conclusions *when one is present*. Read the
order as "if this argument has a genuine flaw, here is where to look first", not as "expect to
find one". **Most well-constructed arguments commit none of these**, and walking in expecting a
hit is itself confirmation bias. The `[HIGH]` tag means high-yield when present, not common. For
each: definition, when it **breaks** a conclusion, and when flagging it is a **nitpick** (or not
a fallacy at all).

### Correlation treated as causation `[HIGH]`
Inferring A causes B from the fact that A and B correlate (or A preceded B), ignoring
confounders, coincidence, or reverse causation. Three named failure modes to check: **confounder
/ common cause** (ice cream sales and drownings both track heat), **reverse causation** (B causes
A), **coincidence** (spurious correlation). *Breaks:* whenever a causal claim rests on correlation
alone. *Nitpick:* if the argument only claims association or prediction, or if causation is backed
by more than correlation (a trial, a mechanism, dose-response, temporal order with confounders
controlled). The single highest-yield real-world fallacy. `[EXTERNAL]` SEP, Fallacies.

### Base-rate neglect `[HIGH]`
Judging a probability from case-specific detail while ignoring the prior prevalence. A
90%-accurate test for a 1%-prevalent condition still yields only about an 8% chance of the
condition on a positive result, because false positives from the large healthy majority swamp
true positives. *Breaks:* any probability, diagnosis, screening, or profiling claim that ignores
a base rate that would change the answer. *Nitpick:* when base rates are genuinely uninformative
or already incorporated. Highest-yield fallacy for any quantitative or risk argument.
`[EXTERNAL]` https://en.wikipedia.org/wiki/Base_rate_fallacy

### Cherry-picking / Texas sharpshooter `[HIGH]`
**Cherry-picking:** presenting only the data that supports the conclusion, ignoring contrary
data. **Texas sharpshooter:** finding a pattern in noise *after the fact* by drawing the target
around a cluster (choosing the hypothesis to fit the data you happened to see). *Breaks:* when the
full evidence set would change the conclusion, or a post-hoc pattern is sold as if predicted.
*Nitpick:* when the selection is representative or the hypothesis was genuinely specified in
advance. Sibling: **survivorship bias**, drawing conclusions only from the cases that passed a
filter while the failures that would flip the inference are invisible (the WWII bomber-armor
example). `[EXTERNAL]` https://en.wikipedia.org/wiki/Texas_sharpshooter_fallacy ;
https://en.wikipedia.org/wiki/Survivorship_bias

### Straw man `[HIGH]`
Refuting a distorted, weakened version of a position, then treating the real position as
refuted. *Breaks:* whenever the refuted claim is not the one actually held; the conclusion
"your position fails" does not follow because that position was never engaged. *Nitpick:* if the
restatement is a fair (even if unflattering) paraphrase. Test: would the arguer accept your
restatement? (This is why step 2 steelmans first.)

### Hasty generalization `[HIGH]`
A general conclusion from a sample too small, biased, or unrepresentative to support it.
*Breaks:* when the sample cannot bear the scope of the conclusion. *Nitpick:* when the sample is
actually adequate, or the conclusion is properly hedged ("some", "in my limited experience"). It
is about the *jump from sample to scope*, not about ever generalizing.

### False dilemma `[HIGH]`
Presenting two (or too few) options as exhaustive when live alternatives exist, forcing a choice
among the offered few. *Breaks:* when a real third option would change the conclusion. *Nitpick:*
when the options genuinely are exhaustive (true dilemmas exist: an integer is even or odd) or the
middle options would not rescue the argument. Flag binaries that *suppress live alternatives*,
not every binary.

### Equivocation `[HIGH]`
Trading on a term used with two different meanings across the argument, so the inference works
only if the meanings are illicitly treated as one. *Breaks:* when disambiguating the term makes
the premises stop connecting. *Nitpick:* when the term is used consistently, or the ambiguity is
harmless wordplay that does not carry the inference.

### Circular reasoning / begging the question `[HIGH]`
The conclusion is assumed among the premises (often as an equivalent restatement or a smuggled
contested term), so the argument gives no independent support. Note: these are often *valid*;
the fault is being epistemically useless, unable to move a doubter. *Breaks:* when the exact
premise a reasonable interlocutor would dispute is what gets assumed. *Nitpick:* every valid
deduction "contains" its conclusion in some sense; flag only when a *contested* premise is the
conclusion restated. `[EXTERNAL]` SEP, Fallacies.

### Ad hominem `[HIGH]` **CONTESTED**
Rejecting a claim because of a feature of the person advancing it rather than its merits.
*Breaks:* when the person's trait is offered as the reason the claim is false, while the claim
stands on independent evidence. **Legitimate form (do not flag):** when source credibility *is*
the evidence at issue. If someone says "trust me, I'm an expert", noting that they are biased,
dishonest, or unqualified is a valid rebuttal of *that appeal*, not a fallacy. Check first: does
the argument rest on the source's credibility? `[EXTERNAL]` SEP, Fallacies; ad hominem as
legitimate rebuttal, https://informallogic.ca/index.php/informal_logic/article/view/2990/2442

### Appeal to authority `[HIGH]` **CONTESTED**
Treating an authority's pronouncement as evidence when the source is not a *relevant* expert, is
fringe against consensus, or is offered as *proof* rather than defeasible support. **Legitimate
form (do not flag):** citing genuine, relevant, consensus expert testimony is a reasonable
defeasible inference, the normal way non-specialists form beliefs. Walton's six critical
questions decide it: (1) is E actually an expert, (2) in *this* field, (3) did E actually assert
it, (4) is E trustworthy/unbiased, (5) do other experts agree, (6) is it backed by evidence?
*Breaks* only when one of those fails. `[EXTERNAL]` Walton, *Appeal to Expert Opinion*.

### Slippery slope `[HIGH]` **CONTESTED**
Arguing a first step must be rejected because it will *inevitably* chain to an unacceptable
outcome, when the intermediate links are unsupported. **Legitimate form (do not flag):** a slope
whose links are each independently probable and evidenced is valid consequentialist reasoning.
The quality is in the *link probabilities*, not the shape. *Breaks:* when links are asserted as
inevitable but are weak. Evaluate the transitions, not the form. `[EXTERNAL]` IEP, Fallacies,
https://iep.utm.edu/fallacy/

## Second tier (still useful, more specialized)

- **Motte-and-bailey** `[HIGH]`: advancing a controversial claim (bailey), then when challenged
  retreating to a modest, easily-defended one (motte) as if that were the point, then
  re-advancing the bailey. *Breaks:* when the modest claim's defensibility is used to launder
  the controversial one, which never earned support. Requires tracking claim-substitution across
  an exchange.
- **No true Scotsman** `[HIGH]` **CONTESTED**: defending a generalization against a counterexample
  by arbitrarily redefining the category ("no *true* X does that"). *Breaks:* when the
  redefinition is ad hoc. *Not a fallacy:* when the exclusion rests on a principled, independent
  definition ("no vegetarian eats beef" is just the definition).
- **Sunk cost** `[MED]` **CONTESTED**: justifying continued investment by resources already spent
  rather than expected future value. *Breaks:* when only past spend is cited. *Not a fallacy:*
  when genuine forward-looking reasons (near completion, option value, contractual cost of
  quitting) justify continuing.
- **Appeal to popularity / bandwagon** `[HIGH]`: "many believe or do it, so it is true/right."
  *Breaks:* on matters of fact. *Narrow legitimate cases:* claims *about* popularity, convention-
  constituted facts (language usage), or many *independent* judges (wisdom of crowds, which is
  closer to expert consensus).
- **Appeal to nature** `[MED]`: "natural, therefore good/safe." *Breaks:* when "natural" does the
  evaluative work with no independent reason (arsenic and hemlock are natural; many synthetic
  medicines save lives).
  *Nitpick:* when "natural" is shorthand for a real evidenced property.
- **Composition / division** `[HIGH]`: inferring the whole has a property because the parts do
  (composition), or each part has it because the whole does (division). *Breaks:* for
  **additive** properties (each part is light, but the weights sum, so the plane is
  heavy) and for **emergent/interactive** properties (each neuron is unconscious, the brain is
  conscious). *Not a fallacy:* for genuinely **distributive** properties ("every brick is red,
  so the wall is red"). Test: does the property aggregate or emerge (fallacy) or distribute
  unchanged to the whole (valid)?

## Formal fallacies (short: rarer in real prose)

Invalid by *structure* regardless of content. In real arguments these usually surface as hidden
conditional reasoning.

- **Affirming the consequent:** `If P then Q. Q. Therefore P.` Invalid. ("The ground is wet,
  therefore it rained": a sprinkler also wets the ground.) Contrast valid modus ponens.
- **Denying the antecedent:** `If P then Q. Not P. Therefore not Q.` Invalid. Contrast valid
  modus tollens.
- **Undistributed middle:** `All A are B. All C are B. Therefore all C are A.` Invalid; the
  shared term B never links A and C. ("All dogs are mammals; all cats are mammals; therefore
  cats are dogs.")

Even a formally invalid argument can have a true conclusion (the fallacy fallacy again): "invalid"
means "not established by this argument", not "false". `[EXTERNAL]`
https://en.wikipedia.org/wiki/Affirming_the_consequent and companion pages.

## Sources

SEP, Fallacies: https://plato.stanford.edu/entries/fallacies/ . IEP, Fallacies:
https://iep.utm.edu/fallacy/ . Walton, *Argumentation Schemes* (Cambridge 2008) and *Appeal to
Expert Opinion* (PSU Press). Wikipedia entries linked inline for individual fallacies. All public.
