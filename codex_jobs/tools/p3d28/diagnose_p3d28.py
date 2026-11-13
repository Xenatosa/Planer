#!/usr/bin/env python3
"""Reproduce the p3d27 D1 Float32 delta diagnosis for p3d28."""
from __future__ import annotations

import base64
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy import ndimage as ndi

ROOT = Path(__file__).resolve().parents[3]
TOOLS = ROOT / "codex_jobs/tools/p3d28"
RESULTS = TOOLS / "results"
RELIEF3D = ROOT / "team/art/dorfmap_grundgeruest/relief3d"
D1 = (126.0, 0.0, 168.0, 43.0)
REFERENCE = Path("/tmp/relief_p3d27_r3_reference_after.json.gz")


def load_relief(path: Path) -> dict:
    return json.loads(gzip.decompress(path.read_bytes()))


def d1_heights(data: dict) -> np.ndarray:
    rs = int(data["rs"])
    nx, ny = int(data["nx"]), int(data["ny"])
    g = np.frombuffer(base64.b64decode(data["GB"]), dtype=np.float32)
    g = g.reshape(ny * rs + 1, nx * rs + 1)
    x0, z0, x1, z1 = D1
    return g[int(z0 * rs):int(z1 * rs) + 1,
             int(x0 * rs):int(x1 * rs) + 1].copy()


def read_probe(round_no: int) -> tuple[dict, dict]:
    probe = json.loads((RESULTS.parent.parent / "p3d27" / "results" /
                        f"p3d27_V3_round{round_no:02d}_official_probe.json").read_text())
    relief_path = Path(probe["probe_relief"])
    if not relief_path.exists():
        raise FileNotFoundError(relief_path)
    return probe, load_relief(relief_path)


def hit_sets(probe: dict) -> dict[str, list[dict]]:
    hits = {"R5_loch": [], "G5_beule_klippe": [], "R4_schlucht": [],
            "R8b_delle": []}
    for hit in probe.get("rules_D1_hits", []):
        if hit.get("regel") in hits:
            hits[hit["regel"]].append(hit)
    for hit in probe.get("R9_D1_hits", []):
        if hit.get("regel") == "R8b_delle":
            hits["R8b_delle"].append(hit)
    return hits


def stats(field: np.ndarray) -> dict:
    d = field.astype(np.float64)
    a = np.abs(d)
    return {
        "min_m": float(d.min()), "max_m": float(d.max()),
        "max_abs_m": float(a.max()), "mean_abs_m": float(a.mean()),
        "p95_abs_m": float(np.quantile(a, .95)),
        "changed_over_1mm_vertices": int(np.count_nonzero(a > .001)),
        "changed_over_1cm_vertices": int(np.count_nonzero(a > .01)),
        "changed_over_10cm_vertices": int(np.count_nonzero(a > .1)),
        "total_vertices": int(d.size),
    }


def nearest_delta(field: np.ndarray, hit: dict) -> float:
    ix = int(np.clip(round((float(hit["x"]) - D1[0]) * 2), 0, field.shape[1] - 1))
    iz = int(np.clip(round((float(hit["z"]) - D1[1]) * 2), 0, field.shape[0] - 1))
    return float(field[iz, ix])


def report_hits(hits: dict[str, list[dict]], delta: np.ndarray) -> dict:
    out = {}
    for rule, items in hits.items():
        values = [nearest_delta(delta, hit) for hit in items]
        out[rule] = {
            "count": len(items),
            "locations_xz": [[float(hit["x"]), float(hit["z"])] for hit in items],
            "nearest_mesh_delta_m": values,
            "hit_vertices_over_1cm_delta": sum(abs(v) > .01 for v in values),
            "median_abs_delta_m": float(np.median(np.abs(values))) if values else None,
        }
    return out


def color(value: float) -> str:
    # Symmetric diverging scale clipped to +/- 6 m.
    t = float(np.clip(value / 6.0, -1.0, 1.0))
    if t < 0:
        q = 1.0 + t
        rgb = (int(45 + 210 * q), int(75 + 180 * q), 190)
    else:
        q = 1.0 - t
        rgb = (220, int(60 + 175 * q), int(55 + 175 * q))
    return "#%02x%02x%02x" % rgb


