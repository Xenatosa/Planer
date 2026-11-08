# Anschluss t141u (nach p3d3)

## p3d3 ad479b9 — nicht mergen
Unabhaengig (06.11. ~23:05): Mesh D1 702 Vert. geaendert, max|Δ| 3,31 m; Kreuzung 152.5|28.5 Mesh-ptp≈0 (GB≈3,11); G1 0 Vert.; D2 max|Δ| 0; Klippe 140|35 h identisch GB. Bericht Stufe 1,746→0,038 m an Schnittpunkt plausibel. Clay: Kreuzung weicher, Wandfussnaht weiter sichtbar, Wegende ohne klaren Auslauf.
Blocker: delta 10 Anstiege (R3_laengs D1 +5, G7b D1 +1, Clay); R8a 23; Saegezahn 47; G1 unangetastet (VAR=2 schaltet Wege/Rampen aus); Suite 13/9. Tests: Grenzen nicht gelockert (Wegende-Null wieder aktiv).

## Laeuft
- **p3d4** `/workspace/wt_dorfmap_p3d4` Branch `art/dorfmap-p3d4` Basis p3d3
- Log `codex_jobs/log_p3d4.txt` (ab 07.11. 10:47 Fortsetzung `log_p3d4b.txt`) Ende `ende_p3d4.txt`
- Log-Modell: gpt-6-luna / xhigh
- Isoliert: Wegenden-Auslauf, Wandfussnaht, Kreuzung ohne R3+5 / ohne Endpunkt-Verschlechterung

## Nach ende_p3d4
Bericht lesen, Mesh unabhaengig messen, Nahbilder ansehen, nur mergen wenn Delta ok und Kriterien. Sonst Zahlen + naechster isolierter Auftrag noch am selben Tag — nicht bis Werktag liegen lassen.

## Stand 07.11. ~15:00 — p3d4 nicht gemergt, p3d5 laeuft
- **p3d5** `/workspace/wt_dorfmap_p3d5` Branch `art/dorfmap-p3d5` Basis p3d4 d407307; Log `codex_jobs/log_p3d5.txt`, Ende `ende_p3d5.txt`, Start `starte_p3d5.sh`; Log gpt-6-luna/xhigh.
- Nach ende_p3d5: gleiche Gegenpruefung (delta 0? R3 D1<=6, Wandfuss-Nahbild ohne Stufen/Splitter, G11 0, t42u 0, D2 bytegleich, Lochscan xvfb). Nur bei Bestehen nach grundgeruest mergen; sonst Zahlen + naechster isolierter Auftrag sofort.

## Stand 07.11. ~19:00 — p3d5 nicht gemergt, p3d6 laeuft
- **p3d6** `/workspace/wt_dorfmap_p3d6` Branch `art/dorfmap-p3d6` Basis p3d5 6e58af0; Log `codex_jobs/log_p3d6.txt`, Ende `ende_p3d6.txt`, Start `starte_p3d6.sh`; Log gpt-6-luna/xhigh.
- Nach ende_p3d6: gleiche Gegenpruefung (delta 0? R3 D1<=6, R9w G1<=6, Wandfuss-Nahbild ohne Kerben, G7b D1 0, t42u 0, D2 bytegleich, Lochscan xvfb). Nur bei Bestehen mergen; sonst Zahlen + naechster isolierter Auftrag sofort.

## Stand 08.11. ~05:20 — p3d6 nicht gemergt, p3d7 laeuft
- p3d6 0cdb862 unabhaengig bestaetigt (Zahlen = Bericht, 19 Deltas, R3 D1 10); Ursache: D1/G1-Gelaende seit p3d4 unveraendert (Hash bbc2de2f…), Kreuzungsplateau 5.03 m mit ~1 m/m-Uebergaengen. Details runde_o_status.md (Watch 08.11. ~05:20).
- **p3d7** `/workspace/wt_dorfmap_p3d7` Branch `art/dorfmap-p3d7` Basis p3d6 0cdb862; Log `codex_jobs/log_p3d7.txt`, Ende `ende_p3d7.txt`, Start `starte_p3d7.sh`, Auftrag `job_p3d7.txt`, Messgrundlage `codex_jobs/tools/p3d7_lp/`; Log gpt-6-luna/xhigh, PID 568228.

