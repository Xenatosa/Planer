#!/usr/bin/env python3
"""Deterministische Bestandsmessung an der Dorfkarten-Zellquelle.

Die Eingabe wird nur gelesen. Zellzahlen sind Kartenmessungen; Objektzahlen
aus relief_daten.json.gz werden getrennt als Modellbestand ausgewiesen.
Aufruf im relief3d-Ordner: python3 pruefung/regelmessung.py [--out DATEI]
"""
from __future__ import annotations

import argparse
import csv
import gzip
import json
import math
from collections import deque
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[2]
RELIEF3D = Path(__file__).resolve().parents[1]
TILE_X = "ABCDEFGH"
NX, NY = 336, 303
SOURCE_FIELDS = (
    "untergrund", "hindernis_id", "hindernis_art", "wasser_eis", "ebene",
    "bauzone_bestand", "bauzone_plan", "begehbar", "bebaubar",
)


def percentile(values: Iterable[float], p: float) -> float | None:
    a = sorted(float(v) for v in values if math.isfinite(float(v)))
    if not a:
        return None
    q = (len(a) - 1) * p / 100
    lo, hi = math.floor(q), math.ceil(q)
    v = a[lo] + (a[hi] - a[lo]) * (q - lo)
    return round(v, 4)


def components(mask: list[list[bool]]) -> dict:
    """8-neighbour connected regions, reported as cell areas."""
    h, w = len(mask), len(mask[0]) if mask else 0
    seen = bytearray(h * w)
    sizes: list[int] = []
    for y in range(h):
        for x in range(w):
            i = y * w + x
            if not mask[y][x] or seen[i]:
                continue
            seen[i] = 1
            q = deque([(x, y)])
            n = 0
            while q:
                cx, cy = q.popleft()
                n += 1
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if not (dx or dy):
                            continue
                        xx, yy = cx + dx, cy + dy
                        if 0 <= xx < w and 0 <= yy < h:
                            j = yy * w + xx
                            if mask[yy][xx] and not seen[j]:
                                seen[j] = 1
                                q.append((xx, yy))
            sizes.append(n)
    return {
        "components_8n": len(sizes),
        "largest_component_cells": max(sizes, default=0),
        "component_area_cells_p50": percentile(sizes, 50),
        "component_area_cells_p95": percentile(sizes, 95),
    }


def tile(cx: int, cy: int) -> str:
    return f"{TILE_X[min(7, cx // 42)]}{min(6, cy // 43) + 1}"


