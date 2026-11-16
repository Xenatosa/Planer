# P10 Vertex-Hash-Vergleich D1/G1/D2: index.html vs. alle_kacheln.html

Referenz: `index.html` (Kacheln D1, G1, D2) · Neu: `/tmp/p10/alle_kacheln.html` (56 Kacheln)

Verglichen im gerenderten Three.js-Szenengraph (Ebene `gelaende`): SHA-256 der Weltkoordinaten (Float32, matrixWorld angewendet) und der Indizes je Mesh (Oberfläche, Seiten, Boden).

**Ergebnis: alle identisch**

| Kachel | Teil | identisch | Vertices | pos_sha256 (Ref) | pos_sha256 (Neu) | idx identisch | Farbe identisch |
|---|---|---|---|---|---|---|---|
| D1 | surface | ja | 7395 | `663e935a5f8b53c8…` | `663e935a5f8b53c8…` | ja | ja |
| D1 | sides | ja | 1360 | `48b61c1b6d1b589a…` | `48b61c1b6d1b589a…` | ja | ja |
| D1 | bottom | ja | 7395 | `110e2ff11c02fcd4…` | `110e2ff11c02fcd4…` | ja | ja |
| G1 | surface | ja | 7395 | `76dbe941cc3be01c…` | `76dbe941cc3be01c…` | ja | ja |
| G1 | sides | ja | 1360 | `99ddcb7db922b0f2…` | `99ddcb7db922b0f2…` | ja | ja |
| G1 | bottom | ja | 7395 | `b6ed71c46935a0e2…` | `b6ed71c46935a0e2…` | ja | ja |
| D2 | surface | ja | 7395 | `ebeb46a15c25bce0…` | `ebeb46a15c25bce0…` | ja | ja |
| D2 | sides | ja | 1360 | `6835acf26107fbe7…` | `6835acf26107fbe7…` | ja | ja |
| D2 | bottom | ja | 7395 | `b33d5a64c686ce3f…` | `b33d5a64c686ce3f…` | ja | ja |

Zusätzlich im Build (Python): `neu.mesh.build_manifest()` erzeugt D1/G1/D2 erneut aus `relief_daten.json.gz`; Kontrolle mit `neu.mesh.tile_mesh()`: {'D1': True, 'D2': True, 'G1': True}.

Nahtprüfung (gemeinsame Randvertices benachbarter Kacheln): 97 Paare, max. Höhendifferenz 0.0 m.

## Mesh-Hashes aller 56 Kacheln (Paket)

| Kachel | Verfahren | surface_mode | Dreiecke | mesh_sha256 |
|---|---|---|---|---|
| A1 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `559a1109b201ac67…` |
| A2 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `9dd2fcf6d3f5fa8d…` |
| A3 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `0088cc908a6d5291…` |
| A4 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `366604829eedbffe…` |
| A5 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `2c85856586744deb…` |
| A6 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `a1f1d4479d851e3a…` |
| A7 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `3b2097f1c8287210…` |
| B1 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `33de94343ae5b5e0…` |
| B2 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `116f8832c7795a74…` |
| B3 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `0adf007d49fe7253…` |
| B4 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `3d2afc1172b7aadb…` |
| B5 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `69277326f12cde02…` |
| B6 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `aea2d162c34c9a24…` |
| B7 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `c74003f809dc8310…` |
| C1 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes+terrain_extensions | 14448 | `45b3840ce7ea56e4…` |
| C2 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `3eea14f7f71763e5…` |
| C3 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `c0c2eaf675e1c69a…` |
| C4 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `b91ef62aab69af1f…` |
| C5 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `c9772ed1812e62b7…` |
| C6 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `e95392fbe8a664c2…` |
| C7 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `459f83f06277cbd5…` |
| D1 | neu.mesh.build_manifest (Prototyp) | GB_with_local_profiles | 14448 | `924d57ae784760cf…` |
| D2 | neu.mesh.build_manifest (Prototyp) | locked_visible_GB_bytes | 14448 | `cbaaa85b2716137a…` |
| D3 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `f7e4ec3a05953caa…` |
| D4 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `215dee0266294c8d…` |
| D5 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `484146b3ddbe80f1…` |
| D6 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `e5c2b2ef4c814ef2…` |
| D7 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `b8cbe1d7158522f1…` |
| E1 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `f868bd6880efa71f…` |
| E2 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `90ef7e44fcdf27df…` |
| E3 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `18b4cb896a6574df…` |
| E4 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `2f04b62a3323a0d4…` |
| E5 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `b88adb03a83fba7d…` |
| E6 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `95707ffcce8763df…` |
| E7 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `24b72ccf64728bd3…` |
| F1 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `254bf4fb01b223ef…` |
| F2 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `d8552f593f1aa69c…` |
| F3 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `2882b5438dfcc585…` |
| F4 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `3cc5326de8d7ae0d…` |
| F5 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `8097e10ca10a1272…` |
| F6 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `802fb6bf5ca9c8f7…` |
| F7 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `945bd40ad5e49d09…` |
| G1 | neu.mesh.build_manifest (Prototyp) | GB_with_local_profiles | 14448 | `91609b79150f323e…` |
| G2 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `c00b862482a623ba…` |
| G3 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `85d71463130d480c…` |
| G4 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `b788a4089e47b28a…` |
| G5 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `80529032172d654d…` |
| G6 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `eb76ab0caa9f4eca…` |
| G7 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `e36d347fba3fa8ed…` |
| H1 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `f8dd46379a884028…` |
| H2 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `067ab339a805aa25…` |
| H3 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `8ce60c78a3dd3269…` |
| H4 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `35f3d79426bda8d0…` |
| H5 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `273a8eba9a2a9df9…` |
| H6 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `8a982ef1365c6a62…` |
| H7 | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `428884c74b6442f9…` |
