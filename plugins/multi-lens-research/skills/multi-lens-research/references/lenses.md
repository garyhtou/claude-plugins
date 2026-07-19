# Lenses: the full catalog, prompts, and how to design new ones

A lens is an angle of attack: a source-type bias plus a question bias. Running
distinct lenses is what stops the research from converging on one first page. This
file is the menu and the prompt templates.

## Why lenses beat "more searches"

Any single query returns a **monoculture**: the top results are the pages that are
already the most linked, most SEO-optimized, and most quoted by each other. Five
agents running that same query return five copies of the same monoculture. Five
agents with **different source-type biases and different questions** return coverage
the monoculture never surfaces: the paper behind the blog post, the GitHub issue
where the feature broke, the competitor's teardown, the postmortem, the release note
that changed everything last month.

## The standard set (5)

Each lens below lists what it hunts, its go-to sources, and a prompt template. Give a
lens the **decomposed sub-questions** plus its angle, never the raw user prompt.

### 1. Academic / primary
- **Hunts:** the authoritative definition, the mechanism, the actual evidence.
- **Sources:** peer-reviewed papers, standards documents (RFCs, ISO, W3C), official
  specifications, primary-source docs, textbooks, government/regulatory filings.
- **Prompt template:**
  > You are the ACADEMIC / PRIMARY-SOURCE lens on: "{question}". Sub-questions:
  > {sub_questions}. Find the authoritative, primary sources: papers, standards,
  > official specs, original documentation. Prefer the source over anyone
  > describing the source. For each finding return the claim, the exact citation
  > (title, author/org, date, URL), and a confidence tag. Ignore blog summaries
  > unless they lead you to a primary source. Do not fabricate citations.

### 2. Technical / practitioner
- **Hunts:** how it really works, how it performs, where it breaks.
- **Sources:** source code and READMEs, engineering blogs, benchmarks, issue
  trackers, API docs, conference talks, practitioner forums.
- **Prompt template:**
  > You are the TECHNICAL / PRACTITIONER lens on: "{question}". Sub-questions:
  > {sub_questions}. Find how it actually works in practice: source code,
  > engineering write-ups, real benchmarks, bug trackers, docs. Prefer concrete
  > mechanisms and measured numbers over marketing. Note versions and dates. Return
  > claim, source, confidence. Flag anything that contradicts the "official" story.

### 3. Applied / case-study
- **Hunts:** who actually uses it, what happened, at what scale.
- **Sources:** case studies, postmortems, incident write-ups, production war
  stories, reviews, "we migrated from X to Y" posts, community threads.
- **Prompt template:**
  > You are the APPLIED / CASE-STUDY lens on: "{question}". Sub-questions:
  > {sub_questions}. Find real-world usage: who adopted it, at what scale, what
  > broke, what they wished they knew. Prefer named, dated, specific accounts over
  > generic claims. Return claim, source, confidence. Capture the context (scale,
  > constraints) so the lesson is transferable, not anecdotal.

### 4. News / recency
- **Hunts:** the current state and what changed lately (the thing stale sources miss).
- **Sources:** recent news, release notes, changelogs, dated announcements, status
  pages, recent social/forum discussion.
- **Prompt template:**
  > You are the NEWS / RECENCY lens on: "{question}". Sub-questions:
  > {sub_questions}. Find what is true NOW and what changed recently. Prioritize
  > dated sources from the last 6 to 18 months; explicitly flag when the widely
  > repeated answer is out of date. Return claim, source (with date), confidence.
  > A confident-sounding claim with no date is a red flag; note it.

### 5. Contrarian / skeptic (mandatory)
- **Hunts:** the strongest case that the emerging answer is wrong.
- **Sources:** criticism, "considered harmful" essays, failure reports, competitor
  and dissenting analyses, known limitations, retractions, lawsuits, security
  advisories.
- **Prompt template:**
  > You are the CONTRARIAN lens on: "{question}". Assume the popular/likely answer
  > is WRONG. Your job is to build the strongest evidence-based case against it:
  > find the critics, the failures, the limitations, the conflicts of interest, the
  > cases where it did not work. Do not manufacture doubt; find real, sourced
  > counter-evidence. Return claim, source, confidence. If after a genuine effort
  > you find little, say so explicitly (that itself is a finding).

## The deep set (add 3 for high-stakes or broad topics)

### 6. Historical / evolution
- **Hunts:** how it got here, what was tried and abandoned, why.
- **Sources:** origin stories, old versions, deprecation notices, retrospectives,
  "history of X" write-ups, archived pages (Wayback).
- **Angle:** understanding what failed before prevents re-recommending it.

### 7. Adjacent / analogy
- **Hunts:** how neighboring fields solved the same underlying problem.
- **Sources:** other disciplines, other industries, other ecosystems facing the
  analogous challenge.
- **Angle:** breaks tunnel vision; surfaces solutions the in-domain sources never
  mention.

### 8. Data / quantitative
- **Hunts:** the numbers: benchmarks, market size, adoption stats, measured
  tradeoffs, survey data.
- **Sources:** benchmark suites, datasets, surveys (State-of-X reports), pricing,
  quantitative studies.
- **Angle:** forces the qualitative narrative to meet the measured reality; numbers
  often contradict the vibe.

## Designing domain-specific lenses

Swap or add lenses to fit the domain. The pattern is always "a source-type bias plus
a question bias no other lens covers." Examples:

- **Legal / regulatory:** statutes, case law, regulator guidance, compliance filings.
- **Security:** CVEs, advisories, threat reports, red-team write-ups, audit findings.
- **Clinical / health:** trials, meta-analyses, guideline bodies, adverse-event
  databases. (Weight primary evidence heavily; treat single studies as low
  confidence.)
- **Financial / market:** filings, earnings, analyst reports, primary financial data.
- **Product / UX:** user reviews, support forums, churn/complaint threads, competitor
  teardowns.

Keep the total lens count matched to stakes (Step: "Scale to the stakes" in
SKILL.md). More lenses is more coverage and more cost; pick the angles that actually
change the answer for *this* question, and always keep the contrarian lens.
