# Public Reproducibility Release QA

Date: 2026-05-14

## Public Links

- Landing page: https://dkacz.github.io/self-defeating-public-investment-cuts-repro-20260514/
- Repository: https://github.com/dkacz/self-defeating-public-investment-cuts-repro-20260514
- Notebook: https://github.com/dkacz/self-defeating-public-investment-cuts-repro-20260514/blob/main/notebooks/self_defeating_public_investment_cuts_repro.ipynb

## Published Object

- GitHub owner/repo: `dkacz/self-defeating-public-investment-cuts-repro-20260514`
- Visibility: public
- Published commit: `db0de1dee4420b7fe219791ad78c16aa8a10bc7d`
- GitHub Pages source: `main:/docs`
- GitHub Pages build status: `built`

## Local Release Checks

- Public release directory: `artifacts/action_tasks/manuscript_imrad_20260427/public_repro_release_mozdzen_20260514/`
- Published file count: 105 after adding the landing page.
- Local file count: 106 including this QA report.
- Approximate size: 7.5 MB.
- Full local reproducibility command from the release root returned:

```text
full replacement reproducibility PASS
```

- Visible public ZIP/PDF files in the release directory: none.
- Public notebook directory contains one notebook:

```text
notebooks/self_defeating_public_investment_cuts_repro.ipynb
```

## Public-Label Repair

After the initial publication, the public first-stage table and notebook still exposed the internal shorthand labels `trade`, `liq`, and `log_gdp_pc`. The public release package was repaired locally on 2026-05-14 so that public tables and the notebook use manuscript-facing labels:

- `investment import content`;
- `household net financial worth`;
- `public debt`;
- `real PPP income`.

The full local release runner was rerun after the repair and returned:

```text
full replacement reproducibility PASS
```

The notebook QA ledger now has 24/24 passing checks and verifies retained specifications as `investment import content` plus `household net financial worth`. A scan of `tables/`, `notebooks/`, and `docs/` finds no public-table/notebook occurrences of raw `trade`, `liq`, or `log_gdp_pc` labels.

Current repaired local hashes:

```text
6e78ed3a1b9df568a53f06540df21883f39691625071452114d7cd53ddf073b4  notebooks/self_defeating_public_investment_cuts_repro.ipynb
87caa58ebeed9bd488403308d9b193eb3f3ef5b754c44cd236742c666f4223e6  tables/moz_full_replacement_first_stage_all.csv
```

## Strategic Status

The public notebook/repository gate is closed locally after the public-label
repair. It still requires pushing the repaired package to the public GitHub
repository before the WhatsApp link can be treated as final. This does not close
the full replacement goal by itself: targeted GPT Pro R8 harvest, WhatsApp
dispatch text, Boox annotation triage after export, and final git cleanup remain
separate gates.
