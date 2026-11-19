#!/usr/bin/env python3
"""P4: P2-Mesh (manifest.json + .glb) lesen, pruefen und auf das 0,1-m-Raster bringen (numpy, keine Zusatzpakete).

Gleiche Regeln wie manifest.mjs / query.mjs:
  - manifest-Schema laut Grundgeruest 19.11.2026 [F]; _FLAECHE uint8 oder float (ganzzahlig 0-5).
  - Gelaende: je Pixelmitte die oberste Flaeche (Hoehe, Klasse, Neigung). Senkrechte Dreiecke zaehlen nicht.
  - Bruecken (manifest.modelle): Deck = hoechste Aufwaertsflaeche (Normale y >= 0,5) <= tiefste + 0,5 m [A];
    Deck-Fussabdruck 1 px geschlossen (Bohlenfugen 1 cm), Fugenpixel bekommen die Hoehe des naechsten Deckpixels [A].
  - begehbar = Klasse nicht in {3,4} UND Neigung <= 35 Grad [F].
"""
from __future__ import annotations

import json
import struct
from pathlib import Path

import numpy as np

NX, NY, PX = 336, 303, 10
W, H = NX * PX, NY * PX
KLASSEN_SOLL = {"0": "grund", "1": "weg", "2": "ufer", "3": "fels_klippe", "4": "wasser", "5": "bruecke"}
BUCHST = "ABCDEFGH"
BEGEHBAR_MAX_NEIGUNG = 35.0
NICHT_BEGEHBAR = (3, 4)
DECK_FENSTER_M, DECK_NY_MIN = 0.5, 0.5
KOMP = {5121: np.uint8, 5123: np.uint16, 5125: np.uint32, 5126: np.float32}
ANZ = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}


def kachel_grenzen(kid: str) -> list[float]:
    i, j = BUCHST.index(kid[0]), int(kid[1]) - 1
    return [42 * i, 43 * j, 42 * (i + 1), NY if j == 6 else 43 * (j + 1)]


def pruefe_manifest(m: dict) -> tuple[list[str], bool]:
    f = []
    if m.get("version") != 1: f.append(f"version {m.get('version')} statt 1")
    if m.get("einheit") != "m": f.append(f"einheit {m.get('einheit')} statt m")
    if m.get("ursprung") != "weltecke": f.append(f"ursprung {m.get('ursprung')} statt weltecke")
    k = m.get("karte") or {}
    if k.get("breite") != NX or k.get("tiefe") != NY: f.append(f"karte {k}")
    if (m.get("klassen") or {}) != KLASSEN_SOLL: f.append(f"klassen {m.get('klassen')}")
    if not isinstance((m.get("attribute") or {}).get("flaeche"), str): f.append("attribute.flaeche fehlt")
    if not isinstance(m.get("uv"), dict): f.append("uv fehlt")
    ids = set()
    for n, t in enumerate(m.get("kacheln") or []):
        kid = t.get("id", "")
        if not (len(kid) == 2 and kid[0] in BUCHST and kid[1] in "1234567"):
            f.append(f"kacheln[{n}]: id {kid}"); continue
        if kid in ids: f.append(f"kacheln[{n}]: id {kid} doppelt")
        ids.add(kid)
        g = t.get("glb")
        if not isinstance(g, str) or not g or g.startswith("/") or ".." in g.split("/"): f.append(f"{kid}: glb-Pfad {g}")
        bb = t.get("bbox")
        if not (isinstance(bb, list) and len(bb) == 4 and all(abs(a - b) <= 1e-6 for a, b in zip(bb, kachel_grenzen(kid)))):
            f.append(f"{kid}: bbox {bb} statt {kachel_grenzen(kid)}")
        if not isinstance(t.get("dreiecke"), int) or t["dreiecke"] < 0: f.append(f"{kid}: dreiecke {t.get('dreiecke')}")
    if not ids: f.append("kacheln leer")
    for n, md in enumerate(m.get("modelle") or []):
        if not md.get("id") or not isinstance(md.get("glb"), str) or md.get("klasse") not in range(6):
            f.append(f"modelle[{n}]: {md}")
    return f, len(ids) == 56


