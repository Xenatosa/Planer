#!/usr/bin/env python3
"""Nahbilder (16 m Ausschnitt, ~19 px/m) an q3-Fundorten der Gruppe a (Tripelpunkte)
fuer die Sichtpruefung. Aufruf: nah_tripelpunkte.py AUSGABE.jpg "x|z,x|z,..." [halbe_breite_m]
"""
import sys, json
sys.path.insert(0, "/workspace/wt_dv2_zonen2/team/art/dorfmap_grundgeruest/relief3d/detail_v2/kanten")
import render_vektoren as rv
from PIL import Image
pts = [tuple(map(float, a.split("|"))) for a in sys.argv[2].split(",")]
half = float(sys.argv[3]) if len(sys.argv) > 3 else 8.0
base = Image.open(rv.SOURCE).convert("RGB").crop((0, 0, 1008, 909))
zonen = rv.load("zonen")
ims = []
for x, z in pts:
    b = rv.Bild(base, span=(x - half, z - half, x + half, z + half), scale=300 / (2 * half), titel=f"{x:g}|{z:g}  ({2*half:g} m)")
    rv.zonen_bild(b, zonen, w=2)
    c = 150
    b.d.ellipse([(c - 5, 40 + c - 5), (c + 5, 40 + c + 5)], outline=(255, 255, 0, 255), width=2)
    ims.append(b.bild())
W = sum(i.width for i in ims) + 6 * (len(ims) - 1)
out = Image.new("RGB", (W, ims[0].height), (30, 36, 44)); x = 0
for i in ims:
    out.paste(i, (x, 0)); x += i.width + 6
out.save(sys.argv[1], "JPEG", quality=82)
