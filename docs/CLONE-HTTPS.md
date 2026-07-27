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
# GitHub
git config --global url."https://github.com/".insteadOf "git@github.com:"
git config --global url."https://github.com/".insteadOf "ssh://git@github.com/"

# GitLab (backup mirrors)
git config --global url."https://gitlab.com/".insteadOf "git@gitlab.com:"
git config --global url."https://gitlab.com/".insteadOf "ssh://git@gitlab.com/"
```

| Stored in repo / `.gitmodules` | What that context uses |
|--------------------------------|------------------------|
| `git@github.com:Org/repo.git` | `https://github.com/Org/repo.git` |
| `git@gitlab.com:group/repo.git` | `https://gitlab.com/group/repo.git` |

Do **not** add these rewrites on the SSH workstation, or every clone there will suddenly speak HTTPS.

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

Develop and push from the **SSH** context. On the HTTPS side, mostly **pull**:

```bash
cd /path/to/https-clone/docker-mise
git fetch --all --tags --prune
git checkout master
git pull --ff-only
git submodule sync --recursive          # after upstream .gitmodules changes
git submodule update --init --recursive
```

Optional helper (save as `bin/sync-from-upstream` on that machine only):

```bash
#!/usr/bin/env bash
# Pull umbrella master + nested submodules (fred/george under cluster included).
set -euo pipefail
git fetch github --tags --prune 2>/dev/null || git fetch origin --tags --prune
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

## Related

- Umbrella clone / remotes: [README.md](../README.md)  
- Dual-push / mirrors: [MAINTAINING.md](../MAINTAINING.md)  
- Cluster apps as submodules: [cluster/README.md](../cluster/README.md) (after `git submodule update --init`)  
