# claude-plugins

A personal Claude Code plugin marketplace. Each plugin lives in `plugins/<name>/`
with a manifest at `plugins/<name>/.claude-plugin/plugin.json`, and every plugin
is listed in the root `.claude-plugin/marketplace.json`.

## Do not add a `version` field to plugin.json

**The omission is deliberate. Do not "fix" it by adding one back.**

`version` is optional, and it is not documentation. Claude Code uses it as the
**cache key for update detection**. The two strategies are mutually exclusive:

| Strategy | Behavior |
| --- | --- |
| `version` **set** | Users receive changes **only** when you bump it. Pushing commits does nothing; `/plugin update` reports "already at the latest version". |
| `version` **omitted** | Claude Code falls back to the **git commit SHA**, so every commit is a new version. |

From the [plugins reference](https://code.claude.com/docs/en/plugins-reference#version-management):

> If you set `version` in `plugin.json`, you must bump it every time you want
> users to receive changes. Pushing new commits alone is not enough, because
> Claude Code sees the same version string and keeps the cached copy. If you're
> iterating quickly, leave `version` unset so the git commit SHA is used instead.

These plugins are iterated on continuously and have no release cycle, so
commit-SHA versioning is the correct fit.

**This repo already hit the failure mode**, which is why the field was removed.
`rails-testing` sat pinned at `0.1.0` while its content was edited across
multiple commits. The locally installed copy stayed a Jul 18 snapshot and never
refreshed, because the version string never changed. The bug is silent: nothing
errors, users simply keep reading stale skills.

If you ever do reintroduce explicit versions, you are committing to bumping on
**every** user-facing change, across all plugins, and the docs recommend adding
a `CHANGELOG.md` alongside.

One consequence to know: without `version`, a plugin's install directory name is
a version string that changes on every update. That only matters for a plugin
whose `SKILL.md` sits at the plugin root with no `name:` in its frontmatter,
since Claude Code would fall back to the directory name. Every skill here uses
the `skills/<name>/SKILL.md` layout with an explicit `name:`, so it does not
apply. Keep it that way.

## Updating a plugin's user-facing copy

A plugin is described in two places that must be kept in sync by hand:

- `plugins/<name>/.claude-plugin/plugin.json` -> `description`
- `.claude-plugin/marketplace.json` -> that plugin's `description`

The skill's own `description:` frontmatter is separate and more important: it is
what Claude reads to decide whether to load the skill, so it should describe
**triggering conditions**, not summarize the skill's workflow.

## Users do not get changes automatically

Even with SHA versioning, an installed plugin is a **copy** in
`~/.claude/plugins/cache/`, not a live view of this repo. Refreshing is manual:

```
/plugin marketplace update garyhtou
/reload-plugins
```

When testing a skill edit with subagents, remember they load the **installed
cache copy**, not your working tree. Point them at the file path in this repo
directly, or the test will silently validate stale content.
