# Speed bench

Repeatable cold/warm timing for Rails bring-up paths used with this umbrella.

## Scenarios

| Scenario | Path |
|----------|------|
| `sample_app_production` | sample_app Dockerfile **final** stage + Thruster (`:80`) |
| `sample_app_development` | sample_app `compose.dev.yml` (**development** stage + live mount) |
| `ubuntu-mise` / `alpine-mise` / `arch-mise` | Flavor image + compose profile **`app`** (sample_app mount + `/cache` volume) |

Each scenario runs **cold** then **warm**:

| Phase | Behavior |
|-------|----------|
| **cold** | Remove dedicated bench image; `docker build --no-cache`; remove bench volume (mise flavors) |
| **warm** | Keep bench image layers + volume; rebuild allowed with cache; start server again |

**Timed range:** start of build → `GET /up` 2xx → `GET /` 2xx (full path).

## Isolation

Uses **only** dedicated names (does not touch daily `:dev` images or `*-cache` volumes):

| Kind | Example |
|------|---------|
| Images | `sample_app:bench-prod`, `sample_app:bench-dev`, `ubuntu-mise:bench`, … |
| Volumes | `ubuntu-mise-bench-cache`, … |
| Compose projects | `sample-app-bench-dev`, `ubuntu-mise-bench`, … |
| Ports | prod `18080`, dev `13000`, ubuntu `13100`, alpine `13200`, arch `13300` |

## Run

From the umbrella (or any cwd):

```bash
./bench/bin/run-speed-tests
```

Useful options:

```bash
./bench/bin/run-speed-tests --list
./bench/bin/run-speed-tests --only prod,ubuntu-mise
./bench/bin/run-speed-tests --only development --phase cold
./bench/bin/run-speed-tests --sample-app /path/to/sample_app
HTTP_TIMEOUT_S=900 ./bench/bin/run-speed-tests
```

Aliases for `--only`: `prod`, `dev`, `ubuntu`, `alpine`, `arch`.

## Outputs

| File | Content |
|------|---------|
| `results/<run_id>.yaml` | Machine-readable timings per scenario/phase |
| `SPEED.md` | Markdown comparison tables (regenerated each full run) |

Regenerate markdown from an existing YAML:

```bash
python3 bench/lib/report.py bench/results/<run_id>.yaml -o bench/SPEED.md
```

## Prerequisites

- Docker + Compose plugin
- `curl`, `python3`
- Flavor `sample_app` submodules initialized for mise scenarios
- Network for cold gem/tool downloads

A full five-scenario cold+warm run can take a long time (especially cold multi-stage Rails + three OS images). Start with `--only prod,dev` while iterating.
