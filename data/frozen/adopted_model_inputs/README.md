# Frozen Adopted Model Inputs

This folder contains the small model-input slice used by the adopted Mozdzen replacement configuration `tiva2022_gfcf_realppp_networth`.

The files are copied from the locally frozen FIGARO/TiVA extension artifact so this branch can rebuild its tables without reading paths outside the branch artifact. These are not live downloads and are not FIGARO diagnostics; they are the adopted official-TiVA GFCF, real-PPP and net-worth model inputs used by the branch tables.

Hashes are written to `data/provenance/adopted_branch_frozen_inputs_manifest_20260514.csv` by `code/run_full_replacement_repro.py`.
