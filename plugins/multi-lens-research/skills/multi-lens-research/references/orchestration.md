# Orchestration: parallel fan-out and the sequential fallback

Same method, two wirings. Use the parallel fan-out when your harness can run
subagents concurrently; use the sequential fallback when it cannot. The rigor is
identical; only throughput differs.

## Choosing a mode

- **Parallel fan-out** when you have a subagent or workflow primitive that runs
  several agents at once (for example Claude Code's Task tool, a workflow runner, or
  any orchestration layer that spawns concurrent agents). This is the default for
  anything above a quick check: it is faster and, more importantly, keeps the lenses
  genuinely independent because each runs in its own context and cannot see the
  others mid-gather.
- **Sequential fallback** when you are a single agent with only your own tool calls.
  You emulate the lenses by rotating through them yourself, one focused batch at a
  time, keeping a running ledger so you do not let earlier findings contaminate later
  lenses.

## Parallel fan-out (recommended)

Pattern, in three stages: **fan out the lenses, verify each load-bearing claim,
synthesize.** Pseudocode (adapt to your harness's actual subagent API):

```
lenses = ["academic", "technical", "applied", "news", "contrarian"]   # +deep set for high stakes

# Stage 1: gather, one subagent per lens, in parallel. Each is blind to the others.
lens_results = parallel(
  lenses.map(lens =>
    () => subagent(prompt_for(lens, question, sub_questions))   # returns claims[]
  )
)                                                               # BARRIER: need all lenses before dedupe

claims = dedupe(flatten(lens_results))        # merge; collapse duplicate claims, keep all distinct sources
load_bearing = rank_by_load(claims).top()     # the claims the conclusion rests on

# Stage 2: adversarially verify load-bearing claims, in parallel.
verified = parallel(
  load_bearing.map(claim =>
    () => refute_by_majority(claim, skeptics=3)   # keep only if majority fail to refute
  )
)

# Stage 3: synthesize from verified + contested + gaps.
report = synthesize(claims, verified, contradictions(claims), open_sub_questions)
```

Notes that matter:

- **The dedupe is a real barrier.** You need every lens back before you can tell
  which claims overlap and which contradict. This is one of the few places a barrier
  is correct; the verify stage after it can stream per-claim.
- **Dedupe by claim, keep sources.** Two lenses finding the same fact is
  corroboration; collapse the claim but keep both citations (that is what raises
  confidence). Two lenses finding opposite facts is a contradiction; keep both and
  flag it.
- **The contrarian lens runs in the same fan-out**, not as an afterthought. Its
  findings are what populate the "contested" and "risks" parts of the synthesis.
- **Later rounds re-enter Stage 1** with narrowed prompts aimed at the weak/contested
  claims and the open sub-questions (see "loop until dry" below).
- **A dead or empty lens is not fatal.** If one lens returns nothing, note the gap and
  proceed; do not block the whole run on it.

## Sequential fallback (single agent, no parallelism)

You cannot spawn agents, so you *become* each lens in turn. The trap to avoid is
letting lens 1's answer frame lens 5's search. Counter it with an explicit ledger and
an explicit adversarial pass.

1. **Keep a claims ledger** (a running list: claim, source, confidence, lens). Write
   to it; do not hold it in your head.
2. **Rotate the lenses deliberately.** Do one focused search batch *as* the academic
   lens, log its claims, then consciously switch stance to the technical lens, and so
   on. Before the contrarian pass, re-read your own draft answer and then attack it.
3. **Do the self-refutation pass explicitly.** For each load-bearing claim, write the
   claim, then the best sourced case against it, then the verdict. Seeing them on the
   page is what prevents the token-doubt shortcut.
4. **Do at least one narrowed second round** on the weakest claims and open gaps
   before synthesizing.

It is slower and a bit more prone to anchoring than true parallelism, so lean harder
on the written ledger and the explicit refutation step to compensate.

## Budget, depth, and loop-until-dry

- **Scale the fan-out to stakes.** Quick check: 5 lenses, one verify pass, one round.
  High-stakes: 8 lenses, 3-to-5-way refute on load-bearing claims, multiple rounds.
- **Loop until dry, not until a counter.** Keep running narrowed rounds while each new
  round surfaces materially new claims or resolves a contested one. Stop when a round
  adds nothing new (converged), when every load-bearing claim is verified or
  explicitly marked contested/unknown, or when you hit the search/compute budget.
- **If you stop on budget, disclose it.** Name what remains unverified so the reader
  knows the edge of the research, rather than inferring completeness.
- **Cap the obvious runaway.** Do not spawn unbounded agents or loop forever; a
  high-stakes research job converges in a handful of rounds. If it is not converging,
  the question is probably under-decomposed (go back to Step 1).
