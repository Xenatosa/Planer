# Gegenprobe Runde 5: Q3-Zonenringe und Q14-Bauzone auf zonen.geojson von art/dv2-zonen2 @ 5dabe976 (#61)

Stand 19.11.2026, QA 748bafe + Runde 5 (F11 + F13, Logikschichten bauzone_plan/slot aus Q3, Q14-Bauzone im Zellformat). Aufruf: `pruefe_alle.py --wurzel /tmp/dv2_qa/alt_dv2_z5 --nur Q3,Q14` mit `vektor/zonen.geojson` aus 5dabe976 (sonst Vektoren aa78160, altes Mesh im dv2-Format).

**Stoßpunkte:** 117 (flaechentyp 61, untergrund 56); mit Fenster 105, hart (Brücke) 12; davon am Kartenrand (F13: 2 Zonen + außerhalb) 48.

**Rest-Ringe** (Gruppe = Ort des größten Ausschlags): {"bruecke": 13, "sonst": 3, "stoss_nah": 1} = 17 Ringe (alle `flaechentyp`, `untergrund` 0). Abschnitte über Schwelle (zusammenhängende Abtastpunkte): {"bruecke": 40, "sonst": 98, "stoss_nah": 13}.

Alle 98 `sonst`-Abschnitte liegen ≤ 3 m an einem Mittellinien-Ende (Median 1,3 m), also an runden Wegenden (vgl. A-DV2-01), 3,0–4,8 cm, Knick ≤ 11°. Die `bruecke`-Abschnitte sind die Brückenrechteck-Ecken (hart, Platzhalter P5).

## Abschnitte über Schwelle

