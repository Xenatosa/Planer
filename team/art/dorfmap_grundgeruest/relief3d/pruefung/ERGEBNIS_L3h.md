# ERGEBNIS L3h – E3-Bach kräftiger, E4-Bach glatter Uferrand (QA P4e S3/S4) – Basis art/dorfmap-fertig @ f942124 (nach #37 P2e)

Kosten: 0 € · Codex: nein · Laufzeit: 18:45–@@ENDE@@

Worktree /workspace/wt_dorfmap_L3h, Branch art/dorfmap-L3h. Start auf bfe8dce, entwickelt dort (v1–v3). Nach Merge von #37 (P2e, Wege & Deko) auf den neuen
Kopf **f942124** gesetzt (Branch war noch nicht gepusht, kein Force-Push nötig): Code/Konfig übernommen, **Binärdaten über die Pipeline neu gebaut**
(nicht übernommen), Basis-Hash in `l3h_stellen.json` auf den Stand nach Schritt 16 gesetzt; Gate, Volllauf, Abstände und Nahbilder auf diesem Endstand.
Neues Skript `relief_l3h.py` = bau_endstand **Schritt 17** (Schritt 16 belegt P2e/Wege & Deko #37) (`L3H=0` schaltet ab, Rückweg `--aus` mit `pruefung/l3h/l3h_rueck.npz`), Stellen in `pruefung/l3h/l3h_stellen.json`.
Viewer: normaler Viewer (P12c); vorher = f942124, nachher = Endstand. Kameras wie QA P4e (E3_bach_weit/mittel, E3_westufer_100/106, E4_bach_145/weit) + Distanz von Norden.

## Kurz
| Stelle | Ergebnis |
|---|---|
| (1) E3-Bach ≈190\|100–120 | **verbessert**: aus Nähe und Distanz (22–60 m) jetzt deutlich als blaues Wasser lesbar statt Schattenfurche, durchgehend im Südteil (bach_mittel/weit). Ehrlich: im schmalen Nordteil (≈188–190\|100–106) bleibt der Ton ungleichmäßig, dort wirken einzelne tiefere Stellen wie kleine Tümpel (Perlen), aus der Distanz nur schwach. Westufer-Form unverändert (westufer_100/106), kein Zickzack zurück. |
| (2) E4-Bach ≈176\|146 | **gelöst**: der dunkle, gezackte Uferrand („Reißverschluss“) ist in Farbe und Clay weg; Bach breiter, Böschung sanft, Bach sichtbar. Ursache gemessen: am Westufer springt die VC auf einem Vertex von ≈230 (Schnee) auf ≈165 (Bett), entlang der Maskentreppe (Ostufer hat einen Verlauf über ≈6 Vertices); dazu der Böschungssprung (Land −1,00…−1,12 m neben Bett −1,48…−1,76 m). |

## Verfahren
- **E3_bett** (Art `bett_tiefer`): Gewicht über das geglättete Abstandsfeld zum Ufer (nicht über Maskenzellen): Ufer-Vertex (Abstand ≤ 0,8 V.) bleibt, ab 2,5 V. voll;
  längs der Rinne verschmiert (normierte Gauß-Faltung σ 4 nur über Wasser, damit keine Perlenkette). Bett im Kern bis 0,55 m unter Spiegel (nur absenken),
  Bett-VC mit Anteil 0,55 Richtung Seeboden-Ton (G7-See ≈125|132|132), Ufer-VC leicht weich (σ 1,5, Band 3). Mittl. Wassertiefe E3 0,12 → 0,30 m (max 0,33 → 0,55), Bett-VC 158|167|175 → 148|156|161.
- **E4_rinne** (Art `ufer` wie L3g/E3 v2): Versatz 1,5 V., σ 3, Band 8, Kern 2,5 V., Neigung ≥ 0,15 m/V., Bett ≥ 0,3 m; Box 170–185|135–153 (Fade 3), 47 neue Wasser-Vertices, nichts entfernt.
- **E4_bett**: wie E3_bett (Kern 0,6 m), dazu Ufer-VC über das geglättete Vorzeichen-Abstandsfeld weich gezeichnet (σ 2, Band 4) → Farbverlauf statt Stufe.
- Versuche (Nahbilder `l3h_nahbilder/versuche/`): v1 (ohne Längsverschmierung, E4-Box bis z 158): E3 Perlenkette, E4-Zacken in Farbe bleiben (VC), Gate 370.
  v2 (+ VC-Glättung E4, Längsverschmierung): E4-Zacken weg, Gate 369 (R5_loch an der Seemündung 178|159, G6 an den Boxkanten, G6 E3 184,5|115,5 Wert 41 durch Vertiefung am Ufer-Vertex).
  v3 (Endstand): E4-Box 135–153 (weg von der Mündung), Längsverschmierung lässt den Ufer-Vertex aus, E3 Kern 0,55 m → Gate 363.

## Gate (Endstand)
regeln **363** (vorher 367), R8 **31**, R9 **321**, W1 **0**, W1 alle 56 0, Lochscan **0** (offen_innen 0). Gegen f942124 nur Wegfall: G6 E4 175,6|140,2, 175,0|151,5, 173,0|152,7,
T1_fleckrand E4 175,0|144,2; keine neuen Treffer. Laufergebnisse `pruefung/l3h/gate/` (inkl. lochscan.json). **Auflage Aufseher:** `pruefung/regeln_letzter_lauf.json`, `r9_letzter_lauf.json` (und r8/w1/w1_alle56) = dieser Gate-Lauf auf dem Endstand, nur über diesen PR.
Hinweis: export_gate.sh meldet lokal wie in allen Läufen „GATE ROT: kein Export/ZIP“ (kein Export-ZIP im Worktree) – unabhängig von L3h, auch auf der Basis so.

## Abstände / Wasser (`pruefung/l3h/l3h_abstaende.py` → `.json`, Basis f942124, zellweite_m 1,2)
Geänderte Vertices 2008 (GB 1334, WV 47 = nur neue Wasser-Vertices, VC 1694), Box 168,5–193|89,5–155,5.
Darauf: Wege **0** (kleinster Abstand 0,6 m), Kreuzungen **0** (0,6 m), Rampenkern **0** (38,5 m), WEGA/Wege/Brücken **0** (0,6 m), D2 **0** (21,5 m; D2-GB sha 749d3c4b… vorher = nachher).
**Sperrzonen:** rampe_5 (rampenwege[5], Wege & Deko) kleinster Abstand **33,6 Zellen = 40,3 m**; Kachel D4/D5 (x 126–168, z 129–215): **0 Änderungen**, kleinster Abstand 0,5 Zellen zur Kachelgrenze x 168;
D1 (inkl. X084/rampe_2): 50 Zellen; Mulde 159|22,9: 72 Zellen. Das Skript bricht ab, wenn in D1/Mulde/D4/D5 etwas geändert würde.
Wasser entfernt 0, WV auf altem Wasser 0, Komponenten 9→9, fill_holes-Differenz = genau die 47 neuen Vertices (keine Löcher), Bett über Spiegel 512 → 506.
Land überflutet nur durch die gewollte Rinnenverbreiterung E4.

## bau_endstand.sh
Schritt 17 (relief_l3h.py → html_payload_p3.py → waende_einsetzen.py), Nebenausgaben l3h_rueck.npz + l3h_bericht.json mitverglichen, `L3H=0` schaltet ab (L3H folgt P2E; L3H=1 mit P2E=0 bricht ab).
Volllauf auf dem Endstand (f942124 + L3h): @@BAU@@

## Rückweg
`relief_l3h.py --aus` + html_payload_p3 + waende_einsetzen → relief_daten 3e37ea58…, relief_neu 3069a0ef…, index 976a4cb1… = exakt f942124 (geprüft), danach wieder Commit-Stand.

## SHA (Endstand)
| Datei | sha256 |
|---|---|
| relief_daten.json.gz | b2ef88a6d3895d090e69660f8a1d17fb7d0ee6acac7324da8da947c72eacd66f |
| neu/relief_neu.json.gz | 575362c0680f2e52074d3407a9762089d7d3e4232378962246c82bc99c86cab5 |
| index.html = neu/index.html | ddedba2bfaae0468173425775ff66f8912132a1f3149f60153552c6f274aa8b3 |
| relief_l3h.py | 8950bb4dccd03a428f03b0b6452a514b0b8317813e3411d65d4853a511c0dcb6 |
| bau_endstand.sh | 24ff110da1abcefe6e7a092c5954dbf878e105c7339f2a8534ccf7de6a0bb00f |
| pruefung/l3h/l3h_rueck.npz | b75cbcf34f1669dea55039925805d7c37abeef03bef83e885362b97b7d3d485a |

## Nahbilder (`pruefung/l3h_nahbilder/`, selbst angesehen)
- `blatt_E3_vorher_nachher.jpg`: E3_bach_weit (45 m), E3_bach_mittel (22 m), E3_westufer_100/106 (15 m), E3 Distanz von Norden (60 m); je Farbe vorher|nachher, Clay vorher|nachher.
- `blatt_E4_vorher_nachher.jpg`: E4_bach_145 (15 m), E4_bach_weit (30 m), E4 Distanz von Norden (45 m).
- Einzelbilder `einzel/<Kamera>_{farbe,clay}_{vorher,nachher}.jpg`; Versuche `versuche/` (v1, v2, Blätter v1|v2|v3).
Die E3/E4-Ausschnitte sind pixelgleich zu v3 auf bfe8dce (P2e ändert nur D4/D5). Bewertung: E4 klar besser (Zacken weg). E3 klar kräftiger und als Wasser lesbar; Restschwäche Nordteil (ungleichmäßiger Ton, kleine Tümpel-Wirkung) – leicht.
