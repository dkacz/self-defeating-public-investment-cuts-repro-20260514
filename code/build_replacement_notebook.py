#!/usr/bin/env python3
"""Build the public reproducibility notebook."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "self_defeating_public_investment_cuts_repro.ipynb"


def md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": text.splitlines(keepends=True),
    }


cells = [
    md(
        """# Self-defeating public investment cuts reproducibility notebook

This notebook reproduces the manuscript-facing tables and checks. It reads only files shipped in this reproducibility package. The state-variable system is investment import content from official OECD TiVA data, public debt, household net financial worth, and real PPP GDP per capita.
"""
    ),
    code(
        """from pathlib import Path
import json
import pandas as pd

ARTIFACT = Path.cwd()
if not (ARTIFACT / 'REPORT.md').exists():
    for parent in Path.cwd().resolve().parents:
        if (parent / 'REPORT.md').exists() and (parent / 'tables').exists():
            ARTIFACT = parent
            break

TABLES = ARTIFACT / 'tables'
RESULTS = ARTIFACT / 'results'
QA = ARTIFACT / 'qa'
FIGURES = ARTIFACT / 'figures'
RESULTS.mkdir(exist_ok=True)
QA.mkdir(exist_ok=True)

checks = []

def record(check, actual, expected, passed=None):
    if passed is None:
        passed = actual == expected
    checks.append({'check': check, 'actual': actual, 'expected': expected, 'passed': bool(passed)})
"""
    ),
    md(
        """## State-variable profile

The first check loads the state-variable table used in the draft and verifies the four-variable universe."""
    ),
    code(
        """state = pd.read_csv(TABLES / 'moz_full_replacement_state_variables.csv')
display(state)

expected_states = {
    'Investment import content',
    'Public debt',
    'Household net financial worth',
    'Real PPP income level',
}
record('four state variables', set(state['State variable']), expected_states)
record('investment import content Poland z', round(float(state.loc[state['State variable'] == 'Investment import content', 'Poland z'].iloc[0]), 3), -0.161)
record('net financial worth Poland z', round(float(state.loc[state['State variable'] == 'Household net financial worth', 'Poland z'].iloc[0]), 3), 0.769)
record('real PPP income Poland z', round(float(state.loc[state['State variable'] == 'Real PPP income level', 'Poland z'].iloc[0]), 3), -0.068)
"""
    ),
    md(
        """## First-stage screen

The retained specifications are investment import content and household net financial worth. Real PPP income remains in the candidate universe but is not retained by the first-stage screen."""
    ),
    code(
        """screen = pd.read_csv(TABLES / 'moz_full_replacement_first_stage_all.csv')
display(screen)

retained = set(screen.loc[screen['Status'] == 'Retained', 'State-variable subset'])
record('retained specifications', retained, {'trade', 'liq'})
real_ppp_p = float(screen.loc[screen['State-variable subset'] == 'log_gdp_pc', 'Output-interaction p-value'].iloc[0])
combined_p = float(screen.loc[screen['State-variable subset'] == 'trade+debt+liq', 'Output-interaction p-value'].iloc[0])
record('real PPP not retained p', round(real_ppp_p, 3), 0.463)
record('combined trade debt liq not retained p', round(combined_p, 3), 0.957)
"""
    ),
    md(
        """## Output and spending responses

The notebook reproduces the horizon-8 output response and the spending response used to normalize the scenario translation."""
    ),
    code(
        """h8 = pd.read_csv(TABLES / 'moz_full_replacement_h8_responses.csv')
paths = pd.read_csv(TABLES / 'moz_full_replacement_response_paths.csv')
display(h8)

selected = paths.loc[paths['Horizon'].isin([0, 2, 5, 8])].copy()
selected.to_csv(RESULTS / 'replacement_notebook_selected_horizons.csv', index=False)
display(selected)

def h8_value(track, col):
    return float(h8.loc[h8['Estimation track'] == track, col].iloc[0])

record('K_Y h8 investment import content', round(h8_value('Polish evaluation based on investment import content', 'K_Y h8'), 2), 1.84)
record('K_Y h8 net financial worth', round(h8_value('Polish evaluation based on household net financial worth', 'K_Y h8'), 2), 2.16)
record('K_Y h8 equal average', round(h8_value('Equal weight average across the two Polish evaluations', 'K_Y h8'), 2), 2.00)
record('K_G h8 equal average', round(h8_value('Equal weight average across the two Polish evaluations', 'K_G h8'), 2), 0.72)
"""
    ),
    md(
        """## Debt endpoint margins

The debt table reports 2036 percentage-point margins relative to the baseline under the institutional debt equation and under the direct debt-to-GDP local-projection path."""
    ),
    code(
        """debt = pd.read_csv(TABLES / 'moz_full_replacement_debt_2036.csv')
debt.to_csv(RESULTS / 'replacement_notebook_debt_margins_2036.csv', index=False)
display(debt)

def debt_value(path, col):
    return float(debt.loc[debt['Empirical path'] == path, col].iloc[0])

record('cut DSA investment import content', round(debt_value('Polish evaluation based on investment import content', 'Cut, institutional debt equation'), 1), 4.9)
record('cut direct investment import content', round(debt_value('Polish evaluation based on investment import content', 'Cut, direct debt-to-GDP local-projection path'), 1), 1.7)
record('cut DSA net financial worth', round(debt_value('Polish evaluation based on household net financial worth', 'Cut, institutional debt equation'), 1), 6.5)
record('cut direct net financial worth', round(debt_value('Polish evaluation based on household net financial worth', 'Cut, direct debt-to-GDP local-projection path'), 1), 4.3)
record('cut DSA equal average', round(debt_value('Equal weight average across the two Polish evaluations', 'Cut, institutional debt equation'), 1), 5.7)
record('cut direct equal average', round(debt_value('Equal weight average across the two Polish evaluations', 'Cut, direct debt-to-GDP local-projection path'), 1), 3.0)
record('debt table rows', len(debt), 4)
record('EU27 benchmark row present', 'EU27 panel benchmark' in set(debt['Empirical path']), True)
record('cut DSA EU27 benchmark', round(debt_value('EU27 panel benchmark', 'Cut, institutional debt equation'), 1), 7.0)
record('cut direct EU27 benchmark', round(debt_value('EU27 panel benchmark', 'Cut, direct debt-to-GDP local-projection path'), 1), 3.7)
"""
    ),
    md(
        """## Figure and QA ledger

The figures are generated outside the notebook by the reproducibility script and checked here for presence. The final cell writes the notebook QA ledger."""
    ),
    code(
        """for figure_name in [
    'figure_intro_dsa_baseline_path.png',
    'moz_full_replacement_ky_paths.png',
    'moz_full_replacement_cut_dsa_margin.png',
]:
    record(f'figure exists: {figure_name}', (FIGURES / figure_name).exists(), True)

check_summary = pd.DataFrame(checks)
check_summary.to_csv(RESULTS / 'replacement_notebook_check_summary.csv', index=False)
display(check_summary)

if not check_summary['passed'].all():
    raise AssertionError('Notebook checks failed')
"""
    ),
]


notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "pygments_lexer": "ipython3"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}


def main() -> None:
    NOTEBOOK.parent.mkdir(parents=True, exist_ok=True)
    NOTEBOOK.write_text(json.dumps(notebook, indent=2) + "\n", encoding="utf-8")
    print(NOTEBOOK)


if __name__ == "__main__":
    main()
