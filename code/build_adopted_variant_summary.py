#!/usr/bin/env python3
"""Build compact operator-facing summary for the Mozdzen replacement branch."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRID = ROOT / "references/upstream_results/variant_grid_summary_from_mozdzen_figaro_tiva_extension_20260514.csv"
CASH_GRID = ROOT / "references/upstream_results/variant_grid_summary_from_cash_transferable_trial_20260514.csv"
OUT_CSV = ROOT / "results/adopted_variant_summary_20260514.csv"
OUT_MD = ROOT / "results/adopted_variant_summary_20260514.md"
OUT_QA = ROOT / "qa/adopted_variant_summary_qa_20260514.csv"
OUT_MANIFEST = ROOT / "results/adopted_variant_summary_manifest_20260514.csv"


SELECTED = [
    ("baseline_frozen_control", "previous_frozen_baseline", "Comparison baseline from accepted clean repro."),
    ("baseline_current_control", "current_control", "Current control in the upstream grid."),
    (
        "tiva2022_gfcf_realppp_networth",
        "adopted_mozdzen_branch",
        "Official TiVA GFCF import-content + real PPP income + household net financial worth.",
    ),
    (
        "tiva2022_gfcf_paper_networth",
        "networth_without_realppp",
        "Diagnostic: same trade/liquidity replacement, old paper income construction.",
    ),
    (
        "tiva2022_gfcf_realppp_credit",
        "old_credit_with_realppp_tiva",
        "Diagnostic: keeps old household-credit liquidity proxy.",
    ),
    (
        "figaro2023_gfcf_realppp_networth",
        "figaro_diagnostic",
        "Diagnostic: newer FIGARO-derived import-content source, not the adopted Mozdzen branch.",
    ),
    (
        "tiva_cf2024_gfcf_realppp_networth",
        "carry_forward_diagnostic",
        "Diagnostic: mechanical carry-forward to 2024, not official OECD data.",
    ),
]

CASH_SELECTED = [
    (
        "tiva2022_gfcf_realppp_cash_transferable",
        "cash_transferable_diagnostic",
        "Diagnostic: literal cash plus transferable deposits liquidity, not the adopted Mozdzen branch.",
    )
]

NUMERIC_FIELDS = [
    "K_Y_h8",
    "K_G_h8",
    "dsa_margin_2036_cut_pp",
    "direct_dy_margin_2036_cut_pp",
    "dsa_margin_2036_expansion_pp",
    "direct_dy_margin_2036_expansion_pp",
]

OUTPUT_FIELDS = [
    "role",
    "variant",
    "lane",
    "measure",
    "income_key",
    "liq_key",
    "profile_year",
    "sample_end_year",
    "pass_count",
    "passing_specs",
    *NUMERIC_FIELDS,
    "note",
]


def read_rows(path: Path) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return {row["variant"]: row for row in csv.DictReader(handle)}


def with_role(row: dict[str, str], role: str, note: str) -> dict[str, str]:
    out = {field: row.get(field, "") for field in OUTPUT_FIELDS}
    out["role"] = role
    out["note"] = note
    return out


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: str) -> str:
    return value.replace("|", "\\|")


def write_md(path: Path, rows: list[dict[str, str]]) -> None:
    cols = [
        "role",
        "variant",
        "passing_specs",
        "K_Y_h8",
        "K_G_h8",
        "dsa_margin_2036_cut_pp",
        "direct_dy_margin_2036_cut_pp",
        "dsa_margin_2036_expansion_pp",
        "direct_dy_margin_2036_expansion_pp",
        "note",
    ]
    lines = [
        "# Adopted Variant Summary - Mozdzen Full Replacement Branch",
        "",
        "This table separates the adopted three-variable Mozdzen branch from diagnostics. Values are copied from upstream local grids and remain pre-Pro until the full branch audit closes.",
        "",
        "|" + "|".join(cols) + "|",
        "|" + "|".join(["---"] * len(cols)) + "|",
    ]
    for row in rows:
        lines.append("|" + "|".join(md_escape(row.get(col, "")) for col in cols) + "|")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    grid = read_rows(GRID)
    cash_grid = read_rows(CASH_GRID)
    rows: list[dict[str, str]] = []
    qa_rows: list[dict[str, str]] = []

    for variant, role, note in SELECTED:
        found = variant in grid
        qa_rows.append({"check": f"variant_present:{variant}", "status": "PASS" if found else "FAIL", "detail": str(GRID.relative_to(ROOT))})
        if found:
            rows.append(with_role(grid[variant], role, note))

    for variant, role, note in CASH_SELECTED:
        found = variant in cash_grid
        qa_rows.append({"check": f"variant_present:{variant}", "status": "PASS" if found else "FAIL", "detail": str(CASH_GRID.relative_to(ROOT))})
        if found:
            rows.append(with_role(cash_grid[variant], role, note))

    adopted = next((row for row in rows if row["role"] == "adopted_mozdzen_branch"), None)
    qa_rows.append(
        {
            "check": "adopted_variant_passes_two_specs",
            "status": "PASS" if adopted and adopted["passing_specs"] == "F01+F03" else "FAIL",
            "detail": adopted["passing_specs"] if adopted else "missing",
        }
    )
    qa_rows.append(
        {
            "check": "adopted_variant_uses_official_tiva_gfcf_realppp_networth",
            "status": "PASS"
            if adopted
            and adopted["lane"] == "tiva2022"
            and adopted["measure"] == "gfcf"
            and adopted["income_key"] == "realppp"
            and adopted["liq_key"] == "networth"
            else "FAIL",
            "detail": "" if adopted else "missing",
        }
    )

    write_csv(OUT_CSV, rows, OUTPUT_FIELDS)
    write_md(OUT_MD, rows)
    write_csv(OUT_QA, qa_rows, ["check", "status", "detail"])

    manifest_rows = []
    for path in [GRID, CASH_GRID, OUT_CSV, OUT_MD, OUT_QA]:
        manifest_rows.append(
            {
                "path": str(path.relative_to(ROOT)),
                "bytes": str(path.stat().st_size),
                "sha256": sha256(path),
            }
        )
    write_csv(OUT_MANIFEST, manifest_rows, ["path", "bytes", "sha256"])

    failures = [row for row in qa_rows if row["status"] != "PASS"]
    if failures:
        raise SystemExit(f"QA failed: {failures}")
    print(f"wrote {OUT_CSV.relative_to(ROOT)} rows={len(rows)}")


if __name__ == "__main__":
    main()
