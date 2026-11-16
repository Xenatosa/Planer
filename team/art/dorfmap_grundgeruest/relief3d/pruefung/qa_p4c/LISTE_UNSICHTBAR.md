# QA P4c: unsichtbare Gate-Treffer (Stand 8cd6d37)

Geprüft im Viewer `alle_kacheln.html` mit Wegen und Wasser, ohne Schatten (`nosh=1`). Je Treffer ein Paarbild links Farbe, rechts Ton (clay), Kamera von Süden, 15 m/35° (G7b: 25 m/45°). Messwert aus `messung.py` (GB-Höhenfeld, Radius 3 m), Rohdaten in `messung_p4c.json`.

Von den 40 neuen L3-Treffern (`pruefung/l3_nahbilder/neue_treffer/`) sind **33 unsichtbar**. Die 7 sichtbaren (T11–T15 an der Naht C4/D4, T17 und T37 an der D1-Rampe) stehen in `LISTE_SICHTBAR.md`. Hinweis: `ERGEBNIS_L3.md` nennt alle 40 unsichtbar; mit Wegen und Wasser und am selben Punkt aus 15 m sehen wir das für diese 7 anders.

Hoher Messwert heißt hier nicht sichtbar: Die Treffer liegen meist in der Wandzone (Hang über 60°). Dort zählen senkrechte Streifen nicht.

