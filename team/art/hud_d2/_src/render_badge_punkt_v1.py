#!/usr/bin/env python3
"""Render the D2 notification dot and its HUD preview with Pillow only."""
from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
MASTER_SIZE = 256
BADGE_PATH = ROOT / "icons_v1" / "d2_ico_badge_punkt.png"
PREVIEW_PATH = ROOT / "vorschau_badge_punkt_v1.png"
HUD_BG = (26, 18, 12)
OUTLINE = (26, 18, 12)

DOCK_SAMPLES = (
    ("d2_ico_dock_helden.png", "Helden"),
    ("d2_ico_dock_karte.png", "Karte"),
    ("d2_ico_dock_armee.png", "Armee"),
    ("d2_ico_dock_inventar.png", "Inventar"),
)


def polygon_for_blob(
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    inset: float,
) -> list[tuple[int, int]]:
    """Return a gently irregular, near-circular ember contour."""
    points: list[tuple[int, int]] = []
    steps = 192
    for i in range(steps):
        angle = 2 * math.pi * i / steps
        wobble = (
            0.010 * math.sin(3 * angle + 0.55)
            + 0.006 * math.sin(5 * angle + 1.80)
            + 0.003 * math.sin(8 * angle - 0.40)
        )
        x = cx + math.cos(angle) * (rx - inset) * (1.0 + wobble)
        y = cy + math.sin(angle) * (ry - inset) * (1.0 + wobble)
        points.append((round(x), round(y)))
    return points


def color_lut(stops: tuple[tuple[int, tuple[int, int, int]], ...]) -> list[int]:
    lut: list[int] = []
    for value in range(256):
        lower = stops[0]
        upper = stops[-1]
        for i in range(len(stops) - 1):
            if stops[i][0] <= value <= stops[i + 1][0]:
                lower, upper = stops[i], stops[i + 1]
                break
        span = max(1, upper[0] - lower[0])
        t = (value - lower[0]) / span
        lut.extend(
            round(lower[1][channel] * (1 - t) + upper[1][channel] * t)
            for channel in range(3)
        )
    return lut


def ember_gradient(size: int, supersample: int, center: tuple[int, int]) -> Image.Image:
    """Build a warm radial fill with a pale, top-left lit core."""
    canvas_size = size * supersample
    cx, cy = center
    radius = round(108 * supersample)
    # Pillow's radial gradient is resized so that its falloff reaches the
    # ember edge, rather than filling the whole 256 px canvas.
    grad_diameter = radius * 2
    gradient = Image.radial_gradient("L").resize(
        (grad_diameter, grad_diameter), Image.Resampling.LANCZOS
    )
    field = Image.new("L", (canvas_size, canvas_size), 0)
    hot_x = round(cx - 8 * supersample)
    hot_y = round(cy - 10 * supersample)
    field.paste(gradient, (hot_x - radius, hot_y - radius))
    field = ImageOps.invert(field)
    lut = color_lut(
        (
            (0, (137, 39, 15)),
            (24, (176, 47, 15)),
            (54, (220, 63, 16)),
            (92, (245, 91, 21)),
            (132, (255, 133, 31)),
            (174, (255, 177, 61)),
            (215, (255, 218, 125)),
            (246, (255, 239, 187)),
            (255, (255, 248, 220)),
        )
    )
    indexed = field.convert("P")
    indexed.putpalette(lut)
    return indexed.convert("RGB")


