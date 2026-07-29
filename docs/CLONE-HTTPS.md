# SSH remotes here, HTTPS in another context

Canonical remotes and `.gitmodules` in this tree use **SSH** (`git@github.com:…`, `git@gitlab.com:…`). That stays the source of truth for development on machines with SSH keys.

Some environments cannot use SSH (policy, CI, locked-down hosts). In those contexts, keep **the same clone layout and submodule pins**, but rewrite SSH URLs to **HTTPS at git-config level** so you do not thrash `.gitmodules` or dual-commit URL strings.

## Nested tree (what gets rewritten)

```text
docker-mise                 # umbrella
├── ubuntu-mise / alpine-mise / arch-mise
└── cluster/                # docker-mise-cluster
    ├── fred/
    └── george/
```

One `url.*.insteadOf` config covers **all levels** of submodule URLs.

## Recommended: rewrite only where HTTPS is required

On the **HTTPS-only** machine or user account (**not** on your normal SSH workstation), set:

```bash
# Use --add so multiple insteadOf values stack (plain git config overwrites the same key).

# GitHub (scp-style and ssh:// URLs)
git config --global --add url."https://github.com/".insteadOf "git@github.com:"
git config --global --add url."https://github.com/".insteadOf "ssh://git@github.com/"

# GitLab backup mirrors (separate url.* key — does not replace GitHub)
git config --global --add url."https://gitlab.com/".insteadOf "git@gitlab.com:"
git config --global --add url."https://gitlab.com/".insteadOf "ssh://git@gitlab.com/"
```

| Stored in repo / `.gitmodules` | What that context uses |
|--------------------------------|------------------------|
| `git@github.com:Org/repo.git` | `https://github.com/Org/repo.git` |
| `git@gitlab.com:group/repo.git` | `https://gitlab.com/group/repo.git` |

Do **not** add these rewrites on the SSH workstation, or every clone there will suddenly speak HTTPS.

### Why `--add` (and why GitHub + GitLab both work)

Git stores these as **multi-valued** keys under different sections:

```ini
[url "https://github.com/"]
	insteadOf = git@github.com:
	insteadOf = ssh://git@github.com/
[url "https://gitlab.com/"]
	insteadOf = git@gitlab.com:
	insteadOf = ssh://git@gitlab.com/
```

- **GitHub vs GitLab** use different `url."<base>".insteadOf` keys (`https://github.com/` vs `https://gitlab.com/`). Setting both hosts is fine; neither replaces the other.
- **Two patterns for one host** (e.g. `git@github.com:` and `ssh://git@github.com/`) share the **same** key. A second `git config` **without** `--add` replaces the first value. Always use `--add` when stacking.

Verify:

```bash
git config --global --get-regexp '^url\..*\.insteadof$'
# expect four lines if you set both hosts and both URL shapes
```

Reset and re-apply if you overwrote something:

```bash
git config --global --unset-all url."https://github.com/".insteadOf
git config --global --unset-all url."https://gitlab.com/".insteadOf
# then re-run the four --add lines above
```

Or edit `~/.gitconfig` by hand into the multi-`insteadOf` form shown above.

### Auth (HTTPS context)

1. GitHub: `gh auth login` (HTTPS) and/or a credential helper + PAT with `repo` scope  
2. GitLab: `glab auth login` or PAT  
3. Smoke test:

```bash
git ls-remote https://github.com/Ruby-on-Rails-Wizardry/docker-mise.git HEAD
```

## Both contexts on one machine

Use path-scoped config so only the restricted checkout rewrites:

```ini
# ~/.gitconfig
[includeIf "gitdir:~/work-https/"]
  path = ~/.gitconfig-https
```

```ini
# ~/.gitconfig-https
[url "https://github.com/"]
  insteadOf = git@github.com:
  insteadOf = ssh://git@github.com/
[url "https://gitlab.com/"]
  insteadOf = git@gitlab.com:
  insteadOf = ssh://git@gitlab.com/
```

- SSH worktree: e.g. `~/Ruby-on-Rails-Wizardry/docker-mise`  
- HTTPS worktree: e.g. `~/work-https/docker-mise`  

## Clone (HTTPS context)

Either form works once `insteadOf` is set; HTTPS clone URL is fine too:

```bash
git clone --recurse-submodules -b master \
  https://github.com/Ruby-on-Rails-Wizardry/docker-mise.git
cd docker-mise
```

If the clone was done without submodules:

```bash
git submodule update --init --recursive
```

Standalone cluster:

```bash
git clone --recurse-submodules -b master \
  https://github.com/Ruby-on-Rails-Wizardry/docker-mise-cluster.git
```

## Keeping the HTTPS context up to date

Shared product work lives on **`master`** (push from the SSH context). The HTTPS clone should **track `master`**, not rewrite it.

If that environment needs **site-local edits** (for example corporate base images that inject proxy/CA certs into `FROM` lines), keep those on a branch named **`local`** and **rebase** it onto updated `master`. Do **not** merge `local` into public `master` or dual-commit proxy bits into the shared repos.

### A. Read-only sync (no local patches)

```bash
cd /path/to/https-clone/docker-mise
git fetch --all --tags --prune
git checkout master
git pull --ff-only
git submodule sync --recursive          # after upstream .gitmodules changes
git submodule update --init --recursive
```

### B. Site-local branch `local` (proxy / cert base images, etc.)

#### Layout of branches

