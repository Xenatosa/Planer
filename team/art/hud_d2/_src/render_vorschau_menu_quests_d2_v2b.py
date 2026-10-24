#!/usr/bin/env python3
"""Render the D2 quest-tab previews v2b at 576x1024."""
from __future__ import annotations

from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


HERE = Path(__file__).resolve().parent
HUD = HERE.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import render_vorschau_menu_quests_d2_v2 as v2


W, H = 1080, 1920
OUT_SIZE = (576, 1024)
# The dock separator starts at y=1708 in the approved v2 chrome.
PANEL = (14, 304, 1052, 1402)
DETAIL_PANEL = PANEL
v2.PANEL = PANEL
v2.DETAIL_PANEL = DETAIL_PANEL

OUTS = {
    "taeglich": HUD / "vorschau_menu_quests_d2_v2b_taeglich.png",
    "tutorial": HUD / "vorschau_menu_quests_d2_v2b_tutorial.png",
    "haupt": HUD / "vorschau_menu_quests_d2_v2b_haupt.png",
    "neben": HUD / "vorschau_menu_quests_d2_v2b_neben.png",
    "woche": HUD / "vorschau_menu_quests_d2_v2b_woche.png",
    "erfolge": HUD / "vorschau_menu_quests_d2_v2b_erfolge.png",
    "event": HUD / "vorschau_menu_quests_d2_v2b_event.png",
    "detail": HUD / "vorschau_menu_quests_d2_v2b_detail.png",
    "alle": HUD / "vorschau_menu_quests_d2_v2b_alle.png",
}

C_TEXT = (243, 231, 207, 255)
C_MUTED = (185, 169, 136, 255)
C_GOLD = (255, 217, 168, 255)
C_BRONZE = (201, 138, 74, 245)
C_GLOW = (255, 138, 42, 255)
C_INK = (11, 9, 8, 255)

TABS = [
    ("TUTORIAL", "d2_ico_quest_fertig"),
    ("HAUPT", "d2_ico_quest"),
    ("NEBEN", "d2_ico_bauen"),
    ("TÄGLICH", "d2_ico_gratis_login"),
    ("WOCHE", "d2_ico_kiste"),
    ("ERFOLGE", "d2_ico_erfolge"),
    ("EVENT", "d2_ico_events"),
]

REWARD_INFO = {
    "crystal": ("d2_ico_zeitkristall", "ZEITKRISTALLE"),
    "clock": ("d2_ico_uhr", "GLUTUHREN"),
    "food": ("d2_ico_nahrung", "NAHRUNG"),
    "wood": ("d2_ico_holz", "HOLZ"),
    "stone": ("d2_ico_stein", "STEIN"),
    "xp": ("xp", "HELDEN-EP"),
    "shell": ("d2_ico_gold_muschel", "MUSCHELN"),
    "ticket": ("d2_ico_kiste", "AHNENRUF-TICKETS"),
    "echo": ("d2_ico_erfolge", "ECHOSPLITTER"),
    "points": ("d2_ico_stern", "PUNKTE"),
    "eventcoin": ("eventcoin", "FESTMÜNZEN"),
}


def font(path: Path, size: int, weight: int = 800) -> ImageFont.FreeTypeFont:
    result = ImageFont.truetype(str(path), size)
    if path == v2.FONT_BALOO:
        try:
            result.set_variation_by_axes([weight])
        except (AttributeError, OSError):
            pass
    return result


def draw_header(base: Image.Image, subtitle: str, detail: bool = False) -> None:
    px, py, pw, _ = DETAIL_PANEL if detail else PANEL
    back = (px + 24, py + 12, 78, 78)
    v2.draw_gradient(base, back, (65, 47, 34), (24, 17, 13), 20,
                     outline=(202, 150, 93, 205), outline_width=2)
    base.alpha_composite(v2.icon("d2_ico_zurueck", (42, 42)), (back[0] + 18, back[1] + 18))
    d = ImageDraw.Draw(base, "RGBA")
    d.text((px + 126, py + 6), "TAGESAUFGABE" if detail else "AUFGABEN",
           font=font(v2.FONT_LILITA, 54 if not detail else 52),
           fill=(255, 231, 193, 255), stroke_width=1, stroke_fill=(40, 21, 12, 190))
    d.text((px + 130, py + 59), subtitle, font=font(v2.FONT_BALOO, 21, 800), fill=C_MUTED)

    seal_x, seal_y = px + pw - 106, py + 14
    v2.draw_gradient(base, (seal_x, seal_y, 72, 72), (80, 45, 24), (22, 15, 11), 21,
                     outline=(221, 157, 86, 165), outline_width=2)
    seal_icon = "d2_ico_quest_fertig" if detail else "d2_ico_quest"
    base.alpha_composite(v2.icon(seal_icon, (48, 48)), (seal_x + 12, seal_y + 12))
