#!/usr/bin/env python3
"""Build manuscript tables and simple figures for the Mozdzen replacement draft."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RUN_OUTPUTS = ROOT / "data/frozen/adopted_run_outputs"
INPUTS = ROOT / "data/frozen/adopted_model_inputs"
EU27_BENCHMARK_DEBT = ROOT / "data/frozen/eu27_benchmark_debt/eu27_benchmark_debt_2036.csv"

TABLES = ROOT / "tables"
FIGURES = ROOT / "figures"
QA = ROOT / "qa"
for path in [TABLES, FIGURES, QA]:
    path.mkdir(parents=True, exist_ok=True)


def write_table(df: pd.DataFrame, stem: str) -> None:
    df.to_csv(TABLES / f"{stem}.csv", index=False)
    (TABLES / f"{stem}.md").write_text(df.to_markdown(index=False) + "\n", encoding="utf-8")


def fmt(v: float, digits: int = 2, signed: bool = False) -> str:
    if signed:
        return f"{v:+.{digits}f}"
    return f"{v:.{digits}f}"


def build_state_table() -> pd.DataFrame:
    panel = pd.read_csv(INPUTS / "country_feature_panel.csv")
    pol = panel[(panel["country"] == "POL") & (panel["year"] == 2022)].iloc[0]
    trans = pd.read_csv(INPUTS / "variant_transformations.csv").set_index("raw_column")
    debt_std = pd.read_csv(INPUTS / "state_variable_standardization_current.csv").set_index("raw_column")

    rows = [
        {
            "State variable": "Investment import content",
            "Measure": "Import content of gross fixed capital formation, from OECD TiVA domestic value-added shares",
            "Source": "OECD TiVA 2025, GFCF_VA_SH",
            "Mean": fmt(trans.loc["trade_raw", "mean"], 3),
            "SD": fmt(trans.loc["trade_raw", "sd"], 3),
            "N": "513",
            "Poland value": fmt(pol["trade_raw"], 3),
            "Poland z": fmt(pol["trade_z"], 3, signed=True),
        },
        {
            "State variable": "Public debt",
            "Measure": "Maastricht gross debt, percent of GDP",
            "Source": "Eurostat government debt",
            "Mean": fmt(debt_std.loc["debt_raw", "mean"], 1),
            "SD": fmt(debt_std.loc["debt_raw", "sd"], 1),
            "N": "567",
            "Poland value": fmt(pol["debt_raw"], 1),
            "Poland z": fmt(pol["debt_z"], 3, signed=True),
        },
        {
            "State variable": "Household net financial worth",
            "Measure": "Negative household net financial worth divided by nominal GDP",
            "Source": "Eurostat financial accounts and nominal GDP",
            "Mean": fmt(trans.loc["liq_raw", "mean"], 3),
            "SD": fmt(trans.loc["liq_raw", "sd"], 3),
            "N": "513",
            "Poland value": fmt(pol["liq_raw"], 3),
            "Poland z": fmt(pol["liq_z"], 3, signed=True),
        },
        {
            "State variable": "Real PPP income level",
            "Measure": "Log real GDP per capita in 2020 PPS terms",
            "Source": "Eurostat national accounts",
            "Mean": fmt(trans.loc["log_gdp_pc_raw", "mean"], 3),
            "SD": fmt(trans.loc["log_gdp_pc_raw", "sd"], 3),
            "N": "513",
            "Poland value": fmt(pol["log_gdp_pc_raw"], 3),
            "Poland z": fmt(pol["log_gdp_pc_z"], 3, signed=True),
        },
    ]
    df = pd.DataFrame(rows)
    write_table(df, "moz_full_replacement_state_variables")
    return df


def build_first_stage_tables() -> pd.DataFrame:
    fs = pd.read_csv(RUN_OUTPUTS / "feature_screen" / "feature_robustness_summary.csv")
    keep = fs[
        [
            "spec_id",
            "features",
            "p_wald_y_h8",
            "mahalanobis_support_p",
            "max_abs_poland_z",
            "loo_ok_count",
            "boot_ok_count",
            "time_ok_count",
            "gate_status",
        ]
    ].copy()
    keep["p_wald_y_h8"] = keep["p_wald_y_h8"].map(lambda x: fmt(x, 3))
    keep["mahalanobis_support_p"] = keep["mahalanobis_support_p"].map(lambda x: fmt(x, 3))
    keep["max_abs_poland_z"] = keep["max_abs_poland_z"].map(lambda x: fmt(x, 3))
    keep["stability"] = (
        keep["loo_ok_count"].astype(str)
        + "/27; "
        + keep["boot_ok_count"].astype(str)
        + "/19; "
        + keep["time_ok_count"].astype(str)
        + "/3"
    )
    keep["Status"] = keep["gate_status"].map(
        {"PASS_ROBUSTNESS_GATE": "Retained", "FAIL_ROBUSTNESS_GATE": "Not retained"}
    )
    out = keep[
        [
            "spec_id",
            "features",
            "p_wald_y_h8",
            "mahalanobis_support_p",
            "max_abs_poland_z",
            "stability",
            "Status",
        ]
    ].rename(
        columns={
            "spec_id": "Spec ID",
            "features": "State-variable subset",
            "p_wald_y_h8": "Output-interaction p-value",
            "mahalanobis_support_p": "Support p-value",
            "max_abs_poland_z": "Max abs Poland z",
        }
    )
    write_table(out, "moz_full_replacement_first_stage_all")
    retained = out[out["Status"] == "Retained"].copy()
    write_table(retained, "moz_full_replacement_first_stage_retained")
    return out


def build_response_tables() -> pd.DataFrame:
    paths = pd.read_csv(RUN_OUTPUTS / "polish_output_spending" / "polish_output_spending_paths.csv")
    piv = paths.pivot_table(
        index="horizon",
        columns="features",
        values=["K_Y_cumulative", "K_G_cumulative"],
        aggfunc="first",
    )
    out = pd.DataFrame({"Horizon": list(range(9))})
    for feature, label in [("trade", "Investment import content"), ("liq", "Net financial worth")]:
        out[f"{label} K_Y"] = [fmt(piv.loc[h, ("K_Y_cumulative", feature)], 2) for h in range(9)]
        out[f"{label} K_G"] = [fmt(piv.loc[h, ("K_G_cumulative", feature)], 2) for h in range(9)]
    out["Equal-weight K_Y"] = [
        fmt((piv.loc[h, ("K_Y_cumulative", "trade")] + piv.loc[h, ("K_Y_cumulative", "liq")]) / 2, 2)
        for h in range(9)
    ]
    out["Equal-weight K_G"] = [
        fmt((piv.loc[h, ("K_G_cumulative", "trade")] + piv.loc[h, ("K_G_cumulative", "liq")]) / 2, 2)
        for h in range(9)
    ]
    write_table(out, "moz_full_replacement_response_paths")

    h8 = out[out["Horizon"] == 8].iloc[0]
    headline = pd.DataFrame(
        [
            ["EU27 panel benchmark", "Common EU27 response without state interactions", "2.11", "n/a"],
            [
                "Polish evaluation based on investment import content",
                "Official TiVA GFCF import-content profile",
                h8["Investment import content K_Y"],
                h8["Investment import content K_G"],
            ],
            [
                "Polish evaluation based on household net financial worth",
                "Eurostat financial-accounts balance-sheet profile",
                h8["Net financial worth K_Y"],
                h8["Net financial worth K_G"],
            ],
            [
                "Equal weight average across the two Polish evaluations",
                "Arithmetic average of the two retained Polish paths",
                h8["Equal-weight K_Y"],
                h8["Equal-weight K_G"],
            ],
        ],
        columns=["Estimation track", "Country characteristics used for evaluation", "K_Y h8", "K_G h8"],
    )
    write_table(headline, "moz_full_replacement_h8_responses")
    return paths


def build_debt_table() -> pd.DataFrame:
    debt = pd.read_csv(RUN_OUTPUTS / "debt_accounting" / "polish_debt_2036_summary.csv")
    eu27 = pd.read_csv(EU27_BENCHMARK_DEBT).iloc[0]

    def val(feature: str, sign: str, col: str) -> float:
        row = debt[(debt["features"] == feature) & (debt["scenario_sign"] == sign)].iloc[0]
        return float(row[col])

    rows = [
        [
            eu27["empirical_path"],
            fmt(float(eu27["expansion_institutional_debt_equation"]), 1, signed=True),
            fmt(float(eu27["expansion_direct_debt_to_gdp_lp_path"]), 1, signed=True),
            fmt(float(eu27["cut_institutional_debt_equation"]), 1, signed=True),
            fmt(float(eu27["cut_direct_debt_to_gdp_lp_path"]), 1, signed=True),
        ]
    ]
    for label, feature in [
        ("Polish evaluation based on investment import content", "trade"),
        ("Polish evaluation based on household net financial worth", "liq"),
    ]:
        rows.append(
            [
                label,
                fmt(val(feature, "expansion", "dsa_margin_vs_baseline_pp"), 1, signed=True),
                fmt(val(feature, "expansion", "direct_DY_LP_margin_pp"), 1, signed=True),
                fmt(val(feature, "cut", "dsa_margin_vs_baseline_pp"), 1, signed=True),
                fmt(val(feature, "cut", "direct_DY_LP_margin_pp"), 1, signed=True),
            ]
        )
    rows.append(
        [
            "Equal weight average across the two Polish evaluations",
            fmt((val("trade", "expansion", "dsa_margin_vs_baseline_pp") + val("liq", "expansion", "dsa_margin_vs_baseline_pp")) / 2, 1, signed=True),
            fmt((val("trade", "expansion", "direct_DY_LP_margin_pp") + val("liq", "expansion", "direct_DY_LP_margin_pp")) / 2, 1, signed=True),
            fmt((val("trade", "cut", "dsa_margin_vs_baseline_pp") + val("liq", "cut", "dsa_margin_vs_baseline_pp")) / 2, 1, signed=True),
            fmt((val("trade", "cut", "direct_DY_LP_margin_pp") + val("liq", "cut", "direct_DY_LP_margin_pp")) / 2, 1, signed=True),
        ]
    )
    out = pd.DataFrame(
        rows,
        columns=[
            "Empirical path",
            "Expansion, institutional debt equation",
            "Expansion, direct debt-to-GDP local-projection path",
            "Cut, institutional debt equation",
            "Cut, direct debt-to-GDP local-projection path",
        ],
    )
    write_table(out, "moz_full_replacement_debt_2036")
    return out


def build_figures(paths: pd.DataFrame) -> None:
    labels = {"trade": "Investment import content", "liq": "Net financial worth"}
    fig, ax = plt.subplots(figsize=(6.5, 4))
    for feature, label in labels.items():
        sub = paths[paths["features"] == feature]
        ax.plot(sub["horizon"], sub["K_Y_cumulative"], marker="o", label=label)
    avg = paths.groupby("horizon", as_index=False)["K_Y_cumulative"].mean()
    ax.plot(avg["horizon"], avg["K_Y_cumulative"], marker="o", linestyle="--", label="Equal-weight average")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xlabel("Horizon")
    ax.set_ylabel("Cumulative output response")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES / "moz_full_replacement_ky_paths.png", dpi=200)
    plt.close(fig)

    debt_paths = pd.read_csv(RUN_OUTPUTS / "debt_accounting" / "dsa_debt_paths.csv")
    fig, ax = plt.subplots(figsize=(6.5, 4))
    for feature, label in labels.items():
        sub = debt_paths[(debt_paths["features"] == feature) & (debt_paths["scenario_sign"] == "cut")]
        ax.plot(sub["year"], sub["dsa_margin_vs_baseline_pp"], marker="o", label=f"{label}, cut")
    avg_cut = (
        debt_paths[debt_paths["scenario_sign"] == "cut"]
        .groupby("year", as_index=False)["dsa_margin_vs_baseline_pp"]
        .mean()
    )
    ax.plot(avg_cut["year"], avg_cut["dsa_margin_vs_baseline_pp"], marker="o", linestyle="--", label="Equal-weight, cut")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xlabel("Year")
    ax.set_ylabel("Debt-to-GDP margin versus baseline, pp")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES / "moz_full_replacement_cut_dsa_margin.png", dpi=200)
    plt.close(fig)


def main() -> None:
    required_inputs = [
        INPUTS / "country_feature_panel.csv",
        INPUTS / "variant_transformations.csv",
        INPUTS / "state_variable_standardization_current.csv",
        RUN_OUTPUTS / "feature_screen" / "feature_robustness_summary.csv",
        RUN_OUTPUTS / "polish_output_spending" / "polish_output_spending_paths.csv",
        RUN_OUTPUTS / "debt_accounting" / "polish_debt_2036_summary.csv",
        RUN_OUTPUTS / "debt_accounting" / "dsa_debt_paths.csv",
        EU27_BENCHMARK_DEBT,
    ]
    missing = [str(path.relative_to(ROOT)) for path in required_inputs if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing frozen adopted inputs: {missing}")

    state = build_state_table()
    screen = build_first_stage_tables()
    paths = build_response_tables()
    debt = build_debt_table()
    build_figures(paths)

    qa_rows = [
        {"check": "state_rows", "status": "PASS" if len(state) == 4 else "FAIL", "detail": str(len(state))},
        {"check": "screen_rows", "status": "PASS" if len(screen) == 15 else "FAIL", "detail": str(len(screen))},
        {
            "check": "retained_specs",
            "status": "PASS"
            if set(screen.loc[screen["Status"] == "Retained", "Spec ID"]) == {"F01", "F03"}
            else "FAIL",
            "detail": ",".join(screen.loc[screen["Status"] == "Retained", "Spec ID"]),
        },
        {"check": "debt_rows", "status": "PASS" if len(debt) == 4 else "FAIL", "detail": str(len(debt))},
        {
            "check": "debt_table_includes_eu27_benchmark",
            "status": "PASS" if "EU27 panel benchmark" in set(debt["Empirical path"]) else "FAIL",
            "detail": ",".join(debt["Empirical path"]),
        },
        {
            "check": "uses_local_frozen_inputs",
            "status": "PASS" if not missing else "FAIL",
            "detail": "data/frozen/adopted_model_inputs + data/frozen/adopted_run_outputs",
        },
    ]
    pd.DataFrame(qa_rows).to_csv(QA / "replacement_tables_figures_qa_20260514.csv", index=False)
    failures = [row for row in qa_rows if row["status"] != "PASS"]
    if failures:
        raise SystemExit(f"QA failed: {failures}")
    print("replacement tables and figures built")


if __name__ == "__main__":
    main()
