#!/usr/bin/env python3
"""Regenerates the diagrams in assets/ (light and dark SVG). Run from anywhere: python3 scripts/make_graphics.py
No dependencies. Diagrams that show data read it from this repository, so they cannot drift."""
# ── svg kit: a small, dependency-free set of helpers for clean, Apple-style diagrams ─────────────────────────
# Light and dark themes, system font stack, soft cards, Apple system colours. Every graphic is generated, so it
# can be reproduced and, where it shows data, regenerated from that data.
from __future__ import annotations

import html
from pathlib import Path

SANS = '-apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Segoe UI", Inter, Helvetica, Arial, sans-serif'
MONO = 'ui-monospace, "SF Mono", SFMono-Regular, Menlo, Consolas, monospace'

THEMES = {
    "light": dict(
        bg0="#fbfbfd", bg1="#f2f2f7", card="#ffffff", edge="#e5e5ea", text="#1d1d1f", sub="#6e6e73", faint="#aeaeb2",
        track="#e8e8ed", shadow=0.07, chip="#f5f5f7",
        blue="#007aff", green="#34c759", orange="#ff9500", pink="#ff2d55", purple="#af52de", teal="#30b0c7",
        indigo="#5856d6", yellow="#d4a000", red="#ff3b30", mint="#00a99d", cyan="#32ade6", brown="#a2845e",
        ink=dict(blue="#0062cc", green="#248a3d", orange="#b25000", pink="#d30f45", purple="#8944ab", teal="#00809a",
                 indigo="#4a48c0", yellow="#8a6500", red="#d70015", mint="#007a72", cyan="#0071a4", brown="#7f6a4d", faint="#6e6e73"),
    ),
    "dark": dict(
        bg0="#1c1c1e", bg1="#000000", card="#2c2c2e", edge="#3a3a3c", text="#f5f5f7", sub="#a1a1a6", faint="#636366",
        track="#3a3a3c", shadow=0.5, chip="#38383a",
        blue="#0a84ff", green="#30d158", orange="#ff9f0a", pink="#ff375f", purple="#bf5af2", teal="#40c8e0",
        indigo="#5e5ce6", yellow="#ffd60a", red="#ff453a", mint="#63e6e2", cyan="#64d2ff", brown="#ac8e68",
        ink=dict(blue="#0a84ff", green="#30d158", orange="#ff9f0a", pink="#ff375f", purple="#bf5af2", teal="#40c8e0",
                 indigo="#7d7aff", yellow="#ffd60a", red="#ff453a", mint="#63e6e2", cyan="#64d2ff", brown="#ac8e68", faint="#a1a1a6"),
    ),
}


def esc(s) -> str:
    return html.escape(str(s), quote=True)


def wrap(text: str, width: int) -> list[str]:
    lines, line = [], ""
    for word in text.split():
        if line and len(line) + 1 + len(word) > width:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    if line:
        lines.append(line)
    return lines


def text_width(s: str, size: float, mono: bool = False, weight: int = 400) -> float:
    k = 0.60 if mono else (0.56 if weight < 600 else 0.585)
    return len(s) * size * k


