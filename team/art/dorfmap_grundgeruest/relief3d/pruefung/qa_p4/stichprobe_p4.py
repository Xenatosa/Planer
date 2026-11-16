#!/usr/bin/env python3
"""QA P4 Stichprobe G6_facette / G5_beule_klippe mit Nahbildern (wiederholbar, z. B. auf dem L1-Ergebnis).

Ablauf:
 1. Trefferliste lesen (Standard: RELIEF3D/pruefung/regeln_letzter_lauf.json; mit --neu-pruefen wird
    pruefe_regeln.py frisch auf den Hoehendaten gerechnet, Schwellen/Pruefer unveraendert).
 2. Je Regel und Kachel bis zu N Stichproben: schlimmste Werte zuerst, Mindestabstand --abstand m,
    damit nicht 5 Punkte desselben Clusters gezogen werden (Rest wird mit den naechstschlimmsten aufgefuellt).
 3. Voll-Viewer bauen (baue_vollansicht.py -> /tmp, ganze Karte aus main.js + Hoehendaten) und
    je Stichprobe rendern mit dem unveraenderten Repo-Renderer pruefung/o18/render_t119u.js:
      A = Spielkamera flach (aus Sueden wie Startansicht 'schraeg', 35 Grad, 35 m, Textur)
      B = Detail steil (60 Grad, 16 m, Textur)
      C = Detail steil Clay (reine Form)
      D = optional (--nah) Spielkamera nah, 35 Grad, 15 m, Textur
    Der Treffer liegt jeweils in der Bildmitte (rote Eckmarken).
 4. Komposit-JPG je Stichprobe + stichprobe.json + TABELLE_ROH.md (Urteil-Spalte leer, Sichtung von Hand).

Aufruf (Ausgangsstand):
  python3 stichprobe_p4.py --relief3d ../.. --label 8e374b0 --out bilder_8e374b0
Wiederholung auf L1 (Worktree/Commit des L1-Ergebnisses):
  python3 stichprobe_p4.py --relief3d /pfad/zum/L1-worktree/team/art/dorfmap_grundgeruest/relief3d \
      --label L1_<commit> --out bilder_L1_<commit> --neu-pruefen
  optional --daten /pfad/relief_daten.json.gz (andere Hoehendaten), --treffer eigene.json, --html fertiger Voll-Viewer.
Voraussetzung: NODE_PATH mit playwright (Standard /tmp/w3/node_modules), python3 mit numpy/scipy/skimage/PIL.
"""
import argparse, json, math, os, subprocess, sys, tempfile, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HIER = Path(__file__).resolve().parent
NAH = False
REGELN = ('G6_facette', 'G5_beule_klippe')
KACHELN = ('C5', 'C3', 'C4', 'D4', 'B4')
KURZ = {'G6_facette': 'G6', 'G5_beule_klippe': 'G5'}


def auswahl(treffer, n, abstand):
    out = []
    for r in REGELN:
        for k in KACHELN:
            alle = sorted([t for t in treffer if t['regel'] == r and t['feld'] == k], key=lambda t: (-abs(float(t['wert'])), t['x'], t['z']))
            wahl, rest = [], []
            for t in alle:
                if len(wahl) >= n: break
                (rest if any(math.hypot(t['x'] - w['x'], t['z'] - w['z']) < abstand for w in wahl) else wahl).append(t)
            for t in rest:
                if len(wahl) >= n: break
                wahl.append(t)
            for i, t in enumerate(wahl, 1):
                out.append(dict(id=f"{KURZ[r]}_{k}_{i}", regel=r, kachel=k, x=t['x'], z=t['z'], wert=t['wert'], rang_wert=alle.index(t) + 1, anzahl_kachel=len(alle)))
    return out


def kameras(st):
    cams = []
    for s in st:
        x, z = s['x'], s['z']
        # rel=1: y relativ zur Gelaendehoehe am Ziel (__test.H)
        cams.append(dict(n=s['id'] + '_A', pos=[x, 35 * math.sin(math.radians(35)), z + 35 * math.cos(math.radians(35))], ziel=[x, 0, z], rel=1))
        if NAH: cams.append(dict(n=s['id'] + '_D', pos=[x, 15 * math.sin(math.radians(35)), z + 15 * math.cos(math.radians(35))], ziel=[x, 0, z], rel=1))
        cams.append(dict(n=s['id'] + '_B', pos=[x, 16 * math.sin(math.radians(60)), z + 16 * math.cos(math.radians(60))], ziel=[x, 0, z], rel=1))
    return cams


