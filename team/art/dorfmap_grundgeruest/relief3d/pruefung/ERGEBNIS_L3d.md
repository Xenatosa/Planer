# ERGEBNIS L3d – QA-P4d-Platten, H7-Rand, E3-Westufer, G7-Nordufer (Basis art/dorfmap-fertig @ 2771f70)

Kosten: 0 € · Codex: nein · Laufzeit: 15:14–16:05

Basis: zunaechst 9742a92, nach Steuerung (P12b #29 gemergt) lokal auf **2771f70** neu angelegt (vor dem ersten Push, kein Force-Push).
2771f70 aendert gegenueber 9742a92 nur viewer_alle.js + P12b-Berichte; Reliefdaten identisch (relief_daten sha 76a1e583…).
Gate und alle Nahbilder auf 2771f70 mit dem normalen (jetzt weichen) Viewer. Erweiterung nach QA P4d (PR #30, LISTE_SICHTBAR.md).

## Ergebnis je QA-Stelle
| QA | Ort | Schwere | Ergebnis |
|---|---|---|---|
| S1 | E7 ≈193\|276 (Insel 22 Vertices) | stark | **behoben** – Platte weg (paar_P4d_stark_1.jpg) |
| S1 | E7 ≈202\|275 (3 V.) | stark | **behoben** (paar_P4d_stark_2.jpg) |
| S2 | F7 ≈218\|274 (6 V.) | stark | **behoben** (paar_P4d_stark_1.jpg) |
| S3 | F7 ≈237\|275 (9 V., Treppenrand) | stark | **behoben** (paar_P4d_stark_1.jpg) |
| S4 | H7 ≈303\|268 (6 V.) und ≈308\|268 (9 V.) | stark | **behoben**, beide Bloecke weg (paar_P4d_stark_2.jpg, auch Ton) |
| S5 | H7-Suedostbucht ≈333\|276, weisse Kuppe | leicht | **behoben** – Landkuppe am Kartenrand wird Wasser (69 V.), unter Wasser nur noch weicher heller Schimmer (paar_P4d_leicht.jpg) |
| S6 | H7-Rand x=336 z≈281,5, V-Kerbe | leicht | **behoben** – Spiegel dort 0,86 m zu tief (5 V.), auf Median der Nachbarn; Kerbe und flache Platte weg |
| S8 | A7 ≈30–33\|263, B7 ≈46\|265,5, C7 ≈129\|270,5 (QA 124\|268), D7 ≈136\|270,5 | leicht | **behoben** (5 Inseln, 19 V.; S8_*-Bilder) |
| S8 | G7 ≈255\|282 | leicht | **Ausnahme: nicht reproduzierbar** – dort Land 2,1 m ueber Spiegel, keine Insel/kein Bett ueber Spiegel im Umkreis 10 m, Nahbild ohne Platte (AUSNAHMEN_L3d.md) |
| – | E3-Westufer (Zickzack in VC/Rinne) | Auftrag | **verbessert** (maessig): Rinne quer geglaettet + VC-Uebergang lokal, Zacken weicher, nicht ganz weg |
| – | G7-Nordufer westlich x≈265 (Maskenrand) | Auftrag | **Ausnahme** nach 2 Versuchen (AUSNAHMEN_L3d.md), Maske dort unveraendert |

Ursache S1–S4/S8: kleine, ganz von Wasser umschlossene Landinseln in der Wassermaske (WV = −999) – das Gelaende ragt dort als flache Rasterplatte
(0,5-Zellen-Kontur) ueber den Spiegel, im Wasser deshalb hell und eckig. Keine Textur-, sondern eine Masken-/Hoehenursache.

## Umsetzung (relief_l3d.py, Konfiguration pruefung/l3d/l3d_stellen.json)
- **P4d_platten** (Art „inseln“): Inseln, deren Schwerpunkt ≤ 4 Zellen von einem QA-Punkt liegt (max. 60 Vertices) → Wasser; WV = Mittel des
  Wasserrings (flach); Huegel darunter harmonisch auf das umgebende Bett abgesenkt (Radius 4 Vertices, nie angehoben), Insel ≥ 0,5 m unter Spiegel;
  VC der Inselvertices = Ringmittel. 11 Inseln, 74 Vertices. Grosse Insel D7/E7 170,9\|261,1 (155 V.) und F6 222,6\|221,5 nicht im Befund → nicht angefasst.
- **P4d_S5_bucht** (Art „bucht“): Box x 332,5–336, z 275–280; Maske waechst in Land ≤ 0,9 m ueber Nachbarspiegel, Restinseln mitgenommen,
  GB ≤ Spiegel − 0,3 m. 69 neue Wasservertices.
- **P4d_S6_kerbe** (Art „wv_glatt“): Box x 330–336, z 279–285; Wasservertices mit |WV − Median(5×5-Wassernachbarn)| > 0,3 m → Median. 5 Vertices (max 0,864 m).
- **E3_west** (Art „farbe“ + rinne, unveraendert seit erstem Stand): VC 1508 Vertices (max 22 Stufen), GB-Rinne 945 Vertices; 3 Runden Nachglaetten mit Klemmen.
- **G7_nord** (Art „wassermaske“): `aktiv: false` (zwei Versuche dokumentiert).
- FW.h folgt den GB-Aenderungen bilinear (571 Feinbandpunkte, relief_l3.fw_folgen), FW.c aus VC (40 Punkte). Rueckweg speichert GB/WV/VC/FW.c/FW.h.

## Gate je Regel (vorher 2771f70 / nachher L3d inkl. P4d)
| Regel | vorher | nachher |
|---|---|---|
| regeln gesamt | 372 | **369** |
| G6_facette | 217 | **214** (3 E3-Treffer weg, kein neuer) |
| alle uebrigen (G2, G2f, G3f, G5, G7, G7b, G8, R1–R6, T1–T5) | gleich | gleich (G8 1/1, R6 4/4) |
| R8 / R9 | 31 / 325 | 31 / 325 |
| W1 / W1 alle 56 | 0 / 0 | 0 / 0 |
| Lochscan (offen_innen) | 0 | 0 |
Dateien `pruefung/l3d/gate/regeln_vorher.json`, `regeln_nachher.json`. Keine neuen Treffer.

## Wassermasken-Beleg (`pruefung/l3d/l3d_abstaende.json`)
- Wasser entfernt: 0. Neue Wasservertices 143 in 12 Gruppen = genau die 11 Inseln + Bucht S5 (Liste `wasser_lokal.neues_wasser_gruppen_x_z_n`).
- fill_holes-Vergleich: Unterschied nur in der Bucht S5 (69 Vertices, Box x 331,5–336, z 276–279,5, am Kartenrand); die Inseln lagen schon im
  fill_holes des Flusses → Aussenkontur des Flusslaufs sonst unveraendert. Komponenten 9 → 9, keine neuen Inseln (Skriptabbruch sonst).
- WV auf altem Wasser nur S6 geaendert (5 Vertices ab 334\|281,5). Bett ueber Spiegel (alte Maske) 525 → 523, nirgends angehoben.
- G7-Nordufer: Maske dort bitgleich.

## Abstaende / feste Flaechen (korrekter Massstab, zellweite_m 1,2)
Geaenderte Vertices 2407 (GB 1791, WV 148, VC 1581).
| Flaeche | geaenderte Vertices darauf | kleinster Abstand |
|---|---|---|
| Weg (vektor.json) | 0 | 0,5 Zellen (0,6 m) |
| Kreuzung | 0 | 1,5 Zellen (1,8 m) |
| Rampenkern | 0 | 21,5 Zellen |
| WEGA/wege/Bruecken | 0 | 0,5 Zellen (0,6 m) |
| D2 | 0 | 15,5 Zellen |
D2 GB sha256 749d3c4b… vorher = nachher. Sperrzonen D1 (X084/rampe_2, Mulde 159|22,9): nicht beruehrt (Aenderungen nur z ≥ 83,5; Mulde ≥ 65 Zellen). Skript `pruefung/l3d/l3d_abstaende.py`.

## bau_endstand.sh
Schritt 12 (nach L3c2-Schritt 11, der schon drin war): `relief_l3d.py`, `html_payload_p3.py`, `waende_einsetzen.py`; Nebenausgaben
`pruefung/l3d/l3d_rueck.npz` + `l3d_bericht.json` werden mitverglichen. `L3D=0` laesst Schritt 12 weg.
Kompletter Lauf `sh bau_endstand.sh /tmp/l3d_endbau` auf Commit 40c391a (Code/Daten = Lieferstand; danach nur Berichte): **27/27 gleich, ENDBAU BITGLEICH (411 s)**, Schritt l3d 13 s (pruefung/l3d/bau_endstand_sha256_vergleich.txt).

## Rueckweg
`python3 relief_l3d.py --aus` → relief_daten/relief_neu sha = 2771f70 (76a1e583… / 233b8373…), danach html_payload_p3.py + waende_einsetzen.py fuer index.html.
Wieder anwenden → bitgleich (geprueft).

## SHA Lieferstand
relief_daten.json.gz cc9e8a0a7982f5c1836fd86edb9b2b749c768135582d2cdcb71a209f68258281
neu/relief_neu.json.gz 31c39f093d53c309798b5752ce28ddc60ab63960148e177b1d12f34eba2b301c
index.html = neu/index.html 03542379541b64ec6b7041ad368829bc7d6698ff5752d18d881993bebe8c6fc2
pruefung/l3d/l3d_rueck.npz 112d8599…, l3d_bericht.json d710ab84…

## Nahbilder (pruefung/l3d_nahbilder/, Viewer 2771f70, je farbe / ohnew = ohne Wasser / clay, vorher|nachher)
- Paare gross: `paar_P4d_stark_1.jpg` (E7 193, F7 218, F7 237), `paar_P4d_stark_2.jpg` (H7-Bloecke farbe+Ton, E7 202), `paar_P4d_leicht.jpg` (S5, S6, C7, G7 255|282),
  `paar_E3_west_gross.jpg`, `paar_G7_nord_gross.jpg`.
- Uebersichten: `uebersicht_P4d.jpg` (alle 13 QA-Kameras), `uebersicht_E3.jpg`, `uebersicht_E3_querschnitte.jpg`, `uebersicht_G7.jpg`; Einzelbilder `S*_…`, `E3_*`, `t*_E3_*`, `G7_*`.
Ehrliche Bewertung: Alle starken Platten sind spurlos weg (auch im Ton-Bild); S5/S6 sauber. E3 nur maessig besser. G7-Nordufer unveraendert (kleine Zacken im weichen Rand).
Nebenbei gesehen (nicht im Auftrag, nicht angefasst): kleine helle Zacken am F7-Nordufer ≈240|271 (Kamera S3 oben).

Pruefer und Schwellen unveraendert. Nichts nach main.
