# Reliability: flaky tests, boundaries, coverage, CI, and review

Keeping the suite deterministic and honest, and the anti-pattern catalog for
review mode. Applies to both frameworks.

## Contents
1. Flaky tests: root causes, detection, prevention
2. Time and timezones
3. Database isolation (and why DatabaseCleaner is usually unneeded now)
4. External HTTP: WebMock and VCR
5. Background jobs, mailers, ActionCable
6. Coverage (SimpleCov)
7. CI and speed
8. Security / PII in tests
9. Anti-pattern catalog (review mode)

---

## 1. Flaky tests

A flaky test passes sometimes and fails sometimes with no code change. Fowler
calls them a "virulent infection": one ignored red build teaches the team to
ignore all of them, destroying the suite's value
(https://martinfowler.com/articles/nonDeterminism.html). **Fix them; do not
retry-to-green.** Quarantine a newly-flaky test out of the main gate if you must,
file it, and fix within a bounded window.

**Root causes and the one-line fix:**

1. **Leaked global state / no isolation**: shared DB rows, class vars,
   singletons, memoized globals, `ENV`, `Current`, `Time.zone` left mutated. Fix:
   reset between tests; lean on transactional tests for the DB. Fowler's trick:
   prefer rebuilding state before each test over cleaning up after.
2. **Order dependence**: test A leaves state test B relies on; passes alone,
   fails in sequence. Run random order (default) to surface it. The random order
   is the messenger, not the bug.
3. **Time**: real clock, boundary instants (midnight, month/year, DST). Freeze
   time; see §2.
4. **Async / JS timing**: never bare `sleep`; rely on Capybara auto-waiting
   matchers (`have_content`, `have_selector`) that poll up to
   `Capybara.default_max_wait_time`. Never assert on state before the async settles.
5. **Remote services / network**: stub with WebMock/VCR (§4). No test hits the
   real network.
6. **Random data**: Faker/unseeded randomness producing an occasional invalid or
   colliding value. Seed Ruby's PRNG **and Faker separately** (Faker ignores the
   global seed); prefer sequences over `Faker.unique`. See test-data.md.
7. **DB order without `ORDER BY`**: `Model.all.first` relies on arbitrary
   database order. Always add explicit ordering in both code and assertion; assert
   unordered collections with `contain_exactly` / `match_array`, not `eq`.
8. **Resource leaks**: unclosed connections/files. Fowler's trick: size the pool
   to 1 in tests so a leak fails immediately in the responsible test.

**Detection and reproduction:**

- Reproduce with the printed seed: `rspec --seed N` / `bin/rails test --seed N`
  reruns the exact order.
- `rspec --bisect --seed N` runs progressively smaller subsets to find the
  **minimal set of specs that, in that order, reproduce the failure**, pinpointing
  the coupled pair. Workflow: reproduce with `--seed`, then isolate with `--bisect`.
- Rerun a suspect test many times (or the suite N times) to measure the flake rate
  before and after a fix.

**Prevention checklist:**

- [ ] Random order, committed to. Fix, do not disable, order-dependent failures.
- [ ] Freeze/travel time for any time-sensitive assertion; use `Time.current` /
      `Time.zone`, never `Time.now`.
- [ ] Seed randomness (Ruby PRNG and `Faker::Config.random`); sequences over `Faker.unique`.
- [ ] Block the network (`WebMock.disable_net_connect!`); stub all external HTTP.
- [ ] No bare `sleep`; Capybara auto-waiting only.
- [ ] Always `ORDER BY` when asserting on order; never trust default DB order.
- [ ] Reset global state (class vars, `ENV`, caches, `Current`, `Time.zone`).
- [ ] Isolate the DB (transactional tests; verify no cross-test leakage).
- [ ] One reason to fail per test; no hidden dependence on prior tests.
- [ ] In parallel runs, share no resources (files, ports, external fixtures) across workers.

## 2. Time and timezones

Prefer Rails' `ActiveSupport::Testing::TimeHelpers` over the Timecop gem:

