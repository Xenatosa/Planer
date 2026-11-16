#!/usr/bin/env python3
"""P10: Gelaende-Meshes aller 56 Kacheln (A-H x 1-7) aus relief_daten.json.gz.

Verfahren = das von index.html (neu/pipeline.py -> neu/mesh.py, Viewer neu/viewer.js):
  * D1, G1, D2: unveraendert ueber neu.mesh.build_manifest() (Variante 2, Wegende 1,
    Kreuzung 24 = Standard), daraus Kachelmesh mit neu.mesh.tile_mesh().
  * Alle uebrigen 53 Kacheln: dasselbe neu.mesh.tile_mesh() auf dem sichtbaren
    GB-Hoehenfeld (Verfahren von D2, "locked_visible_GB_bytes"). Die 293
    terrain_extensions-Vertices des Pakets (Rampenauslauf ausserhalb D1/G1, alle in C1)
    werden wie in pruefung/neu_mesh_adapter.py auf GB gelegt (abschaltbar mit
    --ohne-erweiterung).
  * Waende D1/G1: neu.wand.build_wall_manifest() wie in neu/pipeline.py (eigene Ebene
    'waende', vom Lochscan nicht erfasst - wie in index.html).
Schreibt NUR in das Ausgabeverzeichnis (Standard /tmp/p10). Keine Repo-Datei wird geaendert.

Aufruf (im Ordner relief3d):
  python3 pruefung/alle_kacheln/baue_alle_kacheln.py [--out /tmp/p10] [--ohne-erweiterung] [--ohne-html]
Ergebnis: <out>/alle_kacheln.json.gz (Meshpaket), <out>/alle_kacheln.html (Viewer, alle 56 Kacheln),
          <out>/alle_kacheln_build.json (Kennzahlen, Hashes je Kachel, Nahtpruefung).
  --testloch C3 baut zusaetzlich eine Positivkontrolle (1 Dreieck fehlt) fuer den Lochscan.
"""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

HIER = Path(__file__).resolve().parent
R = HIER.parents[1]  # .../relief3d
sys.path.insert(0, str(R))

from neu import mesh as M  # noqa: E402
from neu.wand import build_wall_manifest  # noqa: E402

BUCHST = "ABCDEFGH"


def kachel_grenzen(nx: int, ny: int) -> dict[str, tuple[int, int, int, int]]:
    """Wie TILE_BOUNDS/pruefe_regeln.feld: Spalte 42 Zellen, Zeile 43 Zellen."""
    out = {}
    for iz in range(7):
        for ix in range(8):
            x0, z0 = ix * 42, iz * 43
            out[f"{BUCHST[ix]}{iz + 1}"] = (x0, z0, min(nx, x0 + 42), min(ny, z0 + 43))
    return out


def _b64(a: np.ndarray) -> str:
    return base64.b64encode(a.tobytes(order="C")).decode("ascii")


