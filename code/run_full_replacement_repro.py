#!/usr/bin/env python3
"""Run the local reproducibility chain for the Mozdzen full replacement branch."""

from __future__ import annotations

import csv
import hashlib
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT / "code"
QA = ROOT / "qa"
RESULTS = ROOT / "results"
PROV = ROOT / "data/provenance"

SCRIPT_STEPS = [
    ("rebuild_adopted_state_variables_from_sources.py", []),
    ("build_adopted_variant_summary.py", []),
    ("build_replacement_tables_figures.py", []),
    ("check_manuscript_replacement_qa.py", []),
    ("build_replacement_notebook.py", []),
    ("execute_replacement_notebook.py", [str(ROOT / "notebooks/self_defeating_public_investment_cuts_repro.ipynb")]),
]

QA_FILES = [
    QA / "source_rebuild_adopted_state_variables_qa_20260514.csv",
    QA / "adopted_variant_summary_qa_20260514.csv",
    QA / "replacement_tables_figures_qa_20260514.csv",
    QA / "manuscript_replacement_qa_20260514.csv",
    RESULTS / "replacement_notebook_check_summary.csv",
]

FROZEN_DIRS = [
    ROOT / "data/frozen/adopted_sources",
    ROOT / "data/frozen/adopted_model_inputs",
    ROOT / "data/frozen/adopted_run_outputs",
    ROOT / "data/frozen/eu27_benchmark_debt",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_manifest() -> None:
    rows = []
    for folder in FROZEN_DIRS:
        for path in sorted(p for p in folder.rglob("*") if p.is_file()):
            rows.append(
                {
                    "path": str(path.relative_to(ROOT)),
                    "bytes": path.stat().st_size,
                    "sha256": sha256(path),
                }
            )
    PROV.mkdir(parents=True, exist_ok=True)
    out = PROV / "adopted_branch_frozen_inputs_manifest_20260514.csv"
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["path", "bytes", "sha256"])
        writer.writeheader()
        writer.writerows(rows)


def refresh_feature_screen_manifest() -> None:
    manifest = ROOT / "data/frozen/adopted_run_outputs/feature_screen/source_manifest.csv"
    rows = []
    for folder in [ROOT / "data/frozen/adopted_model_inputs", ROOT / "data/frozen/adopted_run_outputs/feature_screen"]:
        for path in sorted(p for p in folder.rglob("*") if p.is_file()):
            if path == manifest:
                continue
            rows.append(
                {
                    "path": str(path.relative_to(ROOT)),
                    "sha256": sha256(path),
                    "bytes": path.stat().st_size,
                }
            )
    with manifest.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["path", "sha256", "bytes"])
        writer.writeheader()
        writer.writerows(rows)


def refresh_notebook_manifest() -> None:
    rows = [
        ("code/build_replacement_notebook.py", "notebook builder"),
        ("code/execute_replacement_notebook.py", "notebook execution checker"),
        ("notebooks/self_defeating_public_investment_cuts_repro.ipynb", "public reproducibility notebook"),
        ("results/replacement_notebook_check_summary.csv", "notebook QA ledger"),
        ("results/replacement_notebook_selected_horizons.csv", "notebook selected-horizon output table"),
        ("results/replacement_notebook_debt_margins_2036.csv", "notebook debt endpoint output table"),
        ("qa/replacement_notebook_execution_log.txt", "notebook execution log"),
    ]
    out = RESULTS / "replacement_notebook_manifest_20260514.csv"
    manifest_rows = []
    for rel_path, role in rows:
        path = ROOT / rel_path
        if not path.exists():
            raise FileNotFoundError(f"missing notebook manifest input: {rel_path}")
        manifest_rows.append({"path": rel_path, "role": role, "sha256": sha256(path)})
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["path", "role", "sha256"])
        writer.writeheader()
        writer.writerows(manifest_rows)


