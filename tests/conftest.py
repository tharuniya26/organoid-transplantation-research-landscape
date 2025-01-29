from __future__ import annotations
import pandas as pd
import pytest

@pytest.fixture
def synthetic_studies():
    """Synthetic software fixture; not scientific evidence."""
    base = {
        "study_id": "TST001", "title": "Synthetic organoid graft", "publication_year": 2020,
        "journal": "Test Journal", "doi": "10.1234/test.1", "pmid": "12345678",
        "organoid_type": "Kidney", "stem_cell_source": "Induced pluripotent stem cell",
        "target_tissue": "Kidney", "disease_application": "Software testing",
        "experimental_model": "Synthetic mouse model", "species": "Mouse",
        "transplantation_site": "Renal subcapsular space", "transplantation_approach": "Synthetic",
        "evidence_stage": "Preclinical in vivo", "engraftment_reported": "Reported positive",
        "vascularization_reported": "Not assessed", "functional_outcomes": "Synthetic endpoint",
        "safety_outcomes": "Not assessed", "major_limitations": "Synthetic fixture",
        "study_design": "Controlled animal experiment", "source_reference": "https://example.org/test",
        "verification_status": "Verified",
    }
    return pd.DataFrame([base])

