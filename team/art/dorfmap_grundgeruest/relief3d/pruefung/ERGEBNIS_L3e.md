# ERGEBNIS L3e – F7-Nordufer-Zaehnchen, G7-Nordufer, G7-Plaettchen (Basis art/dorfmap-fertig @ b3698e0)

Kosten: 0 € · Codex: nein · Laufzeit: 16:05–16:51

Basis: **b3698e0** (L3d #31 gemergt; baut auf #31 auf). Branch art/dorfmap-L3e, vor dem ersten Push angelegt (kein Force-Push noetig).
Gate-Vorher auf b3698e0 gemessen: 369 / 31 / 325, W1 0, Lochscan 0. Nahbilder vorher/nachher mit dem Viewer `pruefung/alle_kacheln` (P12b) von b3698e0.

## Ergebnis je Stelle
| Prio | Stelle | Ergebnis |
|---|---|---|
| 1 | F7-Nordufer Zaehnchen ≈240\|271 | **behoben** – Zaehnchen weg, Uferlinie glatt (paar_F7_nord.jpg, kontur_F7_nord.png). Rest: sehr schwache helle Schlieren im Flachwasser am diagonalen Ostteil x≈244–250 (s. offene Befunde 1) |
| 2 | G7-Nordufer x 244–276 (Weg A) | **Treppe behoben** – sichtbare Uferlinie folgt der Hoehenlinie (Linienstuecke 6 → 2, Zacken max 0,295 → 0,124 Zellen, `l3e/l3e_konturmass.json`), Nahtkerbe 252\|264 weg (paar_G7_nord.jpg). **Offener sichtbarer Befund:** feiner heller Saegesaum am Rand aus Abstand noch erkennbar (offene Befunde 1) |
| 3 | G7-Plaettchen NO ≈283,5\|268,8 (QA) | **behoben** – Plaettchen weg, auch im Ton (paar_G7_plaettchen.jpg) |
| 4 | Ufer E7–H7, gleichartige Zaehnchen | **gesucht, keine gleich starke Stelle**: Datenmass (Landvertex ≤ 0,15 m ueber Spiegel neben ≥ 0,3 m tiefem Wasservertex) → 22 Kandidaten, die 12 groessten als Nahbild (S_*.jpg, paar_uferschau_E7_H7.jpg). Kein Zaehnchen wie F7. Sichtbar feine Zacken nur an F7/G7-Suedufer ≈246\|279 und E7-Rinne x≈218 (offene Befunde 2) |
| 5 | E3-West Rest-Zickzack | **nicht bearbeitet** (Zeit, Prio 5) – Stand wie L3d |
| – | QA G7 ≈255\|282 | **von QA gestrichen (Schaetzfehler, = F7 237\|275, in L3d behoben)** – keine Ausnahme |
| – | AUSNAHMEN_L3d.md | G7-Nordufer dort keine Ausnahme mehr (in L3e behoben, sichtbarer Rest = offener Befund hier); G7 255\|282 als „von QA gestrichen“ |

## Ursache (gemessen)
- **F7/G7-Zaehnchen und -Treppe = Geometrie + Maske, nicht VC.** Im Ton (clay) gleich sichtbar. Am Ufer liegen Landvertices nur 0–0,2 m ueber dem Spiegel
  direkt neben Wasservertices mit > 0,3 m tiefem Bett (teils Land unter / Bett ueber Spiegel). Die Hoehenlinie Gelaende = Spiegel schneidet dann jede
  Rasterkante am gleichen Bruchteil → Stufe je Vertex (Treppe/Zahn). Datenkontur-Plot `l3e_nahbilder/kontur_*.png` (rot = sichtbare Linie wie Viewer).
- **Nahtkerbe 252\|264 (Zwischenstand)**: kam aus dem Bezugsspiegel. Der Fluss faellt dort ≈0,8 m auf 2 Zellen; Naechster-Nachbar-Spiegel hat Stufen quer
  zum Ufer → Rippel in der Boeschung. Behoben mit glattem Bezug (Gauss 2 Vertices, auf altem Wasser wie Viewer-WR auf WV−0,6…WV+0,3 geklemmt).
- **G7-Plaettchen**: Suedwestufer mit Bett ueber Spiegel (Rasterinsel am Rand) – gleiche Ursache, gleiche Behandlung.

## Umsetzung (relief_l3e.py, Konfiguration pruefung/l3e/l3e_stellen.json, Art „ufer“ = Weg A)
- Vorzeichenabstand zur Wassermaske (±0,5 an der Kante), Gauss-geglaettet (σ 2 Vertices) → glatte Uferkurve, subzellig.
- Gelaende im Band (5 Vertices) = glatter Spiegel + Querprofil(Abstand): Profil aus den Daten (Median je Abstandsklasse), Kern |t| ≤ 1 Vertex linear
  durch 0 (Neigung ≥ 0,45 m/Vertex) – dann trifft die lineare Dreiecksinterpolation im Viewer die Nulllinie exakt; Wasserseite faellt mindestens bis 0,8 m.
- Maske waechst nur bis zur Kurve (neue Wasservertices nur angrenzend, WV = glatter Spiegel); **kein Wasser entfernt**, WV auf altem Wasser unveraendert.
- Vorzeichen im Kern erzwungen (Wasser ≥ 5 mm unter Spiegel, Land ≥ 5 mm darueber), feste Flaechen (Wege/Kreuzung/Rampenkern/WEGA/D2) ausgeschlossen.
- FW.h im Band bilinear auf das neue GB (3350 Feinbandpunkte), VC/FW.c unveraendert, 17 Objekthoehen nachgefuehrt. Basis-Hash-Pruefung im Skript.
- Stellen: F7_nord (x 230–242,5, z 267–274), G7_nord (x 244–276, z 250–271), G7_plaettchen (x 276–292, z 265–274).
- Zahlen: GB 2007 Vertices (max 0,567 m), neue Wasservertices 117 (16/78/23), VC 0.

Weg-A-Versuche am G7-Nordufer (alle mit Nahbild geprueft): a linear flach (heller Streifen) → b steiler (Streifen) → c Datenprofil (gut) → d linearer Kern →
e FW.h nachgefuehrt → f Kernneigung 0,45 → g/h Rest glatter, Boxen getrennt → i glatter Spiegelbezug (Nahtkerbe weg) → k Wasserseite tiefer (Endstand).
Die Treppe ist mit A behoben, Weg B (Polylinie) war deshalb nicht noetig; der Restsaum (unten) liegt im Viewer-Farbraster und waere mit B (Maske bleibt Raster) gleich.

## Gate je Regel (vorher b3698e0 / nachher L3e)
| Regel | vorher | nachher |
|---|---|---|
| regeln gesamt | 369 | **368** |
| G6_facette | 214 | **213** (G7 264,0\|268,8 Wert 18 weg, kein neuer Treffer) |
| alle uebrigen | gleich | gleich |
| R8 / R9 | 31 / 325 | 31 / 325 |
| W1 / W1 alle 56 | 0 / 0 | 0 / 0 |
| Lochscan (offen_innen) | 0 | 0 |
Dateien `pruefung/l3e/gate/*_vorher.json`, `*_nachher.json`. **Keine neuen Treffer.**

## Wasser-/Flusslauf-Beleg (`pruefung/l3e/l3e_abstaende.json`)
- Wasser entfernt 0; neue Wasservertices 117, alle am Ufer der drei Stellen (Box x 229,5–292,5, z 253,5–273), Liste `wasser_detail.neues_wasser_gruppen_x_z_n`.
- fill_holes-Unterschied = genau diese 117 Randvertices (keine eingeschlossenen Loecher gefuellt oder erzeugt), Komponenten 9 → 9, Lochscan 0.
- WV auf altem Wasser geaendert: 0. Bett ueber Spiegel 523 → 515 (nirgends mehr). Ein alter Wasservertex in G7_nord liegt landseitig der glatten Kurve
  und bleibt Wasser (kein Entfernen; unsichtbar, s. AUSNAHMEN_L3e.md).

## Abstaende / feste Flaechen (korrekter Massstab, zellweite_m 1,2)
Geaenderte Vertices 2007 (GB 2007, WV 117, VC 0).
| Flaeche | geaenderte Vertices darauf | kleinster Abstand |
|---|---|---|
| Weg (vektor.json) | 0 | 50,14 Zellen (60,17 m) |
| Kreuzung | 0 | 48,37 Zellen (58,05 m) |
| Rampenkern | 0 | 4,47 Zellen (5,37 m) |
| WEGA / Wege / Bruecken | 0 | 48,58 Zellen (58,3 m) |
| D2 | 0 | 191,64 Zellen (229,97 m); D2-GB sha 749d3c4b… vorher = nachher (bitgleich) |
Sperrzonen D1 (X084/rampe_2, Mulde 159\|22,9): kleinster Abstand 252 Zellen, nicht angefasst. Prototypen D1/D2/G1 unveraendert.

## bau_endstand.sh
Echter **Schritt 13** (relief_l3e.py → html_payload_p3.py → waende_einsetzen.py, Nebenausgaben pruefung/l3e/l3e_rueck.npz + l3e_bericht.json
werden mitverglichen). `L3E=0` laesst Schritt 13 weg (Stand nach 12 = b3698e0); L3E folgt standardmaessig L3D (L3D=0 mit L3E=1 bricht ab).
Volllauf `sh bau_endstand.sh /tmp/l3e_bau` auf Commit d2eac11: **ENDBAU BITGLEICH (416 s)**, 29/29 Ausgaben gleich (u. a. relief_daten, relief_neu,
index.html, neu/index.html, l3d_*, l3e_rueck.npz, l3e_bericht.json), keine Warnung zu geschriebenen Dateien.

## Rueckweg
`python3 relief_l3e.py --aus` (pruefung/l3e/l3e_rueck.npz: GB/WV/VC/FW.c/FW.h, Objekte, Prototypen) → relief_daten.json.gz cc9e8a0a…,
neu/relief_neu.json.gz 31c39f09… = b3698e0 (geprueft).Danach payload + waende: index.html und neu/index.html 03542379… = b3698e0 (bitgleich).
Wieder anwenden → exakt der Nachher-Stand (sha unten).

## SHA (nachher)
| Datei | sha256 |
|---|---|
| relief_daten.json.gz | a023ec2b82a8f83be020d1a9ec601b30fa9a90b14630f608f220081617ece29f |
| neu/relief_neu.json.gz | 399fc725844b5d380e7e941e3fc22ee4e0bdaf002a7f08f4a1e9cf683efd7f7c |
| index.html = neu/index.html | 97ce8f3ca795428a7f9352b8af52b611f567a69caef0e5de78272463d513a493 |
| pruefung/l3e/l3e_rueck.npz | 533cf3f756b9a45fe8118f0771dc7c152e1373a86b3bbfac86e8f7a4c57d0657 |
| relief_l3e.py | 88174f1829d346bc259d29f6e24f21e342dacf68e88353ef839cc12393cee9a9 |
| pruefung/l3e/l3e_stellen.json | 0df0456e59258f0dc896b4fafd74887845ea430a2bdb7933d231de1c2e1d5056 |
GB/WV/VC nachher (Skript): b3fbd201… (Basis f793b7ec…). D2-GB 749d3c4b… unveraendert.

## Offene sichtbare Befunde (Entscheidung bei Grundgeruest/New Bot: einfachere Geometrie, Maske, Viewer oder A/B an Fabian)
1. **Feiner heller Saum / Schlieren an diagonal (SW–NO) verlaufenden Ufern** – G7-Nordufer (aus Abstand, G7_nord_257_265, G7_nord_oben),
   F7-Ostteil x≈244–250 (F7_z_244_270). Messwert: Geometrie glatt (Kontur max 0,124 Zellen Abweichung, `l3e_konturmass.json`), aber Viewer-Alpha
   zeigt die Rastertreppe der Maske (`l3e_nahbilder/viewerfarbe_alpha_F7.png`, mittlere Zeile): P12b gibt Ring-1-Vertices Alpha ×0,6 und helle Flachwasserfarbe
   (Tiefe 0); die Dreiecke vom Ring 1 zum ersten Wasservertex liegen bei SW–NO-Ufern quer zur festen Dreiecksdiagonale (NW–SO) und ziehen die helle Farbe
   in Streifen ins Wasser. Unabhaengig von der Boeschungsneigung (0,25 und 0,45 m/Vertex gleich). Mit Daten allein nicht weg; Ansatz waere Viewer
   (z. B. Ring-1-Farbe = Nachbarwasserfarbe oder Alpha aus geglaetteter Tiefe) – nicht mein Auftrag (Viewer/Pruefer unveraendert).
2. **F7/G7-Suedufer ≈246\|279 und E7-Rinne x≈218 (z 254–267)**: feine Zacken am Rand (S_246_279, S_218_259). Versuch je einmal mit Art „ufer“:
   Suedufer ohne sichtbaren Gewinn (zurueckgenommen), E7-Rinne mit 2 neuen G6-Treffern (F6 217,9\|257,8 Wert 25, F7 214,5\|267,2 Wert 6) → zurueckgenommen.
3. **E3-West Rest-Zickzack** – nicht bearbeitet (Prio 5, Zeit).

## Nahbilder (`pruefung/l3e_nahbilder/`)
Je Kamera `<name>_akt_{farbe,ohnew,clay}_{vorher,nachher}.jpg` (Kameras `kameras.json`: Name, x, z, Abstand, Neigung; oben = Norden).
Paare: `paar_F7_nord.jpg`, `paar_G7_nord.jpg`, `paar_G7_plaettchen.jpg`, `paar_uferschau_E7_H7.jpg`. Datenplots: `kontur_F7_nord.png`, `kontur_G7_nord.png`,
`viewerfarbe_alpha_F7.png`. Selbst angesehen, Bewertung wie oben.
