#!/usr/bin/env python3
"""Validate AI API security/privacy transparency reviews and build RANKINGS.md."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parent
SUBMISSIONS = ROOT / "data" / "submissions"
OUTPUT = ROOT / "RANKINGS.md"
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{2,79}$")
STATUSES = {"documented", "not_documented", "not_applicable"}
CONTROLS = (
    "privacy_policy",
    "retention_period",
    "training_use",
    "deletion_process",
    "subprocessors",
    "security_contact",
    "incident_status",
    "encryption_in_transit",
    "access_controls",
    "independent_assurance",
)


def fail(message: str) -> None:
    raise ValueError(message)


def text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{field} must be a non-empty string")
    return value.strip()


def https_url(value: Any, field: str) -> str:
    value = text(value, field)
    parsed = urlsplit(value)
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        fail(f"{field} must be a public HTTPS URL without credentials")
    return value


def iso_date(value: Any, field: str) -> str:
    raw = text(value, field)
    try:
        date.fromisoformat(raw)
    except ValueError as error:
        raise ValueError(f"{field} must be an ISO date (YYYY-MM-DD)") from error
    return raw


def validate(data: Any, source: Path) -> dict[str, Any]:
    if not isinstance(data, dict):
        fail(f"{source}: root must be an object")
    if data.get("schema_version") != 1:
        fail(f"{source}: schema_version must be 1")
    submission_id = text(data.get("id"), "id")
    if not ID_RE.fullmatch(submission_id):
        fail("id must use lowercase letters, digits, and hyphens")
    if source.parent == SUBMISSIONS and source.stem != submission_id:
        fail(f"{source}: filename must equal id")
    text(data.get("title"), "title")
    reviewed_at = iso_date(data.get("reviewed_at"), "reviewed_at")
    author = data.get("author")
    if not isinstance(author, dict):
        fail("author must be an object")
    text(author.get("github"), "author.github")
    text(author.get("affiliation"), "author.affiliation")
    conflicts = data.get("conflicts")
    if not isinstance(conflicts, list) or any(not isinstance(item, str) for item in conflicts):
        fail("conflicts must be an array of strings")
    methodology = https_url(data.get("methodology_url"), "methodology_url")
    entries = data.get("entries")
    if not isinstance(entries, list) or len(entries) < 2:
        fail("entries must contain at least two comparable providers")
    seen: set[str] = set()
    normalized = []
    for index, entry in enumerate(entries):
        field = f"entries[{index}]"
        if not isinstance(entry, dict):
            fail(f"{field} must be an object")
        provider = text(entry.get("provider"), f"{field}.provider")
        service_scope = text(entry.get("service_scope"), f"{field}.service_scope")
        identity = f"{provider}\0{service_scope}".casefold()
        if identity in seen:
            fail(f"{field}: provider and service_scope are duplicated")
        seen.add(identity)
        controls = entry.get("controls")
        if not isinstance(controls, dict) or set(controls) != set(CONTROLS):
            fail(f"{field}.controls must contain exactly: {', '.join(CONTROLS)}")
        documented = 0
        applicable = 0
        checked_controls: dict[str, dict[str, str]] = {}
        for control_name in CONTROLS:
            control = controls[control_name]
            control_field = f"{field}.controls.{control_name}"
            if not isinstance(control, dict):
                fail(f"{control_field} must be an object")
            status = text(control.get("status"), f"{control_field}.status")
            if status not in STATUSES:
                fail(f"{control_field}.status must be one of {sorted(STATUSES)}")
            note = text(control.get("note"), f"{control_field}.note")
            source_url = control.get("source_url", "")
            if status == "documented":
                source_url = https_url(source_url, f"{control_field}.source_url")
                documented += 1
                applicable += 1
            elif status == "not_documented":
                if source_url:
                    source_url = https_url(source_url, f"{control_field}.source_url")
                applicable += 1
            else:
                if source_url:
                    source_url = https_url(source_url, f"{control_field}.source_url")
            checked_controls[control_name] = {"status": status, "source_url": source_url, "note": note}
        if applicable == 0:
            fail(f"{field}: at least one control must be applicable")
        normalized.append(
            {
                "provider": provider,
                "service_scope": service_scope,
                "documented": documented,
                "applicable": applicable,
                "transparency_score": documented * 100 / applicable,
                "controls": checked_controls,
            }
        )
    normalized.sort(key=lambda item: (-item["transparency_score"], -item["documented"], item["provider"].casefold()))
    return {**data, "reviewed_at": reviewed_at, "methodology_url": methodology, "entries": normalized}


def load_submissions() -> list[dict[str, Any]]:
    submissions = []
    for path in sorted(SUBMISSIONS.glob("*.json")):
        try:
            submissions.append(validate(json.loads(path.read_text(encoding="utf-8")), path))
        except json.JSONDecodeError as error:
            raise ValueError(f"{path}: invalid JSON: {error.msg}") from error
    return submissions


def render(submissions: list[dict[str, Any]]) -> str:
    lines = [
        "# AI API Security & Privacy Transparency Rankings",
        "",
        "> Generated from reviewed files in `data/submissions/`. This ranks public evidence coverage, not actual security, honesty, legal compliance, breach history, or proof that data cannot be misused.",
        "",
    ]
    if not submissions:
        lines += [
            "## Awaiting the first reviewed submission",
            "",
            "No real provider is ranked yet. Use the fictional example to test the format, then submit a dated, source-by-source review through a pull request.",
            "",
            "See [CONTRIBUTING.md](CONTRIBUTING.md) and [data/examples/example-ranking.json](data/examples/example-ranking.json).",
            "",
        ]
        return "\n".join(lines)
    for submission in submissions:
        lines += [
            f"## {submission['title']}",
            "",
            f"Reviewed: `{submission['reviewed_at']}` | [Method]({submission['methodology_url']}) | Submitted by `@{submission['author']['github']}` ({submission['author']['affiliation']})",
            "",
            "| Rank | Provider / service | Publicly documented controls | Applicable controls | Transparency score |",
            "| ---: | --- | ---: | ---: | ---: |",
        ]
        for rank, entry in enumerate(submission["entries"], 1):
            label = f"{entry['provider']} / {entry['service_scope']}"
            lines.append(f"| {rank} | {label} | {entry['documented']} | {entry['applicable']} | {entry['transparency_score']:.1f}% |")
        lines += [""]
        for entry in submission["entries"]:
            lines += [f"### {entry['provider']} / {entry['service_scope']}", "", "| Control | Status | Evidence / review note |", "| --- | --- | --- |"]
            for name in CONTROLS:
                control = entry["controls"][name]
                evidence = f"[source]({control['source_url']})" if control["source_url"] else "No public source recorded"
                lines.append(f"| `{name}` | `{control['status']}` | {evidence}: {control['note']} |")
            lines.append("")
        conflicts = "; ".join(submission["conflicts"]) or "None declared"
        lines += [f"Conflicts: {conflicts}", ""]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if RANKINGS.md is stale")
    parser.add_argument("--validate", type=Path, help="validate one example or proposed submission")
    args = parser.parse_args(argv)
    try:
        if args.validate:
            validate(json.loads(args.validate.read_text(encoding="utf-8")), args.validate)
            print(f"valid: {args.validate}")
            return 0
        output = render(load_submissions())
        if args.check:
            if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != output:
                print("RANKINGS.md is stale; run python3 rankings.py", file=sys.stderr)
                return 1
            print("RANKINGS.md is current")
            return 0
        OUTPUT.write_text(output, encoding="utf-8")
        print(f"wrote {OUTPUT}")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
