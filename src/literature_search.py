"""Reproducible public-metadata retrieval for PubMed and ClinicalTrials.gov."""
from __future__ import annotations

import json
import logging
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

LOGGER = logging.getLogger(__name__)
PUBMED_ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"


def build_pubmed_url(query: str, retmax: int = 500) -> str:
    """Build an NCBI E-utilities JSON search URL without credentials."""
    params = {"db": "pubmed", "term": query, "retmode": "json", "retmax": retmax}
    return f"{PUBMED_ESEARCH}?{urlencode(params)}"


def search_pubmed(query: str, cache_path: Path, retmax: int = 500) -> dict:
    """Retrieve PubMed identifiers or reuse an existing raw cache."""
    if cache_path.exists():
        return json.loads(cache_path.read_text(encoding="utf-8"))
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    request = Request(build_pubmed_url(query, retmax), headers={"User-Agent": "organoid-evidence-map/1.0"})
    try:
        with urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except OSError as exc:
        raise RuntimeError(f"PubMed retrieval failed: {exc}") from exc
    cache_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    LOGGER.info("Cached PubMed search at %s", cache_path)
    return payload

