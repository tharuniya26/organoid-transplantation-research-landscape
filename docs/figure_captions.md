# Figure captions

1. **Research workflow.** Structured path from literature identification through translational interpretation. Original vector graphic; author credit included.
2. **Publication timeline.** Included verified primary studies per publication year. Zero-count years are retained.
3. **Organoid research distribution.** Study coverage by organoid category; counts are not efficacy estimates.
4. **Stem-cell sources.** Reported cell-source categories in the curated corpus.
5. **Research network.** Heterogeneous graph connecting organoid types to cell sources, target tissues, experimental models, engraftment status, and coded barriers. Every edge stores supporting study IDs.
6. **Translational evidence heatmap.** Descriptive matrix using supported, unsupported, uncertain, and unassessed states; not a readiness score.
7. **Translational barrier landscape.** Overlapping keyword-coded limitation categories from study-level notes.
8. **Conceptual transplantation workflow.** Research pathway from cell source to clinical translation evaluation; not empirical patient flow.
9. **Evidence gaps.** Number of organoid categories without supported evidence in each matrix domain.

All figures were generated from `data/processed/organoid_study_database.csv` by `src/visualization.py`, except Figures 1 and 8, which are original conceptual diagrams.

