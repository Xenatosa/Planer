# Ergebnis p3d4

Stand: 2026-11-07 · Worktree `/workspace/wt_dorfmap_p3d4` · Branch `art/dorfmap-p3d4` · Basis `origin/art/dorfmap-p3d3` (`ad479b9`)

## Aenderungen

- `neu/mesh.py`: Drei unabhaengige, per Umgebungsvariable schaltbare Wegende- und Kreuzungsvarianten. Standard ist Gelaendevariante 2, Wegendevariante 1 und Kreuzungsvariante 2. Wegende 1 korrigiert nur die drei D1/G1-Endpunkte mit R8a-Treffern, mit mindestens 4 m Auslauf und maximal 0,10 Neigung. Kreuzung 2 verwendet eine radiale gemeinsame Flaeche ohne Laengsarme; der Rand ist 3 m breit. Damit bleibt das andere D1-Ende `156.5|37.5` ausserhalb des Kreuzungsarms.
- `neu/wand.py`: Eigener Schalter fuer den Wandfuss. Die Standardvariante senkt nur den Wandfuss bis 0,15 m unter das vorhandene Terrain. Die Terrainhoehe wird mit derselben Dreiecksdiagonale wie im angezeigten Terrainmesh abgetastet; die Probe umfasst die tatsaechliche Wandbreite. Die Klippenoberkante bleibt unveraendert.
- `main.js`, `neu/pipeline.py` und `neu/build.json`: Sparse Wegende-Erweiterungen werden am sichtbaren Neu-Mesh eingebunden und die Mesh-/Wandmesswerte werden protokolliert. `pruefung/neu_mesh_adapter.py` speist fuer die unveraenderten historischen Gates die sichtbaren D1/G1-Meshwerte ein; D2 wird bytegleich durchgereicht.
- `neu/delta.py`: Die Delta-Ergebniszeilen erhalten fuer ein einheitliches JSON-Schema auch bei Regelanstiegen das optionale Feld `metrik: null`. Gate- und Bildanstiege brechen weiterhin mit Exit 1 ab.
- `index.html`, `neu/index.html` und `pruefung/bilder_p3d4/`: finaler Neu-Mesh-Viewer, Kameras sowie je fuenf Clay-Kontroll- und Ergebnisbilder.

Keine Zellquellwerte, Quellspalten, Overlay-, Referenz- oder Pruefschwellen wurden geaendert. Kein globaler Relief-Rewrite, keine globale Daempfung, kein Prozesspool und keine Loeschung.

## Direkte Gates und sichtbares Neu-Mesh

Die unveraenderten Direktpruefungen auf `relief_daten.json.gz` reproduzieren fuer `pruefe_regeln.py` 570 Treffer statt der Auftragsnotiz 596; R8=48 und R9=334 stimmen mit der Notiz ueberein. Anschliessend wurden dieselben Gates mit dem Neu-Mesh-Adapter ausgefuehrt. Die Zaehler in der Spalte „nachher“ sind daher Messungen am sichtbaren Neu-Mesh, nicht Legacy-GB-Zaehler.

### `pruefe_regeln.py`

