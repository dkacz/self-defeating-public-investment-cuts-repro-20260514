# State-variable screen

## Scope

This public reproduction block evaluates the feature-combination selection step for the Polish heterogeneity model. It starts from the four-feature literature universe `trade/debt/liq/log_gdp_pc` and enumerates all `15` non-empty subsets.

The script is deliberately ordered as a single selection exercise:

1. enumerate all feature subsets;
2. estimate output and spending kernels for every subset;
3. apply robustness criteria that use first-stage diagnostics only, with no later accounting results, no later-stage signs, no output-only fit ranking and no kernel-sign filters.

This public reproduction block does not calculate later accounting paths. Those estimates for the selected specifications belong to later modelling blocks.

## Robustness criteria

| criterion | local_reference | use |
| --- | --- | --- |
| ex_ante_feature_universe | references/papers_txt/ilzetzki_mendoza_vegh_2013_fiscal_multipliers.txt; references/papers_txt/huidrom_kose_lim_ohnsorge_2019_why_fiscal_positions.txt; references/papers_txt/bernardini_peersman_2017_heterogeneous_multipliers.txt; references/papers_txt/krajewski_pilat_2025_liquidity_constraints_poland.txt; references/papers_txt/mcmanus_ozkan_trzeciakiewicz_2020_credit_constraints.txt | Justifies trade openness, public debt, level of development and the Polish liquidity or credit-constraint extension. |
| local_projection_core | references/papers_txt/jorda_2005_aer_lp.txt; references/papers_txt/ciaffi_2024_jpm_fiscal_debt.txt | Justifies local projections estimated separately at each horizon and separate output and debt responses. |
| shock_feature_interactions | references/papers_txt/auerbach_gorodnichenko_2012_output_responses.txt; references/papers_txt/ramey_zubairy_2018_multipliers_good_bad.txt; references/papers_txt/cloyne_jorda_taylor_2023_state_dependent_lp.txt | Justifies interacting fiscal shocks with state or country characteristics. |
| common_sample | pre-specified notebook design rule | Candidate specifications are compared on the same h8 observation universe where feasible. The model-averaging papers remain model-uncertainty context, not direct support for this fixed-sample rule. |
| rank_condition_collinearity | references/papers_txt/welsch_kuh_1977_linear_regression_diagnostics_nber.txt | Regression diagnostic hygiene: full rank, condition number and collinearity checks. |
| poland_support_overlap | references/papers_txt/crump_hotz_imbens_mitnik_2009_limited_overlap.txt; references/papers_txt/li_morgan_zaslavsky_2018_balancing_covariates_overlap_weights.txt | Justifies common-support or overlap checks before using Poland's feature profile. |
| cluster_bootstrap_and_delete_country | references/papers_txt/cameron_miller_2015_cluster_robust_practitioners_guide.txt; references/papers_txt/mackinnon_nielsen_webb_2023_jackknife_bootstrap_cluster.txt | Justifies country-level resampling and delete-one-country checks. This public reproduction block uses these draws only as finite-run reproducibility checks, not as sign filters. |
| lp_inference_and_time_stability | references/papers_txt/jorda_2005_aer_lp.txt; references/papers_txt/olea_plagborg_moller_2022_lp_inference.txt; references/papers_txt/huidrom_kose_lim_ohnsorge_2019_why_fiscal_positions.txt; references/papers_txt/ramey_zubairy_2018_multipliers_good_bad.txt | Justifies uncertainty and robustness checks across horizons and samples. This public reproduction block uses time blocks only as finite-run reproducibility checks, not as sign filters. |
| excluded_kernel_sign_gates | pre-specified notebook design rule | The gate deliberately excludes K_Y>0, K_G>0 and positive-sign stability of kernels. Subsequent numerical points use the selected specifications separately. |

## Stage 1: robustness winners

The screen selects only specifications with strong output-interaction evidence at `p < 0.05` and clean numerical/support diagnostics. It does not use later accounting outcomes or signs.

