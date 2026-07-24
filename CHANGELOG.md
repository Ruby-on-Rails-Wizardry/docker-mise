# Changelog

All notable changes to the **docker-mise** umbrella (submodule pins and umbrella docs) are documented in this file.

Flavor host UX and image changes are recorded in each flavor’s `CHANGELOG.md`:

- [ubuntu-mise](https://github.com/Ruby-on-Rails-Wizardry/ubuntu-mise/blob/master/CHANGELOG.md)
- [alpine-mise](https://github.com/Ruby-on-Rails-Wizardry/alpine-mise/blob/master/CHANGELOG.md)
- [arch-mise](https://github.com/Ruby-on-Rails-Wizardry/arch-mise/blob/master/CHANGELOG.md)

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Umbrella tags are optional; primary version tags live on the flavor repos. See [docs/RELEASE.md](docs/RELEASE.md).

## [Unreleased]

### Added

- [bench/](bench/) cold/warm Rails bring-up speed harness (`bin/run-speed-tests`) and [SPEED.md](bench/SPEED.md)

### Changed

- Pin ubuntu-mise, alpine-mise, arch-mise to **v0.4.0**

### Fixed

### Security

<!-- Pin bumps: "Pin flavors to vX.Y.Z". -->

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
