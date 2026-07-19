---
name: rails-testing
description: Use when writing, running, reviewing, or fixing tests in a Ruby on Rails app (Rails-first, but also plain Ruby gems and POROs), with either RSpec or Minitest. Detects the project's framework, then applies Rails-specific mechanics and judgment: what to test at each layer (model, request, system), factory_bot vs fixtures, verified doubles and a disciplined mocking policy (Sandi Metz), request specs over controller specs, keeping system specs few, avoiding flaky tests (time, ordering, network, seeds), and catching performance regressions (N+1 queries, query counts). Composes with test-driven-development, which owns the red-green loop while this owns the Rails "how." Triggers on "write a spec/test," "model/request/system spec," "RSpec," "Minitest," "factory_bot," "my test is flaky," "test this Rails model / controller / job / mailer," "N+1 / too many queries / slow endpoint," or setting up a Rails test suite. Use it even when the user just says "add tests" to Rails code.
---

# Rails Testing (RSpec & Minitest)

Write Rails tests that (1) verify **behavior through the public interface**, not
implementation; (2) fail for exactly one clear reason; and (3) stay
**deterministic** so the suite never becomes noise. This skill is
**framework-aware**: it works with both RSpec (common in product apps, e.g.
large open-source Rails codebases) and Minitest + fixtures (the Rails-core
default). Treat Minitest as a first-class citizen, never an afterthought.

The single most common way an agent writes bad Rails tests is **over-mocking and
asserting on internals** so the test passes while the real thing is broken and
breaks on every refactor. The judgment sections below exist to prevent that.

## How this composes with other skills

- **`test-driven-development`** owns the *when and the order*: write the failing
  test first, **watch it fail for the right reason**, write minimal code, watch
  it pass. This skill owns the *Rails how*: which spec type, what to assert, what
  to mock, how to build data, how to run it. When TDD is active, follow its
  red-green-refactor loop and use this skill for the mechanics of each step. Do
  not restate TDD's rules; defer to it.
- **`subagent-driven-development`** / delegated implementers: an implementer
  writing Rails code should load this skill so its tests follow these mechanics.
- If neither is active and the user asks for tests on existing code, still write
  behavior-first tests here (adding characterization tests to legacy code is
  legitimate; note you did not watch them fail against missing code).

## Step 0: Detect the framework and match local conventions (always first)

Never assume RSpec. Detect, then **read a neighboring test file** and copy its
structure, helpers, and naming. Matching the codebase beats any default here.

**RSpec** if: a `.rspec` file exists, a `spec/` directory exists, or `rspec-rails`
is in the Gemfile. Specs live in `spec/**/*_spec.rb`; run with `bundle exec rspec`.

**Minitest** if: `test/test_helper.rb` exists and there is no `spec/` / `rspec-rails`.
Tests live in `test/**/*_test.rb`; run with `bin/rails test`.

Quick check:

```bash
ls .rspec spec 2>/dev/null; ls test/test_helper.rb 2>/dev/null
grep -E "rspec-rails|minitest" Gemfile Gemfile.lock 2>/dev/null | head
```

If both exist, follow the directory the target code is already tested in; if
genuinely new, prefer the framework the rest of the suite uses. If the project
has neither yet, ask the user which they want before scaffolding.

Also detect the support cast so you use what's already there: `factory_bot` (or
fixtures), `shoulda-matchers`, `webmock`/`vcr`, `simplecov`, the JS driver
(`selenium`, `cuprite`), and any `spec/support` / `test_helper` sign-in helpers.

## Off Rails: plain Ruby gems and POROs

All of this skill's **judgment** (what to test, the mocking policy, FIRST) applies
unchanged to non-Rails Ruby. Only the harness differs, and there is no Rails to
scaffold it, so wire it up yourself and skip the Rails-only sections
(request/system specs, factory_bot-vs-fixtures for the DB, ActiveSupport time
helpers unless you add the gem):

- **RSpec:** there is no `rails_helper`. Require your library in
  `spec/spec_helper.rb`, and put `lib/` on the load path (`.rspec` with
  `--require spec_helper` plus `-I lib`, or a `require_relative`). No DB, so no
  `use_transactional_fixtures`.
- **Minitest:** there is no `bin/rails test`. Require `minitest/autorun` and run
  via `ruby -Ilib -Itest test/foo_test.rb` or a `Rake::TestTask` (`rake test`),
  prefixed with `bundle exec` when the project uses a Gemfile/local bundle so the
  bundled Minitest loads, not a system one. Plain Minitest names tests
  `def test_...`; the `test "name" do` macro is
  **ActiveSupport sugar, unavailable without Rails** (use `def test_`, or define
  the macro yourself).

## The core judgment: what to test (Sandi Metz's rules)

