#!/usr/bin/env python3
"""P6-Runner: alle Regeln Q1-Q14 gegen einen detail_v2-Datensatz.
Aufruf: python3 pruefe_alle.py --wurzel <detail_v2> [--referenz qa/referenz] [--abnahme <ordner>] [--nur Q1,Q7] [--out bericht.json]
Exit: 0 = alle ok, 1 = mindestens ein Fehler, 2 = kein Fehler, aber Eingaben fehlen (Regel 'offen')."""
import argparse, json, sys, time, traceback
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from dv2qa.welt import Kontext, Fehlt
from dv2qa import regeln_a as A, regeln_b as B, regeln_c as C

REGELN = {'Q1': A.q1, 'Q2': A.q2, 'Q3': A.q3, 'Q4': A.q4, 'Q5': A.q5, 'Q6': B.q6, 'Q7': B.q7, 'Q8': B.q8, 'Q9': B.q9,
          'Q10': B.q10, 'Q11': C.q11, 'Q12': C.q12, 'Q13': C.q13, 'Q14': C.q14}


def laufe(wurzel, referenz=None, abnahme=None, nur=None, konfig=None, still=False):
    ctx = Kontext(wurzel, referenz or Path(__file__).resolve().parent / 'referenz', abnahme, konfig)
    out = {'format': 'dv2-qa-1', 'wurzel': str(wurzel), 'zeit': time.strftime('%Y-%m-%d %H:%M:%S %Z'), 'regeln': {}}
    t00 = time.time()
    for name, f in REGELN.items():
        if nur and name not in nur: continue
        t0 = time.time()
        try:
            r = f(ctx)
        except Fehlt as e:
            r = {'regel': name, 'status': 'offen', 'werte': {}, 'befunde': [], 'notiz': f'Eingabe fehlt: {e}'}
        except Exception as e:
            r = {'regel': name, 'status': 'fehler', 'werte': {}, 'befunde': [{'ausnahme': repr(e)[:300], 'trace': traceback.format_exc()[-600:]}], 'notiz': 'Pruefer-Ausnahme'}
        r['dauer_s'] = round(time.time() - t0, 2)
        out['regeln'][name] = r
        if not still: print(f"{name:4s} {r['status']:7s} {r['dauer_s']:7.1f}s  {json.dumps(r['werte'], ensure_ascii=False)[:220]}", flush=True)
    st = [r['status'] for r in out['regeln'].values()]
    out['gesamt'] = 'fehler' if 'fehler' in st else 'offen' if 'offen' in st else 'ok'
    out['zaehlung'] = {s: st.count(s) for s in ('ok', 'fehler', 'offen')}
    out['dauer_s'] = round(time.time() - t00, 1)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--wurzel', required=True); ap.add_argument('--referenz'); ap.add_argument('--abnahme')
    ap.add_argument('--nur'); ap.add_argument('--konfig'); ap.add_argument('--out')
    a = ap.parse_args()
    nur = set(a.nur.upper().split(',')) if a.nur else None
    out = laufe(Path(a.wurzel), Path(a.referenz) if a.referenz else None, Path(a.abnahme) if a.abnahme else None, nur, a.konfig)
    js = json.dumps(out, ensure_ascii=False, indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
    if a.out: Path(a.out).write_text(js)
    print(f"GESAMT {out['gesamt'].upper()} {out['zaehlung']} ({out['dauer_s']} s)")
    sys.exit({'ok': 0, 'fehler': 1, 'offen': 2}[out['gesamt']])


if __name__ == '__main__':
    main()
