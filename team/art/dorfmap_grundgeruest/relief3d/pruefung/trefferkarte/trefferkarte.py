#!/usr/bin/env python3
"""P6 Trefferkarte: 8x7-Raster (A-H x 1-7) aus den Gate-JSONs.

Aufruf (aus relief3d/):  python3 pruefung/trefferkarte/trefferkarte.py
Vergleich:               ... --vorher ALTER_ORDNER   (enthaelt die drei JSONs)
Exit 1, wenn eine Summe nicht exakt mit dem JSON uebereinstimmt.
Liest nur; aendert keine Relief- oder Prueferdateien.
"""
import argparse, datetime, html, json, os, subprocess, sys

HIER = os.path.dirname(os.path.abspath(__file__))
PRUEF = os.path.dirname(HIER)
SPALTEN = "ABCDEFGH"
ZEILEN = range(1, 8)
FELDER = [f"{s}{z}" for z in ZEILEN for s in SPALTEN]
FAMILIEN = ["Hoehen", "Wege", "Texturen", "R8", "R9", "Sonstige"]
KURZ = {"Hoehen": "H", "Wege": "W", "Texturen": "T", "R8": "R8", "R9": "R9", "Sonstige": "S"}
QUELLEN = [("regeln", "regeln_letzter_lauf.json"), ("r8", "r8_letzter_lauf.json"), ("r9", "r9_letzter_lauf.json")]


def familie(quelle, regel):
    if quelle == "r8":
        return "R8"
    if quelle == "r9":
        return "R9"
    if regel.startswith(("G", "R3_", "R5_")):
        return "Hoehen"
    if regel.startswith(("R1_", "R2_", "R6_")):
        return "Wege"
    if regel.startswith("T"):
        return "Texturen"
    return "Sonstige"


def lade(ordner, pfade=None):
    """Liest die drei JSONs, zaehlt je Feld x Familie x Regel und prueft die Summen."""
    pfade = pfade or {q: os.path.join(ordner, n) for q, n in QUELLEN}
    feld = {f: {fa: 0 for fa in FAMILIEN} for f in FELDER}
    regeln_je_feld = {f: {} for f in FELDER}
    kartenweit = []
    dateien, fehler = {}, []
    for q, _ in QUELLEN:
        d = json.load(open(pfade[q], encoding="utf-8"))
        tr = d.get("treffer", [])
        summe = d.get("summe")
        je_regel = sum(d.get("je_regel", {}).values())
        gezaehlt_raster = gezaehlt_kw = 0
        fam_summe = {fa: 0 for fa in FAMILIEN}
        for t in tr:
            r = str(t.get("regel", "?"))
            fa = familie(q, r)
            fam_summe[fa] += 1
            f = str(t.get("feld", ""))
            if f in feld:
                feld[f][fa] += 1
                regeln_je_feld[f][r] = regeln_je_feld[f].get(r, 0) + 1
                gezaehlt_raster += 1
            else:
                kartenweit.append({"quelle": q, "regel": r, "feld": f, "familie": fa})
                gezaehlt_kw += 1
        ok = summe == len(tr) == je_regel == gezaehlt_raster + gezaehlt_kw
        if not ok:
            fehler.append(f"{q}: summe={summe} len(treffer)={len(tr)} je_regel={je_regel} "
                          f"raster+kartenweit={gezaehlt_raster}+{gezaehlt_kw}")
        dateien[q] = {"pfad": os.path.relpath(pfade[q], PRUEF), "summe": summe, "len_treffer": len(tr),
                      "summe_je_regel": je_regel, "im_raster": gezaehlt_raster, "kartenweit": gezaehlt_kw,
                      "je_familie": {k: v for k, v in fam_summe.items() if v}, "ok": ok}
    return {"felder": feld, "regeln_je_feld": regeln_je_feld, "kartenweit": kartenweit,
            "dateien": dateien, "fehler": fehler,
            "gesamt": sum(v["summe"] or 0 for v in dateien.values())}


def total(stand, f, fam=None):
    z = stand["felder"][f]
    return z[fam] if fam else sum(z.values())


def farbe(n, maxn):
    if n == 0:
        return (46, 125, 50)
    t = min(1.0, n / max(1, maxn))
    if t < 0.5:  # gelb -> orange
        u = t / 0.5
        return (int(253 - 8 * u), int(216 - 100 * u), int(53 - 30 * u))
    u = (t - 0.5) / 0.5  # orange -> rot
    return (int(245 - 47 * u), int(116 - 76 * u), int(23 + 10 * u))


