# P10b Vertex-Hash-Vergleich D1/G1/D2: index.html vs. alle_kacheln.html

Referenz: `index.html` (Kacheln D1, G1, D2) · Neu: `/tmp/p10b/alle_kacheln.html` (56 Kacheln)

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

Wandkörper (Ebene `waende`):

| Kachel | in index.html | im neuen HTML | identisch | pos_sha256 |
|---|---|---|---|---|
| D1 | ja | ja | ja | `8ea133b816a8804d` |
| G1 | ja | ja | ja | `b2e5783541653133` |
| D2 | nein | nein | ja | `-` |

Zusätzlich im Build (Python): `neu.mesh.build_manifest()` erzeugt D1/G1/D2 erneut aus `relief_daten.json.gz`; Kontrolle mit `neu.mesh.tile_mesh()`: {'D1': True, 'D2': True, 'G1': True}.

Nahtprüfung (gemeinsame Randvertices benachbarter Kacheln): 97 Paare, max. Höhendifferenz 0.0 m.

## Mesh-Hashes aller 56 Kacheln (Paket)

| Kachel | Bounds | Verfahren | surface_mode | Dreiecke | mesh_sha256 |
|---|---|---|---|---|---|
| A1 | [0, 0, 42, 43] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `559a1109b201ac67…` |
| A2 | [0, 43, 42, 86] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `9dd2fcf6d3f5fa8d…` |
| A3 | [0, 86, 42, 129] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `0088cc908a6d5291…` |
| A4 | [0, 129, 42, 172] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `366604829eedbffe…` |
| A5 | [0, 172, 42, 215] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `2c85856586744deb…` |
| A6 | [0, 215, 42, 258] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `a1f1d4479d851e3a…` |
| A7 | [0, 258, 42, 303] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 15120 | `fc17e51e02aac025…` |
| B1 | [42, 0, 84, 43] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `33de94343ae5b5e0…` |
| B2 | [42, 43, 84, 86] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `116f8832c7795a74…` |
| B3 | [42, 86, 84, 129] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `0adf007d49fe7253…` |
| B4 | [42, 129, 84, 172] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `3d2afc1172b7aadb…` |
| B5 | [42, 172, 84, 215] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `69277326f12cde02…` |
| B6 | [42, 215, 84, 258] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `aea2d162c34c9a24…` |
| B7 | [42, 258, 84, 303] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 15120 | `c68882206c53bcba…` |
| C1 | [84, 0, 126, 43] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes+terrain_extensions | 14448 | `45b3840ce7ea56e4…` |
| C2 | [84, 43, 126, 86] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `3eea14f7f71763e5…` |
| C3 | [84, 86, 126, 129] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `c0c2eaf675e1c69a…` |
| C4 | [84, 129, 126, 172] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `b91ef62aab69af1f…` |
| C5 | [84, 172, 126, 215] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `c9772ed1812e62b7…` |
| C6 | [84, 215, 126, 258] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `e95392fbe8a664c2…` |
| C7 | [84, 258, 126, 303] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 15120 | `c044592007bfb3ec…` |
| D1 | [126, 0, 168, 43] | neu.mesh.build_manifest (Prototyp) | GB_with_local_profiles | 14448 | `924d57ae784760cf…` |
| D2 | [126, 43, 168, 86] | neu.mesh.build_manifest (Prototyp) | locked_visible_GB_bytes | 14448 | `cbaaa85b2716137a…` |
| D3 | [126, 86, 168, 129] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `f7e4ec3a05953caa…` |
| D4 | [126, 129, 168, 172] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `215dee0266294c8d…` |
| D5 | [126, 172, 168, 215] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `484146b3ddbe80f1…` |
| D6 | [126, 215, 168, 258] | neu.mesh.terrain_heights + tile_mesh auf GB | locked_visible_GB_bytes+wegprofil | 14448 | `3508afb0bf250ef5…` |
| D7 | [126, 258, 168, 303] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 15120 | `57a43c6bd5452c95…` |
| E1 | [168, 0, 210, 43] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `f868bd6880efa71f…` |
| E2 | [168, 43, 210, 86] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `90ef7e44fcdf27df…` |
| E3 | [168, 86, 210, 129] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `18b4cb896a6574df…` |
| E4 | [168, 129, 210, 172] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `2f04b62a3323a0d4…` |
| E5 | [168, 172, 210, 215] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `b88adb03a83fba7d…` |
| E6 | [168, 215, 210, 258] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `95707ffcce8763df…` |
| E7 | [168, 258, 210, 303] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 15120 | `b86fc422b934474d…` |
| F1 | [210, 0, 252, 43] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `254bf4fb01b223ef…` |
| F2 | [210, 43, 252, 86] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `d8552f593f1aa69c…` |
| F3 | [210, 86, 252, 129] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `2882b5438dfcc585…` |
| F4 | [210, 129, 252, 172] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `3cc5326de8d7ae0d…` |
| F5 | [210, 172, 252, 215] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `8097e10ca10a1272…` |
| F6 | [210, 215, 252, 258] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `802fb6bf5ca9c8f7…` |
| F7 | [210, 258, 252, 303] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 15120 | `180c4394a1a1fc64…` |
| G1 | [252, 0, 294, 43] | neu.mesh.build_manifest (Prototyp) | GB_with_local_profiles | 14448 | `91609b79150f323e…` |
| G2 | [252, 43, 294, 86] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `c00b862482a623ba…` |
| G3 | [252, 86, 294, 129] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `85d71463130d480c…` |
| G4 | [252, 129, 294, 172] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `b788a4089e47b28a…` |
| G5 | [252, 172, 294, 215] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `80529032172d654d…` |
| G6 | [252, 215, 294, 258] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `eb76ab0caa9f4eca…` |
| G7 | [252, 258, 294, 303] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 15120 | `f2dafbf7d50a2d7a…` |
| H1 | [294, 0, 336, 43] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `f8dd46379a884028…` |
| H2 | [294, 43, 336, 86] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `067ab339a805aa25…` |
| H3 | [294, 86, 336, 129] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `8ce60c78a3dd3269…` |
| H4 | [294, 129, 336, 172] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `35f3d79426bda8d0…` |
| H5 | [294, 172, 336, 215] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `273a8eba9a2a9df9…` |
| H6 | [294, 215, 336, 258] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 14448 | `8a982ef1365c6a62…` |
| H7 | [294, 258, 336, 303] | neu.mesh.tile_mesh auf GB (wie D2) | locked_visible_GB_bytes | 15120 | `05f95cc5fca44bf2…` |
