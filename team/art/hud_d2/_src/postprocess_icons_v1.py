#!/usr/bin/env python3
"""Freistellen all raws, derive inactive, build overview, write icons_v1.md."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path("/workspace/handygame-plan/team/art/hud_d2")
OUT = ROOT / "icons_v1"
RAW = OUT / "_raw"
FREI = ROOT / "_src" / "freistell_magenta_icon.py"
DERIVE = ROOT / "_src" / "derive_dock_inaktiv.py"

INACTIVE = {
    "d2_ico_dock_dorf_inaktiv.png": "d2_ico_dock_dorf.png",
    "d2_ico_dock_helden_inaktiv.png": "d2_ico_dock_helden.png",
    "d2_ico_dock_karte_inaktiv.png": "d2_ico_dock_karte.png",
    "d2_ico_dock_armee_inaktiv.png": "d2_ico_dock_armee.png",
    "d2_ico_dock_gilde_inaktiv.png": "d2_ico_dock_gilde.png",
    "d2_ico_dock_inventar_inaktiv.png": "d2_ico_dock_inventar.png",
}

def freistell_raws():
    results = []
    for raw in sorted(RAW.glob("*_raw.png")):
        asset = raw.name.replace("_raw.png", "")
        dst = OUT / f"{asset}.png"
        if dst.exists() and dst.stat().st_mtime >= raw.stat().st_mtime:
            # already processed unless forced
            pass
        r = subprocess.run([sys.executable, str(FREI), str(raw), str(dst)], capture_output=True, text=True)
        results.append((asset, r.returncode, r.stdout.strip(), r.stderr.strip()))
        print(asset, "rc", r.returncode, r.stdout.strip()[:120])
    return results

def derive_inactive():
    for dst_name, src_name in INACTIVE.items():
        src = OUT / src_name
        dst = OUT / dst_name
        if not src.exists():
            print("SKIP inactive, missing active:", src_name)
            continue
        subprocess.check_call([sys.executable, str(DERIVE), str(src), str(dst)])

def qa():
    problems = []
    masters = sorted(OUT.glob("d2_ico_*.png"))
    for p in masters:
        a = np.array(Image.open(p).convert("RGBA"))
        if a.shape[:2] != (256, 256):
            problems.append(f"{p.name}: size {a.shape[:2]}")
        corners = [int(a[0,0,3]), int(a[0,-1,3]), int(a[-1,0,3]), int(a[-1,-1,3])]
        if any(c > 5 for c in corners):
            problems.append(f"{p.name}: corner alpha {corners}")
        rgb = a[..., :3].astype(float)
        mag = ((rgb - [255, 0, 255]) ** 2).sum(axis=2) ** 0.5
        left = int(((a[..., 3] > 20) & (mag < 60)).sum())
        if left:
            problems.append(f"{p.name}: magenta leftovers {left}px")
        opaque = int((a[..., 3] > 20).sum())
        if opaque < 2000:
            problems.append(f"{p.name}: very sparse opaque={opaque}")
    return masters, problems

def overview(masters):
    # grid ~10 cols
    cols = 10
    cell, gap, pad = 128, 8, 16
    n = len(masters)
    rows = (n + cols - 1) // cols
    w = pad * 2 + cols * cell + (cols - 1) * gap
    h = pad * 2 + rows * cell + (rows - 1) * gap
    canvas = Image.new("RGB", (w, h), (0x1A, 0x12, 0x0C))
    for i, p in enumerate(masters):
        r, c = divmod(i, cols)
        im = Image.open(p).convert("RGBA").resize((cell, cell), Image.Resampling.LANCZOS)
        x = pad + c * (cell + gap)
        y = pad + r * (cell + gap)
        canvas.paste(im, (x, y), im)
    out = OUT / "uebersicht_icons_v1.png"
    canvas.save(out)
    print("overview", out, canvas.size)
    return out

if __name__ == "__main__":
    freistell_raws()
    derive_inactive()
    masters, problems = qa()
    overview(sorted(OUT.glob("d2_ico_*.png")))
    print(f"masters={len(list(OUT.glob('d2_ico_*.png')))} problems={len(problems)}")
    for p in problems:
        print("PROBLEM:", p)
    (OUT / "_batch" / "qa_problems.json").write_text(json.dumps(problems, indent=2))