## Nach ende_p3d7 (Pruefschema)
1. Log: Zeilen `model: gpt-6-luna` / `reasoning effort: xhigh`; Commit gepusht, Worktree sauber.
2. `git diff --stat ad479b9 <commit>` auf gen_relief.py, pruefung/*.py, neu/tests, *.js-Tests: unveraendert (Adapter/delta.py wie p3d6).
3. Detached Kopie (`git worktree add --detach /tmp/gp_p3d7 <commit>`), `RELIEF_NEU=1 gen_relief.py && baue_html.py`, keine Diffs; t42u 0; Adapter -> gate.json.gz; Loch xvfb 0; regeln/r8/r9 auf Adapter-Gate.
4. PFLICHT: Adapter-height_sha256 D1 != bbc2de2f… (sonst Lauf wertlos), D2 = 749d3c4b…, D2-Screenshot e8db06e6….
5. Zahlen: R3_laengs D1 <=6 (r3_profil.py aus tools/p3d7_lp fuer Profil/Abschnitte), R8/R8a D1/G1 0, Kreuzung <=0.20, Endpunkt 156.5|37.5 <=0.20, Klippe 140|35 7.8840365, G7b/G6/R9w/Saegezahn nicht schlechter als p3d6.
6. delta.py: p3d6 -> p3d7 0 Gate-Anstiege; VAR0 -> p3d7 < 19 (5 Kameras aus bilder_p3d6/kameras.json selbst rendern). pytest (python3 -m pytest, user-installiert) nicht schlechter als 26/5.
7. Nahbilder bilder_p3d7 selbst ansehen (D1 Kreuzung + Streiflicht rampe_11, Wandfuss 140|35, Wegende, G1, D2) vs bilder_p3d6.
8. Merge nach grundgeruest nur bei delta 0 und allen Kriterien; sonst Zahlen + naechster isolierter Auftrag sofort (Wandfuss D1/G1 als eigenes Thema, falls R3 geloest).

## Stand 08.11. ~11:00 — p3d7 gegengeprueft, nicht gemergt; p3d8 startet
- p3d7 5dc3fa8 unabhaengig in /tmp/gp_p3d7 (detached) neu gebaut: deterministisch, Pruefer/gen_relief/pruefe_*/neu/tests/Schwellen seit ad479b9 unveraendert (Adapter/delta.py identisch mit p3d6). Log gpt-6-luna/xhigh, 564322 Tokens.
- Messung = Codex-Bericht: R3 D1 13 (p3d6 10, Ziel <=6), Kreuzung 152.5|28.5 Stufe 0.572 (p3d6 0.116, Ziel <=0.20), Endpunkt 156.5|37.5 Stufe 0.123 (p3d6 0.188) aber neuer R8a-Treffer D1, R8/R8a D1 nicht mehr 0. delta p3d6->p3d7 21 Anstiege, VAR0->p3d7 24. Adapter-Gates 567/41/337 (p3d6 563/39/336). pytest 23/8 (p3d6 26/5). max |Δh| D1 5.97074 m bei 144.5|21.5 (Quelle 12.865 -> Mesh 6.895).
- Gehalten: t42u 0, Loch xvfb 0, D1-Hash bbc2de2f… -> ad026456… (Nachweis erfuellt), G1 38afeb30…, D2 749d3c4b…, Klippe 140|35 = 7.8840365 m, LOD1 134316. D2-Screenshot p3d7 = b060ec58… (p3d6 e8db06e6…; 3294 px, max |d|=8, Mesh bytegleich, D1-Suedrand in der Draufsicht sichtbar).
- Nahbilder: D1-Kreuzung neues Facetten-/Gratband; Streiflicht zeigt Kante; Wegende rechts gestuft; Wandfuss Kerben plus mehr Sprenkel; G1 pixelgleich.
- Ursache: 1D-LP trifft sich am Schnitt bei ~4.42 m, aber der 2D-Transfer schreibt die Profilhoehe hart in den Korridor (1.8+8.0 = 9.8 m seitlich) und das laterale Fade wirkt nicht als Hoehenmischung (wall_weight=1 abseits der Wand). Deshalb der 5.97-m-Absturz 7.9 m neben rampe_2.
- NICHT nach grundgeruest mergen.
- **p3d8** `/workspace/wt_dorfmap_p3d8` Branch `art/dorfmap-p3d8` Basis p3d6 0cdb862; Log `codex_jobs/log_p3d8.txt`, Ende `ende_p3d8.txt`, Start `starte_p3d8.sh`, Auftrag `job_p3d8.txt`; Log gpt-6-luna/xhigh, PID 718042.

