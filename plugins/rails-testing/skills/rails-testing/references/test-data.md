# Test data: factory_bot, fixtures, determinism

How to build the least data that makes a test readable and correct. Applies to
both frameworks. The governing smell to avoid is the **mystery guest**: data the
test depends on but does not show, so the reader cannot connect setup to
assertion.

## The four factory_bot strategies (the "fast tests" lever)

Default to the cheapest strategy that still exercises what you are testing.
`build_stubbed` > `build` > `create` in cost.

- **`build(:user)`**: `.new`, **not saved**. No DB write for the record itself.
  Gotcha: **`build` still `create`s its associations** (`build(:comment)` hits the
  DB for the associated `post`) unless you override them. Fires `after(:build)`.
- **`create(:user)`**: builds then `save!`s. Associations created. Fires
  `after(:build)`, `before(:create)`, `after(:create)`. Slowest. Use only when
  the code must round-trip the DB: a query/scope, `reload`, a DB-level constraint,
  or a callback that hits the DB.
- **`build_stubbed(:user)`**: assigns attributes like `build`, returns a
  fake-persisted object: sequential `id` / timestamps, `persisted? == true`,
  clears dirty tracking, associations also stubbed (no DB), and **raises if you
  call `save` / `update` / `destroy`**. Fastest, and doubles as a guard against
  accidental writes. Ideal for view/presenter specs and pure logic. Caveat: it
  defines singleton methods, so a stubbed object cannot be `Marshal.dump`ed.
- **`attributes_for(:user)`**: a Hash of attributes (associations **not** built).
  Ideal for controller/request params.

thoughtbot's guidance: default to `build_stubbed`; reach for `create` only when
persistence is genuinely required
(https://thoughtbot.com/blog/use-factory-bots-build-stubbed-for-a-faster-test).

## Writing factories: minimal, valid, trait-driven

```ruby
FactoryBot.define do
  factory :user do
    sequence(:email) { |n| "user#{n}@example.com" }  # unique values, no collisions
    name { "Test User" }

    trait :admin     { role { "admin" } }
    trait :confirmed { confirmed_at { Time.current } }

    transient { posts_count { 0 } }                   # config, not an attribute

    # opt-in association creation only when asked (keeps the base factory cheap)
    after(:create) do |user, evaluator|
      create_list(:post, evaluator.posts_count, author: user)
    end

    factory :admin_user, traits: [:admin]             # nested factory
  end
end
```

- **Keep the base factory to the minimum attributes needed for validity.** A
  bloated factory couples every test to fields it doesn't care about and slows
  every `create`. Push all variation into **traits** (`create(:user, :admin, :confirmed)`),
  which are orthogonal, composable, and work with every strategy.
- **Sequences** for unique fields (email, username) so validations don't collide.
- **Transient attributes** pass config into callbacks/associations without being
  model attributes (`evaluator.posts_count`).
- **Avoid `after(:create)` callbacks that always build associations.** They make
  `create` expensive and surprising and are the #1 cause of slow factory suites.
  Prefer traits + explicit `create_list` in the test, or an opt-in transient count.
- **Do not put business logic or scenarios in factories.** Factories build valid
  data; the test builds the scenario.

Specify only the attributes the test is about, so intent is visible:
`create(:user, :admin)` reads as "an admin"; the flag is the thing under test.

## Linting factories

`FactoryBot.lint` builds every factory (and every trait with `traits: true`) and
raises if any is invalid: it catches factories that rotted after a schema or
validation change. Run it as a **rake task in CI**, not in `before(:suite)`
(linting creates records and would slow every run). Clean up after:

```ruby
# lib/tasks/factory_bot.rake
task lint_factories: :environment do
  DatabaseCleaner.cleaning { FactoryBot.lint(traits: true) }  # or wrap in a rolled-back transaction
end
```

## Fixtures (Rails default; first-class with Minitest)

See minitest.md for the mechanics (labels, hashed ids, `fixtures :all`, ERB, the
load-once + per-test-transaction performance model). The essentials that affect
data design:

- Reference associations by **label**, never id (`author: david`).
- Keep the shared set **small and stable** (a handful of canonical records). A
  large shared fixture set is exactly the mystery guest at scale: a test relies on
  `users(:david)` having some property defined far away.
- Fixtures can bypass validations, so they can persist a state your model would
  reject. Be deliberate about that.

## Fixtures vs factories: the real tradeoff

| Dimension | Fixtures | factory_bot |
| --- | --- | --- |
| Speed | Loaded once; fastest raw load | Per-test creation; slower unless `build` / `build_stubbed` |
| Validity | Can persist invalid rows (bypass validations) | Records pass validations; can't silently create invalid state |
| Locality | Data lives far from the test (mystery guest) | Each test declares the state it needs |
| Maintenance | One shared dataset; edits ripple | Traits express variation without duplication |

- **RSpec community leans factories** (readability, per-test intent). thoughtbot,
  the RSpec Style Guide, and Everyday Rails all default to factory_bot.
- **Rails core / DHH lean fixtures + Minitest** for raw speed ("fast tests"): no
  per-test object graph, no accidental record explosions.
- **Pragmatic synthesis:** use **both**. Fixtures (or a tiny factory set) for a
  small, truly-global reference set (countries, plans, feature flags); factories
  for everything test-specific. If a factory suite gets slow, `build_stubbed`
  recovers most of the fixture speed advantage without the maintainability cost.
  Above all, **match what the codebase already uses.**

## Faker and determinism (a real flakiness source)

Faker generates realistic values but is **non-deterministic unless seeded**, and
**Faker does not honor Ruby's global `srand` seed**: seed it separately so a red
run is replayable.

```ruby
# RSpec: spec_helper.rb
config.before(:suite) do
  seed = RSpec.configuration.seed
  Kernel.srand(seed)
  Faker::Config.random = Random.new(seed)   # Faker has its own PRNG
end
```

- Prefer **sequences** over `Faker.unique` for uniqueness. `Faker.unique` breaks
  determinism for subsequent values and can exhaust its retry space.
- Do not use `db/seeds.rb` data in tests; tests build their own data, or you
  reintroduce the mystery guest.

Sources: https://github.com/thoughtbot/factory_bot/blob/main/GETTING_STARTED.md,
https://thoughtbot.com/blog/mystery-guest,
https://island94.org/2019/11/deterministic-test-data-with-faker-factorybot-and-rspec,
https://semaphore.io/blog/2014/01/14/rails-testing-antipatterns-fixtures-and-factories.html.
