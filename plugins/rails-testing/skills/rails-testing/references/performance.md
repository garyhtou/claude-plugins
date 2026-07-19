# Performance-regression testing reference

How to use the test suite to stop Rails performance regressions, mainly N+1 and
runaway query counts. The SKILL.md holds the judgment; this holds the mechanics,
tool APIs, and the "why." Opinionated where the community has consensus.

## Contents
1. The core principle: assert counts, not time
2. What tests can and cannot catch (the determinism split)
3. The N+1 test done right (scale-invariance, not magic numbers)
4. Tooling map (what each gem is actually for)
5. strict_loading: the broad always-on tripwire
6. Keeping performance tests from being flaky themselves
7. Anti-patterns
8. Sources

---

## 1. The core principle: assert counts, not time

**A performance-regression test asserts on a count you can make deterministic (SQL
queries, and to a lesser degree object allocations), never on wall-clock time.**
Query count is a pure function of the code path and the input: same records, same
code, same number of queries, on any machine, every run. That is a true regression
signal. Wall-clock time is a function of the machine, its noisy neighbors, GC
timing, and I/O, so a time threshold on shared CI is either so tight it is flaky or
so loose it never catches the regression you wrote it for. Shared CI runners have
been measured at >30% run-to-run variance (a ~45% false-alarm rate) versus ~0% on
isolated bare metal. Flaky performance tests get muted, then deleted.

Rails itself shipped the deterministic primitive (`assert_queries_count`,
`assert_no_queries`, `assert_queries_match` in `ActiveRecord::Assertions::QueryAssertions`,
public since Rails 7.2), which is a tacit endorsement that query counting is the
sanctioned in-CI performance primitive.

**Legitimate home for time-based benchmarking:** a separate, out-of-band suite on
isolated hardware (or a noise-controlling service), with warmup, many iterations,
comparing relative deltas, treated as a trend report, never a PR gate. Keep
`benchmark-ips` / `derailed_benchmarks` / `rspec-benchmark` time matchers there,
not in CI.

## 2. What tests can and cannot catch (the determinism split)

| Problem | Test-catchable in CI? | How | Determinism |
| --- | --- | --- | --- |
| N+1 / query-count growth | **Yes** | count SQL events; assert count constant across dataset sizes | deterministic |
| Missing index / bad SQL plan | **Partially** | assert query *shape* (a join, not a loop); plan quality needs prod-scale data CI lacks | shape yes, plan no |
| Wall-clock latency / p95 | **No** | too noisy on shared runners | flaky |
| Memory / allocations | **Possible** | assert object-allocation counts (deterministic-ish) | object counts yes, bytes noisier |

Almost every latency regression a test could catch shows up first as *more queries*
or *more allocations*. Guard those, and you catch the cause before the symptom.
Berkopec's rule of thumb for "healthy": a controller action should issue roughly
**one SQL query per table**, and N+1s during collection/partial rendering are the
most common offenders.

## 3. The N+1 test done right (scale-invariance, not magic numbers)

**Brittle (do not do this):**
```ruby
# "2 posts -> 3 queries": breaks the day anyone adds an unrelated query
expect { get "/posts" }.to make_database_queries(count: 3)
```
A new `current_user` lookup, a feature-flag read, a counter-cache write, or a join
from a schema change flips the number, and the test goes red for a reason unrelated
to N+1. People then "fix" it by bumping the magic number, which trains everyone to
treat it as noise. That is testing an incidental implementation detail, not behavior.

**Robust: assert the query count does NOT grow with the number of records.** Run
the same code at two dataset sizes and assert the count is constant (O(1)). A fixed
baseline of "boring" queries cancels out; only genuine growth fails. This is
performance testing, not feature testing.
```ruby
# RSpec, via n_plus_one_control
require "n_plus_one_control/rspec"

context "N+1", :n_plus_one do
  populate { |n| create_list(:post, n, :with_author) }   # n records per scale factor

  specify do
    expect { get "/posts" }.to perform_constant_number_of_queries
  end
end
```
For a legitimately linear relationship, bound the slope instead:
`perform_linear_number_of_queries(slope: 1)`. Minitest:
`assert_perform_constant_number_of_queries(populate: ->(n){ create_list(:post, n) }) { get "/posts" }`.

