# Gegenprobe Runde 6: Q3-Zonenringe auf art/dorfmap-fertig bf9f62d (#61 gemergt, zonen.geojson = 5dabe976)

QA Runde 6 (F14 Brücke offen bis P5, F15 Wegenden-Ausnahme A-DV2-01). Vollständige Abschnittsliste und Stoßpunktliste: `R5_zonen_5dabe976.md` (Zonen unverändert).

## Q3 Zonenringe (Vektor) nach Gruppe

| Gruppe | Ringe | Abschnitte | Behandlung |
|---|---|---|---|
| bruecke | 13 | 40 | **offen P5** (F14), Befund mit `offen: P5` |
| sonst (Wegenden) | 10 | 98 | Ausnahme A-DV2-01 (F15), 0 Rest |
| stoss_nah | 6 | 13 | **hart → Befund P1c** |
| kartenrand_nah | 0 | 0 | – (F13) |

## stoss_nah: 13 Abschnitte

Bogenlänge = Abstand des Abschnitts (erster–letzter Abtastpunkt) zum nächsten Stoßpunkt entlang des Rings. Alle liegen **außerhalb** des ± 0,5-m-Fensters (kürzester Abstand 0,502–0,851 m); der Abschnitt beginnt jeweils direkt hinter der Fenstergrenze. Kein Fehler in der Fensterlogik: Im Selbsttest (F11/F13) hinterlässt eine 90-Grad-Ecke am Stoßpunkt außerhalb des Fensters keinen Rest. Alle 13 liegen 0,96–1,48 m vor einem Mittellinien-Ende, also runde Wegenden, die direkt am Stoßpunkt beginnen → Befund für P1c.

| Ring | Typ | x | z | Abw. cm | Knick ° | Länge m | Stoßpunkt x | z | Bogenlänge min–max m | im Fenster |
|---|---|---|---|---|---|---|---|---|---|---|
| flaechentyp_00011 | weg | 193.89 | 77.5 | 3.1 | 6.3 | 0.5 | 193.795 | 76.914 | 0.545–0.995 | nein |
| flaechentyp_00012 | weg | 208.34 | 191.5 | 4.8 | 9.8 | 0.5 | 208.341 | 192.363 | 0.547–0.997 | nein |
| flaechentyp_00012 | weg | 218.32 | 201.32 | 3.0 | 6.3 | 0.05 | 217.824 | 201.292 | 0.502–0.502 | nein |
| flaechentyp_00012 | weg | 221.38 | 202.75 | 3.5 | 7.8 | 0.15 | 220.943 | 201.911 | 0.851–0.951 | nein |
| flaechentyp_00012 | weg | 296.09 | 167.86 | 3.5 | 7.5 | 0.5 | 296.063 | 168.458 | 0.504–0.954 | nein |
| flaechentyp_00012 | weg | 295.81 | 167.28 | 3.5 | 7.3 | 0.5 | 295.035 | 166.829 | 0.516–0.966 | nein |
| flaechentyp_00012 | weg | 192.24 | 111.26 | 4.7 | 10.1 | 0.85 | 192.815 | 110.545 | 0.533–1.383 | nein |
| flaechentyp_00015 | ufer | 192.24 | 111.25 | 4.7 | 10.1 | 0.85 | 192.815 | 110.545 | 0.527–1.377 | nein |
| flaechentyp_00018 | ufer | 208.34 | 191.5 | 4.8 | 9.8 | 0.5 | 208.341 | 192.363 | 0.547–0.997 | nein |
| flaechentyp_00037 | fels | 295.54 | 167.03 | 3.5 | 8.0 | 0.5 | 295.035 | 166.829 | 0.549–0.999 | nein |
| flaechentyp_00037 | fels | 295.97 | 167.52 | 3.5 | 7.6 | 0.5 | 296.063 | 168.458 | 0.52–0.97 | nein |
| flaechentyp_00052 | grund | 193.89 | 77.51 | 3.1 | 6.3 | 0.5 | 193.795 | 76.914 | 0.507–0.957 | nein |
| flaechentyp_00052 | grund | 221.41 | 202.78 | 3.6 | 7.3 | 0.2 | 220.943 | 201.911 | 0.841–0.991 | nein |

## F14 Brücke offen bis P5 (je Ring größter Ausschlag)

| Ring | Quelle | Abw. cm | Knick ° | x | z |
|---|---|---|---|---|---|
| flaechentyp_00007 | vektor | 18.8 | 103.8 | 187.04 | 76.21 |
| flaechentyp_00008 | vektor | 21.1 | 120.2 | 188.06 | 123.98 |
| flaechentyp_00009 | vektor | 21.4 | 103.1 | 175.44 | 129.68 |
| flaechentyp_00010 | vektor | 18.6 | 96.8 | 187.81 | 73.29 |
| flaechentyp_00012 | vektor | 19.7 | 4.5 | 184.29 | 129.91 |
| flaechentyp_00015 | vektor | 23.9 | 139.8 | 190.14 | 74.32 |
| flaechentyp_00016 | vektor | 23.4 | 125.4 | 178.2 | 129.45 |
| flaechentyp_00017 | vektor | 24.2 | 140.7 | 189.68 | 76.11 |
| flaechentyp_00018 | vektor | 19.1 | 93.7 | 184.28 | 129.91 |
| flaechentyp_00052 | vektor | 16.3 | 83.8 | 187.81 | 73.29 |
| flaechentyp_00054 | vektor | 18.7 | 103.2 | 186.99 | 76.2 |
| flaechentyp_00055 | vektor | 22.5 | 115.5 | 188.07 | 123.98 |
| flaechentyp_00056 | vektor | 15.3 | 50.4 | 184.27 | 129.93 |

## F15 Wegenden-Ausnahme A-DV2-01 (je Ring)

| Ring | Abschnitte | max. Abw. cm |
|---|---|---|
| flaechentyp_00010 | 9 | 4.8 |
| flaechentyp_00011 | 16 | 4.8 |
| flaechentyp_00012 | 24 | 4.8 |
| flaechentyp_00015 | 1 | 4.7 |
| flaechentyp_00018 | 1 | 4.7 |
| flaechentyp_00037 | 1 | 3.5 |
| flaechentyp_00052 | 37 | 4.8 |
| flaechentyp_00054 | 2 | 4.8 |
| flaechentyp_00056 | 6 | 4.8 |
| flaechentyp_00058 | 1 | 3.1 |

Mesh-Kantenzüge (altes Mesh, folgt den Zonen nicht, nur Bericht): {"ringe": 107, "ringe_je_gruppe": {"kartenrand_nah": 12, "sonst": 95}}.