```ruby
travel_to Time.zone.local(2026, 7, 18, 9, 0, 0) do
  # Time.current / Date.today / Time.zone.now are frozen at that instant
end
freeze_time { ... }   # freeze at now
travel 1.day          # jump forward (block form auto-undoes; else travel_back)
```

- TimeHelpers **always freezes** on `travel_to` (Timecop's `travel` keeps ticking).
  It does **not** support nested travels; it raises rather than returning wrong
  times. Prefer block forms so the stub always tears down.
- Use `Time.zone.now` / `Time.current` / `Time.zone.local`, **not** `Time.now` /
  `Time.new` (which use the system zone and differ between laptop and CI).
- In app code, inject the clock (`Time.current`, or a `clock:` param) so it is
  substitutable. Test the timezone edge (a user in `America/Los_Angeles` at 11pm
  is "tomorrow" in UTC).

## 3. Database isolation

Rails wraps each test in a transaction rolled back on completion
(`use_transactional_tests` / `use_transactional_fixtures`, default true). This is
the fastest isolation (the skipped commit is what costs) and makes tests
independent. It only works when the test code and the app-under-test **share one
DB connection**.

**DatabaseCleaner is usually unnecessary now.** Rails 5.1+ system tests make the
test thread and the app server thread share a connection, so JS browser tests can
be wrapped in transactions again. Modern recommendation: drop the DatabaseCleaner
gem, set `use_transactional_fixtures = true`. Keep DatabaseCleaner only for true
edge cases (real multi-connection setups, non-Rails-managed connections, legacy
stacks). Its strategies for reference: `:transaction` (fast, default),
`:truncation` (works across connections, slow), `:deletion`.

## 4. External HTTP: WebMock and VCR

**Block the network** so nothing escapes unnoticed:

```ruby
require "webmock/rspec"      # or "webmock/minitest"
WebMock.disable_net_connect!(allow_localhost: true)   # localhost for Capybara

stub_request(:get, "https://api.example.com/rates")
  .to_return(status: 200, body: { usd: 1.0 }.to_json,
             headers: { "Content-Type" => "application/json" })
```

To **assert the outgoing request happened** (an HTTP call is an outgoing command,
so this is the "assert the message is sent" check for a boundary you can't spy on
directly), use `have_requested` / `assert_requested`, matching the payload when it
matters:

```ruby
expect(WebMock).to have_requested(:post, "https://crm.example.com/contacts")
  .with(body: { email: "a@b.com" }.to_json,
        headers: { "Content-Type" => "application/json" }).once
# Minitest: assert_requested(:post, url, body: ..., times: 1)
```

Assert **absence** with `not_to have_requested` (the error path made no call). With
`disable_net_connect!` on, an un-stubbed request already raises, so you rarely need
to assert a call did *not* fire unless a specific branch must skip it.

**VCR** records real HTTP interactions to YAML "cassettes" and replays them:

```ruby
VCR.configure do |c|
  c.cassette_library_dir = "spec/cassettes"
  c.hook_into :webmock
  c.ignore_localhost = true
  c.configure_rspec_metadata!                     # one cassette per example, named automatically
  c.filter_sensitive_data("<API_KEY>") { ENV["API_KEY"] }                 # MANDATORY, see §8
  c.filter_sensitive_data("<AUTH>") { |i| i.request.headers["Authorization"]&.first }
end
```

- Match on `[:method, :uri, :body]` when the body matters (POSTs); default is
  method + URI.
- Keep cassettes small (one per test) and **commit them only after filtering
  secrets**.
- In CI, use record mode `:none` so a missing cassette fails loudly instead of
  hitting the network; record `:once` / `:new_episodes` locally.
- Re-record periodically so cassettes don't silently drift from the real API;
  pair with an occasional real contract test.

## 5. Background jobs, mailers, ActionCable

- **Confirm the test env actually uses the `:test` adapters first.** A normal
  `rails new` sets `config.active_job.queue_adapter = :test` and
  `config.action_mailer.delivery_method = :test` in `config/environments/test.rb`,
  but a `--minimal` app disables the ActiveJob/ActionMailer railties and strips
  that config, so `deliver_later` / `perform_enqueued_jobs` will try real SMTP
  (`Errno::ECONNREFUSED ... port 25`) until you re-enable the railties and set both
  test modes yourself. If job/mail assertions behave strangely, check this before
  anything else.
- **Active Job** (`:test` adapter enqueues but does not run;
  `ActiveJob::TestHelper`): assert **enqueue** in unit/request tests
  (`assert_enqueued_with(job:, args:)` / RSpec `have_enqueued_job`); run the job's
  own logic in a dedicated job test, or `perform_enqueued_jobs { ... }` for the
  end-to-end effect.
- **Sidekiq** (if used directly rather than via ActiveJob): `fake!` (default,
  jobs pushed to `Worker.jobs`), `inline!` (run synchronously), `disable!` (real
  Redis). If you use ActiveJob over Sidekiq, keep the queue adapter `:test` in the
  test env so ActiveJob's assertions work.
- **Action Mailer** (`:test` delivery): `deliver_now` populates
  `ActionMailer::Base.deliveries`; `deliver_later` enqueues a job (assert with
  `assert_enqueued_email_with` / `have_enqueued_mail`, or wrap in
  `perform_enqueued_jobs`). Assert on recipients/subject/body.
- **ActionCable** (`ActionCable::TestHelper`, channel/connection test cases):
  `subscribe`, then `assert_has_stream`, `assert_broadcasts(stream, n)`,
  `assert_broadcast_on`.

## 6. Coverage (SimpleCov)

```ruby
require "simplecov"
SimpleCov.start "rails" do
  enable_coverage :branch                 # branch, not just line
  minimum_coverage line: 90, branch: 80
  maximum_coverage_drop 1                  # fail if a PR erodes coverage
end
```

- Coverage measures **execution, not correctness**: a line ran, not that the
  behavior was worth checking. High coverage is not good tests; low coverage is a
  real warning.
- Enable **branch coverage**: line coverage never tells you whether both arms of a
  conditional ran.
- Treat thresholds as **guardrails, not goals**. Chasing 100% breeds
  assertion-free tests that execute code without checking behavior. Prefer
  `maximum_coverage_drop` (stop silent erosion) over mandating an absolute ceiling.

## 7. CI and speed

- **Parallelize:** Rails' built-in `parallelize` (per-process DB) or the
  `parallel_tests` gem. Split by **recorded per-test runtime**, not file count, so
  nodes finish together. Parallel tests fail if workers share resources (files,
  ports, external services), so keep state per-worker.
- **Run only affected tests** locally / in PRs for a fast loop; keep the full
  suite on the merge gate.
- **Retries hide flakiness.** Blind `rspec-retry` makes a flaky suite green
  without fixing the flake and lets flakes accumulate. If you retry, **track and
  report** every retried test and treat it as a bug; quarantine flakes into a
  separate visible job rather than silently retrying in the main gate.
- **Fail-fast while iterating**, full suite on the gate. **Profile** with
  `rspec --profile` / Minitest reporters; converting one slow `create`-heavy
  system test into a request or `build_stubbed` unit test is often the biggest win.

## 8. Security / PII in tests

- **Never commit real secrets in VCR cassettes.** Recording captures live
  `Authorization` headers, API keys, tokens, and PII into YAML that then lands in
  git. Use `filter_sensitive_data` to replace them **before** the cassette is
  written, from both env vars and live request/response headers; scrub PII in
  bodies (`c.before_record { |i| i.response.body.gsub!(/\d{3}-\d{2}-\d{4}/, "<SSN>") }`).
- **Audit cassettes before committing**: grep for tokens, emails, SSNs, cookies.
  A leaked cassette is a leaked credential; rotate if exposed.
- Do not use production data as fixtures/seeds unless anonymized. Filter secrets
  from logs and CI artifacts too (coverage reports, failure screenshots can
  capture PII on-screen).

## 9. Anti-pattern catalog (review mode)

When reviewing tests, hunt these and report each with file, smell, and fix:

- **Testing implementation, not behavior / over-mocking**: the test re-asserts
  internal calls; it passes when the real integration is broken and breaks on
  every refactor. Fix: use real objects; mock only outgoing commands to boundaries
  (philosophy.md). Operational check: does a behavior-preserving refactor redden it?
- **Passes for the wrong reason**: the arrange block never establishes the
  precondition the test name claims, so the example goes green on an unrelated
  error or on state that was already true. A `"declined card"` example that stubs
  no decline is passing on a `NoMethodError` from a nil gateway, which means the
  decline path has zero coverage while looking covered. This hides behind an
  otherwise-clean test, so it is the first thing to check, before any named smell.
  Fix: arrange the failure explicitly, then constrain the assertion to it.
- **Name/behavior mismatch**: the description promises something the body does
  not do (`"works end to end"` on a model spec, `"blows up on a dead card"` with
  no card). Strong review signal: it usually means the author knew what they
  meant to test and did not get there. Fix: make the body match the name, or
  rename to what it actually tests, whichever is the real intent.
- **Mystery guest**: the test depends on data defined far away (a distant `let`,
  a broad fixture, a `before(:all)`). Fix: make the essential data local and visible.
- **`before(:all)` records that escape the transaction**: distinct from, and more
  serious than, the mystery-guest smell above. Transactional tests wrap each
  *example*, not `before(:all)`, so rows created there are committed: they leak
  into every spec that runs afterward, break under parallel workers on a unique
  index, and leave the in-memory ivar diverging from the DB once an example's
  writes roll back. Fix: `let` + factories (§3), or `test-prof`'s `let_it_be`
  when the setup cost is real.
- **Misplaced or mixed spec types**: several top-level `describe`s of different
  types in one file, or explicit `type:` metadata compensating for the wrong
  directory. Breaks `infer_spec_type_from_file_location!`, makes
  `rspec spec/models` silently skip or unexpectedly boot a browser. Fix: one
  spec type per file, in the directory that implies it.
- **Fragile / overspecified test**: asserts on incidental details or exact
  internal structure. Fix: assert the behavior the caller relies on.
- **Weak / vacuous assertion**: the opposite failure, an assertion so loose it
  verifies almost nothing (`be > 0`, `be_truthy`, `be_present`, `not_to be_nil`,
  `have_received(:x)` with no `.with(...)` when the args are the behavior). It gives
  green coverage while pinning no real behavior, so the code could break and the
  test stay green. LLM-written suites lean on these to reach green. Fix: assert the
  exact expected value/effect from explicit input.
- **Non-deterministic test**: time, randomness, order, network, leaked state.
  Fix: §1 checklist.
- **Assertion roulette**: many unlabeled assertions in one test; on failure you
  can't tell which broke. Fix: split, or name/aggregate them.
- **Eager test**: one test exercising many behaviors. Fix: one behavior per test.
- **Testing private methods**: binds tests to implementation. Fix: test through
  the public API.
- **Testing the framework**: `have_many`/validation one-liners that just re-state
  a model line, or asserting Rails' own machinery. Fix: test your rules and usage.
- **Redundant controller/view specs**: logic already covered by request/system
  specs. Fix: prefer request specs; add a controller spec only for genuine
  controller-only conditional logic.
- **Bare `raise_error` / bare `double`**: both match anything and hide bugs. Fix:
  constrain the error class/message; use verified doubles.
- **`sleep` in system specs**: races. Fix: Capybara auto-waiting matchers.

Sources: https://martinfowler.com/articles/nonDeterminism.html,
https://thoughtbot.com/blog/dealing-with-flaky-tests,
https://guides.rubyonrails.org/testing.html,
https://api.rubyonrails.org/classes/ActiveSupport/Testing/TimeHelpers.html,
https://github.com/bblimke/webmock, https://github.com/vcr/vcr,
https://github.com/simplecov-ruby/simplecov, http://xunitpatterns.com/.
