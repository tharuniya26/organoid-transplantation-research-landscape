"""Evidence matrix and non-composite quality-domain summaries."""
from __future__ import annotations

from pathlib import Path
import pandas as pd


def _status(series: pd.Series) -> str:
    values = set(series.dropna())
    if "Reported positive" in values:
        return "Supported"
    if "Reported negative" in values:
        return "Unsupported"
    if values & {"Unclear"}:
        return "Uncertain"
    return "Unassessed"


def build_translational_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate descriptive support by organoid type; no readiness score is produced."""
    rows = []
    for organoid, group in sorted(df.groupby("organoid_type")):
        rows.append({
            "organoid_type": organoid,
            "in_vitro_functional_characterization": "Supported" if group["functional_outcomes"].notna().any() else "Unassessed",
            "preclinical_engraftment": _status(group["engraftment_reported"]),
            "vascular_integration": _status(group["vascularization_reported"]),
            "functional_maturation": "Supported" if group["functional_outcomes"].notna().any() else "Unassessed",
            "safety_assessment": "Supported" if group["safety_outcomes"].str.contains("adverse|mortality|safety", case=False, na=False).any() else "Unassessed",
            "human_clinical_investigation": "Unassessed",
            "manufacturing_and_scale_up": "Uncertain" if group["major_limitations"].str.contains("off-target|quality|variab|scale", case=False, na=False).any() else "Unassessed",
            "supporting_studies": ";".join(group["study_id"]),
        })
    return pd.DataFrame(rows)


def build_quality_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Record study-level appraisal domains without an invalid universal score."""
    return pd.DataFrame({
        "study_id": df["study_id"],
        "model_reported": df["experimental_model"].notna().map({True: "Yes", False: "No"}),
        "control_design_identifiable": df["study_design"].str.contains("Controlled|Comparative", na=False).map({True: "Yes", False: "Unclear"}),
        "engraftment_assessed": (~df["engraftment_reported"].isin(["Not assessed", "Not reported"])).map({True: "Yes", False: "No"}),
        "functional_outcome_reported": df["functional_outcomes"].notna().map({True: "Yes", False: "No"}),
        "safety_assessed": (~df["safety_outcomes"].isin(["Not assessed", "Not reported"])).map({True: "Yes", False: "No"}),
        "clinical_applicability": "Indirect preclinical evidence",
        "appraisal_note": df["major_limitations"],
    })


def export_translational_outputs(df: pd.DataFrame, output_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    output_dir.mkdir(parents=True, exist_ok=True)
    matrix = build_translational_matrix(df)
    quality = build_quality_summary(df)
    matrix.to_csv(output_dir / "translational_evidence_matrix.csv", index=False)
    quality.to_csv(output_dir / "evidence_quality_summary.csv", index=False)
    return matrix, quality

