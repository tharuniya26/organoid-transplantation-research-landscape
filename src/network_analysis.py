"""Evidence-backed heterogeneous network construction and metrics."""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import networkx as nx
import pandas as pd


def _node_id(kind: str, label: str) -> str:
    return f"{kind}:{label}"


def build_network(df: pd.DataFrame) -> nx.Graph:
    """Create study-provenanced relationships from curated table fields."""
    graph = nx.Graph(title="Organoid transplantation evidence network")
    for row in df.itertuples(index=False):
        source = _node_id("organoid_type", row.organoid_type)
        graph.add_node(source, node_type="Organoid type", label=row.organoid_type)
        targets = [
            ("stem_cell_source", "Stem-cell source", row.stem_cell_source, "derived_from"),
            ("target_tissue", "Target tissue", row.target_tissue, "targets"),
            ("experimental_model", "Experimental model", row.experimental_model, "tested_in"),
            ("reported_outcome", "Reported outcome", row.engraftment_reported, "engraftment_status"),
        ]
        for kind, display_kind, label, relation in targets:
            node = _node_id(kind, label)
            graph.add_node(node, node_type=display_kind, label=label)
            if graph.has_edge(source, node):
                studies = set(graph[source][node]["study_ids"].split(";"))
                studies.add(row.study_id)
                graph[source][node]["study_ids"] = ";".join(sorted(studies))
                graph[source][node]["evidence_count"] = len(studies)
            else:
                graph.add_edge(source, node, relation=relation, study_ids=row.study_id, evidence_count=1)
        for barrier in str(row.major_limitations).split(";"):
            barrier = barrier.strip()
            if not barrier:
                continue
            node = _node_id("translational_barrier", barrier)
            graph.add_node(node, node_type="Translational barrier", label=barrier)
            if graph.has_edge(source, node):
                studies = set(graph[source][node]["study_ids"].split(";"))
                studies.add(row.study_id)
                graph[source][node]["study_ids"] = ";".join(sorted(studies))
                graph[source][node]["evidence_count"] = len(studies)
            else:
                graph.add_edge(source, node, relation="limited_by", study_ids=row.study_id, evidence_count=1)
    return graph


def network_metrics(graph: nx.Graph) -> pd.DataFrame:
    """Return graph-level and category relationship metrics."""
    rows = [
        {"metric": "node_count", "category": "all", "value": graph.number_of_nodes()},
        {"metric": "edge_count", "category": "all", "value": graph.number_of_edges()},
        {"metric": "connected_components", "category": "all", "value": nx.number_connected_components(graph)},
    ]
    for category, count in sorted(Counter(data["node_type"] for _, data in graph.nodes(data=True)).items()):
        rows.append({"metric": "nodes_by_type", "category": category, "value": count})
    for relation, count in sorted(Counter(data["relation"] for *_, data in graph.edges(data=True)).items()):
        rows.append({"metric": "edges_by_relation", "category": relation, "value": count})
    return pd.DataFrame(rows)


def export_network(df: pd.DataFrame, output_dir: Path) -> tuple[nx.Graph, pd.DataFrame]:
    output_dir.mkdir(parents=True, exist_ok=True)
    graph = build_network(df)
    metrics = network_metrics(graph)
    nx.write_graphml(graph, output_dir / "organoid_research_network.graphml")
    metrics.to_csv(output_dir / "network_metrics.csv", index=False)
    return graph, metrics

