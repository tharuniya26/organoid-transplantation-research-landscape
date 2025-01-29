"""Render report pages to a contact sheet for visual QA."""
from pathlib import Path
import pymupdf
from PIL import Image, ImageOps, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
doc = pymupdf.open(ROOT / "reports" / "organoid_transplantation_evidence_mapping.pdf")
thumbs = []
for page in doc:
    pix = page.get_pixmap(matrix=pymupdf.Matrix(0.8, 0.8), alpha=False)
    image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    canvas = Image.new("RGB", (image.width + 20, image.height + 35), "white")
    canvas.paste(image, (10, 25)); ImageDraw.Draw(canvas).text((10, 7), f"Page {page.number + 1}", fill="black")
    thumbs.append(canvas)
cols = 3; rows = (len(thumbs) + cols - 1) // cols
cell_w = max(i.width for i in thumbs); cell_h = max(i.height for i in thumbs)
sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), "#dddddd")
for index, item in enumerate(thumbs): sheet.paste(item, ((index % cols) * cell_w, (index // cols) * cell_h))
sheet.save(ROOT / ".work" / "report_contact_sheet.png")
print(f"pages={doc.page_count}; text_chars={sum(len(page.get_text()) for page in doc)}")
