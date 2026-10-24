#!/usr/bin/env python3
"""Render four D2 quest-log detail previews based on the approved v2b chrome."""
from __future__ import annotations

from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageOps


HERE = Path(__file__).resolve().parent
HUD = HERE.parent
REPO = HUD.parents[2]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import render_vorschau_menu_quests_d2_v2b as v2b
import render_vorschau_menu_quests_d2_v2 as v2


W, H = 1080, 1920
OUT_SIZE = (576, 1024)
PANEL = (14, 304, 1052, 1402)  # bottom edge sits on the dock separator at y=1708
v2.PANEL = PANEL
v2.DETAIL_PANEL = PANEL
v2b.PANEL = PANEL
v2b.DETAIL_PANEL = PANEL

OUTS = {
    "haupt": HUD / "vorschau_menu_quests_d2_v2c_detail_haupt.png",
    "neben": HUD / "vorschau_menu_quests_d2_v2c_detail_neben.png",
    "tutorial": HUD / "vorschau_menu_quests_d2_v2c_detail_tutorial.png",
    "erfolge": HUD / "vorschau_menu_quests_d2_v2c_detail_erfolge.png",
    "alle": HUD / "vorschau_menu_quests_d2_v2c_details_alle.png",
}

RUKA_PORTRAIT = REPO / "team/art/heroes/hero_ruka_portrait_alpha.png"
C_TEXT = (243, 231, 207, 255)
C_MUTED = (185, 169, 136, 255)
C_GOLD = (255, 217, 168, 255)
C_AMBER = (255, 179, 97, 255)
C_BRONZE = (201, 138, 74, 245)


def font(path: Path, size: int, weight: int = 800) -> ImageFont.FreeTypeFont:
    return v2b.font(path, size, weight)


def draw_section_label(base: Image.Image, y: int, label: str) -> None:
    d = ImageDraw.Draw(base, "RGBA")
    d.text((42, y), label, font=font(v2.FONT_BALOO, 22, 800), fill=(255, 221, 176, 255))
    text_width = d.textbbox((0, 0), label, font=font(v2.FONT_BALOO, 22, 800))[2]
    d.line((58 + text_width, y + 17, 1038, y + 17), fill=(190, 136, 83, 115), width=2)


def wrap_text(text: str, face: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    d = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    lines: list[str] = []
    current = ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if current and d.textbbox((0, 0), candidate, font=face)[2] > max_width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def draw_story(base: Image.Image, y: int, story: str, compact: bool = False) -> None:
    x, width, height = 36, 1008, (130 if compact else 150)
    v2.draw_gradient(base, (x, y, width, height), (57, 39, 27), (21, 16, 13), 18,
                     outline=(196, 145, 91, 170), outline_width=2)
    d = ImageDraw.Draw(base, "RGBA")
    d.line((x + 16, y + 12, x + width - 16, y + 12), fill=(255, 221, 177, 45), width=1)
    face = font(v2.FONT_BALOO, 24 if not compact else 22, 700)
    lines = wrap_text(story, face, width - 48)
    max_lines = 4 if not compact else 3
    lines = lines[:max_lines]
    line_height = 31 if not compact else 29
    total_h = len(lines) * line_height
    top = y + (height - total_h) // 2
    for i, line in enumerate(lines):
        d.text((x + 24, top + i * line_height), line, font=face,
               fill=(235, 222, 197, 255), stroke_width=1,
               stroke_fill=(10, 8, 7, 145))


def draw_portrait(base: Image.Image, x: int, y: int, size: int, achievement: bool = False) -> None:
    v2.draw_gradient(base, (x, y, size, size), (94, 58, 31), (24, 17, 13), 20,
                     outline=(238, 180, 105, 220), outline_width=2)
    if achievement:
        art = v2.icon("d2_ico_erfolge", (size - 28, size - 28))
        base.alpha_composite(art, (x + 14, y + 14))
        # The small star studs reinforce this as an achievement seal.
        for ox, oy in ((18, 18), (size - 40, 18), (18, size - 40), (size - 40, size - 40)):
            base.alpha_composite(v2.icon("d2_ico_stern", (22, 22)), (x + ox, y + oy))
    else:
        image = Image.open(RUKA_PORTRAIT).convert("RGBA")
        image = ImageOps.fit(image, (size - 10, size - 10), method=Image.Resampling.LANCZOS,
                             centering=(0.5, 0.36))
        mask = Image.new("L", image.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, image.width - 1, image.height - 1),
                                                radius=16, fill=255)
        image.putalpha(Image.composite(image.getchannel("A"), Image.new("L", image.size, 0), mask))
        base.alpha_composite(image, (x + 5, y + 5))


