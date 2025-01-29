"""Build a temporary contact sheet for visual QA of generated PNG figures."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
paths = sorted((ROOT / "figures").glob("figure_*.png"))
thumbs = []
for path in paths:
    image = Image.open(path).convert("RGB")
    image.thumbnail((600, 420))
    canvas = Image.new("RGB", (620, 470), "white")
    canvas.paste(image, ((620 - image.width) // 2, 35))
    ImageDraw.Draw(canvas).text((10, 10), path.stem, fill="black")
    thumbs.append(canvas)
cols = 3
rows = (len(thumbs) + cols - 1) // cols
sheet = Image.new("RGB", (cols * 620, rows * 470), "#dddddd")
for index, item in enumerate(thumbs):
    sheet.paste(item, ((index % cols) * 620, (index // cols) * 470))
out = ROOT / ".work" / "figure_contact_sheet.png"
sheet.save(out)
print(f"Rendered contact sheet for {len(paths)} figures: {out}")