def diff_farbe(d, maxd):
    if d == 0:
        return (120, 120, 120)
    t = min(1.0, abs(d) / max(1, maxd))
    return (int(46 + 40 * (1 - t)), int(160 - 40 * t), int(60)) if d < 0 else (int(200 + 40 * t), int(120 - 80 * t), 40)


def commit():
    try:
        return subprocess.run(["git", "-C", PRUEF, "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True, timeout=3).stdout.strip() or "?"
    except Exception:
        return "?"


def rgb(c):
    return "#%02x%02x%02x" % c


def schreibe_html(stand, pfad, titel, kopf, vorher=None):
    maxn = max(total(stand, f) for f in FELDER)
    daten = {"felder": stand["felder"], "regeln": stand["regeln_je_feld"]}
    if vorher:
        daten["vorher"] = vorher["felder"]
    zellen = []
    for z in ZEILEN:
        zellen.append(f"<tr><th>{z}</th>")
        for s in SPALTEN:
            f = f"{s}{z}"
            zellen.append(f'<td id="z_{f}" data-f="{f}"></td>')
        zellen.append("</tr>")
    kw = "".join(f"<li>{html.escape(k['quelle'])}: {html.escape(k['regel'])} (feld '{html.escape(k['feld'])}', "
                 f"{k['familie']})</li>" for k in stand["kartenweit"]) or "<li>keine</li>"
    zeilen_dat = "".join(
        f"<tr><td>{q}</td><td>{v['pfad']}</td><td>{v['summe']}</td><td>{v['im_raster']}</td><td>{v['kartenweit']}</td>"
        f"<td>{', '.join(f'{k} {n}' for k, n in v['je_familie'].items())}</td><td>{'OK' if v['ok'] else 'FEHLER'}</td></tr>"
        for q, v in stand["dateien"].items())
    knoepfe = "".join(f'<button data-fam="{fa}">{fa}</button>' for fa in [""] + FAMILIEN).replace(
        'data-fam="">', 'data-fam="" class="an">Gesamt')
    js = """
const D=%s, FAM=%s, KURZ=%s, MAX=%d, VERGL=%s;
function col(n,m){if(n==0)return'rgb(46,125,50)';let t=Math.min(1,n/Math.max(1,m));
 if(t<.5){let u=t/.5;return`rgb(${253-8*u|0},${216-100*u|0},${53-30*u|0})`}
 let u=(t-.5)/.5;return`rgb(${245-47*u|0},${116-76*u|0},${23+10*u|0})`}
function dcol(d,m){if(d==0)return'rgb(120,120,120)';let t=Math.min(1,Math.abs(d)/Math.max(1,m));
 return d<0?`rgb(${46+40*(1-t)|0},${160-40*t|0},60)`:`rgb(${200+40*t|0},${120-80*t|0},40)`}
function wert(src,f,fam){let z=src[f];return fam?z[fam]:FAM.reduce((a,k)=>a+z[k],0)}
function male(fam){let m=0;for(const f in D.felder){let v=VERGL?Math.abs(wert(D.felder,f,fam)-wert(D.vorher,f,fam)):wert(D.felder,f,fam);m=Math.max(m,v)}
 for(const td of document.querySelectorAll('td[data-f]')){const f=td.dataset.f,n=wert(D.felder,f,fam);
  let fams=FAM.filter(k=>D.felder[f][k]).map(k=>KURZ[k]+' '+D.felder[f][k]).join(' · ');
  if(VERGL){const v=wert(D.vorher,f,fam),d=n-v;td.style.background=dcol(d,m);
   td.innerHTML=`<b>${d>0?'+':''}${d}</b><small>${v} → ${n}</small>`}
  else{td.style.background=col(n,m);td.innerHTML=`<b>${n}</b><small>${fams||'–'}</small>`}
  const r=D.regeln[f];td.title=f+'\\n'+(Object.keys(r).sort().map(k=>k+': '+r[k]).join('\\n')||'keine Treffer')}}
document.querySelectorAll('button').forEach(b=>b.onclick=()=>{document.querySelectorAll('button').forEach(x=>x.classList.remove('an'));b.classList.add('an');male(b.dataset.fam)});
male('');
""" % (json.dumps(daten), json.dumps(FAMILIEN), json.dumps(KURZ), maxn, "true" if vorher else "false")
    doc = f"""<!doctype html><html lang="de"><meta charset="utf-8"><title>{html.escape(titel)}</title>
<style>body{{font-family:system-ui,sans-serif;background:#1b1b1b;color:#eee;margin:20px}}
table.k{{border-collapse:collapse}}table.k td{{width:110px;height:78px;text-align:center;border:2px solid #111;color:#111;vertical-align:middle}}
table.k td b{{display:block;font-size:26px}}table.k td small{{font-size:11px}}table.k th{{padding:4px 8px}}
button{{margin:2px;padding:6px 10px;background:#333;color:#eee;border:1px solid #666;cursor:pointer}}button.an{{background:#c0662a}}
table.d{{border-collapse:collapse;margin-top:14px}}table.d td,table.d th{{border:1px solid #555;padding:3px 8px;font-size:13px}}</style>
<h1>{html.escape(titel)}</h1><p>{html.escape(kopf)}</p><div>{knoepfe}</div>
<table class="k"><tr><th></th>{''.join(f'<th>{s}</th>' for s in SPALTEN)}</tr>{''.join(zellen)}</table>
<p>Legende: grün = 0, gelb → rot = steigende Trefferzahl (Skala bis Maximum der Auswahl){' · Vergleich: grün = weniger, rot = mehr' if vorher else ''}.
Kürzel: H Höhen (G*, R3, R5) · W Wege (R1, R2, R6) · T Texturen (T*) · R8 (r8-Datei) · R9 (r9-Datei inkl. R8b) · S Sonstige. Tooltip je Kachel zeigt die Einzelregeln.</p>
<h3>Kartenweit (ohne Kachel)</h3><ul>{kw}</ul>
<table class="d"><tr><th>Quelle</th><th>Datei</th><th>summe</th><th>im Raster</th><th>kartenweit</th><th>je Familie</th><th>Prüfung</th></tr>{zeilen_dat}</table>
<script>{js}</script></html>"""
    open(pfad, "w", encoding="utf-8").write(doc)


def schreibe_png(stand, pfad, titel, kopf, vorher=None):
    from PIL import Image, ImageDraw, ImageFont
    def font(g, fett=False):
        for n in (["DejaVuSans-Bold.ttf"] if fett else []) + ["DejaVuSans.ttf"]:
            try:
                return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/" + n, g)
            except OSError:
                pass
        return ImageFont.load_default()
    zw, zh, li, ob = 150, 104, 50, 120
    kw_zeilen = len(stand["kartenweit"])
    breite, hoehe = li + 8 * zw + 30, ob + 7 * zh + 150 + 22 * kw_zeilen
    im = Image.new("RGB", (breite, hoehe), (27, 27, 27))
    d = ImageDraw.Draw(im)
    d.text((li, 18), titel, font=font(28, True), fill=(240, 240, 240))
    d.text((li, 58), kopf, font=font(15), fill=(200, 200, 200))
    werte = {f: total(stand, f) for f in FELDER}
    if vorher:
        diffs = {f: werte[f] - total(vorher, f) for f in FELDER}
        maxd = max(abs(v) for v in diffs.values())
    maxn = max(werte.values())
    for i, s in enumerate(SPALTEN):
        d.text((li + i * zw + zw // 2 - 6, ob - 26), s, font=font(18, True), fill=(220, 220, 220))
    for j, z in enumerate(ZEILEN):
        d.text((16, ob + j * zh + zh // 2 - 10), str(z), font=font(18, True), fill=(220, 220, 220))
        for i, s in enumerate(SPALTEN):
            f = f"{s}{z}"
            x, y = li + i * zw, ob + j * zh
            c = diff_farbe(diffs[f], maxd) if vorher else farbe(werte[f], maxn)
            d.rectangle([x, y, x + zw - 3, y + zh - 3], fill=c)
            gross = (("+" if diffs[f] > 0 else "") + str(diffs[f])) if vorher else str(werte[f])
            d.text((x + 8, y + 6), f, font=font(12), fill=(20, 20, 20))
            d.text((x + zw // 2, y + 36), gross, font=font(30, True), fill=(15, 15, 15), anchor="mm")
            if vorher:
                klein = f"{total(vorher, f)} → {werte[f]}"
                d.text((x + zw // 2, y + 76), klein, font=font(13), fill=(15, 15, 15), anchor="mm")
            else:
                teile = [f"{KURZ[k]} {stand['felder'][f][k]}" for k in FAMILIEN if stand["felder"][f][k]]
                for k, zeile in enumerate([" · ".join(teile[:3]), " · ".join(teile[3:])]):
                    d.text((x + zw // 2, y + 70 + 16 * k), zeile, font=font(12), fill=(15, 15, 15), anchor="mm")
    y = ob + 7 * zh + 14
    leg = ("Vergleich: grün = weniger Treffer, rot = mehr" if vorher else
           "Farbe: grün = 0, gelb → rot = mehr Treffer (max %d)" % maxn)
    d.text((li, y), leg + ". H Höhen (G*, R3, R5) · W Wege (R1, R2, R6) · T Texturen · R8 · R9 (inkl. R8b) · S Sonstige",
           font=font(13), fill=(210, 210, 210))
    sumz = "  |  ".join(f"{q}: {v['summe']} ({v['im_raster']} Raster + {v['kartenweit']} kartenweit) {'OK' if v['ok'] else 'FEHLER'}"
                        for q, v in stand["dateien"].items())
    d.text((li, y + 26), "Summen: " + sumz, font=font(13, True), fill=(235, 235, 235))
    d.text((li, y + 54), f"Kartenweit (ohne Kachel): {kw_zeilen}", font=font(13, True), fill=(235, 235, 235))
    for k, t in enumerate(stand["kartenweit"]):
        d.text((li + 12, y + 78 + 22 * k), f"{t['quelle']}: {t['regel']} (feld '{t['feld']}', {t['familie']})",
               font=font(12), fill=(210, 210, 210))
    im.save(pfad)


def json_aus(stand):
    return {"felder": {f: dict(v, gesamt=sum(v.values())) for f, v in stand["felder"].items()},
            "regeln_je_feld": stand["regeln_je_feld"], "kartenweit": stand["kartenweit"],
            "dateien": stand["dateien"], "gesamt": stand["gesamt"],
            "je_familie": {fa: sum(stand["felder"][f][fa] for f in FELDER) +
                           sum(1 for k in stand["kartenweit"] if k["familie"] == fa) for fa in FAMILIEN}}


def main():
    ap = argparse.ArgumentParser(description="Trefferkarte 8x7 aus den Gate-JSONs")
    ap.add_argument("--regeln", default=os.path.join(PRUEF, "regeln_letzter_lauf.json"))
    ap.add_argument("--r8", default=os.path.join(PRUEF, "r8_letzter_lauf.json"))
    ap.add_argument("--r9", default=os.path.join(PRUEF, "r9_letzter_lauf.json"))
    ap.add_argument("--aus", default=HIER, help="Ausgabeordner")
    ap.add_argument("--vorher", help="Ordner mit den drei JSONs des Vorher-Stands (Vergleich)")
    a = ap.parse_args()
    os.makedirs(a.aus, exist_ok=True)
    stand = lade(None, {"regeln": a.regeln, "r8": a.r8, "r9": a.r9})
    zeit = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    kopf = (f"Commit {commit()} · erzeugt {zeit} · regeln {stand['dateien']['regeln']['summe']} · "
            f"r8 {stand['dateien']['r8']['summe']} · r9 {stand['dateien']['r9']['summe']} · gesamt {stand['gesamt']}")
    schreibe_html(stand, os.path.join(a.aus, "trefferkarte.html"), "Trefferkarte Dorfmap", kopf)
    json.dump(json_aus(stand), open(os.path.join(a.aus, "trefferkarte.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    try:
        schreibe_png(stand, os.path.join(a.aus, "trefferkarte.png"), "Trefferkarte Dorfmap", kopf)
    except ImportError:
        print("WARNUNG: Pillow fehlt (pip install pillow); PNG nicht erzeugt, HTML/JSON schon.", file=sys.stderr)
    fehler = list(stand["fehler"])
    if a.vorher:
        alt = lade(a.vorher)
        fehler += ["vorher " + f for f in alt["fehler"]]
        vk = f"vorher {alt['gesamt']} → jetzt {stand['gesamt']} ({stand['gesamt'] - alt['gesamt']:+d}) · {kopf}"
        schreibe_html(stand, os.path.join(a.aus, "vergleich.html"), "Trefferkarte Vergleich", vk, alt)
        try:
            schreibe_png(stand, os.path.join(a.aus, "vergleich.png"), "Trefferkarte Vergleich", vk, alt)
        except ImportError:
            pass
    for q, v in stand["dateien"].items():
        print(f"{q}: summe {v['summe']} = {v['im_raster']} Raster + {v['kartenweit']} kartenweit -> {'OK' if v['ok'] else 'FEHLER'}")
    if fehler:
        print("SUMMEN FALSCH:\n  " + "\n  ".join(fehler), file=sys.stderr)
        sys.exit(1)
    print(f"OK, Ausgabe in {os.path.relpath(a.aus)}")


if __name__ == "__main__":
    main()