def draw_quest_card(base: Image.Image, spec: dict) -> None:
    x, y, width, height = 36, 516, 1008, 194
    v2.texture_card(base, (x, y, width, height), ready=spec.get("ready", False))
    draw_portrait(base, x + 16, y + 15, 164, achievement=spec.get("achievement", False))
    text_x = x + 202
    d = ImageDraw.Draw(base, "RGBA")
    d.text((text_x, y + 18), spec["category"], font=font(v2.FONT_BALOO, 21, 800),
           fill=C_AMBER)
    max_title = 700 if spec.get("achievement", False) else 752
    title_face = v2b.fit_text(spec["title"], max_title, 45, v2.FONT_LILITA)
    d.text((text_x - 2, y + 49), spec["title"], font=title_face,
           fill=(255, 242, 217, 255), stroke_width=1, stroke_fill=(9, 7, 6, 170))
    d.text((text_x, y + 112), "QUESTGEBERIN" if not spec.get("achievement", False) else "DAUERHAFTER ERFOLG",
           font=font(v2.FONT_BALOO, 17, 800), fill=C_MUTED)
    if spec.get("achievement", False):
        # Current account score is visible without suggesting it is a reward for this tier.
        score_x = x + width - 220
        v2.draw_gradient(base, (score_x, y + 117, 196, 54), (80, 50, 27), (24, 17, 13), 16,
                         outline=(207, 151, 83, 175), outline_width=2)
        base.alpha_composite(v2.icon("d2_ico_stern", (34, 34)), (score_x + 10, y + 127))
        d.text((score_x + 52, y + 143), "240 PUNKTE", font=font(v2.FONT_LILITA, 21),
               fill=C_GOLD, anchor="lm")
    else:
        d.text((text_x + 130, y + 112), "RUKA · WOLFSHERZ", font=font(v2.FONT_LILITA, 20),
               fill=(230, 211, 178, 255))


def draw_goal_row(base: Image.Image, y: int, goal: dict, width: int = 1008) -> None:
    x, height = 36, 62
    current = goal.get("current", False)
    complete = goal["done"]
    if current:
        v2.draw_gradient(base, (x, y, width, height), (76, 47, 25), (23, 17, 12), 13,
                         outline=(255, 158, 68, 225), outline_width=2)
        d = ImageDraw.Draw(base, "RGBA")
        d.rounded_rectangle((x + 2, y + 8, x + 7, y + height - 8), 2,
                             fill=(255, 140, 48, 235))
    else:
        v2.draw_gradient(base, (x, y, width, height), (45, 33, 24), (17, 14, 12), 13,
                         outline=(155, 112, 70, 145), outline_width=1)

    if goal.get("stage"):
        icon = v2.icon("d2_ico_stern", (34, 34))
        base.alpha_composite(icon, (x + 12, y + 14))
        d = ImageDraw.Draw(base, "RGBA")
        if complete:
            d.ellipse((x + 54, y + 18, x + 80, y + 44), fill=(88, 60, 33, 255),
                      outline=(224, 177, 107, 235), width=2)
            d.line((x + 60, y + 31, x + 65, y + 36, x + 75, y + 25),
                   fill=(255, 231, 184, 255), width=3, joint="curve")
        else:
            d.rounded_rectangle((x + 54, y + 18, x + 80, y + 44), 5,
                                outline=(198, 158, 104, 220), width=2)
    else:
        d = ImageDraw.Draw(base, "RGBA")
        if complete:
            d.ellipse((x + 13, y + 13, x + 49, y + 49), fill=(93, 65, 35, 255),
                      outline=(232, 185, 112, 235), width=2)
            d.line((x + 22, y + 31, x + 29, y + 38, x + 41, y + 23),
                   fill=(255, 231, 184, 255), width=4, joint="curve")
        else:
            d.rounded_rectangle((x + 14, y + 14, x + 48, y + 48), 7,
                                outline=(198, 158, 104, 220), width=2)

    left = x + (92 if goal.get("stage") else 66)
    label_face = v2b.fit_text(goal["label"], width - 270, 24, v2.FONT_BALOO)
    d = ImageDraw.Draw(base, "RGBA")
    d.text((left, y + 8), goal["label"], font=label_face,
           fill=(255, 235, 203, 255) if current else C_TEXT)
    counter = f"{goal['value']} / {goal['total']}"
    d.text((x + width - 20, y + 9), counter, font=font(v2.FONT_LILITA, 20),
           fill=C_GOLD if current or complete else C_MUTED, anchor="ra")
    bar_x, bar_y = left, y + 40
    bar_w = x + width - 20 - bar_x - 98
    v2b.draw_progress(base, bar_x, bar_y, bar_w, 12, goal["value"], goal["total"],
                      muted=not current and not complete)