class Canvas:
    def __init__(self, w: int, h: int, theme: str, title: str, desc: str, radius: int = 28):
        self.w, self.h, self.t, self.name = w, h, THEMES[theme], theme
        self.title, self.desc, self.radius = title, desc, radius
        self.parts: list[str] = []
        self.defs: list[str] = []

    # primitives ---------------------------------------------------------------------------------------------
    def add(self, s: str):
        self.parts.append(s)

    def text(self, x, y, s, size=16, weight=400, fill=None, anchor="start", mono=False, opacity=None, spacing=None):
        fill = fill or self.t["text"]
        fam = MONO if mono else SANS
        extra = (f' opacity="{opacity}"' if opacity is not None else "") + (f' letter-spacing="{spacing}"' if spacing is not None else "")
        self.add(f'<text x="{x}" y="{y}" font-family=\'{fam}\' font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{extra}>{esc(s)}</text>')

    def lines(self, x, y, rows: list[str], size=15, weight=400, fill=None, anchor="start", lh=1.35, mono=False):
        for i, row in enumerate(rows):
            self.text(x, y + i * size * lh, row, size, weight, fill, anchor, mono)

    def rect(self, x, y, w, h, r=16, fill=None, stroke=None, sw=1, shadow=False, opacity=None):
        fill = fill or self.t["card"]
        attrs = f'fill="{fill}"' + (f' stroke="{stroke}" stroke-width="{sw}"' if stroke else "") + (f' opacity="{opacity}"' if opacity is not None else "") + (' filter="url(#sh)"' if shadow else "")
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" {attrs}/>')

    def card(self, x, y, w, h, r=20, fill=None):
        self.rect(x, y, w, h, r, fill=fill, stroke=self.t["edge"], shadow=True)

    def dot(self, cx, cy, r, color):
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>')

    def pill(self, x, y, label, color=None, size=13, weight=600, mono=False, pad=12, h=None, fill=None, anchor="start", text_fill=None):
        w = text_width(label, size, mono, weight) + pad * 2
        h = h or size + 14
        x0 = x - w / 2 if anchor == "middle" else (x - w if anchor == "end" else x)
        color = color or self.t["sub"]
        self.rect(x0, y, w, h, r=h / 2, fill=fill or self.t["chip"])
        self.text(x0 + w / 2, y + h / 2 + size * 0.35, label, size, weight, text_fill or color, "middle", mono)
        return w

    def badge(self, x, y, label, color, size=12):
        w = text_width(label, size, False, 700) + 18
        self.rect(x, y, w, size + 10, r=(size + 10) / 2, fill=color, opacity=0.14)
        self.text(x + w / 2, y + (size + 10) / 2 + size * 0.35, label, size, 700, color, "middle")
        return w

    def arrow(self, x1, y1, x2, y2, color=None, sw=2, head=7):
        color = color or self.t["faint"]
        import math
        a = math.atan2(y2 - y1, x2 - x1)
        bx, by = x2 - math.cos(a) * 1.5, y2 - math.sin(a) * 1.5
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{bx}" y2="{by}" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>')
        p1 = (x2 - head * math.cos(a - 0.5), y2 - head * math.sin(a - 0.5))
        p2 = (x2 - head * math.cos(a + 0.5), y2 - head * math.sin(a + 0.5))
        self.add(f'<path d="M{p1[0]:.1f} {p1[1]:.1f} L{x2} {y2} L{p2[0]:.1f} {p2[1]:.1f}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')

    def elbow(self, x1, y1, x2, y2, color=None, sw=2):
        """Right, then up/down, then right into the target, with rounded corners."""
        color = color or self.t["faint"]
        mid = (x1 + x2) / 2
        r = min(10, abs(y2 - y1) / 2)
        sgn = 1 if y2 > y1 else -1
        d = f"M{x1} {y1} H{mid - r} Q{mid} {y1} {mid} {y1 + sgn * r} V{y2 - sgn * r} Q{mid} {y2} {mid + r} {y2} H{x2 - 2}"
        self.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>')
        self.add(f'<path d="M{x2 - 7} {y2 - 4} L{x2} {y2} L{x2 - 7} {y2 + 4}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')

    # output -------------------------------------------------------------------------------------------------
    def svg(self) -> str:
        t = self.t
        head = (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" role="img" aria-labelledby="t d">'
            f'<title id="t">{esc(self.title)}</title><desc id="d">{esc(self.desc)}</desc>'
            f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["bg0"]}"/><stop offset="1" stop-color="{t["bg1"]}"/></linearGradient>'
            f'<filter id="sh" x="-8%" y="-8%" width="116%" height="128%"><feDropShadow dx="0" dy="3" stdDeviation="7" flood-color="#000" flood-opacity="{t["shadow"]}"/></filter>'
            + "".join(self.defs)
            + "</defs>"
            f'<rect width="{self.w}" height="{self.h}" rx="{self.radius}" fill="url(#bg)"/>'
            f'<rect x=".5" y=".5" width="{self.w - 1}" height="{self.h - 1}" rx="{self.radius}" fill="none" stroke="{t["edge"]}"/>'
        )
        return head + "".join(self.parts) + "</svg>\n"


