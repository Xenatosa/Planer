# P2 Wegnetz – Analyse vor Änderung (16.11.2026, Wege & Deko)

Basis `art/dorfmap-fertig` 8e374b0, Branch `wege/dorfmap-p2`. Marker: [S] gemessen, [A] Annahme, [R] gerechnet.
**Keine Datei der Karte geändert.** vektor.json aac6afff…, neu/zellen_relief.csv 99d30e55…, relief_daten.json.gz 5e8fdb51…, index.html 1eb5d246… unverändert [S].

## Gate vorher [S]
Eigener Lochscan `/tmp/p2_gate_loch.json` statt `/tmp/gate_loch.json` (sonst gleiche Befehle wie export_gate.sh), 13,4 s.
pruefe_regeln 570 (R1_blind 24, R2_getrennt 15, R6_wasser_schnee 4, R3 35/23/22, R5_loch 17, G6 220, G5 68, T1 94 …), r8 48 (R8_stufe 9, R8_gitter 10, R8_quer 5, R8a_wegende 24), r9 334 (R8b 25, R9 34, R9w 275). Identisch zum FERTIGPLAN.

## Befund: Das Gate liest vektor.json nicht [S]
- `pruefe_regeln.py`, `r8_kreuzung.py`, `r9_form.py`, `loch_o18g.js`, `export_gate.sh` enthalten keinen Bezug auf `vektor.json` oder `neu/` (rg).
- R1/R2 werden aus `relief_daten.json.gz` gemessen: `D['wege']` (2839 Zellen), `WEGA`, `bruecken` (20), `rampenwege` (13).
- `relief_daten.json.gz` erzeugt das Legacy-`gen_relief.py` aus `../_alt/modell3d_t36u/zellen_eigenschaften.csv`. `vektor.json` ist dagegen eine **Ausgabe** von `neu/vektor.py` (aus den Zellen) und Eingabe nur für den Opt-in-Pfad `RELIEF_NEU=1` → `neu/relief_neu.json.gz`.
- `vektor.json` enthält nur GASSE 42 / ANBINDUNG 11 / HAUSWEG 9 und 88 Kreuzungen, **keine der 13 Rampen**.
→ Eine Änderung an vektor.json ändert keine Gate-Zahl [R aus Datenfluss].

## Was die Treffer sind [S] (Koordinaten in Zellen à 1,2 m, Daten: p2_analyse.json, Bild: uebersicht_wegmaske_treffer.png)
- **R1_blind 24 / R2 13 von 15**: die 13 `rampenwege` sind prozedurale Abstiegsrampen (`gen_relief.py` `_rampen()` rampe_0–10 an Nord/Suedgrat/Krater/Ostgrat, `_serp()` rampe_11 = X084, rampe_12 = X069). Sie liegen frei im Gelände ohne Anschluss ans Dorfwegnetz. Abstand Rampenende → nächste Netzzelle 6,4–61,1 Zellen (≈ 8–73 m); nur rampe_5-Anfang hängt an rampe_3 (0,8). Die Rampen bilden 11 eigene R2-Komponenten.
- **R2 2 weitere**: Wegkomponente G2 (1588 Zellen, Lücke 41,2 Zellen zur Hauptkomponente) und D2 (1227 Zellen, Lücke 9,0 Zellen bei 176|127), dazu kleine Wegreste E3 (38, Lücke 15,3) und F4 (94, Lücke 5,4) – das sind Dorfwege aus `D['wege']`/WEGA, nicht aus vektor.json.
- **R6_wasser_schnee 4**: kein Wegthema. Regel = Wasser (WV) auf Gelände > 10 m. F1 214|14,9 (361 Feinzellen, G 11,4–12,8 m) und drei Kleinstflächen G1 (6/7/22 Feinzellen, G 12,4–13,1 m). Lösung nur über Wasser-/Höhendaten (P1/Art Umgebung).

## Folgerung
Eine echte Korrektur bräuchte neue Wegstücke von 8–73 m durch das Gelände (in `gen_relief.py` eingeschnitten) bzw. Wasser/Höhen-Änderung und ein neu erzeugtes `relief_daten.json.gz` – das ändert Höhen (GB) und kollidiert mit P1/L1 (Codex, gleiche Binärdatei). Nur die Listen in relief_daten.json.gz zu patchen würde die Zahl ohne sichtbare Änderung senken (Prüfer-Umgehung, gegen Lieferregel 5). Deshalb hier gestoppt; Entscheidung beim Dorfmap-Grundgerüst.
