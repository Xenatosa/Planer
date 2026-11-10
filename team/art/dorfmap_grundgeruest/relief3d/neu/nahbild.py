"""Render six deterministic close-up cameras per selected tile, clay and texture."""
from __future__ import annotations

import argparse
import base64
import gzip
import json
import math
import os
import shutil
import subprocess
import time
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RENDER = ROOT / "pruefung" / "o18" / "render_t119u.js"
ANALYZER = Path(__file__).with_name("nahbild.js")
TILES = ("D1", "G1", "D2")
CAMERAS = ("draufsicht", "streiflicht_west", "streiflicht_ost", "kreuzung", "wegende", "wandfuss")


def _array(d: dict, key: str, dtype: np.dtype, shape: tuple[int, ...]) -> np.ndarray:
    return np.frombuffer(base64.b64decode(d[key]), dtype=dtype).reshape(shape)


def _column(d: dict, key: str) -> np.ndarray:
    col = d["spalten"][key]
    dtype = {"uint8": np.uint8, "uint16": np.uint16, "uint32": np.uint32}[col["t"]]
    idx = np.frombuffer(base64.b64decode(col["i"]), dtype=dtype).astype(np.int64)
    return np.asarray(col["w"], dtype=object)[idx]


def _tile(name: str, nx: int, ny: int) -> tuple[int, int, int, int]:
    ci = ord(name[0]) - ord("A")
    ri = int(name[1:]) - 1
    return ci * 42, min((ci + 1) * 42, nx), ri * 43, min((ri + 1) * 43, ny)


def _height(g: np.ndarray, rs: int, x: float, z: float) -> float:
    gx, gy = g.shape[1], g.shape[0]
    fx, fz = np.clip(x * rs, 0, gx - 1.001), np.clip(z * rs, 0, gy - 1.001)
    ix, iz = int(fx), int(fz)
    u, v = fx - ix, fz - iz
    return float((g[iz, ix] * (1 - u) + g[iz, ix + 1] * u) * (1 - v) + (g[iz + 1, ix] * (1 - u) + g[iz + 1, ix + 1] * u) * v)


def _road_and_endpoints(d: dict, bounds: tuple[int, int, int, int]) -> tuple[list[tuple[float, float]], list[tuple[float, float]]]:
    x0, x1, z0, z1 = bounds
    roads = np.zeros((z1 - z0, x1 - x0), dtype=bool)
    for x, z in d.get("wege", []):
        if x0 <= x < x1 and z0 <= z < z1:
            roads[int(z) - z0, int(x) - x0] = True
    if roads.any():
        degree = np.zeros_like(roads, dtype=np.int16)
        degree[1:] += roads[:-1]
        degree[:-1] += roads[1:]
        degree[:, 1:] += roads[:, :-1]
        degree[:, :-1] += roads[:, 1:]
        crossings = [(x0 + x + 0.5, z0 + z + 0.5) for z, x in zip(*np.nonzero(roads & (degree >= 3)))]
        ends = [(x0 + x + 0.5, z0 + z + 0.5) for z, x in zip(*np.nonzero(roads & (degree == 1)))]
    else:
        crossings, ends = [], []
    ramps = []
    for path in d.get("rampenwege", []):
        if len(path) < 2:
            continue
        for p in (path[0], path[-1]):
            if x0 <= p[0] <= x1 and z0 <= p[1] <= z1:
                ramps.append((float(p[0]), float(p[1])))
    return crossings, ramps or ends


def _pick(points: list[tuple[float, float]], center: tuple[float, float], fallback: tuple[float, float]) -> tuple[float, float]:
    if not points:
        return fallback
    # Stable central choice avoids depending on source record ordering.
    return min(points, key=lambda p: (round(math.hypot(p[0] - center[0], p[1] - center[1]), 5), p[1], p[0]))


def _camera_pos(g: np.ndarray, rs: int, tile_bounds: tuple[int, int, int, int],
                anchor: tuple[float, float], dx: float, dz: float, clearance: float) -> list[float]:
    x0, x1, z0, z1 = tile_bounds
    x = float(np.clip(anchor[0] + dx, x0 + 1.0, x1 - 1.0))
    z = float(np.clip(anchor[1] + dz, z0 + 1.0, z1 - 1.0))
    # Place the camera above the terrain at its own position, since a nearby
    # ridge can otherwise put a camera below the local surface.
    y = _height(g, rs, x, z) + clearance
    return [x, y, z]


