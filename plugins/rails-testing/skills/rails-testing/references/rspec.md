# RSpec + rspec-rails reference

Depth for writing RSpec on modern Rails (6/7/8). The SKILL.md holds the judgment
(what to test, what to mock); this holds the mechanics. Opinionated where the
community has consensus; contested points flagged.

## Contents
1. Config files and spec types
2. describe / context / it and naming
3. let, subject, hooks
4. Matchers (equality, high-value, rails, shoulda-matchers)
5. Verified doubles and mocking
6. Request specs
7. System specs (Capybara)
8. Shared examples, support/, helpers
9. Config knobs worth setting

---

## 1. Config files and spec types

Three files, by design:

- **`.rspec`**: CLI defaults, one flag per line. Almost always just
  `--require spec_helper`. Keep `--format documentation` out of it (noisy in CI);
  pass per-run.
- **`spec/spec_helper.rb`**: configures RSpec itself, **no Rails**. Require this
  in pure-Ruby specs (POROs, `lib/`) so they stay fast.
- **`spec/rails_helper.rb`**: requires `spec_helper`, boots Rails
  (`require File.expand_path("../config/environment", __dir__)`), aborts if
  `Rails.env.production?`, loads `rspec/rails`. Require this in any spec touching
  Rails. The split exists purely so non-Rails specs don't pay Rails' boot cost.

`rails generate rspec:install` generates a config block whose important defaults are:

```ruby
RSpec.configure do |config|
  config.fixture_paths = [Rails.root.join("spec/fixtures")] # Rails 7.1+ (was fixture_path, singular)
  config.use_transactional_fixtures = true                  # wrap each example in a rolled-back transaction
  config.infer_spec_type_from_file_location!                # dir => type: metadata
  config.filter_rails_from_backtrace!
end
```

`use_transactional_fixtures = true` is Rails' built-in per-example cleanup and is
why most suites **no longer need database_cleaner** (see reliability.md).

Directory -> `type:` inference:

| Directory | type | Use |
| --- | --- | --- |
| `spec/models/` | `:model` | models, POROs, validations, scopes, logic |
| `spec/requests/` | `:request` | **preferred** for controller/HTTP behavior |
| `spec/system/` | `:system` | **preferred** for end-to-end browser tests |
| `spec/jobs/`, `spec/mailers/`, `spec/helpers/` | resp. | ActiveJob, mail, view helpers |
| `spec/views/`, `spec/routing/` | resp. | rarely needed |
| `spec/features/` | `:feature` | legacy end-to-end (use system) |
| `spec/controllers/` | `:controller` | **discouraged** (use request) |

You can always override with explicit `type:` metadata regardless of location.

**Modern default (rspec-rails 7/8):** the generator now ships
`infer_spec_type_from_file_location!` **commented out** and treats directory-based
inference as legacy, nudging you toward **explicit `type:` metadata on each file**
(`RSpec.describe Coupon, type: :model`). Both work; prefer explicit `type:` for
new suites (it is unambiguous and location-independent), and match whatever the
existing suite already does.