def svg_map(fields: dict[int, np.ndarray], probes: dict[int, dict], routes: list, path: Path) -> None:
    cell = 7
    pad, gap, title_h, footer = 44, 28, 30, 54
    wgrid, hgrid = fields[1].shape[1] * cell, fields[1].shape[0] * cell
    panel_w = wgrid + pad * 2
    panel_h = hgrid + title_h + footer
    width, height = panel_w * 2 + gap, panel_h
    body = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            '<rect width="100%" height="100%" fill="#fafafa"/>',
            '<style>text{font-family:Arial,sans-serif;fill:#202124}.small{font-size:11px}.title{font-size:17px;font-weight:bold}</style>']
    palette = {"R5_loch": "#1457d9", "G5_beule_klippe": "#e22b1d",
               "R4_schlucht": "#951ea8", "R8b_delle": "#ff9700"}
    for panel, round_no in enumerate((1, 6)):
        xbase = panel * (panel_w + gap)
        ybase = title_h
        delta = fields[round_no]
        body.append(f'<text class="title" x="{xbase+pad}" y="21">Runde {round_no} − p3d17, D1 (m)</text>')
        body.append(f'<rect x="{xbase+pad}" y="{ybase}" width="{wgrid}" height="{hgrid}" fill="white" stroke="#444"/>')
        for iz in range(delta.shape[0]):
            y = ybase + (delta.shape[0] - 1 - iz) * cell
            for ix in range(delta.shape[1]):
                body.append(f'<rect x="{xbase+pad+ix*cell}" y="{y}" width="{cell+0.2}" height="{cell+0.2}" fill="{color(float(delta[iz,ix]))}"/>')
        # Show the two unchanged V3 route axes.
        for route_index in (2, 11):
            points = []
            for rx, rz in routes[route_index]:
                px = xbase + pad + (float(rx) - D1[0]) * 2 * cell
                py = ybase + (D1[3] - float(rz)) * 2 * cell
                points.append(f"{px:.1f},{py:.1f}")
            body.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="#222" stroke-width="1.4" opacity=".8"/>')
        hits = hit_sets(probes[round_no])
        for rule, items in hits.items():
            for h in items:
                cx = xbase + pad + (float(h["x"]) - D1[0]) * 2 * cell
                cy = ybase + (D1[3] - float(h["z"])) * 2 * cell
                body.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="2.6" fill="{palette[rule]}" stroke="white" stroke-width=".55"/>')
        body.append(f'<text class="small" x="{xbase+pad}" y="{ybase+hgrid+18}">schwarz: Rampe 2/11; rot: G5; blau: R5; violett: R4; orange: R8b</text>')
        s = stats(delta)
        body.append(f'<text class="small" x="{xbase+pad}" y="{ybase+hgrid+36}">MAE {s["mean_abs_m"]:.3f} m · P95 |Δ| {s["p95_abs_m"]:.3f} m · |Δ|&gt;1 cm: {s["changed_over_1cm_vertices"]}</text>')
    body.append('</svg>')
    path.write_text("\n".join(body) + "\n", encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    reference_data = load_relief(REFERENCE)
    reference = d1_heights(reference_data)
    reference_hash = hashlib.sha256(reference.astype("<f4").tobytes()).hexdigest()
    if reference_hash != "26b849f6384993d5029b58dc08f6c657406785e26939f7c172a0d8fafe1ace29":
        raise RuntimeError(f"p3d17 D1 Referenzhash unerwartet: {reference_hash}")
    maps, probes, rounds = {}, {}, {}
    for round_no in (1, 6):
        probe, relief = read_probe(round_no)
        field = d1_heights(relief)
        if field.shape != reference.shape:
            raise RuntimeError("D1-Gittergeometrie weicht zwischen Probe und Referenz ab")
        delta = field.astype(np.float64) - reference.astype(np.float64)
        maps[round_no], probes[round_no] = delta, probe
        hits = hit_sets(probe)
        rounds[str(round_no)] = {
            "official_probe_json": f"codex_jobs/tools/p3d27/results/p3d27_V3_round{round_no:02d}_official_probe.json",
            "probe_relief_sha256": hashlib.sha256(Path(probe["probe_relief"]).read_bytes()).hexdigest(),
            "D1_height_sha256": probe["D1_height_sha256"],
            "delta_to_p3d17_m": delta.tolist(), "delta_stats": stats(delta),
            "checker_locations_relative_to_nearest_changed_mesh_vertex": report_hits(hits, delta),
            "checker_counts": {name: len(items) for name, items in hits.items()},
        }
    baseline_model = {}
    for round_no in (1, 6):
        item = json.loads((ROOT / f"codex_jobs/tools/p3d27/results/p3d27_V3_round{round_no:02d}_model.json").read_text())
        baseline_model[str(round_no)] = {
            "objective_mode": item.get("objective_mode"),
            "family_row_counts": item.get("family_row_counts"),
            "variables": item.get("variables"), "constraints": item.get("constraints"),
            "tie_break_reference_mesh": item.get("tie_break_reference_mesh"),
            "diagnostic_groups_enabled": item.get("diagnostic_groups_enabled"),
        }
    result = {
        "tag": "p3d28", "reference": {
            "file": str(REFERENCE), "D1_xz_bounds": list(D1),
            "spacing_map_units": 0.5, "height_sha256": reference_hash,
        },
        "rounds": rounds,
        "p3d27_model_diagnosis": baseline_model,
        "interpretation": {
            "primary": "The p3d27 checker loop used objective_mode=diagnostic. With family slack already zero, that solve did not select or preserve a p3d17-like surface; the secondary movement tie-break is not run in this mode.",
            "scope": "The full D1 surface grid was variable; variable_bounds bounded covered vertices to +/-4 m relative to the source field, while route grades, axis supports, R8, and R3 families constrained local route/crossing relationships rather than pinning the rest of D1 to p3d17.",
        },
        "map_file": "codex_jobs/tools/p3d28/results/p3d28_d1_delta_comparison.svg",
    }
    (RESULTS / "p3d28_diagnose_d1.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    svg_map(maps, probes, reference_data["rampenwege"],
            RESULTS / "p3d28_d1_delta_comparison.svg")
    for r, item in rounds.items():
        print(f"round {r}: {json.dumps(item['delta_stats'], sort_keys=True)}; hits={item['checker_counts']}")


if __name__ == "__main__":
    main()
