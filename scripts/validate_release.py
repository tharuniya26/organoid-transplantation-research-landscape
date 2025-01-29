"""Read-only release checks for links, notebooks, figures, and network provenance."""
from __future__ import annotations
import json
import re
from pathlib import Path

import networkx as nx
from PIL import Image

from src.data_extraction import load_studies
from src.data_validation import assert_valid

ROOT = Path(__file__).resolve().parents[1]
studies = load_studies()
assert_valid(studies)
study_ids = set(studies["study_id"])

graph = nx.read_graphml(ROOT / "results" / "organoid_research_network.graphml")
for left, right, data in graph.edges(data=True):
    provenance = set(str(data.get("study_ids", "")).split(";")) - {""}
    assert provenance, f"Missing provenance: {left} -- {right}"
    assert provenance <= study_ids, f"Unknown study provenance: {provenance - study_ids}"
    assert int(data["evidence_count"]) == len(provenance), f"Bad evidence_count: {left} -- {right}"

notebook_count = 0
for path in sorted((ROOT / "notebooks").glob("*.ipynb")):
    notebook_count += 1
    notebook = json.loads(path.read_text(encoding="utf-8"))
    headings = "".join("".join(c["source"]) for c in notebook["cells"] if c["cell_type"] == "markdown")
    for required in ("Scientific objective", "Methods", "Biological interpretation", "Limitations"):
        assert required in headings, f"{path.name}: missing {required}"
    code_cells = [c for c in notebook["cells"] if c["cell_type"] == "code"]
    assert code_cells and all(c.get("execution_count") is not None for c in code_cells), f"{path.name}: unexecuted code"
    assert not any(o.get("output_type") == "error" for c in code_cells for o in c.get("outputs", [])), f"{path.name}: error output"

readme = (ROOT / "README.md").read_text(encoding="utf-8")
local_links = []
for target in re.findall(r"!?(?:\[[^\]]*\])\(([^)]+)\)", readme):
    if not re.match(r"(?:https?://|mailto:|#)", target):
        local_links.append(target)
        assert (ROOT / target).exists(), f"Broken README link: {target}"

pngs = sorted((ROOT / "figures").glob("figure_*.png"))
svgs = sorted((ROOT / "figures").glob("figure_*.svg"))
assert len(pngs) == len(svgs) == 9
for path in pngs:
    with Image.open(path) as image:
        assert image.width >= 2400 or image.height >= 1200, f"Low-resolution figure: {path.name}"

gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
assert "source_material_private/" in gitignore
assert len(list((ROOT / "source_material_private").glob("*.pdf"))) == 2

print(f"release_checks=passed; studies={len(studies)}; graph={graph.number_of_nodes()} nodes/{graph.number_of_edges()} edges; notebooks={notebook_count}; figures={len(pngs)} PNG+SVG pairs; README_local_links={len(local_links)}")
