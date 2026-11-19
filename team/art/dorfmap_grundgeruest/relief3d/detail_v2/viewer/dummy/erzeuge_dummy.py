"""P3 Viewer v2: Dummy-Mesh im Planformat (DETAIL_V2_PLAN.md 3.2, Export-Zeile) [S].

Grob aus dem alten Hoehenraster GB (relief_daten.json.gz, 0,5 m) mit Schrittweite --schritt (Standard 2 = 1,0 m),
je Kachel eine .glb (glTF 2.0 binaer, kein Draco) + manifest.json. NUR zum Testen des Viewers, kein echtes Mesh [A].
Kacheln A-H x 1-7, Schnitt bei x = 42*i, z = 43*j (letzte Zeile bis z = 303), 1 Einheit = 1 m, y oben.
Attribute: POSITION, NORMAL (global aus dem Raster, nahtlos), TEXCOORD_0 = Welt-XZ in m, TEXCOORD_1 = (x/336, z/303).
Aufruf (im Ordner relief3d):  python3 detail_v2/viewer/dummy/erzeuge_dummy.py --out /tmp/dv2_viewer/dummy_mesh [--schritt 2] [--kacheln A1,B1]
Ausgabe gehoert NICHT nach detail_v2/mesh/ (dort liefert P2 das echte Mesh).
"""
import argparse, base64, gzip, hashlib, json, struct
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]          # relief3d/
NX, NZ, KX, KZ = 336, 303, 42, 43
SPALTEN = "ABCDEFGH"


def schnitte():
    xs = [KX * i for i in range(9)]
    zs = [KZ * j for j in range(7)] + [NZ]           # 0..258, letzte Zeile 258..303 [A]
    return xs, zs


def glb(name, pos, nor, uv0, uv1, idx, extras):
    teile, views, acc = [], [], []
    def add(arr, ziel, typ, komp, mm=False):
        b = arr.tobytes(); off = sum(len(t) for t in teile)
        teile.append(b + b"\0" * (-len(b) % 4))
        views.append({"buffer": 0, "byteOffset": off, "byteLength": len(b), **({"target": ziel} if ziel else {})})
        a = {"bufferView": len(views) - 1, "componentType": komp, "count": int(arr.shape[0]) if arr.ndim > 1 else int(arr.size), "type": typ}
        if mm: a["min"] = arr.min(0).tolist(); a["max"] = arr.max(0).tolist()
        acc.append(a); return len(acc) - 1
    ap = add(pos, 34962, "VEC3", 5126, True); an = add(nor, 34962, "VEC3", 5126)
    a0 = add(uv0, 34962, "VEC2", 5126); a1 = add(uv1, 34962, "VEC2", 5126); ai = add(idx, 34963, "SCALAR", 5125)
    binb = b"".join(teile)
    js = {"asset": {"version": "2.0", "generator": "dv2 viewer dummy (P3)"}, "scene": 0, "scenes": [{"nodes": [0]}],
          "nodes": [{"mesh": 0, "name": name, "extras": extras}],
          "meshes": [{"name": name, "primitives": [{"attributes": {"POSITION": ap, "NORMAL": an, "TEXCOORD_0": a0, "TEXCOORD_1": a1}, "indices": ai, "mode": 4}]}],
          "buffers": [{"byteLength": len(binb)}], "bufferViews": views, "accessors": acc}
    j = json.dumps(js, separators=(",", ":")).encode(); j += b" " * (-len(j) % 4)
    return struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(j) + 8 + len(binb)) + struct.pack("<II", len(j), 0x4E4F534A) + j + struct.pack("<II", len(binb), 0x004E4942) + binb


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); ap.add_argument("--schritt", type=int, default=2)
    ap.add_argument("--kacheln", default=""); ap.add_argument("--daten", default=str(ROOT / "relief_daten.json.gz")); a = ap.parse_args()
    D = json.load(gzip.open(a.daten)); rs = int(D["rs"]); GX, GZ = NX * rs + 1, NZ * rs + 1
    G = np.frombuffer(base64.b64decode(D["GB"]), np.float32).reshape(GZ, GX).astype(np.float64)
    s = a.schritt; d = s / rs                                  # Abstand in m
    gy, gx = np.gradient(G, 1.0 / rs)                          # Normalen global aus dem Raster -> nahtlos
    N = np.dstack([-gx, np.ones_like(G), -gy]); N /= np.linalg.norm(N, axis=2, keepdims=True)
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    xs, zs = schnitte(); wahl = set(a.kacheln.split(",")) if a.kacheln else None; kacheln = []
    for j in range(7):
        for i in range(8):
            kid = f"{SPALTEN[i]}{j + 1}"
            if wahl and kid not in wahl: continue
            x0, x1, z0, z1 = xs[i], xs[i + 1], zs[j], zs[j + 1]
            ii = np.arange(x0 * rs, x1 * rs + 1, s); jj = np.arange(z0 * rs, z1 * rs + 1, s)
            if ii[-1] != x1 * rs: ii = np.append(ii, x1 * rs)
            if jj[-1] != z1 * rs: jj = np.append(jj, z1 * rs)
            J, I = np.meshgrid(jj, ii, indexing="ij"); w, h = len(ii), len(jj)
            pos = np.stack([I / rs, G[J, I], J / rs], -1).reshape(-1, 3).astype(np.float32)
            nor = N[J, I].reshape(-1, 3).astype(np.float32)
            uv0 = pos[:, [0, 2]].copy(); uv1 = np.stack([pos[:, 0] / NX, pos[:, 2] / NZ], -1).astype(np.float32)
            a_ = (np.arange(h - 1)[:, None] * w + np.arange(w - 1)[None, :]).ravel(); b_ = a_ + 1; c_ = a_ + w; d_ = c_ + 1
            idx = np.stack([a_, c_, b_, b_, c_, d_], -1).reshape(-1).astype(np.uint32)   # Wicklung: Normale nach +y
            data = glb(f"gelaende_{kid}", pos, nor, uv0, uv1, idx, {"kachel": kid, "dummy": True})
            (out / f"{kid}.glb").write_bytes(data)
            kacheln.append({"id": kid, "datei": f"{kid}.glb", "bounds": [x0, z0, x1, z1], "vertices": int(len(pos)), "dreiecke": int(len(idx) // 3),
                            "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    man = {"format": "dorfmap-detail-v2-mesh", "version": 1, "quelle": f"DUMMY aus GB (relief_daten.json.gz), Schritt {d:g} m - kein echtes Mesh",
           "einheit_m": 1, "achsen": {"x": "Ost (0..336)", "y": "oben (m)", "z": "Sued (0..303)"}, "welt": {"x_m": NX, "z_m": NZ},
           "kachelschema": {"spalten": SPALTEN, "zeilen": 7, "schnitt_x": xs, "schnitt_z": zs, "id": "Spalte + Zeile, z. B. E3"},
           "uv": {"TEXCOORD_0": "Welt-XZ in m", "TEXCOORD_1": "(x/336, z/303)"}, "draco": False,
           "budget": {"dreiecke_je_kachel_max": 60000, "dreiecke_gesamt_max": 1600000},
           "kacheln": kacheln, "dreiecke_gesamt": sum(k["dreiecke"] for k in kacheln)}
    (out / "manifest.json").write_text(json.dumps(man, indent=1, ensure_ascii=False))
    print(json.dumps({"kacheln": len(kacheln), "dreiecke_gesamt": man["dreiecke_gesamt"], "max_je_kachel": max(k["dreiecke"] for k in kacheln),
                      "bytes": sum(k["bytes"] for k in kacheln)}))


if __name__ == "__main__":
    main()
