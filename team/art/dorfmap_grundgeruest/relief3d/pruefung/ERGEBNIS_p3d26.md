# Ergebnis p3d26

Stand 13.11.2026 · Branch `art/dorfmap-p3d26` · Basis `89c61ce` (`origin/art/dorfmap-p3d25`) · Kosten 0 EUR.

Endstand nach Überschreitung der vorgegebenen Gesamtzeit. Die Familienmachbarkeit ist belegt; die offizielle Float32-Probe und das Meshgate wurden deshalb nicht begonnen.

Marker: `[S]` ausgeführte Messung oder Test · `[R]` Modellbefund · `[A]` Annahme · `[F]` Freigabe.

## Prüferausnahme und Tests

`[F]` Fabian hat am 13.11.2026 (Widget `t166s961`) ausschließlich für den 4-m-Auslauf am Anfang von `rampe_2`, ID `rampe_2_anfang`, Koordinate `126.51|31.62`, die R8a-Paargrenze von 0,10 m auf 0,18 m freigegeben. Alle anderen 25 Rampenenden behalten 0,10 m. V3 speichert denselben Start als `126.5100002|31.6200017`; die Zuordnung verlangt Wegend-ID plus Koordinate innerhalb 1e-5 Karten-Einheiten (12 µm), nicht einen räumlichen Suchradius.

`[S]` Die neue Policy-Testdatei besteht mit 2 Tests. Ein synthetisches Paar mit 0,17 m am freigegebenen Ende ist kein Treffer; 0,19 m ist ein Treffer. Für jedes der übrigen 25 Wegenden ergibt 0,11 m einen Treffer. Die Testbelege liegen in [`p3d26_R8a_exception_tests.json`](../../../../../codex_jobs/tools/p3d26/results/p3d26_R8a_exception_tests.json).

`[S]` Die p3d17-R3-Kalibrierung vor und nach der Prüferänderung ist identisch: D1 `6/17/19`, D1-Höhenhash `26b849f6384993d5029b58dc08f6c657406785e26939f7c172a0d8fafe1ace29`, bytegleicher Transfer. Belege: [`vorher`](../../../../../codex_jobs/tools/p3d26/results/p3d26_R3_calibration_before.json) und [`nachher`](../../../../../codex_jobs/tools/p3d26/results/p3d26_R3_calibration_after.json).

`[S]` Die bestehende Suite `python3 -m pytest -q neu/tests` ergibt 26 bestanden und 5 fehlgeschlagen; dieselben fünf Altfehler sind in p3d18 dokumentiert (R8a insgesamt, R9-Sägezahn D1, D1-Wandkante, F1/C1-Wegende, Schattenbild). Der zusätzliche R8a-Policy-Test besteht separat. `py_compile` und `git diff --check` bestehen.

### Vollständiger Diff des offiziellen R8-Prüfers

