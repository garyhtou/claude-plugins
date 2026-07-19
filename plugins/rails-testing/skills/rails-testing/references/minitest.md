# Minitest + Rails reference

Minitest is Rails' default test framework and, with fixtures, the Rails-core
("Omakase") choice. Treat it as a first-class target, not an RSpec fallback. The
SKILL.md holds the judgment; this holds the mechanics. Primary source: the Rails
Testing Guide (https://guides.rubyonrails.org/testing.html).

## Contents
1. test/ structure and run commands
2. Two syntax styles
3. Assertions (argument order matters)
4. Fixtures
5. factory_bot with Minitest
6. Mocking: minitest/mock and mocha
7. Integration vs system tests
8. Parallel testing
9. Time, jobs, mail helpers
10. Gotchas checklist

---

## 1. test/ structure and run commands

Each folder maps to a base class:

| Folder | Base class |
| --- | --- |
| `test/models/` | `ActiveSupport::TestCase` |
| `test/controllers/`, `test/integration/` | `ActionDispatch::IntegrationTest` |
| `test/system/` | `ActionDispatch::SystemTestCase` |
| `test/mailers/` | `ActionMailer::TestCase` |
| `test/jobs/` | `ActiveJob::TestCase` |
| `test/helpers/` | `ActionView::TestCase` |
| `test/channels/` | `ActionCable::Channel::TestCase` |
| `test/fixtures/` | YAML data (+ `files/`, mailer subdirs) |

`test/test_helper.rb` is required by every test file (`require "test_helper"`); it
sets `ENV["RAILS_ENV"] ||= "test"`, loads the env, usually declares
`fixtures :all`, and enables `parallelize`.

Run commands (prefer the `bin/rails` binstub):

```bash
bin/rails test                                 # whole suite (EXCLUDES system tests)
bin/rails test test/models/article_test.rb     # one file
bin/rails test test/models/article_test.rb:6   # one test by line
bin/rails test test/models/article_test.rb:6-20 # a line range
bin/rails test test/models                      # a directory
bin/rails test -n test_the_truth                # filter by method name (regex ok: -n "/truth/")
bin/rails test -f                               # fail fast
bin/rails test --seed 1234                      # reproduce a random ordering
bin/rails test -b                               # full backtrace (don't filter Rails frames)
bin/rails test:system                           # system tests (NOT run by plain `test`)
bin/rails test:all                              # everything including system
```

`-n` matches the **method** name: the `test "the truth"` macro defines
`test_the_truth` (spaces -> underscores), so filter with `-n test_the_truth`. The
`path:line` form targets whichever test the line falls inside, ideal for iterating
on one failing test.

## 2. Two syntax styles

**(a) Classic / xUnit (what Rails devs overwhelmingly use):**

```ruby
require "test_helper"

class ArticleTest < ActiveSupport::TestCase
  setup    { @article = articles(:one) }   # runs before each test
  teardown { Rails.cache.clear }            # runs after each test

  test "the title must be present" do        # Rails `test` macro
    @article.title = nil
    assert_not @article.valid?
  end

  def test_saving_increments_count           # plain method form, also valid
    assert_difference "Article.count", 1 do
      Article.create!(title: "x")
    end
  end
end
```

The `test "..." do` macro is Rails sugar defining a `test_<slug>` method with
readable failure output. Two tests with the same description raise "test already
defined." `setup` / `teardown` accept a block, symbol, or lambda; multiple `setup`
blocks run in order. `assert_not` is a **Rails** addition (see §3).

**Off Rails (plain gems/POROs), none of that sugar exists:** subclass
`Minitest::Test` (not `ActiveSupport::TestCase`), require `minitest/autorun`, name
tests `def test_...` (the `test "..." do` macro and `assert_not` are ActiveSupport
extensions, so either define them yourself or use `def test_` + `refute`), and run
with `ruby -Ilib -Itest test/foo_test.rb` or a `Rake::TestTask` (`rake test`),
never `bin/rails test`. See the SKILL's "Off Rails" section.

**(b) Spec style (`describe` / `it`)** via `minitest/spec`: less common in Rails
app code, more in gems:

```ruby
describe Meme do
  before { @meme = Meme.new }
  it "responds positively" do
    _(@meme.cheezburger?).must_equal "OHAI!"   # note the _() wrapper
  end
end
```

Expectations need the `_( )` wrapper; methods are `must_*` / `wont_*`. Rails-core
convention favors the classic style; the `test` macro + fixtures is the default.
Both styles run on the same runner.

## 3. Assertions (argument order matters)

**Critical: `assert_equal(expected, actual)`: expected first, actual second.**
Reversing it produces misleading failure messages. Single most common Minitest mistake.

Core (`Minitest::Assertions`), each with a `refute_*` inverse:

| Assertion | Notes |
| --- | --- |
| `assert(test)` / `refute(test)` | truthy / falsey |
| `assert_equal(exp, act)` | `==`; **expected first** |
| `assert_nil(obj)` | is nil |
| `assert_same(exp, act)` | object **identity** (`equal?`), not `==` |
| `assert_match(regexp, str)` | pattern |
| `assert_includes(coll, obj)` | membership |
| `assert_empty(obj)` | `obj.empty?` |
| `assert_predicate(obj, :zero?)` | calls a `?` method, nicer message |
| `assert_instance_of` / `assert_kind_of` | exact class / class-or-subclass |
| `assert_respond_to(obj, :m)` | responds to |
| `assert_raises(Err) { ... }` | **returns the exception** so you can assert its message |
| `assert_in_delta(exp, act, d)` | float comparison |

```ruby
err = assert_raises(ArgumentError) { do_thing }
assert_equal "bad arg", err.message
```

Rails aliases `assert_not`, `assert_not_equal`, `assert_not_nil` (but not every
inverse); for the rest use `refute_*`.

Rails-added assertions:

```ruby
# state / DB change
assert_difference "Article.count", 1 do ... end       # String (eval'd) or lambda; delta default 1
assert_difference ["A.count", "B.count"], -1 do ... end
assert_no_difference("Article.count") { ... }
assert_changes -> { order.status }, from: "pending", to: "paid" do ... end
assert_no_changes(-> { order.status }) { ... }

# HTTP / routing (integration & controller tests)
assert_response :success            # or :redirect, :missing (404), :error (5xx), or 200
assert_redirected_to article_url(@article)
assert_routing "/photos/1", controller: "photos", action: "show", id: "1"

# HTML (assert_select / modern alias assert_dom)
assert_select "ul.nav" do assert_select "li", count: 3 end
assert_dom "a[href=?]", article_url(article), text: "Read"

# mail
assert_emails(1) { UserMailer.welcome(user).deliver_now }
assert_enqueued_email_with(UserMailer, :welcome, args: [user]) { ... }  # deliver_later

# Action Cable
assert_broadcasts("notifications", 1) { ... }
assert_broadcast_on("notifications", body: "hi") { ... }

# query counting
assert_queries_count(2) { ... }
assert_no_queries { ... }
```

Custom assertions are plain methods calling `assert` / `refute`, mixed into
`ActiveSupport::TestCase` via a module.

## 4. Fixtures

YAML in `test/fixtures/<table>.yml`:

```yaml
# users.yml
david:
  name: David
  email: david@example.com
# articles.yml
welcome:
  title: Welcome to Rails!
  author: david          # association by fixture LABEL, not id
```

- **Labels -> deterministic hashed IDs.** You never write primary keys; Rails
  hashes the label into a stable id, and associations reference the **label**
  (`author: david`), which Rails resolves. Never hardcode ids.
- **Accessors:** the file name becomes a method: `users(:david)`,
  `articles(:welcome, :other)`, `users(:david).id`.
- **`fixtures :all`** in `test_helper.rb` loads every file for every test.
- **ERB is preprocessed**, so fixtures can be generated
  (`<% 1.upto(100) do |i| %> ... <% end %>`).
- **ActiveStorage / mailer:** `ActiveStorage::FixtureSet.blob filename: "x.png"`;
  mailer body fixtures live in `test/fixtures/<mailer_name>/`.

**Performance model:** fixtures load **once** (bulk insert, outside the
per-test transaction); then each test runs in a transaction rolled back at the
end (`use_transactional_tests = true`, default). Fast, and tests never see each
other's mutations. Disable per class with `self.use_transactional_tests = false`
(e.g. when the code manages its own transactions).

Fixtures vs factories: fixtures are dramatically faster (loaded once) and are
Rails core's choice for exactly that reason (DHH's "fast tests"). The cost is
global shared data that can become brittle ("change one fixture, break 40 tests")
and the label/hashed-id learning curve. See test-data.md for the full tradeoff.

