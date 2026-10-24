#!/usr/bin/env python3
"""Render D2 Events overview and Stammeswettstreit detail at 576x1024."""
from __future__ import annotations

from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFont


HERE = Path(__file__).resolve().parent
HUD = HERE.parent
sys.path.insert(0, str(HERE))
import render_vorschau_menu_quests_d2_v2 as d2  # noqa: E402


OUT_OVERVIEW = HUD / "vorschau_menu_events_d2_v1.png"
OUT_DETAIL = HUD / "vorschau_menu_events_d2_v1_detail.png"
OUT_SIZE = (576, 1024)
W, H = 1080, 1920
PANEL = (14, 304, 1052, 1372)

C_TEXT = (243, 231, 207, 255)
C_SOFT = (214, 199, 166, 255)
C_MUTED = (185, 169, 136, 255)
C_GOLD = (255, 217, 168, 255)
C_ORANGE = (255, 138, 42, 255)
C_INK = (11, 9, 8, 255)


def font(path: Path, size: int, weight: int = 800) -> ImageFont.FreeTypeFont:
    return d2.font(path, size, weight)


def text_fit(text: str, width: int, size: int, *, lilita: bool = False,
             minimum: int = 16) -> ImageFont.FreeTypeFont:
    path = d2.FONT_LILITA if lilita else d2.FONT_BALOO
    face = font(path, size, 800)
    draw = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    while draw.textbbox((0, 0), text, font=face)[2] > width and face.size > minimum:
        face = font(path, face.size - 1, 800)
    return face


def text(base: Image.Image, xy: tuple[int, int], value: str, size: int,
         color=C_TEXT, *, lilita: bool = False, anchor: str | None = None,
         stroke: bool = False) -> None:
    ImageDraw.Draw(base, "RGBA").text(
        xy, value, font=font(d2.FONT_LILITA if lilita else d2.FONT_BALOO, size, 800),
        fill=color, anchor=anchor,
        stroke_width=1 if stroke else 0,
        stroke_fill=(19, 10, 7, 185) if stroke else None,
    )


def fitted_text(base: Image.Image, xy: tuple[int, int], value: str, width: int,
                size: int, color=C_TEXT, *, lilita: bool = False,
                minimum: int = 16, anchor: str | None = None,
                stroke: bool = False) -> None:
    face = text_fit(value, width, size, lilita=lilita, minimum=minimum)
    ImageDraw.Draw(base, "RGBA").text(
        xy, value, font=face, fill=color, anchor=anchor,
        stroke_width=1 if stroke else 0,
        stroke_fill=(19, 10, 7, 185) if stroke else None,
    )


def draw_header(base: Image.Image, title: str, subtitle: str) -> None:
    x, y, w, _ = PANEL
    back = (x + 24, y + 12, 78, 78)
    d2.draw_gradient(base, back, (65, 47, 34), (24, 17, 13), 20,
                     outline=(202, 150, 93, 205), outline_width=2)
    base.alpha_composite(d2.icon("d2_ico_zurueck", (42, 42)), (back[0] + 18, back[1] + 18))
    fitted_text(base, (x + 126, y + 5), title, w - 275, 58, (255, 231, 193, 255),
                lilita=True, minimum=39, stroke=True)
    fitted_text(base, (x + 130, y + 62), subtitle, w - 300, 22, C_MUTED,
                minimum=17)
    seal = (x + w - 106, y + 14, 72, 72)
    d2.draw_gradient(base, seal, (80, 45, 24), (22, 15, 11), 21,
                     outline=(221, 157, 86, 165), outline_width=2)
    base.alpha_composite(d2.icon("d2_ico_events", (50, 50)), (seal[0] + 11, seal[1] + 10))


