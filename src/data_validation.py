"""Schema and scientific-coding validation for the curated evidence table."""
from __future__ import annotations

import re
import pandas as pd

REQUIRED_COLUMNS = [
    "study_id", "title", "publication_year", "journal", "doi", "pmid",
    "organoid_type", "stem_cell_source", "target_tissue", "disease_application",
    "experimental_model", "species", "transplantation_site", "transplantation_approach",
    "evidence_stage", "engraftment_reported", "vascularization_reported",
    "functional_outcomes", "safety_outcomes", "major_limitations", "study_design",
    "source_reference", "verification_status",
]
REPORTING = {"Not reported", "Not assessed", "Reported negative", "Reported positive", "Unclear"}
EVIDENCE_STAGES = {"In vitro", "Ex vivo", "Preclinical in vivo", "Human feasibility", "Interventional clinical trial", "Approved therapy"}
ORGANOID_TYPES = {"Brain", "Colonic", "Intestinal", "Kidney", "Liver", "Retinal"}


def validate_doi(value: str) -> bool:
    """Return True for a syntactically plausible DOI or a missing value."""
    return pd.isna(value) or bool(re.fullmatch(r"10\.\d{4,9}/\S+", str(value).strip(), re.I))


def validate_pmid(value: str) -> bool:
    """Return True for a numeric PubMed identifier or a missing value."""
    return pd.isna(value) or bool(re.fullmatch(r"\d{6,9}", str(value).strip()))


def validate_dataset(df: pd.DataFrame) -> list[str]:
    """Return all detected schema/coding errors; an empty list means valid."""
    errors: list[str] = []
    missing = sorted(set(REQUIRED_COLUMNS) - set(df.columns))
    if missing:
        return [f"Missing columns: {', '.join(missing)}"]
    if df["study_id"].duplicated().any():
        errors.append("Duplicate study_id values")
    if df["doi"].dropna().str.lower().duplicated().any():
        errors.append("Duplicate DOI values")
    if df["pmid"].dropna().duplicated().any():
        errors.append("Duplicate PMID values")
    for column in ("study_id", "title", "publication_year", "organoid_type", "evidence_stage", "verification_status", "source_reference"):
        if df[column].isna().any() or df[column].astype(str).str.strip().eq("").any():
            errors.append(f"Missing required values in {column}")
    bad_dois = df.loc[~df["doi"].map(validate_doi), "study_id"].tolist()
    bad_pmids = df.loc[~df["pmid"].map(validate_pmid), "study_id"].tolist()
    if bad_dois:
        errors.append(f"Invalid DOI: {', '.join(bad_dois)}")
    if bad_pmids:
        errors.append(f"Invalid PMID: {', '.join(bad_pmids)}")
    for column in ("engraftment_reported", "vascularization_reported"):
        invalid = sorted(set(df[column].dropna()) - REPORTING)
        if invalid:
            errors.append(f"Invalid {column}: {invalid}")
    if invalid := sorted(set(df["evidence_stage"]) - EVIDENCE_STAGES):
        errors.append(f"Invalid evidence_stage: {invalid}")
    if invalid := sorted(set(df["organoid_type"]) - ORGANOID_TYPES):
        errors.append(f"Invalid organoid_type: {invalid}")
    return errors


def assert_valid(df: pd.DataFrame) -> None:
    """Raise ValueError if the curated table violates validation rules."""
    errors = validate_dataset(df)
    if errors:
        raise ValueError("; ".join(errors))

