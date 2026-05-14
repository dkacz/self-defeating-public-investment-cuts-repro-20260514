#!/usr/bin/env python3
"""Local QA for the Mozdzen full-replacement manuscript draft."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_MOZDZEN_FULL_REPLACEMENT_DRAFT_20260514.md"
OUT = ROOT / "qa" / "manuscript_replacement_qa_20260514.csv"


def add(rows: list[dict[str, str]], check: str, status: str, detail: str) -> None:
    rows.append({"check": check, "status": status, "detail": detail})


def count_phrase(text: str, phrase: str) -> int:
    pattern = r"(?<![A-Za-z0-9_])" + re.escape(phrase) + r"(?![A-Za-z0-9_])"
    return len(re.findall(pattern, text, flags=re.IGNORECASE))


def main() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    rows: list[dict[str, str]] = []

    required = {
        "investment import content": "investment import content",
        "household net financial worth": "household net financial worth",
        "real PPP income level": "real PPP income level",
        "h8 import content 1.84": "1.84",
        "h8 net worth 2.16": "2.16",
        "h8 equal average 2.00": "2.00",
        "cut average DSA 5.7": "5.7",
        "real PPP screen p": "p=0.463",
        "combined branch screen p": "p=0.957",
        "Carbonari relevance": "Carbonari, Farcomeni, Maurici and Trovato (2024)",
        "M01 structural balance clarification": "endpoint structural balance is close to -10 percent of GDP",
        "domestic debt definition distinction": "national public-debt concept",
        "KG policy scale translation": "one-percentage-point action is the policy scale",
    }
    for label, needle in required.items():
        add(rows, f"required:{label}", "PASS" if needle in text else "FAIL", needle)

    banned = [
        "replacement branch",
        "this branch",
        "this draft",
        "draft",
        "previous draft",
        "earlier draft",
        "draft evolution",
        "repair history",
        "audit-round",
        "audit round",
        "we previously",
        "previous version",
        "earlier version",
        "old variable",
        "old baseline",
        "accepted baseline",
        "accepted manuscript",
        "final notebook",
        "internal history",
        "repo",
        "artifact",
        "helper",
        "script",
        "raw column",
        "run output",
        "operator",
        "GPT Pro",
        "Pro R1",
        "Pro R2",
        "Pro R3",
        "Pro R4",
        "former household",
        "accepted model",
        "household credit",
        "household liquidity constraints",
        "trade openness",
        "2.82",
        "1.48",
        "12.4",
        "sensitivity only",
        "replacement-baseline",
        "baseline_frozen",
        "tiva2022",
        "FIGARO",
        "F21",
        "F11",
        "F14",
    ]
    for needle in banned:
        count = count_phrase(text, needle)
        add(rows, f"banned:{needle}", "PASS" if count == 0 else "FAIL", f"count={count}")

    image_paths = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
    if image_paths:
        add(rows, "images:present", "PASS", f"count={len(image_paths)}")
    else:
        add(rows, "images:present", "FAIL", "count=0")
    for rel in image_paths:
        path = (MANUSCRIPT.parent / rel).resolve()
        detail = str(path.relative_to(ROOT)) if path.exists() else str((MANUSCRIPT.parent / rel).relative_to(ROOT))
        add(rows, f"image_exists:{rel}", "PASS" if path.exists() else "FAIL", detail)

    fail_count = sum(1 for row in rows if row["status"] == "FAIL")
    add(rows, "overall", "PASS" if fail_count == 0 else "FAIL", f"fail_count={fail_count}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["check", "status", "detail"])
        writer.writeheader()
        writer.writerows(rows)

    if fail_count:
        raise SystemExit(f"FAIL manuscript replacement QA: {fail_count} failures; see {OUT.relative_to(ROOT)}")
    print(f"PASS manuscript replacement QA: {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