def draw_goals(base: Image.Image, y: int, goals: list[dict]) -> int:
    row_gap = 5
    for index, goal in enumerate(goals):
        draw_goal_row(base, y + index * (62 + row_gap), goal)
    return y + len(goals) * 62 + max(0, len(goals) - 1) * row_gap


def draw_reward_tiles(base: Image.Image, y: int, rewards: list[dict], height: int = 160) -> None:
    count = len(rewards)
    tile_w, gap = 320, 18
    total_w = count * tile_w + (count - 1) * gap
    start_x = (W - total_w) // 2
    for index, reward in enumerate(rewards):
        x = start_x + index * (tile_w + gap)
        v2.draw_gradient(base, (x, y, tile_w, height), (72, 47, 30), (20, 15, 12), 17,
                         outline=(205, 151, 91, 205), outline_width=2)
        d = ImageDraw.Draw(base, "RGBA")
        d.line((x + 14, y + 4, x + tile_w - 14, y + 4), fill=(255, 224, 181, 95), width=2)
        if reward.get("kind") == "xp":
            art = v2.fit_icon(v2.HERO_XP, (70, 70))
        else:
            art = v2.icon(reward["icon"], (70, 70))
        base.alpha_composite(art, (x + (tile_w - 70) // 2, y + 13))
        d.text((x + tile_w // 2, y + 101), reward["amount"], font=font(v2.FONT_LILITA, 26),
               fill=(255, 240, 213, 255), anchor="mm")
        label_face = v2b.fit_text(reward["label"], tile_w - 20, 17, v2.FONT_BALOO)
        d.text((x + tile_w // 2, y + 134), reward["label"], font=label_face,
               fill=(221, 189, 147, 255), anchor="mm")


def draw_action_footer(base: Image.Image, spec: dict, button_y: int, note: str) -> None:
    v2.draw_primary_button(base, (344, button_y, 392, 88), spec["button"], 31)
    note_y = button_y + 106
    d = ImageDraw.Draw(base, "RGBA")
    d.line((74, note_y - 12, 1006, note_y - 12), fill=(151, 108, 67, 115), width=2)
    if spec.get("chapter"):
        base.alpha_composite(v2.icon("d2_ico_dock_karte", (31, 31)), (81, note_y + 4))
        d.text((124, note_y + 20), spec["chapter"], font=font(v2.FONT_BALOO, 20, 800),
               fill=(226, 203, 166, 255), anchor="lm")
        v2b.draw_progress(base, 674, note_y + 11, 310, 18,
                          spec.get("chapter_progress", (20, 27))[0],
                          spec.get("chapter_progress", (20, 27))[1])
    elif spec.get("next_tier"):
        base.alpha_composite(v2.icon("d2_ico_stern", (31, 31)), (81, note_y + 4))
        d.text((124, note_y + 20), spec["next_tier"], font=font(v2.FONT_BALOO, 20, 800),
               fill=(226, 203, 166, 255), anchor="lm")
    else:
        base.alpha_composite(v2.icon("d2_ico_quest_fertig", (31, 31)), (81, note_y + 4))
        d.text((124, note_y + 20), note, font=font(v2.FONT_BALOO, 20, 800),
               fill=(206, 187, 153, 255), anchor="lm")


def build_detail(spec: dict) -> Image.Image:
    base = v2.draw_base()
    v2b.draw_outer_panel(base, detail=True)
    v2b.draw_header(base, spec["tab_subtitle"], detail=False)
    tab_index = {"tutorial": 0, "haupt": 1, "neben": 2, "erfolge": 5}[spec["key"]]
    v2b.draw_tabs(base, tab_index)

    draw_quest_card(base, spec)
    draw_section_label(base, 724, "BESCHREIBUNG")
    compact = spec["key"] == "erfolge"
    story_y = 752 if compact else 752
    draw_story(base, story_y, spec["story"], compact=compact)

    goals_title_y = 896 if compact else 918
    goals_y = 927 if compact else 949
    draw_section_label(base, goals_title_y, "ZIELE")
    goals_end = draw_goals(base, goals_y, spec["goals"])

    rewards_label_y = max(goals_end + 17, 1250 if not compact else 1274)
    draw_section_label(base, rewards_label_y, "BELOHNUNGEN")
    rewards_y = rewards_label_y + 30
    draw_reward_tiles(base, rewards_y, spec["rewards"], height=158)

    button_y = max(rewards_y + 182, 1512 if not compact else 1490)
    draw_action_footer(base, spec, button_y, spec.get("note", ""))

    # Reapply the v2b inner frame after drawing the content, keeping the detail panel flush to the dock.
    px, py, pw, ph = PANEL
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((px + 2, py + 2, px + pw - 3, py + ph - 3), 28,
                        outline=C_BRONZE, width=3)
    d.rounded_rectangle((px + 10, py + 10, px + pw - 11, py + ph - 11), 23,
                        outline=(239, 186, 124, 70), width=1)
    return base


SPECS = [
    {
        "key": "haupt", "tab_subtitle": "HAUPT · QUEST-DETAIL · KAPITEL 10",
        "category": "HAUPTQUEST · KAPITEL 10 · DIE FURT",
        "title": "Wächter der Furt", "ready": True,
        "story": "Ruka hält am Rand der Furt inne: Unter dem dünnen Eis zieht ein dunkler Schatten vorbei. Olm versperrt den einzigen sicheren Weg. Wenn der Stamm zusammensteht, erreicht ihr das andere Ufer, bevor die Glut die Schwärme anlockt.",
        "goals": [
            {"label": "Späher an der Furt zurückdrängen", "value": 1, "total": 1, "done": True},
            {"label": "Empfohlene Kampfkraft für Mission 10 erreichen", "value": 100, "total": 100, "done": True},
            {"label": "Olm in Mission 10 besiegen", "value": 1, "total": 1, "done": True, "current": True},
        ],
        "rewards": [
            {"kind": "xp", "amount": "150", "label": "HELDEN-EP"},
            {"icon": "d2_ico_kiste", "amount": "1", "label": "AHNENRUF-TICKET"},
        ],
        "button": "ABHOLEN", "chapter": "KAPITEL 10 · 20 / 27 QUESTS",
        "chapter_progress": (20, 27),
    },
    {
        "key": "neben", "tab_subtitle": "NEBEN · QUEST-DETAIL · FREIWILLIG",
        "category": "NEBENQUEST · STAMMESLEBEN",
        "title": "Ein Feuer für alle", "ready": False,
        "story": "Am windstillen Ufer sitzt eine Familie ohne Schutz vor der Nacht. Ruka verspricht, Holz und Nahrung mit ihnen zu teilen. Ein kleines Feuer spendet Wärme – doch jedes Aufflammen kann die Tiefenschwärme aus der Tiefe rufen.",
        "goals": [
            {"label": "Trockenes Feuerholz sammeln", "value": 3, "total": 5, "done": False, "current": True},
            {"label": "Nahrung für den Abend bereitlegen", "value": 2, "total": 3, "done": False},
            {"label": "Eine Schutzhütte am Ufer errichten", "value": 0, "total": 1, "done": False},
            {"label": "Muscheln für Werkzeuge beisteuern", "value": 8, "total": 20, "done": False},
        ],
        "rewards": [
            {"icon": "d2_ico_holz", "amount": "300", "label": "HOLZ"},
            {"icon": "d2_ico_nahrung", "amount": "250", "label": "NAHRUNG"},
            {"icon": "d2_ico_gold_muschel", "amount": "20", "label": "MUSCHELN"},
        ],
        "button": "ZUM ZIEL", "note": "OPTIONALES ZIEL · OHNE ZEITLIMIT",
    },
    {
        "key": "tutorial", "tab_subtitle": "TUTORIAL · QUEST-DETAIL · SCHRITT 14",
        "category": "TUTORIAL · SCHRITT 14 VON 20",
        "title": "Kriegerlager auf Stufe 2", "ready": True,
        "story": "Ruka zeigt auf die Pfähle im Schnee: Das Lager muss dem Sturm standhalten. Gemeinsam verstärkt ihr die Wände und schafft Platz für neue Krieger. So kann der Stamm den nächsten Weg durchs Eis sicher erkunden.",
        "goals": [
            {"label": "Platz für das Kriegerlager vorbereiten", "value": 1, "total": 1, "done": True},
            {"label": "Holz und Stein für den Ausbau sammeln", "value": 2, "total": 2, "done": True},
            {"label": "Kriegerlager auf Stufe 2 verbessern", "value": 2, "total": 2, "done": True, "current": True},
        ],
        "rewards": [
            {"icon": "d2_ico_nahrung", "amount": "300", "label": "NAHRUNG"},
            {"icon": "d2_ico_holz", "amount": "200", "label": "HOLZ"},
        ],
        "button": "ABHOLEN", "note": "DANACH FOLGT DER NÄCHSTE TUTORIAL-SCHRITT",
    },
    {
        "key": "erfolge", "tab_subtitle": "ERFOLGE · QUEST-DETAIL · STUFE II",
        "category": "ERFOLG · STERNENSAMMLER · STUFE II",
        "title": "Sternensammler", "achievement": True,
        "story": "Jeder Stern erzählt von einem Weg, den der Stamm trotz Eis und Gefahr gemeistert hat. Die alten Prüfungen messen nicht nur Stärke: Sie zeigen, wie weit ihr gemeinsam in die unbekannte Welt vorgedrungen seid.",
        "goals": [
            {"label": "STUFE I · 10 KAMPAGNENSTERNE", "value": 10, "total": 10, "done": True, "stage": True},
            {"label": "STUFE II · 30 KAMPAGNENSTERNE", "value": 24, "total": 30, "done": False, "current": True, "stage": True},
            {"label": "STUFE III · 60 KAMPAGNENSTERNE", "value": 24, "total": 60, "done": False, "stage": True},
            {"label": "STUFE IV · 100 KAMPAGNENSTERNE", "value": 24, "total": 100, "done": False, "stage": True},
            {"label": "STUFE V · 150 KAMPAGNENSTERNE", "value": 24, "total": 150, "done": False, "stage": True},
        ],
        "rewards": [
            {"icon": "d2_ico_erfolge", "amount": "50", "label": "ECHOSPLITTER · STUFE II"},
        ],
        "button": "ZUM ZIEL", "next_tier": "NÄCHSTE STUFE III · 60 STERNE",
    },
]


def save_preview(image: Image.Image, path: Path) -> None:
    image.convert("RGB").resize(OUT_SIZE, Image.Resampling.LANCZOS).save(path, optimize=True)


def make_contact_sheet(paths: list[Path]) -> Path:
    gap, margin = 12, 12
    sheet = Image.new("RGB", (margin * 2 + 4 * OUT_SIZE[0] + 3 * gap,
                               margin * 2 + OUT_SIZE[1]), (13, 10, 9))
    d = ImageDraw.Draw(sheet)
    for index, path in enumerate(paths):
        image = Image.open(path).convert("RGB")
        x = margin + index * (OUT_SIZE[0] + gap)
        sheet.paste(image, (x, margin))
        d.rectangle((x, margin, x + OUT_SIZE[0] - 1, margin + OUT_SIZE[1] - 1),
                    outline=(153, 105, 61), width=1)
    sheet.save(OUTS["alle"], optimize=True)
    return OUTS["alle"]


def render() -> list[Path]:
    paths: list[Path] = []
    for spec in SPECS:
        path = OUTS[spec["key"]]
        save_preview(build_detail(spec), path)
        paths.append(path)
    paths.append(make_contact_sheet(paths))
    return paths


if __name__ == "__main__":
    for output in render():
        print(output)