| Ring | Typ | Gruppe | Abw. cm | Knick ° | x | z | nächstes Wegende m |
|---|---|---|---|---|---|---|---|
| flaechentyp_00007 | bruecke | bruecke | 18.8 | 104 | 187.04 | 76.21 | 2.2 |
| flaechentyp_00007 | bruecke | bruecke | 15.2 | 64 | 187.09 | 76.22 | 2.1 |
| flaechentyp_00007 | bruecke | bruecke | 17.3 | 83 | 187.82 | 73.29 | 1.9 |
| flaechentyp_00007 | bruecke | bruecke | 9.5 | 40 | 189.67 | 76.12 | 1.5 |
| flaechentyp_00007 | bruecke | bruecke | 9.5 | 43 | 190.13 | 74.29 | 1.5 |
| flaechentyp_00008 | bruecke | bruecke | 20.8 | 120 | 181.62 | 129.5 | 2.6 |
| flaechentyp_00008 | bruecke | bruecke | 17.2 | 84 | 184.28 | 129.91 | 2.6 |
| flaechentyp_00008 | bruecke | bruecke | 17.9 | 89 | 185.74 | 122.99 | 1.5 |
| flaechentyp_00008 | bruecke | bruecke | 21.1 | 116 | 188.06 | 123.98 | 3.0 |
| flaechentyp_00009 | bruecke | bruecke | 21.4 | 112 | 175.44 | 129.68 | 0.8 |
| flaechentyp_00009 | bruecke | bruecke | 16.9 | 85 | 176.79 | 126.13 | 2.7 |
| flaechentyp_00009 | bruecke | bruecke | 5.3 | 29 | 177.59 | 129.68 | 2.1 |
| flaechentyp_00009 | bruecke | bruecke | 11.1 | 57 | 178.19 | 129.45 | 1.6 |
| flaechentyp_00009 | bruecke | bruecke | 20.1 | 103 | 179.31 | 126.51 | 1.5 |
| flaechentyp_00010 | weg | bruecke | 18.1 | 94 | 176.79 | 126.13 | 2.7 |
| flaechentyp_00010 | weg | bruecke | 16.0 | 77 | 187.01 | 76.21 | 2.2 |
| flaechentyp_00010 | weg | bruecke | 6.5 | 1 | 187.61 | 73.26 | 2.1 |
| flaechentyp_00010 | weg | bruecke | 18.6 | 97 | 187.81 | 73.29 | 1.9 |
| flaechentyp_00012 | weg | bruecke | 19.7 | 102 | 184.29 | 129.91 | 2.6 |
| flaechentyp_00012 | weg | bruecke | 12.7 | 62 | 188.07 | 123.98 | 3.0 |
| flaechentyp_00015 | ufer | bruecke | 17.4 | 92 | 185.75 | 122.97 | 1.5 |
| flaechentyp_00015 | ufer | bruecke | 4.2 | 5 | 185.94 | 123.1 | 1.5 |
| flaechentyp_00015 | ufer | bruecke | 18.0 | 97 | 187.85 | 73.29 | 1.9 |
| flaechentyp_00015 | ufer | bruecke | 14.2 | 67 | 188.06 | 123.98 | 3.0 |
| flaechentyp_00015 | ufer | bruecke | 3.1 | 6 | 189.79 | 73.84 | 1.5 |
| flaechentyp_00015 | ufer | bruecke | 23.9 | 140 | 190.14 | 74.32 | 1.5 |
| flaechentyp_00016 | ufer | bruecke | 13.9 | 69 | 175.45 | 129.68 | 0.8 |
| flaechentyp_00016 | ufer | bruecke | 5.5 | 29 | 177.6 | 129.68 | 2.1 |
| flaechentyp_00016 | ufer | bruecke | 23.4 | 125 | 178.2 | 129.45 | 1.6 |
| flaechentyp_00017 | ufer | bruecke | 18.2 | 98 | 176.82 | 126.14 | 2.7 |
| flaechentyp_00017 | ufer | bruecke | 15.3 | 77 | 179.29 | 126.51 | 1.5 |
| flaechentyp_00017 | ufer | bruecke | 15.7 | 77 | 187.01 | 76.22 | 2.2 |
| flaechentyp_00017 | ufer | bruecke | 24.2 | 141 | 189.68 | 76.11 | 1.5 |
| flaechentyp_00018 | ufer | bruecke | 12.5 | 61 | 181.62 | 129.5 | 2.6 |
| flaechentyp_00018 | ufer | bruecke | 19.1 | 96 | 184.28 | 129.91 | 2.6 |
| flaechentyp_00052 | grund | bruecke | 16.3 | 84 | 187.81 | 73.29 | 1.9 |
| flaechentyp_00054 | grund | bruecke | 18.0 | 88 | 176.8 | 126.12 | 2.7 |
| flaechentyp_00054 | grund | bruecke | 18.7 | 103 | 186.99 | 76.2 | 2.2 |
| flaechentyp_00055 | grund | bruecke | 22.5 | 118 | 188.07 | 123.98 | 3.0 |
| flaechentyp_00056 | grund | bruecke | 15.3 | 79 | 184.27 | 129.93 | 2.6 |
| flaechentyp_00010 | weg | sonst | 3.1 | 7 | 140.05 | 74.54 | 1.5 |
| flaechentyp_00010 | weg | sonst | 4.8 | 10 | 148.32 | 53.94 | 1.0 |
| flaechentyp_00010 | weg | sonst | 4.8 | 10 | 158.25 | 115.25 | 1.0 |
| flaechentyp_00010 | weg | sonst | 4.8 | 10 | 159.22 | 140.65 | 1.0 |
| flaechentyp_00010 | weg | sonst | 4.8 | 10 | 167.75 | 55.21 | 1.0 |
| flaechentyp_00010 | weg | sonst | 4.8 | 10 | 168.49 | 110.42 | 1.0 |
| flaechentyp_00010 | weg | sonst | 3.1 | 6 | 174.13 | 30.36 | 1.5 |
| flaechentyp_00010 | weg | sonst | 3.1 | 7 | 182.4 | 106.08 | 1.5 |
| flaechentyp_00010 | weg | sonst | 3.2 | 7 | 187.2 | 41.54 | 1.5 |
| flaechentyp_00011 | weg | sonst | 3.1 | 7 | 194.94 | 78.41 | 1.5 |
| flaechentyp_00011 | weg | sonst | 4.8 | 10 | 241.28 | 41.14 | 1.0 |
| flaechentyp_00011 | weg | sonst | 3.2 | 7 | 249.5 | 36.85 | 1.5 |
| flaechentyp_00011 | weg | sonst | 3.1 | 7 | 249.6 | 82.99 | 1.5 |
| flaechentyp_00011 | weg | sonst | 3.1 | 7 | 264.72 | 31.74 | 1.5 |
| flaechentyp_00011 | weg | sonst | 4.1 | 9 | 273.35 | 35.5 | 1.0 |
| flaechentyp_00011 | weg | sonst | 4.4 | 10 | 276.57 | 91.25 | 1.0 |
| flaechentyp_00011 | weg | sonst | 4.1 | 10 | 279.31 | 40.07 | 1.0 |
| flaechentyp_00011 | weg | sonst | 3.1 | 7 | 279.72 | 31.32 | 1.5 |
| flaechentyp_00011 | weg | sonst | 3.1 | 8 | 285.34 | 54.26 | 1.5 |
| flaechentyp_00011 | weg | sonst | 4.4 | 10 | 286.63 | 45.51 | 1.0 |
| flaechentyp_00011 | weg | sonst | 4.8 | 10 | 289.57 | 89.88 | 1.0 |
| flaechentyp_00011 | weg | sonst | 3.5 | 7 | 293.81 | 51.25 | 1.3 |
| flaechentyp_00011 | weg | sonst | 3.1 | 7 | 298.05 | 79.2 | 1.5 |
| flaechentyp_00011 | weg | sonst | 3.5 | 8 | 321.0 | 36.85 | 1.3 |
| flaechentyp_00011 | weg | sonst | 3.1 | 7 | 330.35 | 67.3 | 1.5 |
| flaechentyp_00012 | weg | sonst | 3.1 | 7 | 180.72 | 148.96 | 1.5 |
| flaechentyp_00012 | weg | sonst | 4.8 | 10 | 190.27 | 182.15 | 1.0 |
| flaechentyp_00012 | weg | sonst | 4.7 | 9 | 192.22 | 111.35 | 1.0 |
| flaechentyp_00012 | weg | sonst | 4.8 | 10 | 201.45 | 186.61 | 1.0 |
| flaechentyp_00012 | weg | sonst | 3.0 | 6 | 204.97 | 139.8 | 1.5 |
| flaechentyp_00012 | weg | sonst | 4.7 | 10 | 207.65 | 108.48 | 1.0 |
| flaechentyp_00012 | weg | sonst | 4.7 | 9 | 208.42 | 191.37 | 1.0 |
| flaechentyp_00012 | weg | sonst | 3.5 | 8 | 213.94 | 120.07 | 1.3 |
| flaechentyp_00012 | weg | sonst | 3.8 | 8 | 221.74 | 203.09 | 1.2 |
| flaechentyp_00012 | weg | sonst | 3.5 | 8 | 223.82 | 121.35 | 1.3 |
| flaechentyp_00012 | weg | sonst | 3.1 | 7 | 234.01 | 186.71 | 1.5 |
| flaechentyp_00012 | weg | sonst | 3.1 | 7 | 239.06 | 125.99 | 1.5 |
| flaechentyp_00012 | weg | sonst | 3.1 | 7 | 248.2 | 141.13 | 1.5 |
| flaechentyp_00012 | weg | sonst | 3.1 | 7 | 249.16 | 144.87 | 1.5 |
| flaechentyp_00012 | weg | sonst | 3.1 | 7 | 253.77 | 160.64 | 1.5 |
| flaechentyp_00012 | weg | sonst | 3.2 | 7 | 258.15 | 131.15 | 1.5 |
| flaechentyp_00012 | weg | sonst | 3.1 | 7 | 262.1 | 172.37 | 1.5 |
| flaechentyp_00012 | weg | sonst | 3.6 | 8 | 267.32 | 172.12 | 1.3 |
| flaechentyp_00012 | weg | sonst | 3.1 | 7 | 278.91 | 141.14 | 1.5 |
| flaechentyp_00012 | weg | sonst | 3.5 | 8 | 284.83 | 161.88 | 1.3 |
| flaechentyp_00012 | weg | sonst | 3.5 | 7 | 295.93 | 167.44 | 1.3 |
| flaechentyp_00012 | weg | sonst | 3.5 | 7 | 298.01 | 171.76 | 1.3 |
| flaechentyp_00012 | weg | sonst | 3.8 | 8 | 302.58 | 182.17 | 1.2 |
| flaechentyp_00012 | weg | sonst | 3.2 | 7 | 304.16 | 187.54 | 1.5 |
| flaechentyp_00015 | ufer | sonst | 4.7 | 8 | 192.22 | 111.35 | 1.0 |
| flaechentyp_00018 | ufer | sonst | 4.7 | 9 | 208.42 | 191.37 | 1.0 |
| flaechentyp_00037 | fels | sonst | 3.5 | 8 | 295.92 | 167.43 | 1.3 |
| flaechentyp_00052 | grund | sonst | 3.1 | 7 | 140.0 | 76.39 | 1.5 |
| flaechentyp_00052 | grund | sonst | 4.8 | 10 | 148.22 | 53.61 | 1.0 |
| flaechentyp_00052 | grund | sonst | 4.8 | 10 | 158.25 | 115.25 | 1.0 |
| flaechentyp_00052 | grund | sonst | 4.8 | 10 | 159.22 | 140.65 | 1.0 |
| flaechentyp_00052 | grund | sonst | 4.8 | 10 | 167.74 | 55.21 | 1.0 |
| flaechentyp_00052 | grund | sonst | 3.1 | 7 | 174.13 | 30.36 | 1.5 |
| flaechentyp_00052 | grund | sonst | 3.2 | 7 | 187.2 | 41.54 | 1.5 |
| flaechentyp_00052 | grund | sonst | 3.2 | 7 | 194.91 | 78.4 | 1.5 |
| flaechentyp_00052 | grund | sonst | 3.0 | 6 | 204.99 | 139.79 | 1.5 |
| flaechentyp_00052 | grund | sonst | 4.8 | 10 | 207.63 | 109.42 | 1.0 |
| flaechentyp_00052 | grund | sonst | 3.5 | 8 | 214.0 | 121.07 | 1.3 |
| flaechentyp_00052 | grund | sonst | 3.8 | 8 | 221.73 | 203.09 | 1.2 |
| flaechentyp_00052 | grund | sonst | 3.6 | 8 | 223.95 | 121.17 | 1.3 |
| flaechentyp_00052 | grund | sonst | 3.2 | 7 | 239.08 | 125.97 | 1.5 |
| flaechentyp_00052 | grund | sonst | 4.8 | 10 | 241.28 | 41.14 | 1.0 |
| flaechentyp_00052 | grund | sonst | 3.1 | 7 | 248.2 | 141.1 | 1.5 |
| flaechentyp_00052 | grund | sonst | 3.1 | 7 | 249.26 | 145.87 | 1.5 |
| flaechentyp_00052 | grund | sonst | 3.1 | 7 | 249.49 | 36.85 | 1.5 |
| flaechentyp_00052 | grund | sonst | 3.1 | 7 | 250.98 | 83.22 | 1.5 |
| flaechentyp_00052 | grund | sonst | 3.1 | 7 | 258.16 | 131.13 | 1.5 |
| flaechentyp_00052 | grund | sonst | 3.1 | 7 | 265.31 | 32.7 | 1.5 |
| flaechentyp_00052 | grund | sonst | 4.1 | 9 | 273.36 | 35.5 | 1.0 |
| flaechentyp_00052 | grund | sonst | 4.5 | 10 | 276.54 | 91.22 | 1.0 |
| flaechentyp_00052 | grund | sonst | 3.1 | 7 | 277.97 | 140.58 | 1.5 |
| flaechentyp_00052 | grund | sonst | 4.1 | 10 | 279.31 | 40.07 | 1.0 |
| flaechentyp_00052 | grund | sonst | 3.1 | 7 | 279.71 | 31.32 | 1.5 |
| flaechentyp_00052 | grund | sonst | 3.5 | 8 | 284.53 | 161.99 | 1.3 |
| flaechentyp_00052 | grund | sonst | 3.1 | 7 | 286.27 | 53.71 | 1.5 |
| flaechentyp_00052 | grund | sonst | 4.4 | 10 | 286.63 | 45.51 | 1.0 |
| flaechentyp_00052 | grund | sonst | 4.8 | 11 | 289.56 | 89.88 | 1.0 |
| flaechentyp_00052 | grund | sonst | 3.5 | 8 | 293.87 | 51.32 | 1.3 |
| flaechentyp_00052 | grund | sonst | 3.5 | 7 | 298.01 | 171.77 | 1.3 |
| flaechentyp_00052 | grund | sonst | 3.2 | 7 | 298.06 | 79.19 | 1.5 |
| flaechentyp_00052 | grund | sonst | 3.8 | 8 | 302.55 | 182.14 | 1.2 |
| flaechentyp_00052 | grund | sonst | 3.2 | 7 | 304.16 | 187.55 | 1.5 |
| flaechentyp_00052 | grund | sonst | 3.6 | 8 | 321.0 | 36.85 | 1.3 |
| flaechentyp_00052 | grund | sonst | 3.2 | 7 | 330.36 | 67.3 | 1.5 |
| flaechentyp_00054 | grund | sonst | 4.8 | 10 | 168.57 | 110.5 | 1.0 |
| flaechentyp_00054 | grund | sonst | 3.2 | 7 | 182.41 | 106.05 | 1.5 |
| flaechentyp_00056 | grund | sonst | 3.1 | 7 | 181.05 | 148.01 | 1.5 |
| flaechentyp_00056 | grund | sonst | 4.8 | 10 | 190.23 | 181.92 | 1.0 |
| flaechentyp_00056 | grund | sonst | 4.8 | 10 | 201.14 | 186.84 | 1.0 |
| flaechentyp_00056 | grund | sonst | 3.1 | 7 | 234.01 | 186.71 | 1.5 |
| flaechentyp_00056 | grund | sonst | 3.1 | 7 | 262.02 | 172.24 | 1.5 |
| flaechentyp_00056 | grund | sonst | 3.5 | 7 | 267.92 | 172.06 | 1.3 |
| flaechentyp_00058 | grund | sonst | 3.1 | 7 | 253.8 | 160.63 | 1.5 |
| flaechentyp_00011 | weg | stoss_nah | 3.1 | 6 | 193.89 | 77.5 | 1.5 |
| flaechentyp_00012 | weg | stoss_nah | 4.7 | 10 | 192.24 | 111.26 | 1.0 |
| flaechentyp_00012 | weg | stoss_nah | 4.8 | 10 | 208.34 | 191.5 | 1.0 |
| flaechentyp_00012 | weg | stoss_nah | 3.0 | 6 | 218.32 | 201.32 | 1.5 |
| flaechentyp_00012 | weg | stoss_nah | 3.5 | 8 | 221.38 | 202.75 | 1.2 |
| flaechentyp_00012 | weg | stoss_nah | 3.5 | 7 | 295.81 | 167.28 | 1.3 |
| flaechentyp_00012 | weg | stoss_nah | 3.5 | 8 | 296.09 | 167.86 | 1.3 |
| flaechentyp_00015 | ufer | stoss_nah | 4.7 | 10 | 192.24 | 111.25 | 1.0 |
| flaechentyp_00018 | ufer | stoss_nah | 4.8 | 10 | 208.34 | 191.5 | 1.0 |
| flaechentyp_00037 | fels | stoss_nah | 3.5 | 8 | 295.54 | 167.03 | 1.3 |
| flaechentyp_00037 | fels | stoss_nah | 3.5 | 8 | 295.97 | 167.52 | 1.3 |
| flaechentyp_00052 | grund | stoss_nah | 3.1 | 6 | 193.89 | 77.51 | 1.5 |
| flaechentyp_00052 | grund | stoss_nah | 3.6 | 7 | 221.41 | 202.78 | 1.2 |