## Nach ende_p3d8 (Pruefschema)
Wie „Nach ende_p3d7“, mit /tmp/gp_p3d8 und Vergleich gegen die unabhaengige p3d6-Referenz (R3 D1 nicht >10, Kreuzung nicht >0.116 bzw. <=0.20, delta p3d6->p3d8 = 0 Gate-Anstiege, D1-Hash != bbc2de2f…, G1/D2/Klippe halten, kein 5.97-m-Seitencrash). Nur mergen wenn alle Kriterien; sonst Zahlen + naechster isolierter Auftrag sofort.

## Stand 08.11. ~18:00 — p3d8 gegengeprüft, nicht gemergt; p3d9 startet
- p3d8 123408b unabhaengig in /tmp/gp_p3d8 (detached) neu gebaut: deterministisch, Pruefer/gen_relief/pruefe_*/neu/tests/Schwellen seit ad479b9 unveraendert (Adapter/delta.py identisch mit p3d6). Log gpt-6-luna/xhigh.
- Messung = Codex-Bericht (G1-Bild-SHA im Bericht falsch notiert, Datei pixelgleich zu p3d6): R3 D1 14 (p3d6 10, Ziel <=6), Kreuzung 152.5|28.5 Stufe 0.043 (p3d6 0.116), Endpunkt 156.5|37.5 Stufe 0.135 (p3d6 0.188), R8/R8a D1/G1 0. delta p3d6->p3d8 14 Anstiege (3 Gate: R3 laengs +4 / quer +2 / woelb +1), VAR0->p3d8 20. Adapter-Gates 570/39/336 (p3d6 563/39/336). pytest 26/5. max |Δh| D1 2.90825 m bei 148.0|29.5; 144.5|21.5 nur 0.002 m.
- Gehalten: t42u 0, Loch xvfb 0, D1-Hash bbc2de2f… -> d8d44ff9…, G1 38afeb30…, D2 749d3c4b… + Screenshot e8db06e6… bytegleich, Klippe 140|35 = 7.8840365 m, LOD1 134316.
- Nahbilder: Kreuzung flacher/tiefer, weich; Streiflicht ohne harte Stufe; Wandfuss Kerben bleiben; Wegende keine Treppe; G1/D2 pixelgleich.
- Ursache: LP-Plane Hc=4.012 m plus zusaetzliches plane_mix 4.8–8.0 m ueberschreibt die R3-Uebergaenge (rampe_2 s=-6: p3d6 7.189 -> 5.130, LP-Soll ~7.3). Fade-Mischung selbst ist korrekt (kein p3d7-Seitencrash).
- NICHT nach grundgeruest mergen.
- **p3d9** `/workspace/wt_dorfmap_p3d9` Branch `art/dorfmap-p3d9` Basis p3d8 123408b; Log `codex_jobs/log_p3d9.txt`, Ende `ende_p3d9.txt`, Start `starte_p3d9.sh`, Auftrag `job_p3d9.txt`; Log gpt-6-luna/xhigh, PID 1002037.

## Nach ende_p3d9 (Pruefschema)
Wie „Nach ende_p3d8“, mit /tmp/gp_p3d9 und Vergleich gegen die unabhaengige p3d6- und p3d8-Referenz (R3 D1 nicht >10, Ziel <=6; Kreuzung nicht >0.116 bzw. <=0.20; delta p3d6->p3d9 = 0 Gate-Anstiege; D1-Hash != d8d44ff9… und != bbc2de2f… / ad026456…; G1/D2/Klippe halten; kein Seitencrash). Nur mergen wenn alle Kriterien; sonst Zahlen + naechster isolierter Auftrag sofort.