def render_badge(size: int = MASTER_SIZE) -> Image.Image:
    """Create a transparent 256 px ember point with a compact dark outline."""
    supersample = 4
    s = size / MASTER_SIZE * supersample
    canvas_size = round(size * supersample)
    cx = cy = canvas_size / 2
    rx, ry = 106 * s, 108 * s

    outer = Image.new("L", (canvas_size, canvas_size), 0)
    ImageDraw.Draw(outer).polygon(
        polygon_for_blob(cx, cy, rx, ry, 0), fill=255
    )
    rim = Image.new("L", (canvas_size, canvas_size), 0)
    ImageDraw.Draw(rim).polygon(
        polygon_for_blob(cx, cy, rx, ry, 15 * s), fill=255
    )
    interior = Image.new("L", (canvas_size, canvas_size), 0)
    ImageDraw.Draw(interior).polygon(
        polygon_for_blob(cx, cy, rx, ry, 24 * s), fill=255
    )

    art = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    dark = Image.new("RGBA", art.size, (*OUTLINE, 255))
    art.paste(dark, (0, 0), outer)
    warm_rim = Image.new("RGBA", art.size, (133, 43, 18, 255))
    art.paste(warm_rim, (0, 0), rim)

    gradient = ember_gradient(canvas_size // supersample, supersample, (cx, cy))
    fill = Image.new("RGBA", art.size, (0, 0, 0, 0))
    fill_rgb = gradient.resize(art.size, Image.Resampling.LANCZOS)
    fill.paste(fill_rgb, (0, 0), interior)
    art.alpha_composite(fill)

    # A restrained cream glint reinforces the light source without adding
    # detail that would disappear at the 24 px HUD size.
    glint = Image.new("RGBA", art.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glint)
    gx = round((cx / supersample - 26) * supersample)
    gy = round((cy / supersample - 34) * supersample)
    gd.ellipse((gx - 10 * s, gy - 4 * s, gx + 10 * s, gy + 4 * s),
               fill=(255, 242, 195, 190))
    glint.putalpha(ImageChopsMultiply(glint.getchannel("A"), interior))
    art.alpha_composite(glint)

    return art.resize((size, size), Image.Resampling.LANCZOS)


def ImageChopsMultiply(first: Image.Image, second: Image.Image) -> Image.Image:
    """Small local helper to keep the renderer's imports limited to Pillow."""
    from PIL import ImageChops

    return ImageChops.multiply(first, second)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    paths = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    )
    try:
        return ImageFont.truetype(paths, size)
    except OSError:
        return ImageFont.load_default()


def find_icon_dir(explicit: Path | None) -> Path:
    required = {name for name, _label in DOCK_SAMPLES}
    candidates: list[Path] = []
    if explicit is not None:
        candidates.append(explicit.expanduser().resolve())
    candidates.append(ROOT / "icons_v1")
    workspace = ROOT.parents[3]
    candidates.extend(sorted(workspace.glob("*/team/art/hud_d2/icons_v1")))
    for candidate in candidates:
        if all((candidate / name).is_file() for name in required):
            return candidate
    expected = ", ".join(sorted(required))
    raise FileNotFoundError(
        "Dock-Master nicht gefunden. Bitte --source-dir auf icons_v1 setzen; "
        f"benötigt werden: {expected}"
    )