## 5. factory_bot with Minitest

If the team prefers factories, add `factory_bot_rails` and include the syntax
methods so `create` / `build` work bare:

```ruby
# test/test_helper.rb
module ActiveSupport
  class TestCase
    include FactoryBot::Syntax::Methods   # else every call is FactoryBot.create(:user)
  end
end
```

Factories and fixtures can coexist. The common critique (and why Rails core
sticks with fixtures) is that factories are slow when a test unintentionally
`create`s many associated records. The `build_stubbed` / `build` ladder recovers
most of that speed (see test-data.md).

## 6. Mocking: minitest/mock and mocha

**Built-in `minitest/mock` is deliberately minimal.**

`Object#stub` replaces a method for a block only; the method must already exist;
no argument matching:

```ruby
Time.stub :now, Time.at(0) do
  assert obj.stale?
end
account.stub(:balance, -> { 100 }) do ... end   # a callable's result is used
```

`Minitest::Mock` is a strict expectation object:

```ruby
mock = Minitest::Mock.new
mock.expect(:save, true)
mock.expect(:update, true, [{ name: "x" }])       # with args
# ... exercise code with `mock` ...
assert mock.verify                                  # fails unless every expectation was met
```

`verify` raises `MockExpectationError` on an unmet or unexpected call.