| features | robustness_score | finite_run_share | p_wald_y_h8 | mahalanobis_support_p | h8_condition_number | max_abs_feature_corr_h8 |
| --- | --- | --- | --- | --- | --- | --- |
| trade | 9 | 1.000000 | 0.003771 | 0.871864 | 70.880814 | 0.000000 |
| liq | 9 | 1.000000 | 0.013043 | 0.441307 | 68.369588 | 0.000000 |

## Output-interaction multiplicity sensitivity

The output-relevance screen is reported with raw p-values and simple 15-test multiplicity diagnostics. The gate itself uses the pre-specified raw `p < 0.05` output-relevance rule; the adjusted columns are sensitivity diagnostics, not additional hidden filters.

| features | p_wald_y_h8 | p_wald_y_h8_bonferroni | q_wald_y_h8_bh | raw_p_pass_unadjusted |
| --- | --- | --- | --- | --- |
| trade | 0.003771 | 0.056568 | 0.056568 | True |
| liq | 0.013043 | 0.195652 | 0.097826 | True |
| debt | 0.119830 | 1.000000 | 0.599148 | False |
| log_gdp_pc | 0.463297 | 1.000000 | 0.975771 | False |
| trade+debt+log_gdp_pc | 0.658554 | 1.000000 | 0.975771 | False |
| trade+log_gdp_pc | 0.675856 | 1.000000 | 0.975771 | False |
| trade+liq+log_gdp_pc | 0.690439 | 1.000000 | 0.975771 | False |
| trade+liq | 0.696225 | 1.000000 | 0.975771 | False |
| debt+liq | 0.804693 | 1.000000 | 0.975771 | False |
| trade+debt | 0.895313 | 1.000000 | 0.975771 | False |
| debt+log_gdp_pc | 0.898835 | 1.000000 | 0.975771 | False |
| liq+log_gdp_pc | 0.906285 | 1.000000 | 0.975771 | False |
| trade+debt+liq | 0.957030 | 1.000000 | 0.975771 | False |
| debt+liq+log_gdp_pc | 0.966691 | 1.000000 | 0.975771 | False |
| trade+debt+liq+log_gdp_pc | 0.975771 | 1.000000 | 0.975771 | False |

## Full robustness ranking

| features | gate_status | robustness_score | gate_reason | p_wald_y_h8 | mahalanobis_support_p | h8_condition_number | max_abs_feature_corr_h8 | finite_run_share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trade | PASS_ROBUSTNESS_GATE | 9 | all_checks_pass | 0.003771 | 0.871864 | 70.880814 | 0.000000 | 1.000000 |
| liq | PASS_ROBUSTNESS_GATE | 9 | all_checks_pass | 0.013043 | 0.441307 | 68.369588 | 0.000000 | 1.000000 |
| debt | FAIL_ROBUSTNESS_GATE | 8 | failed_output_interaction_p | 0.119830 | 0.712772 | 70.735072 | 0.000000 | 1.000000 |
| log_gdp_pc | FAIL_ROBUSTNESS_GATE | 8 | failed_output_interaction_p | 0.463297 | 0.945748 | 68.794480 | 0.000000 | 1.000000 |
| trade+debt+log_gdp_pc | FAIL_ROBUSTNESS_GATE | 8 | failed_output_interaction_p | 0.658554 | 0.976694 | 72.200433 | 0.249751 | 1.000000 |
| trade+log_gdp_pc | FAIL_ROBUSTNESS_GATE | 8 | failed_output_interaction_p | 0.675856 | 0.985900 | 71.101604 | 0.035025 | 1.000000 |
| trade+liq+log_gdp_pc | FAIL_ROBUSTNESS_GATE | 8 | failed_output_interaction_p | 0.690439 | 0.838935 | 71.201494 | 0.509186 | 1.000000 |
| trade+liq | FAIL_ROBUSTNESS_GATE | 8 | failed_output_interaction_p | 0.696225 | 0.713125 | 70.963703 | 0.151801 | 1.000000 |
| debt+liq | FAIL_ROBUSTNESS_GATE | 8 | failed_output_interaction_p | 0.804693 | 0.738448 | 70.793723 | 0.452516 | 1.000000 |
| trade+debt | FAIL_ROBUSTNESS_GATE | 8 | failed_output_interaction_p | 0.895313 | 0.902502 | 72.113452 | 0.249751 | 1.000000 |
| debt+log_gdp_pc | FAIL_ROBUSTNESS_GATE | 8 | failed_output_interaction_p | 0.898835 | 0.933109 | 70.839176 | 0.140759 | 1.000000 |
| liq+log_gdp_pc | FAIL_ROBUSTNESS_GATE | 8 | failed_output_interaction_p | 0.906285 | 0.703199 | 68.822358 | 0.509186 | 1.000000 |
| trade+debt+liq | FAIL_ROBUSTNESS_GATE | 8 | failed_output_interaction_p | 0.957030 | 0.870916 | 72.199017 | 0.452516 | 1.000000 |
| debt+liq+log_gdp_pc | FAIL_ROBUSTNESS_GATE | 8 | failed_output_interaction_p | 0.966691 | 0.871098 | 70.873536 | 0.509186 | 1.000000 |
| trade+debt+liq+log_gdp_pc | FAIL_ROBUSTNESS_GATE | 8 | failed_output_interaction_p | 0.975771 | 0.929638 | 72.300540 | 0.509186 | 1.000000 |

