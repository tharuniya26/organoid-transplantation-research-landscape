# Data provenance

Each row is traceable to the PubMed record in `source_reference`; DOI and PMID are both stored when available. Candidate records were identified from the source review, targeted PubMed searching, and reference chaining. Bibliographic metadata and abstract-level outcomes were checked on 18 October 2026.

The curated CSV is human-authored secondary research data. It does not contain participant-level data, raw microscopy, or copyrighted article figures. Outcome descriptions are concise paraphrases. Source PDFs supplied by the user are checksummed and privately retained; the public analysis has no dependency on them.

Version 1.0 contains 15 studies published from 2012–2023, six organoid categories, five stem-cell-source categories, and nine experimental-model categories. All 15 records have a DOI and PMID (30 source identifiers in total), and all are marked `Verified`. The executed schema contains no structurally blank cells; however, five engraftment/vascularization fields are explicitly coded `Not assessed`, `Not reported`, or `Unclear`, which is scientific unavailability rather than a database omission. Counts reflect this bounded corpus and may change after a systematic update. Corrections should preserve `study_id` values where possible and document the change in version control.