**Consensus (strong):** request specs over controller specs (controller specs
have been discouraged since rspec-rails 3.5; for new apps do not add
`rails-controller-testing`), and system specs over feature specs (system specs
give JS driver config, cross-thread DB visibility, and screenshot-on-failure out
of the box). Sources: rspec-rails README (https://rubydoc.info/gems/rspec-rails),
rspec/rspec-rails#1838, https://www.codewithjason.com/use-controller-request-specs-rails-dont/.

## 2. describe / context / it and naming

- `describe "#instance_method"` and `describe ".class_method"`: the `#` / `.`
  convention distinguishes instance from class methods.
- `context` states a **condition**: start it with "when" / "with" / "without".
  A lone context with no negative counterpart is a smell.
- `it` states an **outcome** in third-person present, no "should":
  `it "returns nil"`, not `it "should return nil"`. Move conditionals into a
  `context`, not the example description.
- Use `described_class` instead of hard-coding the class in the outermost
  `describe`, so a rename does not touch every reference.

```ruby
RSpec.describe Order do
  describe "#total" do
    context "when the order has a discount" do
      it "subtracts the discount amount" do
        # ...
      end
    end
  end
end
```

Source: RSpec Style Guide (https://rspec.rubystyle.guide/).

**One-expectation-per-example is contested.** The old betterspecs.org dogma
predates `aggregate_failures` and verified doubles; treat it as historical. Modern
pragmatic rule: one *behavior* per example, but when setup is expensive, group
related assertions and tag `:aggregate_failures` so every failure is reported:

```ruby
it "creates the user", :aggregate_failures do
  post "/users", params: valid_params
  expect(response).to have_http_status(:created)
  expect(response.parsed_body["email"]).to eq("a@b.com")
end
```

## 3. let, subject, hooks

- **`let(:x) { ... }`**: lazy, memoized per example. Default choice. Prefer over
  `@ivars` (a typo'd `let` raises `NameError`; a typo'd ivar silently returns `nil`).
- **`let!(:x) { ... }`**: eager (runs a `before` that calls `x`). Use **only**
  when the record must exist for an absence/negative assertion even though no
  example references it. Overusing `let!` creates records every example and
  silently slows the suite.
- **`before` hook**: for procedural setup with no value to name (stubbing,
  `travel_to`, sign-in). Rule: `let` for values, `before` for actions.
- **`subject`**: name it (`subject(:order) { described_class.new(...) }`);
  anonymous subjects hurt readability. `it { is_expected.to be_valid }` is sugar
  for `expect(subject)`. Do **not** stub the subject (the object under test).
- Declaration order convention: `subject` -> `let!` / `let` -> `before` / `after`
  -> nested groups.

Balance DRY against locality: deeply nested `let`s defined far from the example
recreate the mystery-guest smell. Sometimes an inline literal beats a distant `let`.

## 4. Matchers

**Equality / identity (get this right):**

- `eq`: value equality (`==`). Default for most assertions.
- `eql`: typed equality (`eql?`): `1` is not `eql` to `1.0`.
- `equal` / `be`: object identity (`equal?`). `be_truthy` / `be_falsey` /
  `be_nil` for truthiness; `be > 5`, `be_within(0.1).of(3)` for numerics.

**High-value:**

- **`change`**: `expect { act }.to change { Model.count }.by(1)`, or
  `.from(a).to(b)`. Needs a **block** on the left.
- **`raise_error`**: `expect { act }.to raise_error(MyError, /msg/)`. **Always
  pass a class and/or message**; a bare `raise_error` matches any error
  (including a `NoMethodError` from your own typo) and hides bugs.
- **`contain_exactly` / `match_array`**: order-independent collection equality.
  Use these instead of `eq` when order is not guaranteed (e.g. an unordered
  relation) to avoid flaky order-dependence.
- **`have_attributes`**, `include`, `all`, `start_with`, `match` (regex/matcher).
- **Predicate matchers**: any `foo?` becomes `be_foo` / `have_foo`
  (`be_valid` from `valid?`, `be_empty`, `have_key`).
- **Composable**: pass matchers as arguments:
  `contain_exactly(a_string_starting_with("x"), a_value_within(0.1).of(2.5))`.

**Custom matchers**: `RSpec::Matchers.define(:be_a_multiple_of) { |n| match { |a| a % n == 0 } }`.
Prefer a well-named custom matcher over a helper when it improves the failure message.

**Negated matchers** (for asserting a side effect does *not* happen inside a
compound expectation): `not_to` works alone, but to `.and` several negatives
together you need a defined negated matcher, since `change`/`have_enqueued_job`
have no built-in negation:

```ruby
RSpec::Matchers.define_negated_matcher :not_change, :change
RSpec::Matchers.define_negated_matcher :not_have_enqueued_job, :have_enqueued_job

expect { service.call(bad_input) }
  .to raise_error(ActiveRecord::RecordInvalid)
  .and not_change(User, :count)
  .and not_have_enqueued_job(SyncJob)
```

This is the idiomatic way to prove an error path fired **no** side effects.

**rspec-rails matchers:** `have_http_status(:created)` (symbol, code, or generic
`:success` / `:redirect`), `redirect_to`, `have_enqueued_job` /
`have_enqueued_mail`, `have_broadcasted_to`, route matchers `route_to` /
`be_routable`. `render_template` / `assigns` need `rails-controller-testing`;
in request specs assert on `response.body` / redirect location instead.

**shoulda-matchers (thoughtbot)**: one-liners for the model's declared contract.
Configure in `rails_helper`:

```ruby
Shoulda::Matchers.configure do |c|
  c.integrate { |with| with.test_framework :rspec; with.library :rails }
end
```

- Validations: `validate_presence_of(:name)`,
  `validate_uniqueness_of(:email).case_insensitive`,
  `validate_length_of(:bio).is_at_most(500)`, `validate_numericality_of`.
- Associations: `have_many(:comments).dependent(:destroy)`,
  `belong_to(:author).optional`, `have_one(:profile)`.
- Others: `define_enum_for`, `have_db_index`, `permit(...)` (strong params).

`it { is_expected.to validate_presence_of(:name) }`. Contested: critics
(codewithjason) argue association one-liners just re-assert a model line;
thoughtbot notes they actually exercise the machinery. Pragmatic: cheap
regression guards for the declared contract, not a substitute for behavior tests.
`validate_uniqueness_of` is a known gotcha (needs a persisted record to test against).

## 5. Verified doubles and mocking

Set `config.mock_with :rspec { |m| m.verify_partial_doubles = true }` (default).

- **`instance_double(User, name: "A")`**: verifies the stubbed method **exists on
  User** with a valid signature. A renamed/removed method fails the test. This is
  the single most important mocking practice; it stops mocks drifting out of sync.
- **`class_double(User)`**, **`object_double(instance)`**: same for class methods
  / a specific instance.
- Plain **`double`** verifies nothing. Use only when no class exists yet.
- **allow vs expect vs spy:**
  - `allow(x).to receive(:m).and_return(v)`: stub, no call requirement.
  - `expect(x).to receive(:m)`: mock, set **before** the action.
  - **spy**: `instance_spy(Klass)` then assert after with
    `expect(x).to have_received(:m).with(args)`. Reads arrange-act-assert; prefer
    it for outgoing-command verification (the one legitimate mock cell).
  - Chainable: `.with`, `.once` / `.exactly(n).times`, `.and_raise`,
    `.and_call_original`, `.ordered`.
- **`stub_const("Foo::BAR", 5)`** / `stub_const("SomeClass", fake)`: the correct
  way to replace a constant/class for one example; restored after.
- **Avoid `allow_any_instance_of` / `expect_any_instance_of`**: a design smell
  (you cannot name the instance). Inject the collaborator instead.

See philosophy.md for *which* messages to mock (Sandi Metz). The mechanics here
serve that policy; do not mock more than the outgoing-command cell calls for.

## 6. Request specs (the workhorse)

```ruby
RSpec.describe "Articles", type: :request do
  describe "GET /articles" do
    it "returns all articles" do
      create_list(:article, 3)
      get articles_path
      expect(response).to have_http_status(:ok)
      expect(response.parsed_body.size).to eq(3)
    end
  end
end
```

- Verb helpers `get/post/patch/put/delete` take `params:`, `headers:`, and
  `as: :json` (sets Content-Type and encodes the body). Follow redirects with
  `follow_redirect!`.
- Assert on `response`: `have_http_status`, `response.body`, `response.headers`,
  `response.location`. Use **`response.parsed_body`** (parses JSON/HTML) over
  `JSON.parse(response.body)`.
- **JSON APIs:** send with `as: :json`; assert on `parsed_body` with composable
  matchers (`include`, `match`, `contain_exactly`). Test status + body + relevant
  headers; never internal ivars (a controller-spec habit).

**Auth (Devise + Warden):** Devise's `sign_in` controller helper does **not** work
in request specs. Use Warden test helpers:

```ruby
# spec/support/warden.rb
RSpec.configure do |config|
  config.include Warden::Test::Helpers, type: :request
  config.after(type: :request) { Warden.test_reset! }   # required, or a login leaks
end
# in a spec:
before { login_as(user, scope: :user) }
```

For token/JWT APIs, pass the auth header directly via a helper that returns headers.
If the behavior needs no browser/JS, a request spec is 1-2 orders of magnitude
faster and less flaky than a system spec: push coverage here.

## 7. System specs (Capybara)

```ruby
RSpec.configure do |config|
  config.before(:each, type: :system) { driven_by :rack_test }
  config.before(:each, type: :system, js: true) do
    driven_by :selenium, using: :headless_chrome, screen_size: [1400, 1400]
    # or, increasingly preferred: driven_by :cuprite
  end
end
```

- **`rack_test`**: no JS, in-process, fast. Default for non-JS system specs.
- **`selenium :headless_chrome`**: real browser via chromedriver. Standard for JS.
- **Cuprite**: Chrome over CDP, no chromedriver; faster, fewer moving parts;
  increasingly the community's preferred JS driver.

Capybara idioms: `visit`, `click_on`, `fill_in "Email", with: "..."`, `select`,
`check`, `within("#sidebar") { ... }`. Assert with `have_content`,
`have_selector`, `have_current_path`. Prefer **negative Capybara matchers**
(`have_no_content`) over `not_to have_content`.

**Flakiness (critical):** rely on Capybara's auto-waiting (`have_content` retries
up to `Capybara.default_max_wait_time`, default 2s; raise to ~5s in CI). **Never
`sleep`.** Never mix waiting and non-waiting APIs: `have_no_css` waits;
`page.has_css?(...)).to be false` checks once and races. Rails system specs share
the DB connection between the test thread and the app server, so data created in
the test is visible to the browser (the feature that feature specs lack), and a
screenshot is auto-saved to `tmp/screenshots` on failure. See reliability.md.

## 8. Shared examples, support/, helpers

- **`spec/support/` is not autoloaded.** Require it in `rails_helper`:
  `Dir[Rails.root.join("spec/support/**/*.rb")].sort.each { |f| require f }`. The
  generated line ships commented out (eager-requiring everything slows single-file
  boot); enable it if you use shared examples/helpers broadly.
- **`shared_examples` / `it_behaves_like`**: a reusable contract ("behaves like a
  soft-deletable record"). `it_behaves_like` nests in its own context;
  `include_examples` inlines into the current scope.
- **`shared_context` / `include_context`**: reusable setup; auto-include by
  metadata with `config.include_context "...", :tag`.
- **Custom helper modules** in `spec/support/`, scoped by type:
  `config.include ApiHelpers, type: :request`. Scoping keeps helpers out of specs
  that don't need them.

## 9. Config knobs worth setting

- `config.order = :random` + `Kernel.srand config.seed`: random order surfaces
  order-dependence; the seed prints so you can reproduce with `--seed`.
- `config.filter_run_when_matching :focus`: lets `fit` / `fdescribe` narrow a run.
- `config.example_status_persistence_file_path = "spec/examples.txt"`: enables
  `--only-failures` / `--next-failure` (gitignore the file).
- `config.include FactoryBot::Syntax::Methods`: call `create(:user)` bare.
- `config.include ActiveSupport::Testing::TimeHelpers` and
  `config.include ActiveJob::TestHelper`: time travel and job assertions.

Primary sources: https://rspec.info/features/, https://rubydoc.info/gems/rspec-rails,
https://rspec.rubystyle.guide/, https://github.com/thoughtbot/shoulda-matchers,
https://evilmartians.com/chronicles/system-of-a-test-setting-up-end-to-end-rails-testing.