```diff
diff --git a/team/art/dorfmap_grundgeruest/relief3d/pruefung/r8_kreuzung.py b/team/art/dorfmap_grundgeruest/relief3d/pruefung/r8_kreuzung.py
--- a/team/art/dorfmap_grundgeruest/relief3d/pruefung/r8_kreuzung.py
+++ b/team/art/dorfmap_grundgeruest/relief3d/pruefung/r8_kreuzung.py
@@ -7,6 +7,7 @@
 import json,gzip,sys,base64,numpy as np,scipy.ndimage as nd
 from scipy.spatial import cKDTree
+from r8a_policy import r8a_exception_for_endpoint, r8a_pair_is_hit, r8a_pair_limit_m
 f=sys.argv[1] if len(sys.argv)>1 else 'relief_daten.json.gz';D=json.load(gzip.open(f));NX,NY,RS=D['nx'],D['ny'],D['rs'];GX,GY=NX*RS+1,NY*RS+1
@@ -78,7 +79,9 @@ for g in grp.values():
         if all(K[i][1].endswith(('_anfang','_ende')) for i in g):   # reines Wegende: Quergefaelle senkrecht zur Wegrichtung (Laengsgefaelle zaehlt nicht)
             i0=g[0];ri=int(K[i0][1].split('_')[1]);pp=R[ri][0];dv=(pp[min(8,len(pp)-1)]-pp[0]) if K[i0][1].endswith('_anfang') else (pp[-1]-pp[max(0,len(pp)-9)]);dv=dv/max(np.hypot(*dv),1e-9);q=float(abs(-dv[1]*co[0]+dv[0]*co[1])*100);KL[-1]['quer_pct']=round(q,1)
         if q>3.0:hit('R8_quer',x,z,round(q,1),art=KL[-1]['art'])
-# R8a Wegende (t122u): Auslauf 4 m hinter dem Ende, Streifen +-2,5 m um die verlaengerte Mittellinie, ohne Wand (Neigung>1): max Nachbar-dh (0,25 m) > 0,10 m = Treffer
+# R8a Wegende (t122u): Auslauf 4 m hinter dem Ende, Streifen +-2,5 m um die verlaengerte Mittellinie, ohne Wand (Neigung>1).
+# Alle Wegenden behalten 0,10 m, ausser R8a_ausnahme_rampe2_start ([F] Fabian, t166s961, 2026-11-13):
+# nur rampe_2_anfang bei 126.51|31.62 erhaelt im eigenen 4-m-Auslauf 0,18 m.
 gyF,gxF=np.gradient(H,1/FS);WANDF=np.hypot(gxF,gyF)>1.0
 for i,(p,_) in enumerate(R):
@@ -89,7 +92,8 @@ for i,(p,_) in enumerate(R):
         for ax in (0,1):
             dA=np.abs(np.diff(A,axis=ax));mm=(M[1:,:]&M[:-1,:]) if ax==0 else (M[:,1:]&M[:,:-1])
             if mm.any():st=max(st,float(dA[mm].max()))
-        if st>0.10:hit('R8a_wegende',q0[0],q0[1],round(st,2),weg=f'rampe_{i}_{e}')
+        weg=f'rampe_{i}_{e}';limit=r8a_pair_limit_m(weg,q0);ausnahme=r8a_exception_for_endpoint(weg,q0)
+        if r8a_pair_is_hit(st,weg,q0):hit('R8a_wegende',q0[0],q0[1],round(st,2),weg=weg,limit_m=limit,ausnahme=ausnahme)
```

Die gemeinsame Policy in `r8a_policy.py` wird sowohl vom offiziellen Prüfer als auch vom p3d23-Familienmodell aufgerufen. Das Familienmodell wendet 0,18 m ausschließlich auf die Paare im bestehenden 4-m-Auslauf der identifizierten `rampe_2_anfang`-Geometrie an; übrige Wegende-Paare bleiben bei 0,10 m. Wegdaten und andere Schwellen wurden nicht geändert.

## Geometriewahl

`[R]` Arbeitsbasis ist p3d23 V3 mit unverändertem Start von rampe_2. p3d24 dokumentiert V3 als Basis mit den kleinsten lokalen Geometrieänderungen an rampe_2 und unveränderter rampe_11; p3d25 V1 bleibt nur die ausdrücklich erlaubte zweite Wahl, falls der V3-Hartsolve mit der Ausnahme unlösbar ist. Keine Wegdaten wurden bisher verändert.

## Familienmachbarkeit

`[S]` V3 ist im p3d23-Familienmodell mit allen Familien hart **machbar**, HiGHS Status 7 (`Optimal`), 7.885 Variablen und 25.886 Bedingungen. `diagnostic_groups_enabled=[]`; alle 27 Familien-Schlupfvariablen sind 0 und der gewichtete L1-Schlupf ist 0. Deshalb wurde die zweite Wahl p3d25 V1 nicht ausgeführt.

