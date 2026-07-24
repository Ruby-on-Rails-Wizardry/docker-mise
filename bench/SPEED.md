# Speed test results

Automated comparison of Rails bring-up paths under `docker-mise/bench`.

## Run metadata

| Field | Value |
|-------|-------|
| run_id | `20260724T152433Z-199361` |
| started_at (UTC) | 2026-07-24T15:26:11Z |
| host | niko |
| sample_app | `/home/rob/Ruby-on-Rails-Wizardry/docker-mise/ubuntu-mise/sample_app` |
| http_timeout_s | 600 |
| source yaml | `20260724T152433Z-199361.yaml` |

## Metric definitions

| Metric | Meaning |
|--------|---------|
| **cold** | No dedicated bench image; `docker build --no-cache`; bench volume removed if used |
| **warm** | Rebuild allowed with layer cache; bench volume/image kept from cold |
| **t_build_s** | Image build only |
| **t_up_s** | Wall time from scenario start until `GET /up` is 2xx |
| **t_root_s** | Wall time from scenario start until `GET /` is 2xx |
| **t_total_s** | Same as **t_root_s** (full path end-to-end) |

Timed range always includes build (when performed) + container start + HTTP wait.

## Summary (total time to `GET /`)

| Scenario | cold | warm | speedup |
|----------|-----:|-----:|--------:|
| sample_app_production | 97.6s | 4.4s | 21.98× |
| sample_app_development | 109.3s | 3.8s | 29.08× |
| ubuntu-mise | 109.4s | 4.1s | 26.73× |
| alpine-mise | FAIL | FAIL | — |
| arch-mise | 98.2s | 4.1s | 23.95× |

## Detail

| Scenario | Phase | ok | t_build_s | t_up_s | t_root_s | t_total_s | port | notes |
|----------|-------|----|----------:|-------:|---------:|----------:|-----:|-------|
| sample_app_production | cold | yes | 94.9s | 97.5s | 97.6s | 97.6s | 18080 | Dockerfile final stage + Thruster; no named volume |
| sample_app_production | warm | yes | 1.9s | 4.4s | 4.4s | 4.4s | 18080 | Dockerfile final stage + Thruster; no named volume |
| sample_app_development | cold | yes | 106.2s | 109.2s | 109.3s | 109.3s | 13000 | compose.dev.yml development stage + live mount |
| sample_app_development | warm | yes | 2.1s | 3.7s | 3.8s | 3.8s | 13000 | compose.dev.yml development stage + live mount |
| ubuntu-mise | cold | yes | 73.3s | 109.3s | 109.4s | 109.4s | 13100 | compose profile app; sample_app bind + ubuntu-mise-bench-cache |
| ubuntu-mise | warm | yes | 1.3s | 4.0s | 4.1s | 4.1s | 13100 | compose profile app; sample_app bind + ubuntu-mise-bench-cache |
| alpine-mise | cold | no | — | — | — | — | — | timeout waiting for /up |
| alpine-mise | warm | no | — | — | — | — | — | timeout waiting for /up |
| arch-mise | cold | yes | 58.0s | 98.1s | 98.2s | 98.2s | 13300 | compose profile app; sample_app bind + arch-mise-bench-cache |
| arch-mise | warm | yes | 1.3s | 4.0s | 4.1s | 4.1s | 13300 | compose profile app; sample_app bind + arch-mise-bench-cache |

## Setup notes

| Scenario | What is timed |
|----------|---------------|
| sample_app production | `docker build` (final stage) + `docker run` Thruster/`rails server` on :80 |
| sample_app development | `docker compose -f compose.dev.yml build` + `up` (live mount) |
| ubuntu/alpine/arch-mise | Flavor `bin/build` + `compose --profile app up app` (sample_app mount + `/cache` volume) |

Bench uses **dedicated** image and volume names (`*:bench*`) so daily `:dev` images and `*-cache` volumes are left alone.

## Alpine failure note

`alpine-mise` timed out on both cold and warm. Container logs showed mise installing precompiled Ruby into `/cache`, then:

```text
/cache/mise/installs/ruby/4.0.6/bin/ruby: not found
```

That is consistent with **glibc prebuilt Ruby on musl Alpine**. Fixing Alpine for this path is out of band for this speed run (e.g. `ruby.compile=true` on Alpine or a musl-compatible Ruby install). Ubuntu and Arch (glibc) completed normally.

