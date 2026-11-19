#!/usr/bin/env python3
"""Render P1c GeoJSON over the existing top-down overview."""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from shapely.geometry import shape


HERE = Path(__file__).resolve().parent
RELIEF = HERE.parents[1]
ROOT = RELIEF.parents[0]
VECTOR = RELIEF / "detail_v2" / "vektor"
SOURCE = ROOT / "raster_c20_z25_vorschau.png"
SCALE = 3.0  # preview map body: 1008 x 909 px = 336 x 303 cells


def load(name):
    return json.loads((VECTOR / f"{name}.geojson").read_text(encoding="utf-8"))["features"]


def each_line(geom):
    if geom.geom_type == "LineString":
        yield list(geom.coords)
    elif geom.geom_type == "Polygon":
        yield list(geom.exterior.coords)
        for ring in geom.interiors:
            yield list(ring.coords)
    elif geom.geom_type in ("MultiLineString", "MultiPolygon", "GeometryCollection"):
        for part in geom.geoms:
            yield from each_line(part)


def pxline(coords, origin=(0.0, 0.0), scale=SCALE):
    ox, oz = origin
    return [((x - ox) * scale, (z - oz) * scale) for x, z, *_ in coords]


def draw_features(draw, feature_sets, origin=(0.0, 0.0), scale=SCALE, width=1):
    for name, features in feature_sets:
        for f in features:
            props = f.get("properties", {})
            geom = shape(f["geometry"])
            if name == "zones":
                if props.get("layer") != "flaechentyp":
                    continue
                color = {"wasser": (45, 118, 220), "bruecke": (255, 220, 70),
                         "weg": (244, 66, 91), "ufer": (60, 194, 212),
                         "fels": (190, 112, 45), "grund": (50, 120, 85)}.get(props.get("typ"), (255, 255, 255))
                line_width = max(1, width)
            elif name == "kanten":
                color = (255, 48, 25) if props.get("typ") != "steil55" else (255, 177, 24)
                line_width = max(2, width + 1)
            else:
                color = (255, 25, 220)
                line_width = max(2, width + 1)
            for coords in each_line(geom):
                points = pxline(coords, origin, scale)
                if len(points) >= 2:
                    draw.line(points, fill=color, width=line_width, joint="curve")


def render(base: Image.Image, out: Path, feature_sets, origin=(0, 0), span=None, scale=SCALE, title=None):
    if span:
        x0, z0, x1, z1 = span
        crop = base.crop((int(x0 * SCALE), int(z0 * SCALE), int(x1 * SCALE), int(z1 * SCALE)))
        crop = crop.resize((int((x1 - x0) * scale), int((z1 - z0) * scale)), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (crop.width, crop.height + 36), (30, 36, 44))
        canvas.paste(crop, (0, 36))
        draw = ImageDraw.Draw(canvas)
        draw.text((10, 10), title or "P1c Vektoren", fill=(250, 250, 250))
        draw_features(draw, feature_sets, origin=(x0, z0 - 36 / scale), scale=scale, width=2)
        anchors = [(300, 90, "300|90"), (290, 98, "290|98")] if title and title.startswith("G3/H3") else (
            [(84, 129, "84|129")] if title and title.startswith("B3/C3") else [])
        for x, z, label in anchors:
            px, py = (x - x0) * scale, 36 + (z - z0) * scale
            draw.ellipse((px - 7, py - 7, px + 7, py + 7), fill=(255, 244, 55), outline=(20, 20, 20), width=2)
            draw.text((px + 9, py - 16), label, fill=(20, 20, 20), stroke_width=1, stroke_fill=(255, 255, 255))
    else:
        canvas = Image.new("RGB", (base.width, base.height + 54), (30, 36, 44))
        canvas.paste(base, (0, 54))
        draw = ImageDraw.Draw(canvas)
        draw.text((12, 8), "P1c · Grat, Klippenkanten und Flächentypen", fill=(250, 250, 250))
        draw.text((12, 30), "Flächengrenzen · Steilheit 55° · Klippen · Grate (Viewer-Meter)", fill=(225, 230, 235))
        draw_features(draw, feature_sets, origin=(0, -54 / SCALE), scale=SCALE, width=1)
    canvas.save(out, "JPEG", quality=85, optimize=True, progressive=True)


def main():
    old = Image.open(SOURCE).convert("RGB").crop((0, 0, 1008, 909))
    features = [("zones", load("zonen")), ("kanten", load("kanten")), ("grat", load("grat"))]
    render(old, HERE / "uebersicht_kanten.jpg", features)
    render(old, HERE / "nahbild_g3h3.jpg", features, span=(275, 65, 325, 115), scale=9.0,
           title="G3/H3 · Gratanker 300|90 und 290|98")
    render(old, HERE / "nahbild_b3c3.jpg", features, span=(59, 104, 109, 154), scale=9.0,
           title="B3/C3 · Gratanker 84|129")
    for p in (HERE / "uebersicht_kanten.jpg", HERE / "nahbild_g3h3.jpg", HERE / "nahbild_b3c3.jpg"):
        im = Image.open(p)
        print(f"{p.name}: {im.width}x{im.height} {p.stat().st_size} bytes")


if __name__ == "__main__":
    main()
