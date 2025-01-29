from src.data_validation import validate_dataset, validate_doi, validate_pmid

def test_identifier_validation():
    assert validate_doi("10.1038/nature12271")
    assert not validate_doi("doi:unknown")
    assert validate_pmid("23823721")
    assert not validate_pmid("PMID23823721")

def test_valid_synthetic_dataset(synthetic_studies):
    assert validate_dataset(synthetic_studies) == []

def test_duplicate_detection(synthetic_studies):
    duplicated = synthetic_studies.copy()
    duplicated.loc[1] = duplicated.loc[0]
    errors = validate_dataset(duplicated)
    assert any("Duplicate" in error for error in errors)

def test_controlled_vocabulary(synthetic_studies):
    synthetic_studies.loc[0, "engraftment_reported"] = "Probably"
    assert any("Invalid engraftment" in error for error in validate_dataset(synthetic_studies))

def test_missing_required_value(synthetic_studies):
    synthetic_studies.loc[0, "title"] = None
    assert any("Missing required values in title" in error for error in validate_dataset(synthetic_studies))

