"""Dataset loading and normalization helpers."""
from __future__ import annotations

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = PROJECT_ROOT / "data" / "processed" / "organoid_study_database.csv"


def load_studies(path: Path | str = DEFAULT_DATA) -> pd.DataFrame:
    """Load the curated study table without coercing identifiers to numbers."""
    return pd.read_csv(path, dtype={"study_id": "string", "doi": "string", "pmid": "string"})


def split_terms(value: object) -> list[str]:
    """Split semicolon-delimited evidence terms, excluding missing placeholders."""
    if pd.isna(value):
        return []
    return [part.strip() for part in str(value).split(";") if part.strip()]

