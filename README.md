# docker-mise

Umbrella repo for **mise** development base images. Each OS flavor is a **git submodule** (default remote: **GitHub**; GitLab is a backup mirror on each flavor).

| Submodule | GitHub (default) | Purpose |
|-----------|------------------|---------|
| [ubuntu-mise](https://github.com/Ruby-on-Rails-Wizardry/ubuntu-mise) | `git@github.com:Ruby-on-Rails-Wizardry/ubuntu-mise.git` | Ubuntu 24.04 + mise + `/cache` |
| [alpine-mise](https://github.com/Ruby-on-Rails-Wizardry/alpine-mise) | `git@github.com:Ruby-on-Rails-Wizardry/alpine-mise.git` | Alpine + mise + `/cache` |
| [arch-mise](https://github.com/Ruby-on-Rails-Wizardry/arch-mise) | `git@github.com:Ruby-on-Rails-Wizardry/arch-mise.git` | Arch + mise + `/cache` |
| [cluster](https://github.com/Ruby-on-Rails-Wizardry/docker-mise-cluster) | `git@github.com:Ruby-on-Rails-Wizardry/docker-mise-cluster.git` | Multi-app Rails cluster template + nginx path proxy |

## Clone this umbrella

```bash
git clone --recurse-submodules -b master \
  git@github.com:Ruby-on-Rails-Wizardry/docker-mise.git
cd docker-mise
```

If you already cloned without submodules:

```bash
git submodule update --init --recursive
```

Canonical remotes and `.gitmodules` use **SSH**. For a second machine or policy that **must use HTTPS**, keep SSH in the repos and rewrite URLs only there — see **[docs/CLONE-HTTPS.md](docs/CLONE-HTTPS.md)**.

## Use a base image

```bash
cd ubuntu-mise   # or alpine-mise / arch-mise
task setup && task shell
# or: ./bin/setup && ./bin/shell
```

See each submodule’s `README.md` for Task / Compose / cache details.

## Multi-app cluster template

```bash
cd cluster
bin/setup --docker-build
bin/compose up
# http://localhost:8080/  → home; /fred/ and /george/ via nginx
```

See [cluster/README.md](cluster/README.md).

## Remotes (this umbrella)

| Name | Role | URL |
|------|------|-----|
| **github** | default | `git@github.com:Ruby-on-Rails-Wizardry/docker-mise.git` |
| **gitlab** | backup | `git@gitlab.com:ruby-on-rails-wizardry/docker-mise.git` |

```bash
git remote -v
git push github master
git push gitlab master
```

Flavor repos also use **github** (default) + **gitlab** (backup). After cloning a submodule, run `./bin/setup-remotes` inside it (submodule checkout often only has `origin`).

## Maintaining

For periodic upkeep (rebuilds, doc sync across flavors, dual-push, submodule pins), see **[MAINTAINING.md](./MAINTAINING.md)** and each flavor’s `AGENTS.md` maintainer section.

SSH vs HTTPS dual context (same tree, different network policy): **[docs/CLONE-HTTPS.md](docs/CLONE-HTTPS.md)**.

## Releases

Versioned shipping (coordinated flavor tags + GitHub Releases + umbrella pins): **[docs/RELEASE.md](./docs/RELEASE.md)**.  
History: [CHANGELOG.md](./CHANGELOG.md) (umbrella); each flavor has its own changelog.

Agent/human shortcuts: **send it**, **ship it**, or **cut a release** mean run that process end-to-end.

## Agent notes

See [AGENTS.md](./AGENTS.md). Follow [MAINTAINING.md](./MAINTAINING.md) for maintenance; [docs/RELEASE.md](./docs/RELEASE.md) for releases.
