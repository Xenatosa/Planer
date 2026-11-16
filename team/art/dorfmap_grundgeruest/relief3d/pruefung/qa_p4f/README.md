# QA P4f – finale Sichtprüfung Dorfmap (art/dorfmap-fertig @ a6b00ba)

Endabnahme nach P2e (#37, rampe_5 D4/D5 Farbangleich) und L3h (#38, E3-Bach, E4-Bachrand, Talhang E3).

## Gate (Prüfer/Schwellen unverändert)
```
cd team/art/dorfmap_grundgeruest/relief3d
export NODE_PATH=/tmp/w3/node_modules
HTML=index.html OUT=/tmp/gate_loch.json RAND=0.6 node pruefung/loch_o18g.js
GATE_LOCH_JSON=/tmp/gate_loch.json sh pruefung/export_gate.sh   # „GATE ROT“, Exit 1 = erwartete Exportsperre
git checkout pruefung/w1_alle56_letzter_lauf.json                # vom Gate geändert, zurückgesetzt
```
| Größe | Ist a6b00ba | Soll laut #38 |
|---|---|---|
| regeln | 363 (G6 209, G5 34, G7b_feld 29, R3_laengs 21, R1 17, …), Ausnahmen 0 | 363 (Basis 367) |
| R8 | 31 (21 Kreuzungen) | 31 |
| R9 | 321 (R8b 18, R9 34, R9w 269) | 321 |
| W1 / W1 alle 56 | 0 / 0 | 0 / 0 |
| Lochscan offen_innen | 0 | 0 |

Ist = Soll.

## Methode
1. Vollansicht aller 56 Kacheln: `python3 pruefung/alle_kacheln/baue_alle_kacheln.py --out /tmp/p4f` (Naht max 0, wand_dreiecke 0).
2. Jede Kachel einzeln: Übersicht + 4 Quadranten (30 m), Farbe und Ton → `bilder_a6b00ba/kacheln/<K>.jpg` (links Farbe, rechts Ton).
3. 85 Nahbilder vorher (bfe8dce) / jetzt (a6b00ba): `punkte_p4f.json` (78) + `punkte_neu.json` (5) + `punkte_g1_krater.json` (2) → `vn/` (oben vorher, unten jetzt; je links Farbe, rechts Ton). Pixel-Diff zusätzlich: geänderte Nahbilder liegen nur im Bereich E2-Brücken (minimal), E3, E4, D4, D5 und C4|D4-Rand; alle übrigen bildgleich (mittlere Abweichung 0,00).
4. Schatten-Stichprobe an Nähten (`punkte_schatten.json`, SH=1) → `schatten/`: Schatten laufen über x=84, x=126, z=43 und B6\|C6 durch, keine Kante.
5. Messung `messung.py` → `messung_p4f.json`; Gate-Treffer je Ort aus `regeln_letzter_lauf.json`.
6. Gesamtansicht der Karte (`gesamt.js`, 2400×1500): `gesamt/gesamt_suedwest.jpg` (Schrägblick), `gesamt_sued.jpg`, `gesamt_steil.jpg`, `gesamt_sued_schatten.jpg`.

Werkzeuge: `rendere_kacheln.js`, `komposit.py`, `paar.py`, `vergleich.py`, `messung.py` (aus qa_p4e), `gesamt.js` (neu).

## Ergebnis
- **54 sauber / 2 leicht / 0 stark** → `TABELLE.md`
- sichtbar (leicht): **E3** Tümpelkette Nordufer ≈190\|103; **G1** Krater mit Wasserfleck ≈272,5\|10 (alt, schon in bfe8dce) → `LISTE_SICHTBAR.md`
- behoben gegenüber P4e: D4 (133\|155), D5 (135\|185), E4 (176\|146), Talhang E3; E3-Bach aus Distanz klar als Wasser erkennbar
- Ausnahmen: 16 (14 aus P4e weiter unsichtbar, 2 neu: A15 C2-Mulde, A16 G1-Gate-Treffer) → `LISTE_AUSNAHMEN.md`

## Kosten
0 € extern, kein Codex, nur lokale Renderläufe auf der Box (Auftrag 20:51–21:20 MEZ, ≈½ h).