def lies_glb(p: Path, attribut: str = "_FLAECHE") -> dict:
    b = p.read_bytes()
    if b[:4] != b"glTF": raise ValueError(f"{p.name}: keine glb-Datei")
    off, gltf, binc = 12, None, None
    while off < len(b):
        ln, typ = struct.unpack_from("<II", b, off)
        d = b[off + 8: off + 8 + ln]
        if typ == 0x4E4F534A: gltf = json.loads(d)
        elif typ == 0x004E4942: binc = d
        off += 8 + ln
    for n in gltf.get("nodes", []):
        if any(k in n for k in ("matrix", "rotation", "scale")) or any(v != 0 for v in n.get("translation", [])):
            raise ValueError(f"{p.name}: Node-Transformation vorhanden")

    def acc(i):
        a = gltf["accessors"][i]; bv = gltf["bufferViews"][a["bufferView"]]
        dt = np.dtype(KOMP[a["componentType"]]).newbyteorder("<"); k = ANZ[a["type"]]
        start = bv.get("byteOffset", 0) + a.get("byteOffset", 0); stride = bv.get("byteStride") or k * dt.itemsize
        if stride == k * dt.itemsize:
            return np.frombuffer(binc, dt, a["count"] * k, start).reshape(-1, k).astype(np.float64 if dt.kind == "f" else np.int64)
        raw = np.frombuffer(binc, np.uint8, (a["count"] - 1) * stride + k * dt.itemsize, start)
        return np.stack([np.frombuffer(raw[n * stride: n * stride + k * dt.itemsize].tobytes(), dt) for n in range(a["count"])]).astype(float)

    P, I, F, basis, mitf = [], [], [], 0, None
    for m in gltf.get("meshes", []):
        for pr in m["primitives"]:
            if pr.get("mode", 4) != 4: continue
            pos = acc(pr["attributes"]["POSITION"])
            idx = acc(pr["indices"]).ravel() if "indices" in pr else np.arange(len(pos))
            hat = attribut in pr["attributes"]
            if mitf is None: mitf = hat
            elif mitf != hat: raise ValueError(f"{p.name}: {attribut} nur an einem Teil der Primitives")
            if hat:
                v = acc(pr["attributes"][attribut]).ravel().astype(float)
                if (np.abs(v - np.round(v)) > 1e-3).any() or v.min() < 0 or v.max() > 5:
                    raise ValueError(f"{p.name}: {attribut} nicht ganzzahlig 0-5")
                F.append(np.round(v).astype(np.uint8))
            P.append(pos); I.append(idx + basis); basis += len(pos)
    return {"pos": np.concatenate(P), "idx": np.concatenate(I).reshape(-1, 3), "fl": np.concatenate(F) if mitf else None}


def lade_mesh(manifest_pfad: Path) -> dict:
    m = json.loads(manifest_pfad.read_text(encoding="utf-8"))
    fehler, voll = pruefe_manifest(m)
    if fehler: raise ValueError("manifest.json ungueltig: " + "; ".join(fehler))
    attr, basis = m["attribute"]["flaeche"], manifest_pfad.parent
    teile, abw = [], []
    for k in m["kacheln"]:
        t = lies_glb(basis / k["glb"], attr)
        if t["fl"] is None: raise ValueError(f"{k['glb']}: {attr} fehlt")
        if len(t["idx"]) != k["dreiecke"]: abw.append(f"{k['id']}: {len(t['idx'])} statt {k['dreiecke']}")
        teile.append(t)
    if abw: raise ValueError("manifest.dreiecke passt nicht: " + "; ".join(abw))
    pos, idx, fl, b = [], [], [], 0
    for t in teile:
        pos.append(t["pos"]); idx.append(t["idx"] + b); fl.append(t["fl"]); b += len(t["pos"])
    gel = {"pos": np.concatenate(pos), "idx": np.concatenate(idx), "fl": np.concatenate(fl)}
    modelle = [{"id": md["id"], "klasse": md["klasse"], **lies_glb(basis / md["glb"], attr)} for md in m.get("modelle", [])]
    f3 = gel["fl"][gel["idx"]]
    gemischt = int((~((f3[:, 0] == f3[:, 1]) & (f3[:, 1] == f3[:, 2]))).sum())
    return {"manifest": m, "vollstaendig": voll, "gelaende": gel, "modelle": modelle, "gemischte_dreiecke": gemischt}


