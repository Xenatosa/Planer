# P2b – Rampen-/Wegböschungen D1/E1/G6, Brücke E2, Farbe rampe_5 (Basis art/dorfmap-fertig @d5b17e2, L3b enthalten)

Branch `wege/dorfmap-p2b-v2` (neu auf d5b17e2, kein Force-Push; der alte lokale Stand auf 8cd6d37 wurde nicht gepusht). Nicht gemergt – erst nach dem Aufseher-JA.

## Ablauf (reproduzierbar, in relief3d/)
1. `python3 relief_p2b.py` (Konfiguration `pruefung/p2_analyse/p2b/p2b_stellen.json`, prüft GB-Basis-SHA und D2-Hash, Rücknahme-Daten `p2b_rueck.npz`, Bericht `p2b_bericht.json`)
2. `python3 pruefung/p2_analyse/p2b/p2b_bruecken.py` (Brücke E2)
3. `python3 gen_textur.py vc`, danach `python3 pruefung/p2_analyse/p2b/p2b_vc_lokal.py <vorher relief_daten> <vorher relief_neu>` (siehe Risiken)
4. `python3 pruefung/p2_analyse/p2b/p2b_r5_textur.py` (Farbe rampe_5)
5. `html_payload_p3.py`, `p10c/waende_einsetzen.py`, Gate, `RELIEF_GELAENDE_VAR=0 sh pruefung/alle_kacheln/alles.sh`

Der P2b-Schritt läuft nach relief_l3 und ist **noch nicht in `bau_endstand.sh`** eingetragen.

## Verfahren
- **Rampenböschung** (`rampe_boeschung`): Kern der Rampe (≤ 1,0 Zellen) bleibt bytegleich; 1,0–2,0 Zellen = Kernprofil (Wegoberfläche verlängert, R3 misst bei ±1,5); danach Böschung Kernprofil → harmonische Füllung (Laplace, ohne innere Extrema → keine Dellen), Smoothstep über 4 Zellen, weicher Auslauf an Stationsenden bzw. Ellipse. Feste Maske: Wasser, WEGA/wege, Brücken, andere Rampenkerne ±2,0, vektor-Wege und Kreuzungen (m→Zellen umgerechnet), D2 + 3 Zellen Fade.
- **Feinband**: `FW.h` wird im selben Gewicht auf die neue Böschung gezogen (Maske/vid eingefroren); ohne das zeigt das Feinband weiter die alte Form.
- **Befund L3 [S]**: `relief_l3.schutz()` nimmt `vektor.json` `mittellinie_m`/`polygon_m` (Meter) als Zellen. Der L3-Schutz „G017“ lag deshalb bei 272|230 (G6) statt 227|192 (F5) – Schein-Schutz. Betrifft vermutlich weitere L3/L3b-Schutzflächen.

## Stellen
| Stelle | Verfahren | Ergebnis | Nahbild |
|---|---|---|---|
| 23 G6 Rippen | Böschung rampe_4 (H6→F6) neu, Ellipse 282\|228 | **Rippen weg**, glatte Böschung; feiner Randsaum an der Kante bleibt (leicht) | [23](nahbilder/23_G6_rippen_paar.jpg) |
| 03 D1 Zickzack | Böschung rampe_2 + rampe_8 (X084) neu, Kreuzung rampe_2/rampe_8: Ausreißer im Kern rampe_8 aufs Kernprofil (03c) | Hang nördlich/östlich glatter, Kernspitzen an der Kreuzung weg. **Zickzack-Wand bleibt sichtbar.** Ursache [S]: rampe_2 (~6,5 m) und rampe_8 (~3–4 m) kreuzen sich mit 2,5–3,5 m Höhenunterschied; die Wand ist die Rasterkante zwischen beiden Kernen. Getestet: Kern rampe_2 an der Kreuzung freigeben → Wand weg, aber rampe_2-Oberfläche sinkt bis 0,84 m (R3_laengs_m +4 auf rampe_2) → verworfen (Wegoberfläche höhengleich). Braucht Entscheidung: welche Rampe oben liegt (oder Brücke/Absenkung einer Rampe). | [03](nahbilder/03_D1_zickzack_paar.jpg) |
| T17/T37 (zu 03) | – | T17 (G6 157,4\|24,2) entfällt im Gate; T37 (G7b 147\|21) bleibt, Bild unverändert | [T17](nahbilder/T17_G6_D1_paar.jpg), [T37](nahbilder/T37_G7b_D1_paar.jpg) |
| 14 E1 Finne | Öffnen 1,5 m + σ 0,5 m, Ellipse 181\|27 (1,5×2,5, Fade 1,5) | Spitze im Höhenfeld weg (max 1,78 m), im Nahbild nur leicht ruhiger. Größerer Bereich (2,5×3,5) → neuer Treffer R1_wand am Ende von rampe_2 → verworfen | [14](nahbilder/14_E1_finne_paar.jpg) |
| 20 E2 Westufer | – | **nicht angefasst.** Stufen = Rasterkante der Wasserfläche (Ufer −1,38 m, Wasser −1,32…−1,39 m, Wasserzellen fest). Ohne Wasser-Darstellung (L3c) nicht lösbar | [20](nahbilder/20_E2_ufer_paar.jpg) |
| W2 Brücke E2 | 18 Brückenzellen x 187–195, z 74–75, Deck y 0,3 wie G014; vektor.json sieht keine Furt vor | **Brücke durchgehend**, R2_getrennt −1 | [W2](nahbilder/W2_E2_bruecke_paar.jpg) |
| Stummel E1 (W10) | – | nicht angefasst: Wegende G012 am Klippenfuß, kein Bach (vektor `wegenden` ziel gelaende) | – |
| rampe_5 milchig | nur Farbe: im fleckenlosen VC-Bereich (Fleck-Energie 0,14 statt ~4) Fleckmuster aus 22 Zellen westlich aufgesetzt (1447 VC-Punkte, 5716 FW.c) | Band in Farbe schwächer, **nicht ganz weg** (große Olivflecken fehlen weiter). Gate R1_blind rampe_5 bleibt (Anschluss, nicht Farbe) | [N04](nahbilder/N04_D4_rampe5_paar.jpg), [N05](nahbilder/N05_D5_rampe5_paar.jpg) |