def baue(out_dir: Path, mit_erweiterung: bool = True, testloch: str | None = None, name: str = "alle_kacheln") -> dict:
    t0 = time.time()
    relief = R / "relief_daten.json.gz"
    source = M.load_relief(relief)
    rs, nx, ny = int(source.data["rs"]), int(source.data["nx"]), int(source.data["ny"])
    # 1) Prototyp-Kacheln exakt wie neu/pipeline.py (Standardvarianten aus der Umgebung).
    manifest = M.build_manifest(relief, R / "neu" / "zellen_relief.csv",
                                R / "neu" / "vektor.json", R / "neu" / "felder.npz")
    waende = build_wall_manifest(R / "neu" / "vektor.json", terrain_tiles=manifest["tiles"])
    t_proto = time.time() - t0

    # 2) Hoehenfeld fuer alle anderen Kacheln = GB (+ terrain_extensions wie Gate-Adapter).
    feld = source.heights.copy()
    ext = manifest["terrain_extensions"]
    ext_n = 0
    if mit_erweiterung and ext.get("vertices"):
        P = np.frombuffer(base64.b64decode(ext["vertices_xyz_f32"]), dtype="<f4").reshape(-1, 3)
        ix = np.rint(P[:, 0] * rs).astype(np.int64)
        iz = np.rint(P[:, 2] * rs).astype(np.int64)
        feld[iz, ix] = P[:, 1]
        ext_n = len(P)

    grenzen = kachel_grenzen(nx, ny)
    # Kachelgrenzen der Prototypen muessen mit der Rasterformel uebereinstimmen.
    for t, b in M.TILE_BOUNDS.items():
        if tuple(b) != grenzen[t]:
            raise RuntimeError(f"TILE_BOUNDS {t}={b} weicht von Rasterformel {grenzen[t]} ab")
    proto = set(manifest["tiles"])
    # neu.mesh.tile_mesh() kennt nur TILE_BOUNDS; im eigenen Prozess um die
    # restlichen Kacheln ergaenzen (keine Dateiaenderung), damit dieselbe Funktion
    # (gleiche Diagonale, Dreiecksreihenfolge, Vertexreihenfolge) baut.
    for t, b in grenzen.items():
        M.TILE_BOUNDS.setdefault(t, b)

    tiles: dict[str, dict] = {}
    kontrolle = {}
    for t, (x0, z0, x1, z1) in grenzen.items():
        if t in proto:
            item = dict(manifest["tiles"][t])
            # Kontrolle: Proto-Kachel muss mit tile_mesh() auf ihrem Hoehenfeld identisch sein.
            P = np.frombuffer(base64.b64decode(item["vertices_xyz_f32"]), dtype="<f4").reshape(-1, 3)
            I = np.frombuffer(base64.b64decode(item["indices_u32"]), dtype="<u4")
            slab = P[:, 1].reshape((z1 - z0) * rs + 1, (x1 - x0) * rs + 1)
            P2, I2 = M.tile_mesh(source, t, slab)
            kontrolle[t] = bool(np.array_equal(P, P2) and np.array_equal(I, I2))
            item["verfahren"] = "neu.mesh.build_manifest (Prototyp)"
        else:
            slab = feld[z0 * rs: z1 * rs + 1, x0 * rs: x1 * rs + 1]
            P, I = M.tile_mesh(source, t, slab)
            item = {
                "bounds": [x0, z0, x1, z1], "samples_per_m": rs, "sampling_m": 1.0 / rs,
                "surface_mode": "locked_visible_GB_bytes" + ("+terrain_extensions" if
                                                                   (slab != source.heights[z0 * rs: z1 * rs + 1, x0 * rs: x1 * rs + 1]).any() else ""),
                "vertices_xyz_f32": _b64(P), "indices_u32": _b64(I),
                "vertices": int(len(P)), "triangles": int(len(I) // 3),
                "height_sha256": hashlib.sha256(P[:, 1].tobytes()).hexdigest(),
                "mesh_sha256": hashlib.sha256(P.tobytes() + I.tobytes()).hexdigest(),
                "verfahren": "neu.mesh.tile_mesh auf GB (wie D2)",
            }
        cols, rows = (x1 - x0) * rs, (z1 - z0) * rs
        item["closed_triangles"] = item["triangles"] * 2 + 2 * 2 * (cols + rows)
        tiles[t] = item
    if not all(kontrolle.values()):
        raise RuntimeError(f"Prototyp-Kachel nicht mit tile_mesh reproduzierbar: {kontrolle}")

    # 3) Nahtpruefung: gemeinsame Randvertices benachbarter Kacheln (Hoehe gleich?).
    def pos(t):
        it = tiles[t]
        return np.frombuffer(base64.b64decode(it["vertices_xyz_f32"]), dtype="<f4").reshape(-1, 3)
    naht = {"paare": 0, "max_abs_m": 0.0, "abweichend": []}
    for t, (x0, z0, x1, z1) in grenzen.items():
        ix, iz = BUCHST.index(t[0]), int(t[1]) - 1
        W = (x1 - x0) * rs + 1
        H = (z1 - z0) * rs + 1
        A = pos(t).reshape(H, W, 3)
        for nb, sel_a, sel_b in (
            (f"{BUCHST[ix + 1]}{iz + 1}" if ix < 7 else None, lambda a: a[:, -1], lambda b: b[:, 0]),
            (f"{BUCHST[ix]}{iz + 2}" if iz < 6 else None, lambda a: a[-1, :], lambda b: b[0, :]),
        ):
            if nb is None:
                continue
            bx0, bz0, bx1, bz1 = grenzen[nb]
            B = pos(nb).reshape((bz1 - bz0) * rs + 1, (bx1 - bx0) * rs + 1, 3)
            ea, eb = sel_a(A), sel_b(B)
            if not np.array_equal(ea[:, [0, 2]], eb[:, [0, 2]]):
                raise RuntimeError(f"Naht {t}/{nb}: x/z-Raster passt nicht")
            d = float(np.max(np.abs(ea[:, 1].astype(np.float64) - eb[:, 1])))
            naht["paare"] += 1
            naht["max_abs_m"] = max(naht["max_abs_m"], d)
            if d > 0:
                naht["abweichend"].append({"kacheln": [t, nb], "max_abs_m": round(d, 6)})

    if testloch:
        # Positivkontrolle fuer den Lochscan: ein Dreieck in der Kachelmitte entfernen.
        it = tiles[testloch]
        I = np.frombuffer(base64.b64decode(it["indices_u32"]), dtype="<u4").copy()
        bx0, bz0, bx1, bz1 = it["bounds"]
        cols, rows = (bx1 - bx0) * rs, (bz1 - bz0) * rs
        mitte = ((rows // 2) * cols + cols // 2) * 6  # erstes Dreieck der mittleren Rasterzelle
        entfernt = I[mitte:mitte + 3].tolist()
        I = np.delete(I, np.s_[mitte:mitte + 3])
        it["indices_u32"] = _b64(I)
        it["triangles"] = int(len(I) // 3)
        it["closed_triangles"] -= 1
        it["testloch_entfernt"] = entfernt
        it["surface_mode"] += "+TESTLOCH"

    paket = {
        "nx": nx, "ny": ny, "rs": rs, "GB": source.data.get("GB") or source.data["G"],
        "VC": source.data["VC"], "start": source.data.get("start"),
        "alle_kacheln": {
            "format": "p10-alle-kacheln-v1",
            "quelle": "relief_daten.json.gz",
            "source_relief_sha256": source.source_file_sha256,
            "terrain_variant": manifest["terrain_variant"],
            "terrain_extensions_angewendet": ext_n,
            "reihenfolge": list(grenzen),
            "tiles": tiles,
            "waende": waende,
        },
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    roh = json.dumps(paket, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    gz = gzip.compress(roh, compresslevel=9, mtime=0)
    (out_dir / f"{name}.json.gz").write_bytes(gz)
    info = {
        "name": name, "testloch": testloch,
        "quelle": "relief_daten.json.gz", "source_relief_sha256": source.source_file_sha256,
        "kacheln": len(tiles), "prototyp_kacheln": sorted(proto),
        "prototyp_mit_tile_mesh_identisch": kontrolle,
        "terrain_extensions_angewendet": ext_n,
        "flaechen_dreiecke": sum(t["triangles"] for t in tiles.values()),
        "geschlossen_dreiecke": sum(t["closed_triangles"] for t in tiles.values()),
        "wand_dreiecke": sum(t["triangles"] for t in waende["tiles"].values()),
        "naht": naht,
        "paket_bytes": len(gz),
        "kacheln_info": {t: {k: v for k, v in it.items() if k not in ("vertices_xyz_f32", "indices_u32")}
                         for t, it in tiles.items()},
        "dauer_s": {"prototyp": round(t_proto, 2), "gesamt": round(time.time() - t0, 2)},
    }
    return info


def baue_html(out_dir: Path, name: str = "alle_kacheln") -> int:
    node_dir = Path(os.environ.get("NODE_DIR", "/tmp/w3"))
    env = {**os.environ, "NODE_PATH": str(node_dir / "node_modules")}
    with tempfile.TemporaryDirectory(prefix="p10_bundle_") as tmp:
        bundle = Path(tmp) / "b.js"
        # Bundle in ein Temp-Verzeichnis (NICHT /tmp/w3/bundle_r.js).
        subprocess.run([str(node_dir / "node_modules" / ".bin" / "esbuild"), str(HIER / "einstieg.js"),
                        "--bundle", "--minify", "--format=iife", f"--outfile={bundle}"],
                       cwd=R, env=env, check=True)
        js = bundle.read_text(encoding="utf-8")
    data = base64.b64encode((out_dir / f"{name}.json.gz").read_bytes()).decode("ascii")
    vorlage = (HIER / "vorlage.html").read_text(encoding="utf-8")
    doc = vorlage.replace("/*__DATEN__*/", f'window.P10_GZ="{data}";').replace("/*__JS__*/", js)
    doc = "\n".join(line.rstrip() for line in doc.splitlines()) + "\n"
    (out_dir / f"{name}.html").write_text(doc, encoding="utf-8")
    return len(doc.encode("utf-8"))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=os.environ.get("P10_OUT", "/tmp/p10"))
    ap.add_argument("--ohne-erweiterung", action="store_true")
    ap.add_argument("--ohne-html", action="store_true")
    ap.add_argument("--testloch", metavar="KACHEL", help="Positivkontrolle: entfernt 1 Dreieck in KACHEL, schreibt alle_kacheln_testloch_<KACHEL>.*")
    a = ap.parse_args()
    out = Path(a.out)
    if out.resolve() == Path("/tmp/w3") or str(out.resolve()).startswith("/tmp/w3/"):
        raise SystemExit("Ausgabe nach /tmp/w3 ist gesperrt (laufende Jobs).")
    t = time.time()
    name = f"alle_kacheln_testloch_{a.testloch}" if a.testloch else "alle_kacheln"
    info = baue(out, not a.ohne_erweiterung, a.testloch, name)
    if not a.ohne_html:
        th = time.time()
        info["html_bytes"] = baue_html(out, name)
        info["dauer_s"]["html"] = round(time.time() - th, 2)
    info["dauer_s"]["gesamt"] = round(time.time() - t, 2)
    (out / f"{name}_build.json").write_text(json.dumps(info, ensure_ascii=False, indent=1, sort_keys=True) + "\n")
    kurz = {k: info[k] for k in ("kacheln", "prototyp_mit_tile_mesh_identisch", "terrain_extensions_angewendet",
                                  "flaechen_dreiecke", "geschlossen_dreiecke", "naht", "paket_bytes", "dauer_s")}
    kurz["html_bytes"] = info.get("html_bytes")
    print(json.dumps(kurz, ensure_ascii=False))


if __name__ == "__main__":
    main()
