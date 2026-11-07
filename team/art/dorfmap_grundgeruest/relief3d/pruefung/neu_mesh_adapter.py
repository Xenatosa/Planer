#!/usr/bin/env python3
"""Create an unchanged-schema gate input with the visible prototype mesh embedded.

The historical rule scripts consume relief_daten.json.gz fields G/GB.  This
adapter copies the source payload, substitutes only the D1/G1 tile samples from
neu_mesh_tiles, and leaves D2 and every other source byte untouched.
"""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from neu.mesh import TILE_BOUNDS, build_manifest
from neu.objekte import OBJECT_KEYS


def _read_gzip(path: Path) -> dict:
    return json.loads(gzip.decompress(path.read_bytes()))


def _source_field(data: dict, key: str) -> np.ndarray:
    return np.frombuffer(base64.b64decode(data[key]), dtype=np.float32).copy().reshape(
        int(data["ny"]) * int(data["rs"]) + 1,
        int(data["nx"]) * int(data["rs"]) + 1,
    )


def _mesh_heights(tile: dict, name: str, shape: tuple[int, int]) -> np.ndarray:
    positions = np.frombuffer(base64.b64decode(tile["vertices_xyz_f32"]), dtype="<f4").reshape(-1, 3)
    x0, z0, x1, z1 = TILE_BOUNDS[name]
    rs = int(tile.get("samples_per_m", 2))
    expected = ((z1 - z0) * rs + 1, (x1 - x0) * rs + 1)
    if shape != expected or len(positions) != expected[0] * expected[1]:
        raise ValueError(f"{name}: Meshraster passt nicht: {shape}, {len(positions)} Vertices")
    xx = np.tile(np.arange(x0 * rs, x1 * rs + 1, dtype=np.float32) / rs, expected[0])
    zz = np.repeat(np.arange(z0 * rs, z1 * rs + 1, dtype=np.float32) / rs, expected[1])
    if not np.array_equal(positions[:, 0], xx) or not np.array_equal(positions[:, 2], zz):
        raise ValueError(f"{name}: Meshvertices liegen nicht auf dem erwarteten Raster")
    return positions[:, 1].reshape(expected)