## Stoßpunktliste (Sichtprüfung 1,7 m in P6 Pflicht)

| Layer | x | z | Zonen | Typen | Kartenrand | Fenster |
|---|---|---|---|---|---|---|
| flaechentyp | 0.0 | 26.006 | flaechentyp_00026, flaechentyp_00053, ausserhalb | fels, grund | ja | ±0,5 m |
| flaechentyp | 0.0 | 33.973 | flaechentyp_00026, flaechentyp_00053, ausserhalb | fels, grund | ja | ±0,5 m |
| flaechentyp | 0.0 | 44.487 | flaechentyp_00026, flaechentyp_00052, ausserhalb | fels, grund | ja | ±0,5 m |
| flaechentyp | 0.0 | 238.156 | flaechentyp_00016, flaechentyp_00052, ausserhalb | grund, ufer | ja | ±0,5 m |
| flaechentyp | 0.0 | 240.654 | flaechentyp_00003, flaechentyp_00016, ausserhalb | ufer, wasser | ja | ±0,5 m |
| flaechentyp | 0.0 | 253.354 | flaechentyp_00003, flaechentyp_00022, ausserhalb | ufer, wasser | ja | ±0,5 m |
| flaechentyp | 0.0 | 255.853 | flaechentyp_00022, flaechentyp_00061, ausserhalb | grund, ufer | ja | ±0,5 m |
| flaechentyp | 0.0 | 270.626 | flaechentyp_00022, flaechentyp_00061, ausserhalb | grund, ufer | ja | ±0,5 m |
| flaechentyp | 0.0 | 273.123 | flaechentyp_00003, flaechentyp_00022, ausserhalb | ufer, wasser | ja | ±0,5 m |
| flaechentyp | 0.0 | 278.381 | flaechentyp_00003, flaechentyp_00024, ausserhalb | ufer, wasser | ja | ±0,5 m |
| flaechentyp | 0.0 | 280.88 | flaechentyp_00024, flaechentyp_00062, ausserhalb | grund, ufer | ja | ±0,5 m |
| flaechentyp | 21.395 | 0.0 | flaechentyp_00026, flaechentyp_00045, ausserhalb | fels, grund | ja | ±0,5 m |
| flaechentyp | 31.28 | 199.586 | flaechentyp_00016, flaechentyp_00040, flaechentyp_00052 | fels, grund, ufer |  | ±0,5 m |
| flaechentyp | 31.3 | 194.958 | flaechentyp_00016, flaechentyp_00040, flaechentyp_00052 | fels, grund, ufer |  | ±0,5 m |
| flaechentyp | 173.585 | 137.342 | flaechentyp_00010, flaechentyp_00016, flaechentyp_00052 | grund, ufer, weg |  | ±0,5 m |
| flaechentyp | 175.432 | 129.682 | flaechentyp_00009, flaechentyp_00010, flaechentyp_00016 | bruecke, ufer, weg |  | **hart** |
| flaechentyp | 176.793 | 126.132 | flaechentyp_00009, flaechentyp_00010, flaechentyp_00017, flaechentyp_00054 | bruecke, grund, ufer, weg |  | **hart** |
| flaechentyp | 178.202 | 129.451 | flaechentyp_00003, flaechentyp_00009, flaechentyp_00016 | bruecke, ufer, wasser |  | **hart** |
| flaechentyp | 179.315 | 126.507 | flaechentyp_00003, flaechentyp_00009, flaechentyp_00017 | bruecke, ufer, wasser |  | **hart** |
| flaechentyp | 181.598 | 129.5 | flaechentyp_00003, flaechentyp_00008, flaechentyp_00018 | bruecke, ufer, wasser |  | **hart** |
| flaechentyp | 184.281 | 129.909 | flaechentyp_00008, flaechentyp_00012, flaechentyp_00018, flaechentyp_00056 | bruecke, grund, ufer, weg |  | **hart** |
| flaechentyp | 185.746 | 122.979 | flaechentyp_00003, flaechentyp_00008, flaechentyp_00015 | bruecke, ufer, wasser |  | **hart** |
| flaechentyp | 187.018 | 76.207 | flaechentyp_00007, flaechentyp_00010, flaechentyp_00017, flaechentyp_00054 | bruecke, grund, ufer, weg |  | **hart** |
| flaechentyp | 187.824 | 73.289 | flaechentyp_00007, flaechentyp_00010, flaechentyp_00015, flaechentyp_00052 | bruecke, grund, ufer, weg |  | **hart** |
| flaechentyp | 188.072 | 123.98 | flaechentyp_00008, flaechentyp_00012, flaechentyp_00015, flaechentyp_00055 | bruecke, grund, ufer, weg |  | **hart** |
| flaechentyp | 189.682 | 76.112 | flaechentyp_00003, flaechentyp_00007, flaechentyp_00017 | bruecke, ufer, wasser |  | **hart** |
| flaechentyp | 190.141 | 74.317 | flaechentyp_00003, flaechentyp_00007, flaechentyp_00015 | bruecke, ufer, wasser |  | **hart** |
| flaechentyp | 192.368 | 112.336 | flaechentyp_00012, flaechentyp_00015, flaechentyp_00055 | grund, ufer, weg |  | ±0,5 m |
| flaechentyp | 192.815 | 110.545 | flaechentyp_00012, flaechentyp_00015, flaechentyp_00052 | grund, ufer, weg |  | ±0,5 m |
| flaechentyp | 193.795 | 76.914 | flaechentyp_00011, flaechentyp_00015, flaechentyp_00052 | grund, ufer, weg |  | ±0,5 m |
| flaechentyp | 193.983 | 76.241 | flaechentyp_00011, flaechentyp_00015, flaechentyp_00052 | grund, ufer, weg |  | ±0,5 m |
| flaechentyp | 202.903 | 225.577 | flaechentyp_00016, flaechentyp_00041, flaechentyp_00052 | fels, grund, ufer |  | ±0,5 m |
| flaechentyp | 208.341 | 192.363 | flaechentyp_00003, flaechentyp_00012, flaechentyp_00018 | ufer, wasser, weg |  | ±0,5 m |
| flaechentyp | 209.585 | 6.603 | flaechentyp_00013, flaechentyp_00026, flaechentyp_00045 | fels, grund, ufer |  | ±0,5 m |
| flaechentyp | 209.933 | 192.844 | flaechentyp_00003, flaechentyp_00012, flaechentyp_00019 | ufer, wasser, weg |  | ±0,5 m |
| flaechentyp | 211.158 | 190.662 | flaechentyp_00012, flaechentyp_00018, flaechentyp_00056 | grund, ufer, weg |  | ±0,5 m |
| flaechentyp | 212.295 | 0.0 | flaechentyp_00013, flaechentyp_00045, ausserhalb | grund, ufer | ja | ±0,5 m |
| flaechentyp | 213.686 | 248.04 | flaechentyp_00016, flaechentyp_00041, flaechentyp_00052 | fels, grund, ufer |  | ±0,5 m |
| flaechentyp | 214.795 | 0.0 | flaechentyp_00000, flaechentyp_00013, ausserhalb | ufer, wasser | ja | ±0,5 m |
| flaechentyp | 216.801 | 199.226 | flaechentyp_00003, flaechentyp_00012, flaechentyp_00019 | ufer, wasser, weg |  | ±0,5 m |
| flaechentyp | 217.824 | 201.292 | flaechentyp_00003, flaechentyp_00012, flaechentyp_00020 | ufer, wasser, weg |  | ±0,5 m |
| flaechentyp | 218.779 | 0.0 | flaechentyp_00000, flaechentyp_00013, ausserhalb | ufer, wasser | ja | ±0,5 m |
| flaechentyp | 220.322 | 9.382 | flaechentyp_00013, flaechentyp_00026, flaechentyp_00046 | fels, grund, ufer |  | ±0,5 m |
| flaechentyp | 220.943 | 201.911 | flaechentyp_00012, flaechentyp_00020, flaechentyp_00052 | grund, ufer, weg |  | ±0,5 m |
| flaechentyp | 221.278 | 0.0 | flaechentyp_00013, flaechentyp_00046, ausserhalb | grund, ufer | ja | ±0,5 m |
| flaechentyp | 223.35 | 235.02 | flaechentyp_00020, flaechentyp_00043, flaechentyp_00052 | fels, grund, ufer |  | ±0,5 m |
| flaechentyp | 226.232 | 219.172 | flaechentyp_00020, flaechentyp_00043, flaechentyp_00052 | fels, grund, ufer |  | ±0,5 m |
| flaechentyp | 240.7 | 0.0 | flaechentyp_00026, flaechentyp_00046, ausserhalb | fels, grund | ja | ±0,5 m |
| flaechentyp | 295.035 | 166.829 | flaechentyp_00012, flaechentyp_00037, flaechentyp_00052 | fels, grund, weg |  | ±0,5 m |
| flaechentyp | 296.063 | 168.458 | flaechentyp_00012, flaechentyp_00037, flaechentyp_00052 | fels, grund, weg |  | ±0,5 m |
| flaechentyp | 336.0 | 4.159 | flaechentyp_00026, flaechentyp_00050, ausserhalb | fels, grund | ja | ±0,5 m |
| flaechentyp | 336.0 | 11.0 | flaechentyp_00026, flaechentyp_00050, ausserhalb | fels, grund | ja | ±0,5 m |
| flaechentyp | 336.0 | 36.521 | flaechentyp_00026, flaechentyp_00052, ausserhalb | fels, grund | ja | ±0,5 m |
| flaechentyp | 336.0 | 82.021 | flaechentyp_00031, flaechentyp_00052, ausserhalb | fels, grund | ja | ±0,5 m |
| flaechentyp | 336.0 | 97.096 | flaechentyp_00031, flaechentyp_00052, ausserhalb | fels, grund | ja | ±0,5 m |
| flaechentyp | 336.0 | 260.831 | flaechentyp_00020, flaechentyp_00052, ausserhalb | grund, ufer | ja | ±0,5 m |
| flaechentyp | 336.0 | 263.33 | flaechentyp_00003, flaechentyp_00020, ausserhalb | ufer, wasser | ja | ±0,5 m |
| flaechentyp | 336.0 | 268.176 | flaechentyp_00003, flaechentyp_00025, ausserhalb | ufer, wasser | ja | ±0,5 m |
| flaechentyp | 336.0 | 274.046 | flaechentyp_00003, flaechentyp_00025, ausserhalb | ufer, wasser | ja | ±0,5 m |
| flaechentyp | 336.0 | 285.515 | flaechentyp_00003, flaechentyp_00024, ausserhalb | ufer, wasser | ja | ±0,5 m |
| flaechentyp | 336.0 | 288.012 | flaechentyp_00024, flaechentyp_00062, ausserhalb | grund, ufer | ja | ±0,5 m |
| untergrund | 0.0 | 12.0 | untergrund_00063, untergrund_00089, ausserhalb | BODEN, SCHNEE | ja | ±0,5 m |
| untergrund | 0.0 | 30.4 | untergrund_00063, untergrund_00089, ausserhalb | BODEN, SCHNEE | ja | ±0,5 m |
| untergrund | 0.0 | 39.3 | untergrund_00081, untergrund_00089, ausserhalb | SCHATTEN, SCHNEE | ja | ±0,5 m |
| untergrund | 0.0 | 49.2 | untergrund_00081, untergrund_00089, ausserhalb | SCHATTEN, SCHNEE | ja | ±0,5 m |
| untergrund | 0.0 | 71.8 | untergrund_00089, untergrund_00096, ausserhalb | SCHNEE, WALD | ja | ±0,5 m |
| untergrund | 0.0 | 84.8 | untergrund_00089, untergrund_00096, ausserhalb | SCHNEE, WALD | ja | ±0,5 m |
| untergrund | 0.0 | 89.3 | untergrund_00089, untergrund_00097, ausserhalb | SCHNEE, WALD | ja | ±0,5 m |
| untergrund | 0.0 | 99.9 | untergrund_00089, untergrund_00097, ausserhalb | SCHNEE, WALD | ja | ±0,5 m |
| untergrund | 0.0 | 106.0 | untergrund_00089, untergrund_00099, ausserhalb | SCHNEE, WALD | ja | ±0,5 m |
| untergrund | 0.0 | 252.3 | untergrund_00089, untergrund_00099, ausserhalb | SCHNEE, WALD | ja | ±0,5 m |
| untergrund | 0.0 | 288.4 | untergrund_00089, untergrund_00108, ausserhalb | SCHNEE, WALD | ja | ±0,5 m |
| untergrund | 2.8 | 39.4 | untergrund_00081, untergrund_00089, untergrund_00094 | SCHATTEN, SCHNEE, WALD |  | ±0,5 m |
| untergrund | 9.1 | 44.0 | untergrund_00081, untergrund_00089, untergrund_00094 | SCHATTEN, SCHNEE, WALD |  | ±0,5 m |
| untergrund | 9.2 | 36.5 | untergrund_00079, untergrund_00089, untergrund_00094 | SCHATTEN, SCHNEE, WALD |  | ±0,5 m |
| untergrund | 17.6 | 31.0 | untergrund_00066, untergrund_00079, untergrund_00089 | BODEN, SCHATTEN, SCHNEE |  | ±0,5 m |
| untergrund | 20.1 | 41.7 | untergrund_00079, untergrund_00089, untergrund_00094 | SCHATTEN, SCHNEE, WALD |  | ±0,5 m |
| untergrund | 24.7 | 33.2 | untergrund_00066, untergrund_00079, untergrund_00089 | BODEN, SCHATTEN, SCHNEE |  | ±0,5 m |
| untergrund | 56.5 | 39.1 | untergrund_00066, untergrund_00080, untergrund_00089 | BODEN, SCHATTEN, SCHNEE |  | ±0,5 m |
| untergrund | 62.7 | 36.5 | untergrund_00066, untergrund_00080, untergrund_00093 | BODEN, SCHATTEN, WALD |  | ±0,5 m |
| untergrund | 64.6 | 34.1 | untergrund_00066, untergrund_00089, untergrund_00093 | BODEN, SCHNEE, WALD |  | ±0,5 m |
| untergrund | 66.6 | 42.7 | untergrund_00080, untergrund_00089, untergrund_00093 | SCHATTEN, SCHNEE, WALD |  | ±0,5 m |
| untergrund | 92.0 | 129.3 | untergrund_00083, untergrund_00089, untergrund_00100 | SCHATTEN, SCHNEE, WALD |  | ±0,5 m |
| untergrund | 104.8 | 109.2 | untergrund_00082, untergrund_00089, untergrund_00100 | SCHATTEN, SCHNEE, WALD |  | ±0,5 m |
| untergrund | 114.6 | 245.6 | untergrund_00085, untergrund_00089, untergrund_00107 | SCHATTEN, SCHNEE, WALD |  | ±0,5 m |
| untergrund | 116.4 | 133.2 | untergrund_00083, untergrund_00089, untergrund_00100 | SCHATTEN, SCHNEE, WALD |  | ±0,5 m |
| untergrund | 119.1 | 34.5 | untergrund_00074, untergrund_00089, untergrund_00091 | SCHATTEN, SCHNEE, WALD |  | ±0,5 m |
| untergrund | 123.6 | 118.7 | untergrund_00082, untergrund_00089, untergrund_00100 | SCHATTEN, SCHNEE, WALD |  | ±0,5 m |
| untergrund | 123.9 | 243.3 | untergrund_00085, untergrund_00089, untergrund_00107 | SCHATTEN, SCHNEE, WALD |  | ±0,5 m |
| untergrund | 140.1 | 19.1 | untergrund_00074, untergrund_00089, untergrund_00091 | SCHATTEN, SCHNEE, WALD |  | ±0,5 m |
| untergrund | 143.4 | 29.2 | untergrund_00068, untergrund_00074, untergrund_00089 | BODEN, SCHATTEN, SCHNEE |  | ±0,5 m |
| untergrund | 153.0 | 26.1 | untergrund_00068, untergrund_00074, untergrund_00089 | BODEN, SCHATTEN, SCHNEE |  | ±0,5 m |
| untergrund | 162.2 | 22.5 | untergrund_00067, untergrund_00074, untergrund_00089 | BODEN, SCHATTEN, SCHNEE |  | ±0,5 m |
| untergrund | 170.5 | 25.5 | untergrund_00067, untergrund_00074, untergrund_00089 | BODEN, SCHATTEN, SCHNEE |  | ±0,5 m |
| untergrund | 211.5 | 231.1 | untergrund_00087, untergrund_00089, untergrund_00104 | SCHATTEN, SCHNEE, WALD |  | ±0,5 m |
| untergrund | 217.3 | 235.8 | untergrund_00087, untergrund_00089, untergrund_00104 | SCHATTEN, SCHNEE, WALD |  | ±0,5 m |
| untergrund | 222.0 | 29.2 | untergrund_00075, untergrund_00089, untergrund_00092 | SCHATTEN, SCHNEE, WALD |  | ±0,5 m |
| untergrund | 226.0 | 21.7 | untergrund_00075, untergrund_00089, untergrund_00092 | SCHATTEN, SCHNEE, WALD |  | ±0,5 m |
| untergrund | 233.5 | 41.3 | untergrund_00065, untergrund_00089, untergrund_00092 | BODEN, SCHNEE, WALD |  | ±0,5 m |
| untergrund | 238.4 | 32.0 | untergrund_00065, untergrund_00076, untergrund_00092 | BODEN, SCHATTEN, WALD |  | ±0,5 m |
| untergrund | 240.8 | 20.0 | untergrund_00076, untergrund_00089, untergrund_00092 | SCHATTEN, SCHNEE, WALD |  | ±0,5 m |
| untergrund | 256.6 | 27.8 | untergrund_00065, untergrund_00076, untergrund_00090 | BODEN, SCHATTEN, WALD |  | ±0,5 m |
| untergrund | 267.8 | 15.1 | untergrund_00076, untergrund_00089, untergrund_00090 | SCHATTEN, SCHNEE, WALD |  | ±0,5 m |
| untergrund | 268.8 | 17.5 | untergrund_00065, untergrund_00089, untergrund_00090 | BODEN, SCHNEE, WALD |  | ±0,5 m |
| untergrund | 277.6 | 241.7 | untergrund_00086, untergrund_00089, untergrund_00106 | SCHATTEN, SCHNEE, WALD |  | ±0,5 m |
| untergrund | 289.0 | 228.1 | untergrund_00086, untergrund_00089, untergrund_00106 | SCHATTEN, SCHNEE, WALD |  | ±0,5 m |
| untergrund | 296.2 | 226.2 | untergrund_00086, untergrund_00089, untergrund_00105 | SCHATTEN, SCHNEE, WALD |  | ±0,5 m |
| untergrund | 301.7 | 232.8 | untergrund_00086, untergrund_00089, untergrund_00105 | SCHATTEN, SCHNEE, WALD |  | ±0,5 m |
| untergrund | 336.0 | 10.0 | untergrund_00077, untergrund_00089, ausserhalb | SCHATTEN, SCHNEE | ja | ±0,5 m |
| untergrund | 336.0 | 21.5 | untergrund_00077, untergrund_00089, ausserhalb | SCHATTEN, SCHNEE | ja | ±0,5 m |
| untergrund | 336.0 | 69.8 | untergrund_00089, untergrund_00095, ausserhalb | SCHNEE, WALD | ja | ±0,5 m |
| untergrund | 336.0 | 85.9 | untergrund_00089, untergrund_00095, ausserhalb | SCHNEE, WALD | ja | ±0,5 m |
| untergrund | 336.0 | 89.8 | untergrund_00089, untergrund_00098, ausserhalb | SCHNEE, WALD | ja | ±0,5 m |
| untergrund | 336.0 | 181.4 | untergrund_00089, untergrund_00098, ausserhalb | SCHNEE, WALD | ja | ±0,5 m |
| untergrund | 336.0 | 207.7 | untergrund_00089, untergrund_00103, ausserhalb | SCHNEE, WALD | ja | ±0,5 m |
| untergrund | 336.0 | 250.2 | untergrund_00089, untergrund_00103, ausserhalb | SCHNEE, WALD | ja | ±0,5 m |
| untergrund | 336.0 | 277.5 | untergrund_00089, untergrund_00108, ausserhalb | SCHNEE, WALD | ja | ±0,5 m |

## Q14 Bauzone (Zellformat)

Komponenten 25, Zellsumme 31893 (Soll 31893), doppelt 0; CSV `neu/zellen_relief.csv` (bauzone_plan = 1): 31893; fehlend 0, zusätzlich 0 → deckungsgleich: ja. Q14 gesamt bleibt am alten Mesh nur wegen des fehlenden Wasserspiegel-Modells fehler.
