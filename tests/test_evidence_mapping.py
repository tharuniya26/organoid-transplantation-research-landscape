from src.evidence_mapping import count_table, generate_landscape_outputs

def test_counts_preserve_categories(synthetic_studies):
    table = count_table(synthetic_studies, "organoid_type")
    assert table.to_dict("records") == [{"organoid_type": "Kidney", "study_count": 1}]

def test_output_consistency(synthetic_studies, tmp_path):
    outputs = generate_landscape_outputs(synthetic_studies, tmp_path)
    assert int(outputs["summary"].query("metric == 'verified_studies'")["value"].iloc[0]) == 1
    assert (tmp_path / "landscape_summary.csv").exists()