def adapt_data(source: dict, mesh_package: dict) -> dict:
    manifest = mesh_package.get("neu_mesh_tiles")
    if not manifest or manifest.get("format") != "relief-neu-tile-mesh-v2":
        raise ValueError("neu_mesh_tiles im Format relief-neu-tile-mesh-v2 fehlt")
    expected_source_hash = hashlib.sha256(
        json.dumps(source, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    # The source hash in the manifest covers the compressed original file,
    # checked by adapt_files where both input paths and exact bytes are present.
    if (source["nx"], source["ny"], source["rs"]) != (
        mesh_package["nx"], mesh_package["ny"], mesh_package["rs"]
    ):
        raise ValueError("Mesh und Quellenrelief haben verschiedene Abmessungen")

    out = dict(source)
    # Object base-height deltas live inside the opt-in mesh manifest so the
    # original source arrays remain byte-for-byte present in the package.
    # Apply those same derived positions to G11's unchanged-schema input.
    binding = manifest.get("object_binding") or {}
    for name, updates in binding.get("height_updates", {}).items():
        if name not in OBJECT_KEYS or name not in source:
            continue
        objects = [list(row) for row in source[name]]
        for index, height in updates:
            if not (0 <= int(index) < len(objects)):
                raise ValueError(f"Objektbindung {name}[{index}] liegt ausserhalb der Quellliste")
            objects[int(index)][1] = float(height)
        out[name] = objects
    patched: dict[str, np.ndarray] = {}
    mesh_fields: dict[str, np.ndarray] = {}
    extensions = manifest.get("terrain_extensions") or {}
    extension_positions = np.frombuffer(
        base64.b64decode(extensions.get("vertices_xyz_f32", "")), dtype="<f4",
    ).reshape(-1, 3)
    for key in ("G", "GB"):
        field = _source_field(source, key)
        # D2 deliberately remains the original G/GB payload, even when those
        # two legacy fields have independent bytes in the source package.
        for name in ("D1", "G1"):
            item = manifest["tiles"].get(name)
            if item is None:
                raise ValueError(f"Meshpaket ohne Kachel {name}")
            x0, z0, x1, z1 = TILE_BOUNDS[name]
            rs = int(mesh_package["rs"])
            ys = slice(z0 * rs, z1 * rs + 1)
            xs = slice(x0 * rs, x1 * rs + 1)
            heights = _mesh_heights(item, name, field[ys, xs].shape)
            if key == "G" and name == "D1":
                # r9 reads legacy G. Keep D1's shared z=43 row as original G
                # so the adjacent locked D2 slice remains byte-identical.
                heights = heights.copy()
                heights[-1, :] = field[ys, xs][-1, :]
            if key == "GB":
                patched[name] = heights
                mesh_fields[name] = heights
            field[ys, xs] = heights
        if len(extension_positions):
            ix = np.rint(extension_positions[:, 0] * int(source["rs"])).astype(np.int64)
            iz = np.rint(extension_positions[:, 2] * int(source["rs"])).astype(np.int64)
            if np.any((ix < 0) | (iz < 0) | (ix >= field.shape[1]) | (iz >= field.shape[0])):
                raise ValueError("Lokale Terrain-Erweiterung liegt ausserhalb des Reliefgitters")
            in_d2 = (
                (ix >= TILE_BOUNDS["D2"][0] * int(source["rs"]))
                & (ix <= TILE_BOUNDS["D2"][2] * int(source["rs"]))
                & (iz >= TILE_BOUNDS["D2"][1] * int(source["rs"]))
                & (iz <= TILE_BOUNDS["D2"][3] * int(source["rs"]))
            )
            if in_d2.any():
                raise ValueError("Lokale Terrain-Erweiterung greift in D2 ein")
            field[iz, ix] = extension_positions[:, 1]
        out[key] = base64.b64encode(field.astype("<f4", copy=False).tobytes()).decode("ascii")

    # R8/G6 read the legacy fine-band samples after loading G/GB.  The Neu
    # viewer draws the tiled mesh instead, so replace only valid FW heights in
    # D1/G1 with bilinear samples from that same tile surface.  D2 FW entries
    # and every non-prototype tile stay byte-for-byte as in the source.
    fw_source = source["FW"]
    fw = dict(fw_source)
    fs = int(fw["fs"])
    width = int(source["nx"]) * fs + 1
    vertex_ids = np.frombuffer(base64.b64decode(fw["vid"]), dtype=np.uint32)
    fine_heights = np.frombuffer(base64.b64decode(fw["h"]), dtype=np.float32).copy()
    if len(vertex_ids) != len(fine_heights):
        raise ValueError("FW.vid/FW.h haben verschiedene Laengen")
    vx = (vertex_ids % width).astype(np.float64) / fs
    vz = (vertex_ids // width).astype(np.float64) / fs
    for name in ("D1", "G1"):
        x0, z0, x1, z1 = TILE_BOUNDS[name]
        mask = (vx >= x0) & (vx <= x1) & (vz >= z0) & (vz <= z1)
        if name == "D1":
            # D1's south edge is also D2's north edge. Keep the fine-band
            # samples on that shared D2 border exactly as supplied.
            mask &= vz < z1 - 1e-6
        if not mask.any():
            continue
        tile = mesh_fields[name]
        tile_rs = int(manifest["tiles"][name].get("samples_per_m", 2))
        u = np.clip((vx[mask] - x0) * tile_rs, 0, tile.shape[1] - 1.001)
        v = np.clip((vz[mask] - z0) * tile_rs, 0, tile.shape[0] - 1.001)
        ix, iz = np.floor(u).astype(np.int64), np.floor(v).astype(np.int64)
        du, dv = u - ix, v - iz
        fine_heights[mask] = (
            tile[iz, ix] * (1.0 - du) * (1.0 - dv)
            + tile[iz, ix + 1] * du * (1.0 - dv)
            + tile[iz + 1, ix] * (1.0 - du) * dv
            + tile[iz + 1, ix + 1] * du * dv
        ).astype(np.float32)
    extension_ids = np.frombuffer(
        base64.b64decode(extensions.get("fine_vid_u32", "")), dtype="<u4",
    )
    extension_heights = np.frombuffer(
        base64.b64decode(extensions.get("fine_h_f32", "")), dtype="<f4",
    )
    if len(extension_ids) != len(extension_heights):
        raise ValueError("Lokale Terrain-Erweiterung hat ungleiche Feinband-Arrays")
    if len(extension_ids):
        extension_positions = np.searchsorted(vertex_ids, extension_ids)
        if np.any(extension_positions >= len(vertex_ids)) or not np.array_equal(
            vertex_ids[extension_positions], extension_ids,
        ):
            raise ValueError("Lokale Terrain-Erweiterung verweist auf fehlende Feinband-IDs")
        ext_x = (extension_ids % width).astype(np.float64) / fs
        ext_z = (extension_ids // width).astype(np.float64) / fs
        in_d2 = (
            (ext_x >= TILE_BOUNDS["D2"][0]) & (ext_x <= TILE_BOUNDS["D2"][2])
            & (ext_z >= TILE_BOUNDS["D2"][1]) & (ext_z <= TILE_BOUNDS["D2"][3])
        )
        if in_d2.any():
            raise ValueError("Feinband-Erweiterung greift in D2 ein")
        fine_heights[extension_positions] = extension_heights
    fw["h"] = base64.b64encode(fine_heights.astype("<f4", copy=False).tobytes()).decode("ascii")
    out["FW"] = fw

    # The generated package's D2 mesh must still equal the source's visible GB
    # vertices byte for byte; this is checked here before gates receive it.
    source_visible = _source_field(source, "GB")
    d2_item = manifest["tiles"]["D2"]
    d2 = _mesh_heights(d2_item, "D2", (
        (TILE_BOUNDS["D2"][3] - TILE_BOUNDS["D2"][1]) * int(source["rs"]) + 1,
        (TILE_BOUNDS["D2"][2] - TILE_BOUNDS["D2"][0]) * int(source["rs"]) + 1,
    ))
    x0, z0, x1, z1 = TILE_BOUNDS["D2"]
    rs = int(source["rs"])
    d2_source = source_visible[z0 * rs : z1 * rs + 1, x0 * rs : x1 * rs + 1]
    if d2.tobytes() != d2_source.tobytes():
        raise ValueError("D2 Mesh ist nicht bytegleich mit der sichtbaren GB-Quelle")
    out["neu_mesh_gate"] = {
        "format": "legacy-gates-over-neu-mesh-v1",
        "source_relief_sha256_json": expected_source_hash,
        "terrain_variant": manifest.get("terrain_variant"),
        "tiles_patched": ["D1", "G1"],
        "fw_samples_patched": int(np.count_nonzero(fine_heights != np.frombuffer(
            base64.b64decode(fw_source["h"]), dtype=np.float32
        ))),
        "terrain_extension_vertices": int(len(extension_positions)),
        "terrain_extension_fine_vertices": int(len(extension_ids)),
        "d2_gb_mesh_bytegleich": True,
        "height_sha256": {
            name: hashlib.sha256(value.astype("<f4", copy=False).tobytes()).hexdigest()
            for name, value in sorted(patched.items())
        },
    }
    return out


def _build_variant_package(source_path: Path, variant: str) -> dict:
    base = _read_gzip(source_path)
    manifest = build_manifest(
        source_path,
        ROOT / "neu" / "zellen_relief.csv",
        ROOT / "neu" / "vektor.json",
        ROOT / "neu" / "felder.npz",
        variant=variant,
    )
    package = dict(base)
    package["neu_mesh_tiles"] = manifest
    return package


def adapt_files(source_path: Path, mesh_path: Path, output_path: Path) -> dict:
    source_raw = source_path.read_bytes()
    mesh_raw = mesh_path.read_bytes()
    source = json.loads(gzip.decompress(source_raw))
    package = json.loads(gzip.decompress(mesh_raw))
    manifest = package.get("neu_mesh_tiles") or {}
    actual = hashlib.sha256(source_raw).hexdigest()
    if manifest.get("source_relief_sha256") != actual:
        raise ValueError("Meshpaket stammt nicht bytegenau aus der angegebenen Reliefquelle")
    adapted = adapt_data(source, package)
    raw = json.dumps(adapted, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
    return adapted["neu_mesh_gate"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "relief_daten.json.gz")
    parser.add_argument("--mesh", type=Path, default=ROOT / "neu" / "relief_neu.json.gz")
    parser.add_argument("--variant", choices=("0", "1", "2"))
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.variant is None:
        metadata = adapt_files(args.source, args.mesh, args.out)
    else:
        package = _build_variant_package(args.source, args.variant)
        # Reuse the same strict byte and coordinate checks as the built artifact.
        source = _read_gzip(args.source)
        adapted = adapt_data(source, package)
        raw = json.dumps(adapted, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
        metadata = adapted["neu_mesh_gate"]
    print(json.dumps({"output": str(args.out), **metadata}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
