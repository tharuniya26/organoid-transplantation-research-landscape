# Search strategy

## Databases and date

PubMed was searched and identifier records were checked on **18 October 2026**. ClinicalTrials.gov was checked to distinguish registered human investigation from published transplantation outcomes. Candidate studies cited by the supplied review were used for seed-and-expand searching. The machine-readable search log is in `data/metadata/search_log.csv`.

## Exact reproducible queries

1. `(organoid*[Title/Abstract]) AND (transplant*[Title/Abstract] OR engraft*[Title/Abstract])`
2. `((kidney OR renal OR intestinal OR colon* OR retinal OR liver OR brain OR cortical) AND organoid*) AND (transplant* OR engraft*)`

Organ-specific title and DOI checks supplemented these broad queries. PubMed identifiers, DOIs, titles, journal, and year were verified against PubMed records. The code in `src/literature_search.py` constructs a public NCBI E-utilities request and caches raw JSON when run with network access.

## Retrieval and deduplication

Records are deduplicated by normalized DOI, then PMID, then normalized title. A record is not counted twice when one experiment has multiple database entries. Follow-up reports with a substantively distinct endpoint may remain separate (for example kidney-organoid morphogenesis versus later in vivo filtration), and this relationship must be considered when interpreting counts.

## Scope limitation

This is a reproducible **structured evidence map**, not a PRISMA systematic review. Full database export and dual independent screening were not performed. The 15-study database is a verified, deliberately bounded seed corpus suitable for transparent computation, not an exhaustive prevalence sample.

