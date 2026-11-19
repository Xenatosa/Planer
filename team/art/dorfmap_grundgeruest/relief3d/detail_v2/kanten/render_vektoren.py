#!/usr/bin/env python3
"""Bilder zur konstruktiven Zonen-Neufassung (P1c-Nacharbeit), alle < 1 MB.

  kanten/uebersicht_zonen.jpg   Flaechentyp gefuellt + Untergrundgrenzen, Kanten, Grat
  kanten/nahbild_72_154.jpg     Nahbild um 72|154
  kanten/e2_vorher_nachher.jpg  Bruecke E2: vorher (ed6e935, Zellpolygone) | nachher
  ../tag1_vektoren.jpg          alle Vektoren ueber der alten Draufsicht
Aufruf: render_vektoren.py [--vorher ZONEN_VORHER.geojson]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw
from shapely.geometry import shape

HERE = Path(__file__).resolve().parent
RELIEF = HERE.parents[1]
ROOT = RELIEF.parents[0]
VECTOR = RELIEF / "detail_v2" / "vektor"
SOURCE = ROOT / "raster_c20_z25_vorschau.png"
SCALE = 3.0
FT = {"wasser": (45, 118, 220), "bruecke": (255, 220, 70), "weg": (244, 66, 91),
      "ufer": (60, 194, 212), "fels": (150, 95, 50), "grund": (60, 140, 90)}


def load(name, path=None):
    p = Path(path) if path else VECTOR / f"{name}.geojson"
    return json.loads(p.read_text(encoding="utf-8"))["features"]


def rings(g):
    if g.geom_type == "Polygon":
        yield list(g.exterior.coords), [list(r.coords) for r in g.interiors]
    elif hasattr(g, "geoms"):
        for q in g.geoms:
            yield from rings(q)


def lines(g):
    if g.geom_type == "LineString":
        yield list(g.coords)
    elif g.geom_type == "Polygon":
        yield list(g.exterior.coords)
        for r in g.interiors:
            yield list(r.coords)
    elif hasattr(g, "geoms"):
        for q in g.geoms:
            yield from lines(q)


class Bild:
    def __init__(self, base, span=None, scale=SCALE, kopf=40, titel=""):
        if span:
            x0, z0, x1, z1 = span
            crop = base.crop((int(x0 * SCALE), int(z0 * SCALE), int(x1 * SCALE), int(z1 * SCALE)))
            crop = crop.resize((int((x1 - x0) * scale), int((z1 - z0) * scale)), Image.Resampling.LANCZOS)
        else:
            x0, z0, crop = 0.0, 0.0, base
        self.o, self.s, self.k, self.titel = (x0, z0), scale, kopf, titel
        self.im = Image.new("RGB", (crop.width, crop.height + kopf), (30, 36, 44))
        self.im.paste(crop, (0, kopf))
        self.ov = Image.new("RGBA", self.im.size, (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.ov)

    def px(self, cs):
        return [((x - self.o[0]) * self.s, self.k + (z - self.o[1]) * self.s) for x, z, *_ in cs]

    def fill(self, g, rgb, a=110):
        for ext, holes in rings(g):
            self.d.polygon(self.px(ext), fill=rgb + (a,))
            for h in holes:
                self.d.polygon(self.px(h), fill=(0, 0, 0, 0))

    def line(self, g, rgb, w=1, a=255):
        for cs in lines(g):
            p = self.px(cs)
            if len(p) >= 2:
                self.d.line(p, fill=rgb + (a,), width=w, joint="curve")

    def bild(self):
        img = Image.alpha_composite(self.im.convert("RGBA"), self.ov).convert("RGB")
        d = ImageDraw.Draw(img)
        d.rectangle([(0, 0), (img.width, self.k)], fill=(30, 36, 44))
        d.text((10, 12), self.titel, fill=(250, 250, 250))
        return img

    def save(self, out):
        img = self.bild()
        img.save(out, "JPEG", quality=82, optimize=True, progressive=True)
        print(f"{out}: {img.width}x{img.height} {Path(out).stat().st_size} bytes")


def zonen_bild(b, zonen, w=1, fuellen=True):
    for f in zonen:
        p = f["properties"]
        if p.get("layer") == "flaechentyp":
            g = shape(f["geometry"])
            if fuellen:
                b.fill(g, FT.get(p["typ"], (255, 255, 255)), 120)
            b.line(g, FT.get(p["typ"], (255, 255, 255)), w)
    for f in zonen:
        if f["properties"].get("layer") == "untergrund":
            b.line(shape(f["geometry"]), (255, 255, 255), max(1, w - 1), 200)


def kanten_grat(b, kanten, grat, w=2):
    for f in kanten:
        b.line(shape(f["geometry"]), (255, 48, 25) if f["properties"].get("typ") != "steil55" else (255, 177, 24), w)
    for f in grat:
        b.line(shape(f["geometry"]), (255, 25, 220), w)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vorher", default=None)
    a = ap.parse_args()
    base = Image.open(SOURCE).convert("RGB").crop((0, 0, 1008, 909))
    zonen, kanten, grat = load("zonen"), load("kanten"), load("grat")

    b = Bild(base, titel="P1c Zonen konstruktiv: Flaechentyp (gefuellt), Untergrundgrenzen (weiss), Kanten, Grat")
    zonen_bild(b, zonen)
    kanten_grat(b, kanten, grat)
    b.save(HERE / "uebersicht_zonen.jpg")

    b = Bild(base, span=(47, 129, 97, 179), scale=12.0, titel="Nahbild 72|154 (50 x 50 m)")
    zonen_bild(b, zonen, w=2)
    kanten_grat(b, kanten, grat, 3)
    b.d.ellipse([(300 - 6, 340 - 6), (300 + 6, 340 + 6)], outline=(255, 255, 0, 255), width=3)
    b.save(HERE / "nahbild_72_154.jpg")

    if a.vorher:
        span = (176, 59, 207, 90)
        v = Bild(base, span=span, scale=14.0, titel="E2 vorher (ed6e935, Zellpolygone)")
        zonen_bild(v, load("", a.vorher), w=2)
        n = Bild(base, span=span, scale=14.0, titel="E2 nachher (konstruktiv aus Vektoren)")
        zonen_bild(n, zonen, w=2)
        rect = shape({"type": "Polygon", "coordinates": [[(186, 73), (197, 73), (197, 75), (186, 75), (186, 73)]]})
        for x in (v, n):
            x.line(rect, (255, 255, 255), 1, 160)
        vi, ni = v.bild(), n.bild()
        both = Image.new("RGB", (vi.width + ni.width + 8, vi.height), (30, 36, 44))
        both.paste(vi, (0, 0))
        both.paste(ni, (vi.width + 8, 0))
        out = HERE / "e2_vorher_nachher.jpg"
        both.save(out, "JPEG", quality=82, optimize=True, progressive=True)
        print(f"{out}: {both.width}x{both.height} {out.stat().st_size} bytes")

    b = Bild(base, titel="Tag 1 Vektoren: Wege, Kreuzungen, Wasser, Ufer, Kanten, Grat, Zonen (alte Draufsicht)")
    zonen_bild(b, zonen, fuellen=False)
    for f in load("wasser"):
        b.fill(shape(f["geometry"]), (45, 118, 220), 90)
        b.line(shape(f["geometry"]), (20, 70, 200), 2)
    for f in load("ufer"):
        if f["properties"].get("typ") == "uferlinie":
            b.line(shape(f["geometry"]), (0, 230, 255), 1)
    for f in load("wege"):
        r = f["properties"].get("rolle")
        if r == "mittellinie":
            b.line(shape(f["geometry"]), (255, 255, 255), 1)
        elif r in ("rand_links", "rand_rechts"):
            b.line(shape(f["geometry"]), (244, 66, 91), 1)
    for f in load("kreuzungen"):
        b.fill(shape(f["geometry"]), (255, 140, 0), 120)
    kanten_grat(b, kanten, grat)
    b.save(RELIEF / "detail_v2" / "tag1_vektoren.jpg")


if __name__ == "__main__":
    main()