def camera_list(d: dict, tiles: tuple[str, ...] = TILES) -> list[dict]:
    nx, ny, rs = d["nx"], d["ny"], d["rs"]
    g = _array(d, "GB", np.float32, (ny * rs + 1, nx * rs + 1))
    klippe = _column(d, "klippe").reshape(ny, nx)
    wand_name = _column(d, "wand_name").reshape(ny, nx)
    untergrund = _column(d, "untergrund").reshape(ny, nx)
    cameras: list[dict] = []
    for tile in tiles:
        bounds = _tile(tile, nx, ny)
        x0, x1, z0, z1 = bounds
        cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
        fallback = (cx, cz)
        hy = _height(g, rs, cx, cz)
        crossings, ends = _road_and_endpoints(d, bounds)
        crossing = _pick(crossings, (cx, cz), fallback)
        endpoint = _pick(ends, (cx, cz), fallback)

        # Use marked wall-foot cells first; when a tile has no explicit foot, use its
        # nearest wall cell, still derived only from the source cell columns.
        foot = np.argwhere((klippe[z0:z1, x0:x1] == "WAND_FUSS") | np.char.startswith(untergrund[z0:z1, x0:x1].astype(str), "KLIPPE"))
        if not len(foot):
            # Keep even the fallback local to this tile. A global wall pick can
            # accidentally make D2's wall-foot camera point into D1.
            local_walls = wand_name[z0:z1, x0:x1]
            foot = np.argwhere(np.isin(local_walls, ("Nord", "Krater", "Ostgrat", "Suedgrat")))
        foot_points = [(float(x0 + x + 0.5), float(z0 + z + 0.5)) for z, x in foot]
        wall = _pick(foot_points, (cx, cz), fallback)

        cameras.extend([
            {"n": f"{tile}_draufsicht", "pos": [cx, hy + 55.0, cz], "ziel": [cx, hy, cz], "az": 315, "el": 45, "st": 90},
            {"n": f"{tile}_streiflicht_west", "pos": _camera_pos(g, rs, bounds, (cx, cz), -14.0, 0.0, 15.0), "ziel": [cx, hy + 1.0, cz], "az": 45, "el": 12, "st": 100},
            {"n": f"{tile}_streiflicht_ost", "pos": _camera_pos(g, rs, bounds, (cx, cz), 14.0, 0.0, 15.0), "ziel": [cx, hy + 1.0, cz], "az": 225, "el": 12, "st": 100},
            {"n": f"{tile}_kreuzung", "pos": _camera_pos(g, rs, bounds, crossing, -8.0, -7.0, 18.0), "ziel": [crossing[0], _height(g, rs, *crossing), crossing[1]], "az": 135, "el": 18, "st": 90},
            {"n": f"{tile}_wegende", "pos": _camera_pos(g, rs, bounds, endpoint, 8.0, 7.0, 18.0), "ziel": [endpoint[0], _height(g, rs, *endpoint), endpoint[1]], "az": 315, "el": 18, "st": 90},
            {"n": f"{tile}_wandfuss", "pos": _camera_pos(g, rs, bounds, wall, -8.0, -6.0, 18.0), "ziel": [wall[0], _height(g, rs, *wall), wall[1]], "az": 135, "el": 15, "st": 95},
        ])
    return cameras


def render(html: Path, data: Path, output: Path, tiles: tuple[str, ...], node_path: Path) -> dict:
    with gzip.open(data, "rt", encoding="utf-8") as f:
        d = json.load(f)
    cameras = camera_list(d, tiles)
    output.mkdir(parents=True, exist_ok=True)
    cameras_path = output / "kameras.json"
    cameras_path.write_text(json.dumps(cameras, separators=(",", ":"), ensure_ascii=False) + "\n", encoding="utf-8")
    env = {**os.environ, "NODE_PATH": str(node_path)}
    xvfb = os.environ.get("NAHBILD_XVFB", "1") == "1" and shutil.which("xvfb-run") is not None
    if xvfb:
        env["HEADLESS"] = "0"
    started = time.monotonic()
    # Shadow-map updates are stateful between camera changes; disabling cast
    # shadows leaves directional surface shading intact and makes captures stable.
    for mode, query in (("clay", "?clay=1&manual=1&nosh=1"), ("textur", "?manual=1&nosh=1")):
        outdir = output / mode
        outdir.mkdir(parents=True, exist_ok=True)
        cmd = ["node", str(RENDER), str(html.resolve()), str(outdir.resolve()), str(cameras_path.resolve()), query, "1000", "700"]
        if xvfb:
            cmd = ["xvfb-run", "-a", *cmd]
        subprocess.run(cmd, cwd=ROOT, env=env, check=True)
    elapsed = round(time.monotonic() - started, 3)
    metrics_path = output / "nahbild_werte.json"
    subprocess.run(
        ["node", str(ANALYZER), str(output.resolve()), str(metrics_path.resolve())],
        cwd=ROOT, env=env, check=True,
    )
    return {"kacheln": list(tiles), "kameras_je_kachel": len(CAMERAS), "bilder": len(cameras) * 2, "laufzeit_s": elapsed, "werte": str(metrics_path)}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--html", type=Path, default=ROOT / "index.html")
    ap.add_argument("--data", type=Path, default=ROOT / "relief_daten.json.gz")
    ap.add_argument("--out", type=Path, default=ROOT / "pruefung" / "nahbild_pnahbild")
    ap.add_argument("--tiles", default=",".join(TILES))
    ap.add_argument("--node-path", type=Path, default=Path("/tmp/w3/node_modules"))
    args = ap.parse_args()
    tiles = tuple(t.strip().upper() for t in args.tiles.split(",") if t.strip())
    if not tiles or any(len(t) < 2 for t in tiles):
        raise ValueError("--tiles erwartet Feldnamen wie D1,G1,D2")
    print(json.dumps(render(args.html, args.data, args.out, tiles, args.node_path), sort_keys=True))


if __name__ == "__main__":
    main()