| Regel | direkt vorher | sichtbares Neu-Mesh | D1 vorher→nachher | G1 vorher→nachher | D2 vorher→nachher |
|---|---:|---:|---:|---:|---:|
| G11_objekt_schwebt_sinkt | 0 | 4 | 0→2 | 0→2 | 0→0 |
| G2_spitze_oben | 3 | 3 | 0→0 | 0→0 | 0→0 |
| G2_spitze_oben_fein | 8 | 8 | 0→0 | 0→0 | 0→0 |
| G3_spitze_unten | 3 | 3 | 0→0 | 0→0 | 0→0 |
| G3_spitze_unten_fein | 2 | 2 | 0→0 | 1→0 | 0→0 |
| G5_beule_klippe | 68 | 67 | 1→0 | 0→0 | 0→0 |
| G6_facette | 220 | 216 | 5→0 | 4→3 | 0→0 |
| G7_wand_glatte_flaeche | 1 | 1 | 0→0 | 0→0 | 0→0 |
| G7b_wandkontur_feld | 24 | 25 | 0→1 | 0→0 | 0→0 |
| G7b_wandkontur_kantenschaerfe | 1 | 1 | 0→0 | 0→0 | 0→0 |
| G7b_wandkontur_rauheit | 1 | 1 | 0→0 | 0→0 | 0→0 |
| G8_fluss_nicht_bis_rand | 1 | 1 | 0→0 | 0→0 | 0→0 |
| R1_blind | 24 | 24 | 2→2 | 1→1 | 0→0 |
| R2_getrennt | 15 | 15 | 1→1 | 0→0 | 1→1 |
| R3_laengs_m | 35 | 39 | 6→10 | 1→1 | 0→0 |
| R3_quer_pct | 23 | 19 | 11→7 | 0→0 | 0→0 |
| R3_woelb_m | 22 | 19 | 10→7 | 0→0 | 0→0 |
| R5_loch | 17 | 17 | 0→0 | 0→0 | 0→0 |
| R6_wasser_schnee | 4 | 4 | 0→0 | 3→3 | 0→0 |
| T1_fleckrand | 94 | 94 | 0→0 | 3→3 | 7→7 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | 0→0 | 0→0 | 0→0 |
| T3_streifen_ringe_bildpruefung_offen | 1 | 1 | 0→0 | 0→0 | 0→0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | 0→0 | 0→0 | 0→0 |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | 0→0 | 0→0 | 0→0 |
| **Summe** | **570** | **567** | **36→30** | **13→13** | **8→8** |

### R8

| Regel | vorher | sichtbares Neu-Mesh | D1 vorher→nachher | G1 vorher→nachher | D2 vorher→nachher |
|---|---:|---:|---:|---:|---:|
| R8_stufe | 9 | 7 | 2→0 | 0→0 | 0→0 |
| R8_gitter | 10 | 8 | 2→0 | 0→0 | 0→0 |
| R8_quer | 5 | 4 | 1→0 | 0→0 | 0→0 |
| R8a_wegende | 24 | 20 | 3→0 | 1→0 | 0→0 |
| **Summe** | **48** | **39** | **8→0** | **1→0** | **0→0** |

### R9

| Regel | vorher | sichtbares Neu-Mesh | D1 vorher→nachher | G1 vorher→nachher | D2 vorher→nachher |
|---|---:|---:|---:|---:|---:|
| R8b_delle | 25 | 22 | 2→0 | 1→0 | 0→0 |
| R9_saegezahn | 34 | 34 | 1→1 | 1→1 | 0→0 |
| R9w_wellen | 275 | 280 | 23→21 | 6→12 | 0→0 |
| **Summe** | **334** | **336** | **26→22** | **8→13** | **0→0** |

R9w steigt global genau um +5 gegen den historischen Direktwert. In G1 betraegt der Direktvergleich fuer R9w +6; gegen die sichtbare Neu-Mesh-VAR0-Kontrolle sinkt G1 von 13 auf 12. Die strenge Neu-Mesh-Deltapruefung ist unten ausgewiesen.

## Zielmessungen

