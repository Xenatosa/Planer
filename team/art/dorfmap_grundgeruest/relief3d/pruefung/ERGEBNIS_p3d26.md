# Ergebnis p3d26

Stand 13.11.2026 · Branch `art/dorfmap-p3d26` · Basis `89c61ce` (`origin/art/dorfmap-p3d25`) · Kosten 0 EUR.

Zwischenstand nach Prüferausnahme und Tests. Familienmachbarkeit, offizielle Float32-Probe und Meshgate stehen noch aus.

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

## Geometriewahl und nächster Schritt

`[R]` Arbeitsbasis ist p3d23 V3 mit unverändertem Start von rampe_2. p3d24 dokumentiert V3 als Basis mit den kleinsten lokalen Geometrieänderungen an rampe_2 und unveränderter rampe_11; p3d25 V1 bleibt nur die ausdrücklich erlaubte zweite Wahl, falls der V3-Hartsolve mit der Ausnahme unlösbar ist. Keine Wegdaten wurden bisher verändert.

`[S]` Der all-hart Familienlauf mit 0,18 m nur an `rampe_2_anfang` ist noch nicht ausgeführt. Daher sind offizielle Probe, Regel- und Kachelzahlen nach Änderung, Mesh, Delta, LOD1 und Bilder noch nicht gemessen. Das Arbeitsziel ist bis zu diesen Schritten offen.
