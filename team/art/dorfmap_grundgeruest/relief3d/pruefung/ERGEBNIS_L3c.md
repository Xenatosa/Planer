# ERGEBNIS L3c – Wasser-Folgebefunde aus QA P4c (G7, C7, H7, E3, E2-Westufer) + Maßstab-Fix Wegschutz

> **Ersetzt durch `ERGEBNIS_L3c2.md`** (Neuaufbau auf a6a4831 nach P2b/P2c; PR #22 wird geschlossen). Die Zahlen unten (Gate 374→377, Fix-Regionen 16/19/20/22/23) gelten nur für den alten Stand d5b17e2 und wurden in L3c2 nicht übernommen: L3/L3b bleiben dort eingefroren, nur die 7 Wegtreffer werden zurückgesetzt.

Branch `art/dorfmap-L3c`, Basis `d5b17e2` (L3b-Kopf, PR #20 – **baut auf #20 auf, erst nach #20 mergen**). Kein Codex, 0 €.
Umsetzung im schaltbaren Nachschritt `relief_l3.py` (Stellen `L3c_*` in `pruefung/l3_stellen.json`). `--aus` und erneutes Einschalten sind bytegleich.

## 1. Maßstab-Fehler in `relief_l3.schutz()` – behoben und mit Test belegt
- **Fehler:** `vektor.json` gibt Mittellinien, Breiten und Kreuzungspolygone in **Metern** an (`karte.zellweite_m = 1,2`). `schutz()` hat diese Werte als **Zellen** benutzt. Dadurch lag der Schutz um den Faktor 1,2 verschoben bzw. zu breit; echte Wegflächen weit vom Ursprung lagen teils **außerhalb** des Schutzes.
- **Fix:** Mittellinie, Halbbreite, Kreuzungspolygon und Übergang werden durch `zellweite_m` geteilt (`relief_l3.py`, `schutz()`). `rampenwege`, `wege` und `WEGA` in `relief_daten` sind schon Zellen und bleiben unverändert.
- **Test** `pruefung/test_l3_schutz.py` (neu):
  - Median-Abstand der Weg-Quellzellen (`zellen_relief`) zur Mittellinie: neu 0,0 Zellen, alt 49,53 Zellen.
  - Quellzellen von Wegen und Kreuzungen (4120) im Schutz: neu 4120 von 4120. Allein durch den vektor-Teil geschützt: neu 100 %, alt 43,6 %.
  - WEGA-Vertices im Schutz: 100 %.
  - Ergebnis: neuer Code besteht (exit 0), alter Code fällt durch (exit 1).
- **Alle L3-, L3b- und L3c-Stellen wurden mit dem korrigierten Schutz neu angewendet.** Vertices, die vorher fälschlich geändert waren, haben jetzt wieder ihren Originalwert (Ursprungsstand vor L3).

### Alte Aussage „Wege 0,0 m“ war falsch (L3 und L3b)
Die Messung damals benutzte denselben falschen Maßstab. Mit richtigem Maßstab hatte der Stand `d5b17e2` **7 geänderte Vertices auf echten vektor.json-Wegflächen**:
- Stelle 13 (G4, ≈277,5\|140,5): 5 Vertices, max 0,284 m.
- Stelle 18 (H2, ≈330\|67): 2 Vertices, 0,06 m und 0,002 m.

Kreuzungen, Rampenkerne und WEGA hatten 0 Treffer. In L3c sind alle 7 Vertices zurückgesetzt.

### Kleinster Abstand je Stelle nach dem Fix
Abstand der geänderten Vertices zu den geschützten Flächen. Einheit Zellen (1 Zelle = 1,2 m), Vertexraster 0,5. Quelle `l3c_abstaende_je_stelle.json`, Skript-Logik im Bericht; alter Stand ebenfalls dort.

| Stelle | Kachel | Vertices | max Δ m | Vektorweg | Kreuzung | Rampenkern | WEGA/wege | Wasser | auf Weg/Kreuz/Rampe | auf Wasser |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 | C3 | 2077 | 2.405 | 36.0 | 39.15 | 44.32 | 38.01 | 19.45 | 0 | 0 |
| 02 | C3 | 1215 | 1.51 | 34.79 | 33.2 | 33.35 | 33.68 | 40.07 | 0 | 0 |
| 03 | D1 | 1411 | 2.348 | 6.71 | 5.15 | 0.5 | 5.83 | 36.69 | 0 | 0 |
| 04 | C3 | 492 | 1.32 | 34.64 | 33.09 | 24.14 | 33.32 | 51.97 | 0 | 0 |
| 05 | D4 | 891 | 2.405 | 15.0 | 17.5 | 1.41 | 17.5 | 22.98 | 0 | 0 |
| 06 | C4 | 741 | 1.605 | 39.2 | 40.48 | 1.8 | 41.15 | 28.15 | 0 | 0 |
| 06b | C4 | 501 | 1.704 | 31.95 | 33.72 | 1.8 | 34.15 | 27.95 | 0 | 0 |
| 07 | D6 | 904 | 2.537 | 47.71 | 48.13 | 2.0 | 46.04 | 10.77 | 0 | 0 |
| 08 | B4 | 696 | 1.29 | 76.13 | 78.54 | 44.32 | 78.6 | 38.5 | 0 | 0 |
| 09 | C5 | 874 | 1.135 | 56.02 | 56.7 | 1.8 | 57.4 | 34.71 | 0 | 0 |
| 10 | E7 | 104 | 0.045 | 65.76 | 66.71 | 29.44 | 67.06 | 0.5 | 0 | 0 |
| 11 | C4 | 1150 | 1.099 | 67.8 | 69.1 | 17.89 | 69.77 | 48.63 | 0 | 0 |
| 12 | D6 | 421 | 1.178 | 67.53 | 68.31 | 0.5 | 66.19 | 15.7 | 0 | 0 |
| 13 | G4 | 577 | 1.61 | 2.06 | 2.92 | 1.8 | 2.0 | 77.78 | 0 | 0 |
| 14 | E1 | 647 | 3.223 | 5.7 | 7.43 | 1.8 | 6.8 | 19.14 | 0 | 0 |
| 15 | C6 | 697 | 1.014 | 93.43 | 94.04 | 9.18 | 93.13 | 33.74 | 0 | 0 |
| 16 | H6 | 1050 | 1.922 | 31.08 | 30.36 | 4.12 | 30.66 | 32.0 | 0 | 0 |
| 17 | H3 | 516 | 0.709 | 14.33 | 16.32 | 44.55 | 14.21 | 83.44 | 0 | 0 |
| 18 | H2 | 1304 | 1.241 | 2.06 | 5.7 | 55.86 | 1.58 | 65.12 | 0 | 0 |
| 19 | G3 | 1078 | 1.028 | 3.54 | 3.0 | 8.85 | 3.0 | 85.65 | 0 | 0 |
| 20 | E2 | 307 | 0.087 | 7.0 | 8.5 | 25.61 | 6.5 | 1.58 | 0 | 0 |
| 21 | F6 | 208 | 1.271 | 15.21 | 17.61 | 21.32 | 17.1 | 1.58 | 0 | 0 |
| 21b | F6 | 973 | 1.865 | 26.4 | 29.33 | 7.16 | 28.18 | 1.58 | 0 | 0 |
| 22 | F1 | 393 | 0.164 | 25.81 | 28.64 | 17.22 | 26.52 | 0.5 | 0 | 0 |
| 23 | G6 | 1359 | 1.705 | 22.68 | 20.43 | 0.5 | 21.02 | 6.8 | 0 | 0 |
| L3b_10 | E7/F7 | 3869 | 0.75 | 66.5 | 66.5 | 15.4 | 65.02 | Wasserstelle | 0 | 2267 |
| L3b_22 | F1 | 1677 | 0.669 | 23.88 | 26.28 | 7.91 | 24.23 | Wasserstelle | 0 | 361 |
| L3b_24 | C4/D4 | 840 | 1.402 | 28.86 | 30.91 | 1.8 | 31.18 | 28.43 | 0 | 0 |
| L3c_G7 | G7 | 1390 | 0.66 | 57.21 | 57.0 | 5.83 | 55.51 | Wasserstelle | 0 | 685 |
| L3c_C7 | C7 | 1511 | 0.818 | 125.9 | 126.57 | 43.8 | 124.45 | Wasserstelle | 0 | 808 |
| L3c_H7 | H7 | 2031 | 0.968 | 76.04 | 74.5 | 43.41 | 75.03 | Wasserstelle | 0 | 1044 |
| L3c_G7b | G7/H7 | 2802 | 1.057 | 55.11 | 53.24 | 10.4 | 53.6 | Wasserstelle | 0 | 1517 |

Summen nach dem Fix:
- Geänderte Vertices auf vektor.json-Weg / Kreuzung / Rampenkern (rampenwege ≤ 1,8) / WEGA-wege: **0 / 0 / 0 / 0**.
- Änderungen ohne Stelle: 0.
- Nicht-Wasserstellen auf Wasser: 0. Wasserstellen ändern Wasser gewollt; die Belege stehen unten.

Kleinste Abstände: 03, 12 und 23 liegen 0,5 Zellen am Rampenkern; das ist die geschützte Böschung `rampe_m`, nicht der Kern. 13 und 18 liegen 2,06 Zellen am Weg, 19 liegt 3,0 Zellen an der Kreuzung.

### Folgen des Fix für alte Stellen (Nahbild geprüft, `l3c_nahbilder/fix_regionen/`)
Wo der Schutz vorher falsch lag, wirkt jetzt die Stelle bzw. der Originalwert kehrt zurück. Betroffen sind 13 G4 (max 2,0 m), 23 G6 (max 1,7 m), 16 H6, 18 H2, L3b_22, 19 und 20. Im Ton-Nahbild ist jede dieser Regionen gleich oder ruhiger, nichts Neues ist sichtbar. Bei 23 G6 sind die Rippen am Hangfuß jetzt glatter. Die alte Begründung „Rippen am Weg G017 geschützt“ war maßstabsbedingt falsch: G017 liegt 22,7 Zellen entfernt.

> Hinweis: In G6 (Stelle 23) arbeitet ggf. Wege & Deko (P2b). L3c ändert GB dort um bis zu 1,7 m gegenüber `d5b17e2`; das ist beim Mergen zu beachten.

## 2. Ursache der „hellen Platten“ (geprüft)
- **C7 und G7-Ost:** **eingeschlossene Landinseln** in der Wassermaske, 39 + 3 Vertices (C7) und 5 Vertices (G7 ≈271,5\|259,5). Das Wasser endet dort in 0,5er Rasterkanten über hellem Gelände. Es ist keine Textur und keine Wasserfarbe. Behebung: Die Inseln werden Wasser (WV aus der Nachbarschaft), das Bett liegt 0,6 m unter dem Spiegel.
- **G7 Leitern/Linien:** 1-Zeilen-Rillen und Stufen in WV und Bett. Der Viewer zeichnet Schaum bei WV-Nachbarsprüngen über 0,9 (`viewer_alle.js`). Die Rillen wurden geschlossen und geglättet. Schaum-Vertices in G7: 83 → 1.
- **H7 Blöcke:** Das Landufer lag bis 0,37 m unter dem Spiegel. Es wurde knapp darüber gehoben (+0,08 m) und geglättet.
- **E2-Westufer und E3-Bach (Treppen):** Das ist der **Rasterrand des Wassermeshes im Renderer**. `viewer_alle.js` setzt Nicht-Wasser-Vertices auf `min(mittleres WR, GL+0,02)`, dadurch folgt die Wasserkante dem 0,5er Zellraster. Mit Daten allein ist das nicht lösbar (Versuch unten). → Dev UI.

## 3. Ergebnis je Stelle (Nahbild entscheidet, selbst angesehen)

| Stelle | Maßnahme | Ergebnis | Nahbild-Paar |
|---|---|---|---|
| G7 (≈255–265\|265–276) + Ost (x 266–298) | `L3c_G7`, `L3c_G7b` | **weg**: keine Leitern, keine Linien, keine Platte, Wasser durchgehend | `l3c_nahbilder/paare/G7_vorher_nachher.jpg` |
| C7 (≈88–100\|276–284) | `L3c_C7`: 2 Inseln gefüllt | **weg** | `paare/C7_vorher_nachher.jpg` |
| H7 (≈315–335\|268–280) | `L3c_H7`: Landufer heben | **teilweise**: Blöcke weg, Treppenrand der SO-Bucht bleibt → Ausnahme | `paare/H7_vorher_nachher.jpg` |
| E2-Westufer (Stelle 20) | Versuch Wasserrand: Landufer +0,12 m, WV-Randband −0,15 m | **Ausnahme**: Treppe bleibt (Renderer-Rasterkante) | `paare/E2_vorher_nachher.jpg`, Versuch `versuch_wasserrand_e1/` |
| E3 (≈186–193\|88–128) | 2 Versuche (L3c-Erstversuch, Wasserrand) | **Ausnahme**: Sägezahn = Renderer-Rasterkante; Wasserrand-Versuch ließ den Bach teils verschwinden → verworfen | `paare/E3_vorher_nachher.jpg`, `versuch_wasserrand_e1/` |

Paarblätter zeigen: Ton vorher \| Ton nachher \| Farbe vorher \| Farbe nachher. Einzelbilder liegen in `l3c_nahbilder/einzel/`.

## 4. Gate vorher/nachher (d5b17e2 → L3c), `L3c_gate_vorher_nachher.json`

| Prüfer | vorher | nachher |
|---|---:|---:|
| pruefe_regeln (export_gate) | 374 | 377 |
| pruefe_regeln mit eigenem Lochscan `/tmp/gate_loch_L3c.json` | 374 | 377 |
| r8 | 33 | 33 |
| r9 | 325 | 325 |
| W1 / W1 alle56 | 0 / 0 | 0 / 0 |

- Geändert ist nur **G6_facette 213 → 216**; G5_beule_klippe ist netto gleich (1 neu, 1 weg).
- 4 neue Treffer (G5 G4, G6 G6, G6 G7, G6 H7), alle im Nahbild unsichtbar, siehe `AUSNAHMEN_L3c.md`.
- **R6_wasser_schnee 4 → 4, G8_fluss_nicht_bis_rand 1 → 1, R5_loch 4 → 4.**
- Lochscan Hauptviewer: 0 offene Innenkanten.

## 5. Wasser-Belege (`l3c_sha_belege.json`)
- Wasser entfernt: 0 Vertices. Neues Wasser: 47 Vertices, nur die 3 eingeschlossenen Inseln; außerhalb von fill_holes(alt): 0.
- Flussverlauf/Außenkontur: SHA256 von fill_holes(Maske) vorher = nachher. Die Rohmaske ändert sich nur durch die Inseln.
- WV auf altem Wasser: 4092 Vertices geändert, max 0,895 m (Rillen und Stufen in G7/H7).
- Wasserfälle: keine in den Stellen. R6 und G8 unverändert.

## 6. Weitere Belege
- D2 bitgleich (`749d3c4b…80f6`; relief_l3 bricht sonst ab). D1 und D2: GB, WV und VC vs `d5b17e2` 0 Vertices geändert → **Sperrzone D1 (X084/rampe_2, Mulde 159\|22,9) unberührt**.
- Unverändert: G, WEGA, wege, rampenwege, bruecken, vektor.json, alle Prüfer und Schwellen.
- `alles.sh /tmp/l3c/p10`: Prototyp D1/G1/D2 identisch mit index.html, Naht max 0,0 m, Lochscan 56 nur C3-Positivkontrolle (3) → 0 echte Löcher.

- SHA256 Endstand: relief_daten.json.gz `d96fc4b4…`, neu/relief_neu.json.gz `a609c5b9…`, index.html = neu/index.html `74dad828…`.
- `--aus`-Roundtrip: an→aus→an zweimal gefahren. aus und an sind jeweils bytegleich. Zum allerersten an-Stand differiert nur VC (gen_textur ist nicht idempotent). Das Gate auf dem Endstand ist identisch (377/33/325/0). Die Exportsperre („GATE ROT“) bestand schon vorher bei 374.

## Pipeline
`relief_l3.py` → `gen_textur.py vc` → `waende_einsetzen.py` → `html_payload_p3.py` → Gate → `alles.sh`.
