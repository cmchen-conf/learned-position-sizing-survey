# Learning How Much to Trade

Selected survey data, figure scripts and reported rerun results accompanying *Learning How Much to Trade: A Survey of Machine-Learned Position Sizing and Its Evaluation*. The files come from the manuscript source bundle (main article v0.15.19, supplement v0.15.20).

## Survey data and figures

- `study_records.csv` contains the 95 rows of supplementary Table A.1, exported from its typesetting source. Column values preserve the source notation, including LaTeX markup. This is a table export, not the original coding ledger.
- `figure/year_branch.csv` contains counts by publication year and branch. With R and ggplot2 installed, run `cd figure && Rscript gen_trend.R` to draw the trend plot.
- `scripts/mm_objects_v0.15.5.py` and `figure/gen_tree.py` are the original scripts for the sized-object table and taxonomy figure. Both require the original coding_v0.8.csv in the repository root. That input is absent from this snapshot. The tabulated object counts, table source and manuscript number definitions are included.
- Run `python3 scripts/check_snapshot.py` from the repository root to check study identifiers and branch totals in the two exported tables. This packaging check requires only the Python standard library.

## Reported experimental results

The TeX table fragments in `reported_results/` contain the codebase candidate list, reported paired differences, per-seed results, market-path intervals and simulator results. These are table outputs. The original training drivers, patches, environment specifications, analysis pipeline, screening ledger and raw run outputs are not included. This snapshot alone cannot rerun the experiments.
