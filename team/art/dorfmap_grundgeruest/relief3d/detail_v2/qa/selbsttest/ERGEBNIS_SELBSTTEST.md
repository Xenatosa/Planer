# Selbsttest QA detail_v2 (P6)

Lauf: 2026-11-19 18:56 CET · Dauer 111 s · Ergebnis: **BESTANDEN**

Dummy: 4 Kacheln D2/E2/D3/E3 im verbindlichen Format (PLAN_QA_DV2.md Abschn. 8 inkl. Runde 2: Bett Kl. 4 geschlossen, Spiegelmodell, wege/kreuzungen im #56-Schema), gebaut von `selbsttest/baue_dummy.py` nach `/tmp/dv2_qa/dummy/`.

| Fall | Regel | Soll | Ist | ok | Detail |
|---|---|---|---|---|---|
| sauber | Q1 | ok | ok | ja | {"kanten": 251302, "vertices_roh": 88254, "duplikate_verschweisst": 4185, "gemischte_dreiecke": 0, "manifest_fehler": 0, "kanten_mehr_als_2": 0, "randkanten_inn |
| sauber | Q2 | ok | ok | ja | {"linien": 11, "hausdorff_max_m": 0.0, "schwelle_m": 0.02} |
| sauber | Q3 | ok | ok | ja | {"linien": 10, "abw_max_m": 0.0, "knick_max_grad": 0.0001, "mesh_kantenzuege": 10, "mesh_abw_max_m": 0.0, "mesh_knick_max_grad": 0.0001, "p5_regel": "aus (Bruec |
| sauber | Q4 | ok | ok | ja | {"kreuzungen": 1, "je_art": {"weg_kreuzung": 1}, "gefaelle_max": 0.0, "rest_max_m": 0.0, "schwellen": [0.02, 0.02]} |
| sauber | Q5 | ok | ok | ja | {"kandidaten": 4446, "tiefe_max_m": 0.0125, "schwelle_m": 0.03, "band_m": 3.0} |
| sauber | Q6 | ok | ok | ja | {"stationen": 169, "einsenkung_min_m": 0.0398, "einsenkung_max_m": 0.0401, "quer_max": 0.0125, "laengs_max_grad": 1.1458, "schwellen": [0.03, 0.05, 0.035, 20]} |
| sauber | Q7 | ok | ok | ja | {"alte_vertices": 7395, "nicht_abgedeckt": 0, "ueber_schwelle": 0, "dh_max_m": 0.008, "dh_p99_m": 0.008, "schwelle_m": 0.01, "umriss_ok": true, "regel_quelle":  |
| sauber | Q8 | ok | ok | ja | {"uferlinien": 2, "spiegelmodelle": ["wasser_W01"], "spiegel_randpunkte": 3438, "spalt_punkte": 0, "spalt_max_m": -0.0135, "ueberlappung_max_m": 0.05, "ueberlap |
| sauber | Q9 | ok | ok | ja | {"dreiecke_gesamt": 168090, "dreiecke_max_kachel": 50159, "normale_unten": 0, "entartet": 0, "kante_zu_lang": 0, "min_winkel_grad": 45.0, "winkel_unter_20": 0,  |
| sauber | Q10 | ok | ok | ja | {"gespiegelt_uv0": 0, "davon_triplanar": 0, "gespiegelt_uv1": 0, "uv1_abweichend": 0, "nan_uv0": 0, "nan_uv1": 0, "nan_uv2": 0, "spruenge_uv0": 0, "triplanar_dr |
| sauber | Q11 | ok | ok | ja | {"punkte": 9937, "dh_max_m": 0.0152, "ueber_2cm": 0, "flaeche_gleich": 0.9996, "felder_vollstaendig": true, "tests_gruen": true, "test_dateien": 1, "quellen": { |
| sauber | Q12 | ok | ok | ja | {"E2": {"teile": {"bohle": 1, "traeger": 1, "pfosten": 1, "gelaender": 2, "auflager": 1}, "spalt_max_m": 0.0, "stufe_max_m": 0.0, "gelaender_hoehe_m": 1.0}} |
| sauber | Q13 | ok | ok | ja | {"soll": 25, "vorhanden": 25, "qualitaet": [90]} |
| sauber | Q14 | ok | ok | ja | {"wege_alt": 4, "wege_fehlend": 0, "wege_ausnahme": [], "wege_zusaetzlich": 0, "hausdorff_max_m": 0.0, "wasser_massgeblich": "spiegel_sichtbar_m2 (Spiegelmodell |
| sauber | Q8/Q14-Spiegel | ok | 3438 Randpkt., Spalt 0 | ja | Spiegelmodell 5 cm im Ufer, Schnitt an jeder Station; sichtbar 361.2 m2 vs. Bett Kl. 4 361.2 m2 |
| sauber | Q1-Duplikate | kein Loch | 4185 dupl., 0 Rand | ja | positionsgleiche Klassengrenz-Duplikate werden verschweisst, 0 Innenrandkanten, 0 Strahlloecher |
| Q1 | Q1 | fehler | fehler | ja | 3 m2 Dreiecke bei 205/110 entfernt + 1 Nahtvertex E2 um 1 mm angehoben -> {"art": "innenrand", "x": 168.0, "z": 49.8} |
| Q1_bett | Q1 | fehler | fehler | ja | Loch r 0,5 m im Bachbett (Klasse 4) unter dem Spiegelmodell - Spiegel ist nicht Teil von Q1 -> {"art": "innenrand", "x": 191.0, "z": 109.6} |
| Q1_luecke | Q1 | fehler | fehler | ja | echte Naht-Luecke: Weg-Duplikate am Klassenrand z=99 (x 150-153) um 1 cm verschoben -> {"art": "innenrand", "x": 149.8, "z": 99.0} |
| Q2 | Q2 | fehler | fehler | ja | Mesh-Vertices auf Wegrand z=73,6 (x 140-145) um 4 cm verschoben -> {"datei": "wege.geojson", "id": "W1", "hausdorff_m": 0.04, "x": 140.25, "z": 73.6} |
| Q3 | Q3 | fehler | fehler | ja | Wegrand W1 rechts x 150-153 Zickzack +-5 cm -> {"datei": "wege.geojson", "id": "W1", "quelle": "vektor", "abw_m": 0.0442, "knick_grad": 53.1, "x": 152.82, "z": 75.56} |
| Q4 | Q4 | fehler | fehler | ja | Buckel 5 cm in Kreuzung K1 -> {"id": "K001", "art": "weg_kreuzung", "gefaelle": 0.0001, "rest_m": 0.0467, "x": 200.0, "z": 74.6} |
| Q5 | Q5 | fehler | fehler | ja | Delle 6 cm, r 0,6 m, 2 m neben Wegrand W1 (150/77,6) -> {"x": 149.8, "z": 77.6, "tiefe_m": 0.0342} |
| Q6 | Q6 | fehler | fehler | ja | Weg W4 x 150-156 nicht eingesenkt -> {"id": "W4", "x": 150.0, "z": 100.0, "art": ["einsenkung"], "einsenkung_m": 0.0001, "quer": 0.0125, "laengs_grad": 2.0} |
| Q7 | Q7 | fehler | fehler | ja | D2-Flaeche x140-150 z50-60 um 1,5 cm angehoben (> 1 cm) -> {"x": 148.5, "z": 55.0, "dh_m": 0.015} |
| Q7_lage | Q7 | fehler | fehler | ja | D2-Lage/Form: Weg W1 im D2-Bereich um 0,6 m nach Norden verschoben -> {"x": 131.5, "z": 73.5, "dh_m": 0.0372} |
| Q8 | Q8 | fehler | fehler | ja | Spiegelmodell +10 cm (Schnittlinie wandert vom Uferspline weg) -> {"art": "spalt spiegel/ufer", "x": 189.35, "z": 110.5, "spiegel_ueber_gelaende_m": 0.0865} |
| Q8_spalt | Q8 | fehler | fehler | ja | Spalt Spiegel/Ufer: linke Spiegelkante 15 cm vor dem Ufer (Kante ueber dem Bett) -> {"art": "spalt spiegel/ufer", "x": 189.55, "z": 43.7, "spiegel_ueber_gelaende_m": 0.0367} |
| Q8_ueberlappung | Q8 | fehler | fehler | ja | Spiegelkanten 0,3 m ins Ufer gezogen (Ueberlappung > 10 cm, kein Spalt) -> {"art": "ueberlappung spiegel/ufer", "x": 193.9, "z": 127.9, "ueberlappung_m": 0.3} |
| Q8_ohne_schnitt | Q8 | fehler | fehler | ja | Spiegel 0,4 m tiefer = unter Bett und Uferkante, schneidet das Ufer nicht -> {"ufer": "W01_U0", "art": "spiegel unter uferkante ohne schnitt", "x": 189.4, "z": 43.5, "spiegel_m": 2.93, "gelaende_min_m": 3.0618} |
| Q9 | Q9 | fehler | fehler | ja | 5 Dreiecke in D3 mit umgedrehter Windung (Normale nach unten) -> {"art": "normale_unten", "x": 126.13, "z": 86.07} |
| Q10 | Q10 | fehler | fehler | ja | Kachel E3: UV0 gespiegelt (u = -x), UV1 um 0,001 versetzt -> {"art": "uv0_gespiegelt", "x": 168.13, "z": 86.07} |
| Q10_triplanar | Q10 | fehler | fehler | ja | Triplanar-Zone (Felskegel, Klasse 3, ~40 Grad): UV0 mit NaN und 5-cm-Spruengen an Duplikaten -> {"art": "uv_nan", "x": 140.27, "z": 110.33} |
| Q10_flip | Q10 | fehler | fehler | ja | Triplanar-Zone: UV0 gespiegelt (u = 2*143 - x) -> {"art": "uv0_gespiegelt", "x": 140.27, "z": 110.33} |
| Q10_uv2 | Q10 | fehler | fehler | ja | UV2 Weg W4 x 150-160: Bogenlaenge x 1,3 (30 % Verzerrung) -> {"art": "uv2_verzerrung", "x": 150.13, "z": 99.07, "grad_u": 31.297, "scherung_cos": 0.0002, "quer_rel": 1.0} |
| Q11 | Q11 | fehler | fehler | ja | flaeche.png 10x10 m auf Fels (echte Datenschicht query.mjs/manifest.mjs) -> {"art": "flaeche", "anteil_gleich": 0.98591} |
| Q12 | Q12 | fehler | fehler | ja | Bruecke E2 ohne Gelaender/Handlauf, Widerlager 5 cm ueber Gelaende -> {"bruecke": "E2", "fehlende_teile": ["gelaender"]} |
| Q13 | Q13 | fehler | fehler | ja | 2 der 25 Abnahmebilder fehlen -> {"datei": "dorfkern_clay_30m.jpg", "fehler": "fehlt"} |
| Q14 | Q14 | fehler | fehler | ja | Mittellinie W4 0,5 m versetzt, Bauzone +2 % Radius -> {"weg": "W4/0", "hausdorff_m": 0.5} |
| Q14_fehlt | Q14 | fehler | fehler | ja | Referenz-Teilstueck W8/0 fehlt in wege.geojson, nicht in q14_ausnahmen -> bleibt hart -> {"weg": "W8/0", "fehler": "Mittellinie fehlt in wege.geojson"} |
| Q14_zelle_fehlt | Q14 | fehler | fehler | ja | Bauzone Zellformat (#61): 1 Zelle aus der CSV fehlt in zonen.geojson -> {"art": "bauzone", "fehler": "1 Zellen aus der CSV fehlen in zonen.geojson", "zellen": [[206, 117]]} |
| Q3_bruecke_p5_laengs | Q3 | fehler | fehler | ja | P5-Regel an: Deckecken frei, aber Delle 4 cm auf der Laengsseite des Brueckenrechtecks bleibt hart -> {"datei": "zonen.geojson", "id": "flaechentyp_br01", "quelle": "vektor", "abw_m": 0.0494, "knick_grad": 13.4, "x": 113.98, "z": 63.12, "gruppe": "brue |
| Q3_wegende_weit | Q3 | fehler | fehler | ja | Delle ~4,1 cm an Grund-Zone, aber > 3 m vor jedem Wegende -> hart -> {"datei": "zonen.geojson", "id": "flaechentyp_gr01", "quelle": "vektor", "abw_m": 0.0422, "knick_grad": 12.9, "x": 124.88, "z": 100.0, "gruppe": "sons |
| Q3_wegende_gross | Q3 | fehler | fehler | ja | Delle ~6 cm (> 4,8 cm) 2 m vor Wegende W5 -> hart -> {"datei": "zonen.geojson", "id": "flaechentyp_gr01", "quelle": "vektor", "abw_m": 0.0728, "knick_grad": 21.7, "x": 115.2, "z": 99.98, "gruppe": "sonst |
| Q14_wasser | Q14 | fehler | fehler | ja | Spiegelmodell +5 cm und 0,5 m ins Ufer: sichtbare Spiegelflaeche ~+9 % -> {"art": "wasserflaeche", "spiegel_sichtbar_m2": 395.6, "referenz_m2": 361.199999999999, "rel": 0.0952, "klasse4_m2": 361.2} |
| Q10_kurve | Q10 | ok | ok | ja | enge S-Kurve W4 (r ~4 m) mit 15 % UV2-Stauchung: nur gekennzeichnet, nicht blockierend -> {"uv2_enge_kurve_dreiecke": 700, "uv2_enge_kurve_ueber_10pct_gekennzeichnet": 280, "uv2_enge_kurve_max_abw": 0.1499, "kurvenradius_min_m": 5.05, "uv2_ |
| Q14_ohne_zonen | Q14 | offen | offen | ja | zonen.geojson fehlt (P1c): Bauzone "Eingabe fehlt", nicht bestanden -> {"bauzone_format": null, "bauzone_zellen": null, "wege_ausnahme": [], "bauzone": "Eingabe fehlt: zonen.geojson (P1c)"} |
| Q14_zellen | Q14 | ok | ok | ja | Bauzone Zellformat (#61, 2 Komponenten + Slot-Punkt): Zellsumme = Soll, Zellmenge deckungsgleich mit CSV -> {"bauzone_format": "zellen", "bauzone_zellen": {"komponenten": 2, "zellen_summe": 112, "zellen_eindeutig": 112, "zellen_doppelt": 0, "zellen_soll": 11 |
| Q3_logik | Q3 | ok | ok | ja | zackige Slot- und Bauzonen-Polygone + Zellpunkte in zonen.geojson, Q3-Quelle ohne Layer-Filter: Logikschichten ausgeschlossen -> {"p5_regel": "aus (Bruecken-Befunde offen bis P5)", "bruecke_offen_p5": {"abschnitte": 0, "ringe": {}}, "wegenden_ausnahme": {"id": "A-DV2-01", "absch |
| Q3_bruecke | Q3 | offen | offen | ja | F14: Brueckenrechteck (Platzhalter) - Ecken 90 Grad = offener Befund P5 (nicht ok, nicht Ausnahme) -> {"p5_regel": "aus (Bruecken-Befunde offen bis P5)", "bruecke_offen_p5": {"abschnitte": 4, "ringe": {"flaechentyp_br01": {"abw_max_cm": 18.5, "knick_ma |
| Q3_bruecke_p5 | Q3 | ok | ok | ja | F14 P5-Regel an (konfig q3_bruecke_p5.aktiv): 4 Deckecken je +-0,5 m frei, Laengsseiten glatt -> ok -> {"p5_regel": "aktiv", "p5_deckecken": [[110.0, 60.0], [110.0, 63.0], [118.0, 63.0], [118.0, 60.0]], "bruecke_offen_p5": {"abschnitte": 0, "ringe": {}} |
| Q3_wegende | Q3 | ok | ok | ja | F15: Delle ~4,1 cm (Knick 13 Grad) an Grund-Zone 2 m vor Wegende W5 -> Ausnahme A-DV2-01 -> {"p5_regel": "aus (Bruecken-Befunde offen bis P5)", "bruecke_offen_p5": {"abschnitte": 0, "ringe": {}}, "wegenden_ausnahme": {"id": "A-DV2-01", "absch |
| Q14_ausnahme | Q14 | ok | ok | ja | W9/0 fehlt, steht aber in q14_ausnahmen (wie A-DV2-02): Ausnahme statt Fehler -> {"bauzone_format": "flaeche", "bauzone_zellen": null, "wege_ausnahme": ["W9/0 (A-TEST)"], "bauzone": "vorhanden"} |
| leer | Runner | exit 2 | exit 2 | ja | fehlende Eingaben -> offen |
| Q5 | Runner | exit 1 | exit 1 | ja | Fehler -> Exit 1 |
| repo | Q14-Referenz | ~6630,17 | 6630.17 | ja | Referenz zur Laufzeit aus wasser.geojson (konfig q14_wasser_referenz, Runde 3), Stand art/dorfmap-fertig aa78160 |
| einheit | Q3-Geometrie | ok | ok | ja | (a) Kreis r 2,0 m: 0,25 vs. 0,05 m: neu abw 2.53 / 2.29 cm (Diff 2.4 mm, Sehnenpfeil 0,25-m-Polygon 3.9 mm), Knick 7.2/4.3 Grad; alt abw 1.05 / 1.87 cm (Diff 8.2 mm) |
| einheit | Q3-Geometrie | ok | ok | ja | (b) DP-Stuetzpunkte = dicht: 72 DP-Punkte (Abstand 0.14-1.14 m) vs. 2001 dicht: neu 1.85 / 1.82 cm (Diff 0.2 mm); alt 1.88 / 1.64 cm |
| einheit | Q3-Geometrie | ok | ok | ja | (c) Delle 5 cm gefunden (dicht + DP): abw dicht 4.01 cm, DP (5 Punkte) 4.01 cm |
| einheit | Q3-Geometrie | ok | ok | ja | (c) Zickzack +-5 cm gefunden: abw 4.54 cm, Knick 53.1 Grad |
| einheit | Q3-Geometrie | ok | ok | ja | (c) 90-Grad-Ecke gefunden: Knick 90.0 Grad, abw 18.5 cm |
| einheit | Q3-Geometrie | ok | ok | ja | F11 Kartenrand-Abschnitt + Kartenecke ausgenommen: Ring B, Ecke (20/10): roh abw 18.5 cm / Knick 90 Grad, ausgenommen 11/11 Punkte (Gruppe kartenrand) |
| einheit | Q3-Geometrie | ok | ok | ja | F11 Stosspunkt-Fenster +-0,5 m ausgenommen: Stosspunkt [(10.0, 5.0, ['A', 'B', 'C'])] (dazu 3 am Kartenrand, F13); Ring B roh Knick 90 Grad an (10/5), im Fenster ausgenommen, kein Rest-Befund im Fenster |
| einheit | Q3-Geometrie | ok | ok | ja | F11 Knick knapp ausserhalb des Fensters gefunden: Buckel 5 cm bei 0,65 m Bogenlaenge vom Stosspunkt: abw 4.3 cm, Knick 53 Grad, Gruppe ['stoss_nah'] |
| einheit | Q3-Geometrie | ok | ok | ja | F11 Brueckenecke bleibt hart: C typ bruecke: Stosspunkt (10/5) ausgenommen=False, Ring B Knick 90 Grad gefunden, Gruppe ['bruecke'] |
| einheit | Q3-Geometrie | ok | ok | ja | F13 Kartenrand-Stoss (2 Zonen + Rand) im Fenster ausgenommen: ohne Rand 0 Stosspunkte, mit Rand 2: [(10.0, 0.0, ['A', 'B', 'ausserhalb']), (10.0, 10.0, ['A', 'B', 'ausserhalb'])]; Ring B roh abw 18.5 cm an (10/10) ausgenommen, Ring B ohne Rest-Befund |
| einheit | Q3-Geometrie | ok | ok | ja | F13 Kartenrand-Stoss mit Bruecke bleibt hart: B typ bruecke: 2 Stosspunkte hart, Ring B an (10/10) gefunden (abw 15.1 cm) |