## QA

| check | status | detail |
| --- | --- | --- |
| spec_count_is_15 | PASS | spec_count=15 |
| all_nonempty_feature_subsets_present | PASS | expected 2^4 - 1 = 15 subsets of trade/debt/liq/log_gdp_pc |
| gate_reasons_are_stage1_only | PASS | gate_reason uses only pre-specified robustness diagnostics |
| robustness_summary_has_stage1_columns_only | PASS | feature_robustness_summary.csv contains only feature-selection diagnostics |
| no_kernel_quantiles_in_robustness_summary | PASS | feature_robustness_summary.csv omits K_Y/K_G quantiles; they stay in separate stability appendices |
| kernel_outputs_are_stage1_only | PASS | all-spec kernel outputs contain only output, spending and feature-profile fields |
| no_kernel_sign_gate_columns | PASS | gate excludes K_Y>0, K_G>0 and positive kernel-stability filters |
| no_positive_sign_summary_columns | PASS | robustness summary does not keep unused positive-sign diagnostics |
| result_file_set_is_stage1_only | PASS | extra=[]; missing=[] |
| output_only_bic_not_computed | PASS | No output-only BIC or fit ranking is part of gate logic. |
| multiplicity_sensitivity_written | PASS | raw p-values, Bonferroni p-values and Benjamini-Hochberg q-values are written as sensitivity diagnostics |
| support_excludes_poland_profile_target | PASS | target rows removed by country/profile-year filter; targets=POL_2022_target; min_distance_to_pol=0.000000000 |
| failed_gate_reasons_are_unambiguous | PASS | failed rows use failed_* reason labels |
| dependency_manifest_present | PASS | requirements.txt documents Python dependencies |
| bootstrap_draws_complete | PASS | min_boot_ok=19 |
| time_blocks_complete | PASS | min_time_ok=3 |
| required_text_references_present | PASS | text_reference_count=18 |

## Reproducibility notes

- The runner re-execs Python with `OPENBLAS_NUM_THREADS=1`, `OMP_NUM_THREADS=1` and `MKL_NUM_THREADS=1` before importing NumPy, so the plain command `python3 code/feature_screen_model.py` enforces the BLAS thread policy.
- `results/source_manifest.csv` is deterministic for public-archive source files, this block's stable CSV outputs, and this block report. It explicitly omits itself from its own hash list.
- `results/run_manifest.json` is dynamic run metadata. It records timestamp, platform, Python version, git head, git status and BLAS thread variables, so byte-for-byte equality is not expected across machines.

## Files

- `code/feature_screen_model.py`
- `data/`
- `references/papers_txt/`
- `results/feature_robustness_summary.csv`
- `results/criteria_literature_map.csv`
- `results/output_interaction_multiplicity_h8.csv`
- `results/loo_kernel_draws.csv`
- `results/bootstrap_kernel_draws.csv`
- `results/time_block_kernel_draws.csv`
- `results/source_manifest.csv`