**mocha** (very common in Rails) is richer. Require it **after** the test library:

```ruby
# test_helper.rb, AFTER require "rails/test_help"
require "mocha/minitest"                             # auto-verifies at teardown
```

```ruby
product.stubs(:save).returns(true)
product.stubs(:name).returns("x").then.returns("y") # sequential returns
product.expects(:name).with("abc").returns(true)    # expectation + arg matcher
Product.any_instance.stubs(:name).returns("stub")   # every instance
obj.expects(:log).with(has_entry(level: :warn))     # parameter matchers
seq = sequence("load"); obj.expects(:start).in_sequence(seq)  # ordering
m = mock("payment"); m.expects(:process).with(:usd).returns(:ok).once
s = stub(method1: :r1); s = stub_everything          # lenient stubs
```

Reach for mocha when you need matchers, `any_instance`, or sequences that
`minitest/mock` cannot express. As always, mock only outgoing commands to true
boundaries (see philosophy.md); `any_instance` and class-method stubbing are
powerful but coupling-prone.

## 7. Integration vs system tests

**`ActionDispatch::IntegrationTest`**: full stack through real requests
(routing -> controller -> view), **no JS, no browser**. Fast. This is also what
modern controller tests use, and the recommended place for controller/API
behavior:

```ruby
class ArticlesTest < ActionDispatch::IntegrationTest
  test "create then show" do
    assert_difference "Article.count", 1 do
      post articles_url, params: { article: { title: "Hi" } }
    end
    assert_redirected_to article_url(Article.last)
    follow_redirect!
    assert_select "h1", "Hi"
  end
end
```

Verbs `get post patch put delete head` with `params:`, `headers:`, `env:`,
`xhr: true`, `as: :json`. After a request you get `@response`, `@request`,
`follow_redirect!`, `cookies`. `as: :json` sets content type and parses
`response.parsed_body`.

**`ActionDispatch::SystemTestCase`**: real browser via Capybara, exercises JS.
Configure once:

