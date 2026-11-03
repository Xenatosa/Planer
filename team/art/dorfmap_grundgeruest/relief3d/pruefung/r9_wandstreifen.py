#!/usr/bin/env python3
"""R9s: short-period normal-direction changes on steep wall faces.

The detector uses 0.25 m samples. It compares the exact coarse triangle surface
with the stored fine-band surface, reports band-edge height mismatch separately,
and lists one R9s hit per tile that contains a periodic normal change >10 degrees
with a period below 2 m.
"""
import argparse
import base64
import gzip
import json
import sys

import numpy as np
from scipy import ndimage as ndi


FS_OUT = 4
PERIODS = (0.25, 2.0)
AMP_LIMIT = 10.0
CORR_LIMIT = 0.53
MIN_PAIRS = 64


def read_data(path):
    with gzip.open(path, "rt", encoding="utf-8") as f:
        return json.load(f)


def decode(s, dtype):
    return np.frombuffer(base64.b64decode(s), dtype=dtype)


def triangulated_at_fine(g, nx, ny, rs, fs):
    """Evaluate the renderer's two-triangle split at every fine-grid vertex."""
    fny, fnx = ny * fs + 1, nx * fs + 1
    x = np.arange(fnx, dtype=np.float32) * (rs / fs)
    ix = np.minimum(x.astype(np.int32), g.shape[1] - 2)
    ax = x - ix
    out = np.empty((fny, fnx), dtype=np.float32)
    for fy in range(fny):
        z = fy * (rs / fs)
        iz = min(int(z), g.shape[0] - 2)
        az = z - iz
        a, b = g[iz, ix], g[iz, ix + 1]
        c, d = g[iz + 1, ix], g[iz + 1, ix + 1]
        out[fy] = np.where(az >= ax, a + az * (c - a) + ax * (d - c),
                           a + ax * (b - a) + az * (d - b))
    return out


def wall_normals(height, spacing):
    gz, gx = np.gradient(height.astype(np.float32), spacing, edge_order=1)
    steep = np.hypot(gx, gz)
    # Horizontal direction of the surface normal; its sign is immaterial here.
    theta = np.arctan2(gz, gx)
    c = ndi.gaussian_filter(np.cos(2 * theta), sigma=2.0 / spacing, mode="nearest")
    s = ndi.gaussian_filter(np.sin(2 * theta), sigma=2.0 / spacing, mode="nearest")
    trend = 0.5 * np.arctan2(s, c)
    residual = 0.5 * np.arctan2(np.sin(2 * (theta - trend)), np.cos(2 * (theta - trend)))
    return steep, residual


def paired_slices(shape, dx, dy, lag):
    h, w = shape
    sx0, sx1 = max(0, -dx * lag), min(w, w - dx * lag)
    sy0, sy1 = max(0, -dy * lag), min(h, h - dy * lag)
    return (slice(sy0, sy1), slice(sx0, sx1)), (slice(sy0 + dy * lag, sy1 + dy * lag),
                                                    slice(sx0 + dx * lag, sx1 + dx * lag))


def periodic_signal(residual, mask, spacing):
    """Find a correlated normal-angle repeat at a sub-2 m displacement."""
    best = None
    dirs = ((1, 0), (0, 1), (1, 1), (1, -1))
    for dx, dy in dirs:
        for lag in range(1, int(np.ceil(PERIODS[1] / (spacing * np.hypot(dx, dy)))) + 1):
            period = spacing * lag * np.hypot(dx, dy)
            if not PERIODS[0] <= period < PERIODS[1]:
                continue
            a_sl, b_sl = paired_slices(mask.shape, dx, dy, lag)
            ok = mask[a_sl] & mask[b_sl]
            n = int(ok.sum())
            if n < MIN_PAIRS:
                continue
            a = residual[a_sl][ok].astype(np.float64)
            b = residual[b_sl][ok].astype(np.float64)
            a -= a.mean()
            b -= b.mean()
            sa, sb = a.std(), b.std()
            amp = float(np.degrees(np.sqrt(sa * sb) * np.sqrt(2.0)))
            if sa < 1e-8 or sb < 1e-8:
                continue
            corr = float(np.mean(a * b) / (sa * sb))
            cand = {"periode_m": round(float(period), 2),
                    "abweichung_grad": round(amp, 1),
                    "korrelation": round(corr, 3), "paare": n,
                    "treffer": bool(amp > AMP_LIMIT and corr >= CORR_LIMIT)}
            if best is None or (corr * amp, corr, -period) > (best["korrelation"] * best["abweichung_grad"],
                                                                 best["korrelation"], -best["periode_m"]):
                best = cand
    return best


def field_slices(nx, ny, fs, x_tile, z_tile):
    x0, x1 = x_tile * 42 * fs, min((x_tile + 1) * 42 * fs, nx * fs)
    z0, z1 = z_tile * 43 * fs, min((z_tile + 1) * 43 * fs, ny * fs)
    return slice(z0, z1), slice(x0, x1)