- **D1-Kreuzung `152.5|28.5`:** R8-Stufe **0,116 m**, Gitter **0,000 m**. Gegenueber der sichtbaren VAR0-Kontrolle (1,746 m / 2,353 m) ist die Stufe um 1,630 m gesunken. Der Uebergang ist radial und ohne harte Platte.
- **D1-Endpunkt `156.5|37.5`:** R8-Stufe **0,188 m**, Gitter **0,089 m**; im p3d3-Mesh waren es 0,380 m, in VAR0 0,064 m. Damit liegt der Endpunkt unter 0,20 m und ist gegenueber p3d3 verbessert, aber nicht ganz auf Kontrollniveau.
- **D1/G1 R8a:** an den drei betroffenen D1- und einem G1-Endpunkt verbleibt **kein Treffer** oberhalb 0,10 m. Global bleiben 20 R8a-Treffer in anderen Kacheln stehen; sie wurden nicht global bearbeitet.
- **R3_laengs D1:** **6→10** gegen die Neu-Mesh-VAR0-Kontrolle (+4); gegen das p3d3-Kontrollziel waere Delta ≤0 erforderlich. Dieses Teilziel ist verfehlt.
- **Clay Wandfuss D1:** Facetten **382→419** und Normalenspruenge **3696→3760** gegen VAR0; gegen den p3d3-Endstand (415 / 3811) sind Facetten +4 und Normalenspruenge −51. Die Naht bleibt im Bild sichtbar. Die Forderung „keine Facettenzunahme“ ist damit knapp verfehlt; die Klippenoberkante blieb unveraendert.
- **Mesh-Aenderungen:** D1 956 geaenderte Hoehenvertices, max. |Delta| 3,305 m; G1 480, max. |Delta| 0,559 m; D2 0. D1/G1-Erweiterung ausserhalb der Kacheln: 293 grobe und 1.246 feine Stuetzstellen.

## Clay-Bilder und Bildzahlen

Die Bilder wurden mit demselben Browser, derselben Kamera und derselben Clay-Einstellung gerendert und einzeln angesehen. Zahlen sind Bildindikatoren, keine Ersatzmessung fuer Hoehenbytes. D2-Hoehenhash und Adapter-Guard sind bytegleich; der finale D2-Screenshot war bei einer direkten Wiederholung ebenfalls bytegleich. Die D2-Bildindikatoren unterscheiden sich dennoch leicht von der VAR0-Aufnahme.

| Ansicht | VAR0-Kontrolle | p3d4 Neu-Mesh | Sichtbefund |
|---|---|---|---|
| D1 Kreuzung | [Bild](bilder_p3d4/control/clay/D1_kreuzung.png) | [Bild](bilder_p3d4/mesh/clay/D1_kreuzung.png) | Weicher gemeinsamer Uebergang; R8-Stufe 0,116 m. Bildindikatoren fuer Normalenspruenge steigen. |
| D1 Wandfuss 140\|35 | [Bild](bilder_p3d4/control/clay/D1_wandfuss_140_35.png) | [Bild](bilder_p3d4/mesh/clay/D1_wandfuss_140_35.png) | Naht am T-Anschluss bleibt sichtbar. Facettenzaehler gegen VAR0 erhoeht. |
| D1 Wegende | [Bild](bilder_p3d4/control/clay/D1_wegende.png) | [Bild](bilder_p3d4/mesh/clay/D1_wegende.png) | Weicher Auslauf; kleinere Restkanten bleiben im Schattenbereich sichtbar. |
| G1 Wandfuss | [Bild](bilder_p3d4/control/clay/G1_wandfuss.png) | [Bild](bilder_p3d4/mesh/clay/G1_wandfuss.png) | Anschluss ist sichtbar; Bildmetriken bleiben gleich oder sinken leicht. |
| D2 Draufsicht | [Bild](bilder_p3d4/control/clay/D2_draufsicht.png) | [Bild](bilder_p3d4/mesh/clay/D2_draufsicht.png) | Keine neue Reliefaenderung erkennbar; Meshhoehen bleiben bytegleich. |

| Ansicht | Metrik | VAR0 | p3d4 | Δ |
|---|---|---:|---:|---:|
| D1 Kreuzung | Facetten | 445 | 369 | −76 |
| D1 Kreuzung | Normalenspruenge | 511 | 775 | +264 |
| D1 Kreuzung | Sprunginseln | 94 | 113 | +19 |
| D1 Wandfuss | Kantenzaehne | 1562 | 1540 | −22 |
| D1 Wandfuss | Facetten | 382 | 419 | +37 |
| D1 Wandfuss | Normalenspruenge | 3696 | 3760 | +64 |
| D1 Wandfuss | Sprunginseln | 173 | 205 | +32 |
| D1 Wandfuss | Loecher | 51 | 48 | −3 |
| D1 Wegende | Facetten | 787 | 807 | +20 |
| D1 Wegende | Normalenspruenge | 2453 | 2180 | −273 |
| D1 Wegende | Loecher | 42 | 43 | +1 |
| G1 Wandfuss | Facetten | 532 | 530 | −2 |
| G1 Wandfuss | Normalenspruenge | 2877 | 2874 | −3 |
| D2 Draufsicht | Kantenzaehne | 313 | 314 | +1 |
| D2 Draufsicht | Normalenspruenge | 2266 | 2272 | +6 |
| D2 Draufsicht | Loecher | 13 | 14 | +1 |

