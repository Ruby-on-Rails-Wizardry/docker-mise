#!/usr/bin/env python3
"""Generate SPEED.md from a bench results YAML file."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def load_simple_yaml(path: Path) -> dict:
    """Minimal YAML loader for our fixed result shape (no PyYAML required)."""
    try:
        import yaml  # type: ignore

        return yaml.safe_load(path.read_text())
    except ImportError:
        pass

    data: dict = {"results": []}
    current: dict | None = None
    for raw in path.read_text().splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith("run_id:"):
            data["run_id"] = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("started_at:"):
            data["started_at"] = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("host:"):
            data["host"] = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("sample_app:"):
            data["sample_app"] = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("http_timeout_s:"):
            data["http_timeout_s"] = int(line.split(":", 1)[1].strip())
        elif line.strip() == "results:":
            continue
        elif line.startswith("  -"):
            current = {}
            data["results"].append(current)
            rest = line[3:].strip()
            if rest:
                # Inline list item: "- key: value"
                _assign(current, rest)
        elif current is not None and line.startswith("    "):
            _assign(current, line.strip())
    return data


def _assign(current: dict, stripped: str) -> None:
    key, _, val = stripped.partition(":")
    key = key.strip()
    val = val.strip()
    if val in ("null", ""):
        current[key] = None
    elif val in ("true", "false"):
        current[key] = val == "true"
    elif val.startswith('"') and val.endswith('"'):
        current[key] = val[1:-1].encode("utf-8").decode("unicode_escape")
    else:
        try:
            if "." in val:
                current[key] = float(val)
            else:
                current[key] = int(val)
        except ValueError:
            current[key] = val


def fmt_s(v) -> str:
    if v is None:
        return "—"
    return f"{float(v):.1f}s"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("results_yaml", type=Path)
    ap.add_argument("-o", "--output", type=Path, required=True)
    args = ap.parse_args()

    data = load_simple_yaml(args.results_yaml)
    results = data.get("results") or []

    # Index by scenario + phase
    by: dict[tuple[str, str], dict] = {}
    for r in results:
        by[(r.get("scenario") or "?", r.get("phase") or "?")] = r

    scenarios = []
    for r in results:
        s = r.get("scenario")
        if s and s not in scenarios:
            scenarios.append(s)

    lines: list[str] = []
    lines.append("# Speed test results")
    lines.append("")
    lines.append("Automated comparison of Rails bring-up paths under `docker-mise/bench`.")
    lines.append("")
    lines.append("## Run metadata")
    lines.append("")
    lines.append("| Field | Value |")
    lines.append("|-------|-------|")
    lines.append(f"| run_id | `{data.get('run_id', '')}` |")
    lines.append(f"| started_at (UTC) | {data.get('started_at', '')} |")
    lines.append(f"| host | {data.get('host', '')} |")
    lines.append(f"| sample_app | `{data.get('sample_app', '')}` |")
    lines.append(f"| http_timeout_s | {data.get('http_timeout_s', '')} |")
    lines.append(f"| source yaml | `{args.results_yaml.name}` |")
    lines.append("")
    lines.append("## Metric definitions")
    lines.append("")
    lines.append("| Metric | Meaning |")
    lines.append("|--------|---------|")
    lines.append("| **cold** | No dedicated bench image; `docker build --no-cache`; bench volume removed if used |")
    lines.append("| **warm** | Rebuild allowed with layer cache; bench volume/image kept from cold |")
    lines.append("| **t_build_s** | Image build only |")
    lines.append("| **t_up_s** | Wall time from scenario start until `GET /up` is 2xx |")
    lines.append("| **t_root_s** | Wall time from scenario start until `GET /` is 2xx |")
    lines.append("| **t_total_s** | Same as **t_root_s** (full path end-to-end) |")
    lines.append("")
    lines.append("Timed range always includes build (when performed) + container start + HTTP wait.")
    lines.append("")

    lines.append("## Summary (total time to `GET /`)")
    lines.append("")
    lines.append("| Scenario | cold | warm | speedup |")
    lines.append("|----------|-----:|-----:|--------:|")
    for s in scenarios:
        cold = by.get((s, "cold"))
        warm = by.get((s, "warm"))
        c = cold.get("t_total_s") if cold and cold.get("ok") else None
        w = warm.get("t_total_s") if warm and warm.get("ok") else None
        if c and w and float(w) > 0:
            speedup = f"{float(c) / float(w):.2f}×"
        else:
            speedup = "—"
        c_s = fmt_s(c) if c is not None else ("FAIL" if cold and not cold.get("ok") else "—")
        w_s = fmt_s(w) if w is not None else ("FAIL" if warm and not warm.get("ok") else "—")
        if c is None and cold and not cold.get("ok"):
            c_s = "FAIL"
        if w is None and warm and not warm.get("ok"):
            w_s = "FAIL"
        lines.append(f"| {s} | {c_s} | {w_s} | {speedup} |")
    lines.append("")

    lines.append("## Detail")
    lines.append("")
    lines.append("| Scenario | Phase | ok | t_build_s | t_up_s | t_root_s | t_total_s | port | notes |")
    lines.append("|----------|-------|----|----------:|-------:|---------:|----------:|-----:|-------|")
    for r in results:
        ok = "yes" if r.get("ok") else "no"
        notes = r.get("error") or r.get("notes") or ""
        notes = str(notes).replace("|", "\\|")
        lines.append(
            "| {scenario} | {phase} | {ok} | {tb} | {tu} | {tr} | {tt} | {port} | {notes} |".format(
                scenario=r.get("scenario", ""),
                phase=r.get("phase", ""),
                ok=ok,
                tb=fmt_s(r.get("t_build_s")),
                tu=fmt_s(r.get("t_up_s")),
                tr=fmt_s(r.get("t_root_s")),
                tt=fmt_s(r.get("t_total_s")),
                port=r.get("port") if r.get("port") is not None else "—",
                notes=notes,
            )
        )
    lines.append("")

    lines.append("## Setup notes")
    lines.append("")
    lines.append("| Scenario | What is timed |")
    lines.append("|----------|---------------|")
    lines.append("| sample_app production | `docker build` (final stage) + `docker run` Thruster/`rails server` on :80 |")
    lines.append("| sample_app development | `docker compose -f compose.dev.yml build` + `up` (live mount) |")
    lines.append("| ubuntu/alpine/arch-mise | Flavor `bin/build` + `compose --profile app up app` (sample_app mount + `/cache` volume) |")
    lines.append("")
    lines.append("Bench uses **dedicated** image and volume names (`*:bench*`) so daily `:dev` images and `*-cache` volumes are left alone.")
    lines.append("")

    args.output.write_text("\n".join(lines) + "\n")
    print(args.output, file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