def header(c: Canvas, title: str, subtitle: str, x=56, y=82, size=40):
    c.text(x, y, title, size, 700, c.t["text"], spacing=-0.5)
    c.text(x, y + 34, subtitle, 18, 400, c.t["sub"])


def build(out: Path, name: str, make, *args):
    """make(theme) -> Canvas. Writes <name>-light.svg and <name>-dark.svg."""
    out.mkdir(parents=True, exist_ok=True)
    for theme in ("light", "dark"):
        (out / f"{name}-{theme}.svg").write_text(make(theme, *args).svg(), encoding="utf-8")


def picture(name: str, alt: str, folder="assets", width="100%") -> str:
    return (
        f'<p align="center">\n  <picture>\n'
        f'    <source media="(prefers-color-scheme: dark)" srcset="{folder}/{name}-dark.svg">\n'
        f'    <img src="{folder}/{name}-light.svg" alt="{esc(alt)}" width="{width}">\n'
        f'  </picture>\n</p>\n'
    )


import collections


CATS = [  # (index name, display name, colour key)
    ("BIM and IFC", "BIM and IFC", "blue"),
    ("CAD and drawing", "CAD and drawing", "indigo"),
    ("Documents and records", "Documents and records", "teal"),
    ("Scheduling and planning", "Scheduling and planning", "green"),
    ("Field data collection", "Field data collection", "orange"),
    ("Reality capture and survey", "Reality capture and survey", "pink"),
    ("GIS and site", "GIS and site", "mint"),
    ("Structural and analysis", "Structural and analysis", "purple"),
    ("Energy MEP and sustainability", "Energy, MEP and sustainability", "cyan"),
    ("Machine learning and datasets", "Machine learning and datasets", "red"),
    ("Cost accounting and ERP", "Cost accounting and ERP", "yellow"),
    ("Collaboration and PM", "Collaboration and PM", "brown"),
    ("Automation robotics and fabrication", "Automation, robotics and fabrication", "indigo"),
]
PERMISSIVE = ("MIT", "APACHE", "BSD", "ISC", "UNLICENSE", "0BSD", "CC0", "ZLIB", "BSL")
WEAK = ("LGPL", "MPL", "EPL", "CDDL")




def licence_class(lic: str) -> str:
    u = (lic or "").upper()
    if u.startswith(("AGPL", "GPL")) or u.startswith("GPL"):
        return "Strong copyleft"
    if any(u.startswith(p) for p in WEAK):
        return "Weak copyleft"
    if any(u.startswith(p) for p in PERMISSIVE):
        return "Permissive"
    return "Custom or unrecognised"


