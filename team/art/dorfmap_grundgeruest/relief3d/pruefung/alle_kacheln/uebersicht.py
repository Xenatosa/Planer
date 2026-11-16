#!/usr/bin/env python3
"""P10: Uebersichtsbild aus den 56 Nahbildern (8 Spalten A-H x 7 Zeilen 1-7).
Aufruf: python3 pruefung/alle_kacheln/uebersicht.py [/tmp/p10/nahbilder] [/tmp/p10/nahbilder_uebersicht.png] [Breite=320] [lochscan_alle.json]
Mit Lochscan-JSON wird die R5_loch-Zahl je Kachel ins Bild geschrieben."""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

d = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/p10/nahbilder")
out = Path(sys.argv[2] if len(sys.argv) > 2 else "/tmp/p10/nahbilder_uebersicht.png")
w = int(sys.argv[3]) if len(sys.argv) > 3 else 320
loch = json.loads(Path(sys.argv[4]).read_text())["je_kachel"] if len(sys.argv) > 4 else None
erst = Image.open(d / "A1.png")
h = round(w * erst.height / erst.width)
rand, kopf = 4, 34
B = Image.new("RGB", (8 * (w + rand) + rand + 30, 7 * (h + rand) + rand + kopf), (40, 44, 48))
dr = ImageDraw.Draw(B)
try:
    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
except OSError:
    f = ImageFont.load_default()
for i, c in enumerate("ABCDEFGH"):
    dr.text((30 + rand + i * (w + rand) + w // 2 - 6, 6), c, fill=(255, 255, 255), font=f)
for r in range(1, 8):
    dr.text((8, kopf + rand + (r - 1) * (h + rand) + h // 2 - 10), str(r), fill=(255, 255, 255), font=f)
    for i, c in enumerate("ABCDEFGH"):
        t = f"{c}{r}"
        p = d / f"{t}.png"
        x, y = 30 + rand + i * (w + rand), kopf + rand + (r - 1) * (h + rand)
        if p.exists():
            B.paste(Image.open(p).convert("RGB").resize((w, h), Image.LANCZOS), (x, y))
        else:
            dr.rectangle([x, y, x + w, y + h], outline=(200, 60, 60))
            dr.text((x + 8, y + 8), f"{t} fehlt", fill=(255, 120, 120), font=f)
        if loch is not None:
            n = loch.get(t, 0)
            dr.text((x + w - 70, y + 6), f"R5 {n}", fill=(255, 80, 80) if n else (180, 255, 180), font=f)
B.save(out, optimize=True)
print(out, B.size, out.stat().st_size)
