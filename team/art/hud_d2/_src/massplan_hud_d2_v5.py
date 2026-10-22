#!/usr/bin/env python3
"""Massplan Dorf-HUD D2 "Obsidian & Glut" v2 (Epodarien, 22.10.2026, Feedback Fabian 21:09: Top-Leiste nur 3 Waehrungen + Ressourcen-Knopf).
0 $: nur PIL, keine KI-Bilder. Erzeugt:
  ../massplan_hud_d2_v5.png         Massplan (1080x1920 Canvas + Legende rechts)
  ../massplan_hud_d2_v5_bloecke.png Bausteine d2_* an den Positionen (1080x1920)
  ../massplan_hud_d2_v5_elemente.json  alle Werte (Quelle fuer die .md-Tabelle)
Aufruf: python3 team/art/hud_d2/_src/massplan_hud_d2_v5.py  (aus Repo-Root oder beliebig)
HUD v5/v5.7 (team/art/_alt/) wird NICHT verwendet.
"""
import re, json, os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
OUT = os.path.abspath(os.path.join(HERE, ".."))
EXP = os.path.join(ROOT, "team/art/ui-kit/menus_v3/vorlage_D2_export")
FONTS = os.path.join(ROOT, "team/art/ui/fonts")
VILLAGE = os.path.join(ROOT, "team/art/ui/village/e1_village_bg_stilA_v2.png")
MAN = json.load(open(os.path.join(EXP, "manifest_9slice.json")))

W, H = 1080, 1920
SAFE_TOP, SAFE_BOT = 90, 48          # Notch oben, Gestenleiste unten
MARGIN = 28                           # D2 Aussenrand
TOUCH_MIN = 96                        # Fabian: min. 96 (D2-Vorlage: 120 Ziel)

def font(name, size):
    p = {"lilita": "LilitaOne-Regular.ttf", "baloo": "Baloo2-Variable.ttf"}[name]
    f = ImageFont.truetype(os.path.join(FONTS, p), size)
    if name == "baloo":
        try: f.set_variation_by_axes([800])
        except Exception: pass
    return f

# ---------------------------------------------------------------- Layout
# (id, name, x, y, w, h, sprite, hitbox(x,y,w,h) or None, gruppe)
E = []
def add(i, name, x, y, w, h, sprite="", hit=None, grp="", note=""):
    E.append(dict(id=i, name=name, x=x, y=y, w=w, h=h, sprite=sprite,
                  hit=list(hit) if hit else [x, y, w, h], grp=grp, note=note))

T = SAFE_TOP
# Top-Leiste 90..282 (2 Zeilen)
add("A1", "Avatar (Portraet)", 28, T + 8, 128, 128, "d2_panel_frame (9-Slice)", (28, T, 128, 144), "top",
    "Portraet 104 innen (12 px), antippbar -> Profil")
add("A2", "Level-Badge", 28 + 128 - 4 - 60, T + 8 + 128 - 4 - 40, 60, 40, "d2_badge_stufe", None, "top",
    "innen rechts unten 4/4, Lilita 26")
# eine Zeile: Zeitkristalle + Plus, Wissen, Gold (Muscheln)
add("R1", "Pill Zeitkristalle", 172, T + 8, 248, 80, "d2_pill_ressource", (172, T, 248, 96), "top",
    "Icon 64 bei x+8/y+8, Zahl Lilita 40 ab x+84 (Platz 152)")
add("R2", "Plus Zeitkristalle -> Shop", 432, T + 8, 80, 80, "d2_btn_plus_pill + d2_ico_plus", (422, T, 100, 96), "top",
    "sichtbar 80 (= Pill-Hoehe), Hitbox 100x96 (2 px Luft zu R1 und 10 px zu R3)")
add("R3", "Pill Wissen", 532, T + 8, 248, 80, "d2_pill_ressource", (532, T, 248, 96), "top", "")
add("R4", "Pill Gold (Muscheln)", 800, T + 8, 248, 80, "d2_pill_ressource", (800, T, 248, 96), "top", "")
# Ressourcen-Knopf: nur Icon (Kiste), unter der Waehrungszeile, buendig mit R1
KX, KY, KS = 172, T + 106, 104
add("K1", "Knopf Ressourcen (Kiste)", KX, KY, KS, KS, "d2_btn_quadrat_normal / _gedrueckt (offen)", None, "top",
    "nur Icon d2_ico_kiste 72 bei x+16/y+16, kein Text, kein Pfeil")
# geoeffnete Liste (nur im Zustand offen), verankert an RB (12 px darunter, linke Kante = RB)
LX, LY, LW_, ROWH = KX, KY + KS + 12, 600, 120
RL = ["Holz", "Stein", "Nahrung"]
LH = 24 + 40 + len(RL) * ROWH + 24
add("L0", "Ressourcen-Liste (offen)", LX, LY, LW_, LH, "d2_dropdown_liste (9-Slice 72)", None, "liste",
    "Anker: 12 px unter K1, linke Kante = K1; schliesst per Tipp auf K1 oder Scrim")
