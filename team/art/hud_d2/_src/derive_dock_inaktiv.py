#!/usr/bin/env python3
"""Derive dock inactive icons: desaturate ~35%, brightness -20%, dampen ember oranges."""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageEnhance

def dampen_ember(rgb: np.ndarray) -> np.ndarray:
    r, g, b = rgb[...,0].astype(np.float32), rgb[...,1].astype(np.float32), rgb[...,2].astype(np.float32)
    # warm orange-ish pixels: high R, mid G, low B relative
    warm = (r > 140) & (r > g) & (g > b) & ((r - b) > 40)
    # pull toward gray-brown
    gray = 0.3*r + 0.5*g + 0.2*b
    factor = np.where(warm, 0.35, 1.0)[..., None]
    target = np.stack([gray*0.85, gray*0.75, gray*0.65], axis=-1)
    out = rgb.astype(np.float32) * (1 - (1-factor[:,:,0:1])*0)  # placeholder
    # blend warm toward muted
    blend = np.where(warm, 0.75, 0.0)[..., None]
    out = rgb.astype(np.float32) * (1 - blend) + target * blend
    return np.clip(out, 0, 255).astype(np.uint8)

def derive(src: Path, dst: Path) -> None:
    im = Image.open(src).convert("RGBA")
    arr = np.array(im)
    rgb, a = arr[..., :3], arr[..., 3]
    rgb = dampen_ember(rgb)
    # desaturate to ~35% saturation remaining -> enhancer 0.35
    tmp = Image.fromarray(np.dstack([rgb, a]), "RGBA")
    # operate on RGB only
    rgb_im = Image.fromarray(rgb, "RGB")
    rgb_im = ImageEnhance.Color(rgb_im).enhance(0.35)
    rgb_im = ImageEnhance.Brightness(rgb_im).enhance(0.80)
    out = Image.merge("RGBA", (*rgb_im.split(), Image.fromarray(a, "L")))
    out.save(dst)
    print(f"OK {dst}")

if __name__ == "__main__":
    derive(Path(sys.argv[1]), Path(sys.argv[2]))
