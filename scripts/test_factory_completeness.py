#!/usr/bin/env python3
"""Assert factory HTML matches FACTORY-INSTRUCTION-SET.md (SDT completeness bar)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = [
    "repeating-linear-gradient",
    "coaching-led curriculum",
    "vertical and ad capacity",
]
HOME_REQUIRED = [
    "hero-photo",
    "icon-grid",
    "icon-tile",
    "search-hero",
    "class=\"stat\"",
    "class=\"card step\"",
    "class=\"partner\"",
    "class=\"insight\"",
    "class=\"formbox\"",
    "Request a Proposal",
    "Consultation",
]
NAV_FORBIDDEN_DUP = None  # checked separately


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def main() -> None:
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    for needle in FORBIDDEN:
        if needle in home:
            fail(f"home contains forbidden leftover {needle!r}")
    for needle in HOME_REQUIRED:
        if needle not in home:
            fail(f"home missing required module marker {needle!r}")
    if home.count(">Contact</a>") > 1:
        fail("duplicate Contact nav items")
    if "Insights" not in home:
        fail("nav/home missing Insights")

    leaf = ROOT / "trading-bot-development" / "custom-crypto-trading-bots" / "index.html"
    text = leaf.read_text(encoding="utf-8")
    if "<h1>" not in text:
        fail("child page missing h1")
    if text.count("<p>") < 3:
        fail("child page has fewer than 3 paragraphs")
    if "class=\"formbox\"" not in text:
        fail("child page missing inline form")
    for needle in FORBIDDEN:
        if needle in text:
            fail(f"child page contains forbidden leftover {needle!r}")

    insights = list((ROOT / "insights").glob("*/index.html"))
    if len(insights) < 6:
        fail(f"expected >=6 insight articles, got {len(insights)}")
    if not (ROOT / "search" / "index.html").exists():
        fail("missing /search/")
    if not (ROOT / "FACTORY-INSTRUCTION-SET.md").exists():
        fail("missing FACTORY-INSTRUCTION-SET.md")

    print("PASS: factory completeness checks")


if __name__ == "__main__":
    main()
