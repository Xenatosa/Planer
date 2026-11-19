# Masken ohne Mesh (Vorlauf P4, Do 19.11.2026)

Erzeugt mit `python3 baue_masken.py --ohne-mesh --out masken_ohne_mesh` auf `art/dorfmap-fertig` @ bf9f62d (nach #61).
Ersetzt Fr durch den Lauf mit P2-Mesh (`hoehe.png`, Neigung in `begehbar`, F10, Brücken-Deck). Klassen-/Codes s. `../legende.json`.

| Quelle | Git-Blob |
|---|---|
| vektor/wege.geojson (P1a2 #59) | 0a636c339fa74b5a5a4dc87760b8cfb3277625cf |
| vektor/kreuzungen.geojson | f843bd8b6a3f7d1de165eeb6aefff4e1f8ec000d |
| vektor/wasser.geojson (#60) | fa9e4785485f0722fc4c2d1c66f8ae5fd72bf226 |
| vektor/ufer.geojson (#60) | 6e70128229a3b434dec5bbfa386f9757dc7a1e97 |
| vektor/zonen.geojson (#61) | 49d26955d706cd8ca71ab142a5313dcdb4040d49 |
| vektor/kanten.geojson, grat.geojson | nur Linien, nicht gerastert |

Gerastert werden nur Polygone mit `klasse` (zonen.geojson Flächentyp-Layer, wege.geojson Bänder mit Weg-Typ → 1) und `untergrund` (zonen.geojson).
`wasser.geojson`/`ufer.geojson`/`kreuzungen.geojson` haben kein `klasse`; ihr Inhalt steckt in den Flächentyp-Polygonen von zonen.geojson (#61), Kreuzungen zu 99,5 % als Weg gedeckt.

Dateien: `flaeche.png` (8 bit), `begehbar.png` (1 bit, nur Fläche), `untergrund.png` (8 bit), `weg_typ.png` (8 bit), `bauzone.png` (1 bit),
`slot_zonen.png` (8 bit), `masken_meta.json`, `abgleich_begehbar_3d.json`, `abgleich_slots.json`.