| Nr | Kachel | x | z | Regel | Messwert | Nahbild | Urteil / Notiz |
|---|---|---|---|---|---|---|---|
| T01 | C4 | 121.8 | 144.2 | G2 | zacke 0.61 m, hang max 61.1° | [nah](bilder_8cd6d37/nah/T01_G2_C4.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. Gratkante C4 glatt |
| T02 | C3 | 101.0 | 100.2 | G5 | zacke 0.2 m, hang max 50.1° | [nah](bilder_8cd6d37/nah/T02_G5_C3.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. glatt in Farbe und Ton |
| T03 | G4 | 274.1 | 132.6 | G5 | zacke 1.01 m, hang max 72.7° | [nah](bilder_8cd6d37/nah/T03_G5_G4.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. Kissenblock G4 weich, kein Zickzack |
| T04 | G4 | 272.5 | 131.5 | G5 | zacke 1.24 m, hang max 76.3° | [nah](bilder_8cd6d37/nah/T04_G5_G4.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. Kissenblock G4 weich |
| T05 | G4 | 275.0 | 134.5 | G5 | zacke 0.35 m, hang max 64.3° | [nah](bilder_8cd6d37/nah/T05_G5_G4.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. glatt in Farbe und Ton |
| T06 | G4 | 275.5 | 135.0 | G5 | zacke 0.35 m, hang max 63.9° | [nah](bilder_8cd6d37/nah/T06_G5_G4.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. glatt in Farbe und Ton |
| T07 | G4 | 276.0 | 135.5 | G5 | zacke 0.35 m, hang max 63.8° | [nah](bilder_8cd6d37/nah/T07_G5_G4.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. glatt in Farbe und Ton |
| T08 | G4 | 276.5 | 136.0 | G5 | zacke 0.33 m, hang max 63.6° | [nah](bilder_8cd6d37/nah/T08_G5_G4.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. glatt in Farbe und Ton |
| T09 | G4 | 277.0 | 136.5 | G5 | zacke 0.32 m, hang max 65.1° | [nah](bilder_8cd6d37/nah/T09_G5_G4.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. glatt in Farbe und Ton |
| T10 | G4 | 280.6 | 138.5 | G5 | zacke 0.84 m, hang max 75.0° | [nah](bilder_8cd6d37/nah/T10_G5_G4.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. Blockfuß G4 weich |
| T16 | D1 | 145.6 | 19.2 | G6 | zacke 0.19 m, hang max 58.2° | [nah](bilder_8cd6d37/nah/T16_G6_D1.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. glatt in Farbe und Ton |
| T18 | C3 | 93.5 | 95.3 | G6 | zacke 0.17 m, hang max 53.2° | [nah](bilder_8cd6d37/nah/T18_G6_C3.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. glatt in Farbe und Ton |
| T19 | C3 | 95.8 | 104.0 | G6 | zacke 0.16 m, hang max 49.3° | [nah](bilder_8cd6d37/nah/T19_G6_C3.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. glatt in Farbe und Ton |
| T20 | G3 | 288.7 | 101.8 | G6 | zacke 0.49 m, hang max 60.2° | [nah](bilder_8cd6d37/nah/T20_G6_G3.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. glatt in Farbe und Ton |
| T21 | G3 | 289.7 | 103.4 | G6 | zacke 0.22 m, hang max 41.5° | [nah](bilder_8cd6d37/nah/T21_G6_G3.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. glatt in Farbe und Ton |
| T22 | C3 | 114.1 | 109.1 | G6 | zacke 0.56 m, hang max 75.9° | [nah](bilder_8cd6d37/nah/T22_G6_C3.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. Wandzone C3, nur senkrechte Streifen |
| T23 | C3 | 107.5 | 111.5 | G6 | zacke 0.25 m, hang max 66.0° | [nah](bilder_8cd6d37/nah/T23_G6_C3.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. glatt in Farbe und Ton |
| T24 | C3 | 114.9 | 114.1 | G6 | zacke 0.7 m, hang max 70.3° | [nah](bilder_8cd6d37/nah/T24_G6_C3.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. Wandzone C3 |
| T25 | C3 | 116.7 | 124.3 | G6 | zacke 0.52 m, hang max 69.6° | [nah](bilder_8cd6d37/nah/T25_G6_C3.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. Wandzone C3 |
| T26 | D4 | 133.3 | 137.4 | G6 | zacke 0.33 m, hang max 54.6° | [nah](bilder_8cd6d37/nah/T26_G6_D4.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. glatt in Farbe und Ton |
| T27 | G4 | 283.1 | 139.4 | G6 | zacke 0.79 m, hang max 69.2° | [nah](bilder_8cd6d37/nah/T27_G6_G4.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. Wandzone G4 |
| T28 | C4 | 119.3 | 148.5 | G6 | zacke 0.26 m, hang max 54.0° | [nah](bilder_8cd6d37/nah/T28_G6_C4.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. glatt in Farbe und Ton |
| T29 | C4 | 119.2 | 151.9 | G6 | zacke 0.14 m, hang max 52.4° | [nah](bilder_8cd6d37/nah/T29_G6_C4.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. glatt in Farbe und Ton |
| T30 | C4 | 121.0 | 156.7 | G6 | zacke 0.23 m, hang max 50.1° | [nah](bilder_8cd6d37/nah/T30_G6_C4.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. glatt in Farbe und Ton |
| T31 | C5 | 87.2 | 173.2 | G6 | zacke 0.15 m, hang max 60.1° | [nah](bilder_8cd6d37/nah/T31_G6_C5.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. glatt in Farbe und Ton |
| T32 | C6 | 99.5 | 218.7 | G6 | zacke 0.54 m, hang max 72.4° | [nah](bilder_8cd6d37/nah/T32_G6_C6.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. Wandfuß C6 rund |
| T33 | C6 | 95.5 | 220.0 | G6 | zacke 0.32 m, hang max 65.6° | [nah](bilder_8cd6d37/nah/T33_G6_C6.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. glatt in Farbe und Ton |
| T34 | C6 | 97.2 | 219.9 | G6 | zacke 0.16 m, hang max 46.3° | [nah](bilder_8cd6d37/nah/T34_G6_C6.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. glatt in Farbe und Ton |
| T35 | G6 | 287.2 | 221.2 | G6 | zacke 0.16 m, hang max 38.5° | [nah](bilder_8cd6d37/nah/T35_G6_G6.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. feine Randzacken gehören zu Stelle 23 (G6, in Arbeit), kein eigener Befund |
| T36 | G6 | 283.8 | 222.3 | G6 | zacke 0.2 m, hang max 52.1° | [nah](bilder_8cd6d37/nah/T36_G6_G6.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. wie T35, gehört zu Stelle 23 |
| T38 | D6 | 147.0 | 236.0 | G7b | zacke 0.91 m, hang max 76.6° | [nah](bilder_8cd6d37/nah/T38_G7b_D6.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. Wandfuß D6, Streifen in Wandzone, kein Zacken sichtbar |
| T39 | G3 | 273.0 | 107.0 | G7b | zacke 0.59 m, hang max 74.0° | [nah](bilder_8cd6d37/nah/T39_G7b_G3.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. Wandkante G3 glatt |
| T40 | G4 | 273.0 | 150.0 | G7b | zacke 0.01 m, hang max 1.2° | [nah](bilder_8cd6d37/nah/T40_G7b_G4.jpg) · [L3-Bild](../l3_nahbilder/neue_treffer/) | unsichtbar. Fläche eben (Hang 1°); nur treppige Wegränder im Ton, siehe Nebenbefund W4 |
| P2 | C5 | 107.8 | 183.8 | G2fein | zacke 0.25 m, hang max 60.8° | [nah](bilder_8cd6d37/nah/P2_G2fein_C5.jpg) · [näher](bilder_8cd6d37/nah/P2_G2fein_C5_nah.jpg) | unsichtbar. P2-Kandidat G2_spitze_oben_fein (Gate-Treffer 107,2|184,8: 0,59). Hang glatt, keine Spitze. |
| P2 | D3 | 147 | 107 | G7b | zacke 0.0 m, hang max 0.0° | [nah](bilder_8cd6d37/nah/P2_G7b_D3.jpg) · [näher](bilder_8cd6d37/nah/P2_G7b_D3_nah.jpg) | unsichtbar. P2-Kandidat G7b_wandkontur_feld (147|107: 0,256). Flache Wiese neben Weg, keine Wandkontur zu sehen. |