def measure_field(name, sl, coarse_resid, actual_resid, fine_resid,
                  coarse_wall, actual_wall, fine_wall, band_vertices, band_interior,
                  seam_delta, seam_boundary):
    cz, cx = sl
    def probe(resid, mask):
        return periodic_signal(resid[cz, cx], mask[cz, cx], 1.0 / FS_OUT)

    coarse = probe(coarse_resid, coarse_wall)
    actual = probe(actual_resid, actual_wall)
    fine = probe(fine_resid, fine_wall & band_interior)
    seam_m = seam_boundary[cz, cx]
    seam_d = seam_delta[cz, cx][seam_m]
    bd = band_vertices[cz, cx]
    wall = actual_wall[cz, cx]
    return {
        "wandpunkte": int(wall.sum()),
        "feinbandanteil_pct": round(100 * float((wall & bd).sum()) / max(1, int(wall.sum())), 1),
        "raster_gegenprobe": coarse,
        "feinband_innen": fine,
        "tatsaechliches_netz": actual,
        "naht_hoehenabweichung_m": {
            "punkte": int(seam_d.size),
            "mittel": round(float(seam_d.mean()), 4) if seam_d.size else 0.0,
            "p95": round(float(np.percentile(seam_d, 95)), 4) if seam_d.size else 0.0,
            "max": round(float(seam_d.max()), 4) if seam_d.size else 0.0,
            "ueber_2cm": int((seam_d > 0.02).sum()),
        },
        "treffer": int(actual is not None and actual["treffer"]),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("relief", nargs="?", default="relief_daten.json.gz")
    ap.add_argument("out", nargs="?")
    args = ap.parse_args()
    d = read_data(args.relief)
    nx, ny, rs = int(d["nx"]), int(d["ny"]), int(d["rs"])
    gx, gy = nx * rs + 1, ny * rs + 1
    # GB is the final coarse mesh height used by main.js. G is the earlier
    # source surface and would report seams that are not present in the view.
    g = decode(d.get("GB", d["G"]), np.float32).reshape(gy, gx)
    coarse = triangulated_at_fine(g, nx, ny, rs, FS_OUT)
    actual = coarse.copy()
    fw = d["FW"]
    vids = decode(fw["vid"], np.uint32)
    fh = decode(fw["h"], np.float32)
    actual.ravel()[vids] = fh

    band = np.zeros((ny, nx), dtype=bool)
    band.flat[decode(fw["band"], np.uint32)] = True
    bc = np.repeat(np.repeat(band, FS_OUT, axis=0), FS_OUT, axis=1)
    bv = np.zeros((ny * FS_OUT + 1, nx * FS_OUT + 1), dtype=bool)
    bv[:-1, :-1] |= bc
    bv[1:, :-1] |= bc
    bv[:-1, 1:] |= bc
    bv[1:, 1:] |= bc
    bdist = ndi.distance_transform_edt(bv) / FS_OUT
    b_interior = bv & (bdist >= 0.75)

    # Mark vertices lying on an actual fine-band/non-band cell edge. This
    # isolates a geometric T-joint from nearby wall relief and shading.
    boundary = np.zeros_like(bv)
    boundary[1:-1, :-1] |= bc[:-1, :] ^ bc[1:, :]
    boundary[:-1, 1:-1] |= bc[:, :-1] ^ bc[:, 1:]
    seam_delta = np.abs(actual - coarse)

    coarse_s, coarse_r = wall_normals(coarse, 1.0 / FS_OUT)
    actual_s, actual_r = wall_normals(actual, 1.0 / FS_OUT)
    coarse_wall = (coarse_s > 1.0)
    actual_wall = (actual_s > 1.0)
    fine_wall = actual_wall & bv

    # Remove water from the wall candidate set. WV uses the same 0.5 m grid;
    # nearest-cell expansion only classifies samples and does not alter data.
    wv = decode(d["WV"], np.float32).reshape(gy, gx)
    water = np.repeat(np.repeat(wv[:-1, :-1] > -900, FS_OUT // rs, axis=0),
                      FS_OUT // rs, axis=1)
    water = np.pad(water, ((0, 1), (0, 1)), mode="edge")
    coarse_wall &= ~water
    actual_wall &= ~water
    fine_wall &= ~water

    tiles = {}
    for zt in range((ny + 42) // 43):
        for xt in range((nx + 41) // 42):
            name = "ABCDEFGH"[xt] + str(zt + 1)
            sl = field_slices(nx, ny, FS_OUT, xt, zt)
            tiles[name] = measure_field(name, sl, coarse_r, actual_r, actual_r,
                                        coarse_wall, actual_wall, fine_wall,
                                        bv, b_interior, seam_delta, boundary)

    summe = sum(x["treffer"] for x in tiles.values())
    out = {"regel": "R9s_wandstreifen", "summe": summe, "je_kachel": tiles,
           "definition": {"abstand_m": "0,25-m-Stichprobe; Wandneigung >1",
                          "treffer": "Normalenrichtung periodisch korreliert, RMS-Amplitude >10 Grad, Periode 0,25 bis <2 m",
                          "raster_gegenprobe": "GB allein, als Renderer-Dreiecke auf 0,25 m abgetastet",
                          "feinband_innen": "gespeicherte FW-Hoehen, mindestens 0,75 m vom Bandrand",
                          "naht": "FW-Hoehe gegen exakte Grobdreieck-Interpolation an Bandrandpunkten"}}
    txt = json.dumps(out, ensure_ascii=False, separators=(",", ":"))
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print(json.dumps({"summe": summe,
                      "raster_gegenprobe": sum(bool(x["raster_gegenprobe"] and x["raster_gegenprobe"]["treffer"]) for x in tiles.values()),
                      "feinband_innen": sum(bool(x["feinband_innen"] and x["feinband_innen"]["treffer"]) for x in tiles.values()),
                      "tatsaechliches_netz": sum(bool(x["tatsaechliches_netz"] and x["tatsaechliches_netz"]["treffer"]) for x in tiles.values()),
                      "D1": tiles.get("D1"), "G1": tiles.get("G1")}, ensure_ascii=False))
    return 1 if summe else 0


if __name__ == "__main__":
    sys.exit(main())