def draw_tabs(base: Image.Image, active: int, y: int = 402) -> None:
    x0, width, height, gap = 36, 138, 104, 6
    for index, (label, icon_name) in enumerate(TABS):
        x = x0 + index * (width + gap)
        is_active = index == active
        sprite = "d2_tab_aktiv" if is_active else "d2_tab_inaktiv"
        v2.paste_9(base, sprite, (x, y, width, height), (8, 8, 8, 12 if is_active else 10))
        if is_active:
            v2.add_clipped_glow(base, (x + 12, y + height - 20, width - 24, 16),
                                (255, 115, 35, 130), 8, (x, y, width, height))
            ImageDraw.Draw(base, "RGBA").line((x + 14, y + height - 5,
                                                x + width - 14, y + height - 5),
                                               fill=(255, 138, 42, 235), width=4)
        art = v2.icon(icon_name, (62, 62))
        art = ImageEnhance.Brightness(art).enhance(1.2 if is_active else 0.9)
        base.alpha_composite(art, (x + (width - 62) // 2, y + 3))
        d = ImageDraw.Draw(base, "RGBA")
        d.text((x + width // 2, y + 80), label, font=font(v2.FONT_LILITA, 18),
               fill=(255, 223, 177, 255) if is_active else (179, 163, 132, 255),
               anchor="mm", stroke_width=1, stroke_fill=(8, 6, 5, 165))
        if is_active:
            base.alpha_composite(v2.icon("d2_ico_badge_punkt", (24, 24)), (x + width - 31, y + 3))


def draw_outer_panel(base: Image.Image, detail: bool = False) -> None:
    v2.draw_outer_panel(base, DETAIL_PANEL if detail else PANEL)


def draw_event_coin(base: Image.Image, x: int, y: int, size: int) -> None:
    """A distinct festival token; it is not the game's shell/gold currency."""
    d = ImageDraw.Draw(base, "RGBA")
    cx, cy = x + size // 2, y + size // 2
    r = size // 2 - 2
    d.ellipse((cx-r+2, cy-r+4, cx+r+2, cy+r+4), fill=(53, 29, 14, 255))
    d.ellipse((cx-r, cy-r, cx+r, cy+r), fill=(210, 121, 43, 255),
              outline=(255, 218, 151, 255), width=max(2, size // 14))
    d.ellipse((cx-r+size//7, cy-r+size//7, cx+r-size//7, cy+r-size//7),
              fill=(119, 58, 23, 255), outline=(255, 190, 105, 255), width=2)
    d.text((cx, cy), "F", font=font(v2.FONT_LILITA, max(20, size // 2)),
           fill=(255, 229, 180, 255), anchor="mm", stroke_width=1,
           stroke_fill=(75, 34, 15, 190))


def reward_icon(base: Image.Image, key: str, x: int, y: int, size: int) -> None:
    sprite, _ = REWARD_INFO[key]
    if sprite == "xp":
        art = v2.fit_icon(v2.HERO_XP, (size, size))
    elif sprite == "eventcoin":
        draw_event_coin(base, x, y, size)
        return
    else:
        art = v2.icon(sprite, (size, size))
    base.alpha_composite(art, (x, y))


def draw_reward_chip(base: Image.Image, x: int, y: int, width: int, key: str,
                     amount: str, muted: bool = False, height: int = 36) -> None:
    v2.paste_9(base, "d2_chip", (x, y, width, height), (33, 4, 33, 4))
    _, label = REWARD_INFO[key]
    reward_icon(base, key, x + 6, y + (height - 27) // 2, 27)
    text = f"{amount} {label}"
    face = font(v2.FONT_LILITA, 18)
    d = ImageDraw.Draw(base, "RGBA")
    while d.textbbox((0, 0), text, font=face)[2] > width - 43 and face.size > 13:
        face = font(v2.FONT_LILITA, face.size - 1)
    d.text((x + 40, y + height // 2), text, font=face,
           fill=(164, 153, 129, 255) if muted else (238, 222, 188, 255),
           anchor="lm", stroke_width=0 if muted else 1,
           stroke_fill=(8, 6, 5, 135))


def draw_summary_card(base: Image.Image, icon_name: str, eyebrow: str, headline: str,
                      note: str, metric: str | None = None, metric_label: str | None = None,
                      progress: tuple[int, int] | None = None,
                      metric_icon: str | None = None) -> None:
    x, y, w, h = 36, 516, 1008, 150
    v2.add_clipped_glow(base, (x + 100, y + 6, w - 200, h - 12), (255, 105, 24, 62), 25,
                        (x, y, w, h))
    v2.paste_9(base, "d2_panel_frame_glut", (x, y, w, h), (72, 72, 72, 72))
    v2.draw_gradient(base, (x + 9, y + 9, w - 18, h - 18), (51, 32, 22), (19, 13, 10),
                     19, outline=(255, 214, 160, 75), outline_width=1)
    v2.draw_gradient(base, (x + 18, y + 15, 104, 98), (95, 54, 28), (24, 15, 11),
                     17, outline=(226, 168, 99, 175), outline_width=2)
    v2.add_clipped_glow(base, (x + 37, y + 31, 66, 66), (255, 110, 35, 45), 18,
                        (x + 18, y + 15, 104, 98))
    base.alpha_composite(v2.icon(icon_name, (76, 76)), (x + 32, y + 26))
    text_x = x + 144
    d = ImageDraw.Draw(base, "RGBA")
    d.text((text_x, y + 20), eyebrow, font=font(v2.FONT_BALOO, 18, 800),
           fill=(255, 178, 94, 255))
    right_edge = x + w - 220 if metric else x + w - 22
    headline_font = font(v2.FONT_LILITA, 28)
    while d.textbbox((0, 0), headline, font=headline_font)[2] > right_edge - text_x and headline_font.size > 19:
        headline_font = font(v2.FONT_LILITA, headline_font.size - 1)
    d.text((text_x, y + 51), headline, font=headline_font, fill=(255, 241, 215, 255),
           stroke_width=1, stroke_fill=(15, 9, 7, 170))
    d.text((text_x, y + 91), note, font=font(v2.FONT_BALOO, 17, 700), fill=C_MUTED)
    if progress:
        bar_x, bar_y, bar_w = text_x, y + 127, min(440, right_edge - text_x)
        v2.draw_progress(base, bar_x, bar_y, bar_w, 12, progress[0], progress[1])
    if metric:
        bx, by, bw, bh = x + w - 205, y + 16, 182, 118
        v2.draw_gradient(base, (bx, by, bw, bh), (82, 46, 26), (25, 16, 12), 19,
                         outline=(255, 177, 93, 190), outline_width=2)
        if metric_label:
            d.text((bx + bw // 2, by + 23), metric_label,
                   font=font(v2.FONT_BALOO, 15, 800), fill=(224, 199, 163, 255), anchor="mm")
        if metric_icon:
            reward_icon(base, metric_icon, bx + 17, by + 61, 36)
            d.text((bx + 112, by + 77), metric, font=font(v2.FONT_LILITA, 34),
                   fill=C_GOLD, anchor="mm", stroke_width=1, stroke_fill=(39, 19, 9, 180))
        else:
            d.text((bx + bw // 2, by + (65 if metric_label else 49)), metric,
                   font=font(v2.FONT_LILITA, 34), fill=C_GOLD, anchor="mm",
                   stroke_width=1, stroke_fill=(39, 19, 9, 180))


def draw_progress(base: Image.Image, x: int, y: int, width: int, height: int,
                  current: int, total: int, muted: bool = False) -> None:
    v2.draw_progress(base, x, y, width, height, current, total, muted=muted)


def fit_text(text: str, max_width: int, start_size: int = 27,
             path: Path | None = None) -> ImageFont.FreeTypeFont:
    path = path or v2.FONT_LILITA
    face = font(path, start_size, 800)
    d = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    while d.textbbox((0, 0), text, font=face)[2] > max_width and face.size > 17:
        face = font(path, face.size - 1, 800)
    return face


def draw_icon_frame(base: Image.Image, x: int, y: int, width: int, height: int,
                    icon_name: str, category: str, muted: bool = False) -> None:
    v2.draw_gradient(base, (x, y, width, height), (74, 47, 29), (20, 15, 12), 16,
                     outline=(191, 139, 83, 205) if not muted else (104, 94, 77, 160),
                     outline_width=2)
    icon_size = min(126, width - 28, height - 62)
    art = v2.icon(icon_name, (icon_size, icon_size))
    if muted:
        art = ImageEnhance.Brightness(art).enhance(0.42)
    base.alpha_composite(art, (x + (width - icon_size) // 2, y + 8))
    d = ImageDraw.Draw(base, "RGBA")
    cat_face = fit_text(category, width - 8, 15, v2.FONT_BALOO)
    d.text((x + width // 2, y + height - 13), category, font=cat_face,
           fill=(255, 191, 116, 255) if not muted else (157, 148, 128, 255),
           anchor="mm", stroke_width=1, stroke_fill=(9, 7, 6, 175))


def draw_lock_badge(base: Image.Image, x: int, y: int, width: int, height: int) -> None:
    v2.draw_gradient(base, (x, y, width, height), (59, 45, 33), (22, 17, 13), 15,
                     outline=(126, 103, 76, 170), outline_width=2)
    base.alpha_composite(v2.icon("d2_ico_schloss", (28, 28)), (x + 10, y + (height - 28) // 2))
    d = ImageDraw.Draw(base, "RGBA")
    d.text((x + width // 2 + 16, y + height // 2), "GESPERRT",
           font=font(v2.FONT_LILITA, 17), fill=(183, 165, 135, 255), anchor="mm")


def draw_row(base: Image.Image, y: int, item: dict, height: int = 142) -> None:
    x, width = 36, 1008
    state = item["state"]
    ready = state == "ready"
    claimed = state == "claimed"
    locked = state == "locked"
    box = (x, y, width, height)
    v2.texture_card(base, box, ready=ready, muted=claimed or locked)
    icon_h = height - 20
    draw_icon_frame(base, x + 13, y + 10, 100, icon_h,
                    item["icon"], item.get("category", "ZIEL"), muted=claimed or locked)

    text_x = x + 128
    right = x + width - 198
    max_text = right - text_x
    title = item["title"]
    d = ImageDraw.Draw(base, "RGBA")
    title_face = fit_text(title, max_text, 28)
    d.text((text_x, y + 7), title, font=title_face,
           fill=(255, 242, 217, 255) if not (claimed or locked) else (169, 159, 138, 255),
           stroke_width=1 if not locked else 0, stroke_fill=(9, 7, 6, 170))
    desc_face = fit_text(item["desc"], max_text, 18, v2.FONT_BALOO)
    d.text((text_x, y + 39), item["desc"], font=desc_face,
           fill=C_MUTED if not (claimed or locked) else (139, 133, 118, 255))

    if "progress" in item:
        current, total = item["progress"]
        bar_x, bar_y, bar_w = text_x, y + 66, min(492, max_text - 92)
        draw_progress(base, bar_x, bar_y, bar_w, 18, current, total,
                      muted=claimed or locked)
        meter = f"{current} / {total}"
        counter = C_GOLD if ready else (C_MUTED if claimed or locked else C_TEXT)
        d.text((bar_x + bar_w + 10, bar_y + 9), meter, font=font(v2.FONT_LILITA, 19),
               fill=counter, anchor="lm")

    rewards = item.get("rewards", [])
    chip_y = y + height - 40
    if rewards and not locked:
        chip_x = text_x
        for reward in rewards[:2]:
            if isinstance(reward, dict):
                kind, amount = reward["kind"], reward["amount"]
                chip_w = reward.get("width", 226)
            else:
                kind, amount = reward[0], reward[1]
                chip_w = 226
            draw_reward_chip(base, chip_x, chip_y, chip_w, kind, str(amount),
                             muted=claimed, height=34)
            chip_x += chip_w + 8

    action_x, action_y = x + width - 180, y + (height - 54) // 2
    if ready:
        v2.draw_primary_button(base, (action_x, action_y, 156, 54), "ABHOLEN", 21)
    elif claimed:
        v2.draw_gradient(base, (action_x + 46, action_y - 1, 62, 62), (73, 51, 31), (19, 15, 11),
                         20, outline=(147, 125, 89, 150), outline_width=2)
        base.alpha_composite(v2.icon("d2_ico_quest_fertig", (42, 42)),
                             (action_x + 56, action_y + 9))
    elif locked:
        draw_lock_badge(base, action_x - 2, action_y + 2, 158, 50)
    elif item.get("action", True):
        v2.draw_secondary_button(base, (action_x + 2, action_y, 152, 54), "LOS")


def draw_collect_all(base: Image.Image, count: int, y: int = 1514) -> None:
    if count <= 0:
        return
    x, w, h = 220, 640, 92
    v2.add_clipped_glow(base, (x - 25, y - 4, w + 50, h + 14), (255, 102, 22, 160), 24,
                        (x - 8, y - 5, w + 16, h + 10))
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((x, y + 8, x + w, y + h + 8), 20, fill=(73, 31, 14, 255))
    v2.draw_gradient(base, (x, y, w, h), (255, 192, 106), (216, 78, 14), 18,
                     outline=(255, 226, 177, 245), outline_width=2)
    d = ImageDraw.Draw(base, "RGBA")
    d.line((x + 18, y + 5, x + w - 18, y + 5), fill=(255, 246, 224, 170), width=2)
    d.text((x + 255, y + 45), "ALLE EINSAMMELN", font=font(v2.FONT_LILITA, 30),
           fill=(255, 248, 232, 255), anchor="mm", stroke_width=1,
           stroke_fill=(79, 31, 13, 175))
    badge_x, badge_y = x + w - 86, y + 14
    d.ellipse((badge_x, badge_y, badge_x + 62, badge_y + 62),
              fill=(93, 41, 15, 235), outline=(255, 238, 205, 220), width=2)
    d.text((badge_x + 31, badge_y + 31), str(count), font=font(v2.FONT_LILITA, 31),
           fill=(255, 245, 219, 255), anchor="mm")
    d.text((x + 63, y + 72), f"{count} ABHOLBAR", font=font(v2.FONT_BALOO, 15, 800),
           fill=(255, 229, 192, 255), anchor="lm")


def draw_footer(base: Image.Image, text: str, icon_name: str = "d2_ico_uhr",
                y: int = 1640) -> None:
    d = ImageDraw.Draw(base, "RGBA")
    d.line((66, y - 16, 1014, y - 16), fill=(151, 108, 67, 100), width=2)
    base.alpha_composite(v2.icon(icon_name, (28, 28)), (78, y - 2))
    d.text((119, y + 12), text, font=font(v2.FONT_BALOO, 18, 700),
           fill=(186, 170, 140, 255), anchor="lm")


def draw_screen(title_key: str, active: int, subtitle: str, summary: dict,
                rows: list[dict], row_height: int, claimable: int,
                footer: str, collect_y: int = 1514) -> Image.Image:
    base = v2.draw_base()
    draw_outer_panel(base)
    draw_header(base, subtitle)
    draw_tabs(base, active)
    draw_summary_card(base, **summary)
    start_y, gap = 676, 7
    for index, item in enumerate(rows):
        draw_row(base, start_y + index * (row_height + gap), item, row_height)
    if claimable:
        draw_collect_all(base, claimable, collect_y)
    draw_footer(base, footer)
    return base


def daily_screen() -> Image.Image:
    rows = [
        {"title": "Ernte einholen", "desc": "Sammle 3-mal Produktion ein.", "icon": "d2_ico_nahrung",
         "category": "ERNTE", "progress": (3, 3), "state": "ready",
         "rewards": [("crystal", 8), ("food", 100)]},
        {"title": "Fleißige Hände", "desc": "Verbessere 3 Gebäude.", "icon": "d2_ico_bauen",
         "category": "BAUEN", "progress": (2, 3), "state": "active",
         "rewards": [("crystal", 8), ("wood", 100)]},
        {"title": "Kriegerdrill", "desc": "Bilde 10 Einheiten aus.", "icon": "d2_ico_dock_armee",
         "category": "ARMEE", "progress": (7, 10), "state": "active",
         "rewards": [("crystal", 8), ("xp", 30)]},
        {"title": "Auf ins Feld", "desc": "Spiele 2 Kampagnenmissionen (Wiederholungen zählen).",
         "icon": "d2_ico_dock_karte", "category": "KAMPAGNE", "progress": (1, 2),
         "state": "active", "rewards": [("crystal", 8), ("xp", 40)]},
        {"title": "Volle Bäuche", "desc": "Gib 500 Nahrung aus.", "icon": "d2_ico_gold_muschel",
         "category": "MUSCHELN", "progress": (320, 500), "state": "active",
         "rewards": [("crystal", 8), ("shell", 30)]},
        {"title": "Willkommen zurück", "desc": "Melde dich heute an.", "icon": "d2_ico_gratis_login",
         "category": "LOGIN", "progress": (1, 1), "state": "claimed",
         "rewards": [("crystal", 20), ("clock", "2 × 15 MIN")]},
    ]
    summary = dict(icon_name="d2_ico_zeitkristall", eyebrow="TAGESPRÄMIE",
                   headline="60 ZEITKRISTALLE · 5 QUESTS + LOGIN",
                   note="Login 20 + 5 × 8 · Reset täglich um 04:00",
                   metric="1", metric_label="ABHOLBAR")
    return draw_screen("taeglich", 3, "TÄGLICH · HEUTE", summary, rows, 128, 1,
                       "Nicht abgeholte Belohnungen werden zum Tagesreset gutgeschrieben.", 1514)


def tutorial_screen() -> Image.Image:
    rows = [
        {"title": "Mission 3 gewinnen", "desc": "Gewinne Mission 3.", "icon": "d2_ico_dock_karte",
         "category": "KAMPAGNE", "progress": (1, 1), "state": "claimed",
         "rewards": [("food", 400), ("crystal", 50)]},
        {"title": "Kriegerlager auf Stufe 2", "desc": "Mehr Platz für deine Armee.", "icon": "d2_ico_bauen",
         "category": "BAUEN", "progress": (2, 2), "state": "ready",
         "rewards": [("food", 300), ("wood", 200)]},
        {"title": "Mission 4 gewinnen", "desc": "Gewinne Mission 4.", "icon": "d2_ico_dock_karte",
         "category": "KAMPAGNE", "progress": (0, 1), "state": "locked",
         "rewards": [("wood", 400), ("stone", 200)]},
        {"title": "Mission 5 gewinnen", "desc": "Gewinne Mission 5 (Elite).", "icon": "d2_ico_dock_karte",
         "category": "KAMPAGNE", "progress": (0, 1), "state": "locked",
         "rewards": [("food", 300), ("crystal", 30)]},
        {"title": "Schamanenhütte bauen", "desc": "Baue die Schamanenhütte.", "icon": "d2_ico_bauen",
         "category": "BAUEN", "progress": (0, 1), "state": "locked",
         "rewards": [("wood", 300), ("stone", 100)]},
    ]
    summary = dict(icon_name="d2_ico_quest_fertig", eyebrow="TUTORIAL · LINEAR",
                   headline="DIE NÄCHSTEN SCHRITTE IM DORF",
                   note="Q_TUT_014 von 20 · Belohnung nach jedem Schritt",
                   metric="14 / 20", metric_label="FORTSCHRITT")
    return draw_screen("tutorial", 0, "TUTORIAL · ERSTE STUNDE", summary, rows, 145, 1,
                       "Die nächste Aufgabe folgt nach dem Abschluss des aktiven Schritts.", 1514)


def main_screen() -> Image.Image:
    rows = [
        {"title": "Bereit für die Furt", "desc": "Erreiche 100 % der empfohlenen Kampfkraft für Mission 10.",
         "icon": "d2_ico_wettkampf", "category": "KAMPAGNE", "progress": (100, 100),
         "state": "claimed", "rewards": [("food", 150)]},
        {"title": "Wächter der Furt", "desc": "Besiege Olm in Mission 10.", "icon": "d2_ico_dock_karte",
         "category": "BOSS", "progress": (1, 1), "state": "ready",
         "rewards": [("xp", 150), ("ticket", 1)]},
        {"title": "Das Dorf feiert", "desc": "Sammle 3-mal die Produktion deines Dorfs ein.",
         "icon": "d2_ico_nahrung", "category": "DORF", "progress": (0, 3), "state": "locked",
         "rewards": [("ticket", 2), ("crystal", 30)]},
        {"title": "Felsenwerfer", "desc": "Bilde 2 Felsenwerfer aus.", "icon": "d2_ico_dock_armee",
         "category": "ARMEE", "progress": (0, 2), "state": "locked",
         "rewards": [("xp", 80)]},
        {"title": "Ein Held wächst", "desc": "Bringe einen Helden auf Stufe 3.",
         "icon": "d2_ico_dock_helden", "category": "HELDEN", "progress": (0, 3),
         "state": "locked", "rewards": [("xp", 100)]},
    ]
    summary = dict(icon_name="d2_ico_dock_karte", eyebrow="HAUPTKETTE · KAMPAGNE",
                   headline="WÄCHTER DER FURT",
                   note="Olm besiegen · danach öffnen Tages- und Wochenaufgaben",
                   metric="20 / 27", metric_label="HAUPTQUEST")
    return draw_screen("haupt", 1, "HAUPT · KAMPAGNENFORTSCHRITT", summary, rows, 145, 1,
                       "Hauptquests bleiben erhalten und führen dich zum nächsten Ziel.", 1514)


def side_screen() -> Image.Image:
    rows = [
        {"title": "Das Dorf beleben", "desc": "Dorfleben-Aufgaben folgen mit dem freigeschalteten Feature.",
         "icon": "d2_ico_bauen", "category": "DORFLEBEN", "state": "locked", "action": False},
        {"title": "Stamm schmücken", "desc": "Deko-Ziele erscheinen, sobald Dekorationen verfügbar sind.",
         "icon": "d2_ico_erfolge", "category": "DEKO", "state": "locked", "action": False},
        {"title": "Mit den Ahnen vertraut", "desc": "Heldenbindung ist für spätere Nebenquests vorgesehen.",
         "icon": "d2_ico_dock_helden", "category": "HELDEN", "state": "locked", "action": False},
    ]
    summary = dict(icon_name="d2_ico_bauen", eyebrow="NEBENQUESTS · OPTIONALE ZIELE",
                   headline="DORFLEBEN · DEKO · HELDENBINDUNG",
                   note="Diese Themen sind laut Quest-System noch nicht aktiv.",
                   metric="0", metric_label="VERFÜGBAR")
    base = draw_screen("neben", 2, "NEBEN · OPTIONALE ZIELE", summary, rows, 176, 0,
                       "Nebenquests werden ergänzt, sobald die zugehörigen Features starten.", 1514)
    return base


def weekly_screen() -> Image.Image:
    rows = [
        {"title": "Fleißiger Stamm", "desc": "Schließe 20 Tagesaufgaben ab.", "icon": "d2_ico_quest",
         "category": "TAGESZIELE", "progress": (18, 20), "state": "active", "rewards": [("crystal", 30)]},
        {"title": "Feldzug", "desc": "Spiele 15 Kampagnenmissionen.", "icon": "d2_ico_dock_karte",
         "category": "KAMPAGNE", "progress": (15, 15), "state": "ready",
         "rewards": [("crystal", 25), ("xp", 150)]},
        {"title": "Baumeisterwoche", "desc": "Verbessere 15 Gebäude.", "icon": "d2_ico_bauen",
         "category": "BAUEN", "progress": (9, 15), "state": "active",
         "rewards": [("crystal", 25), ("wood", 300)]},
        {"title": "Heerschau", "desc": "Bilde 60 Einheiten aus.", "icon": "d2_ico_dock_armee",
         "category": "ARMEE", "progress": (46, 60), "state": "active",
         "rewards": [("crystal", 25), ("xp", 150)]},
        {"title": "Alle Stämme vereint", "desc": "Bilde jede der 6 Steinzeit-Einheiten mindestens 1-mal aus.",
         "icon": "d2_ico_dock_armee", "category": "EINHEITEN", "progress": (4, 6),
         "state": "active", "rewards": [("crystal", 25), ("xp", 150)]},
        {"title": "Wochenkiste", "desc": "Schließe 4 von 5 Wochenaufgaben ab.", "icon": "d2_ico_kiste",
         "category": "TRUHE", "progress": (4, 4), "state": "ready",
         "rewards": [("ticket", 2), ("clock", "1 × 60 MIN")]},
    ]
    summary = dict(icon_name="d2_ico_kiste", eyebrow="WOCHENFORTSCHRITT · RESET MO 04:00",
                   headline="130 ZEITKRISTALLE · 5 AUFGABEN",
                   note="Wochenkiste: ab 4 von 5 Aufgaben · 2 Tickets + 1 Glutuhr",
                   metric="4 / 5", metric_label="ZUR KISTE",
                   progress=(4, 5))
    return draw_screen("woche", 4, "WOCHE · MO 04:00", summary, rows, 128, 2,
                       "Reset montags um 04:00 · Europe/Berlin", 1514)


def achievement_screen() -> Image.Image:
    rows = [
        {"title": "Glut des Häuptlings · STUFE I", "desc": "Bringe das Häuptlingsfeuer auf Stufe 3.",
         "icon": "d2_ico_bauen", "category": "DORF", "progress": (3, 3), "state": "claimed",
         "rewards": [("xp", 150)]},
        {"title": "Flamme des Häuptlings · STUFE II", "desc": "Bringe das Häuptlingsfeuer auf Stufe 5.",
         "icon": "d2_ico_bauen", "category": "DORF", "progress": (3, 5), "state": "active",
         "rewards": [("xp", 250)]},
        {"title": "Sternensammler I · STUFE I", "desc": "Sammle 10 Kampagnensterne.",
         "icon": "d2_ico_stern", "category": "KAMPAGNE", "progress": (10, 10), "state": "ready",
         "rewards": [("echo", 20)]},
        {"title": "Sternensammler II · STUFE II", "desc": "Sammle 30 Kampagnensterne.",
         "icon": "d2_ico_stern", "category": "KAMPAGNE", "progress": (24, 30), "state": "locked",
         "rewards": [("echo", 50)]},
        {"title": "Fünf Ahnen", "desc": "Besitze 5 Helden.", "icon": "d2_ico_dock_helden",
         "category": "HELDEN", "progress": (4, 5), "state": "active", "rewards": [("ticket", 1)]},
        {"title": "Treuer Stamm", "desc": "Melde dich an 7 verschiedenen Tagen an.",
         "icon": "d2_ico_gratis_login", "category": "STAMM", "progress": (6, 7),
         "state": "active", "rewards": [("xp", 100)]},
    ]
    summary = dict(icon_name="d2_ico_erfolge", eyebrow="ERFOLGE · KATEGORIEN",
                   headline="DORF · KAMPAGNE · EINHEITEN · HELDEN",
                   note="STUFE I–II · ★ 24 / 90 KAMPAGNENSTERNE",
                   metric="240", metric_label="ERFOLGSPUNKTE")
    return draw_screen("erfolge", 5, "ERFOLGE · DAUERHAFTE ZIELE", summary, rows, 128, 1,
                       "Erfolge bleiben erhalten · Titel und Belohnungen nach Stufe.", 1514)


def event_screen() -> Image.Image:
    rows = [
        {"title": "Ahnenprüfung", "desc": "Absolviere 1 Gratis-Versuch.", "icon": "d2_ico_wettkampf",
         "category": "KAMPF", "progress": (1, 1), "state": "ready", "rewards": [("points", 25)]},
        {"title": "Feldzug", "desc": "Spiele 3 Kampagnenkämpfe (Wiederholungen zählen).",
         "icon": "d2_ico_dock_karte", "category": "KAMPAGNE", "progress": (2, 3),
         "state": "active", "rewards": [("points", 25)]},
        {"title": "Dorf ernten", "desc": "Sammle 3-mal Produktion ein.", "icon": "d2_ico_nahrung",
         "category": "DORF", "progress": (1, 3), "state": "active", "rewards": [("points", 25)]},
        {"title": "Ahnenzeichen spenden", "desc": "Opfere 5 verdiente Ahnenzeichen.",
         "icon": "d2_ico_events", "category": "STAMM", "progress": (2, 5),
         "state": "active", "rewards": [("points", 25)]},
    ]
    summary = dict(icon_name="d2_ico_events", eyebrow="STAMMESWETTSTREIT · 7 TAGE",
                   headline="2.740 PUNKTE · NOCH 4 T 08:32",
                   note="4 Event-Aufgaben pro Tag · je 25 Punkte · 400 Festmünzen max.",
                   metric="80", metric_label="FESTMÜNZEN", metric_icon="eventcoin")
    base = draw_screen("event", 6, "EVENT · STAMMESWETTSTREIT", summary, rows, 172, 1,
                       "2.000 Punkte → 80 Festmünzen · nächste Stufe bei 6.000 Punkten.", 1514)
    return base


def detail_screen() -> Image.Image:
    base = v2.draw_base()
    draw_outer_panel(base, detail=True)
    draw_header(base, "TÄGLICH · ERNTE", detail=True)
    draw_tabs(base, 3)

    x, y, w, h = 36, 516, 1008, 320
    v2.texture_card(base, (x, y, w, h), ready=True)
    draw_icon_frame(base, x + 18, y + 18, 172, 284, "d2_ico_nahrung", "ERNTE")
    text_x = x + 220
    d = ImageDraw.Draw(base, "RGBA")
    d.text((text_x, y + 26), "TÄGLICH · ERNTE", font=font(v2.FONT_BALOO, 21, 800),
           fill=(255, 179, 97, 255))
    d.text((text_x - 2, y + 63), "Ernte einholen", font=font(v2.FONT_LILITA, 42),
           fill=(255, 242, 217, 255), stroke_width=1, stroke_fill=(9, 7, 6, 170))
    d.text((text_x, y + 119), "Sammle 3-mal Produktion ein.",
           font=font(v2.FONT_BALOO, 24, 700), fill=(214, 199, 166, 255))
    v2.draw_gradient(base, (text_x, y + 166, 262, 42), (99, 49, 22), (37, 21, 13),
                     18, outline=(255, 138, 42, 205), outline_width=1)
    d = ImageDraw.Draw(base, "RGBA")
    d.text((text_x + 131, y + 187), "FERTIG · ABHOLBEREIT", font=font(v2.FONT_LILITA, 18),
           fill=C_GOLD, anchor="mm")
    d.text((text_x, y + 226), "FORTSCHRITT", font=font(v2.FONT_BALOO, 17, 800), fill=C_MUTED)
    d.text((x + w - 30, y + 226), "3 / 3", font=font(v2.FONT_LILITA, 21), fill=C_GOLD, anchor="ra")
    draw_progress(base, text_x, y + 251, w - 272, 22, 3, 3)

    d = ImageDraw.Draw(base, "RGBA")
    d.text((42, 864), "BELOHNUNGEN", font=font(v2.FONT_BALOO, 22, 800),
           fill=(255, 221, 176, 255))
    d.line((224, 879, 1038, 879), fill=(190, 136, 83, 115), width=2)
    reward_box = (36, 894, 1008, 384)
    v2.paste_9(base, "d2_panel_frame", reward_box, (72, 72, 72, 72))
    v2.draw_gradient(base, (45, 903, 990, 366), (34, 25, 20), (15, 12, 10), 24,
                     outline=(235, 184, 127, 70), outline_width=1)
    reward_rows = [("crystal", "8", "Zeitkristalle · Belohnung der Tagesaufgabe"),
                   ("food", "100", "Nahrung · zusätzliche Dorfressource")]
    for idx, (kind, amount, note) in enumerate(reward_rows):
        ry = 912 + idx * 178
        if idx:
            ImageDraw.Draw(base, "RGBA").line((72, ry - 9, 1008, ry - 9),
                                               fill=(151, 108, 67, 95), width=2)
        v2.draw_gradient(base, (62, ry + 9, 116, 116), (75, 47, 29), (20, 15, 12), 19,
                         outline=(191, 139, 83, 195), outline_width=2)
        reward_icon(base, kind, 83, ry + 30, 74)
        d = ImageDraw.Draw(base, "RGBA")
        d.text((212, ry + 44), f"{amount}  {REWARD_INFO[kind][1]}",
               font=font(v2.FONT_LILITA, 28), fill=(255, 241, 215, 255))
        d.text((212, ry + 83), note, font=font(v2.FONT_BALOO, 18, 700), fill=C_MUTED)
        d.text((982, ry + 64), "✓", font=font(v2.FONT_LILITA, 34),
               fill=(255, 193, 120, 255), anchor="mm")

    v2.draw_primary_button(base, (346, 1302, 388, 94), "ABHOLEN", 33)
    d = ImageDraw.Draw(base, "RGBA")
    d.line((74, 1430, 1006, 1430), fill=(151, 108, 67, 115), width=2)
    base.alpha_composite(v2.icon("d2_ico_uhr", (38, 38)), (82, 1453))
    d.text((133, 1471), "Bis zum Tagesreset um 04:00 abholbar.",
           font=font(v2.FONT_BALOO, 20, 700), fill=(206, 187, 153, 255), anchor="lm")
    d.text((133, 1511), "Danach wird eine offene Belohnung automatisch gutgeschrieben.",
           font=font(v2.FONT_BALOO, 18, 700), fill=(171, 158, 135, 255), anchor="lm")
    d.text((82, 1658), "EUROPE / BERLIN", font=font(v2.FONT_BALOO, 16, 800),
           fill=(147, 130, 106, 255))
    d.text((1004, 1658), "HEUTE · ERNTE", font=font(v2.FONT_BALOO, 16, 800),
           fill=(147, 130, 106, 255), anchor="ra")

    # Keep the modal body in front of the background and flush to the dock separator.
    px, py, pw, ph = DETAIL_PANEL
    d.rounded_rectangle((px + 2, py + 2, px + pw - 3, py + ph - 3), 28,
                        outline=C_BRONZE, width=3)
    d.rounded_rectangle((px + 10, py + 10, px + pw - 11, py + ph - 11), 23,
                        outline=(239, 186, 124, 70), width=1)
    return base


def save_preview(image: Image.Image, path: Path) -> None:
    image.convert("RGB").resize(OUT_SIZE, Image.Resampling.LANCZOS).save(path, optimize=True)


def make_contact_sheet(paths: list[Path]) -> Path:
    thumbs = []
    for path in paths:
        image = Image.open(path).convert("RGB")
        thumbs.append(image.resize((288, 512), Image.Resampling.LANCZOS))
    gap, margin = 12, 12
    sheet = Image.new("RGB", (margin * 2 + 4 * 288 + 3 * gap,
                               margin * 2 + 2 * 512 + gap), (13, 10, 9))
    draw = ImageDraw.Draw(sheet)
    for index, thumb in enumerate(thumbs):
        col, row = index % 4, index // 4
        px = margin + col * (288 + gap)
        py = margin + row * (512 + gap)
        sheet.paste(thumb, (px, py))
        draw.rectangle((px, py, px + 287, py + 511), outline=(153, 105, 61), width=1)
    sheet.save(OUTS["alle"], optimize=True)
    return OUTS["alle"]


def render() -> list[Path]:
    screens = [
        ("taeglich", daily_screen()),
        ("tutorial", tutorial_screen()),
        ("haupt", main_screen()),
        ("neben", side_screen()),
        ("woche", weekly_screen()),
        ("erfolge", achievement_screen()),
        ("event", event_screen()),
        ("detail", detail_screen()),
    ]
    rendered = []
    for key, screen in screens:
        save_preview(screen, OUTS[key])
        rendered.append(OUTS[key])
    rendered.append(make_contact_sheet([OUTS[key] for key, _ in screens]))
    return rendered


if __name__ == "__main__":
    for output in render():
        print(output)
