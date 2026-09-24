#!/usr/bin/env python3
"""Check that the sources file, the generated index and the README all agree.

Run from the repository root:  python3 scripts/validate.py

The interesting check is the last one: the README index block is re-rendered from
index/tools.json and compared byte for byte, so a hand-edited licence or last-commit
date fails the build instead of quietly going stale.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import refresh  # noqa: E402  (local module, path inserted above)

SOURCES = ROOT / "sources" / "tools.csv"
INDEX = ROOT / "index" / "tools.json"

REQUIRED_COLUMNS = ["name", "kind", "url", "category", "what_it_does", "caveat"]
REQUIRED_FILES = [
    "README.md",
    "sources/tools.csv",
    "index/tools.json",
    "scripts/refresh.py",
    "scripts/validate.py",
    ".github/workflows/validate.yml",
]

errors: list[str] = []


def check_files() -> None:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            errors.append(f"missing required file: {rel}")


def check_sources() -> list[dict[str, str]]:
    if not SOURCES.exists():
        return []
    with SOURCES.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
        header = handle.seek(0) or None  # noqa: F841  (seek keeps the reader honest about the file)
    with SOURCES.open(newline="", encoding="utf-8") as handle:
        first_line = handle.readline().strip().split(",")
    if first_line != REQUIRED_COLUMNS:
        errors.append(f"sources/tools.csv: header is {first_line}, expected {REQUIRED_COLUMNS}")

    names: set[str] = set()
    for index, row in enumerate(rows, start=2):
        for column in REQUIRED_COLUMNS:
            if not (row.get(column) or "").strip():
                errors.append(f"sources/tools.csv row {index}: empty '{column}'")
        name = (row.get("name") or "").strip()
        if name in names:
            errors.append(f"sources/tools.csv row {index}: duplicate name {name!r}")
        names.add(name)
        kind = (row.get("kind") or "").strip()
        if kind not in {"github", "link"}:
            errors.append(f"sources/tools.csv row {index}: kind must be github or link, got {kind!r}")
        url = (row.get("url") or "").strip()
        if kind == "github" and not url.startswith("https://github.com/"):
            errors.append(f"sources/tools.csv row {index}: github entry with a non-GitHub url {url!r}")
        if kind == "github" and url.count("/") != 4:
            errors.append(f"sources/tools.csv row {index}: github url should be owner/repo, got {url!r}")
        category = (row.get("category") or "").strip()
        if category not in refresh.CATEGORY_ORDER:
            errors.append(f"sources/tools.csv row {index}: unknown category {category!r}")
        caveat = (row.get("caveat") or "").strip()
        if len(caveat) < 15:
            errors.append(f"sources/tools.csv row {index}: caveat is too short to be useful")
    return rows


def check_index(rows: list[dict[str, str]]) -> dict:
    if not INDEX.exists():
        errors.append("index/tools.json is missing; run scripts/refresh.py")
        return {}
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    if not data.get("generated_on"):
        errors.append("index/tools.json: no generated_on date")
    entries = data.get("entries", [])
    if len(entries) != len(rows):
        errors.append(f"index/tools.json has {len(entries)} entries but sources/tools.csv has {len(rows)}")
    for entry in entries:
        if entry.get("kind") == "github" and entry.get("status") != "verified":
            errors.append(
                f"index/tools.json: {entry.get('name')} is not verified ({entry.get('status')}); "
                "re-run scripts/refresh.py with a token"
            )
        if not entry.get("licence") and entry.get("kind") == "github":
            errors.append(f"index/tools.json: {entry.get('name')} has no licence recorded")
    return data


def check_readme_matches(rows: list[dict[str, str]], data: dict) -> None:
    readme = ROOT / "README.md"
    if not readme.exists():
        return
    text = readme.read_text(encoding="utf-8")
    if refresh.BEGIN not in text or refresh.END not in text:
        errors.append("README.md: generated index markers are missing")
        return
    block = text.split(refresh.BEGIN, 1)[1].split(refresh.END, 1)[0].strip("\n")

    entries = data.get("entries", [])
    missing = [e for e in entries if e.get("status") != "verified" and e.get("kind") == "github"]
    expected = refresh.render(entries, missing, data.get("generated_on", "")).strip("\n")
    if block.strip() != expected.strip():
        errors.append(
            "README.md: the generated index block is out of date; run scripts/refresh.py "
            "(do not hand-edit rows between the markers)"
        )
    for row in rows:
        if row["name"] not in block:
            errors.append(f"README.md: {row['name']} is missing from the index block")


def main() -> int:
    check_files()
    rows = check_sources()
    data = check_index(rows)
    if data:
        check_readme_matches(rows, data)

    if errors:
        print(f"FAIL: {len(errors)} problem(s)\n")
        for error in errors:
            print(f"  - {error}")
        return 1

    entries = data.get("entries", [])
    verified = len([e for e in entries if e.get("status") == "verified"])
    listed = len(entries) - verified
    print(f"OK: {len(entries)} entries ({verified} verified, {listed} listed resources), index generated {data['generated_on']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