add("L0H", "Kopf 'LAGER'", LX + 24, LY + 24, LW_ - 48, 32, "Text Baloo 700 22, Sperrung 3", None, "liste", "text.muted")
for k, n in enumerate(RL):
    ry = LY + 64 + k * ROWH
    add(f"L{k+1}", f"Zeile {n}", LX + 12, ry, LW_ - 24, ROWH, "Zeile (ganze Zeile antippbar)", None, "liste",
        "Tipp -> Gebaeude/Info; Trenner d2_dropdown_trenner")
    add(f"L{k+1}I", f"Icon {n}", LX + 24, ry + 24, 72, 72, "Icon neu D2", None, "liste", "")
    add(f"L{k+1}N", f"Name {n}", LX + 112, ry + 18, 240, 40, "Text Baloo 800 28", None, "liste", "text.main")
    add(f"L{k+1}B", f"Lagerbalken {n}", LX + 112, ry + 74, 240, 22, "d2_bar_bg + d2_bar_fill_glut", None, "liste", "Fuellung = Menge/Lager")
    add(f"L{k+1}W", f"Menge {n}", LX + 368, ry + 14, 196, 48, "Text Lilita 36 rechtsb.", None, "liste", "text.main")
    add(f"L{k+1}C", f"Lager {n}", LX + 368, ry + 66, 196, 34, "Text Baloo 700 22 rechtsb.", None, "liste", "text.counter, voll = state.missing")