No-dependency version: subscribe to `sql.active_record`, run the block at N and
N+1, compare counts (~11 lines). Same idea, no gem.

**When you do need a raw count, scope it to a query shape**, not the global total,
so unrelated queries never enter the assertion:
```ruby
assert_queries_match(/FROM "comments"/, count: 1) { get "/posts" }  # Rails 7.2+
```

## 4. Tooling map (what each gem is actually for)

Reach for the right layer; most of these can fail a test, a couple only inform.

- **`n_plus_one_control` (palkan / Evil Martians), maintained, Rails 8:** the
  smartest CI tool. Runs the block at multiple scale factors and asserts the count
  does not grow. Matchers `perform_constant_number_of_queries` /
  `perform_linear_number_of_queries(slope:)`; Minitest
  `assert_perform_constant_number_of_queries`. This is the default recommendation
  for N+1 regression guards, and a fixed N+1 becomes a permanent regression test.
- **`db-query-matchers` (sds), maintained, RSpec:** `expect { }.to
  make_database_queries(count: 0..3, matching: /.../, manipulative: true)` and
  `.not_to make_database_queries` (great for asserting a cache/memoization path
  does zero queries). Use for an exact/bounded count on a specific unit. Prefer a
  **range** over an exact integer to reduce brittleness.
- **Rails built-in `QueryAssertions` (public since 7.2), Minitest:**
  `assert_queries_count(n)`, `assert_no_queries { }`, `assert_queries_match(/re/,
  count:)`, `assert_no_queries_match`. No gem needed. Options `count:` and
  `include_schema:`. In RSpec, either use db-query-matchers or `include
  ActiveRecord::Assertions::QueryAssertions` and call the assertion directly (no
  native rspec-rails matcher ships yet).
- **`prosopite` (charkost), maintained, Rails 8:** runtime N+1 detector using
  call-stack + query-fingerprint matching; advertises zero false positives/
  negatives and catches cases Bullet misses (N+1 **after** `create_list`, first/
  last/pluck N+1, non-association N+1). `Prosopite.raise = true` in test env; wrap
  **each** example with `Prosopite.scan` / `Prosopite.finish` (per-example, not
  per-suite). Preferred over Bullet for suite use. Tells you *where*, not *how*.
- **`bullet` (flyerhzm), maintained, Rails 8:** the classic detector; also flags
  unused eager loading and suggests the fix (`add .includes(:comments)`). Set
  `Bullet.raise = true` in the test env to fail CI. **Gotcha:** detection rides
  Rack middleware, so it fires for request/system/controller specs but **not**
  plain model/unit tests unless you wrap them in `Bullet.profile { }`. Known for
  occasional false positives/negatives, which is why Prosopite exists.
- **Query-count loggers are not test tools.** Gems like `query_count` (rubysamurai)
  and `makandra/query_diet` print a per-request query count to the log or a dev
  widget; they have no matcher and no N+1 detection, so they cannot assert anything
  in a spec. Reach for a real matcher instead: `db-query-matchers` (above) for
  RSpec, the Rails built-ins for Minitest, or `n_plus_one_control` for scaling.
  (`Gusto/ar-query-matchers` and `rspec-sqlimit`'s `exceed_query_limit(n)` are other
  RSpec options.)
- **`rspec-benchmark` (dormant ~2019):** matchers `perform_under(n).ms`,
  `perform_at_least(n).ips`, complexity (`perform_constant`/`perform_linear`), and
  `perform_allocation`. The **time** matchers are CI-flaky (see section 1); the
  safe-in-CI subset is `perform_allocation` and the complexity matchers.