def draw_event_art(base: Image.Image, box: tuple[int, int, int, int], icon_name: str,
                   *, muted: bool = False, featured: bool = False) -> None:
    x, y, w, h = box
    d2.draw_gradient(base, box, (96, 54, 29), (23, 15, 12), 22,
                     outline=(239, 174, 105, 190), outline_width=2)
    d2.add_clipped_glow(base, (x + w // 4, y + h // 4, w // 2, h // 2),
                        (255, 103, 23, 100 if featured else 58), 25, box)
    side = min(w - 24, h - 24)
    art = d2.icon(icon_name, (side, side))
    if muted:
        art = ImageEnhance.Brightness(art).enhance(0.56)
    base.alpha_composite(art, (x + (w - side) // 2, y + (h - side) // 2))
    if muted:
        veil = Image.new("RGBA", (w - 8, h - 8), (7, 7, 7, 70))
        base.alpha_composite(veil, (x + 4, y + 4))


def draw_capsule(base: Image.Image, box: tuple[int, int, int, int], label: str,
                 *, warm: bool = False, muted: bool = False, size: int = 20) -> None:
    x, y, w, h = box
    top, bottom = ((105, 56, 27), (37, 22, 15)) if warm else ((49, 36, 27), (20, 16, 13))
    outline = (255, 184, 104, 180) if warm else (185, 142, 96, 100)
    fill = C_GOLD if warm else C_SOFT
    if muted:
        top, bottom, outline, fill = (37, 34, 30), (18, 17, 16), (127, 120, 105, 95), (153, 145, 128, 255)
    d2.draw_gradient(base, box, top, bottom, h // 2, outline=outline, outline_width=2)
    fitted_text(base, (x + w // 2, y + h // 2), label, w - 18, size, fill,
                lilita=True, minimum=14, anchor="mm")


def draw_button(base: Image.Image, box: tuple[int, int, int, int], label: str,
                *, primary: bool = False, muted: bool = False, size: int = 25) -> None:
    x, y, w, h = box
    if primary:
        d2.draw_primary_button(base, box, label, size)
        return
    if muted:
        d2.draw_gradient(base, (x, y + 5, w, h), (58, 55, 48), (25, 24, 22), 16,
                         outline=(141, 132, 111, 110), outline_width=2)
        color = (183, 175, 157, 255)
    else:
        d2.draw_gradient(base, (x, y + 5, w, h), (64, 47, 34), (23, 17, 13), 16,
                         outline=(153, 114, 74, 180), outline_width=2)
        color = C_TEXT
    fitted_text(base, (x + w // 2, y + h // 2), label, w - 16, size, color,
                lilita=True, minimum=15, anchor="mm")


def draw_featured(base: Image.Image) -> None:
    x, y, w, h = 36, 418, 1008, 252
    d2.add_clipped_glow(base, (x + 90, y + 3, w - 180, h + 4), (255, 104, 26, 95), 32,
                        (x, y, w, h))
    d2.paste_9(base, "d2_panel_frame_glut", (x, y, w, h), (72, 72, 72, 72))
    d2.draw_gradient(base, (x + 9, y + 9, w - 18, h - 18), (55, 34, 23), (17, 12, 10), 22,
                     outline=(255, 216, 165, 76), outline_width=1)
    draw_event_art(base, (x + 20, y + 18, 235, h - 36), "d2_ico_event_gildenjagd",
                   featured=True)

    tx = x + 281
    text(base, (tx, y + 25), "NÄCHSTES EVENT", 22, (255, 177, 94, 255))
    fitted_text(base, (tx - 2, y + 53), "Weltboss: Kriegsmammut", 560, 40,
                (255, 241, 215, 255), lilita=True, minimum=28, stroke=True)
    text(base, (tx, y + 111), "Gemeinschafts-Meilensteine · Schadensrangliste", 22, C_MUTED)
    draw_capsule(base, (tx, y + 151, 240, 50), "STARTET IN 4 TAGEN", warm=True, size=21)
    text(base, (tx + 258, y + 164), "28. OKT. · 3 TAGE", 21, C_SOFT)
    text(base, (tx, y + 217), "25 % · 50 % · 75 % · 100 % GEMEINSCHAFT", 18, C_MUTED)


EVENT_ROWS = [
    {
        "icon": "d2_ico_event_turnier", "name": "Stammeswettstreit",
        "description": "7 TAGE · RANGLISTE NACH KAMPFKRAFT-KLASSE",
        "status": "ENDET MORGEN", "live": True, "badge": True,
    },
    {
        "icon": "d2_ico_event_erntefest", "name": "Helden-Festival",
        "description": "14 TAGE · OHNE RANGLISTE",
        "status": "ENDET MORGEN", "live": True, "badge": False,
    },
    {
        "icon": "d2_ico_event_turnier", "name": "Turnier der Zeitalter",
        "description": "3 TAGE · TITEL & KOSMETIK",
        "status": "START 03. NOV.", "live": False, "badge": False,
    },
    {
        "icon": "d2_ico_event_bauwoche", "name": "Baumeister-Wochenende",
        "description": "2 TAGE · MEILENSTEINE",
        "status": "START 07. NOV.", "live": False, "badge": False,
    },
    {
        "icon": "d2_ico_events", "name": "Würfel-Event · 4 Tage",
        "description": "RANGLISTE · FESTMÜNZEN NUR AUS GRATIS-ENERGIE",
        "status": "START 12. NOV.", "live": False, "badge": False,
    },
]


def draw_event_row(base: Image.Image, y: int, item: dict[str, object]) -> None:
    x, w, h = 36, 1008, 174
    live = bool(item["live"])
    ready = bool(item["badge"])
    d2.texture_card(base, (x, y, w, h), ready=ready, muted=not live)
    draw_event_art(base, (x + 14, y + 14, 170, h - 28), str(item["icon"]), muted=not live)
    if ready:
        base.alpha_composite(d2.icon("d2_ico_badge_punkt", (43, 43)), (x + 159, y + 9))
    tx = x + 207
    title_color = (255, 241, 215, 255) if live else (178, 168, 148, 255)
    sub_color = C_MUTED if live else (136, 129, 115, 255)
    fitted_text(base, (tx, y + 23), str(item["name"]), 590, 34, title_color,
                lilita=True, minimum=23, stroke=live)
    fitted_text(base, (tx + 2, y + 71), str(item["description"]), 590, 21,
                sub_color, minimum=15)
    draw_capsule(base, (tx, y + 112, 260, 42), str(item["status"]),
                 warm=live, muted=not live, size=18)
    if live:
        draw_button(base, (x + w - 188, y + 54, 166, 60), "ANSEHEN", size=22)
    else:
        # Dates are taken from the week/day offsets in the GDD calendar.
        fitted_text(base, (x + w - 197, y + 54), "KOMMT", 158, 20,
                    (147, 137, 118, 255), lilita=True, minimum=16, anchor="mm")
        base.alpha_composite(d2.icon("d2_ico_schliessen", (28, 28)),
                             (x + w - 123, y + 88))


def draw_overview() -> Image.Image:
    base = d2.draw_base()
    d2.draw_outer_panel(base, PANEL)
    draw_header(base, "EVENTS", "LIVE & DEMNÄCHST · SAISONWOCHE 4")
    draw_featured(base)
    text(base, (48, 691), "LAUFEND & DEMNÄCHST", 27, (255, 211, 155, 255), lilita=True)
    ImageDraw.Draw(base, "RGBA").line((342, 710, 1030, 710), fill=(169, 116, 66, 120), width=2)
    start_y = 728
    row_h, gap = 174, 7
    for index, item in enumerate(EVENT_ROWS):
        draw_event_row(base, start_y + index * (row_h + gap), item)
    return base.resize(OUT_SIZE, Image.Resampling.LANCZOS)


def draw_event_coins(base: Image.Image, cx: int, cy: int, size: int) -> None:
    d = ImageDraw.Draw(base, "RGBA")
    r = size // 2 - 3
    d.ellipse((cx - r + 4, cy - r + 6, cx + r + 4, cy + r + 6), fill=(34, 18, 11, 255))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(193, 106, 43, 255),
              outline=(255, 213, 145, 255), width=4)
    d.ellipse((cx - r + 10, cy - r + 10, cx + r - 10, cy + r - 10),
              fill=(112, 55, 24, 255), outline=(250, 175, 91, 255), width=2)
    d.text((cx, cy - 2), "F", font=font(d2.FONT_LILITA, size // 2),
           fill=(255, 228, 179, 255), anchor="mm", stroke_width=1,
           stroke_fill=(71, 34, 15, 200))


def draw_event_banner(base: Image.Image) -> None:
    x, y, w, h = 36, 414, 1008, 226
    d2.add_clipped_glow(base, (x + 70, y + 3, w - 140, h + 4), (255, 101, 24, 90), 30,
                        (x, y, w, h))
    d2.paste_9(base, "d2_panel_frame_glut", (x, y, w, h), (72, 72, 72, 72))
    d2.draw_gradient(base, (x + 9, y + 9, w - 18, h - 18), (54, 34, 23), (18, 12, 10), 21,
                     outline=(255, 217, 164, 75), outline_width=1)
    draw_event_art(base, (x + 20, y + 18, 212, h - 36), "d2_ico_event_turnier", featured=True)
    tx = x + 257
    text(base, (tx, y + 22), "RANGLISTEN-EVENT", 21, (255, 177, 94, 255))
    fitted_text(base, (tx - 2, y + 51), "Stammeswettstreit", 555, 42,
                (255, 241, 215, 255), lilita=True, minimum=30, stroke=True)
    text(base, (tx + 2, y + 104), "50er Gruppe · Kampfkraft-Klasse", 23, C_SOFT)
    draw_capsule(base, (tx, y + 145, 235, 48), "ENDET MORGEN", warm=True, size=21)
    text(base, (tx + 260, y + 158), "7 TAGE", 21, C_MUTED)


def draw_summary(base: Image.Image) -> None:
    x, y, w, h = 36, 713, 1008, 104
    d2.paste_9(base, "d2_listenkarte_neutral", (x, y, w, h), (12, 8, 8, 8))
    d2.draw_gradient(base, (x + 8, y + 7, w - 16, h - 14), (43, 29, 20), (17, 13, 11), 15,
                     outline=(242, 185, 119, 60), outline_width=1)
    # Event points use the actual milestone thresholds. Shells stay in the global HUD;
    # Festmünzen are a separate event balance.
    text(base, (x + 26, y + 14), "EVENT-PUNKTE", 18, (255, 177, 94, 255))
    base.alpha_composite(d2.icon("d2_ico_stern", (39, 39)), (x + 24, y + 42))
    text(base, (x + 72, y + 37), "18.400", 31, C_GOLD, lilita=True)
    text(base, (x + 190, y + 47), "/ 30.000", 20, C_MUTED)
    d2.draw_progress(base, x + 26, y + 82, 360, 10, 18400, 30000)
    ImageDraw.Draw(base, "RGBA").line((x + 413, y + 17, x + 413, y + h - 17),
                                       fill=(186, 137, 85, 110), width=2)

    text(base, (x + 439, y + 14), "AHNENZEICHEN", 17, C_MUTED)
    base.alpha_composite(d2.icon("d2_ico_ahnenpruefung", (40, 40)), (x + 440, y + 48))
    text(base, (x + 491, y + 46), "145", 31, C_TEXT, lilita=True)
    ImageDraw.Draw(base, "RGBA").line((x + 626, y + 17, x + 626, y + h - 17),
                                       fill=(186, 137, 85, 110), width=2)

    text(base, (x + 651, y + 14), "FESTMÜNZEN", 17, C_MUTED)
    draw_event_coins(base, x + 678, y + 67, 47)
    text(base, (x + 715, y + 46), "480", 31, C_TEXT, lilita=True)


MILESTONES = [(2000, 80), (6000, 100), (12000, 100), (20000, 80), (30000, 40)]


def draw_milestones(base: Image.Image) -> None:
    x, y, w, h = 36, 826, 1008, 198
    d2.paste_9(base, "d2_panel_frame", (x, y, w, h), (72, 72, 72, 72))
    d2.draw_gradient(base, (x + 8, y + 8, w - 16, h - 16), (39, 29, 22), (14, 12, 10), 18,
                     outline=(238, 181, 116, 55), outline_width=1)
    text(base, (x + 20, y + 13), "MEILENSTEIN-BELOHNUNGEN", 23,
         (255, 211, 155, 255), lilita=True)
    draw_capsule(base, (x + w - 222, y + 10, 200, 34), "FESTMÜNZEN", size=17)
    # Rail and chest positions fit within the panel on both sides.
    centers = [x + 113 + i * 195 for i in range(5)]
    ImageDraw.Draw(base, "RGBA").line((centers[0], y + 91, centers[-1], y + 91),
                                       fill=(117, 77, 45, 255), width=12)
    ImageDraw.Draw(base, "RGBA").line((centers[0], y + 91, centers[2], y + 91),
                                       fill=(238, 127, 42, 255), width=8)
    for idx, ((points, coins), cx) in enumerate(zip(MILESTONES, centers)):
        reached = points <= 18400
        d2.draw_gradient(base, (cx - 50, y + 46, 100, 99),
                         (90, 52, 27) if reached else (49, 39, 29),
                         (24, 16, 12) if reached else (19, 17, 14), 19,
                         outline=(255, 181, 104, 205) if reached else (145, 126, 98, 110),
                         outline_width=2)
        if reached:
            d2.add_clipped_glow(base, (cx - 31, y + 61, 62, 60),
                                (255, 112, 33, 72), 15,
                                (cx - 50, y + 46, 100, 99))
        base.alpha_composite(d2.icon("d2_ico_kiste", (69, 69)), (cx - 34, y + 60))
        fitted_text(base, (cx, y + 154), f"{points // 1000}.000", 105, 19,
                    C_TEXT if reached else C_MUTED, lilita=True, minimum=15, anchor="mm")
        text(base, (cx, y + 179), f"{coins} F", 17,
             (255, 192, 112, 255) if reached else (139, 128, 109, 255),
             lilita=True, anchor="mm")
        if points in (2000, 6000):
            badge_x, badge_y = cx + 26, y + 42
            d = ImageDraw.Draw(base, "RGBA")
            d.ellipse((badge_x, badge_y, badge_x + 31, badge_y + 31),
                      fill=(85, 56, 31, 255), outline=(211, 166, 102, 210), width=2)
            d.line((badge_x + 8, badge_y + 16, badge_x + 13, badge_y + 21),
                   fill=(255, 226, 174, 255), width=3)
            d.line((badge_x + 13, badge_y + 21, badge_x + 24, badge_y + 9),
                   fill=(255, 226, 174, 255), width=3)
        if points == 12000:
            base.alpha_composite(d2.icon("d2_ico_badge_punkt", (34, 34)),
                                 (cx + 27, y + 40))


TASKS = [
    ("Absolviere eine Ahnenprüfung", "Gratis-Versuch · 1 / 1", "d2_ico_ahnenpruefung", True),
    ("Spiele 3 Kampagnen-Kämpfe", "Fortschritt · 3 / 3", "d2_ico_wettkampf", True),
    ("Sammle 3-mal Produktion ein", "Fortschritt · 2 / 3", "d2_ico_nahrung", False),
    ("Opfere 5 verdiente Ahnenzeichen", "Fortschritt · 5 / 5", "d2_ico_event_turnier", True),
]


def draw_task_row(base: Image.Image, y: int, item: tuple[str, str, str, bool]) -> None:
    title, detail, icon_name, claimable = item
    x, w, h = 36, 1008, 113
    d2.texture_card(base, (x, y, w, h), ready=claimable)
    d2.draw_gradient(base, (x + 13, y + 13, 86, 86), (83, 51, 29), (20, 14, 11), 17,
                     outline=(218, 155, 91, 160), outline_width=2)
    base.alpha_composite(d2.icon(icon_name, (70, 70)), (x + 21, y + 21))
    tx = x + 119
    fitted_text(base, (tx, y + 13), title, 510, 29, (255, 241, 215, 255),
                lilita=True, minimum=20, stroke=True)
    text(base, (tx + 2, y + 49), detail, 19, C_MUTED)
    d2.draw_progress(base, tx + 2, y + 83, 365, 10,
                     1 if detail.endswith("1 / 1") else 3 if detail.endswith("3 / 3") else
                     2 if detail.endswith("2 / 3") else 5,
                     1 if detail.endswith("1 / 1") else 3 if detail.endswith("3 / 3") else
                     3 if detail.endswith("2 / 3") else 5)
    text(base, (tx + 382, y + 87), "+25 P", 18, (246, 190, 120, 255),
         lilita=True, anchor="lm")
    draw_button(base, (x + w - 193, y + 27, 171, 59),
                "ABHOLEN" if claimable else "LOS", primary=claimable, size=23)


def draw_detail() -> Image.Image:
    base = d2.draw_base()
    d2.draw_outer_panel(base, PANEL)
    draw_header(base, "STAMMESWETTSTREIT", "RANGLISTEN-EVENT · WOCHE 4")
    draw_event_banner(base)
    fitted_text(base, (53, 651), "Punkte durch Ahnenzeichen, Aufgaben, Ressourcen & Ahnenprüfung.",
                974, 25, C_SOFT, minimum=20)
    fitted_text(base, (53, 682), "Für Rang und Festmünzen zählen nur Gratis-Versuche.",
                974, 21, C_MUTED, minimum=17)
    draw_summary(base)
    draw_milestones(base)
    text(base, (48, 1037), "EVENT-AUFGABEN", 27, (255, 211, 155, 255), lilita=True)
    text(base, (1027, 1042), "4 ABHOLBAR", 18, C_GOLD, lilita=True, anchor="ra")
    for index, item in enumerate(TASKS):
        draw_task_row(base, 1073 + index * 119, item)
    d2.draw_primary_button(base, (252, 1562, 576, 74), "ALLE EINSAMMELN", 31)
    text(base, (540, 1649), "3 AUFGABEN · 1 MEILENSTEIN", 17, C_MUTED,
         lilita=True, anchor="mm")
    return base.resize(OUT_SIZE, Image.Resampling.LANCZOS)


def main() -> None:
    draw_overview().save(OUT_OVERVIEW, optimize=True)
    draw_detail().save(OUT_DETAIL, optimize=True)
    print(f"Wrote {OUT_OVERVIEW}")
    print(f"Wrote {OUT_DETAIL}")


if __name__ == "__main__":
    main()
