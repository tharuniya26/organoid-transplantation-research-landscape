"""Execute validation, analysis, network construction, and figure generation."""
from __future__ import annotations

import logging
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.data_extraction import load_studies
from src.data_validation import assert_valid
from src.evidence_mapping import generate_landscape_outputs
from src.network_analysis import export_network
from src.translational_analysis import export_translational_outputs
from src.visualization import generate_all_figures


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    studies = load_studies()
    assert_valid(studies)
    generate_landscape_outputs(studies, ROOT / "results")
    graph, metrics = export_network(studies, ROOT / "results")
    matrix, _ = export_translational_outputs(studies, ROOT / "results")
    figures = generate_all_figures(studies, graph, matrix, ROOT / "figures")
    print(f"Validated {len(studies)} studies; network {graph.number_of_nodes()} nodes/{graph.number_of_edges()} edges; generated {len(figures)} PNG figures.")


if __name__ == "__main__":
    main()