- **`strong_migrations` (ankane), maintained:** migration-time safety, adjacent but
  essential. Raises `StrongMigrations::UnsafeMigration` on operations that lock a
  big table, add a non-concurrent index, do an un-throttled backfill, etc. Fails
  the migration (and CI if migrations run there) before it locks production.
- **`test-prof` (Evil Martians):** profiles the **speed of the test suite itself**
  (factory cascades, `let_it_be`/`before_all`), not application performance. Do not
  conflate it with the query/N+1 tools. `derailed_benchmarks` is for **diagnosing**
  a regression (esp. memory), not a per-commit gate.

## 5. strict_loading: the broad always-on tripwire

`strict_loading` (Rails 6.1+) flips the default from "silently fire an extra query"
to "raise `ActiveRecord::StrictLoadingViolationError` the moment you lazy-load a
not-preloaded association." Turn it on in test and any request/system/controller
spec that renders or serializes a collection becomes an N+1 detector **for free**,
no assertion needed. It is the one N+1 defense that is native, zero-dependency, and
enforced just by running your existing tests through real code paths.

**Enable it (test + development):**
```ruby
# config/environments/test.rb (and development.rb)
config.active_record.strict_loading_by_default = true
# keep the two defaults: mode :all, action :raise
```
Three distinct settings, and they are widely confused (do not mix them up):
- `config.active_record.strict_loading_by_default` (default `false`) -> set `true`.
- `config.active_record.strict_loading_mode` (default **`:all`**; other value
  **`:n_plus_one_only`**). Values are ONLY those two.
- `config.active_record.action_on_strict_loading_violation` (default **`:raise`**;
  other value **`:log`**). `:log` belongs to THIS setting, not to
  `strict_loading_mode` (a common doc error).

Granularities (most specific wins): global config, per-model
(`self.strict_loading_by_default = true`), per-association
(`has_many :reviews, strict_loading: true`), per-query (`.strict_loading` /
`.strict_loading!(false)` to opt out).

