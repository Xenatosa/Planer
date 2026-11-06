# Plan: echte 3D-Welt (t39u)

Stand: Prototyp `modell3d/welt3d/index.html` – Gelände + Platzhalter-Objekte aus Daten, freie Kamera, Gehen.

## Was fehlt
1. **Höhenkarte** gemalt/gemessen statt geschätzt [A]; Wandhöhen je Wand.
2. **3D-Assets je Epoche** (E1…E100): Häuser je Typ (Hütte, Standard, Turmhaus, Funktion…), Bäume (2–3 Arten), Felsen, Findlinge, Brücke, Zaun, Deko. Stil-Vorgabe (low-poly? Maßstab, Polygon-Budget).
3. **Texturen/Skins** je Untergrund (Schnee, Fels-Wand von der Seite, Wald-Boden, Eis), nahtlos; c20 ist Aufsicht und taugt für Wände nicht.
4. **Gültiger Bauplan mit Polygonen** (v4b statt v8) für die Gebäude-Plätze.
5. **Unity-Pipeline**: GLB-Import, Terrain oder Mesh, Prefabs je Asset, Platzierung per CSV/JSON wie hier.
6. **Kamera-Regeln**: Grenzen (nicht unter den Boden?), Zoom-Bereich, Gehen ja/nein, Kollision.
7. **Performance Handy**: Instancing, LOD, Schatten-Budget, Ziel z. B. 30 fps, < 100 k Dreiecke sichtbar [A].

## Reihenfolge und Aufwand [A]
| # | Schritt | Wer | Aufwand |
|---|---|---|---|
| 1 | Offene Fragen klären (unten) | Fabian | 1 Gespräch |
| 2 | Höhenkarte + Wandhöhen | Art | 1–2 Tage |
| 3 | Bauplan v4b-Polygone exportieren | Wege-Bot | 0,5 Tag |
| 4 | Asset-Liste + Stilprobe (1 Haus, 1 Baum, 1 Fels) | Art | 2–3 Tage |
| 5 | Texturen je Untergrund | Art | 2 Tage |
| 6 | Unity-Szene mit Platzierung aus Daten | Dev | 2–3 Tage |
| 7 | Handy-Test + Optimierung | Dev | 2 Tage |

## Offene Fragen
1. Stil: low-poly oder detailliert/gemalt wirkend?
2. Darf die Kamera unter/hinter alles (wie hier) oder nur schräg von oben?
3. Gehen auf Bodenhöhe im Spiel: ja/nein?
4. Gilt Bauplan v4b (203 Plätze E40) oder der v8-Plan (233)?
5. Zielgeräte und Mindest-fps?