def measure(karte: Path, bauplan: Path, relief: Path | None) -> dict:
    grid: list[list[dict | None]] = [[None for _ in range(NX)] for _ in range(NY)]
    with karte.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            x, y = int(row["cx"]), int(row["cy"])
            if not (0 <= x < NX and 0 <= y < NY) or grid[y][x] is not None:
                raise ValueError(f"ungueltige oder doppelte Zellkoordinate ({x}, {y})")
            grid[y][x] = row
    if any(v is None for row in grid for v in row):
        raise ValueError("Dorfkartenraster ist nicht vollstaendig 336x303")
    rows = [v for row in grid for v in row if v is not None]

    def mask(predicate) -> list[list[bool]]:
        return [[bool(predicate(r)) for r in row] for row in grid]  # type: ignore[arg-type]

    def count(predicate) -> int:
        return sum(bool(predicate(r)) for r in rows)

    def per_tile(predicate) -> dict[str, int]:
        out = {f"{x}{y}": 0 for y in range(1, 8) for x in TILE_X}
        for r in rows:
            if predicate(r):
                out[tile(int(r["cx"]), int(r["cy"]))] += 1
        return out

    forest = mask(lambda r: r["untergrund"] == "WALD")
    tree_sites = mask(lambda r: r["deko_baum_ok"] == "1")
    rock_sites = mask(lambda r: r["deko_fels_ok"] == "1")
    mountain = mask(lambda r: bool(r["wand_name"]) or r["ebene"] in {"KRATER", "GIPFEL", "SIMS"})
    shade = mask(lambda r: r["untergrund"] == "SCHATTEN")
    deco_capacity = [float(r["deko_kapazitaet"]) for r in rows]

    plan = json.loads(bauplan.read_text(encoding="utf-8"))
    buildings = plan.get("E40", [])
    dims = []
    areas = []
    building_tiles: dict[str, int] = {}
    for b in buildings:
        poly = b.get("poly", [])
        if len(poly) < 4:
            continue
        points = poly[:-1] if poly[0] == poly[-1] else poly
        # The recorded placement transform is 1.2 map metres per plan unit.
        xs = [(float(p[0]) + 200.0) * 1.2 for p in points]
        zs = [(float(p[1]) + 40.0) * 1.2 for p in points]
        cx, cz = sum(xs) / len(xs), sum(zs) / len(zs)
        btile = tile(max(0, min(NX - 1, int(cx))), max(0, min(NY - 1, int(cz))))
        building_tiles[btile] = building_tiles.get(btile, 0) + 1
        dims.append((max(xs) - min(xs), max(zs) - min(zs)))
        twice_area = sum(
            xs[i] * zs[(i + 1) % len(xs)] - xs[(i + 1) % len(xs)] * zs[i]
            for i in range(len(xs))
        )
        areas.append(abs(twice_area) / 2)

    model_objects = {}
    model_objects_by_tile = {}
    if relief is not None:
        with gzip.open(relief, "rt", encoding="utf-8") as f:
            d = json.load(f)
        for key in ("baeume", "felsen", "felsbloecke", "findlinge", "steine", "geroell", "gras", "haeuser", "bruecken"):
            objects = d.get(key, [])
            model_objects[key] = len(objects)
            per = {"D1": 0, "G1": 0, "D2": 0}
            for o in objects:
                if key == "haeuser":
                    x, z = float(o["x"]), float(o["z"])
                else:
                    x, z = float(o[0]), float(o[2])
                t = tile(max(0, min(NX - 1, int(x))), max(0, min(NY - 1, int(z))))
                if t in per:
                    per[t] += 1
            model_objects_by_tile[key] = per
        model_objects["wald_trees_note"] = "Anzahl ist Modellbestand; die Zellquelle zeichnet keine Einzelbaumkoordinaten."

    named_mountains = {}
    for name in ("Nord", "Suedgrat", "Krater", "Ostgrat"):
        m = mask(lambda r, n=name: r["wand_name"] == n)
        named_mountains[name] = {"source_cells": sum(sum(row) for row in m), **components(m)}

    slots: dict[str, int] = {}
    for r in rows:
        slots[r["skin_slot"]] = slots.get(r["skin_slot"], 0) + 1

    return {
        "quelle": {
            "karte": "raster_c20_z25_zellen.csv",
            "rows": len(rows),
            "grid_cells": [NX, NY],
            "cell_size_m": 1.0,
            "map_scale_px_per_m": 25,
            "tile_formula": "ABCDEFGH[cx//42] + str(cy//43+1)",
            "source_fields_read_only": list(SOURCE_FIELDS),
        },
        "elemente": {
            "wald_boden": {
                "source_cells": count(lambda r: r["untergrund"] == "WALD"),
                "area_m2": count(lambda r: r["untergrund"] == "WALD"),
                **components(forest),
                "cells_by_tile": per_tile(lambda r: r["untergrund"] == "WALD"),
            },
            "baeume_einzeln": {
                "individual_tree_coordinates_in_map": 0,
                "eligible_planting_cells_deko_baum_ok": count(lambda r: r["deko_baum_ok"] == "1"),
                "eligible_cells_by_tile": per_tile(lambda r: r["deko_baum_ok"] == "1"),
                "limitation": "Die Dorfkarte markiert Eignungszellen, keine einzelnen Baumstandorte.",
            },
            "baumgruppen": {
                "forest_components_8n": components(forest)["components_8n"],
                "eligible_site_components_8n": components(tree_sites)["components_8n"],
                "limitation": "Gruppen sind 8-Nachbar-Komponenten von Wald-/Eignungszellen, keine Sichtklassifikation.",
            },
            "gebaeude_platzhalter": {
                "E40_plan_polygons": len(buildings),
                "bbox_width_m_p5_median_p95": [percentile([v[0] for v in dims], p) for p in (5, 50, 95)],
                "bbox_depth_m_p5_median_p95": [percentile([v[1] for v in dims], p) for p in (5, 50, 95)],
                "polygon_area_m2_p5_median_p95": [percentile(areas, p) for p in (5, 50, 95)],
                "bauzone_bestand_cells": count(lambda r: r["bauzone_bestand"] == "1"),
                "bauzone_plan_cells": count(lambda r: r["bauzone_plan"] == "1"),
                "bebaubar_cells": count(lambda r: r["bebaubar"] == "1"),
            },
            "fels": {
                "terrain_fels_cells": count(lambda r: r["untergrund"] == "FELS"),
                "eligible_placement_cells_deko_fels_ok": count(lambda r: r["deko_fels_ok"] == "1"),
                "eligible_cells_by_tile": per_tile(lambda r: r["deko_fels_ok"] == "1"),
                "eligible_site_components_8n": components(rock_sites)["components_8n"],
                "limitation": "deko_fels_ok bezeichnet erlaubte Zellen, keine gezeichneten Felsobjekte.",
            },
            "deko": {
                "positive_capacity_cells": count(lambda r: float(r["deko_kapazitaet"]) > 0),
                "positive_capacity_cells_by_tile": per_tile(lambda r: float(r["deko_kapazitaet"]) > 0),
                "capacity_sum_source_units": round(sum(deco_capacity), 4),
                "capacity_sum_by_tile_source_units": {
                    t: round(sum(float(r["deko_kapazitaet"]) for r in rows if tile(int(r["cx"]), int(r["cy"])) == t), 4)
                    for t in ("D1", "G1", "D2")
                },
                "capacity_p5_median_p95": [percentile(deco_capacity, p) for p in (5, 50, 95)],
                "limitation": "Die Quelle spezifiziert keine Einheit oder sichtbare Grashalmgeometrie.",
            },
            "gebirge": {
                "source_cells_wand_or_krater_gipfel_sims": sum(sum(row) for row in mountain),
                "source_cells_by_tile": per_tile(lambda r: bool(r["wand_name"]) or r["ebene"] in {"KRATER", "GIPFEL", "SIMS"}),
                "named_wall_bands": named_mountains,
                "source_cell_counts_by_ebene": {
                    label: count(lambda r, v=label: r["ebene"] == v)
                    for label in ("KRATER", "GIPFEL", "SIMS", "WAND", "HANG")
                },
            },
            "wiese_kandidat": {
                "boden_cells": count(lambda r: r["untergrund"] == "BODEN"),
                "boden_cells_by_tile": per_tile(lambda r: r["untergrund"] == "BODEN"),
                "status_note": "BODEN ist ein Quellmaterial; eine eigene WIESEN-Klasse fehlt.",
            },
            "schatten": {
                "source_cells_skin_slot_schatten": sum(sum(row) for row in shade),
                "status_note": "Das Kartenlabel ist messbar; ein Beleuchtungs-/Schattenwurf-Pruefer fehlt.",
            },
            "materialklassen": {
                "source_cells_by_skin_slot": dict(sorted(slots.items())),
            },
        },
        "modellbestand_aus_relief_daten": model_objects,
        "modellbestand_D1_G1_D2": model_objects_by_tile,
        "bauplan_E40_polygone_D1_G1_D2": {t: building_tiles.get(t, 0) for t in ("D1", "G1", "D2")},
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--karte", type=Path, default=ROOT / "raster_c20_z25_zellen.csv")
    ap.add_argument("--bauplan", type=Path, default=ROOT / "pruefung/quelle_plaetze_wachstum_ausbau_planm.json")
    ap.add_argument("--relief", type=Path, default=RELIEF3D / "relief_daten.json.gz")
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    result = measure(args.karte, args.bauplan, args.relief)
    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
