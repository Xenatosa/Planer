# Anschluss t139u (nicht stillstehen)

Stand HEAD nach Grundlagen-Merge: siehe `git log -1` auf art/dorfmap-grundgeruest.
Legacy-Gate unveraendert 570/48/334=952, Loch 0, t42u 0. Mesh der Legacy-Pipeline unveraendert (kein Fortschritt am 3D-Mesh behaupten).

## Laufen jetzt
- Codex `art/dorfmap-pgelaende` Worktree `/workspace/wt_dorfmap_pgelaende`, Log `/workspace/codex_jobs/log_pgelaende.txt`, Ende-Marker `ende_pgelaende.txt`
- Codex `art/dorfmap-pwand` Worktree `/workspace/wt_dorfmap_pwand`, Log `/workspace/codex_jobs/log_pwand.txt`, Ende-Marker `ende_pwand.txt`
- Config und effektive Logs: model gpt-6-luna, reasoning effort xhigh

## Sobald ende_*.txt da ist
1. Bericht `pruefung/ERGEBNIS_<tag>.md` lesen; gegenpruefen: Quellspalten-Diff 0, t42u 0, D2 bytegleich ohne Referenz-Reset, keine Regel +>5, Delta bricht bei Anstieg.
2. Raycast + Gate kartenweit auf dem Worktree.
3. Alle Nahbilder D1/G1/D2 (Ton+betroffene) persoenlich ansehen — Stichprobe reicht nicht als Endurteil; vor Lieferung spaeter alle 56.
4. Pruefen dass RELIEF_NEU=1 wirklich neues 3D-Mesh im Viewer zeigt (nicht nur 2D/Diagnostik).
5. Einzeln mergen nach Gate, pushen, Status in runde_o_status.md.
6. Danach naechste Schichten/Details nur wenn D2/G1/D1 Gate 0 und Nahbilder gut; sonst Zahlen melden (kein Fabian-Kontakt).

## Nicht tun
- Keine Legacy-Flicken mehr.
- Nichts loeschen ohne ausdrueckliches Ja von Fabian.
- Keine Nachricht an Fabian.

## Gegenpruefung pgelaende/pwand (06.11.2026 ~08:30 MEZ, Grok Bot)
- pgelaende 80de512: Quellspalten-Diff 0, t42u 0, D2 bytegleich, pr/r8/r9 570/48/334 (+0 je Regel), Lochscan frisch unter xvfb-run 0 offen (1.700.454 Dr., index.html und neu/index.html). ABER: Standard Variante 0 = pixelgleich zur Legacy; main.js schreibt nur Hoehen ins alte Feld G, kein eigenes sichtbares Mesh, Profil nicht aktiv. Schritt 4 nicht bestanden -> NICHT gemergt.
- pwand cc9e42e: t42u 0, D2 bytegleich, 570/48/334, Lochscan legacy 0, neu (index.html) 0 bei 44.704 Dr.; neu/index.html-Scan Node-Fehler. Nahbilder selbst angesehen: D1/G1-Gelaende fast flache Ebene, Klippe D1 ~140|35 verloren, Waende kantige Brett-Extrusionen; test_beanstandungen 7/7 rot; Legacy-Build aendert index.html. -> NICHT gemergt.
- Folgelauf: Codex p3d (gpt-6-luna/xhigh im Log bestaetigt), Branch art/dorfmap-p3d, Worktree /workspace/wt_dorfmap_p3d, Skript codex_jobs/starte_p3d.sh, Log log_p3d.txt, Ende ende_p3d.txt. Einzige Integration: merged pgelaende+pwand, eigenes D1/G1-Mesh mit Relief, gerundete Wandkontur, Profil aktiv, D2 bytegleich.
- Bei ende_p3d.txt: Schritte 1-6 oben erneut.