`python3 neu/delta.py` wurde VAR0 Neu-Mesh gegen p3d4 ausgefuehrt und brach wie vorgeschrieben ab: **16 Anstiege** (5 Regel/Kachel-, 11 Clay-Bildindikatoren). Regelanstiege: G3_spitze_unten_fein C1 +1, G6_facette G1 +1, G7b_wandkontur_feld D1 +1, R3_laengs_m D1 +4, R9w_wellen F1 +1. Die vollstaendige Delta-Ausgabe lag unter `/tmp/delta_p3d4.md`.

## Integritaet, Build und Tests

- `RELIEF_NEU=1 python3 gen_relief.py` und `RELIEF_NEU=1 python3 baue_html.py`: erfolgreich; LOD1 **168.600 Dreiecke** von 1.300.000.
- Lochscan auf dem finalen Viewer: 9 Meshes, 88.728 Terrain-Dreiecke, **0 offene Innenkanten, 0 Punkte**.
- D2: **0 geaenderte Vertices**, `d2_gb_mesh_bytegleich=true`, SHA-256 `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6`.
- Zellquellspalten: `zellen_quell_diff=0`; `pruefe_t42u.py`: **Summe 0**.
- `pytest -q neu/tests`: **26 bestanden, 5 fehlgeschlagen**. Offen bleiben die globalen R8a=0- und F1/C1-Wegende-Tests, D1-Saegezahn=0, die Negativreferenz Wandkantenschaerfe (2,24 statt ≥3,00) und Schatten-Hochfrequenz (0,307 statt ≤0,25). Keine Schwelle wurde angepasst. Der Delta-Schema-Test besteht nach dem JSON-Feld-Fix.
- `git diff --check`: sauber. Quell-/Overlay-/Referenzdateien sind nicht geaendert.

## Annahmen, Grenzen und offene Punkte

- Der vom Auftrag genannte direkte Ausgangswert `pruefe_regeln=596` war nicht reproduzierbar; die unveraenderte Quelle liefert 570. R8/R9 stimmen mit den vorgegebenen 48/334 ueberein.
- Die R8a-Korrektur bleibt bewusst auf D1/G1 begrenzt. Die 20 anderen globalen R8a-Treffer bleiben stehen.
- Das R3-laengs-Ziel in D1 (Delta ≤0 gegen p3d3 VAR0) ist mit +4 verfehlt. Die globale R9w-Zunahme liegt bei +5; der G1-Kachelvergleich gegen die direkte Quelle liegt bei +6. Der Neu-Mesh-Delta-Checker meldet weiterhin 16 Anstiege.
- Die D1-Wandfussnaht ist visuell noch sichtbar; der Facettenindikator ist gegen p3d3 um 4 gestiegen. Der Anschluss ist damit nicht vollstaendig behoben.
- D2-Daten, Zellquellen und t42u bleiben unveraendert. Die kleinen positiven D2-Screenshotindikatoren sind Rasterwerte; D2-Meshhash und wiederholter finaler Screenshot sind stabil.
- Es lag kein Laufzeit-Log vor, mit dem `gpt-6-luna` und `xhigh` unabhaengig belegt werden koennten. Die Codex-Konfiguration wurde nicht geaendert.

**Gesamtziel teilweise erreicht, nicht vollstaendig:** D1/G1-Wegende-R8a ist beseitigt, Kreuzung und der Endpunkt 156.5|37.5 liegen unter 0,20 m und D2/t42u bleiben exakt. R3-D1, Wandfuss-Clay und der strikte Neu-Mesh-Delta-Abbruch bleiben offen.
