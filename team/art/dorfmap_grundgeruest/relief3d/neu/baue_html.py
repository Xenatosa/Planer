#!/usr/bin/env python3
"""Build an offline SVG inspection view from the prototype JSON."""
from __future__ import annotations

import base64
import html
import json
import os
import struct
from pathlib import Path


PALETTE = {
    "ug_schnee": "#d7e0e6",
    "ug_klippe_wand": "#68615d",
    "ug_klippe_kante": "#82766c",
    "ug_wald": "#718d65",
    "ug_wasser_eis": "#8daed0",
    "ug_fels": "#8a8177",
    "ug_schatten": "#697078",
    "ug_boden": "#8e9b67",
    "ug_sand": "#c6aa70",
}
DEFAULT = Path("/tmp/relief_neu_pregeln")


def _rgb(raw: bytes, index: int) -> str:
    i = index * 3
    return f"#{raw[i]:02x}{raw[i + 1]:02x}{raw[i + 2]:02x}"


def _xy(px: float, pz: float, h: float, cx: float, cy: float) -> str:
    # Fixed isometric projection for comparison only; stored heights stay in metres.
    x = cx + (px - pz) * 3.5
    y = cy + (px + pz) * 1.6 - h * 2.0
    return f"{x:.2f},{y:.2f}"


def _tile_polygons(tile: dict, center_x: float, center_y: float) -> tuple[str, float, float]:
    name = tile["tile"]
    x0, z0, x1, z1 = tile["cell_bounds_xyxy_inclusive_exclusive"]
    cells = tile["cells"]
    cell_map = {(int(c["cx"]), int(c["cy"])): c for c in cells}
    spacing = float(tile["grid_spacing_m"])
    if tile["mode"] == "locked_legacy_reference":
        field = tile["display_fields"]["GB"]
        w, h = int(field["width"]), int(field["height"])
        heights = struct.unpack(f"<{w * h}f", base64.b64decode(field["bytes_b64"]))
        vc_field = tile["display_fields"]["VC"]
        vc = base64.b64decode(vc_field["bytes_b64"])
        rs = 2
        cell_step = rs
    else:
        w, h = int(tile["height_width"]), int(tile["height_height"])
        heights = struct.unpack(f"<{w * h}f", base64.b64decode(tile["height_f32_le_b64"]))
        vc = b""
        rs = 1
        cell_step = 1

    pieces = []
    width_m, depth_m = x1 - x0, z1 - z0
    # Draw from back to front so nearer cells cover farther cell edges.
    for diag in range((width_m - 1) + (depth_m - 1) + 1):
        for lz in range(depth_m):
            lx = diag - lz
            if not (0 <= lx < width_m):
                continue
            wx, wz = x0 + lx, z0 + lz
            cell = cell_map[(wx, wz)]
            gx, gz = lx * cell_step, lz * cell_step
            corners = ((gx, gz), (gx + cell_step, gz), (gx + cell_step, gz + cell_step), (gx, gz + cell_step))
            coords, color_indices = [], []
            for vx, vz in corners:
                idx = vz * w + vx
                coords.append(_xy(vx * spacing, vz * spacing, heights[idx], center_x, center_y))
                color_indices.append(idx)
            if vc:
                sums = [sum(vc[i * 3 + ch] for i in color_indices) / len(color_indices) for ch in range(3)]
                fill = "#" + "".join(f"{round(v):02x}" for v in sums)
            else:
                fill = PALETTE.get(cell.get("skin_slot", ""), "#8a8a83")
            points = " ".join(coords)
            title = html.escape(f"{name} cx={wx} cy={wz} {cell.get('untergrund', '')}")
            pieces.append(f'<polygon points="{points}" fill="{fill}"><title>{title}</title></polygon>')
    return "\n".join(pieces), width_m, depth_m


def render(data: dict) -> str:
    tiles = {t["tile"]: t for t in data["tiles"]}
    positions = {"D1": (250.0, 245.0), "D2": (650.0, 245.0), "G1": (1050.0, 245.0)}
    bodies = []
    for name in ("D1", "D2", "G1"):
        svg, _, _ = _tile_polygons(tiles[name], *positions[name])
        x, y = positions[name]
        tile = tiles[name]
        bodies.append(f'<g aria-label="Kachel {name}">{svg}<text x="{x}" y="35" class="label">{name} · {tile["mode"]}</text></g>')
    hashes = tiles["D2"]["display_fields"]
    return f'''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Relief-Neubau-Prototyp (pregeln)</title>
<style>body{{margin:0;background:#182128;color:#e7edf0;font:14px system-ui,sans-serif}}main{{padding:18px}}h1{{font-size:20px;margin:0 0 8px}}p{{max-width:1100px;line-height:1.5}}svg{{background:#dfe6e9;width:min(100%,1400px);height:auto;border:1px solid #59656c}}.label{{font:bold 16px sans-serif;fill:#182128;text-anchor:middle}}</style></head>
<body><main><h1>Relief-Neubau-Prototyp · D1, D2, G1</h1>
<p>D1 und G1 zeigen ein neues 1-m-Quellzellen-Höhenfeld. D2 bleibt ein schreibgeschützter Referenzblock. Die Vorschau ist eine isometrische Rasteransicht; sie ersetzt weder Texturen noch den bestehenden Viewer. Für D2 sind die seriellen GB-, VC-, WV- und WEGA-Feldbytes eingebettet.</p>
<p>D2-GB SHA-256: <code>{hashes['GB']['sha256']}</code> · D2-VC SHA-256: <code>{hashes['VC']['sha256']}</code> · LOD1-Schätzung: {data['lod1_triangle_estimate']:,} Dreiecke</p>
<p><a href="../index.html">Bestehenden Relief-Viewer öffnen</a></p>
<svg viewBox="0 0 1300 720" role="img" aria-label="Isometrische Vorschau der drei Prototypkacheln">{''.join(bodies)}</svg>
</main></body></html>'''


def build(data_path: Path, output_path: Path) -> str:
    data = json.loads(data_path.read_text(encoding="utf-8"))
    result = render(data)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(result, encoding="utf-8")
    return result


def main() -> int:
    out_dir = Path(os.environ.get("RELIEF_NEU_DIR", str(DEFAULT)))
    data_path = Path(os.environ.get("RELIEF_NEU_DATA", str(out_dir / "prototyp.json")))
    output_path = out_dir / "index.html"
    result = build(data_path, output_path)
    print(json.dumps({"output": str(output_path), "bytes": len(result.encode("utf-8"))}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