def treffer(pos: np.ndarray, idx: np.ndarray, block: int = 200_000):
    """Pixelmitten-Treffer aller Dreiecke: yield (pixel_index, y, tri_index, ny). Senkrechte Dreiecke entfallen."""
    A, B, C = pos[idx[:, 0]], pos[idx[:, 1]], pos[idx[:, 2]]
    n = np.cross(B - A, C - A); ln = np.linalg.norm(n, axis=1); ny = np.where(ln > 0, n[:, 1] / np.maximum(ln, 1e-300), 0)
    xs = np.stack([A[:, 0], B[:, 0], C[:, 0]], 1) * PX - 0.5; zs = np.stack([A[:, 2], B[:, 2], C[:, 2]], 1) * PX - 0.5
    i0 = np.maximum(0, np.ceil(xs.min(1) - 1e-9)).astype(np.int64); i1 = np.minimum(W - 1, np.floor(xs.max(1) + 1e-9)).astype(np.int64)
    j0 = np.maximum(0, np.ceil(zs.min(1) - 1e-9)).astype(np.int64); j1 = np.minimum(H - 1, np.floor(zs.max(1) + 1e-9)).astype(np.int64)
    ok = (i1 >= i0) & (j1 >= j0) & (np.abs(ny) > 1e-9)
    kx, kz = (i1 - i0 + 1), (j1 - j0 + 1)
    for K in np.unique(np.maximum(kx, kz)[ok]):
        sel = np.nonzero(ok & (np.maximum(kx, kz) == K))[0]
        dj, di = np.divmod(np.arange(K * K), K)
        for s in range(0, len(sel), max(1, block // (K * K))):
            t = sel[s: s + max(1, block // (K * K))]
            I = i0[t, None] + di[None]; J = j0[t, None] + dj[None]
            px = (I + 0.5) / PX; pz = (J + 0.5) / PX
            ax, az, bx, bz, cx, cz = (A[t, 0, None], A[t, 2, None], B[t, 0, None], B[t, 2, None], C[t, 0, None], C[t, 2, None])
            d = (bz - cz) * (ax - cx) + (cx - bx) * (az - cz)
            l1 = ((bz - cz) * (px - cx) + (cx - bx) * (pz - cz)) / d
            l2 = ((cz - az) * (px - cx) + (ax - cx) * (pz - cz)) / d
            l3 = 1 - l1 - l2
            m = (I <= i1[t, None]) & (J <= j1[t, None]) & (l1 >= -1e-9) & (l2 >= -1e-9) & (l3 >= -1e-9)
            y = l1 * A[t, 1, None] + l2 * B[t, 1, None] + l3 * C[t, 1, None]
            tt = np.broadcast_to(t[:, None], m.shape)
            yield (J[m] * W + I[m]), y[m], tt[m], ny[tt[m]]


def rastere(mesh: dict) -> dict:
    from scipy import ndimage
    g = mesh["gelaende"]
    hy = np.full(W * H, -np.inf); ht = np.full(W * H, -1, np.int64); hn = np.zeros(W * H)
    for pix, y, t, ny in treffer(g["pos"], g["idx"]):
        o = np.argsort(y, kind="stable"); pix, y, t, ny = pix[o], y[o], t[o], ny[o]
        m = y > hy[pix]
        hy[pix[m]] = y[m]; ht[pix[m]] = t[m]; hn[pix[m]] = ny[m]
    getroffen = ht >= 0
    f3 = g["fl"][g["idx"]]
    kl = np.full(W * H, -1, np.int16)
    rein = (f3[:, 0] == f3[:, 1]) & (f3[:, 1] == f3[:, 2])
    kl[getroffen] = np.where(rein[ht[getroffen]], f3[ht[getroffen], 0].astype(np.int16), np.int16(-1))
    hoehe = np.where(getroffen, hy, np.nan); neig = np.where(getroffen, np.degrees(np.arccos(np.minimum(1, np.abs(hn)))), np.nan)
    deck_info = []
    deck_maske = np.zeros(W * H, bool)
    for md in mesh["modelle"]:
        tief = np.full(W * H, np.inf)
        Ys, Ns, Ps = [], [], []
        for p, y, _, n in treffer(md["pos"], md["idx"]):
            s = n >= DECK_NY_MIN; Ps.append(p[s]); Ys.append(y[s]); Ns.append(n[s])
        if not Ps or not sum(len(p) for p in Ps): continue
        Pp, Yy, Nn = np.concatenate(Ps), np.concatenate(Ys), np.concatenate(Ns)
        np.minimum.at(tief, Pp, Yy)
        m = Yy <= tief[Pp] + DECK_FENSTER_M + 1e-9
        Pp, Yy, Nn = Pp[m], Yy[m], Nn[m]
        o = np.argsort(Yy, kind="stable"); Pp, Yy, Nn = Pp[o], Yy[o], Nn[o]
        dy = np.full(W * H, np.nan); dn = np.full(W * H, np.nan)
        dy[Pp] = Yy; dn[Pp] = np.degrees(np.arccos(np.minimum(1, np.abs(Nn))))
        maske = ~np.isnan(dy).reshape(H, W)
        zu = ndimage.binary_closing(maske, np.ones((3, 3), bool), border_value=0) | maske
        fuge = zu & ~maske
        if fuge.any():
            _, (jj, ii) = ndimage.distance_transform_edt(~maske, return_indices=True)
            q = (jj * W + ii).ravel()[fuge.ravel()]
            dy[fuge.ravel()] = dy[q]; dn[fuge.ravel()] = dn[q]
        z = zu.ravel()
        hoehe[z] = dy[z]; neig[z] = dn[z]; kl[z] = md["klasse"]; deck_maske |= z
        deck_info.append({"id": md["id"], "deck_px": int(maske.sum()), "fugen_px": int(fuge.sum())})
    return {"hoehe": hoehe.reshape(H, W), "klasse": kl.reshape(H, W), "neigung": neig.reshape(H, W), "deck": deck_info,
            "deck_maske": deck_maske.reshape(H, W),
            "ohne_mesh_px": int((~getroffen).sum())}


def begehbar_regel(klasse: np.ndarray, neigung: np.ndarray) -> np.ndarray:
    return (~np.isin(klasse, NICHT_BEGEHBAR)) & (klasse >= 0) & np.nan_to_num(neigung <= BEGEHBAR_MAX_NEIGUNG + 1e-9, nan=False)