```ruby
# test/application_system_test_case.rb
class ApplicationSystemTestCase < ActionDispatch::SystemTestCase
  driven_by :selenium, using: :headless_chrome, screen_size: [1400, 1400]
  # or the third-party cuprite driver (headless Chrome via CDP, no webdriver):
  # driven_by :cuprite
end
```

Capybara DSL (`visit`, `click_on`, `fill_in`, `assert_selector`, `assert_text`,
`assert_current_path`, `within`, `accept_confirm`). Screenshots on failure are
automatic (`tmp/screenshots/`; env `RAILS_SYSTEM_TESTING_SCREENSHOT`). System
tests share a DB connection with the browser in modern Rails (no truncation
needed) and are **not** part of `bin/rails test` (run `test:system` / `test:all`).

Rule of thumb: integration tests for controller/API behavior; system tests only
for JS-dependent UI flows, kept few.

## 8. Parallel testing (a real Minitest + Rails advantage)

```ruby
class ActiveSupport::TestCase
  parallelize(workers: :number_of_processors)
end
```

- **Processes (default):** forks workers coordinated over DRb; each gets its
  **own database** (`myapp_test-0`, `-1`, ...), created and schema-loaded
  automatically. Safest; required for system tests.
- **Threads:** `parallelize(workers: N, with: :threads)` shares one connection;
  **no separate DBs, not for system tests.** For JRuby/TruffleRuby or thread-safe
  IO-bound suites.
- **`PARALLEL_WORKERS` env var overrides `workers:`** (`PARALLEL_WORKERS=15 bin/rails test`);
  `PARALLEL_WORKERS=1` effectively disables it (needed when using a debugger).
- **`parallelize(threshold: 100)`** skips forking for small runs.
- Per-worker hooks: `parallelize_setup { |worker| ... }` /
  `parallelize_teardown { |worker| ... }`.

Tests must be **order-independent and isolated**; namespace any shared external
state (a Redis key, a temp filename, a port) by `worker` in `parallelize_setup`
or parallel runs collide.

## 9. Time, jobs, mail helpers

- **Time** (`ActiveSupport::Testing::TimeHelpers`): `travel_to(t) { ... }`,
  `freeze_time { ... }`, `travel(1.day)`, `travel_back`. Prefer block forms
  (auto-reset). See reliability.md for the timezone rules.
- **Active Job** (`ActiveJob::TestHelper`; default adapter `:test` enqueues but
  does not run): `assert_enqueued_jobs`, `assert_enqueued_with(job:, args:)`,
  `perform_enqueued_jobs { ... }`, `assert_performed_with`.
- **Action Mailer** (`:test` delivery method): `deliver_now` populates
  `ActionMailer::Base.deliveries` (assert with `assert_emails`); `deliver_later`
  enqueues a job (assert with `assert_enqueued_email_with` or wrap in
  `perform_enqueued_jobs`).

## 10. Gotchas checklist

1. `assert_equal(expected, actual)`: expected first. Never flip it.
2. Reference fixtures by **label** (`users(:david)`, `author: david`), never by id.
3. `bin/rails test` skips `test/system/`; run `test:system` / `test:all`.
4. Tests run **random order** and (with `parallelize`) **in parallel**: keep every
   test isolated; namespace shared external state per worker.
5. `assert_not` is Rails-only; for the general inverse use `refute_*`.
6. `deliver_now` -> `assert_emails`; `deliver_later` -> ActiveJob assertions.
7. `minitest/mock` is minimal (block-scoped, method must exist, no matchers); add
   `mocha` for matchers / `any_instance` / sequences.
8. Reproduce a flaky failure with the printed `--seed`; target one test with `path:line`.
9. Duplicate `test "same name"` descriptions raise an error.
10. `use_transactional_tests` (default) rolls back each test; don't rely on
    records persisting across tests.

Sources: https://guides.rubyonrails.org/testing.html,
https://github.com/minitest/minitest, https://github.com/freerange/mocha,
https://api.rubyonrails.org/classes/ActiveSupport/TestCase.html,
https://blog.appsignal.com/2022/03/16/the-perils-of-parallel-testing-in-ruby-on-rails.html.
