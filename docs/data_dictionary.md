# Data dictionary

| Field | Meaning |
|---|---|
| `study_id` | Stable local identifier (`ORG###`) |
| `title`, `publication_year`, `journal` | Bibliographic description |
| `doi`, `pmid` | Persistent identifiers; missing values stay missing |
| `organoid_type` | Controlled tissue category |
| `stem_cell_source` | Source category as reported |
| `target_tissue`, `disease_application` | Intended biological target and application |
| `experimental_model`, `species` | Recipient model and organism |
| `transplantation_site`, `transplantation_approach` | Graft site and delivery form |
| `evidence_stage` | Defined research-to-clinic stage |
| `engraftment_reported`, `vascularization_reported` | Five-state reporting code |
| `functional_outcomes`, `safety_outcomes` | Concise reported endpoints, not independent replication |
| `major_limitations` | Study/model limitations used for barrier mapping |
| `study_design` | High-level design label |
| `source_reference` | Direct PubMed provenance link |
| `verification_status` | Bibliographic verification state |

The five-state reporting vocabulary is `Not reported`, `Not assessed`, `Reported negative`, `Reported positive`, and `Unclear`. These values must never be collapsed into a binary where missing becomes negative.

The executed completeness summary is exported in `results/landscape_summary.csv`. It separately reports structurally blank cells and scientifically unavailable outcome states, so a coded `Not assessed` value is not mistaken for missing data.