# Seitenleiste rechts
# v5: rechts = Monetarisierung/Belohnungen, links = Wettbewerb/zeitlich begrenzt
SIDE = [("S1", "Beschwören"), ("S2", "Pass"), ("S3", "Shop"), ("S4", "Gratis"), ("S5", "Mail"), ("S6", "Mehr")]
LEFT = [("H1", "Ranglisten"), ("H2", "Arena"), ("H3", "Prüfung")]
BADGE = {"S1": "1", "S2": "2", "S4": "1", "S5": "4", "H2": "3", "B1": "1"}
def sideknopf(i, n, x, y, grp, note=""):
    add(i, f"Seitenknopf {n}", x, y, 120, 120, "d2_btn_quadrat_normal" + (" + Glut-Ring" if i == "S1" else "") + (" / _gedrueckt (offen)" if i == "S6" else ""),
        (x, y, 120, 152), grp, note or "Icon 80; Hitbox inkl. Label 120x152")
    lw = 140 if n in ("Beschwören", "Ranglisten") else 120
    add(i + "L", f"Label {n}", x - (lw - 120) // 2, y + 124, lw, 28, "Text Baloo 800 22", None, grp, "")
    if i in BADGE: add(i + "B", f"Badge {n}", x + 68, y + 4, 48, 38, "d2_badge_zaehler", None, "badge", "")
for k, (i, n) in enumerate(SIDE): sideknopf(i, n, 932, 316 + k * 172, "side")
for k, (i, n) in enumerate(LEFT): sideknopf(i, n, 28, 488 + k * 172, "sidel")
sideknopf("B1", "Bauen", 932, 1396, "side", "Bau-Modus (Hammer); spiegelt Chat C1; zusaetzlich Tipp auf Bauplatz/Gebaeude")
MT = [("Forschung", "GDD 21"), ("Minigames", "GDD 17"), ("Erfolge", "quest-system-v1"),
      ("Artefakte", "GDD 18"), ("Aufwertung", "Scaffold general_upgrade"), ("Abo", "GDD 14"),
      ("Kosmetik", "ausruestung/cosmetic"), ("Einstellungen", "GDD 19.x Nr. 5"), ("Hilfe", "GDD 25.12")]
MCOLS, MSTEPX, MSTEPY = 3, 144, 176
MW = 24 + MCOLS * 120 + (MCOLS - 1) * 24 + 24
MH = 24 + 40 + 3 * 152 + 2 * 24 + 24
MX, MY = 932 + 120 - MW, 1176 - 12 - MH
add("M0", "Mehr-Menue (offen)", MX, MY, MW, MH, "d2_dropdown_liste (9-Slice 72)", None, "mehr",
    "Anker: rechte Kante = S6, 12 px darueber; Kopf 'MEHR' Baloo 22")
for k, (n, src) in enumerate(MT):
    tx = MX + 24 + (k % MCOLS) * MSTEPX; ty = MY + 64 + (k // MCOLS) * MSTEPY
    add(f"M{k+1}", f"Kachel {n}", tx, ty, 120, 120, "d2_btn_quadrat_normal + Label Baloo 20", (tx, ty, 120, 152), "mehr", "Quelle " + src)
# Event-Leiste links (einklappbar)
add("V1", "Event-Knopf (eingeklappt)", 28, 316, 120, 120, "d2_btn_quadrat_normal / _gedrueckt (offen)", (28, 316, 120, 152), "event",
    "Icon 80 (aktuelles Top-Event), Badge = Anzahl laufender Events; Hitbox inkl. Label")
add("V1L", "Label Events", 28, 440, 120, 28, "Text Baloo 800 22", None, "event", "")
add("V1B", "Badge Anzahl Events", 28 + 120 - 4 - 48, 320, 48, 38, "d2_badge_zaehler", None, "badge", "")
EVX, EVY, EVW, EVR = 28, 480, 440, 108
EVN = [("Erntefest", "2T 14:05"), ("Turnier", "5:42:10"), ("Haendler", "47:12"), ("Bauwoche", "6T 03:00"), ("Gilden-Jagd", "1T 08:30")]
add("W0", "Event-Liste (ausgeklappt)", EVX, EVY, EVW, 16 + len(EVN) * EVR + 16, "d2_dropdown_liste (9-Slice 72)", None, "evliste",
    "klappt unter V1 auf, linke Kante = V1; scrollt ab 6 Eintraegen (max. Hoehe bis y 1380)")
for k, (n, t) in enumerate(EVN):
    ry = EVY + 16 + k * EVR
    add(f"W{k+1}", f"Eintrag {n}", EVX + 12, ry, EVW - 24, EVR, "Zeile (antippbar -> Event-Fenster)", None, "evliste", "Trenner d2_dropdown_trenner")
    add(f"W{k+1}I", f"Icon {n}", EVX + 24, ry + 18, 72, 72, "Icon neu D2", None, "evliste", "")
    add(f"W{k+1}N", f"Name {n}", EVX + 112, ry + 14, 300, 40, "Text Baloo 800 28", None, "evliste", "max. 14 Zeichen")
    add(f"W{k+1}T", f"Restzeit {n}", EVX + 112, ry + 58, 300, 36, "Text Lilita 28 + Uhr-Icon 24", None, "evliste", "text.counter, < 1 h = glut")
# Chat + Quest links unten
add("C1", "Chat-Knopf", 28, 1396, 120, 120, "d2_btn_quadrat_normal", None, "left", "Icon 80 innen")
add("C2", "Badge Chat (ungelesen)", 28 + 120 - 4 - 48, 1400, 48, 38, "d2_badge_zaehler", None, "badge", "")
add("Q1", "Quest-Leiste", 28, 1536, 720, 124, "d2_panel_frame (9-Slice)", None, "left",
    "ganze Leiste antippbar; Ende 1660 (16 px vor Platten-Oberkante 1682)")
add("Q2", "Quest-Icon", 28 + 14, 1536 + 14, 96, 96, "Icon neu D2", None, "left", ">= 70 gefordert, 96 gewaehlt")
add("Q3", "Quest-Text", 152, 1552, 452, 40, "Text Lilita 30", None, "left", "1 Zeile, Ellipse '...'")
add("Q4", "Quest-Fortschritt", 152, 1608, 452, 22, "d2_bar_bg + d2_bar_fill_glut", None, "left", "")
add("Q5", "Quest-Zaehler 3/5", 616, 1596, 116, 44, "Text Lilita 32", None, "left", "rechtsbuendig")
# Dock
DY = H - 212
add("D0", "Dock-Hintergrund", 0, DY, 1080, 212, "d2_dock_bg (9-Slice 4/8/4/8)", None, "dock",
    "bottom-anchored, deckt Gestenzone mit")
TABS = ["Dorf", "Helden", "Inventar", "Karte", "Gilde", "Armee"]
TW = 180
for k, n in enumerate(TABS):
    x = k * TW
    add(f"T{k+1}", f"Tab {n}", x, DY, TW, 164, "", (x, DY, TW, 164), "dock", "Hitbox 180x164 (bis Gestenzone)")
    if k == 0:
        add("T1P", "Aktive Platte Dorf", x + 10, DY - 26, 160, 196, "d2_dock_platte_aktiv", None, "dock", "Overlay, ragt 26 hoch (v4: 192 breit -> 160)")
        add("T1I", "Icon Dorf (aktiv)", x + 30, DY - 22, 120, 112, "Icon neu D2", None, "dock", "")
        add("T1T", "Label Dorf (aktiv)", x + 10, DY + 104, 160, 44, "Lilita 34 #FFF3D6", None, "dock", "")
        add("T1S", "Indikator", x + 60, DY + 152, 60, 8, "d2_dock_indikator", None, "dock", "")
    else:
        add(f"T{k+1}I", f"Icon {n}", x + 42, DY + 14, 96, 88, "Icon neu D2", None, "dock", "")
        add(f"T{k+1}T", f"Label {n}", x + 10, DY + 106, 160, 38, "Lilita 30 #BFAE8E", None, "dock", "")
add("T2B", "Badge Helden", TW + TW - 10 - 48, DY + 8, 48, 38, "d2_badge_zaehler", None, "badge", "innen im Tab")
add("T5B", "Badge Gilde", 4 * TW + TW - 10 - 48, DY + 8, 48, 38, "d2_badge_zaehler", None, "badge", "Spende/Jagd offen")
add("G1", "Gestenleiste (System)", 390, H - 24, 300, 10, "System", None, "sys", "nicht antippbar")

GRPCOL = {"top": (255, 138, 42), "side": (63, 224, 208), "event": (255, 177, 90), "left": (181, 123, 255),
          "dock": (155, 227, 122), "liste": (255, 240, 120), "evliste": (120, 220, 255), "sidel": (120, 200, 160), "mehr": (255, 150, 220), "badge": (255, 106, 90), "sys": (200, 200, 200)}

SWATCH = [("bg.base", "#120E0C"), ("panel.top", "#2C201A"), ("panel.bottom", "#120D0B"),
          ("line.bronze", "#C98A4A"), ("line.bronze.light", "#C9A96E"), ("line.muted", "#8A7656"),
          ("line.dark", "#7A664E"), ("text.counter", "#A89674"), ("glut", "#FF8A2A"),
          ("glut.deep", "#E0601A"), ("glut.light", "#FFB15A"), ("glut.text", "#FFD9A8"),
          ("glut.plus", "#FFD27A"), ("text.main", "#F3E7CF"), ("text.muted", "#B9A988"),
          ("text.bone", "#EADFC6"), ("ink", "#0B0908"), ("ink.brown", "#2A1206"),
          ("accent.moon", "#3FE0D0"), ("state.plus", "#9BE37A"), ("state.missing", "#FF6A5A"),
          ("dock.bottom", "#080604"), ("dock.label", "#BFAE8E"), ("dock.label.aktiv", "#FFF3D6"),
          ("dock.platte", "#FF963C")]

# ---------------------------------------------------------------- Checks
def inter(a, b):
    return not (a[0] + a[2] <= b[0] or b[0] + b[2] <= a[0] or a[1] + a[3] <= b[1] or b[1] + b[3] <= a[1])

def checks():
    msgs = []
    inter_ids = {"A1", "R1", "R2", "R3", "R4", "K1", "L1", "L2", "L3", "W1", "W2", "W3", "W4", "W5", "S1", "S2", "S3", "S4", "S5", "S6", "B1", "H1", "H2", "H3", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "V1", "C1", "Q1",
                 "T1", "T2", "T3", "T4", "T5", "T6"}
    hb = [e for e in E if e["id"] in inter_ids]
    for e in hb:
        x, y, w, h = e["hit"]
        if min(w, h) < TOUCH_MIN: msgs.append(f"TOUCH<{TOUCH_MIN}: {e['id']} {w}x{h}")
        if e["grp"] != "dock" and (y < SAFE_TOP or y + h > H - 212):
            msgs.append(f"SAFE: {e['id']}")
        if e["grp"] == "dock" and y + h > H - SAFE_BOT: msgs.append(f"GESTE: {e['id']}")
        if x < 0 or x + w > W: msgs.append(f"RAND: {e['id']}")
    for i, a in enumerate(hb):
        for b in hb[i + 1:]:
            if a["grp"] != b["grp"] and ({a["grp"], b["grp"]} & {"liste", "evliste", "mehr"}): continue  # Listen = Overlay (nie gleichzeitig offen)
            if inter(a["hit"], b["hit"]): msgs.append(f"HITBOX-UEBERLAPP {a['id']}/{b['id']}")
    for e in E:
        if e["grp"] in ("liste", "evliste", "mehr") and e["y"] + e["h"] > 1676: msgs.append(f"LISTE-UEBER-DOCK {e['id']}")
    vis = [e for e in E if e["grp"] in ("top", "side", "sidel", "event", "left", "liste", "evliste", "mehr") and len(e["id"]) == 2]
    for i, a in enumerate(vis):
        for b in vis[i + 1:]:
            r1 = (a["x"], a["y"], a["w"], a["h"]); r2 = (b["x"], b["y"], b["w"], b["h"])
            inside = lambda p, q: p[0] >= q[0] and p[1] >= q[1] and p[0] + p[2] <= q[0] + q[2] and p[1] + p[3] <= q[1] + q[3]
            if a["grp"] != b["grp"] and ({a["grp"], b["grp"]} & {"liste", "evliste", "mehr"}): continue
            if inter(r1, r2) and not (inside(r1, r2) or inside(r2, r1)): msgs.append(f"SICHT-UEBERLAPP {a['id']}/{b['id']}")
    return msgs

# ---------------------------------------------------------------- Plan
def hexrgb(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))

def draw_plan():
    LW = 1120
    img = Image.new("RGB", (W + LW, H), (24, 20, 18))
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 0, W - 1, H - 1], fill=(46, 40, 36))
    for x in range(0, W, 10):
        d.line([x, 0, x, H], fill=(255, 255, 255, 40 if x % 40 == 0 else 12))
    for y in range(0, H, 10):
        d.line([0, y, W, y], fill=(255, 255, 255, 40 if y % 40 == 0 else 12))
    f12 = font("baloo", 14); f16 = font("baloo", 17); f20 = font("baloo", 20); fl = font("lilita", 22)
    for y in range(0, H, 160):
        d.text((2, y + 2), str(y), font=f12, fill=(220, 220, 220))
    for x in range(160, W, 160):
        d.text((x + 2, 2), str(x), font=f12, fill=(220, 220, 220))
    # Safe areas (schraffiert)
    for (y0, y1, t) in [(0, SAFE_TOP, f"Safe-Top / Notch 0-{SAFE_TOP}"), (H - SAFE_BOT, H, f"Gestenzone {H-SAFE_BOT}-{H}")]:
        d.rectangle([0, y0, W, y1 - 1], fill=(255, 60, 60, 60))
        for s in range(-H, W + H, 24):
            d.line([s, y1, s + (y1 - y0), y0], fill=(255, 80, 80, 90), width=2)
        d.text((720, y0 + 12 if y0 == 0 else y0 + 2), t, font=f20, fill=(255, 220, 220))
    d.line([MARGIN, 0, MARGIN, H], fill=(255, 255, 0, 90)); d.line([W - MARGIN, 0, W - MARGIN, H], fill=(255, 255, 0, 90))
    d.line([0, 1676, W, 1676], fill=(255, 255, 0, 120))
    d.text((360, 1662), "Freiraum-Linie 1676 / Platte ab 1682", font=f12, fill=(255, 255, 120))
    d.text((360, 1300), "Dorf-Freiflaeche (Kamera, Gebaeude)  x 352-920 / y 330-1380", font=f16, fill=(200, 200, 200))
    order = sorted(E, key=lambda e: (e["grp"] != "dock" or e["id"] != "D0", e["w"] * e["h"]), reverse=False)
    order = sorted(E, key=lambda e: -e["w"] * e["h"])
    for e in order:
        c = GRPCOL[e["grp"]]
        x, y, w, h = e["x"], e["y"], e["w"], e["h"]
        if e["hit"] != [x, y, w, h]:
            hx, hy, hw, hh = e["hit"]
            for s in range(hx, hx + hw, 8): d.line([s, hy, min(s + 4, hx + hw), hy], fill=c + (200,))
            for s in range(hx, hx + hw, 8): d.line([s, hy + hh - 1, min(s + 4, hx + hw), hy + hh - 1], fill=c + (200,))
            for s in range(hy, hy + hh, 8): d.line([hx, s, hx, min(s + 4, hy + hh)], fill=c + (200,))
            for s in range(hy, hy + hh, 8): d.line([hx + hw - 1, s, hx + hw - 1, min(s + 4, hy + hh)], fill=c + (200,))
        if e["id"] in ("D0",) or e["id"][0] == "T" and len(e["id"]) == 2:
            d.rectangle([x, y, x + w - 1, y + h - 1], outline=c + (255,), width=2)
            continue
        if e["grp"] in ("liste", "evliste"): continue  # in v5-Plan ausgeblendet (Masse unveraendert, s. v3/JSON)
        if e["grp"] == "mehr":
            d.rectangle([x, y, x + w - 1, y + h - 1], fill=c + (30 if e["id"] == "L0" else 18,), outline=c + (255,), width=2)
            continue
        d.rectangle([x, y, x + w - 1, y + h - 1], fill=c + (55,), outline=c + (255,), width=2)
    # Beschriftung: ID-Tag + Kurzmass bei grossen Boxen
    for e in E:
        c = GRPCOL[e["grp"]]
        x, y, w, h = e["x"], e["y"], e["w"], e["h"]
        tag = e["id"]
        if e["id"] == "D0": tx, ty = 900, y + 4
        elif e["id"][0] == "T" and len(e["id"]) == 2: tx, ty = x + 4, y + 168 - 22
        elif e["id"] in ("T1T",): tx, ty = x + 4, y + 2
        elif e["id"] in ("G1",): tx, ty = x + w + 6, y - 6
        elif e["id"] in ("Q1", "L0", "W0", "M0"): tx, ty = x + w - 34, y + h - 20
        elif e["id"][0] in "LW" and len(e["id"]) == 2: tx, ty = x + 4, y + h - 18
        elif w < 70: tx, ty = x + 2, y + 2
        else: tx, ty = x + 4, y + 2
        if e["grp"] in ("liste", "evliste"): continue
        tb = d.textbbox((tx, ty), tag, font=f12)
        d.rectangle([tb[0] - 2, tb[1] - 1, tb[2] + 2, tb[3] + 1], fill=(0, 0, 0, 200))
        d.text((tx, ty), tag, font=f12, fill=c)
        if w >= 200 and h >= 60 and e["id"] not in ("D0",) and not (e["id"][0] == "T" and len(e["id"]) == 2) and e["id"] not in ("T1P", "Q1", "L0", "W0", "M0") and e["grp"] not in ("liste", "mehr"):
            s1 = e["name"]; s2 = f"{x},{y}  {w}x{h}"
            d.text((x + 8, y + 18), s1, font=f16, fill=(255, 255, 255))
            d.text((x + 8, y + 38), s2, font=f16, fill=(255, 255, 255))
    # Legende
    lx = W + 24
    d.text((lx, 20), "Massplan Dorf-HUD D2 \"Obsidian & Glut\" v5", font=font("lilita", 36), fill=(255, 217, 168))
    d.text((lx, 66), "1080x1920 · Raster 10/40 · Safe Top 90 · Geste 48 · Rand 28 · Touch >= 96 (Ziel 120)",
           font=f16, fill=(220, 210, 190))
    d.text((lx, 88), "Box = sichtbar · gestrichelt = Hitbox · rosa = Mehr-Menue offen · Res./Ev.-Liste nur in Legende (Bild s. v3) · px ab oben links",
           font=f16, fill=(220, 210, 190))
    y = 118
    d.text((lx, y), "ID    Element                               x      y      w      h", font=f16, fill=(255, 177, 90)); y += 24
    d.text((lx + 570, y - 24), "Hitbox (HB) / Sprite", font=f16, fill=(255, 177, 90))
    for e in E:
        if e["id"][:2] in ("L2", "L3", "W2", "W3", "W4", "W5") and len(e["id"]) > 2: continue
        if re.fullmatch(r"(S\dL|H\dL|B1L|B1B|V1L|T[2-6][IT]|T[3-6]|S\dB|H\dB|M[2-9])", e["id"]): continue  # Labels/Badges/Tabs: Schema s. Fussnote + JSON  # gleich L1*, je +120 y (s. JSON)
        c = GRPCOL[e["grp"]]
        d.rectangle([lx, y + 4, lx + 12, y + 16], fill=c)
        d.text((lx + 18, y), e["id"], font=f16, fill=c)
        d.text((lx + 66, y), e["name"][:30], font=f16, fill=(235, 225, 205))
        for j, v in enumerate((e["x"], e["y"], e["w"], e["h"])):
            s = str(v); tw = d.textlength(s, font=f16)
            d.text((lx + 370 + j * 58 - tw, y), s, font=f16, fill=(235, 225, 205))
        hb = "" if e["hit"] == [e["x"], e["y"], e["w"], e["h"]] else "HB %d,%d %dx%d " % tuple(e["hit"])
        extra = (hb + e["sprite"])[:58]
        if e["id"] in ("L2", "L3"): extra = "Inhalt wie L1I..L1C, y +%d" % ((int(e["id"][1]) - 1) * 120)
        if e["id"] in ("W2", "W3", "W4", "W5"): extra = "Inhalt wie W1I..W1T, y +%d" % ((int(e["id"][1]) - 1) * EVR)
        d.text((lx + 570, y), extra, font=font("baloo", 15), fill=(180, 170, 150))
        y += 19
    d.text((lx, y + 2), "ohne Zeile: Labels xL: y+124, 120x28 (S1L/H1L 140) · Badges xB = x+68, y+4, 48x38 · Tabs T3-T6 wie T2 (+180) · Kacheln M2-M9 wie M1 (+144 / Zeile +176) · alles in JSON", font=font("baloo", 15), fill=(180, 170, 150)); y += 20
    y += 14
    d.text((lx, y), "Farben (vorlage_D2.md Abschnitt 3 + Dock-Toenung)", font=fl, fill=(255, 217, 168)); y += 34
    for k, (n, hx) in enumerate(SWATCH):
        cx = lx + (k % 4) * 270; cy = y + (k // 4) * 46
        d.rounded_rectangle([cx, cy, cx + 40, cy + 38], 6, fill=hexrgb(hx), outline=(120, 110, 100))
        d.text((cx + 48, cy - 1), n, font=f16, fill=(235, 225, 205))
        d.text((cx + 48, cy + 18), hx, font=f16, fill=(180, 170, 150))
    y += ((len(SWATCH) + 3) // 4) * 46 + 10
    d.text((lx, y), "Gruppen:", font=f16, fill=(235, 225, 205))
    gx = lx + 80
    for g, n in [("top", "Top-Leiste"), ("side", "Seite"), ("event", "Event"), ("left", "Quest"), ("dock", "Dock"), ("badge", "Badge"), ("sidel", "Links"), ("liste", "Res."), ("evliste", "Ev."), ("mehr", "Mehr")]:
        d.rectangle([gx, y + 4, gx + 14, y + 18], fill=GRPCOL[g]); d.text((gx + 20, y), n, font=f16, fill=(235, 225, 205)); gx += 104
    y += 30
    msgs = checks()
    d.text((lx, y), "Pruefung (Skript): " + ("0 Befunde - Touch, Safe Area, Ueberlappung OK" if not msgs else "; ".join(msgs)[:110]),
           font=f16, fill=(155, 227, 122) if not msgs else (255, 106, 90))
    assert y < H - 30, y
    img.save(os.path.join(OUT, "massplan_hud_d2_v5.png"))
    return msgs

# ---------------------------------------------------------------- Bausteine
def sprite(name): return Image.open(os.path.join(EXP, name + ".png")).convert("RGBA")

def nine(name, w, h):
    m = MAN[name + ".png"]; im = sprite(name)
    pl, pt, pr, pb = m["pad_ltrb"]; tw, th = w + pl + pr, h + pt + pb
    sl = m["slice_ltrb"]
    if not sl or (im.size == (tw, th)):
        return im.resize((tw, th), Image.LANCZOS) if im.size != (tw, th) else im, pl, pt
    L, Tt, R, B = sl; sw, sh = im.size
    out = Image.new("RGBA", (tw, th))
    xs = [(0, L, 0, L), (L, sw - R, L, tw - R), (sw - R, sw, tw - R, tw)]
    ys = [(0, Tt, 0, Tt), (Tt, sh - B, Tt, th - B), (sh - B, sh, th - B, th)]
    for sx0, sx1, dx0, dx1 in xs:
        for sy0, sy1, dy0, dy1 in ys:
            if dx1 <= dx0 or dy1 <= dy0 or sx1 <= sx0 or sy1 <= sy0: continue
            out.paste(im.crop((sx0, sy0, sx1, sy1)).resize((dx1 - dx0, dy1 - dy0), Image.LANCZOS), (dx0, dy0))
    return out, pl, pt

def place(base, name, x, y, w, h):
    s, pl, pt = nine(name, w, h); base.alpha_composite(s, (x - pl, y - pt))

def text_c(d, box, s, f, fill, stroke=3, anchor="mm"):
    x, y, w, h = box
    d.text((x + w / 2, y + h / 2), s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0))

def ph_icon(base, x, y, w, h, label="Icon"):
    """neutraler Glyph-Platzhalter, markiert 'Icon neu D2'"""
    lay = Image.new("RGBA", base.size); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([x, y, x + w - 1, y + h - 1], 10, fill=(60, 52, 46, 200), outline=(234, 223, 198, 200), width=2)
    for s in range(x + 6, x + w - 4, 10):
        d.line([s, y + 3, s + 4, y + 3], fill=(234, 223, 198, 140))
    fs = max(12, min(22, w // 5))
    f = font("baloo", fs)
    d.text((x + w / 2, y + h / 2 - fs * 0.55), label, font=f, fill=(234, 223, 198), anchor="mm")
    d.text((x + w / 2, y + h / 2 + fs * 0.55), "neu D2", font=f, fill=(255, 210, 122), anchor="mm")
    base.alpha_composite(lay)

def draw_blocks(offen=None, name="massplan_hud_d2_v5_bloecke.png"):
    bg = Image.open(VILLAGE).convert("RGB")
    s = 1920 / 2600
    bg = bg.crop((1300, 1100, 1300 + int(1080 / s), 1100 + 2600)).resize((W, H), Image.LANCZOS)
    bg = ImageEnhance.Brightness(ImageEnhance.Color(bg).enhance(0.6)).enhance(0.55)
    base = bg.convert("RGBA"); bf28 = font("baloo", 28)
    if offen:  # Scrim ueber der Welt (nicht ueber dem Dock): Tipp schliesst die Liste
        sc = Image.new("RGBA", base.size); ImageDraw.Draw(sc).rectangle([0, 0, W, H - 212], fill=(10, 8, 7, 110))
        base.alpha_composite(sc)
    d = ImageDraw.Draw(base, "RGBA")
    g = {e["id"]: e for e in E}
    R = lambda i: (g[i]["x"], g[i]["y"], g[i]["w"], g[i]["h"])
    # Top-Leiste Hintergrund-Verlauf (Lesbarkeit), ab 0 inkl. Notch
    lay = Image.new("RGBA", base.size); dl = ImageDraw.Draw(lay)
    for yy in range(0, 300):
        dl.line([0, yy, W, yy], fill=(8, 6, 4, int(170 * max(0, 1 - yy / 300) ** 1.5)))
    base.alpha_composite(lay); d = ImageDraw.Draw(base, "RGBA")
    lf40 = font("lilita", 40); lf30 = font("lilita", 30); lf26 = font("lilita", 26); bf22 = font("baloo", 22)
    # Avatar
    x, y, w, h = R("A1"); place(base, "d2_panel_frame", x, y, w, h)
    d.ellipse([x + 12, y + 12, x + w - 12, y + h - 12], fill=(90, 70, 58), outline=(201, 138, 74), width=3)
    d.text((x + w / 2, y + h / 2 - 8), "Portraet", font=font("baloo", 18), fill=(234, 223, 198), anchor="mm")
    x, y, w, h = R("A2"); place(base, "d2_badge_stufe", x, y, w, h)
    text_c(d, (x, y, w, h), "12", lf26, (243, 231, 207), 2)
    vals = {"R1": "1.250", "R3": "8.215", "R4": "45.600"}
    for i, v in vals.items():
        x, y, w, h = R(i); place(base, "d2_pill_ressource", x, y, w, h)
        ph_icon(base, x + 8, y + 8, 64, 64)
        d.text((x + 84, y + h / 2), v, font=lf40, fill=(243, 231, 207), anchor="lm", stroke_width=2, stroke_fill=(0, 0, 0))
        assert d.textlength(v, font=lf40) <= w - 84 - 12, i
    x, y, w, h = R("R2"); place(base, "d2_btn_plus_pill", x, y, w, h)
    pl = sprite("d2_ico_plus").resize((48, 48), Image.LANCZOS)
    base.alpha_composite(pl, (x + 16, y + 16))
    x, y, w, h = R("K1"); place(base, "d2_btn_quadrat_gedrueckt" if offen == "res" else "d2_btn_quadrat_normal", x, y, w, h)
    ph_icon(base, x + 16, y + 16, 72, 72, "Kiste")
    # Seitenknoepfe
    for i, lab, side in [(a, b, "l") for a, b in LEFT] + [(a, b, "r") for a, b in SIDE] + [("B1", "Bauen", "r")]:
        x, y, w, h = R(i)
        if i == "S1":
            gl = Image.new("RGBA", base.size); gd = ImageDraw.Draw(gl)
            for r, a_ in ((12, 50), (8, 90), (4, 160)):
                gd.rounded_rectangle([x - r, y - r, x + w + r, y + h + r], 28 + r, outline=(255, 154, 60, a_), width=4)
            base.alpha_composite(gl)
        place(base, "d2_btn_quadrat_gedrueckt" if (i == "S6" and offen == "mehr") else "d2_btn_quadrat_normal", x, y, w, h)
        ph_icon(base, x + 20, y + 20, 80, 80)
        text_c(d, R(i + "L"), lab, bf22, (255, 217, 168) if i == "S1" else (234, 223, 198), 3)
        assert d.textlength(lab, font=bf22) <= R(i + "L")[2], lab
        if i in BADGE:
            bx, by, bw, bh = R(i + "B"); place(base, "d2_badge_zaehler", bx, by, bw, bh)
            text_c(d, (bx, by, bw, bh), BADGE[i], font("lilita", 24), (255, 255, 255), 2)
    # Event-Knopf
    x, y, w, h = R("V1"); place(base, "d2_btn_quadrat_gedrueckt" if offen == "ev" else "d2_btn_quadrat_normal", x, y, w, h)
    ph_icon(base, x + 20, y + 20, 80, 80)
    text_c(d, R("V1L"), "Events", bf22, (234, 223, 198), 3)
    bx, by, bw, bh = R("V1B"); place(base, "d2_badge_zaehler", bx, by, bw, bh)
    text_c(d, (bx, by, bw, bh), str(len(EVN)), font("lilita", 24), (255, 255, 255), 2)
    # Chat
    x, y, w, h = R("C1"); place(base, "d2_btn_quadrat_normal", x, y, w, h); ph_icon(base, x + 20, y + 20, 80, 80)
    bx, by, bw, bh = R("C2"); place(base, "d2_badge_zaehler", bx, by, bw, bh)
    text_c(d, (bx, by, bw, bh), "5", font("lilita", 24), (255, 255, 255), 2)
    # Quest
    x, y, w, h = R("Q1"); place(base, "d2_panel_frame", x, y, w, h)
    ph_icon(base, *R("Q2"))
    qx, qy, qw, qh = R("Q3")
    d.text((qx, qy + qh / 2), "Holzfaeller auf Stufe 2", font=lf30, fill=(243, 231, 207), anchor="lm", stroke_width=2, stroke_fill=(0, 0, 0))
    bx, by, bw, bh = R("Q4"); place(base, "d2_bar_bg", bx, by, bw, bh)
    place(base, "d2_bar_fill_glut", bx, by, int(bw * 0.6), bh)
    zx, zy, zw, zh = R("Q5")
    d.text((zx + zw, zy + zh / 2), "3/5", font=font("lilita", 32), fill=(255, 217, 168), anchor="rm", stroke_width=2, stroke_fill=(0, 0, 0))
    # Liste (offen)
    if offen == "ev":
        x, y, w, h = R("W0"); place(base, "d2_dropdown_liste", x, y, w, h)
        for k, (n, t) in enumerate(EVN, start=1):
            rx, ry, rw, rh = R(f"W{k}")
            if k > 1: place(base, "d2_dropdown_trenner", rx + 12, ry - 1, rw - 24, 2)
            ph_icon(base, *R(f"W{k}I"))
            nx, ny, nw, nh = R(f"W{k}N"); d.text((nx, ny + nh / 2), n, font=bf28, fill=(243, 231, 207), anchor="lm")
            assert d.textlength(n, font=bf28) <= nw
            tx, ty, tw, th = R(f"W{k}T"); kurz = ":" in t and "T" not in t and t.count(":") == 1
            col = (255, 154, 60) if kurz else (168, 150, 116)
            d.ellipse([tx, ty + 6, tx + 24, ty + 30], outline=col, width=3)
            d.line([tx + 12, ty + 11, tx + 12, ty + 18, tx + 17, ty + 21], fill=col, width=3)
            d.text((tx + 34, ty + th / 2), t, font=font("lilita", 28), fill=col, anchor="lm", stroke_width=2, stroke_fill=(0, 0, 0))
    if offen == "mehr":
        x, y, w, h = R("M0"); place(base, "d2_dropdown_liste", x, y, w, h)
        d.text((x + 24, y + 44), "M E H R", font=bf22, fill=(185, 169, 136), anchor="lm")
        f20 = font("baloo", 20)
        for k, (n, _) in enumerate(MT, start=1):
            tx, ty, tw, th = R(f"M{k}"); place(base, "d2_btn_quadrat_normal", tx, ty, tw, th); ph_icon(base, tx + 20, ty + 20, 80, 80)
            assert d.textlength(n, font=f20) <= 140, n
            text_c(d, (tx - 10, ty + 124, 140, 28), n, f20, (234, 223, 198), 3)
    if offen == "res":
        x, y, w, h = R("L0"); place(base, "d2_dropdown_liste", x, y, w, h)
        hx, hy, hw, hh = R("L0H")
        d.text((hx, hy + hh / 2), "L A G E R", font=font("baloo", 22), fill=(185, 169, 136), anchor="lm")
        data = [("Holz", 12480, 20000), ("Stein", 8215, 20000), ("Nahrung", 14900, 14900)]
        for k, (n, v, cap) in enumerate(data, start=1):
            rx, ry, rw, rh = R(f"L{k}")
            if k > 1: place(base, "d2_dropdown_trenner", rx + 12, ry - 1, rw - 24, 2)
            ph_icon(base, *R(f"L{k}I"))
            nx, ny, nw, nh = R(f"L{k}N"); d.text((nx, ny + nh / 2), n, font=bf28, fill=(243, 231, 207), anchor="lm")
            bx, by, bw, bh = R(f"L{k}B"); place(base, "d2_bar_bg", bx, by, bw, bh)
            place(base, "d2_bar_fill_glut", bx, by, max(30, int(bw * v / cap)), bh)
            fv = f"{v:,}".replace(",", "."); fc = "/ " + f"{cap:,}".replace(",", ".") + (" voll" if v >= cap else "")
            wx, wy, ww, wh = R(f"L{k}W")
            d.text((wx + ww, wy + wh / 2), fv, font=font("lilita", 36), fill=(243, 231, 207), anchor="rm", stroke_width=2, stroke_fill=(0, 0, 0))
            assert d.textlength(fv, font=font("lilita", 36)) <= ww
            qx, qy, qw, qh = R(f"L{k}C")
            d.text((qx + qw, qy + qh / 2), fc, font=font("baloo", 22), fill=(255, 106, 90) if v >= cap else (168, 150, 116), anchor="rm")
            assert d.textlength(fc, font=font("baloo", 22)) <= qw
    # Dock
    d.rectangle([0, H - SAFE_BOT, W, H], fill=(8, 6, 4, 255))
    x, y, w, h = R("D0"); place(base, "d2_dock_bg", x, y, w, h)
    x, y, w, h = R("T1P"); place(base, "d2_dock_platte_aktiv", x, y, w, h)
    ph_icon(base, *R("T1I"))
    text_c(d, R("T1T"), "Dorf", font("lilita", 34), (255, 243, 214), 3)
    place(base, "d2_dock_indikator", *R("T1S"))
    for k, n in enumerate(TABS[1:], start=2):
        ph_icon(base, *R(f"T{k}I")); text_c(d, R(f"T{k}T"), n, lf30, (191, 174, 142), 2)
        assert d.textlength(n, font=lf30) <= R(f"T{k}T")[2] - 12, n
    for bid, bt in (("T2B", "2"), ("T5B", "1")):
        bx, by, bw, bh = R(bid); place(base, "d2_badge_zaehler", bx, by, bw, bh)
        text_c(d, (bx, by, bw, bh), bt, font("lilita", 24), (255, 255, 255), 2)
    x, y, w, h = R("G1"); d.rounded_rectangle([x, y, x + w, y + h], 5, fill=(200, 191, 170, 255))
    d.text((W - 24, H - 300 - 1440 + 1440), "", font=bf22)
    base.convert("RGB").save(os.path.join(OUT, name))

if __name__ == "__main__":
    msgs = draw_plan(); draw_blocks(); draw_blocks("mehr", "massplan_hud_d2_v5_bloecke_mehr.png")
    json.dump(dict(canvas=[W, H], safe_top=SAFE_TOP, safe_bottom=SAFE_BOT, touch_min=TOUCH_MIN, elemente=E),
              open(os.path.join(OUT, "massplan_hud_d2_v5_elemente.json"), "w"), indent=1, ensure_ascii=False)
    print("Befunde:", msgs or "0")
