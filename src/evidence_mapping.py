"""Descriptive evidence-map summaries."""
from __future__ import annotations

from pathlib import Path
import pandas as pd


def count_table(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Count non-missing categories without interpreting them as efficacy."""
    out = df[column].fillna("Missing").value_counts().rename_axis(column).reset_index(name="study_count")
    return out.sort_values(["study_count", column], ascending=[False, True]).reset_index(drop=True)


def generate_landscape_outputs(df: pd.DataFrame, output_dir: Path) -> dict[str, pd.DataFrame]:
    """Compute and export the core descriptive tables."""
    output_dir.mkdir(parents=True, exist_ok=True)
    columns = ["publication_year", "organoid_type", "stem_cell_source", "experimental_model", "evidence_stage", "engraftment_reported", "vascularization_reported"]
    tables = {column: count_table(df, column) for column in columns}
    for name, table in tables.items():
        table.to_csv(output_dir / f"distribution_{name}.csv", index=False)
    summary = pd.DataFrame({
        "metric": [
            "eligible_studies", "verified_studies", "organoid_categories",
            "stem_cell_source_categories", "experimental_model_categories",
            "publication_year_start", "publication_year_end", "doi_identifiers",
            "pmid_identifiers", "verified_source_identifiers", "missing_cells",
            "unverified_records", "unavailable_engraftment_or_vascularization_fields",
        ],
        "value": [
            len(df), int(df["verification_status"].eq("Verified").sum()),
            df["organoid_type"].nunique(), df["stem_cell_source"].nunique(),
            df["experimental_model"].nunique(), int(df["publication_year"].min()),
            int(df["publication_year"].max()), int(df["doi"].notna().sum()),
            int(df["pmid"].notna().sum()),
            int(df["doi"].notna().sum() + df["pmid"].notna().sum()),
            int(df.isna().sum().sum()), int((df["verification_status"] != "Verified").sum()),
            int(df[["engraftment_reported", "vascularization_reported"]]
                .isin(["Not assessed", "Not reported", "Unclear"]).sum().sum()),
        ],
    })
    summary.to_csv(output_dir / "landscape_summary.csv", index=False)
    tables["summary"] = summary
    return tables

