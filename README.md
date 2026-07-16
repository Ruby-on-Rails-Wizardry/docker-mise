# docker-mise

Umbrella repo for **mise** development base images. Each OS flavor is a **git submodule** (default remote: **GitHub**; GitLab is a backup mirror on each flavor).

| Submodule | GitHub (default) | Purpose |
|-----------|------------------|---------|
| [ubuntu-mise](https://github.com/Ruby-on-Rails-Wizardry/ubuntu-mise) | `git@github.com:Ruby-on-Rails-Wizardry/ubuntu-mise.git` | Ubuntu 24.04 + mise + `/cache` |
| [alpine-mise](https://github.com/Ruby-on-Rails-Wizardry/alpine-mise) | `git@github.com:Ruby-on-Rails-Wizardry/alpine-mise.git` | Alpine + mise + `/cache` |
| [arch-mise](https://github.com/Ruby-on-Rails-Wizardry/arch-mise) | `git@github.com:Ruby-on-Rails-Wizardry/arch-mise.git` | Arch + mise + `/cache` |

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

## Use a base image

```bash
cd ubuntu-mise   # or alpine-mise / arch-mise
task setup && task shell
# or: ./bin/setup && ./bin/shell
```

See each submodule’s `README.md` for Task / Compose / cache details.

## Remotes (this umbrella)

| Name | Role | URL |
|------|------|-----|
| **github** | default | `git@github.com:Ruby-on-Rails-Wizardry/docker-mise.git` |

```bash
git remote -v
git push -u github master
```

Flavor repos also have a **gitlab** backup remote; run `./bin/setup-remotes` inside a submodule after cloning.

## Agent notes

See [AGENTS.md](./AGENTS.md).
