# Public reproducibility package

Date: 2026-05-14

This package reproduces the manuscript-facing empirical results for the paper
`Self-Defeating Public Investment Cuts: Evidence from Poland under EU Fiscal
Surveillance`.

The state-variable system uses:

- investment import content from official OECD TiVA GFCF data;
- public debt;
- household net financial worth;
- real PPP GDP per capita.

The retained Polish evaluations are investment import content and household
net financial worth. The package ships frozen source extracts, frozen model
inputs, frozen run outputs, provenance manifests, table and figure builders,
the explanatory Jupyter notebook, and local quality-assurance ledgers.

## Headline values

| Quantity | Value |
| --- | ---: |
| Horizon-8 EU27 output response | 2.11 |
| Horizon-8 investment-import-content Polish response | 1.84 |
| Horizon-8 household-net-financial-worth Polish response | 2.16 |
| Horizon-8 equal-weight Polish response | 2.00 |
| 2036 cut margin, equal-weight institutional debt equation | +5.7 pp |
| 2036 cut margin, equal-weight direct debt-to-GDP path | +3.0 pp |

## How to run

From the package root:

```bash
python3 code/run_full_replacement_repro.py
```

A successful run prints:

```text
full replacement reproducibility PASS
```

The main notebook is:

```text
notebooks/self_defeating_public_investment_cuts_repro.ipynb
```

Local quality-assurance results are recorded in
`qa/full_replacement_repro_qa_20260514.csv` and
`results/replacement_notebook_check_summary.csv`.
