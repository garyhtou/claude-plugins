# Testing philosophy: the "why" behind the rules

The mechanics in the other references serve these ideas. When a mechanical choice
is unclear, come back here. The through-line: **test observable behavior through
the public interface, so tests survive refactoring and actually catch regressions.**

## Contents
1. Sandi Metz's testing rules (the mocking/assertion policy)
2. Test behavior, not implementation (Cooper, Beck)
3. Classicist vs mockist, and the Rails default (Fowler)
4. DHH: test-induced design damage, and Minitest + fixtures
5. What makes a good test (FIRST + two more)
6. The pyramid, the trophy, and where Rails lands

---

## 1. Sandi Metz's testing rules

From "The Magic Tricks of Testing" (RailsConf 2013), the single most useful
artifact for deciding *what to assert and what to mock*. Classify each message by
**direction** and **type**:

- **Direction:** incoming (public API, received from outside) / sent-to-self
  (private) / outgoing (sent to a collaborator).
- **Type:** query (returns a value, no side effect) / command (causes a side
  effect, return ignored).

| Message origin | Query (returns a value) | Command (side effect) |
| --- | --- | --- |
| **Incoming** | **Assert the returned value** | **Assert the direct public side effect** |
| **Sent to self** (private) | Ignore (do not test) | Ignore (do not test) |
| **Outgoing** | Ignore (no assertion, no mock) | **Expect to send** (mock it) |

The one-line rules:

- **Incoming query** -> assert what it returns.
- **Incoming command** -> assert the *direct* public side effect (not incidental ones).
- **Outgoing query** -> do nothing: no assertion, no mock. It is invisible to the
  rest of the app and will be covered as an *incoming* message of the other object.
  Testing it creates redundant, brittle tests.
- **Outgoing command** -> the **only** legitimate mock: assert the message *is
  sent*, not its side effect (the collaborator's own test owns that).
- **Sent-to-self / private** -> never test directly; exercised through the public API.

Overarching: **test everything once**, and never assert the same thing from two
places. This table is why the SKILL says "classicist by default, mock only
outgoing commands." It is precisely where LLM-written tests fail: over-mocking,
asserting on internals, and testing private methods.

Sources: https://gist.github.com/Integralist/7944948,
https://speakerdeck.com/spreeconf/the-magic-tricks-of-testing-sandi-metz.

## 2. Test behavior, not implementation

**Ian Cooper, "TDD, Where Did It All Go Wrong"** (https://www.infoq.com/presentations/tdd-original/):
the industry mistake was writing "a unit test for every method and class," which
bakes implementation details into tests, making them fragile under refactoring and
heavy with mocks. The trigger for a new test should be **a new behavior, not a new
class or method.** Test **through the public API** (the "port"), not internals:
"you cannot refactor if you have implementation details in your tests, because
refactoring by definition changes implementation while preserving the public
interface." Kent Beck's original TDD unit was the behavior, not the method.

For Rails, "the port" usually means: a model's public methods, the request/response
cycle (request specs / integration tests), and a job's or mailer's public behavior,
**not** controller internals, private methods, or ActiveRecord internals.

Corollary: **don't test the framework.** Rails already verifies that
`validates_presence_of`, `enum`, `belongs_to`, and scopes generate their methods.
Test *your* rules (invalid without X, valid with X, the custom validator, the
conditional validation) and *your* usage, focusing on behavior.

## 3. Classicist vs mockist, and the Rails default

**Fowler, "Mocks Aren't Stubs"** (https://martinfowler.com/articles/mocksArentStubs.html)
draws two axes: *state* vs *behavior* verification, and *classical* vs *mockist* TDD.

- **Classicist (Detroit school):** use real objects wherever possible; verify
  state; mock only what is awkward (network, external services).
- **Mockist (London school):** mock all collaborators; verify interactions.

Where the industry landed (Thoughtworks, "Mockists Are Dead. Long Live
Classicists."): over-mocking couples tests to structure and produces the fragile,
refactor-hostile suite Cooper warns about.

**The Rails default this skill adopts: classicist.** Use real objects and
factory-built records; hit the test DB (it is fast enough, and Rails is
DB-centric). Reserve mocks/stubs for **outgoing commands to true boundaries**:
third-party HTTP, payment gateways, mail *delivery*, the clock, SMS. That is
exactly Sandi Metz's "outgoing command -> expect to send" cell, and nothing more.

## 4. DHH: test-induced design damage, and Minitest + fixtures

**DHH, "TDD is Dead. Long Live Testing."** and **"Test-Induced Design Damage"**
(https://dhh.dk/2014/tdd-is-dead-long-live-testing.html,
https://dhh.dk/2014/test-induced-design-damage.html): dogmatic
unit-test-everything-first plus "tests must be fast at all costs" produces needless
indirection, "a dense jungle of service objects and command patterns," created
only to avoid touching the DB/IO. His prescriptions: **don't unit-test controllers,
integration-test them**; value system/integration tests; embrace **Minitest +
fixtures + a real DB** for speed-with-fidelity.

The Beck/Fowler/DHH "Is TDD Dead?" series (https://martinfowler.com/articles/is-tdd-dead/)
is the synthesis: TDD is a tool, not a religion; test at the level that gives
confidence. The practical consequence for this skill: **Minitest + fixtures is a
first-class, legitimate position, never an afterthought**, and the suite's center
of gravity is integration (request) tests, not a mock-heavy unit layer.

## 5. What makes a good test

**FIRST** (Pragmatic Programmers): **F**ast, **I**solated/independent,
**R**epeatable (deterministic: no dependence on time, order, or network),
**S**elf-validating (clear pass/fail, no human inspection), **T**imely (written
with the code). Add the two FIRST omits that matter most for machine-written tests:

- **One reason to fail**: one behavior per example, so a red test names exactly
  what broke. (Carve-out: system/feature specs legitimately assert several UI
  facts per scenario; group them, e.g. RSpec `:aggregate_failures`.)
- **Resistance to refactoring**: a test should break **only when behavior
  changes**, never on a pure rename/extract. This is the operational test of "am I
  testing behavior or implementation?": if a refactor that preserves behavior
  reddens the test, the test was bound to implementation.

## 6. The pyramid, the trophy, and where Rails lands

- The **Test Pyramid** (Fowler): many fast unit tests, fewer integration, fewest
  end-to-end. https://martinfowler.com/bliki/TestPyramid.html
- The **Testing Trophy** (Kent C. Dodds): modern integration tooling is fast and
  reliable enough that **integration should be the thickest layer**; guiding
  principle: "the more your tests resemble the way your software is used, the more
  confidence they can give you." https://kentcdodds.com/blog/write-tests

For Rails these converge on the same shape: a broad base of **model / PORO /
service-object unit tests**, a fat middle of **request specs / integration tests**
(the recommended home for controller and API behavior; controller specs have been
discouraged since RSpec 3.5), and a thin cap of **system specs** for critical
JS-dependent journeys (slow and flaky, so few). Static analysis (RuboCop,
Brakeman, and any type checker) is the free layer underneath.

The anti-pattern catalog and review-mode checklist live in `reliability.md`
(section 9) and the SKILL's review-mode section; the common Rails smells are
over-mocking, mystery guest, fragile/overspecified tests, non-determinism,
assertion roulette, testing private methods or framework behavior, and
controller/view specs duplicating request/system coverage.

Sources: https://martinfowler.com/articles/is-tdd-dead/,
https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications,
https://www.thoughtworks.com/insights/blog/mockists-are-dead-long-live-classicists,
http://xunitpatterns.com/.
