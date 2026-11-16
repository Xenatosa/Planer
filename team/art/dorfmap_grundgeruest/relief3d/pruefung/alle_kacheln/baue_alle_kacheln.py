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
from neu import wand as WD  # noqa: E402

BUCHST = "ABCDEFGH"


def kachel_grenzen(nx: int, ny: int, randzeilen: bool = True) -> dict[str, tuple[int, int, int, int]]:
    """Wie TILE_BOUNDS/pruefe_regeln.feld: Spalte 42 Zellen, Zeile 43 Zellen.

    P10b: pruefe_regeln.feld() ordnet z >= 301 per np.clip(z//43, 0, 6) der Zeile 7 zu. Die
    Zellreihen z 301-302 (ny = 303) werden deshalb an die Kacheln der Zeile 7 angehaengt
    (z1 = ny), statt wie in P10 wegzufallen. randzeilen=False = alter P10-Stand (z1 = 301)."""
    out = {}
    for iz in range(7):
        for ix in range(8):
            x0, z0 = ix * 42, iz * 43
            z1 = ny if (iz == 6 and randzeilen) else min(ny, z0 + 43)
            out[f"{BUCHST[ix]}{iz + 1}"] = (x0, z0, min(nx, x0 + 42), z1)
    return out


def waende_alle(vektor_pfad: Path, terrain_tiles: dict, kacheln: list[str], original: dict) -> dict:
    """Wandkoerper fuer alle Kacheln mit denselben Funktionen wie neu.wand.build_wall_manifest()
    (Schleifenrumpf 1:1, Standardvarianten WANDVAR=1, RELIEF_WANDFUSS_VAR=2), nur mit Kachelliste.
    D2 bleibt wie in der Pipeline wandfrei; was dort unterdrueckt wird, steht in 'd2_unterdrueckt'."""
    variant = int(os.environ.get("WANDVAR", str(WD.DEFAULT_VARIANT)))
    foot_variant = int(os.environ.get("RELIEF_WANDFUSS_VAR", "2"))
    vector = json.loads(vektor_pfad.read_text(encoding="utf-8"))
    out: dict[str, dict] = {}
    nicht_gerendert: dict[str, list] = {}
    for tile in kacheln:
        bounds = M.TILE_BOUNDS[tile]
        terrain = WD._terrain_heights(terrain_tiles, tile) if foot_variant in (1, 2) else None
        pieces, network_chunks, features, used_widths = [], [], 0, []
        normals = np.empty((0, 3), dtype="<f4")
        for wall in vector.get("waende", []):
            nominal = float(wall.get("breite_min_m", 0.0))
            width = max(nominal, 2.4 if variant == 0 else nominal)
            # P10c: neu/wand.py baut in Zellen (Breite / CELL_M); aeltere wand.py ohne _centerline_cells in Metern-als-Zellen.
            width_geo = width / WD.CELL_M if hasattr(WD, "_centerline_cells") else width
            for points, top, bottom in WD._chunks(wall, bounds, width, variant):
                # P10d: Oberkante an lokale Gelaendekrone binden, Schnittreste < 1 Zelle nicht bauen (wie neu/wand.py).
                if hasattr(WD, "bind_chunk_to_terrain"):
                    runs, info = WD.bind_chunk_to_terrain(points, top, bottom, width_geo, terrain, tile)
                    if "grund" in info:
                        nicht_gerendert.setdefault(tile, []).append({
                            "wand": f"{wall.get('name')}:{wall.get('teil')}",
                            "start": [round(float(v), 2) for v in points[0]],
                            "ende": [round(float(v), 2) for v in points[-1]], **info})
                    if not runs:
                        continue
                else:
                    runs = [(points, np.maximum(top, bottom))]
                used_widths.append(width)
                if terrain is not None:
                    network_chunks.extend((rp, rt, width_geo) for rp, rt in runs)
                else:
                    positions, indices = WD._solid(points, np.maximum(top, bottom), np.minimum(top, bottom), width_geo, variant)
                    if len(indices):
                        pieces.append((positions, indices)); features += 1
        if terrain is not None and network_chunks:
            positions, indices, features, _lowered, normals = WD._network_solid(
                network_chunks, terrain[0], terrain[1], tile, embed_m=0.15, split_on_terrain=foot_variant == 2)
            if len(indices):
                pieces = [(positions, indices)]
        if pieces:
            positions = np.concatenate([p for p, _ in pieces]).astype("<f4", copy=False)
            parts, off = [], 0
            for p_, ix_ in pieces:
                parts.append(ix_ + off); off += len(p_)
            indices = np.concatenate(parts).astype("<u4", copy=False)
        else:
            positions, indices = np.empty((0, 3), dtype="<f4"), np.empty((0,), dtype="<u4")
        out[tile] = {
            "vertices_xyz_f32": _b64(positions.reshape(-1)), "indices_u32": _b64(indices),
            "normals_xyz_f32": _b64(normals.reshape(-1)),
            "vertices": int(len(positions)), "triangles": int(len(indices) // 3),
            "features": int(features), "chunks": len(network_chunks) if terrain is not None else features,
            "min_width_m": min(used_widths) if used_widths else None,
            "mesh_sha256": hashlib.sha256(positions.tobytes() + indices.tobytes()).hexdigest(),
        }
    # Kontrolle gegen die Pipeline (D1/G1) und D2-Regel der Pipeline.
    for t in ("D1", "G1"):
        if out[t]["mesh_sha256"] != original["tiles"][t]["mesh_sha256"]:
            raise RuntimeError(f"Wandmesh {t} weicht von neu.wand.build_wall_manifest ab")
    d2 = out.pop("D2")
    out["D2"] = dict(original["tiles"]["D2"])
    nicht_gerendert.pop("D2", None)
    return {"tiles": out, "nicht_gerendert": nicht_gerendert, "d2_unterdrueckt": {k: d2[k] for k in ("vertices", "triangles", "features", "chunks")},
            "d2_unterdrueckt_mesh": d2}


def _b64(a: np.ndarray) -> str:
    return base64.b64encode(a.tobytes(order="C")).decode("ascii")


def baue(out_dir: Path, mit_erweiterung: bool = True, testloch: str | None = None, name: str = "alle_kacheln",
         randzeilen: bool = True, wegprofile: bool = True, alle_waende: bool = True) -> dict:
    t0 = time.time()
    relief = R / "relief_daten.json.gz"
    source = M.load_relief(relief)
    rs, nx, ny = int(source.data["rs"]), int(source.data["nx"]), int(source.data["ny"])
    # 1) Prototyp-Kacheln exakt wie neu/pipeline.py (Standardvarianten aus der Umgebung).
    try:
        manifest = M.build_manifest(relief, R / "neu" / "zellen_relief.csv",
                                    R / "neu" / "vektor.json", R / "neu" / "felder.npz")
        prototyp_quelle = "neu.mesh.build_manifest"
    except RuntimeError as err:
        # P10c: Seit a10fc1e (P3) passt relief_daten.json.gz nicht mehr zur p3d17-Rasterloesung
        # (source_relief_sha256), build_manifest() bricht fuer D1 ab. index.html nutzt das
        # gespeicherte Manifest aus neu/relief_neu.json.gz -> genau dieses verwenden.
        # P10e: Seit P2 (9ace686, Rampen entnommen) bricht build_manifest() auch mit
        # "Erwartete D1-Kreuzung rampe_2/rampe_11 fehlt" ab -> ebenfalls das gespeicherte Manifest.
        if "p3d17" not in str(err) and "rampe_2/rampe_11" not in str(err):
            raise
        manifest = json.loads(gzip.decompress((R / "neu" / "relief_neu.json.gz").read_bytes()))["neu_mesh_tiles"]
        prototyp_quelle = f"neu/relief_neu.json.gz (gespeichert; build_manifest: {err})"
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

    grenzen = kachel_grenzen(nx, ny, randzeilen)
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

    vector = json.loads((R / "neu" / "vektor.json").read_text(encoding="utf-8"))
    with np.load(R / "neu" / "felder.npz", allow_pickle=False) as arch:
        fields = {n: arch[n] for n in arch.files}
    tiles: dict[str, dict] = {}
    kontrolle = {}
    profile = {}
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
            slab = feld[z0 * rs: z1 * rs + 1, x0 * rs: x1 * rs + 1].copy()
            gb = source.heights[z0 * rs: z1 * rs + 1, x0 * rs: x1 * rs + 1]
            if wegprofile:
                # Dieselbe Pipeline-Funktion wie fuer D1/G1 (Variante 2, Wegende 1, Kreuzung 24);
                # ihre Aenderung gegenueber GB wird auf das Feld gelegt.
                h, pinfo = M.terrain_heights(source, t, vector, fields, manifest["terrain_variant"])
                d = h.astype(np.float64) - gb
                if pinfo["changed_vertices"]:
                    slab = (slab.astype(np.float64) + d).astype("<f4")
                    profile[t] = {k: pinfo[k] for k in ("changed_vertices", "max_abs_delta_m", "layers")}
            P, I = M.tile_mesh(source, t, slab)
            item = {
                "bounds": [x0, z0, x1, z1], "samples_per_m": rs, "sampling_m": 1.0 / rs,
                "surface_mode": "locked_visible_GB_bytes" + ("+wegprofil" if t in profile else "") + (
                    "+terrain_extensions" if ext_n and (feld[z0 * rs: z1 * rs + 1, x0 * rs: x1 * rs + 1] != gb).any() else ""),
                "vertices_xyz_f32": _b64(P), "indices_u32": _b64(I),
                "vertices": int(len(P)), "triangles": int(len(I) // 3),
                "height_sha256": hashlib.sha256(P[:, 1].tobytes()).hexdigest(),
                "mesh_sha256": hashlib.sha256(P.tobytes() + I.tobytes()).hexdigest(),
                "verfahren": "neu.mesh.terrain_heights + tile_mesh auf GB" if t in profile else "neu.mesh.tile_mesh auf GB (wie D2)",
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

    # 4) Waende fuer alle Kacheln (gleiche Funktionen wie neu/wand.py), D2 wie Pipeline wandfrei.
    tw = time.time()
    if alle_waende:
        wa = waende_alle(R / "neu" / "vektor.json", tiles, list(grenzen), waende)
        waende_paket = {**{k: v for k, v in waende.items() if k != "tiles"}, "tiles": wa["tiles"], "nicht_gerendert": wa["nicht_gerendert"],
                        "d2_unterdrueckt": wa["d2_unterdrueckt"], "d2_unterdrueckt_mesh": wa["d2_unterdrueckt_mesh"]}
    else:
        waende_paket = waende
    t_waende = time.time() - tw

    # 5) Kennzahlen je Kachel: Wege (WEGA, vektor.json wege), Wasser (WV, vektor.json wasser),
    #    Waende (vektor.json waende -> Wandkoerper), Klippenzellen aus der Zellquelle.
    wega = np.frombuffer(base64.b64decode(source.data["WEGA"]), dtype=np.uint8).reshape(source.heights.shape)
    wv = np.frombuffer(base64.b64decode(source.data["WV"]), dtype="<f4").reshape(source.heights.shape)
    import csv as _csv
    klippe = {}
    with (R.parent / "raster_c20_z25_zellen.csv").open(encoding="utf-8-sig", newline="") as fh:
        for row in _csv.DictReader(fh):
            if row["klippe"] in ("WAND", "KANTE"):
                tt = BUCHST[min(int(row["cx"]) // 42, 7)] + str(min(int(row["cy"]) // 43, 6) + 1)
                klippe.setdefault(tt, {"WAND": 0, "KANTE": 0})[row["klippe"]] += 1
    def _schneidet(poly, b):
        x0, z0, x1, z1 = b
        P_ = np.asarray(poly, dtype=np.float64) / M.CELL_M
        return bool(len(P_) and (P_[:, 0].max() >= x0) and (P_[:, 0].min() <= x1) and (P_[:, 1].max() >= z0) and (P_[:, 1].min() <= z1))
    kennzahlen = {}
    for t, (x0, z0, x1, z1) in grenzen.items():
        sl = (slice(z0 * rs, z1 * rs + 1), slice(x0 * rs, x1 * rs + 1))
        wt = waende_paket["tiles"].get(t, {})
        kennzahlen[t] = {
            "wega_vertices": int(np.count_nonzero(wega[sl])),
            "wv_vertices": int(np.count_nonzero(wv[sl] > -900)),
            "vektor_wege": sum(_schneidet(w["mittellinie_m"], (x0, z0, x1, z1)) for w in vector["wege"]),
            "vektor_wasser": sum(_schneidet(w["polygon_m"], (x0, z0, x1, z1)) for w in vector["wasser"]),
            "wand_chunks": sum(len(list(WD._chunks(w, (x0, z0, x1, z1), float(w["breite_min_m"]), int(waende["variant"]))))
                               for w in vector["waende"]),
            "wand_dreiecke": int(wt.get("triangles", 0)),
            "klippe_WAND_zellen": klippe.get(t, {}).get("WAND", 0),
            "klippe_KANTE_zellen": klippe.get(t, {}).get("KANTE", 0),
            "wegprofil_vertices": profile.get(t, {}).get("changed_vertices", 0) if t not in proto
            else manifest["terrain"][t]["changed_vertices"],
        }

    paket = {
        "nx": nx, "ny": ny, "rs": rs, "GB": source.data.get("GB") or source.data["G"],
        "VC": source.data["VC"], "WV": source.data["WV"], "WEGA": source.data["WEGA"],
        "start": source.data.get("start"), "bruecken": source.data.get("bruecken", []),
        "alle_kacheln": {
            "format": "p10-alle-kacheln-v1",
            "quelle": "relief_daten.json.gz",
            "source_relief_sha256": source.source_file_sha256,
            "terrain_variant": manifest["terrain_variant"],
            "terrain_extensions_angewendet": ext_n,
            "reihenfolge": list(grenzen),
            "tiles": tiles,
            "waende": waende_paket,
            "kennzahlen": kennzahlen,
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
        "prototyp_quelle": prototyp_quelle,
        "terrain_extensions_angewendet": ext_n,
        "flaechen_dreiecke": sum(t["triangles"] for t in tiles.values()),
        "geschlossen_dreiecke": sum(t["closed_triangles"] for t in tiles.values()),
        "wand_dreiecke": sum(t["triangles"] for t in waende_paket["tiles"].values()),
        "naht": naht,
        "randzeilen_z301_303": randzeilen, "wegprofile_andere_kacheln": profile,
        "waende_d2_unterdrueckt": waende_paket.get("d2_unterdrueckt"),
        "kennzahlen": kennzahlen,
        "paket_bytes": len(gz),
        "kacheln_info": {t: {k: v for k, v in it.items() if k not in ("vertices_xyz_f32", "indices_u32")}
                         for t, it in tiles.items()},
        "dauer_s": {"prototyp": round(t_proto, 2), "waende": round(t_waende, 2), "gesamt": round(time.time() - t0, 2)},
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
    ap.add_argument("--nur-html", action="store_true", help="nur HTML aus vorhandenem <out>/<name>.json.gz neu bauen (Viewer-Aenderungen)")
    ap.add_argument("--ohne-randzeilen", action="store_true", help="Zeile 7 wie P10 nur bis z=301")
    ap.add_argument("--ohne-wegprofile", action="store_true", help="kein terrain_heights() fuer Nicht-Prototyp-Kacheln")
    ap.add_argument("--ohne-alle-waende", action="store_true", help="Waende nur D1/G1 wie P10")
    ap.add_argument("--testloch", metavar="KACHEL", help="Positivkontrolle: entfernt 1 Dreieck in KACHEL, schreibt alle_kacheln_testloch_<KACHEL>.*")
    a = ap.parse_args()
    out = Path(a.out)
    if out.resolve() == Path("/tmp/w3") or str(out.resolve()).startswith("/tmp/w3/"):
        raise SystemExit("Ausgabe nach /tmp/w3 ist gesperrt (laufende Jobs).")
    t = time.time()
    name = f"alle_kacheln_testloch_{a.testloch}" if a.testloch else "alle_kacheln"
    if a.nur_html:
        print(json.dumps({"html_bytes": baue_html(out, name)}))
        return
    info = baue(out, not a.ohne_erweiterung, a.testloch, name,
                not a.ohne_randzeilen, not a.ohne_wegprofile, not a.ohne_alle_waende)
    if not a.ohne_html:
        th = time.time()
        info["html_bytes"] = baue_html(out, name)
        info["dauer_s"]["html"] = round(time.time() - th, 2)
    info["dauer_s"]["gesamt"] = round(time.time() - t, 2)
    (out / f"{name}_build.json").write_text(json.dumps(info, ensure_ascii=False, indent=1, sort_keys=True) + "\n")
    kurz = {k: info[k] for k in ("kacheln", "prototyp_mit_tile_mesh_identisch", "prototyp_quelle", "terrain_extensions_angewendet",
                                  "wegprofile_andere_kacheln", "waende_d2_unterdrueckt", "wand_dreiecke",
                                  "flaechen_dreiecke", "geschlossen_dreiecke", "naht", "paket_bytes", "dauer_s")}
    kurz["html_bytes"] = info.get("html_bytes")
    print(json.dumps(kurz, ensure_ascii=False))


if __name__ == "__main__":
    main()
