# welt3d – Prototyp-Welt im Browser (t39u)

`index.html` öffnen (Doppelklick, offline, 4,4 MB). Alles eingebettet: three.js 0.170, Daten, Textur.
**Alle Objekte sind PLATZHALTER** (low-poly, prozedural). 1 Einheit = 1 m. Rote Figur = Mensch 1,8 m.

## Woher kommt was
| Objekt | Quelle | Regel | Anzahl [R] |
|---|---|---|---|
| Gelände, Wasser, Sockel | modell3d (gen_modell3d.py) | Höhen [A], siehe ../ABWEICHUNGEN_C20.md | 336×303 Zellen |
| Gebäude | E40-Plätze `../../pruefung/quelle_plaetze_wachstum_ausbau_planm.json` (v8-Plan, 233) | Grundriss = Platz-Rechteck ×0,9; Höhe je Typ [A] (Hütte 3, Standard 5, Turmhaus 9, Funktion 7 m) | 233 |
| Bäume | untergrund = WALD | 1 Baum je 3×3 m [A], Höhe 6–10 m [A] | 1 206 |
| Felsen | untergrund = FELS | 1 je 3×3 m [A], 0,8–2,2 m [A] | 244 |
| Findlinge | hindernis_art = MASKE, je zusammenhängende Fläche | Größe 0,6·√Fläche [A] | 40 |
| Deko-Steine | dekoplaetze_netz = 1 | 0,6 m [A] | 336 |
| Wege, Brücken | overlay_plaetze_wege (weg_id, bruecke) | flach 6 cm über Boden | 2 839 / 20 Zellen |

Achtung: Der E40-Plan (v8) ist laut BAUPLAN_E100.md überholt; 112 der 233 Plätze liegen außerhalb der Senke [S, t16u]. Gültig wäre v4b (E40 = 203) – dafür fehlen hier die Polygone.

## Neu bauen
`python3 ../gen_modell3d.py` (schreibt /tmp/m3_*.npy) → `python3 gen_welt3d.py` → `python3 baue_html.py` (braucht /tmp/w3: `npm i three@0.170 esbuild playwright`).
Test: `NODE_PATH=/tmp/w3/node_modules node test_welt3d.js` → `test/*.png`, `test/test_ergebnis.json`.
