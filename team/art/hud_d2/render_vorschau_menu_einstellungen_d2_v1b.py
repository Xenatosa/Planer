#!/usr/bin/env python3
"""Render the D2 settings overview and account screen at 576x1024."""
from __future__ import annotations

from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
SRC = HERE / "_src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
import render_vorschau_menu_quests_d2_v2 as d2  # noqa: E402


OUT_MAIN = HERE / "vorschau_menu_einstellungen_d2_v1b.png"
OUT_ACCOUNT = HERE / "vorschau_menu_einstellungen_d2_v1b_konto.png"
OUT_SIZE = (576, 1024)
PANEL = (14, 304, 1052, 1372)

C_TEXT = (243, 231, 207, 255)
C_SOFT = (214, 199, 166, 255)
C_MUTED = (185, 169, 136, 255)
C_GOLD = (255, 217, 168, 255)
C_ORANGE = (255, 138, 42, 255)
C_RED = (233, 76, 55, 255)
C_LINE = (188, 137, 86, 112)


def font(path: Path, size: int, weight: int = 800) -> ImageFont.FreeTypeFont:
    return d2.font(path, size, weight)


def text(base: Image.Image, xy: tuple[int, int], value: str, size: int,
         color=C_TEXT, *, lilita: bool = False, anchor: str | None = None,
         stroke: bool = False) -> None:
    face = font(d2.FONT_LILITA if lilita else d2.FONT_BALOO, size, 800)
    ImageDraw.Draw(base, "RGBA").text(
        xy, value, font=face, fill=color, anchor=anchor,
        stroke_width=1 if stroke else 0,
        stroke_fill=(19, 10, 7, 185) if stroke else None,
    )


def fit_text(base: Image.Image, xy: tuple[int, int], value: str, width: int,
             size: int, color=C_TEXT, *, lilita: bool = False,
             minimum: int = 15, anchor: str | None = None,
             stroke: bool = False) -> None:
    path = d2.FONT_LILITA if lilita else d2.FONT_BALOO
    face = font(path, size, 800)
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    while probe.textbbox((0, 0), value, font=face)[2] > width and face.size > minimum:
        face = font(path, face.size - 1, 800)
    ImageDraw.Draw(base, "RGBA").text(
        xy, value, font=face, fill=color, anchor=anchor,
        stroke_width=1 if stroke else 0,
        stroke_fill=(19, 10, 7, 185) if stroke else None,
    )


def draw_header(base: Image.Image, title: str, subtitle: str,
                *, account: bool = False) -> None:
    x, y, w, _ = PANEL
    back = (x + 24, y + 12, 78, 78)
    d2.draw_gradient(base, back, (65, 47, 34), (24, 17, 13), 20,
                     outline=(202, 150, 93, 205), outline_width=2)
    base.alpha_composite(d2.icon("d2_ico_zurueck", (42, 42)),
                         (back[0] + 18, back[1] + 18))
    fit_text(base, (x + 126, y + 5), title, w - 275, 56,
             (255, 231, 193, 255), lilita=True, minimum=38, stroke=True)
    fit_text(base, (x + 130, y + 61), subtitle, w - 300, 22,
             C_MUTED, minimum=16)

    seal = (x + w - 106, y + 14, 72, 72)
    d2.draw_gradient(base, seal, (80, 45, 24), (22, 15, 11), 21,
                     outline=(221, 157, 86, 165), outline_width=2)
    cx, cy = seal[0] + 36, seal[1] + 36
    draw = ImageDraw.Draw(base, "RGBA")
    if account:
        draw.ellipse((cx - 12, cy - 17, cx + 12, cy + 7),
                     outline=(255, 224, 181, 255), width=3)
        draw.arc((cx - 22, cy + 2, cx + 22, cy + 34), 195, 345,
                 fill=(255, 224, 181, 255), width=4)
    else:
        for offset, knob in ((-14, -8), (0, 8), (14, -3)):
            yy = cy + offset
            draw.line((cx - 19, yy, cx + 19, yy),
                      fill=(236, 191, 132, 220), width=3)
            draw.ellipse((cx + knob - 4, yy - 5, cx + knob + 4, yy + 5),
                         fill=(255, 216, 160, 255),
                         outline=(49, 27, 16, 255), width=1)


def section_heading(base: Image.Image, y: int, label: str) -> None:
    heading = label.upper()
    text(base, (52, y), heading, 25, (255, 205, 145, 255), lilita=True)
    draw = ImageDraw.Draw(base, "RGBA")
    face = font(d2.FONT_LILITA, 25, 800)
    text_right = 52 + draw.textbbox((0, 0), heading, font=face)[2]
    line_x = text_right + 10
    if line_x < 1028:
        draw.line((line_x, y + 16, 1028, y + 16),
                  fill=(186, 123, 67, 110), width=2)


