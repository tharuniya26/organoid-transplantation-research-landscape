"""Inventory embedded source-PDF images without extracting them for reuse."""
from __future__ import annotations
from pathlib import Path
import csv
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "source_material_private"
rows = []
for pdf_path in sorted(SOURCES.glob("*.pdf")):
    doc = pymupdf.open(pdf_path)
    for page in doc:
        images = page.get_images(full=True)
        for index, item in enumerate(images, start=1):
            xref, width, height, bpc, colorspace = item[0], item[2], item[3], item[4], item[5]
            rows.append({"source_document": pdf_path.name, "page": page.number + 1, "image_index": index, "xref": xref, "width_px": width, "height_px": height, "bits_per_component": bpc, "colorspace": colorspace})
        if pdf_path.name.startswith("Organoids-"):
            pix = page.get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5), alpha=False)
            pix.save(ROOT / ".work" / "presentation_page.png")
out = ROOT / "data" / "metadata" / "source_image_inventory.csv"
with out.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=rows[0].keys() if rows else ["source_document", "page"])
    writer.writeheader(); writer.writerows(rows)
print(f"Inventoried {len(rows)} embedded images across {len(list(SOURCES.glob('*.pdf')))} PDFs")