## Stand 08.11. ~23:15 — p3d9 gegengeprueft, nicht gemergt; p3d10 laeuft
- p3d9 acc4e9f unabhaengig in /tmp/gp_p3d9 (detached) neu gebaut: deterministisch, Pruefer/gen_relief/pruefe_*/neu/tests/Schwellen unveraendert (Code-Diff p3d6->p3d9 nur neu/mesh.py). Log gpt-6-luna/xhigh.
- Messung = Codex-Bericht: R3 D1 laengs/quer/woelb 14/10/8 (p3d6 10/7/7, p3d8 14/9/8), R9w D1 22 (21), Kreuzung 152.5|28.5 Stufe 0.177 / Gitter 0.032 (p3d6 0.116/0, p3d8 0.043/0), Endpunkt 156.5|37.5 0.135. Gates 571/39/337. delta p3d6->p3d9 17 (4 Gate), p3d8->p3d9 14 (2 Gate: R3_quer +1, R9w +1), VAR0->p3d9 22. pytest 26/5.
- Gehalten: t42u 0, Loch xvfb 0, LOD1 134316, D1-Hash -> 3f196347…, G1 38afeb30…, D2 749d3c4b… + Screenshot e8db06e6…, Klippe 140|35 GB 7.8840365.
- Nahbilder: Kreuzung weich, aber feine Terrassenlinien (Facetten 317->362); Streiflicht/Wandfuss/Wegende ~p3d8; G1/D2 pixelgleich.
- Ursache: (A) lokales Fenster: MILP-Machbarkeit (codex_jobs/tools/p3d10_milp) zeigt, dass ebene Kreuzung (+-2 m, 0.05 m, <=3 %) plus R3 |lr|<=0.075 im +-16-m-Fenster bzw. mit max|dh|<=1 m unmoeglich ist; ueber die ganze Rampe minimal 2 (frei, Hc ~4.83) bzw. 3 (Wandseite rampe_11 ab s=40 fest, Hc ~4.11) verletzte Abschnitte -> R3 <=6 nur mit Ganzrampen-Profil machbar. (B) 2D-Transfer: Fade-Gewicht <1 auf dem Wegband, Mesh bis 0.40 m neben LP-Soll, neue R3_quer-Treffer.
- NICHT nach grundgeruest mergen.
- **p3d10** `/workspace/wt_dorfmap_p3d10` Branch `art/dorfmap-p3d10` Basis p3d8 123408b; Log `codex_jobs/log_p3d10.txt`, Ende `ende_p3d10.txt`, Start `starte_p3d10.sh`, Auftrag `job_p3d10.txt`; Log gpt-6-luna/xhigh, PID 1191708, Start 08.11. 23:14.

## Nach ende_p3d10 (Pruefschema)
Wie „Nach ende_p3d8“, mit /tmp/gp_p3d10 (detached) und Vergleich gegen die unabhaengigen Referenzen p3d6/p3d8/p3d9 (Skripte /tmp/gp_p3d9_run.sh, /tmp/gp_p3d9_render.sh als Muster; delta-Vorher: /tmp/gp_p3d6_out/after, /tmp/gp_p3d8_out/after2, /tmp/gp_p3d8_out/var0_before). Kriterien: R3 D1 laengs <=6, quer <=7, woelb <=7; Kreuzung <=0.116, Gitter <=0.02; Endpunkt <=0.20; R8/R8a D1/G1 0; R9w D1 <=21; delta p3d6->p3d10 0 Gate-Anstiege; Achse = Soll +-0.02 m (Bericht); D1-Hash != d8d44ff9/3f196347/bbc2de2f/ad026456; G1/D2/Klippe halten; kein Seitencrash; pytest >=26/5. Nur mergen wenn alle Kriterien; sonst Zahlen + naechster isolierter Auftrag sofort.