| Repo | `master` | `local` |
|------|----------|---------|
| **docker-mise** (umbrella) | tracks GitHub | optional: pin bumps after submodule rebases, umbrella-only tweaks |
| **ubuntu-mise** / **alpine-mise** / **arch-mise** | tracks GitHub | Dockerfile / image `FROM` (and similar) for proxy+CA images |
| **cluster** | tracks GitHub | same, if the cluster `Dockerfile` needs a different base |
| **fred** / **george** | tracks GitHub | usually untouched |

One-time setup (HTTPS clone, after `insteadOf` + auth):

```bash
cd /path/to/https-clone/docker-mise
git checkout master && git pull --ff-only
git submodule update --init --recursive

# Create local only where you will patch (example: flavors + cluster)
for d in . ubuntu-mise alpine-mise arch-mise cluster; do
  (
    cd "$d"
    git fetch origin master 2>/dev/null || git fetch github master
    git checkout master
    git pull --ff-only
    git checkout -B local master    # or: git checkout -b local
  )
done
```

Make your site-local commits **only on `local`** (small, focused commits rebase more cleanly).

#### Recurring: use `bin/rebase-local-tree`

From the **umbrella** checkout (HTTPS machine):

```bash
cd /path/to/https-clone/docker-mise
bin/rebase-local-tree              # fetch master, rebase each `local`, pin bumps
bin/rebase-local-tree --dry-run    # show plan only
# Dirty trees: auto WIP "local-cache:" commit before checkout/rebase (override: --no-cache-commit)
# Conflicts: script pauses (TTY) so you can edit/add files, then [c]ontinue / [a]bort / [s]kip / [q]uit
# Non-TTY or CI: --non-interactive (record fail, leave mid-rebase for manual fix)
# Per-repo errors: continue and summarize (stop early: --fail-fast)
```

The script walks the **entire nested submodule tree** depth-first (e.g. `cluster/fred` before `cluster` before `.`):

1. Fetch + fast-forward `master`  
2. If branch `local` exists → `git rebase master`  
3. On repos that have `local` and `.gitmodules`, auto-commit submodule pin bumps when SHAs moved  

| Flag | Meaning |
|------|---------|
| `--dry-run` | Print actions only |
| `--no-commit` | Rebase but do not commit pin bumps |
| `--no-cache-commit` | Fail on dirty worktrees instead of WIP cache commits |
| `--non-interactive` | Do not prompt on conflicts (leave mid-rebase; continue tree) |
| `--fail-fast` | Stop on first repo error |
| `--create-local` | Create `local` from `master` on umbrella + top-level children if missing |
| `--all-create` | Create `local` in every repo (including nested apps) |
| `--branch NAME` | Site branch (default `local`) |
| `--master NAME` | Upstream branch (default `master`) |

### Conflict during rebase

**Interactive terminal (default):** the script **pauses**, lists unmerged paths, and waits:

| Key | Action |
|-----|--------|
| **c** | After you edit + `git add`, run `git rebase --continue` |
| **a** | `git rebase --abort` for this repo |
| **s** | Leave mid-rebase; continue other repos |
| **q** | Exit the whole tree walk |

```bash
# In another terminal (or after the prompt):
cd path/to/repo
# fix conflict markers
git add path/to/fixed-file
# back at the script prompt: c
```

**Non-TTY / CI** (`--non-interactive`): conflicts are left mid-rebase; fix and re-run:

```bash
git -C path/to/repo add …
git -C path/to/repo rebase --continue
# or: git -C path/to/repo rebase --abort
bin/rebase-local-tree
```

Does **not** push. Do not push `local` to public `master`; use a private remote if you need a backup of site commits.

#### Tips so rebases stay easy

| Do | Avoid |
|----|--------|
| Tiny commits only on `local` (e.g. one commit: “use corp base images”) | Mixing product features into `local` |
| Prefer a single `ARG`/`FROM` override or a thin wrapper Dockerfile if possible | Large copy-paste diffs against upstream Dockerfiles |
| Rebase often (weekly) | Letting `local` diverge for months |
| Keep `local` **unpushed** to public `master`, or push only to a **private** remote | `git push origin local:master` |

Backup of the site branch (optional private remote):

```bash
git remote add private https://gitlab.example.com/you/docker-mise-local.git   # once
git push -u private local
```

### C. Minimal pull helper (master only)

```bash
#!/usr/bin/env bash
# Pull umbrella master + nested submodules (no local branch).
set -euo pipefail
git fetch github --tags --prune 2>/dev/null || git fetch origin --tags --prune
git checkout master
git pull --ff-only
git submodule sync --recursive
git submodule update --init --recursive
```

## Patterns to avoid

| Approach | Why it hurts this tree |
|----------|-------------------------|
| Committing `.gitmodules` flips SSH ↔ HTTPS | Constant churn; two contexts fight on every pull |
| Dual URL remotes on every submodule “just in case” | Noise; still need rewrite or careful clone flags |
| Editing remote URLs by hand in each nested repo | Easy to miss `cluster` → `fred` / `george` |
| Committing proxy/CA base-image changes on public **`master`** | Leaks site policy into the product; breaks SSH workstations |
| Merging `master` into `local` forever (no rebase) | History becomes a tangle of “merge master” noise; harder to see real local patches |

## Related

- Umbrella clone / remotes: [README.md](../README.md)  
- Dual-push / mirrors: [MAINTAINING.md](../MAINTAINING.md)  
- Cluster apps as submodules: [cluster/README.md](../cluster/README.md) (after `git submodule update --init`)  