**Posture:** `:raise` in dev and test; if you enable it in production, use `:log`
(monitor violations without 500ing a request). **In the test suite use mode `:all`,
not `:n_plus_one_only`.** `:n_plus_one_only` sounds smarter but Rails can't always
tell single-record from collection access, so it misses real N+1s and gives false
confidence; a test suite wants the strictest signal. (`:n_plus_one_only` is more a
*production* posture, where you don't want to over-eager-load single records.)

**The critical blind spot: it only sees ActiveRecord *association* lazy-loads.** It
does NOT catch N+1 from raw SQL / `find_by_sql`, `.pluck` in a loop,
`.exists?` / `.count` in a loop, `Model.find(id)` inside an iteration, or N+1 that
appears *after* `create_list` in a test. That gap is exactly what a fingerprinting
detector (`prosopite`, raising in test) covers, which is why the two are the
strongest complementary pair. `includes` / `preload` / `eager_load` all satisfy
strict_loading equally (it only cares that the data is loaded before access, not
how). Also note it is disabled inside validations and some reload paths, so a
violation you expect there may not fire.

**Friction (be ready for it), and mitigations:**
- **Serializers** (AMS, Blueprinter, JSONAPI), **GraphQL**, and **admin frameworks**
  (ActiveAdmin, Avo) walk arbitrary associations, so each must be eager-loaded or it
  raises; these often need lookahead-based preloading or a scoped opt-out.
- **`delegate :name, to: :author`** and **callbacks** (`after_save` touching an
  association) raise if that association was not loaded.
- **Factory/fixture setup** that reads an association to build data raises *before*
  the assertion runs. Mitigate by building associations explicitly, reloading
  through an eager query (`User.includes(:activities).find(id)`), or scoping
  strict_loading to the code under test.
- **Existing large app:** do NOT flip it on globally at once (you will drown in
  violations). Adopt per-query/per-model gradually.

**Division of labor and what NOT to do.** strict_loading is the broad safety net;
a handful of `perform_constant_number_of_queries` assertions are the named
guarantees on the endpoints that matter (and survive even if someone disables
strict_loading on a model). **Do not write specs that assert a violation is *not*
raised**, or that an association *is* strict-loaded: the former is already implied
by any request spec that hits the endpoint, and the latter tests Rails internals.
Test the *outcome* (query count), not the mechanism.

## 6. Keeping performance tests from being flaky themselves

Query counting is deterministic only if you control what you count:

- **Filter incidental SQL:** exclude `SCHEMA`, `BEGIN`/`COMMIT`,
  `SAVEPOINT`/`RELEASE`, and cached queries, so you count only what your code
  triggers. Rails' assertions default to `include_schema: false`; n_plus_one_control
  ignores transaction statements by default; db-query-matchers has `ignores` /
  `ignore_cached`.
- **Warm up:** first-call effects (schema load, `current_user` memoization, cache
  priming) inflate the first run. Use a `warmup { get "/posts" }` block (or
  `.with_warming_up`) before measuring.
- **Isolate seeding from the measured block:** create records *outside* the block
  (`populate {}` runs before the expectation; use `let!`), and never memoize the
  subject inside the block (a `let` first-touched inside the expectation hides its
  queries).
- **Assert shape, not total,** when using raw counts (`assert_queries_match(/FROM
  "posts"/, count: 1)`), so a schema change adding an unrelated join does not break
  it.
- **Keep tests independent** (transactional fixtures / clean DB) so counts do not
  depend on what a prior test left behind.

## 7. Anti-patterns

- **Time-threshold assertions on shared CI.** Flaky; either muted or useless. Move
  wall-clock work to an isolated benchmark suite.
- **Hardcoded global query totals** (`make_database_queries(count: 7)` on a whole
  request). Tests implementation incidentals; breaks on unrelated changes; "fixed"
  by bumping the number. Prefer scale-invariance or a scoped shape match.
- **Blanket query-count assertions in every model spec.** Noise; couples the whole
  suite to query implementation. Target request-layer hot spots instead.
- **Dogmatic "zero extra queries everywhere."** Russian-doll caching deliberately
  uses many small, individually-cacheable per-record queries (DHH's "N+1 is a
  feature" argument). Assert *non-scaling* where scaling hurts; leave room for the
  cached-collection pattern as a deliberate choice.
- **Abandoning strict_loading because setup raises.** Scope it, don't drop it.
- **Using a query-count logger (a dev widget) to assert in tests.** Loggers have
  no matcher; use a real one (`db-query-matchers`, the Rails built-ins).

## 8. Sources

- N+1 control (design rationale, the scale-invariance argument): https://evilmartians.com/chronicles/squash-n-plus-one-queries-early-with-n-plus-one-control-test-matchers-for-ruby-and-rails , https://github.com/palkan/n_plus_one_control
- Rails built-in query assertions (public since 7.2): https://api.rubyonrails.org/classes/ActiveRecord/Assertions/QueryAssertions.html , https://github.com/rails/rails/pull/50281
- db-query-matchers: https://github.com/sds/db-query-matchers
- prosopite: https://github.com/charkost/prosopite ; bullet: https://github.com/flyerhzm/bullet
- CI timing variance (why wall-clock is flaky): https://codspeed.io/blog/benchmarks-in-ci-without-noise , https://pythonspeed.com/articles/consistent-benchmarking-in-ci/
- strict_loading: https://thoughtbot.com/blog/strict-loading-in-rails-8-a-railsy-way-to-avoid-n-1-queries , https://blog.saeloun.com/2024/05/21/rails-7-2-strict-loading-using-n-plus-one-only-does-not-eager-load-child-associations/
- Berkopec (query budget, N+1 prevalence): https://www.speedshop.co/2019/01/10/three-activerecord-mistakes.html ; the "N+1 is a feature" counterpoint: https://rossta.net/blog/n-1-is-a-rails-feature.html
- rspec-benchmark: https://github.com/piotrmurach/rspec-benchmark ; strong_migrations: https://github.com/ankane/strong_migrations ; test-prof (suite speed, not app perf): https://test-prof.evilmartians.io/
