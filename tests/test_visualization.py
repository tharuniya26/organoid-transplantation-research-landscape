from src.network_analysis import build_network
from src.translational_analysis import build_translational_matrix
from src.visualization import generate_all_figures

def test_figure_generation(synthetic_studies, tmp_path):
    graph = build_network(synthetic_studies)
    matrix = build_translational_matrix(synthetic_studies)
    figures = generate_all_figures(synthetic_studies, graph, matrix, tmp_path)
    assert len(figures) == 9
    assert all(path.stat().st_size > 1000 for path in figures)

def test_evidence_category_handling(synthetic_studies):
    synthetic_studies.loc[0, "engraftment_reported"] = "Reported negative"
    matrix = build_translational_matrix(synthetic_studies)
    assert matrix.loc[0, "preclinical_engraftment"] == "Unsupported"

