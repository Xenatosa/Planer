#!/usr/bin/env python3
"""Magenta chroma-key + center with 8% padding onto 256x256 RGBA. SynthID untouched."""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter

OUT_SIZE = 256
PAD_FRAC = 0.08  # 8% margin each side -> subject ~84% of canvas
FEATHER = 1.5
MAGENTA = np.array([255.0, 0.0, 255.0])
# Distance thresholds in RGB for key (tolerant of slight bleed)
SOFT = 55.0
HARD = 95.0


def chroma_key(rgb: np.ndarray) -> np.ndarray:
    """Return alpha 0..255 from magenta distance."""
    d = np.linalg.norm(rgb.astype(np.float32) - MAGENTA, axis=2)
    # Also catch near-magenta (high R+B, low G)
    r, g, b = rgb[..., 0].astype(np.float32), rgb[..., 1].astype(np.float32), rgb[..., 2].astype(np.float32)
    mag_score = np.minimum(r, b) - g
    near = (mag_score > 40) & (g < 80) & (r > 160) & (b > 160)
    d = np.where(near, np.minimum(d, SOFT * 0.5), d)
    alpha = np.clip((d - SOFT) / (HARD - SOFT), 0, 1)
    return (alpha * 255).astype(np.uint8)


def despill(rgb: np.ndarray, alpha: np.ndarray) -> np.ndarray:
    """Pull magenta fringe toward neutral on semi-transparent edge."""
    out = rgb.astype(np.float32).copy()
    edge = (alpha > 10) & (alpha < 245)
    r, g, b = out[..., 0], out[..., 1], out[..., 2]
    # where R and B dominate over G, pull toward mid
    spill = edge & (np.minimum(r, b) > g + 20)
    mid = (r + g + b) / 3.0
    out[..., 0] = np.where(spill, np.minimum(r, mid + (g - mid) * 0.3 + 40), r)
    out[..., 2] = np.where(spill, np.minimum(b, mid + (g - mid) * 0.3 + 40), b)
    # also clamp pure magenta leftovers
    out[..., 0] = np.clip(out[..., 0], 0, 255)
    out[..., 1] = np.clip(out[..., 1], 0, 255)
    out[..., 2] = np.clip(out[..., 2], 0, 255)
    return out.astype(np.uint8)


def center_pad(rgba: Image.Image, size: int = OUT_SIZE, pad: float = PAD_FRAC) -> Image.Image:
    a = np.array(rgba)
    alpha = a[..., 3]
    ys, xs = np.where(alpha > 20)
    if len(xs) == 0:
        return Image.new("RGBA", (size, size), (0, 0, 0, 0))
    x0, x1 = int(xs.min()), int(xs.max()) + 1
    y0, y1 = int(ys.min()), int(ys.max()) + 1
    crop = rgba.crop((x0, y0, x1, y1))
    cw, ch = crop.size
    inner = int(round(size * (1 - 2 * pad)))
    scale = min(inner / cw, inner / ch)
    nw, nh = max(1, int(round(cw * scale))), max(1, int(round(ch * scale)))
    crop = crop.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ox = (size - nw) // 2
    oy = (size - nh) // 2
    canvas.paste(crop, (ox, oy), crop)
    return canvas


def square_center_crop(im: Image.Image) -> Image.Image:
    w, h = im.size
    s = min(w, h)
    left = (w - s) // 2
    top = (h - s) // 2
    return im.crop((left, top, left + s, top + s))


def process(src: Path, dst: Path, crop200: Path | None = None) -> dict:
    im = Image.open(src).convert("RGBA")
    im = square_center_crop(im)
    arr = np.array(im)
    rgb = arr[..., :3]
    alpha = chroma_key(rgb)
    # feather
    a_img = Image.fromarray(alpha, mode="L").filter(ImageFilter.GaussianBlur(radius=FEATHER))
    alpha = np.array(a_img)
    # hard kill near-pure magenta
    d = np.linalg.norm(rgb.astype(np.float32) - MAGENTA, axis=2)
    alpha = np.where(d < 35, 0, alpha).astype(np.uint8)
    rgb2 = despill(rgb, alpha)
    rgba = Image.fromarray(np.dstack([rgb2, alpha]), "RGBA")
    master = center_pad(rgba, OUT_SIZE, PAD_FRAC)
    master.save(dst)
    info = {"src": str(src), "dst": str(dst), "size": master.size, "opaque_px": int(np.sum(np.array(master)[..., 3] > 20))}
    if crop200:
        up = master.resize((512, 512), Image.Resampling.NEAREST)
        up.save(crop200)
        info["crop200"] = str(crop200)
    return info


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: freistell_magenta_icon.py SRC DST [CROP200]")
        sys.exit(2)
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    crop = Path(sys.argv[3]) if len(sys.argv) > 3 else None
    print(process(src, dst, crop))
