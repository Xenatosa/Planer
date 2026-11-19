# Selbsttest QA detail_v2 (P6)

Lauf: 2026-11-19 15:08 CET · Dauer 66 s · Ergebnis: **BESTANDEN**

Dummy: 4 Kacheln D2/E2/D3/E3 im angenommenen Format (PLAN_QA_DV2.md Abschn. 2), gebaut von `selbsttest/baue_dummy.py` nach `/tmp/dv2_qa/dummy/`.

| Fall | Regel | Soll | Ist | ok | Detail |
|---|---|---|---|---|---|
| sauber | Q1 | ok | ok | ja | {"kanten": 251302, "kanten_mehr_als_2": 0, "randkanten_innen": 0, "naht_abweichend": 0, "strahlen": 30240, "strahl_loecher": 0, "orte_gescannt": ["dorfkern", "b |
| sauber | Q2 | ok | ok | ja | {"linien": 11, "hausdorff_max_m": 0.0, "schwelle_m": 0.02} |
| sauber | Q3 | ok | ok | ja | {"linien": 11, "abw_max_m": 0.0035, "knick_max_grad": 2.4, "schwellen": [0.03, 15], "grat_silhouette": "Sa per Bild (Q13)"} |
| sauber | Q4 | ok | ok | ja | {"kreuzungen": 1, "gefaelle_max": 0.0, "rest_max_m": 0.0, "schwellen": [0.02, 0.02]} |
| sauber | Q5 | ok | ok | ja | {"kandidaten": 4486, "tiefe_max_m": 0.0125, "schwelle_m": 0.03, "band_m": 3.0} |
| sauber | Q6 | ok | ok | ja | {"stationen": 169, "einsenkung_min_m": 0.0398, "einsenkung_max_m": 0.0401, "quer_max": 0.0125, "laengs_max_grad": 1.1458, "schwellen": [0.03, 0.05, 0.035, 20]} |
| sauber | Q7 | ok | ok | ja | {"alte_vertices": 7395, "nicht_abgedeckt": 0, "ueber_schwelle": 0, "dh_max_m": 0.008, "dh_p99_m": 0.008, "schwelle_m": 0.01, "umriss_ok": true, "regel_quelle":  |
| sauber | Q8 | ok | ok | ja | {"gewaesser": 1, "kontur_ufer_max_m": 0.0, "ufer_kontur_max_m": 0.0, "nicht_monoton": 0, "ueber_krone": 0, "profile": 1722, "schwelle_m": 0.05} |
| sauber | Q9 | ok | ok | ja | {"dreiecke_gesamt": 167238, "dreiecke_max_kachel": 50161, "normale_unten": 0, "entartet": 0, "kante_zu_lang": 0, "min_winkel_grad": 45.0, "winkel_unter_20": 0,  |
| sauber | Q10 | ok | ok | ja | {"gespiegelt_uv0": 0, "gespiegelt_uv1": 0, "uv1_abweichend": 0, "verzerrung_max_bis35": 0.0768, "verzerrung_ueber_10pct": 0, "max_neigung_grad": 22.6, "wand": " |
| sauber | Q11 | ok | ok | ja | {"punkte": 9937, "dh_max_m": 0.0101, "ueber_2cm": 0, "flaeche_gleich": 0.9996, "felder_vollstaendig": true, "tests_gruen": true} |
| sauber | Q12 | ok | ok | ja | {"E2": {"teile": {"bohle": 1, "traeger": 1, "pfosten": 1, "gelaender": 2, "auflager": 1}, "spalt_max_m": 0.0, "stufe_max_m": 0.0, "gelaender_hoehe_m": 1.0}} |
| sauber | Q13 | ok | ok | ja | {"soll": 25, "vorhanden": 25, "qualitaet": [90]} |
| sauber | Q14 | ok | ok | ja | {"wege_alt": 4, "wege_fehlend": 0, "wege_zusaetzlich": 0, "hausdorff_max_m": 0.0, "wasser_rel": -0.0, "bauzone_rel": 0.0, "referenz": "Dummy (baue_dummy.py)"} |
| Q1 | Q1 | fehler | fehler | ja | 3 m2 Dreiecke bei 205/110 entfernt + 1 Nahtvertex E2 um 1 mm angehoben -> {"art": "innenrand", "x": 205.2, "z": 110.6} |
| Q2 | Q2 | fehler | fehler | ja | Mesh-Vertices auf Wegrand z=73,6 (x 140-145) um 4 cm verschoben -> {"datei": "wege.geojson", "id": "W1_l", "hausdorff_m": 0.04, "x": 140.25, "z": 73.6} |
| Q3 | Q3 | fehler | fehler | ja | Wegrand W1 rechts x 150-153 Zickzack +-5 cm -> {"datei": "wege.geojson", "id": "W1_r", "abw_m": 0.05, "knick_grad": 53.1, "x": 150.2, "z": 75.65} |
| Q4 | Q4 | fehler | fehler | ja | Buckel 5 cm in Kreuzung K1 -> {"id": "K1", "gefaelle": 0.0001, "rest_m": 0.0467, "x": 200.0, "z": 74.6} |
| Q5 | Q5 | fehler | fehler | ja | Delle 6 cm, r 0,6 m, 2 m neben Wegrand W1 (150/77,6) -> {"x": 149.8, "z": 77.6, "tiefe_m": 0.0342} |
| Q6 | Q6 | fehler | fehler | ja | Weg W4 x 150-156 nicht eingesenkt -> {"id": "W4", "x": 150.0, "z": 100.0, "art": ["einsenkung"], "einsenkung_m": 0.0001, "quer": 0.0125, "laengs_grad": 2.0} |
| Q7 | Q7 | fehler | fehler | ja | D2-Flaeche x140-150 z50-60 um 1,5 cm angehoben (> 1 cm) -> {"x": 148.5, "z": 55.0, "dh_m": 0.015} |
| Q7_lage | Q7 | fehler | fehler | ja | D2-Lage/Form: Weg W1 im D2-Bereich um 0,6 m nach Norden verschoben -> {"x": 131.5, "z": 73.5, "dh_m": 0.0372} |
| Q8 | Q8 | fehler | fehler | ja | Wasserspiegel in wasser.geojson +10 cm (Schnittlinie wandert vom Uferspline weg) -> {"gewaesser": "BACH", "art": "kontur->ufer", "abstand_m": 0.3569, "x": 189.04, "z": 43.2} |
| Q9 | Q9 | fehler | fehler | ja | 5 Dreiecke in D3 mit umgedrehter Windung (Normale nach unten) -> {"art": "normale_unten", "x": 126.13, "z": 86.07} |
| Q10 | Q10 | fehler | fehler | ja | Kachel E3: UV0 gespiegelt (u = -x), UV1 um 0,001 versetzt -> {"art": "uv0_gespiegelt", "x": 168.13, "z": 86.07} |
| Q11 | Q11 | fehler | fehler | ja | hoehe.png 30x30 m +5 cm, flaeche.png 10x10 m auf Fels -> {"art": "hoehe", "x": 160.12, "z": 101.0, "query_m": 3.5299, "mesh_m": 3.4776, "dh_m": 0.0523} |
| Q12 | Q12 | fehler | fehler | ja | Bruecke E2 ohne Gelaender/Handlauf, Widerlager 5 cm ueber Gelaende -> {"bruecke": "E2", "fehlende_teile": ["gelaender"]} |
| Q13 | Q13 | fehler | fehler | ja | 2 der 25 Abnahmebilder fehlen -> {"datei": "dorfkern_clay_30m.jpg", "fehler": "fehlt"} |
| Q14 | Q14 | fehler | fehler | ja | Mittellinie W4 0,5 m versetzt, Bauzone +2 % Radius -> {"weg": "W4", "hausdorff_m": 0.5} |
| Q14_wasser | Q14 | fehler | fehler | ja | Wasserpolygon 0,3 m breiter (+7 % Flaeche) -> {"art": "wasserflaeche", "neu_m2": 387.0, "alt_m2": 361.2, "rel": 0.0714} |
| leer | Runner | exit 2 | exit 2 | ja | fehlende Eingaben -> offen |
| Q5 | Runner | exit 1 | exit 1 | ja | Fehler -> Exit 1 |
| einheit | Q3-Geometrie | ok | ok | ja | Kreis r=5 m glatt: abw 0.0087 m, knick 0.9 Grad |
| einheit | Q3-Geometrie | ok | ok | ja | Zickzack +-5 cm erkannt: abw 0.0666 m, knick 53.1 Grad |
| einheit | Q3-Geometrie | ok | ok | ja | 90-Grad-Ecke erkannt: knick 90.0 Grad |
