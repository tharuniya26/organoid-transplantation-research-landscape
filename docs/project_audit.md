# Final project audit

Initial audit: **18 October 2026**. Recovery validation completed: **19 October 2026**. Status vocabulary: PASSED, FAILED, NOT VERIFIED, NOT APPLICABLE.

| Domain | Status | Evidence |
|---|---|---|
| Scientific scope and terminology | PASSED | Eligibility rules distinguish organoids from isolated cells, RPE monolayers, spheroids, chips, fetal tissue, and whole-organ transplants |
| Source PDFs reviewed fully | PASSED | 8-page article and 1-page poster extracted and reviewed; checksums in `docs/source_review.md` |
| Source preservation | PASSED | Original PDFs unchanged in ignored `source_material_private/`; SHA-256 values recorded |
| Published-review metadata | PASSED | Title, five-author list, journal, 3(2), July 2025, pp.80–87, and ISSN verified against PDF and official journal page |
| Review DOI | NOT VERIFIED | No DOI appears in the supplied PDF or official issue record |
| Review peer-review status | NOT VERIFIED | Publication is verified; editorial peer-review process was not independently established |
| Prior authorship integrity | PASSED | Historical five-author attribution retained in formal citation; new computational author block remains sole-author |
| Redistribution permission for review PDF | NOT VERIFIED | PDF excluded from public repository; official source link supplied |
| Presentation redistribution/figure rights | NOT VERIFIED | Poster and embedded third-party imagery excluded; image inventory documents rights uncertainty |
| Assignment branding removed from new outputs | PASSED | No logos, course covers, module codes, student numbers, grading, Turnitin, or assignment forms in README/report/figures |
| Literature identifiers | PASSED | 15 rows link to PubMed; DOI and PMID syntax/duplicates pass automated validation |
| Search transparency | PASSED | Databases, exact strings, date, eligibility, deduplication, and single-reviewer limitation documented |
| Systematic-review claim | PASSED | Consistently described as a structured evidence map, not a systematic review |
| Curated database | PASSED | 15 non-synthetic primary records with 23 documented fields and source links |
| Evidence-stage classification | PASSED | All eligible reports correctly coded preclinical in vivo; no human organoid-graft efficacy claim |
| Missing/negative distinction | PASSED | Five-state reporting vocabulary validated and explained |
| Evidence quality | PASSED | Design-relevant domains exported without a composite universal score |
| Computational landscape | PASSED | Pipeline generated seven distributions and `landscape_summary.csv` |
| Network validity | PASSED | 64 nodes, 75 edges; every edge carries one or more supporting study IDs |
| Network interpretation | PASSED | README/report state that topology and centrality do not establish efficacy/readiness |
| Translational matrix | PASSED | Four-state descriptive matrix exported; no numerical readiness ranking |
| Figures | PASSED | Nine original figures exported in PNG and SVG; PNGs at 300 dpi; captions and source notes documented |
| Source-image rights | PASSED | No original article/poster image reused in public outputs |
| Notebooks | PASSED | Six notebooks executed on 18 October 2026; each has execution counts `[1, 2]` and zero error outputs |
| Automated tests | PASSED | 11 collected, 11 passed, 0 failed, 0 skipped using pytest 9.1.1 and a workspace-local base temp directory |
| Recovery test stability | PASSED | A combined multi-process QA command encountered a transient memory error; immediate isolated pytest rerun completed all 11 tests in 8.13 s |
| First test attempt | NOT APPLICABLE | Two setup errors arose from sandbox denial of the default Windows temp directory; rerun in workspace passed all tests |
| Report rendering | PASSED | Six-page PDF rebuilt from the current source and every page visually inspected; no blank/nearly empty pages, clipping, overlap, missing images, or separated captions observed |
| Report peer-review/publication claim | PASSED | Explicitly labelled independent and not peer reviewed |
| Dependency/version record | PASSED | Python requirement and package versions recorded in `pyproject.toml` and `requirements.txt` |
| Secret/credential exposure | PASSED | No private API credentials required or stored |
| AI-assistance transparency | PASSED | Material assistance disclosed in README and report without adding AI as scientific author |
| README/local release links | PASSED | Automated release check resolved all 24 local README image/document links |
| Git repository inspection | NOT APPLICABLE | Workspace is not Git-initialized; `.gitignore` excludes private sources, caches, environments, and secrets; no commit, staging, remote, or push performed |

## Discipline-specific review

- **Regenerative medicine:** conclusions remain preclinical and distinguish microtissue function from organ replacement.
- **Stem-cell biology:** adult stem cells, ESCs, iPSCs, progenitors, maturation, off-target cells, and host vasculature are treated separately.
- **Evidence synthesis:** reproducible query and eligibility framework are present, with honest single-reviewer and non-exhaustive limits.
- **Computational biology/data science:** outputs are derived from validated records; network edges carry provenance; generated files are reproducible.
- **Software engineering:** modules use type hints/docstrings, relative paths, controlled vocabularies, caching, error handling, tests, and pinned dependencies.
- **Portfolio review:** README centres the database, network, and evidence matrix; the report and figures are publication-style and branding-free.

## Remaining unresolved issues

The corpus is not exhaustive and full-text dual extraction was not performed. Study-level randomization, blinding, attrition, sample-size justification, immune response, and exact follow-up require deeper full-text appraisal. Copyright permission for redistributing the supplied published PDF is unresolved. No eligible published human organoid-graft outcome study was identified in this bounded corpus. These limitations prevent describing the project as a definitive systematic review or clinically actionable readiness assessment.

## Release decision

**Ready for public GitHub initialization and review.** Code, curated metadata, derived results, figures, notebooks, and report pass the executed checks. Keep `source_material_private/` excluded, inspect `git status` after initialization, and do not add the original PDFs or poster images without explicit redistribution permission. Add the real repository URL to `CITATION.cff` only after the remote exists.