def make_map(theme, entries, date):
    verified = [e for e in entries if e.get("status") == "verified"]
    counts = collections.Counter(e["category"] for e in verified)
    W, H = 1200, 800
    c = Canvas(W, H, theme, "Open source construction tools, by category",
               f"{len(verified)} open source projects across {len(CATS)} categories, each checked against the GitHub API: " +
               ", ".join(f"{disp} {counts.get(name, 0)}" for name, disp, _ in CATS))
    t = c.t
    c.text(56, 86, f"{len(verified)} open source tools", 44, 700, spacing=-0.8)
    c.text(56, 122, "for construction, each with an honest caveat. Licence, language and last commit read from the GitHub API.", 18, 400, t["sub"])
    c.pill(W - 56, 62, f"Checked {date}", t["sub"], 13, 600, anchor="end")

    x0, y0, gap = 56, 168, 16
    cols = 4
    tw = (W - 2 * x0 - gap * (cols - 1)) / cols
    th = 132
    for i, (name, disp, col) in enumerate(CATS):
        r, k = divmod(i, cols)
        x, y = x0 + k * (tw + gap), y0 + r * (th + gap)
        c.card(x, y, tw, th, 20)
        color = t[col]
        c.dot(x + 26, y + 30, 6, color)
        for j, line in enumerate(wrap(disp, 22)[:2]):
            c.text(x + 42, y + 35 + j * 20, line, 16, 600, t["text"])
        n = counts.get(name, 0)
        unit = "tools" if n != 1 else "tool"
        c.add(f'<text x="{x + 24}" y="{y + th - 22}" font-family=\'{SANS}\' font-size="40" font-weight="700" fill="{c.t["ink"].get(col, color)}" letter-spacing="-1">{n}<tspan font-size="14" font-weight="500" fill="{t["sub"]}" dx="8" letter-spacing="0">{unit}</tspan></text>')

    # licence tile spans the last three columns of the last row
    r = 3
    x = x0 + 1 * (tw + gap)
    y = y0 + r * (th + gap)
    w = tw * 3 + gap * 2
    c.card(x, y, w, th, 20)
    cls = collections.Counter(licence_class(e.get("licence", "")) for e in verified)
    order = [("Permissive", "green"), ("Weak copyleft", "blue"), ("Strong copyleft", "orange"), ("Custom or unrecognised", "faint")]
    total = sum(cls.values()) or 1
    c.text(x + 24, y + 38, "Licences", 16, 600)
    c.text(x + w - 24, y + 38, "permissive licences are the easiest to build a product on", 13, 400, t["sub"], "end")
    bx, bw, by = x + 24, w - 48, y + 60
    cx = bx
    for label, col in order:
        n = cls.get(label, 0)
        if not n:
            continue
        seg = bw * n / total
        c.rect(cx, by, max(seg - 3, 4), 12, r=6, fill=t[col])
        cx += seg
    lx = bx
    for label, col in order:
        n = cls.get(label, 0)
        c.dot(lx + 5, y + 100, 5, t[col])
        s = f"{label} {n}"
        c.text(lx + 16, y + 105, s, 13, 500, t["sub"])
        lx += 16 + text_width(s, 13) + 24
    return c


def make_evaluate(theme):
    W, H = 1200, 470
    c = Canvas(W, H, theme, "Five questions before an open source tool goes on a live job",
               "Is it somebody's day job; what does the licence oblige you to do; can you get your data out; what does it cost to run; and who supports it when it breaks on a Friday.")
    t = c.t
    c.text(56, 84, "Before it goes on a live job", 40, 700, spacing=-0.7)
    c.text(56, 118, "Five questions that matter more than the star count.", 18, 400, t["sub"])
    qs = [("Is it somebody's day job?", "One maintainer and no employer behind it means you are now co-maintaining.", "blue"),
          ("What does the licence oblige you to do?", "Read the licence file itself, not just the badge.", "indigo"),
          ("Can you get your data out?", "Ask what the export looks like before project data goes in.", "teal"),
          ("What does it cost to run?", "A server, a database and a GPU are commitments, not downloads.", "orange"),
          ("Who supports it on a Friday?", "If the answer is the community, plan for the delay.", "pink")]
    gap, y, h = 14, 160, 250
    cw = (1088 - gap * 4) / 5
    for i, (q, a, col) in enumerate(qs):
        x = 56 + i * (cw + gap)
        c.card(x, y, cw, h, 22)
        c.text(x + 20, y + 62, str(i + 1), 44, 700, t["ink"][col], spacing=-1)
        for j, line in enumerate(wrap(q, 17)[:3]):
            c.text(x + 20, y + 96 + j * 22, line, 16.5, 700)
        for j, line in enumerate(wrap(a, 22)[:5]):
            c.text(x + 20, y + 172 + j * 19, line, 13, 400, t["sub"])
    return c


def _load(root):
    import json
    d = json.loads((root / "index" / "tools.json").read_text(encoding="utf-8"))
    return d["entries"], d["generated_on"]


if __name__ == "__main__":
    HERE = Path(__file__).resolve().parent.parent
    out = HERE / "assets"
    entries, date = _load(HERE)
    build(out, "tools-map", make_map, entries, date)
    build(out, "evaluate", make_evaluate)
