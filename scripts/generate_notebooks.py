"""Generate six concise notebooks that reuse the tested src package."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks"

def md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": [line + "\n" for line in text.strip().splitlines()]}

def code(text: str) -> dict:
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [line + "\n" for line in text.strip().splitlines()]}

common = """from pathlib import Path
import sys
ROOT = Path.cwd().resolve()
if ROOT.name == 'notebooks': ROOT = ROOT.parent
sys.path.insert(0, str(ROOT))
from src.data_extraction import load_studies
studies = load_studies(ROOT / 'data' / 'processed' / 'organoid_study_database.csv')
print(f'Loaded {len(studies)} curated studies')"""

specs = [
    ("01_literature_dataset.ipynb", "Literature dataset", "Inspect the verified study corpus and its provenance.", """display(studies[['study_id','publication_year','organoid_type','doi','pmid']])
print('Years:', studies.publication_year.min(), 'to', studies.publication_year.max())""", "The table is a bounded evidence-map corpus; it is not a prevalence sample."),
    ("02_evidence_validation.ipynb", "Evidence validation", "Validate schema, identifiers, duplicates, and controlled categories.", """from src.data_validation import validate_dataset
errors = validate_dataset(studies)
print('Validation:', 'PASSED' if not errors else errors)""", "Passing software checks confirms internal consistency, not independent biological replication."),
    ("03_research_landscape.ipynb", "Research landscape", "Summarize publication years, organoid types, sources, models, and evidence stages.", """from src.evidence_mapping import count_table
display(count_table(studies, 'organoid_type'))
display(count_table(studies, 'evidence_stage'))
display(count_table(studies, 'publication_year'))""", "Kidney is the most represented category, but study frequency is not efficacy."),
    ("04_organoid_network.ipynb", "Organoid network", "Build and inspect the study-provenanced heterogeneous evidence network.", """from src.network_analysis import build_network, network_metrics
graph = build_network(studies)
display(network_metrics(graph))
print('All edges have provenance:', all(d.get('study_ids') for *_, d in graph.edges(data=True)))""", "Network structure describes documented relationships and cannot establish therapeutic readiness."),
    ("05_translational_readiness.ipynb", "Translational evidence", "Construct the descriptive, non-numeric evidence matrix.", """from src.translational_analysis import build_translational_matrix
matrix = build_translational_matrix(studies)
display(matrix.drop(columns='supporting_studies'))""", "No category has eligible human organoid-graft outcome evidence in this corpus."),
    ("06_results_interpretation.ipynb", "Results interpretation", "Integrate executed metrics while preserving biological and review-method limitations.", """from src.network_analysis import build_network
graph = build_network(studies)
summary = {'verified_studies': int(studies.verification_status.eq('Verified').sum()), 'organoid_types': int(studies.organoid_type.nunique()), 'network_relationships': graph.number_of_edges(), 'human_stage_studies': int(studies.evidence_stage.str.contains('Human|clinical|Approved', case=False).sum())}
summary""", "The executed analysis supports a preclinical landscape conclusion, not a clinical recommendation."),
]

for filename, title, objective, analysis, interpretation in specs:
    notebook = {
        "cells": [
            md(f"# {title}\n\n## Scientific objective\n\n{objective}\n\n## Background and data sources\n\nThe input is the identifier-verified curated CSV. Primary records are linked through PubMed. See `docs/search_strategy.md` and `docs/data_provenance.md`."),
            md("## Methods\n\nReusable functions from `src/` are used so notebook and command-line results share one implementation."),
            code(common),
            code(analysis),
            md(f"## Biological interpretation\n\n{interpretation}"),
            md("## Limitations\n\nSingle-reviewer bounded evidence map; heterogeneous models and endpoints; incomplete safety reporting; missing evidence is not a negative result; no causal or clinical-readiness inference from counts."),
        ],
        "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python", "version": "3.11+"}},
        "nbformat": 4, "nbformat_minor": 5,
    }
    (OUT / filename).write_text(json.dumps(notebook, indent=1), encoding="utf-8")
print(f"Generated {len(specs)} notebooks")