## Gate (vorher = d5b17e2 neu gesichert: 374/33/325, W1 0/0)
Gesamt: regeln **374 → 373**, r8 **33 → 33**, r9 **325 → 325**, W1 index.html 0 → 0, W1 alle 56 0 → 0, Lochscan index.html offen_innen 0, Lochscan 56 Kacheln 0, Hash D1/G1/D2 index.html = alle_kacheln: alle identisch.
Nur geänderte Regeln (alle übrigen gleich, volle Liste `P2B_gate_vorher_nachher.json`):

| Prüfer | Regel | vorher (d5b17e2) | nachher | Δ |
|---|---|---|---|---|
| regeln | `G6_facette` | 213 | 214 | +1 |
| regeln | `R2_getrennt` | 9 | 8 | -1 |
| regeln | `R3_quer_pct` | 11 | 10 | -1 |

D2 bitgleich: GB 749d3c4b…, VC 8d7a7b82…, WV 4b33ed17…, WEGA e6cf61d2… (vorher = nachher).
Trefferkarte: `trefferkarte/vergleich.html`.

## Neue Treffer (Ausnahmen)
| Regel | Feld | x\|z | Wert | Urteil | Nahbild |
|---|---|---|---|---|---|
| G6_facette | D1 | 146,1\|17,5 | 6 | unsichtbar (ersetzt 145,6\|19,2 Wert 20) | [Bild](nahbilder/NEU_G6_D1_146_17_paar.jpg) |
| G6_facette | D1 | 145,2\|20,0 | 12 | unsichtbar | [Bild](nahbilder/NEU_G6_D1_145_20_paar.jpg) |
| G6_facette | D1 | 159,0\|22,9 | 6 | weiche Mulde an der rampe_8-Böschung sichtbar, keine Kante – Grenzfall | [Bild](nahbilder/NEU_G6_D1_159_23_paar.jpg) |
| G6_facette | E1 | 184,2\|27,8 | 9 | unsichtbar | [Bild](nahbilder/NEU_G6_E1_184_28_paar.jpg) |
| G6_facette | G6 | 283,6\|222,3 | 10 | unsichtbar (ersetzt 283,8\|222,3) | [Bild](nahbilder/NEU_G6_G6_283_222_paar.jpg) |

Entfallen: G6 145,6\|19,2, 157,4\|24,2 (T17), 185,2\|23,8, 287,2\|221,2, 283,8\|222,3; R3_quer rampe_8 155,6\|22,6; R2_getrennt G2.

## Risiken
- 03 bleibt sichtbar (Höhenkonflikt der Kreuzung rampe_2/rampe_8, Entscheidung nötig).
- `gen_textur.py vc` ist auf diesem Stand nicht idempotent (ändert jedes Mal ~106–250 VC-Punkte in E4, weit weg). `p2b_vc_lokal.py` setzt VC/FW.c außerhalb 8 Zellen um die P2b-Höhenänderung auf den Vorher-Stand zurück; dadurch kein neuer T1 in E4.
- L3-Einheitenfehler (vektor-Meter als Zellen) in `relief_l3.schutz()`.
- P2b noch nicht in `bau_endstand.sh`.
- Kachelbilder vorher/nachher: `kacheln/` (D1, E1, E2, G6, D4, D5).

**Aufwand (Auflage Aufseher):** Kosten 0 €, Codex nein (lokal im Executor, ohne Codex/agy), Laufzeit ca. 1,1 h (16.11.2026 11:25–12:29 Europe/Berlin, inkl. Neuaufsatz auf d5b17e2).
