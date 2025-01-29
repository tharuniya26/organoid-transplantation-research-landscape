"""Colourblind-accessible static scientific visualizations."""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns

PALETTE = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9", "#D55E00"]


def _save(fig: plt.Figure, output_dir: Path, stem: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_dir / f"{stem}.png", dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(output_dir / f"{stem}.svg", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def _title(ax: plt.Axes, title: str, subtitle: str) -> None:
    ax.set_title(title, loc="left", fontsize=15, fontweight="bold", pad=18)
    ax.text(0, 1.02, subtitle, transform=ax.transAxes, fontsize=8.5, color="#555555")


def workflow_figure(output_dir: Path) -> None:
    steps = ["Literature\nsearch", "Screening", "Evidence\nextraction", "Data\nvalidation", "Computational\nanalysis", "Translational\ninterpretation"]
    fig, ax = plt.subplots(figsize=(12, 2.6)); ax.axis("off")
    for i, step in enumerate(steps):
        ax.text(i, 0.5, step, ha="center", va="center", color="white", fontsize=9,
                bbox={"boxstyle": "round,pad=.55", "facecolor": PALETTE[i % len(PALETTE)], "edgecolor": "none"})
        if i < len(steps) - 1:
            ax.annotate("", (i + .66, .5), (i + .34, .5), arrowprops={"arrowstyle": "->", "lw": 1.8, "color": "#555"})
    ax.set_xlim(-.6, len(steps) - .4); ax.set_ylim(0, 1)
    ax.set_title("Structured organoid transplantation evidence-map workflow", fontweight="bold", loc="left")
    ax.text(0, .05, "Author: Tharuniya Anpalakan | Source: documented PubMed-based workflow", transform=ax.transAxes, fontsize=8, color="#555")
    _save(fig, output_dir, "figure_01_research_workflow")


def publication_timeline(df: pd.DataFrame, output_dir: Path) -> None:
    counts = df.groupby("publication_year").size()
    years = range(int(df.publication_year.min()), int(df.publication_year.max()) + 1)
    counts = counts.reindex(years, fill_value=0)
    fig, ax = plt.subplots(figsize=(9, 4.8)); ax.bar(counts.index, counts.values, color=PALETTE[0])
    ax.set(xlabel="Publication year", ylabel="Included studies")
    ax.set_xticks(list(years)); ax.tick_params(axis="x", rotation=45); ax.grid(axis="y", alpha=.25)
    _title(ax, "Publication timeline", "Verified primary transplantation studies in the curated evidence map")
    _save(fig, output_dir, "figure_02_publication_timeline")


def category_bar(df: pd.DataFrame, column: str, title: str, stem: str, output_dir: Path) -> None:
    counts = df[column].value_counts().sort_values()
    fig, ax = plt.subplots(figsize=(9, max(4.6, .55 * len(counts))))
    ax.barh(counts.index, counts.values, color=PALETTE[:len(counts)])
    for i, value in enumerate(counts.values): ax.text(value + .06, i, str(value), va="center")
    ax.set(xlabel="Included studies", ylabel=""); ax.set_xlim(0, max(counts.max() + 1, 2)); ax.grid(axis="x", alpha=.25)
    _title(ax, title, "Counts describe evidence coverage, not therapeutic efficacy")
    _save(fig, output_dir, stem)


def network_figure(graph: nx.Graph, output_dir: Path) -> None:
    type_colors = {"Organoid type": PALETTE[1], "Stem-cell source": PALETTE[2], "Target tissue": PALETTE[4], "Experimental model": PALETTE[0], "Reported outcome": PALETTE[3], "Translational barrier": "#999999"}
    fig, ax = plt.subplots(figsize=(14, 11)); pos = nx.spring_layout(graph, seed=42, k=1.35 / np.sqrt(max(graph.number_of_nodes(), 1)))
    colors = [type_colors.get(graph.nodes[n]["node_type"], "#777") for n in graph]
    sizes = [680 if graph.nodes[n]["node_type"] == "Organoid type" else 120 for n in graph]
    nx.draw_networkx_edges(graph, pos, ax=ax, width=.55, alpha=.28, edge_color="#667788")
    nx.draw_networkx_nodes(graph, pos, ax=ax, node_color=colors, node_size=sizes, linewidths=.4, edgecolors="white")
    major = {n: d["label"] for n, d in graph.nodes(data=True) if d["node_type"] == "Organoid type"}
    nx.draw_networkx_labels(graph, pos, major, ax=ax, font_size=9, font_weight="bold")
    handles = [plt.Line2D([0], [0], marker="o", linestyle="", color=c, label=t, markersize=8) for t, c in type_colors.items()]
    ax.legend(handles=handles, loc="lower left", frameon=False, ncol=2); ax.axis("off")
    ax.set_title("Organoid transplantation evidence network", loc="left", fontsize=17, fontweight="bold")
    ax.text(0, .99, "Edges are documented study relationships; layout and degree do not imply clinical readiness", transform=ax.transAxes, fontsize=9, color="#555")
    _save(fig, output_dir, "figure_05_research_network")


def evidence_heatmap(matrix: pd.DataFrame, output_dir: Path) -> None:
    columns = [c for c in matrix.columns if c not in {"organoid_type", "supporting_studies"}]
    mapping = {"Unassessed": 0, "Uncertain": 1, "Unsupported": 2, "Supported": 3}
    values = matrix.set_index("organoid_type")[columns].replace(mapping).astype(float)
    labels = matrix.set_index("organoid_type")[columns]
    cmap = matplotlib.colors.ListedColormap(["#EEEEEE", "#E69F00", "#D55E00", "#009E73"])
    fig, ax = plt.subplots(figsize=(12, 5.5)); sns.heatmap(values, cmap=cmap, vmin=0, vmax=3, linewidths=1, linecolor="white", cbar=False, ax=ax)
    ax.set_xticklabels([c.replace("_", " ").title() for c in columns], rotation=35, ha="right"); ax.set(xlabel="", ylabel="")
    for y in range(labels.shape[0]):
        for x in range(labels.shape[1]): ax.text(x + .5, y + .5, labels.iloc[y, x], ha="center", va="center", fontsize=6.8)
    _title(ax, "Translational evidence matrix", "Descriptive support across the curated preclinical literature; not a readiness score")
    _save(fig, output_dir, "figure_06_translational_evidence_heatmap")


def barrier_landscape(df: pd.DataFrame, output_dir: Path) -> None:
    keywords = {"No urinary/collecting outlet": "outlet|collecting", "Model generalizability": "mouse|rat|avian|xenograft|chimeric", "Immaturity": "immature|maturation", "Safety/QC": "safety|off-target|quality", "Short/limited follow-up": "short follow|long-term", "Ethical concerns": "ethical"}
    counts = {label: df["major_limitations"].str.contains(pattern, case=False, regex=True, na=False).sum() for label, pattern in keywords.items()}
    series = pd.Series(counts).sort_values()
    fig, ax = plt.subplots(figsize=(9, 5)); ax.barh(series.index, series.values, color=PALETTE[5]); ax.set(xlabel="Studies mentioning coded limitation", ylabel=""); ax.grid(axis="x", alpha=.25)
    _title(ax, "Translational barrier landscape", "Keyword-coded from study-level limitation notes; categories can overlap")
    _save(fig, output_dir, "figure_07_translational_barriers")


def conceptual_workflow(output_dir: Path) -> None:
    steps = ["Stem-cell\nsource", "Directed\ndifferentiation", "Organoid\ndevelopment", "Characterization", "Preclinical\nengraftment", "Functional\nassessment", "Clinical translation\nevaluation"]
    fig, ax = plt.subplots(figsize=(13, 2.8)); ax.axis("off")
    for i, step in enumerate(steps):
        ax.text(i, .5, step, ha="center", va="center", fontsize=8.5, bbox={"boxstyle":"round,pad=.45", "fc":"#EAF2F8", "ec":PALETTE[0]})
        if i < len(steps)-1: ax.annotate("", (i+.62,.5), (i+.38,.5), arrowprops={"arrowstyle":"->", "color":"#555"})
    ax.set_xlim(-.65, len(steps)-.35); ax.set_ylim(0,1); ax.set_title("Conceptual organoid transplantation pathway", loc="left", fontweight="bold")
    _save(fig, output_dir, "figure_08_conceptual_transplantation_workflow")


def evidence_gaps(matrix: pd.DataFrame, output_dir: Path) -> None:
    cols = [c for c in matrix.columns if c not in {"organoid_type", "supporting_studies"}]
    gaps = (matrix[cols] != "Supported").sum().sort_values()
    fig, ax = plt.subplots(figsize=(9, 5)); ax.barh([c.replace("_", " ").title() for c in gaps.index], gaps.values, color=PALETTE[3]); ax.set(xlabel="Organoid categories without supported evidence", ylabel=""); ax.grid(axis="x", alpha=.25)
    _title(ax, "Evidence gaps", "Unassessed, uncertain, and unsupported cells in the translational matrix")
    _save(fig, output_dir, "figure_09_evidence_gaps")


def generate_all_figures(df: pd.DataFrame, graph: nx.Graph, matrix: pd.DataFrame, output_dir: Path) -> list[Path]:
    sns.set_theme(style="whitegrid", context="notebook")
    workflow_figure(output_dir)
    publication_timeline(df, output_dir)
    category_bar(df, "organoid_type", "Organoid research distribution", "figure_03_organoid_distribution", output_dir)
    category_bar(df, "stem_cell_source", "Stem-cell source categories", "figure_04_stem_cell_sources", output_dir)
    network_figure(graph, output_dir)
    evidence_heatmap(matrix, output_dir)
    barrier_landscape(df, output_dir)
    conceptual_workflow(output_dir)
    evidence_gaps(matrix, output_dir)
    return sorted(output_dir.glob("figure_*.png"))