`[S]` Die R8a-Paarbedingungen enthalten 2.054 Paare: 0,10 m überall und 0,18 m nur für die Paare im Rampe-2-Startauslauf. Die benannte Ausnahme und Quelle `[F]` stehen im Solver-JSON. Das größte numerische Restmaß an einem regulären Wegende ist `2,27e-14 m` bei `rampe_11_anfang`, Paar `148.0|2.5`–`148.0|2.75` mit `0.100000000000023 m` gegenüber 0,10 m; das liegt innerhalb der Solver-Fließkommatoleranz. Wegende-Stufe bleibt 0,054 m (numerischer Rest `4,93e-16 m`).

`[S]` Die Kreuzungsmodellwerte erfüllen die unveränderten Grenzen: Stufe `0.116000000002 m`, Gitter `0.0190000000004 m` (Modellziel 0,019 m) und Querneigung `2.9500000000001 %`; Einzelquergrenze 19,5 %. Keine R9w-Gleichheitsfixierung oder Regressionszaun-Höhenpins wurden hinzugefügt (`R9w_exact_bandpass_lock_points=0`, Regressionszaun-Zähler leer). Solverbeleg: [`p3d26_V3_all_hard_with_rampe2_exception.json`](../../../../../codex_jobs/tools/p3d26/results/p3d26_V3_all_hard_with_rampe2_exception.json).

`[S]` Quelle und Transferbasis stimmen mit den p3d23-Belegen überein (Quellhash `b1e347e0…`, Transferhash `07c140cf…`). Die Laufzeitgrenze von etwa fünf Stunden war beim Wiederaufnehmen bereits überschritten: Der Laufzeitnachweis beginnt am 13.11.2026 um ca. 00:37 Europe/Berlin; beim Stand 08:15 waren etwa 7 h 38 min vergangen. Deshalb wurde gemäß Auftrag vor der offiziellen Float32-Probe gestoppt. Es gibt keine p3d26-Proberunde, keine p3d26-Regel-/Kachel-Nachherzahlen, keinen Meshbau, keine Delta-/LOD1-Prüfung und keine Bilder.

### Regelzahlen vorher / p3d26

`[S]` Die historische Vorher-Spalte ist der vorgegebene Stand `9d3f8fc`. Der letzte verfügbare D1/G1/D2-Kontext ist der p3d17-Referenzreplay im aktuellen Prüferschema; er ist keine p3d26-Probe. Wegen des Zeitlimits sind alle p3d26-Nachherwerte ausdrücklich **nicht gemessen**.

| Regel | 9d3f8fc vorher gesamt | p3d17-Referenz D1/G1/D2 | p3d26 nachher |
|---|---:|---:|---|
| R1_blind | 24 | 2 / 1 / 0 | nicht gemessen |
| R2_getrennt | 15 | 1 / 0 / 1 | nicht gemessen |
| R3_laengs_m | 35 | 6 / 1 / 0 | nicht gemessen |
| R3_quer_pct | 29 | 17 / 0 / 0 | nicht gemessen |
| R3_woelb_m | 31 | 19 / 0 / 0 | nicht gemessen |
| R4_rand | 1 | 1 / 0 / 0 | nicht gemessen |
| R4_schlucht | 0 | 0 / 0 / 0 | nicht gemessen |
| R5_loch | 25 | 8 / 0 / 0 | nicht gemessen |
| R5_spitze | 0 | 0 / 0 / 0 | nicht gemessen |
| R6_wasser_schnee | 4 | 0 / 3 / 0 | nicht gemessen |
| G2_spitze_oben | 3 | 0 / 0 / 0 | nicht gemessen |
| G2_spitze_oben_fein | 8 | 0 / 0 / 0 | nicht gemessen |
| G3_spitze_unten | 4 | 1 / 0 / 0 | nicht gemessen |
| G3_spitze_unten_fein | 2 | 0 / 0 / 0 | nicht gemessen |
| G5_beule_klippe | 69 | 2 / 0 / 0 | nicht gemessen |
| G6_facette | 219 | 3 / 3 / 0 | nicht gemessen |
| G7_wand_glatte_flaeche | 1 | 0 / 0 / 0 | nicht gemessen |
| G7b_wandkontur_feld | 25 | 1 / 0 / 0 | nicht gemessen |
| G7b_wandkontur_kantenschaerfe | 1 | 0 / 0 / 0 | nicht gemessen |
| G7b_wandkontur_rauheit | 1 | 0 / 0 / 0 | nicht gemessen |
| G8_fluss_nicht_bis_rand | 1 | 0 / 0 / 0 | nicht gemessen |
| G11_objekt_schwebt_sinkt | 0* | 2 / 2 / 0 | nicht gemessen |
| T1_fleckrand | 94 | 0 / 3 / 7 | nicht gemessen |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 0 / 0 / 0 | nicht gemessen |
| T3_streifen_ringe_bildpruefung_offen | 1 | 0 / 0 / 0 | nicht gemessen |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 0 / 0 / 0 | nicht gemessen |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 0 / 0 / 0 | nicht gemessen |
| **pruefe_regeln Summe** | **596** | **Referenzreplay gesamt 600** | **nicht gemessen** |