def row_rule(base: Image.Image, y: int) -> None:
    ImageDraw.Draw(base, "RGBA").line((66, y + 53, 1014, y + 53),
                                       fill=(185, 150, 111, 52), width=1)


def row_label(base: Image.Image, y: int, label: str) -> None:
    fit_text(base, (70, y + 27), label, 390, 27, C_TEXT,
             lilita=False, minimum=20, anchor="lm")


def draw_slider(base: Image.Image, x: int, cy: int, width: int,
                value: float) -> None:
    draw = ImageDraw.Draw(base, "RGBA")
    track_h = 11
    draw.rounded_rectangle((x, cy - track_h // 2, x + width, cy + track_h // 2),
                           6, fill=(37, 29, 23, 255),
                           outline=(135, 97, 62, 190), width=2)
    fill_w = round((width - 6) * value)
    if fill_w > 0:
        draw.rounded_rectangle((x + 3, cy - 3, x + 3 + fill_w, cy + 3),
                               4, fill=(231, 119, 43, 255))
    knob_x = x + 3 + fill_w
    draw.ellipse((knob_x - 13, cy - 13, knob_x + 13, cy + 13),
                 fill=(255, 220, 166, 255),
                 outline=(98, 49, 24, 255), width=3)
    draw.ellipse((knob_x - 6, cy - 6, knob_x + 6, cy + 6),
                 fill=(244, 138, 51, 255))


def draw_toggle(base: Image.Image, x: int, cy: int, enabled: bool) -> None:
    width, height = 110, 38
    box = (x, cy - height // 2, width, height)
    top, bottom = ((123, 63, 30), (46, 27, 18)) if enabled else ((53, 45, 36), (24, 21, 18))
    outline = (247, 158, 83, 200) if enabled else (140, 120, 94, 145)
    d2.draw_gradient(base, box, top, bottom, height // 2,
                     outline=outline, outline_width=2)
    draw = ImageDraw.Draw(base, "RGBA")
    knob_x = x + (width - 22 if enabled else 22)
    draw.ellipse((knob_x - 14, cy - 14, knob_x + 14, cy + 14),
                 fill=(255, 220, 168, 255) if enabled else (169, 151, 125, 255),
                 outline=(37, 23, 16, 255), width=2)
    text(base, (x + (32 if enabled else 77), cy),
         "AUS" if not enabled else "EIN", 17,
         C_MUTED if not enabled else C_GOLD,
         lilita=True, anchor="mm")


def draw_segments(base: Image.Image, x: int, cy: int, width: int,
                  labels: tuple[str, ...], active: int) -> None:
    height = 42
    y = cy - height // 2
    d2.draw_gradient(base, (x, y, width, height), (35, 27, 21), (15, 12, 10),
                     height // 2, outline=(155, 116, 77, 160), outline_width=2)
    segment_w = width / len(labels)
    draw = ImageDraw.Draw(base, "RGBA")
    for idx, label in enumerate(labels):
        sx = round(x + idx * segment_w)
        ex = round(x + (idx + 1) * segment_w)
        if idx == active:
            d2.draw_gradient(base, (sx + 2, y + 2, ex - sx - 4, height - 4),
                             (121, 62, 31), (54, 30, 19), height // 2 - 3,
                             outline=(246, 170, 93, 190), outline_width=2)
        elif idx:
            draw.line((sx, y + 9, sx, y + height - 9),
                      fill=(157, 121, 83, 100), width=1)
        text(base, ((sx + ex) // 2, cy), label, 21,
             C_GOLD if idx == active else C_SOFT,
             lilita=True, anchor="mm")


def draw_action_row(base: Image.Image, y: int, label: str,
                    *, primary: bool = False) -> None:
    x, w, h = 52, 976, 48
    top, bottom = ((83, 47, 27), (28, 18, 14)) if primary else ((53, 39, 29), (20, 15, 12))
    outline = (238, 166, 96, 190) if primary else (167, 121, 77, 145)
    d2.draw_gradient(base, (x, y, w, h), top, bottom, 14,
                     outline=outline, outline_width=2)
    fit_text(base, (x + 28, y + h // 2), label, w - 100, 25,
             C_TEXT, lilita=True, minimum=19, anchor="lm")
    # Small inset chevron: both strokes stay well inside the button bounds.
    draw = ImageDraw.Draw(base, "RGBA")
    cx, cy = x + w - 30, y + h // 2
    draw.line((cx - 6, cy - 8, cx + 2, cy), fill=(237, 194, 139, 255), width=3)
    draw.line((cx + 2, cy, cx - 6, cy + 8), fill=(237, 194, 139, 255), width=3)


def draw_settings() -> Image.Image:
    base = d2.draw_base()
    d2.draw_outer_panel(base, PANEL)
    draw_header(base, "EINSTELLUNGEN", "SPIEL · AUDIO · BARRIEREFREIHEIT")

    # The menu is a single vertical list; controls align to the right edge of each row.
    section_heading(base, 408, "Audio")
    audio_rows = ((440, "Musik"), (492, "Effekte"), (544, "Sprachlautstärke"))
    for (y, label), amount in zip(audio_rows, (0.72, 0.84, 0.61)):
        row_label(base, y, label)
        draw_slider(base, 478, y + 27, 505, amount)
        row_rule(base, y)
    row_label(base, 596, "Stumm-Schalter")
    draw_toggle(base, 873, 623, False)
    row_rule(base, 596)

    section_heading(base, 662, "Grafik")
    row_label(base, 694, "Qualität")
    draw_segments(base, 613, 721, 392, ("NIEDRIG", "MITTEL", "HOCH"), 1)
    row_rule(base, 694)
    row_label(base, 746, "Bildrate")
    draw_segments(base, 743, 773, 262, ("30 FPS", "60 FPS"), 1)
    row_rule(base, 746)
    row_label(base, 798, "Energiesparen")
    draw_toggle(base, 873, 825, False)
    row_rule(base, 798)

    section_heading(base, 864, "Benachrichtigungen")
    for y, label, active in ((896, "Event-Start", True),
                             (948, "Produktion voll", True),
                             (1000, "Gilde", True)):
        row_label(base, y, label)
        draw_toggle(base, 873, y + 27, active)
        row_rule(base, y)

    section_heading(base, 1066, "Sprache")
    row_label(base, 1098, "Anzeigesprache")
    draw_segments(base, 659, 1125, 346, ("DEUTSCH", "ENGLISH"), 0)
    row_rule(base, 1098)

    section_heading(base, 1164, "Steuerung & Barrierefreiheit")
    row_label(base, 1196, "Textgröße")
    draw_slider(base, 608, 1223, 375, 0.53)
    row_rule(base, 1196)
    row_label(base, 1248, "Vibration")
    draw_toggle(base, 873, 1275, True)
    row_rule(base, 1248)

    section_heading(base, 1324, "Konto & Informationen")
    for y, label, primary in (
        (1356, "Konto", True),
        (1408, "Support / Hilfe", False),
        (1460, "Datenschutz", False),
        (1512, "Nutzungsbedingungen", False),
    ):
        draw_action_row(base, y, label, primary=primary)
    ImageDraw.Draw(base, "RGBA").line((246, 1575, 834, 1575),
                                       fill=(166, 121, 79, 95), width=1)
    text(base, (540, 1597), "EPODARIEN  ·  VERSION 1", 19, C_MUTED,
         lilita=True, anchor="mm")
    return base.resize(OUT_SIZE, Image.Resampling.LANCZOS)


def draw_identity_card(base: Image.Image, dy: int = 0) -> None:
    x, y, w, h = 52, 426 + dy, 976, 205
    d2.paste_9(base, "d2_listenkarte_neutral", (x, y, w, h), (12, 8, 8, 8))
    d2.draw_gradient(base, (x + 8, y + 7, w - 16, h - 14),
                     (49, 34, 24), (19, 14, 11), 16,
                     outline=(235, 176, 111, 105), outline_width=1)
    badge = (x + 23, y + 27, 144, 144)
    d2.draw_gradient(base, badge, (104, 56, 29), (25, 16, 12), 35,
                     outline=(235, 171, 97, 200), outline_width=3)
    # Hand-drawn player crest, contained by its round bezel.
    cx, cy = badge[0] + badge[2] // 2, badge[1] + badge[3] // 2
    draw = ImageDraw.Draw(base, "RGBA")
    draw.polygon(((cx, cy - 44), (cx + 36, cy - 22), (cx + 29, cy + 24),
                  (cx, cy + 47), (cx - 29, cy + 24), (cx - 36, cy - 22)),
                 fill=(55, 29, 17, 255), outline=(246, 186, 112, 255))
    draw.line((cx, cy - 30, cx, cy + 32), fill=(231, 153, 74, 255), width=4)
    draw.line((cx - 20, cy - 12, cx + 20, cy - 12), fill=(231, 153, 74, 255), width=4)
    draw.line((cx - 17, cy + 8, cx + 17, cy + 8), fill=(231, 153, 74, 255), width=4)

    tx = x + 195
    text(base, (tx, y + 37), "SPIELER-ID", 22, (255, 187, 111, 255), lilita=True)
    fit_text(base, (tx, y + 81), "EP-7F3A-92D1", 500, 37,
             (255, 241, 215, 255), lilita=True, minimum=29, stroke=True)
    text(base, (tx, y + 137), "Persönliche Kennung", 21, C_MUTED)

    bx, by, bw, bh = x + w - 190, y + 72, 163, 62
    d2.draw_gradient(base, (bx, by, bw, bh), (74, 49, 32), (27, 19, 14), 15,
                     outline=(199, 147, 93, 185), outline_width=2)
    # Copy symbol is two overlapping sheets with an inset margin.
    draw = ImageDraw.Draw(base, "RGBA")
    draw.rounded_rectangle((bx + 22, by + 18, bx + 48, by + 47), 4,
                           outline=(255, 224, 180, 255), width=3)
    draw.rounded_rectangle((bx + 31, by + 11, bx + 57, by + 40), 4,
                           outline=(255, 224, 180, 255), width=3)
    text(base, (bx + 105, by + 31), "KOPIEREN", 17, C_GOLD,
         lilita=True, anchor="mm")


def draw_google_card(base: Image.Image, dy: int = 0) -> None:
    x, y, w, h = 52, 668 + dy, 976, 260
    d2.paste_9(base, "d2_listenkarte_neutral", (x, y, w, h), (12, 8, 8, 8))
    d2.draw_gradient(base, (x + 8, y + 7, w - 16, h - 14),
                     (47, 32, 23), (18, 13, 11), 16,
                     outline=(218, 157, 96, 86), outline_width=1)
    gx, gy = x + 83, y + 77
    draw = ImageDraw.Draw(base, "RGBA")
    draw.ellipse((gx - 43, gy - 43, gx + 43, gy + 43),
                 fill=(38, 29, 23, 255), outline=(219, 161, 104, 190), width=3)
    text(base, (gx, gy - 1), "G", 52, (255, 222, 179, 255),
         lilita=True, anchor="mm", stroke=True)

    text(base, (x + 151, y + 43), "GOOGLE PLAY GAMES", 22,
         (255, 190, 119, 255), lilita=True)
    fit_text(base, (x + 151, y + 78), "Konto verknüpfen", 650, 33,
             (255, 241, 215, 255), lilita=True, minimum=25, stroke=True)
    fit_text(base, (x + 151, y + 121), "Spielfortschritt mit Google Play Games sichern.",
             700, 23, C_SOFT, minimum=18)
    bx, by, bw, bh = x + 151, y + 172, 340, 58
    d2.draw_gradient(base, (bx, by, bw, bh), (128, 64, 29), (51, 28, 18), 16,
                     outline=(255, 183, 106, 210), outline_width=2)
    text(base, (bx + bw // 2, by + bh // 2), "KONTO VERKNÜPFEN", 22,
         C_TEXT, lilita=True, anchor="mm")


def draw_server_row(base: Image.Image, dy: int = 0) -> None:
    x, y, w, h = 52, 968 + dy, 976, 158
    d2.paste_9(base, "d2_listenkarte_neutral", (x, y, w, h), (12, 8, 8, 8))
    d2.draw_gradient(base, (x + 8, y + 7, w - 16, h - 14),
                     (44, 31, 23), (17, 13, 11), 15,
                     outline=(210, 154, 98, 78), outline_width=1)
    sx, sy = x + 94, y + 79
    draw = ImageDraw.Draw(base, "RGBA")
    draw.ellipse((sx - 40, sy - 40, sx + 40, sy + 40),
                 fill=(42, 29, 21, 255), outline=(204, 148, 90, 175), width=2)
    draw.ellipse((sx - 20, sy - 31, sx + 20, sy + 31),
                 outline=(244, 197, 139, 220), width=2)
    draw.arc((sx - 31, sy - 17, sx + 31, sy + 17), 0, 180,
             fill=(244, 197, 139, 220), width=2)
    draw.arc((sx - 31, sy - 17, sx + 31, sy + 17), 180, 360,
             fill=(244, 197, 139, 220), width=2)
    draw.line((sx - 33, sy, sx + 33, sy), fill=(244, 197, 139, 220), width=2)
    text(base, (x + 158, y + 41), "SERVERREGION", 21,
         (255, 190, 119, 255), lilita=True)
    text(base, (x + 158, y + 76), "EUROPA", 32, (255, 241, 215, 255),
         lilita=True, stroke=True)
    fit_text(base, (x + 158, y + 117), "Server 1 · Europa-West", 19,
             19, C_MUTED, minimum=16)
    d2.draw_gradient(base, (x + w - 178, y + 51, 139, 54),
                     (60, 43, 29), (23, 17, 13), 16,
                     outline=(175, 130, 82, 110), outline_width=1)
    text(base, (x + w - 108, y + 78), "AKTIV", 19, C_GOLD,
         lilita=True, anchor="mm")


def draw_logout(base: Image.Image, dy: int = 0) -> None:
    x, y, w, h = 52, 1172 + dy, 976, 82
    d2.draw_gradient(base, (x, y, w, h), (61, 42, 29), (23, 17, 13), 17,
                     outline=(182, 129, 79, 180), outline_width=2)
    text(base, (x + w // 2, y + h // 2), "ABMELDEN", 26, C_TEXT,
         lilita=True, anchor="mm")
    # Exit glyph, drawn inside the left inset.
    draw = ImageDraw.Draw(base, "RGBA")
    gx, gy = x + 66, y + h // 2
    draw.line((gx - 15, gy, gx + 11, gy), fill=(240, 193, 135, 255), width=4)
    draw.line((gx + 2, gy - 9, gx + 12, gy, gx + 2, gy + 9),
              fill=(240, 193, 135, 255), width=4, joint="curve")


def draw_delete_card(base: Image.Image, dy: int = 0) -> None:
    x, y, w, h = 52, 1292 + dy, 976, 296
    d2.draw_gradient(base, (x, y, w, h), (73, 30, 23), (24, 13, 11), 20,
                     outline=(214, 76, 57, 205), outline_width=3)
    d2.draw_gradient(base, (x + 8, y + 8, w - 16, h - 16),
                     (50, 23, 19), (18, 11, 10), 16,
                     outline=(248, 108, 76, 80), outline_width=1)
    draw = ImageDraw.Draw(base, "RGBA")
    # Warning medallion and exclamation remain within the red framed danger area.
    mx, my = x + 68, y + 73
    draw.ellipse((mx - 30, my - 30, mx + 30, my + 30),
                 fill=(94, 34, 27, 255), outline=(255, 132, 95, 210), width=2)
    draw.line((mx, my - 15, mx, my + 5), fill=(255, 217, 189, 255), width=5)
    draw.ellipse((mx - 3, my + 13, mx + 3, my + 19), fill=(255, 217, 189, 255))
    text(base, (x + 120, y + 57), "KONTO LÖSCHEN", 25,
         (255, 144, 121, 255), lilita=True)
    fit_text(base, (x + 120, y + 99),
             "Die Kontolöschung ist dauerhaft und kann nicht rückgängig gemacht werden.",
             800, 21, (246, 182, 164, 255), minimum=16)
    fit_text(base, (x + 120, y + 135), "Bitte prüfe deine Entscheidung sorgfältig.",
             800, 20, (212, 157, 143, 255), minimum=16)
    bx, by, bw, bh = x + 120, y + 190, 774, 66
    d2.draw_gradient(base, (bx, by, bw, bh), (150, 48, 38), (78, 22, 20), 15,
                     outline=(255, 140, 115, 220), outline_width=2)
    text(base, (bx + bw // 2, by + bh // 2), "KONTO LÖSCHEN", 24,
         (255, 241, 232, 255), lilita=True, anchor="mm")


def draw_account() -> Image.Image:
    base = d2.draw_base()
    d2.draw_outer_panel(base, PANEL)
    draw_header(base, "KONTO", "SPIELERDATEN · VERKNÜPFUNG", account=True)
    dy = 17
    section_heading(base, 391 + dy, "Spielerkennung")
    draw_identity_card(base, dy)
    section_heading(base, 646 + dy, "Verknüpfung")
    draw_google_card(base, dy)
    section_heading(base, 944 + dy, "Server")
    draw_server_row(base, dy)
    draw_logout(base, dy)
    draw_delete_card(base, dy)
    return base.resize(OUT_SIZE, Image.Resampling.LANCZOS)


def main() -> None:
    draw_settings().save(OUT_MAIN, optimize=True)
    draw_account().save(OUT_ACCOUNT, optimize=True)
    print(f"Wrote {OUT_MAIN}")
    print(f"Wrote {OUT_ACCOUNT}")


if __name__ == "__main__":
    main()
