# Release process (umbrella)

How to cut a **coordinated** release of the mise base images under **docker-mise**.

Default branch is **`master`**. Default remote is **`github`** (not `origin`); **`gitlab`** is the backup mirror.

**Flavors are the product.** Each of ubuntu-mise, alpine-mise, and arch-mise gets its own tag, CHANGELOG section, and **required** GitHub Release. This umbrella **pins submodule SHAs** after the flavors ship. Umbrella tags are **optional** (not required for “done”).

A coordinated release is **not done** until:

1. Each shipped flavor has tag **`vX.Y.Z`** and a GitHub Release, and
2. This umbrella has committed and dual-pushed the submodule pins.

## Agent / human trigger phrases

When the user says any of the following, run this process **end-to-end** (do not stop after commit or push alone):

| Phrase | Action |
|--------|--------|
| **send it** | Coordinated release checklist below |
| **ship it** | Same |
| **cut a release** | Same |
| **maintain** / **sync** / **refresh docs** | [MAINTAINING.md](../MAINTAINING.md) only — no version unless you also cut a release |

```text
ubuntu verify → sync alpine/arch → verify each
  → changelog (same X.Y.Z) → commit each flavor
  → tag vX.Y.Z each → dual-push each
  → gh release create ×3 → pin umbrella → dual-push umbrella
```

## What ships where

| Repo | Role in a release |
|------|-------------------|
| **ubuntu-mise** | Develop shared host UX first; release first among flavors |
| **alpine-mise** / **arch-mise** | Same version when shared surface changes |
| **docker-mise** (this repo) | Bump submodule pins; dual-push; optional umbrella CHANGELOG |

Per-flavor checklists: each flavor’s [docs/RELEASE.md](https://github.com/Ruby-on-Rails-Wizardry/ubuntu-mise/blob/master/docs/RELEASE.md) (same shape in alpine/arch).

## Semver (shared host UX)

| Bump | Examples |
|------|----------|
| **MAJOR** | Rename/remove `bin/*` or Task names; break `/cache` or compose contract |
| **MINOR** | New tasks/bin; additive cache dirs; new shells; additive knobs |
| **PATCH** | Bugfixes; `MISE_VERSION`; package refresh; docs of existing behavior |

Use the **same** `X.Y.Z` on all three flavors for shared changes. OS-only Dockerfile fixes may skew one flavor; document that in the umbrella pin commit message.

## Preconditions

- [ ] Working trees clean in umbrella and each flavor you will ship
- [ ] On `master` everywhere (or intentionally ahead)
- [ ] Flavor remotes: `./bin/setup-remotes` inside each submodule
- [ ] Umbrella remotes: `github` + `gitlab`
- [ ] [`gh`](https://cli.github.com/) authenticated for `Ruby-on-Rails-Wizardry/*`
- [ ] `[Unreleased]` in each shipping flavor’s CHANGELOG reflects what ships

## Coordinated checklist

### 1. Stabilize ubuntu

```bash
cd ubuntu-mise
./bin/setup-remotes
task build && task verify && task doctor
```

### 2. Sync siblings

Copy/sync shared surface from ubuntu to alpine and arch:

- `bin/*` (logic)
- `Taskfile.yml` task names / patterns
- shared `docker/` scripts where applicable
- README / AGENTS / RELEASE / CHANGELOG structure (OS name and URLs differ)

Leave Dockerfile base image and package manager OS-specific.

### 3. Verify alpine and arch

```bash
cd alpine-mise && task build && task verify
cd arch-mise && task build && task verify
```

(Skip a flavor only if you cannot build it and the change is documented as not shipping there.)

### 4. Changelog + version section (each flavor)

In each shipping flavor’s `CHANGELOG.md`:

1. Move `[Unreleased]` bullets into `## [X.Y.Z] - YYYY-MM-DD`
2. Restore empty `[Unreleased]` stubs
3. Update footer compare links

Use the **same** `X.Y.Z` when the change set is shared.

### 5. Commit + tag + dual-push each flavor

For each of `ubuntu-mise`, `alpine-mise`, `arch-mise` (order: ubuntu → alpine → arch):

```bash
cd <flavor>
git add -A
git status
git commit -m "Release X.Y.Z

<summary>"
git tag -a vX.Y.Z -m "vX.Y.Z — short summary"
git push github master
git push github vX.Y.Z
git push gitlab master
git push gitlab vX.Y.Z
```

### 6. GitHub Release each flavor (**required**)

```bash
# replace FLAVOR and X.Y.Z
cd <flavor>
awk '/^## \[X.Y.Z\]/{flag=1; next} /^## \[/{flag=0} flag' CHANGELOG.md > /tmp/release-notes.md

gh release create vX.Y.Z \
  --repo Ruby-on-Rails-Wizardry/<flavor> \
  --title "vX.Y.Z" \
  --notes-file /tmp/release-notes.md \
  --verify-tag

gh release view vX.Y.Z --repo Ruby-on-Rails-Wizardry/<flavor>
```

Repos: `ubuntu-mise`, `alpine-mise`, `arch-mise`.

### 7. Pin umbrella

From the docker-mise root:

```bash
# record the commits (or tags) you just shipped
git -C ubuntu-mise rev-parse HEAD
git -C alpine-mise rev-parse HEAD
git -C arch-mise rev-parse HEAD

git add ubuntu-mise alpine-mise arch-mise
```

Optionally update this repo’s [CHANGELOG.md](../CHANGELOG.md):

```markdown
## [Unreleased] → or a dated note under Unreleased
### Changed
- Pin ubuntu-mise, alpine-mise, arch-mise to vX.Y.Z
```

```bash
git commit -m "Bump base image submodule pins to vX.Y.Z

Coordinated flavor release; GitHub Releases on each flavor."
git push github master
git push gitlab master
```

### 8. Optional umbrella tag

Umbrella tags are **not** required. Add only if consumers want a single `docker-mise` handle:

```bash
git tag -a vX.Y.Z -m "vX.Y.Z — pins flavors to vX.Y.Z"
git push github vX.Y.Z
git push gitlab vX.Y.Z
# optional: gh release create on docker-mise
```

### 9. Post-release

- [ ] `gh release list` shows `vX.Y.Z` on each shipped flavor
- [ ] Umbrella `git submodule status` matches intended SHAs
- [ ] New flavor work goes under `[Unreleased]` again

## Single-flavor (OS-only) release

If only one Dockerfile or OS package set changes:

1. Follow that flavor’s `docs/RELEASE.md` alone (patch version; may skew).
2. Still pin the umbrella to the new SHA and dual-push.
3. Note skew in the umbrella commit message.

## What not to ship

- Secrets, `.env`, `compose.override.yml`
- Shared-API drift across flavors without sync or documented OS-only exception
- Tags/pushes without `gh release create` on the flavor (release incomplete)
- Force-push of `master` or shared tags unless explicitly requested

## Maintain vs release

| Intent | Doc |
|--------|-----|
| Versioned shipping (tags + GitHub Releases + pins) | **this file** + flavor `docs/RELEASE.md` |
| Remotes, mirrors, rebuild hygiene, doc sync without a version | [MAINTAINING.md](../MAINTAINING.md) |

## Quick one-liner reminder

```text
verify → sync flavors → changelog → commit → tag → dual-push → gh release ×3 → pin umbrella → dual-push umbrella
```

(Also the definition of **send it** / **ship it** / **cut a release**.)
