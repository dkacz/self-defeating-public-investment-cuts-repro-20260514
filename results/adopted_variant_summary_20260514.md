# Adopted Variant Summary - Mozdzen Full Replacement Branch

This table separates the adopted three-variable Mozdzen branch from diagnostics. Values are copied from upstream local grids and remain pre-Pro until the full branch audit closes.

|role|variant|passing_specs|K_Y_h8|K_G_h8|dsa_margin_2036_cut_pp|direct_dy_margin_2036_cut_pp|dsa_margin_2036_expansion_pp|direct_dy_margin_2036_expansion_pp|note|
|---|---|---|---|---|---|---|---|---|---|
|previous_frozen_baseline|baseline_frozen_control|F01+F11|2.149970968|0.748297990|6.371492666|4.891678068|-5.807471128|-4.891678068|Comparison baseline from accepted clean repro.|
|current_control|baseline_current_control|F01+F11|2.148643156|0.747971739|6.352575237|4.886581685|-5.789236145|-4.886581685|Current control in the upstream grid.|
|adopted_mozdzen_branch|tiva2022_gfcf_realppp_networth|F01+F03|1.998104779|0.720018505|5.696884465|3.019450731|-5.367087202|-3.019450731|Official TiVA GFCF import-content + real PPP income + household net financial worth.|
|networth_without_realppp|tiva2022_gfcf_paper_networth|F01+F03|1.998104779|0.720018505|5.696884465|3.019450731|-5.367087202|-3.019450731|Diagnostic: same trade/liquidity replacement, old paper income construction.|
|old_credit_with_realppp_tiva|tiva2022_gfcf_realppp_credit|F01+F14|0.632502119|0.683652469|-4.419817997|2.327568053|4.747987712|-2.327568053|Diagnostic: keeps old household-credit liquidity proxy.|
|figaro_diagnostic|figaro2023_gfcf_realppp_networth|F03|2.114703444|0.746125764|6.247806441|4.118006860|-5.852717416|-4.118006860|Diagnostic: newer FIGARO-derived import-content source, not the adopted Mozdzen branch.|
|carry_forward_diagnostic|tiva_cf2024_gfcf_realppp_networth|F01+F03|1.964343676|0.720104763|5.480565861|2.879434098|-5.158074478|-2.879434098|Diagnostic: mechanical carry-forward to 2024, not official OECD data.|
|cash_transferable_diagnostic|tiva2022_gfcf_realppp_cash_transferable|F01|1.838266012|0.694029346|4.890650642|1.729581956|-4.636256608|-1.729581956|Diagnostic: literal cash plus transferable deposits liquidity, not the adopted Mozdzen branch.|
