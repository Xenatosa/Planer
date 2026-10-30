# INDEX: gültige Dateien (Stand t32u, 30.10.2026)
Überholtes liegt in `_alt/`. Bilder in `pruefung/` mit älterem Präfix (t14u, t27u, t29u) bleiben hier, weil Overrides als Beleg auf sie verweisen.

## Daten (Hauptordner)
- `raster_c20_z25_zellen.csv`, `raster_c20_z50_zellen.csv`: Zellraster mit 39 Spalten, Schema in `schema_zelle.json`.
- `raster_c20_z25_meta.json`, `raster_c20_z50_meta.json`: Zählungen.
- `raster_c20_z25_overlay_plaetze_wege.csv` (und z50): Plätze, Wege, Furten als Overlay.
- `overrides_t12u.csv`: alle Handkorrekturen mit Beleg. `overrides_c20_z25.csv` ist eine Hilfsliste.
- Text: `SPEC.md`, `BAUPLAN_E100.md`, `PRUEFPROTOKOLL.md`, `UEBERGABE.md`.
- Skripte: `gen_raster.py`, `gen_overlay_e100.py`, `gen_bauzone_befund.py`, `pruef_plaetze_quellen.py`.

## Gültige Vorschaubilder
- `raster_c20_z25_vorschau.png`, `_bebaubar.png`, `_overlay.png`, `_vergleich.png`, `_hoehe_fluss.png`, `_overlay_plaetze_wege.png` (jeweils auch für z50)
- `pruefung/t26u_overlay_E16/E40/E70/E100.png`: Plätze je Epoche
- `pruefung/t29u_bebaubar_erweitert_E100.png`
- `pruefung/t33u_ebenen_vollstaendig.png`: alle 101 808 Zellen in Ebenenfarbe mit Legende (ersetzt t31u/t30u_ebenen, Skript gen_ebenen_bild.py)
- `pruefung/t29u_kacheln_r5_*` und `pruefung/t30u_kacheln_r5_*`: Kachelbögen über die ganze Karte (ersetzen kacheln_r4/r5)
- Belege t31u: `pruefung/t31u_talsued_a/b.png`, `t31u_findling_4x_0/1.png`, `t31u_z50_gipfel.png`, `t31u_z50_sand_w/m/o.png`
- Belege t29u/t30u: `t29u_zoom_*`, `t29u_rand_*`, `t29u_splitter_c20.png`, `t29u_fluss_schollen.png`, `t30u_findling_treffer.png`, `t30u_linie_cx190.png`
- Belege t14u und t27u: Overrides an Felshaufen, Flusseis und Schneebäumen; Brücken X069/X084

## Prüflisten
- `pruefung/t26u_*.csv` und `t26u_zusammenfassung.json` gelten aktuell.
- `pruefung/t16u_plaetze_gegen_bebaubar.csv/.json` sind Eingabe für `gen_bauzone_befund.py`.