def rounded_panel(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    draw.rounded_rectangle(box, radius=18, fill=(26, 18, 12), outline=(76, 55, 38), width=2)
    x1, y1, x2, _y2 = box
    draw.rounded_rectangle((x1 + 2, y1 + 2, x2 - 2, y1 + 7), radius=4,
                           fill=(112, 64, 32))


def compose_sample(master: Image.Image, badge: Image.Image) -> Image.Image:
    icon = master.convert("RGBA").resize((96, 96), Image.Resampling.LANCZOS)
    sample = Image.new("RGBA", (96, 96), (*HUD_BG, 255))
    sample.alpha_composite(icon)
    badge_24 = badge.resize((24, 24), Image.Resampling.LANCZOS)
    sample.alpha_composite(badge_24, (70, 1))
    return sample


def render_preview(badge: Image.Image, icons_dir: Path) -> Image.Image:
    width, height = 1400, 1010
    canvas = Image.new("RGB", (width, height), (18, 13, 9))
    draw = ImageDraw.Draw(canvas)

    draw.line((40, 146, 1360, 146), fill=(74, 53, 36), width=1)

    draw.text((48, 30), "OBSIDIAN & GLUT  ·  HUD D2", font=font(17, True), fill=(255, 178, 71))
    draw.text((48, 57), "BADGE PUNKT", font=font(36, True), fill=(245, 230, 206))
    draw.text((48, 108), "256 px Master  →  24 px im HUD  ·  prozeduraler PIL-Render",
              font=font(17), fill=(184, 164, 142))

    original_box = (40, 170, 550, 950)
    zoom_box = (574, 170, 1360, 950)
    rounded_panel(draw, original_box)
    rounded_panel(draw, zoom_box)

    draw.text((66, 195), "SPIELGRÖSSE  ·  1:1", font=font(20, True), fill=(245, 230, 206))
    draw.text((66, 226), "Dock-Icon 96 px  ·  Badge 24 px", font=font(15), fill=(177, 156, 133))

    masters: list[tuple[str, str, Image.Image]] = []
    for filename, label in DOCK_SAMPLES:
        with Image.open(icons_dir / filename) as src:
            masters.append((filename, label, src.convert("RGBA")))

    strip = (61, 280, 529, 462)
    draw.rounded_rectangle(strip, radius=14, fill=(20, 14, 10), outline=(61, 45, 32), width=1)
    samples: list[tuple[str, Image.Image]] = []
    for index, (_filename, label, master) in enumerate(masters):
        slot_x = 67 + index * 115
        slot_y = 296
        draw.rounded_rectangle((slot_x, slot_y, slot_x + 108, slot_y + 150), radius=10,
                               fill=(31, 22, 15), outline=(82, 59, 40), width=1)
        sample = compose_sample(master, badge)
        samples.append((label, sample))
        canvas.paste(sample.convert("RGB"), (slot_x + 6, slot_y + 7))
        label_box = draw.textbbox((0, 0), label, font=font(14, True))
        label_width = label_box[2] - label_box[0]
        draw.text((slot_x + (108 - label_width) // 2, slot_y + 111), label,
                  font=font(14, True), fill=(224, 202, 174))

    draw.line((66, 507, 524, 507), fill=(69, 49, 33), width=1)
    draw.text((66, 529), "PUNKT IN ORIGINALGRÖSSE", font=font(15, True), fill=(245, 230, 206))
    draw.text((66, 558), "Glutverlauf · dunkle Outline · heller Kern",
              font=font(14), fill=(177, 156, 133))
    badge_24 = badge.resize((24, 24), Image.Resampling.LANCZOS)
    canvas.paste(badge_24, (475, 550), badge_24)
    draw.line((475, 580, 499, 580), fill=(255, 178, 71), width=1)
    draw.line((475, 576, 475, 584), fill=(255, 178, 71), width=1)
    draw.line((499, 576, 499, 584), fill=(255, 178, 71), width=1)
    draw.text((66, 621), "Transparentes RGBA · 256 × 256 Quelle · LANCZOS-Downscale",
              font=font(13), fill=(145, 126, 108))
    draw.text((66, 653), "Badge-Overlay oben rechts auf vier aktiven Dock-Icons",
              font=font(13), fill=(145, 126, 108))

    draw.text((600, 195), "300 %  ·  AUSSCHNITTE", font=font(20, True), fill=(245, 230, 206))
    draw.text((600, 226), "Jeweils 96 × 96 px Spielausschnitt, dreifach skaliert",
              font=font(15), fill=(177, 156, 133))

    grid_x = (659, 983)
    row_y = (270, 604)
    for index, (label, sample) in enumerate(samples):
        col, row = index % 2, index // 2
        x, y = grid_x[col], row_y[row]
        draw.text((x, y), label.upper(), font=font(14, True), fill=(224, 202, 174))
        zoom = sample.resize((288, 288), Image.Resampling.NEAREST)
        canvas.paste(zoom.convert("RGB"), (x, y + 25))
        draw.rectangle((x - 1, y + 24, x + 288, y + 313), outline=(91, 65, 43), width=1)

    draw.text((48, 974), "HUD-Hintergrund #1A120C  ·  Punktquelle procedural mit Python/PIL",
              font=font(13), fill=(145, 126, 108))
    return canvas


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-dir", type=Path, default=None,
        help="Ordner mit den 256×256 Dock-Mastern für die Vorschau (default: automatisch suchen).",
    )
    parser.add_argument("--icon-out", type=Path, default=BADGE_PATH)
    parser.add_argument("--preview-out", type=Path, default=PREVIEW_PATH)
    args = parser.parse_args()

    icons_dir = find_icon_dir(args.source_dir)
    badge = render_badge()
    args.icon_out.parent.mkdir(parents=True, exist_ok=True)
    args.preview_out.parent.mkdir(parents=True, exist_ok=True)
    badge.save(args.icon_out, format="PNG", optimize=True)
    preview = render_preview(badge, icons_dir)
    preview.save(args.preview_out, format="PNG", optimize=True)
    print(f"badge:   {args.icon_out} ({badge.size[0]}×{badge.size[1]} RGBA)")
    print(f"preview: {args.preview_out} ({preview.size[0]}×{preview.size[1]} RGB)")
    print(f"sources: {icons_dir}")


if __name__ == "__main__":
    main()
