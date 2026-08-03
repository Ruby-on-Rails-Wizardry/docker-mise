# Changelog

All notable changes to the **docker-mise** umbrella (submodule pins and umbrella docs) are documented in this file.

Flavor host UX and image changes are recorded in each flavor’s `CHANGELOG.md`:

- [ubuntu-mise](https://github.com/Ruby-on-Rails-Wizardry/ubuntu-mise/blob/master/CHANGELOG.md)
- [alpine-mise](https://github.com/Ruby-on-Rails-Wizardry/alpine-mise/blob/master/CHANGELOG.md)
- [arch-mise](https://github.com/Ruby-on-Rails-Wizardry/arch-mise/blob/master/CHANGELOG.md)
- [docker-mise-cluster](https://github.com/Ruby-on-Rails-Wizardry/docker-mise-cluster/blob/master/CHANGELOG.md) (`cluster/` submodule)

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Umbrella tags are optional; primary version tags live on the flavor repos. See [docs/RELEASE.md](docs/RELEASE.md).

## [Unreleased]

### Added

### Changed

### Fixed

### Security

## 2026-08-03 — pin flavors v0.8.0, cluster v0.7.0

### Changed

- Pin ubuntu-mise, alpine-mise, arch-mise to **v0.8.0** (`/docker/bin`, volume **`cache`**, build-only identity)
- Pin cluster to **v0.7.0** (four apps, single cache volume, `task warm`, compose.yml)


### Added

- Umbrella submodules **`ubuntu-sample`**, **`alpine-sample`**, **`arch-sample`** (Rails [sample_app](https://github.com/Ruby-on-Rails-Wizardry/sample_app); siblings of each `*-mise` flavor)

### Changed

- Flavors no longer nest `sample_app`; sibling samples mount via `PROJECT=…`
- Flavor compose is **dev-only** (no `app` service); **local image only** (`pull_policy: never`)

### Fixed

### Security

<!-- Pin bumps: "Pin flavors to vX.Y.Z". -->

## 2026-07-30 — pin flavors v0.7.0, cluster v0.6.0, samples

### Added

- Submodules **ubuntu-sample**, **alpine-sample**, **arch-sample** ([sample_app](https://github.com/Ruby-on-Rails-Wizardry/sample_app) host UX + dev/prod compose)

### Changed

- Pin [ubuntu-mise](ubuntu-mise/), [alpine-mise](alpine-mise/), [arch-mise](arch-mise/) to **v0.7.0** (sample out of flavor; local-only compose; flavor service/hostname)
- Pin [cluster](cluster/) to **v0.6.0** (prebuilt ubuntu-mise:dev for fred/george; multi-app mise/Task)
- Pin fred/george (via cluster) to host UX matching ubuntu-sample


## 2026-07-29 — pin flavors to v0.6.0

### Changed

- Pin [ubuntu-mise](ubuntu-mise/), [alpine-mise](alpine-mise/), and [arch-mise](arch-mise/) to **v0.6.0** (mise host UX / Taskfile mirrors, `.mise.env` PG 18 default; Alpine falls back to apk PG 17 when 18 missing)

## 2026-07-29 — pin ubuntu-mise v0.5.2

### Changed

- Pin [ubuntu-mise](ubuntu-mise/) to **v0.5.2** (libjemalloc/font/image/sqlite packages; postgresql setup early; apt upgrade before USER)

## Added

### Changed

### Fixed

### Security

<!-- Pin bumps: "Pin flavors to vX.Y.Z". -->

## 2026-07-29 — harden rebase-local-tree

### Changed

- [bin/rebase-local-tree](bin/rebase-local-tree): WIP **cache commit** on dirty trees; **interactive conflict resolution** (pause on conflicts: c/a/s/q); continue-on-error summary; fetch retry; `--no-cache-commit` / `--non-interactive` / `--fail-fast`
- [docs/CLONE-HTTPS.md](docs/CLONE-HTTPS.md): document cache-commit, conflict prompts, and fail-fast behavior

## 2026-07-29 — pin flavors to v0.5.1

### Changed

- Pin [ubuntu-mise](ubuntu-mise/), [alpine-mise](alpine-mise/), [arch-mise](arch-mise/) to **v0.5.1** (compose creates named cache volume when missing)

## 2026-07-29 — pin flavors + cluster v0.5.0

### Changed

- Pin [ubuntu-mise](ubuntu-mise/), [alpine-mise](alpine-mise/), [arch-mise](arch-mise/) to **v0.5.0** (home/ seed, ~/bin runtime tools, optional PG, host shell/TZ/matrix, compose hostnames)
- Pin [cluster/](cluster/) to **v0.5.0** (docker/ layout, host TZ, compose hostnames)

### Added

- Note production topology: Kamal per app (fred/george) on one host; cluster compose is dev-only ([AGENTS.md](AGENTS.md), [cluster/AGENTS.md](cluster/AGENTS.md#production-deployment-kamal--not-compose))

### Changed

- Document supported host matrix for flavor UX: native Linux, native macOS, Windows+WSL (project inside WSL); not native Windows ([AGENTS.md](AGENTS.md))

### Fixed

### Security

<!-- Pin bumps: "Pin flavors to vX.Y.Z". -->

## 2026-07-27 — pin cluster v0.3.1

### Changed

- Pin [cluster/](cluster/) to **v0.3.1** (`bin/db-reset` / Task DB reset shorthands; runtime mise install into `/cache`)

## 2026-07-27 — pin cluster v0.3.0

### Changed

- Pin [cluster/](cluster/) to **v0.3.0** (ubuntu-mise base image + project mount at `/work`)

## 2026-07-27 — pin v0.4.3 / cluster v0.2.1

### Added

- [docs/CLONE-HTTPS.md](docs/CLONE-HTTPS.md) — keep SSH remotes/`.gitmodules` canonical; HTTPS-only contexts use git `url.*.insteadOf` (nested submodules included); site-local **`local`** branch rebased onto **`master`** for proxy/CA image overrides
- [bin/rebase-local-tree](bin/rebase-local-tree) — recursive fetch-`master` + rebase-`local` for the full nested submodule tree (HTTPS site helper)
- Root [Taskfile.yml](Taskfile.yml) + [mise.toml](mise.toml) pin **Task 3.52.0**; includes flavor/cluster Taskfiles (`task ubuntu:…`, `task cluster:up -- fred`, …)

### Changed

- Pin ubuntu-mise, alpine-mise, arch-mise to **v0.4.3**
- Pin [cluster/](cluster/) to **v0.2.1**
- Expand umbrella and `bench/results` `.gitignore` Vim artifact coverage

### Fixed

## 2026-07-27 — pin v0.4.2 / cluster v0.2.0

### Added

- [bench/](bench/) cold/warm Rails bring-up speed harness (`bin/run-speed-tests`) and [SPEED.md](bench/SPEED.md)
- Submodule [cluster/](cluster/) → [docker-mise-cluster](https://github.com/Ruby-on-Rails-Wizardry/docker-mise-cluster) **v0.2.0** (Postgres/Redis, nginx path proxy, one-app compose up)
- Ignore local [partial/](partial/) reference tree in `.gitignore`

### Changed

- Pin ubuntu-mise, alpine-mise, arch-mise to **v0.4.2**
- Pin cluster to **v0.2.0**

## 2026-07-23 — pin v0.3.0

### Changed

- Pin ubuntu-mise, alpine-mise, arch-mise to **v0.3.0** (sample_app submodule, compose `app` service, warm language-version files)

## 2026-07-17 — pin v0.2.0
## 2026-07-17 — pin v0.2.0

### Changed

- Pin ubuntu-mise, alpine-mise, arch-mise to **v0.2.0** (sample setup, compile toolchain, shell TTY, mise trust, shared-cache bundle clean policy)

## 2026-07-17 — pin v0.1.0

### Added

- Documented coordinated release process in [docs/RELEASE.md](docs/RELEASE.md)
- Umbrella changelog for pin bumps and umbrella-only notes
- Cross-links from [MAINTAINING.md](MAINTAINING.md) (maintain vs release)

### Changed

- Pin ubuntu-mise, alpine-mise, arch-mise to **v0.1.0**

[Unreleased]: https://github.com/Ruby-on-Rails-Wizardry/docker-mise/compare/master...HEAD
