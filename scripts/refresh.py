#!/usr/bin/env python3
"""Verify every listed project against the GitHub API and regenerate the README index.

Nothing in the index is hand-written metadata: licence, language, last commit date and
archived status all come from the GitHub API at refresh time, so the list cannot quietly
claim something that is not true.

Usage:
  GITHUB_TOKEN=<token> python3 scripts/refresh.py            # verify, write index, update README
  python3 scripts/refresh.py --check                          # verify only, fail on missing entries

Without a token the API allows 60 requests an hour, which is not enough for this list.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "sources" / "tools.csv"
INDEX = ROOT / "index" / "tools.json"
README = ROOT / "README.md"

BEGIN = "<!-- begin:index -->"
END = "<!-- end:index -->"

CATEGORY_ORDER = [
    "BIM and IFC",
    "CAD and drawing",
    "Documents and records",
    "Scheduling and planning",
    "Field data collection",
    "Reality capture and survey",
    "GIS and site",
    "Structural and analysis",
    "Energy MEP and sustainability",
    "Machine learning and datasets",
    "Cost accounting and ERP",
    "Collaboration and PM",
    "Automation robotics and fabrication",
]

CATEGORY_BLURB = {
    "BIM and IFC": "Model authoring, IFC parsing and model servers. The strongest open source area in construction.",
    "CAD and drawing": "Drawing production, and the PDF and OCR plumbing most document workflows end up needing.",
    "Documents and records": "Document management and archives, one step removed from proper EDMS.",
    "Scheduling and planning": "Gantt and CPM tools, plus the optimisation libraries you build a scheduler on.",
    "Field data collection": "Forms, inspections and field records on a phone, without a commercial platform.",
    "Reality capture and survey": "Photogrammetry, point clouds and the libraries that process them.",
    "GIS and site": "Site mapping, terrain and coordinate reference systems.",
    "Structural and analysis": "Section, frame and nonlinear analysis for engineers who script.",
    "Energy MEP and sustainability": "Simulation and assessment engines: energy, daylight, CFD, LCA.",
    "Machine learning and datasets": "Detection and segmentation tooling, and the datasets that come with it.",
    "Cost accounting and ERP": "General ERPs you can shape into job costing, and accounting basics.",
    "Collaboration and PM": "Project tracking, wikis, files and chat for the office and the site trailer.",
    "Automation robotics and fabrication": "Shop automation and robot middleware, where the field robotics work starts.",
}


def token() -> str | None:
    for name in ("GITHUB_TOKEN", "GH_TOKEN"):
        if os.environ.get(name):
            return os.environ[name]
    return None


def api(path: str, auth: str | None) -> tuple[int, dict]:
    request = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "open-source-construction-tools refresh",
            **({"Authorization": f"Bearer {auth}"} if auth else {}),
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status, json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        detail = {}
        try:
            detail = json.loads(exc.read().decode())
        except Exception:
            pass
        return exc.code, detail
    except urllib.error.URLError as exc:
        return 0, {"message": str(exc)}


def slug_of(url: str) -> str:
    return url.rstrip("/").split("github.com/")[-1]


def load_sources() -> list[dict[str, str]]:
    with SOURCES.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def collect(rows: list[dict[str, str]], auth: str | None) -> tuple[list[dict], list[dict]]:
    verified, missing = [], []
    for row in rows:
        entry = dict(row)
        if row["kind"] != "github":
            entry.update(status="listed", licence="", language="", last_commit="", stars=None, archived=None)
            verified.append(entry)
            continue
        status, data = api(f"/repos/{slug_of(row['url'])}", auth)
        if status != 200:
            entry.update(status=f"error {status}", detail=data.get("message", ""))
            missing.append(entry)
            continue
        licence = (data.get("license") or {}).get("spdx_id") or "none declared"
        entry.update(
            status="verified",
            full_name=data["full_name"],
            licence=licence.replace("NOASSERTION", "custom"),
            language=data.get("language") or "unknown",
            last_commit=(data.get("pushed_at") or "")[:10],
            created=(data.get("created_at") or "")[:10],
            stars=data.get("stargazers_count"),
            archived=bool(data.get("archived")),
            description=(data.get("description") or "").strip(),
            html_url=data["html_url"],
        )
        verified.append(entry)
    return verified, missing


def render(entries: list[dict], missing: list[dict], generated_on: str) -> str:
    out: list[str] = []
    verified = [e for e in entries if e["status"] == "verified"]
    out.append(
        f"*{len(verified)} projects checked against the GitHub API on {generated_on}. "
        f"Licence, language, last commit and archived status are read from the API, not typed by hand.*"
    )
    out.append("")
    for category in CATEGORY_ORDER:
        group = [e for e in verified if e["category"] == category]
        if not group:
            continue
        group.sort(key=lambda e: (-(e.get("stars") or 0), e["name"].lower()))
        out.append(f"### {category}")
        out.append("")
        blurb = CATEGORY_BLURB.get(category)
        if blurb:
            out.append(blurb)
            out.append("")
        out.append("| Project | What it does in a construction workflow | Caveat | Licence | Language | Last commit |")
        out.append("| --- | --- | --- | --- | --- | --- |")
        for entry in group:
            name = f"[{entry['name']}]({entry['url']})"
            if entry.get("archived"):
                name += " *(archived)*"
            out.append(
                "| {name} | {what} | {caveat} | {licence} | {language} | {last} |".format(
                    name=name,
                    what=entry["what_it_does"].strip(),
                    caveat=entry["caveat"].strip(),
                    licence=entry["licence"],
                    language=entry["language"],
                    last=entry["last_commit"],
                )
            )
        out.append("")
    listed = [e for e in entries if e["status"] == "listed"]
    if listed:
        out.append("### Standards, schemas and public data")
        out.append("")
        out.append("Not software, but you will need them, and they belong in the same bookmarks.")
        out.append("")
        out.append("| Resource | What it is | Caveat |")
        out.append("| --- | --- | --- |")
        for entry in listed:
            out.append(f"| [{entry['name']}]({entry['url']}) | {entry['what_it_does']} | {entry['caveat']} |")
        out.append("")
    if missing:
        out.append("### Not verifiable right now")
        out.append("")
        out.append(
            "These entries did not answer when the API was queried. They stay in the list, visible, until "
            "somebody confirms whether they moved or vanished."
        )
        out.append("")
        for entry in missing:
            out.append(f"- **{entry['name']}** — `{entry['url']}` ({entry['status']}: {entry.get('detail', '')})")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def update_readme(block: str) -> bool:
    text = README.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        print(f"note: {BEGIN} / {END} markers not found in README.md, block not written")
        return False
    head, rest = text.split(BEGIN, 1)
    _, tail = rest.split(END, 1)
    README.write_text(f"{head}{BEGIN}\n{block}{END}{tail}", encoding="utf-8")
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify only; fail if an entry is missing")
    args = parser.parse_args(argv)

    auth = token()
    if not auth:
        print("warning: no GITHUB_TOKEN set; the API allows 60 requests an hour and this list needs more")

    rows = load_sources()
    entries, missing = collect(rows, auth)
    generated_on = date.today().isoformat()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    verified_count = len([e for e in entries if e["status"] == "verified"])
    print(f"verified {verified_count}/{len(rows)} entries")
    for entry in missing:
        print(f"  MISSING: {entry['name']} -> {entry['url']} ({entry['status']})")

    INDEX.parent.mkdir(parents=True, exist_ok=True)
    INDEX.write_text(
        json.dumps({"generated_on": generated_on, "generated_at": now, "entries": entries}, indent=2) + "\n",
        encoding="utf-8",
    )

    if not args.check:
        wrote = update_readme(render(entries, missing, generated_on))
        print(f"readme updated: {wrote}; index written to {INDEX.relative_to(ROOT)}")

    if args.check and missing:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
