# Abweichungen Modell ↔ c20 [F]

Entscheid t36u [F]: Modell muss c20 nicht 1:1 folgen. Lage von Senke, Wänden, Fluss, Ebenen bleibt erkennbar.
Raster und c20 unverändert; Abweichung je Zelle steht in `zellen_eigenschaften.csv` (`modell_hoehe_m`, `modell_abw_m`). Bild: `abweichungen_modell_vs_c20.png`.

| Nr | Abweichung [F] | Zellen [R] | Grund |
|---|---|---|---|
| A1 | Wandzellen als steile glatte Rampe (harmonisch gefüllt) statt senkrechter Säulen | 18 752 | Keine Streifen, freie Kamera |
| A2 | Wasser: Bett abgesenkt (SEE 1,5 / WASSER_FARBE 1,0 / BACH 0,5 / sonst 0,8 m [A]), Oberfläche 0,1 m unter Ufer | 6 695 | Wasser mit Tiefe |
| A3 | Freie Fläche geglättet (Gauß σ 1,5 [F]), Abw. > 0,25 m | 490 | Keine Treppenstufen |
| A4 | Sprung > 1 m ohne Wand → als Rampe gefüllt | 37 | Sonst Spitzen/Klippe ohne Wand |
| A5 | Sockel bis −14 m [A] rund um den Rand | – (zell_id −1) | Kein Blick ins Leere |

Zahlen [R]: freie Fläche Abw. max 2,65 m, 99 % ≤ 0,18 m; Wasser max 2,52 m.