def marke(im):
    d = ImageDraw.Draw(im); w, h = im.size; cx, cy = w // 2, h // 2; g, l = 18, 12
    for sx in (-1, 1):
        for sy in (-1, 1):
            d.line([(cx + sx * g, cy + sy * g), (cx + sx * (g + l), cy + sy * g)], fill=(230, 20, 20), width=2)
            d.line([(cx + sx * g, cy + sy * g), (cx + sx * g, cy + sy * (g + l))], fill=(230, 20, 20), width=2)
    return im


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--relief3d', required=True, type=Path)
    ap.add_argument('--label', required=True)
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--daten', type=Path)
    ap.add_argument('--treffer', type=Path)
    ap.add_argument('--neu-pruefen', action='store_true')
    ap.add_argument('--html', type=Path)
    ap.add_argument('--n', type=int, default=5)
    ap.add_argument('--abstand', type=float, default=3.0)
    ap.add_argument('--node-path', default=os.environ.get('NODE_PATH', '/tmp/w3/node_modules'))
    ap.add_argument('--groesse', default='960x680')
    ap.add_argument('--nah', action='store_true', help='zusaetzlich D = Spielkamera nah (35 Grad, 15 m) als <id>_nah.jpg')
    a = ap.parse_args()
    global NAH; NAH = a.nah
    r3d = a.relief3d.resolve(); out = a.out if a.out.is_absolute() else (HIER / a.out); out.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix=f'qa_p4_{a.label}_'))
    daten = (a.daten or r3d / 'relief_daten.json.gz').resolve()
    if a.treffer: tf = a.treffer
    elif a.neu_pruefen:
        tf = tmp / 'regeln.json'
        subprocess.run([sys.executable, str(r3d / 'pruefung/pruefe_regeln.py'), str(daten), str(tf)], cwd=r3d, env={**os.environ, 'LOCHSCAN': '/nonexistent'})
    else: tf = r3d / 'pruefung/regeln_letzter_lauf.json'
    T = json.load(open(tf))['treffer']
    zahl = {r: sum(t['regel'] == r for t in T) for r in REGELN}
    zahl_k = {r: {k: sum(t['regel'] == r and t['feld'] == k for t in T) for k in KACHELN} for r in REGELN}
    st = auswahl(T, a.n, a.abstand)
    html = a.html
    if not html:
        html = tmp / 'voll.html'
        subprocess.run([sys.executable, str(HIER / 'baue_vollansicht.py'), str(r3d), str(html), str(daten)], check=True)
    cams = kameras(st); cf = tmp / 'cams.json'; cf.write_text(json.dumps(cams))
    cf_c = tmp / 'cams_clay.json'; cf_c.write_text(json.dumps([c for c in cams if c['n'].endswith('_B')]))
    W, H = a.groesse.split('x'); env = {**os.environ, 'NODE_PATH': a.node_path}
    rnd = r3d / 'pruefung/o18/render_t119u.js'
    subprocess.run(['node', str(rnd), str(html), str(tmp / 'tex'), str(cf), '?manual=1&nosh=1', W, H], cwd=r3d, env=env, check=True)
    subprocess.run(['node', str(rnd), str(html), str(tmp / 'clay'), str(cf_c), '?clay=1&manual=1&nosh=1', W, H], cwd=r3d, env=env, check=True)
    # Layout: oben A gross (Spielansicht, Urteilsgrundlage), unten B | C halb so gross
    try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
    except Exception: font = ImageFont.load_default()
    for s in st:
        A = Image.open(tmp / 'tex' / f"{s['id']}_A.png").convert('RGB').resize((820, 580), Image.LANCZOS)
        B = Image.open(tmp / 'tex' / f"{s['id']}_B.png").convert('RGB').resize((410, 290), Image.LANCZOS)
        C = Image.open(tmp / 'clay' / f"{s['id']}_B.png").convert('RGB').resize((410, 290), Image.LANCZOS)
        kom = Image.new('RGB', (820, 22 + 580 + 20 + 290), (255, 255, 255)); d = ImageDraw.Draw(kom)
        d.text((6, 3), f"{s['id']}  {s['regel']} {s['kachel']}  x={s['x']} z={s['z']}  Wert={s['wert']}   [{a.label}]   A: Spielkamera flach 35° (Textur)", fill=(150, 0, 0), font=font)
        kom.paste(marke(A), (0, 22))
        d.text((6, 22 + 580 + 3), 'B: Detail steil 60° (Textur)', fill=(0, 0, 0), font=font); d.text((416, 22 + 580 + 3), 'C: Detail steil 60° (Clay, reine Form)', fill=(0, 0, 0), font=font)
        kom.paste(marke(B), (0, 22 + 580 + 20)); kom.paste(marke(C), (410, 22 + 580 + 20))
        if NAH:
            D = marke(Image.open(tmp / 'tex' / f"{s['id']}_D.png").convert('RGB').resize((820, 580), Image.LANCZOS))
            ImageDraw.Draw(D).text((6, 3), f"{s['id']} D: Spielkamera nah 35° 15 m [{a.label}]", fill=(150, 0, 0), font=font)
            D.save(out / f"{s['id']}_nah.jpg", quality=72, optimize=True)
        s['bild'] = f"{out.name}/{s['id']}.jpg"
        kom.save(out / f"{s['id']}.jpg", quality=72, optimize=True)
    meta = dict(label=a.label, relief3d=str(r3d), daten=str(daten), treffer_datei=str(tf), gesamt=zahl, je_kachel=zahl_k, n=a.n, abstand_m=a.abstand,
                kameras=dict(A='Sueden, 35 Grad, 35 m, Textur', B='Sueden, 60 Grad, 16 m, Textur', C='wie B, Clay'), stichproben=st)
    (out / 'stichprobe.json').write_text(json.dumps(meta, indent=1, ensure_ascii=False))
    zeilen = ['| Treffer | Kachel | x | z | Wert | sichtbar ja/nein | Bild | Begründung |', '|---|---|---|---|---|---|---|---|']
    zeilen += [f"| {s['id']} ({s['regel']}) | {s['kachel']} | {s['x']} | {s['z']} | {s['wert']} |  | [{s['id']}]({s['bild']}) |  |" for s in st]
    (out / 'TABELLE_ROH.md').write_text('\n'.join(zeilen) + '\n')
    shutil.rmtree(tmp, ignore_errors=True)
    print(json.dumps(dict(stichproben=len(st), gesamt=zahl, je_kachel=zahl_k, out=str(out))))


if __name__ == '__main__':
    main()