`*` Das historische 596er-Schema hatte keinen G11-Zähler; der aktuelle Referenzreplay zählt 4 G11-Objekttreffer (D1=2, G1=2).

| R8-Regel | 9d3f8fc vorher gesamt | p3d17-Referenz D1/G1/D2 | p3d26 nachher |
|---|---:|---:|---|
| R8_stufe | 9 | 2 / 0 / 0 | nicht gemessen |
| R8_gitter | 10 | 2 / 0 / 0 | nicht gemessen |
| R8_quer | 5 | 0 / 0 / 0 | nicht gemessen |
| R8a_wegende | 24 | 3 / 0 / 0 | nicht gemessen |
| **R8 Summe** | **48** | **gesamt 46; D1=7 / G1=0 / D2=0** | **nicht gemessen** |

| R9-Regel | 9d3f8fc vorher gesamt | p3d17-Referenz D1/G1/D2 | p3d26 nachher |
|---|---:|---:|---|
| R8b_delle | 25 | 1 / 0 / 0 | nicht gemessen |
| R9_saegezahn | 34 | 1 / 1 / 0 | nicht gemessen |
| R9w_wellen | 275 | 27 / 12 / 0 | nicht gemessen |
| **R9 Summe** | **334** | **gesamt 344; D1=29 / G1=13 / D2=0** | **nicht gemessen** |

`[S]` Die D2-Quellwerte wurden nicht geändert; ohne p3d26-Probe ist jedoch nicht neu nachgewiesen, dass keine D2-Treffer hinzukamen. Ebenso sind `t42u=0`, `lod1<1,3 Mio.`, G1-/D2-Hashvergleich und sämtliche geforderten Bildansichten für p3d26 nicht gemessen.

## Laufzeitgrenze und Abschluss

`[S]` Die Machbarkeit ist belegt, die eigentliche offizielle Probe wurde wegen der überschrittenen Gesamtzeitgrenze nicht begonnen. Damit sind die harten Prüferziele und der Meshzustand für p3d26 weder bestanden noch widerlegt; das Ergebnis bleibt unverifiziert. Es wurden keine p3d26-Geometrie- oder Zellquellwerte geändert und kein Mesh erzeugt.

## Drei-Satz-Schluss

`[S]` Die eng begrenzte Ausnahme ist getestet, die R3-Kalibrierung blieb vor/nach der Prüferänderung bei `6/17/19`, und die p3d23-V3-Führung ist mit allen Familien hart machbar. `[S]` Wegen Überschreitung des Fünf-Stunden-Limits wurde die Float32-Probe vor Runde 1 gestoppt; deshalb gibt es keine p3d26-Nachherzahlen, keinen Meshbau und keine Bilder. `[A]` Das Qualitätsziel ist damit nicht verifiziert; D2-Regression, t42u, LOD1 und die übrigen Gateziele bleiben offen.