def validate_manifest(manifest: Path, base: Path, path_col: str) -> dict[str, str]:
    if not manifest.exists():
        return {
            "check": f"manifest_valid:{manifest.relative_to(ROOT)}",
            "status": "FAIL",
            "detail": "missing_manifest",
        }
    with manifest.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    bad: list[str] = []
    for row in rows:
        rel_path = row.get(path_col, "")
        target = base / rel_path
        if not target.exists():
            bad.append(f"missing:{rel_path}")
            continue
        expected_hash = row.get("sha256", "")
        if expected_hash and expected_hash != sha256(target):
            bad.append(f"sha256:{rel_path}")
        expected_bytes = row.get("bytes", "")
        if expected_bytes and str(target.stat().st_size) != str(expected_bytes):
            bad.append(f"bytes:{rel_path}")
    return {
        "check": f"manifest_valid:{manifest.relative_to(ROOT)}",
        "status": "PASS" if not bad else "FAIL",
        "detail": f"rows={len(rows)} bad={len(bad)}" + ("" if not bad else f" first={bad[0]}"),
    }


def latest_packet_manifest() -> tuple[Path, Path] | None:
    manifests = sorted(ROOT.glob("pro_review/r*_20260514/PACKET_MANIFEST_MOZDZEN_FULL_REPLACEMENT_R*.csv"))
    if not manifests:
        return None
    manifest = manifests[-1]
    return manifest, manifest.parent / "packet_input"


def manifest_validation_rows() -> list[dict[str, str]]:
    rows = [
        validate_manifest(PROV / "adopted_sources_manifest_20260514.csv", ROOT, "path"),
        validate_manifest(PROV / "adopted_branch_frozen_inputs_manifest_20260514.csv", ROOT, "path"),
        validate_manifest(RESULTS / "adopted_variant_summary_manifest_20260514.csv", ROOT, "path"),
        validate_manifest(RESULTS / "replacement_notebook_manifest_20260514.csv", ROOT, "path"),
        validate_manifest(ROOT / "data/frozen/adopted_run_outputs/feature_screen/source_manifest.csv", ROOT, "path"),
    ]
    packet = latest_packet_manifest()
    if packet is None:
        rows.append({"check": "manifest_valid:latest_packet_manifest", "status": "PASS", "detail": "not_yet_built"})
    else:
        manifest, base = packet
        rows.append(validate_manifest(manifest, base, "packet_path"))
    return rows


def run_script(name: str, args: list[str]) -> dict[str, str]:
    proc = subprocess.run(
        [sys.executable, str(CODE / name), *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return {
        "script": name,
        "status": "PASS" if proc.returncode == 0 else "FAIL",
        "returncode": str(proc.returncode),
        "output_tail": proc.stdout[-800:].replace(str(ROOT), ".").replace("\n", " | "),
    }


def qa_passes(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, "missing"
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        return False, "empty"
    fields = rows[0].keys()
    if "status" in fields:
        bad = [row for row in rows if row.get("status") != "PASS"]
        return not bad, f"rows={len(rows)} bad={len(bad)}"
    if "passed" in fields:
        bad = [row for row in rows if str(row.get("passed")).lower() != "true"]
        return not bad, f"rows={len(rows)} bad={len(bad)}"
    return False, "no status/passed column"


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    refresh_feature_screen_manifest()
    write_manifest()
    run_rows = [run_script(name, args) for name, args in SCRIPT_STEPS]
    refresh_notebook_manifest()
    write_csv(QA / "full_replacement_repro_run_log_20260514.csv", run_rows, ["script", "status", "returncode", "output_tail"])

    qa_rows = []
    for path in QA_FILES:
        ok, detail = qa_passes(path)
        qa_rows.append(
            {
                "check": f"qa_passes:{path.relative_to(ROOT)}",
                "status": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    external_refs = []
    for script in [CODE / "build_replacement_tables_figures.py"]:
        text = script.read_text(encoding="utf-8")
        for banned in ["ROOT.parent", "mozdzen_figaro_tiva_extension_20260514"]:
            if banned in text:
                external_refs.append(f"{script.relative_to(ROOT)}:{banned}")
    qa_rows.append(
        {
            "check": "no_external_parent_dependency_in_table_builder",
            "status": "PASS" if not external_refs else "FAIL",
            "detail": ";".join(external_refs),
        }
    )
    qa_rows.extend(manifest_validation_rows())

    write_csv(QA / "full_replacement_repro_qa_20260514.csv", qa_rows, ["check", "status", "detail"])
    failures = [row for row in run_rows if row["status"] != "PASS"] + [row for row in qa_rows if row["status"] != "PASS"]
    if failures:
        raise SystemExit(f"full replacement reproducibility failed: {failures}")
    print("full replacement reproducibility PASS")


if __name__ == "__main__":
    main()
