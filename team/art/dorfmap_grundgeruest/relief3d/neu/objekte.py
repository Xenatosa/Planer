"""Attach display objects to the exact prototype terrain they sit on."""
from __future__ import annotations

import base64
from typing import Any

import numpy as np

from .mesh import TILE_BOUNDS
from .wand import _sample_grid


OBJECT_KEYS = ("baeume", "felsen", "findlinge", "steine", "geroell", "felsbloecke")


def bind_objects_to_mesh(data: dict[str, Any], tiles: dict[str, Any]) -> tuple[dict[str, Any], dict[str, list[list[float]]]]:
    """Return sparse base-height updates for D1/G1 without editing source rows."""
    moved_by_kind = {name: 0 for name in OBJECT_KEYS}
    height_updates = {name: [] for name in OBJECT_KEYS}
    max_delta = 0.0
    surfaces: dict[str, tuple[np.ndarray, int]] = {}
    for tile in ("D1", "G1"):
        item = tiles[tile]
        rs = int(item["samples_per_m"])
        x0, z0, x1, z1 = TILE_BOUNDS[tile]
        cols = (x1 - x0) * rs + 1
        rows = (z1 - z0) * rs + 1
        positions = np.frombuffer(
            base64.b64decode(item["vertices_xyz_f32"]), dtype="<f4",
        ).reshape(-1, 3)
        if len(positions) != cols * rows:
            raise ValueError(f"Terrainmesh {tile} hat unerwartete Vertexzahl")
        surfaces[tile] = (positions[:, 1].reshape(rows, cols), rs)

    for name in OBJECT_KEYS:
        objects = data.get(name)
        if not isinstance(objects, list):
            continue
        for index, row in enumerate(objects):
            if not isinstance(row, (list, tuple)) or len(row) < 3:
                continue
            try:
                x, old_y, z = float(row[0]), float(row[1]), float(row[2])
            except (TypeError, ValueError):
                continue
            for tile in ("D1", "G1"):
                x0, z0, x1, z1 = TILE_BOUNDS[tile]
                if not (x0 <= x <= x1 and z0 <= z <= z1):
                    continue
                heights, rs = surfaces[tile]
                new_y = float(_sample_grid(
                    heights, rs, tile,
                    np.asarray([x], dtype=np.float64),
                    np.asarray([z], dtype=np.float64),
                )[0])
                delta = abs(new_y - old_y)
                if delta > 1e-6:
                    new_y = round(new_y, 4)
                    height_updates[name].append([index, new_y])
                    moved_by_kind[name] += 1
                    max_delta = max(max_delta, delta)
                break

    metadata = {
        "tiles": ["D1", "G1"],
        "moved_by_kind": moved_by_kind,
        "moved_total": int(sum(moved_by_kind.values())),
        "max_abs_height_delta_m": round(max_delta, 6),
    }
    return metadata, height_updates
