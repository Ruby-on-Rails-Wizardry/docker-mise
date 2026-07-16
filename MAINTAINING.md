# Maintaining docker-mise and base images

Notes for **humans and agents** who periodically keep these repos healthy.
Default remote is **`github`**; **`gitlab`** is backup on every repo.

## Repos

| Repo | Role | GitHub | GitLab |
|------|------|--------|--------|
| **docker-mise** | Umbrella (submodule pins) | `Ruby-on-Rails-Wizardry/docker-mise` | `ruby-on-rails-wizardry/docker-mise` |
| **ubuntu-mise** | Ubuntu base image | `…/ubuntu-mise` | `…/ubuntu-mise` |
| **alpine-mise** | Alpine base image | `…/alpine-mise` | `…/alpine-mise` |
| **arch-mise** | Arch base image | `…/arch-mise` | `…/arch-mise` |

Branch: **`master`** everywhere.

## Cadence (suggested)

| When | What |
|------|------|
| **Monthly** (or after host OS/tool churn) | Rebuild images, `task verify`, bump `MISE_VERSION` if needed |
| **After any flavor host-UX change** | Edit **ubuntu-mise** first → sync to alpine/arch → push flavors → bump umbrella submodule SHAs |
| **After doc-only changes** | Keep README + AGENTS in sync across flavors; dual-push |
| **Quarterly** | Confirm GitHub/GitLab mirrors match; re-run `./bin/setup-remotes` in each clone |

## Golden rule: three flavors stay API-identical

Shared surface (must match names and behavior):

- `bin/*` (including `setup-remotes`, compose helpers)
- `Taskfile.yml` task names
- `compose.yml` shape (image/volume names differ by flavor)
- `/cache` layout and env vars
- README/AGENTS structure (OS name and URLs differ)

**Workflow for shared changes:**

1. Implement and test in **`ubuntu-mise`**.
2. Copy/sync scripts + docs to **alpine-mise** and **arch-mise** (only Dockerfile package manager / base image differ).
3. `task verify` (or `./bin/verify`) in each flavor you can build.
4. Commit + push each flavor (`github` + `gitlab`).
5. In **docker-mise** umbrella: `git submodule update --remote` (or set SHAs), commit, push both remotes.

## Periodic checklist (copy/paste)

### 1. Remotes and mirrors

```bash
# umbrella
cd docker-mise   # or this checkout
git fetch github gitlab
git status -sb
./ubuntu-mise/bin/setup-remotes   # if working inside a flavor clone
# each flavor:
for d in ubuntu-mise alpine-mise arch-mise; do
  (cd "$d" && ./bin/setup-remotes && git fetch github gitlab && git status -sb)
done
```

Confirm `master` matches on github and gitlab for every repo.

### 2. Docs still accurate

For **each** of umbrella + three flavors:

- [ ] `README.md` quick start still works (`task setup` / `bin/setup`)
- [ ] Compose path still documented as **parallel** (not replacing docker run)
- [ ] Submodule URL is **GitHub**; GitLab described as backup only
- [ ] `AGENTS.md` lists current locked decisions and verify commands
- [ ] No secrets, no committed `.env`

### 3. Image health

```bash
cd ubuntu-mise && task build && task verify && task doctor
# repeat for alpine-mise / arch-mise when practical
```

### 4. Publish

```bash
# inside a flavor
git push github master   # dual-push to GitLab if setup-remotes configured
git push gitlab master   # explicit backup if needed

# umbrella after submodule SHA bumps
git add ubuntu-mise alpine-mise arch-mise
git commit -m "Bump base image submodule pins"
git push github master
git push gitlab master
```

## Agent instructions (maintainers)

When asked to “maintain”, “sync”, “refresh docs”, or “check remotes”:

1. Read **this file** and the relevant `AGENTS.md`.
2. Prefer **Task** / **`bin/*`**; do not invent ad-hoc docker flags.
3. Do **not** rename remotes to `origin`; keep **`github`** / **`gitlab`**.
4. After submodule re-clone, run **`./bin/setup-remotes`** (submodule checkout often only has `origin`).
5. Never commit `.env` or `compose.override.yml`.
6. Dual-push flavors and umbrella when finishing a maintenance pass.
7. Summarize what was checked, what drifted, and what was pushed.

## What not to do

- Share one `/cache` Docker volume across Alpine and glibc images.
- Change only one flavor’s `bin/*` or Task API without syncing siblings.
- Point consumer submodule URLs at GitLab by default (GitHub is canonical for `git submodule add`).
- Force-push `master` on shared remotes unless explicitly requested.
