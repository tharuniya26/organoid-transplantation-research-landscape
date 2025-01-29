from src.network_analysis import build_network, network_metrics

def test_network_edge_provenance(synthetic_studies):
    graph = build_network(synthetic_studies)
    assert graph.number_of_edges() > 0
    assert all(data.get("study_ids") == "TST001" for *_, data in graph.edges(data=True))

def test_network_metrics(synthetic_studies):
    metrics = network_metrics(build_network(synthetic_studies))
    edge_count = metrics.query("metric == 'edge_count'")["value"].iloc[0]
    assert int(edge_count) > 0

