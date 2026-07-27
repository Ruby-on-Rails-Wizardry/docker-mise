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

<!-- Pin bumps: "Pin flavors to vX.Y.Z". -->

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