Classify each message the object under test participates in by **direction**
(incoming from outside / sent to self / outgoing to a collaborator) and **type**
(query returns a value with no side effect; command causes a side effect and the
return is ignored). Then:

| Message origin | Query (returns a value) | Command (has a side effect) |
| --- | --- | --- |
| **Incoming** (the public API you are testing) | **Assert the returned value** | **Assert the direct, public side effect** |
| **Sent to self** (private methods) | **Ignore** (do not test directly) | **Ignore** (do not test directly) |
| **Outgoing** (sent to a collaborator) | **Ignore** (no assertion, no mock) | **Mock it: assert the message is sent** (not its effect) |

**One public method can be both a query and a command.** A method like `check!`
that fires alerts (side effect) *and* returns the list of what breached (value) is
an incoming command **and** an incoming query at once: assert **both** the return
value and the direct side effect. The table classifies *messages*, not methods, so
a method that sends more than one kind of message hits more than one cell. Each
cell also has a negative counterpart worth covering: an outgoing command should be
asserted **sent when it should fire and not sent when it shouldn't** (the no-breach
path sends no alert).

The whole policy in one breath: **assert results of incoming queries; assert
side effects of incoming commands; mock only outgoing commands; ignore outgoing
queries and everything private.** Private methods and outgoing queries get
exercised for free through the public API. Testing them couples the test to
implementation and blocks refactoring. (Sandi Metz, "The Magic Tricks of
Testing"; see `references/philosophy.md`.)

**"Ignore" means do not *assert* on it, not "never touch it."** You may still
**stub an outgoing query to feed the object its input** (stubbing as a means):
e.g. `allow(repo).to receive(:pending).and_return(orders)` so the test has data
to act on. The discipline is that you never *assert* that query was called and
never mock it as the point of the test. Only outgoing **commands** earn an
interaction assertion (`expect(...).to have_received`).

## Mocking policy: classicist by default

Prefer **real objects and real (test-DB) records**; Rails is DB-centric and the
test DB is fast enough. Reserve test doubles for the one cell above (outgoing
commands) and for **true external boundaries**: third-party HTTP, payment
gateways, mail *delivery*, the clock, SMS. Everything you own, use for real.

**A class you own can still be a boundary.** "Use real objects you own" does not
mean instantiate a wrapper/adapter/client whose real implementation talks to a
backend (raises `NotImplementedError`, opens a socket, charges a card). Judge by
what the object *does* at its edge, not who wrote it: an owned `SmsGateway` or
`MetricsSource` that fronts an external system is a boundary, so double it (with a
verified double, since the class exists). Reserve "use it for real" for owned
objects that are pure logic or hit only the test DB.

- **RSpec: use verified doubles whenever the collaborator has a real class**
  (`instance_double(Klass)`, `class_double`, `object_double`) so a renamed or
  missing method fails the test instead of passing silently. A bare `double` /
  `spy` verifies nothing, but it is the **correct fallback (not a lapse) when the
  collaborator is a pure duck type with no backing class**: an injected dependency
  defined only by the messages it receives, or a class you have not written yet.
  A verified double is genuinely impossible there, so reach for the bare double,
  name it, and move on. Set `verify_partial_doubles = true`. Prefer **spies**
  (`have_received`) so tests read arrange-act-assert. Avoid
  `allow_any_instance_of` (you can't name the instance; inject the dependency).
- **Minitest: `minitest/mock` is minimal** (block-scoped `stub`, method must
  already exist, no arg matching). Add **mocha** (`require "mocha/minitest"`,
  auto-verifies at teardown) when you need matchers, sequences, or `any_instance`.
- **Do not mock the object under test**, and do not mock a model inside its own
  test. If you must mock everything to get a test to pass, the design is too
  coupled: inject the collaborator instead.

Over-mocking is the top smell to avoid. A test that only asserts "these methods
were called" re-describes the implementation and gives false confidence.

## What to test at each layer

Weight the suite like a pyramid with a fat integration middle (the Rails reading
of the "testing trophy"):

- **Model / PORO / service-object unit tests (most numerous):** validations you
  *defined*, scopes (assert included **and** excluded records), enums/state
  transitions, and business logic. Fast; no browser.
- **Request specs / integration tests (the center of gravity):** exercise router
  + middleware + controller + response through a real request. This is where
  controller and API behavior belongs. **Prefer request specs over controller
  specs** (controller specs are discouraged since RSpec 3.5); the Minitest
  equivalent is `ActionDispatch::IntegrationTest`. Assert status + body + the
  relevant side effect (a record created, a job enqueued, a mail sent).
- **System / feature specs (fewest):** full browser via Capybara, for genuinely
  JS-dependent, critical happy paths only. They are slow and flaky, so keep them
  few. Turbo Stream responses can often be checked at the **request** layer
  (assert the `text/vnd.turbo-stream.html` body) instead of a system test.

**Do not test the framework.** Rails already tests that `validates_presence_of`,
`enum`, and `belongs_to` generate their methods. Test *your* rules and *your*
usage. **Do not test private methods** directly. **Do not add controller/view
specs** for logic that a request or system spec already covers.

## Writing a good test

Aim for **FIRST** (Fast, Isolated, Repeatable, Self-validating, Timely) plus two
that matter most for machine-written tests: **one reason to fail** (one behavior
per example) and **resistance to refactoring** (only breaks when behavior
changes). Concretely:

- Name the behavior, not the method's mechanics. RSpec: `describe "#total"` /
  `context "when discounted"` / `it "subtracts the discount"`. Every `context`
  states a condition and ideally has a negative counterpart. Minitest:
  `test "total subtracts the discount when discounted"`.
- Keep setup **local and visible**. Specify only the attributes the test is
  about (`create(:user, :admin)` reads as "an admin"); let the factory fill the
  rest. Hidden, far-away setup is the "mystery guest" smell.
- For expensive setup (a request, a browser step), it is fine to make several
  related assertions in one example: wrap them in RSpec `:aggregate_failures` so
  you see every failure, not just the first. System specs legitimately assert
  multiple UI facts.

## Test data: build the cheapest thing that works

- **factory_bot ladder (default to the cheapest):** `build_stubbed` (no DB, fake
  id, raises if you try to save) > `build` (no save, but note it still *creates*
  its associations) > `create` (persists). Reach for `create` only when the code
  must round-trip the DB (a query, a scope, a DB constraint, a callback that
  hits the DB). Keep the base factory **minimal and valid**; push variation into
  **traits**; use **sequences** for unique fields.
- **Minitest + fixtures (Rails default):** reference records by **label**
  (`users(:david)`, `author: david`), never by hardcoded id. Fixtures load once
  and are fast; that speed is why Rails core prefers them.
- Either way: no `db/seeds.rb` data in tests, and seed randomness (see below).

Details, traits, linting, and the fixtures-vs-factories tradeoff:
`references/test-data.md`.

## Running tests (both frameworks)

Iterate on the **narrowest scope** first (one example), widen to the file, then
the suite. Reproduce order-dependent failures with the printed seed.

**RSpec**
```bash
bundle exec rspec spec/models/order_spec.rb          # one file
bundle exec rspec spec/models/order_spec.rb:42       # one example at a line
bundle exec rspec --fail-fast                         # stop at first failure
bundle exec rspec --seed 12345                        # reproduce an ordering
bundle exec rspec --bisect --seed 12345               # find the minimal leaking pair
bundle exec rspec --profile                           # surface the slowest examples
```

**Minitest**
```bash
bin/rails test test/models/order_test.rb             # one file
bin/rails test test/models/order_test.rb:42          # one test at a line
bin/rails test -f                                     # fail fast
bin/rails test --seed 12345                           # reproduce an ordering
bin/rails test -n test_the_total                      # filter by test name
bin/rails test:system      # system tests are NOT in `bin/rails test`; run separately
```

Always run tests in **random order** (both frameworks do by default) so
order-dependence surfaces. Rails' built-in `parallelize` (Minitest) and
`parallel_tests` (either) give a per-process DB; keep tests isolated so parallel
workers don't collide.

## When a test is flaky

Flakiness is a virulent infection: one ignored red build teaches the team to
ignore all of them. Fix, don't retry-to-green. The usual root causes and the
one-line fixes:

- **Time** -> freeze it (`travel_to` / `freeze_time`), and use
  `Time.current` / `Time.zone`, never `Time.now`.
- **Ordering** -> reproduce with `--seed`, isolate with `--bisect`; the random
  order is the messenger, not the bug. Never assert on DB order without `ORDER BY`.
- **Randomness** -> seed Ruby's PRNG **and Faker separately**
  (`Faker::Config.random = Random.new(seed)`); Faker ignores the global seed.
- **Network** -> block it (`WebMock.disable_net_connect!(allow_localhost: true)`)
  and stub; record with VCR (filtering secrets) for replay.
- **Async / JS** -> never `sleep`; rely on Capybara's auto-waiting matchers.
- **Leaked global state** -> reset caches, `ENV`, `Current`, `Time.zone`,
  class vars between tests; lean on transactional tests for the DB.

Full playbook (detection, checklist, HTTP/jobs/mailers, coverage, CI, PII in
cassettes): `references/reliability.md`.

## Performance regression testing

Tests can prevent code from silently becoming non-performant, but only if they
assert the right thing. **Assert deterministic counts (SQL queries, allocations),
never wall-clock time.** Query count is a pure function of code + input, so it is a
true regression signal on any machine; wall-clock time on shared CI runners varies
>30% run to run, so a time threshold is either flaky or useless. Keep time-based
benchmarking (`benchmark-ips`, `rspec-benchmark` time matchers, `derailed_benchmarks`)
out of CI, in a separate isolated suite.

The #1 target is the **N+1 query**, and the robust test asserts the query count
**does not grow with the number of records**, not a magic number:

- **Brittle:** `expect { get "/posts" }.to make_database_queries(count: 3)`. Any
  unrelated added query (a feature flag, a counter cache) flips the number, so it
  gets "fixed" by bumping it. That tests an incidental, not behavior.
- **Robust:** run at two dataset sizes and assert constancy. `n_plus_one_control`:
  `expect { get "/posts" }.to perform_constant_number_of_queries` (with a
  `populate { |n| create_list(:post, n) }`). A fixed baseline of boring queries
  cancels out; only real scaling fails. A fixed N+1 then becomes a permanent
  regression guard.

**Where to put them:** targeted, at the **request/integration layer** (index
actions, serializers, dashboards, any endpoint where you already fixed an N+1), not
as a blanket assertion in every model spec (that is noise and couples the suite to
query implementation).

**Two complementary mechanisms:**
- **Targeted count assertions** on hot endpoints: `n_plus_one_control` for scaling;
  `db-query-matchers` (`make_database_queries(count:, matching:)`, and `.not_to
  make_database_queries` to prove a cache path is free) for RSpec; Rails 7.2+
  built-in `assert_queries_count` / `assert_no_queries` / `assert_queries_match`
  for Minitest (no gem). A raising detector (`prosopite`, preferred over `bullet`
  for suite use because it has fewer false positives and catches post-`create_list`
  N+1) can gate the whole suite via `Prosopite.raise = true`.
- **`strict_loading` as a broad tripwire:** set
  `config.active_record.strict_loading_by_default = true` so any lazy-load of a
  not-preloaded association raises. Run it **raising in development and test** (mode
  `:all`, not `:n_plus_one_only`, which gives false confidence); optionally `:log`
  in production. Every request/system spec then detects N+1 for free. It only sees
  ActiveRecord association lazy-loading (not raw SQL, `.pluck`/`.exists?`-in-a-loop,
  or N+1-after-`create_list`), so pair it with `prosopite` for those and with
  targeted count assertions as the named guarantees. Adopt gradually on an existing
  app; expect friction from serializers, GraphQL, admin frameworks, and callbacks.

Query-count loggers (dev widgets that print a query count) are not test tools;
reach for a real matcher: `db-query-matchers` for RSpec, the Rails 7.2 built-ins
for Minitest. Also useful: `strong_migrations` fails a migration that would lock a
big table in production. Full tool map, APIs, flake-proofing, and the
`strict_loading` posture: `references/performance.md`.

## Review mode

When asked to review or critique tests (not write them), read
`references/reliability.md` (section 9, the anti-pattern catalog) and hunt:
over-mocking / testing implementation,
mystery guest, fragile/overspecified tests, non-deterministic tests, assertion
roulette, testing private methods or framework behavior, and controller/view
specs that duplicate request/system coverage. Report each finding with the file,
the smell, and the concrete fix.

## Reference files (load as needed)

- `references/rspec.md`: RSpec + rspec-rails: structure, `describe`/`context`/
  `let`/`subject`, matchers, verified doubles, factory_bot, shoulda-matchers,
  request & system specs, config.
- `references/minitest.md`: Minitest + Rails: `assert_*` (argument order!),
  fixtures, `minitest/mock` + mocha, integration & system tests, parallelization,
  Rails-core idioms.
- `references/test-data.md`: factory_bot deep dive (strategies, traits, linting),
  fixtures, Faker & determinism, the mystery-guest smell.
- `references/philosophy.md`: the "why": Sandi Metz's full talk, Ian Cooper
  (test through the port), Fowler (classicist vs mockist), DHH (test-induced
  design damage; Minitest + fixtures), FIRST, the testing trophy. Cited.
- `references/reliability.md`: flaky tests, time, HTTP (WebMock/VCR), jobs,
  mailers, ActionCable, coverage (SimpleCov), CI/parallel, security/PII.
- `references/performance.md`: performance-regression testing: assert query counts
  not wall-clock time, the N+1 scale-invariance test, the tool map
  (n_plus_one_control, db-query-matchers, Rails 7.2 query assertions, prosopite/
  bullet), strict_loading as a tripwire, strong_migrations, flake-proofing. Cited.

## Prose style

Match the surrounding code's style exactly. Avoid em dashes in any prose you
generate (comments, commit messages, PR text, test descriptions); recast with
commas, periods, colons, parentheses, or "to" for ranges. Em dashes read as an
AI tell.
