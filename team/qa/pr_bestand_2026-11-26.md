# PR-Bestandsaufnahme Xenatosa/epodarien — 26.11.2026

**Auftrag:** New Bot, 26.11.2026 08:03 MEZ, an Epochen QA.  
**Methode:** nur lesend (kein Merge, kein Schließen, kein Kommentar, kein Push in epodarien). GitHub als Xenatosa (`gh`, Stand 26.11.2026 08:04–08:15 MEZ).  
**Offene PRs:** 46. Default-Basis ist `main`, Abweichungen sind genannt.  
**Kritiker:** Gemeint ist Epochen Kritiker (Dateien unter `team/kritik/`, ggf. als PR-Review von Xenatosa gespiegelt). Das Bot-Konto `quinn-at-outlook[bot]` ist ein statisches Code-Review und ausdrücklich keine Freigabe.  
**Queue-Datei:** nicht im Planer-Repo unter `team/`, sondern `/workspace/uploads/codex_queue.md` (Verweis in `team/TEAM.md` und `team/entscheidungen.md`). Im Arbeitsbaum von `/workspace/handygame-plan` lag eine stark veränderte, nicht committete Arbeitskopie; deshalb wurde nur `git fetch origin` ausgeführt, kein `git pull`, der lokale Änderungen verworfen hätte.  
**Kosten Erstfassung:** 08:04–08:18 MEZ, 0 € (ohne Codex). Korrektur und Codex-Pakete: siehe Kostenzeile am Ende und die Korrektur-Zeile in der Kurzfassung.

## Kurzfassung

**Korrektur 26.11.2026 08:31 MEZ:** In der Erstfassung (08:04–08:18 MEZ) bedeutete „Checks grün“ bei den meisten PRs nur 2× Job „Geheimnisse suchen“ (Gitleaks, je einmal für `push` und `pull_request`). Ein Unity-Lauf (EditMode + PlayMode) steckt nicht darin. Ursache ist nicht ein paths-Filter: In `.github/workflows/android.yml` auf `main` gibt es **keinen `paths:`-Block**. Der Workflow startet nur bei `workflow_dispatch` (Z. 32–37) oder bei `push` auf die Branches `main`, `cursor/**`, `gameplay/**`, `ui/**`, `ci/self-hosted-all` (Z. 38–44). Der Dateikopf sagt ausdrücklich, dass Pull Requests ihn nicht starten (Z. 7–8). Deshalb laufen EditMode/PlayMode nicht, wenn der Head-Branch nur unter `data/`, `nova/`, `tests/`, `quests/`, `art/`, `research/` u. a. liegt. Gitleaks läuft dagegen bei Push/PR (mit `paths-ignore` nur für Medien, `.github/workflows/gitleaks.yml`). Server-Jobs nur bei Änderungen unter `server/**`.

Empfehlungen, die auf diesem „grün“ beruhten, sind angepasst: **#161, #160, #159, #158, #123, #165**. **#57** hatte New Bot als Beispiel ohne Unity-Lauf genannt; das trifft nicht zu: Branch `cursor/**` hat EditMode + PlayMode SUCCESS (APK/Emulator skipped).

Kritiker-Notiz 26.11.2026 (lokal `team/kritik/PRUEFNOTIZ_prs_159_160_161_2026-11-26.md`; nach `git fetch` nicht auf `origin/main` und keinem anderen Remote-Branch gefunden, unversionierte Arbeitsdatei, mtime 08:25 MEZ): **#161 Note 3/10** (6 Muss, davon 3 Compile-Fehler), **#159 und #160 je 9/10** (Muss leer, Sollte offen). **#155 ist vollständig in #158 enthalten.**

- Fachlich am ehesten mergebereit bleibt **#158** (Kritiker 10/10, Quest/Doku, #155 vollständig enthalten). Die Checks dazu waren nur Gitleaks, kein Unity; das ändert die fachliche Freigabe nicht, darf aber nicht als Test-Grün gelesen werden. **#161, #160, #159 sind nicht mergebereit**, solange die Punkte aus der Notiz offen sind.
- **#109** (Beschwörungsvergleich): Die vier Kritiker-Auflagen vom 17.10. sind in den Kernpunkten (P7-Werte, Featured ohne 50/50, PvP-Deckel als Beschluss) erfüllt. Offen bleiben die niedrig priorisierte Ergänzung Whiteout Survival / Last War, die spätere Präzisierung „deckeln, nicht komplett angleichen“ (Wortlaut noch vermischt), der fehlende Kritiker-Recheck und der nie geschriebene PR-Kommentar. **Nicht sofort mergen.**
- Die Behauptung „Queue-Zeile 10, nichts gepusht“ ist **für den Git-Stand falsch**. Drei Commits landeten am 17.10.2026 08:17:51–08:18:28 MESZ auf dem PR-Branch, 2–3 Minuten nach Job-Start 08:15. Die Queue-Zeile blieb auf `[GESTARTET]` und wurde nie `[ERLEDIGT]`; das ist die wahrscheinlichste Quelle der Fehleinschätzung. Siehe Abschnitt P7-Ursache.
- Häufigste Check-Ursachen sind Infrastruktur, nicht der Diff: Runner 24 h nicht zugewiesen (CANCELLED), Billing/Spending-Limit, Artifact-Speicherquota. Echte Code-Fehler sind belegt bei **#156** (Compiler, Unity-Exit 1), **#161** (drei Compile-Fehler plus drei falsche Assertions, von Epochen Kritiker am 26.11. gelesen, Unity nie gelaufen), vermutlich **#85/#62** (Unity-Exit 1) und **#88** (Gitleaks Exit 1, ohne Billing-Text).
- Sieben PRs haben Merge-Konflikte mit der Basis (`DIRTY`): **#102, #101, #100, #85, #76, #62, #60**.
- Stapeln: `#151 → #152 → #162 → #164` (D2-Menüs). `#108` sitzt auf dem Head von `#88`. `#110` zielt nicht auf `main`, sondern auf `cursor/rechtsrecherche-play-e9e7`.
- Backend-Reihenfolge laut Queue-Kopf: zuerst **#66**, dann **#91**, dann **#67** (alle Draft, Gitleaks + Server-Jobs grün, kein Unity, weit hinter `main`).
- Viele PRs vom 13.–17.10. sind 40+ Tage offen und 68–111 Commits hinter `main`. Das allein ist kein Schließgrund, aber Merge ohne Einholen von `main` ist riskant.

## Liste der offenen PRs

### [#165](https://github.com/Xenatosa/epodarien/pull/165) — Dorfkarte E1: konfiguriertes 5x4 Chunk-Raster
- **Branch:** `art/dorfkarte-e1-chunkraster-v1` → `main` (10 voraus, 0 hinter, `MERGEABLE`/`CLEAN`)
- **Alter:** 31 Tage (erstellt 26.10.2026 08:26 MEZ, zuletzt 06.11.2026 10:13 MEZ)
- **Checks:** nur 2× Gitleaks SUCCESS (push + pull_request). Kein Unity-Lauf — Branch `art/**` steht nicht in android.yml Z. 38–44; der Diff umfasst aber Code und viele Assets (289 Dateien).
- **Kritiker:** keine Epochen-Kritiker-Datei. Quinn: statisch „sauber, keine Blocker“, Freigabe liege beim Chef.
- **Duplikat/überholt:** nicht belegt. Die spätere Dorfmap-Arbeit (detail_v2) liegt vor allem im Planer-/Art-Zweig; ob dieses Unity-Chunk-Raster noch der aktuelle Integrationsweg ist, ist hier nicht entschieden.
- **Empfehlung:** fixen — nicht mergen allein wegen „grün“ (nur Gitleaks). Zuerst EditMode/PlayMode nachholen (z. B. `workflow_dispatch` auf dem Branch oder Push nach `ci/self-hosted-all`) und klären, ob der E1-Chunk-Stand nach der November-Dorfmap noch gewollt ist.

### [#164](https://github.com/Xenatosa/epodarien/pull/164) — UI: Einstellungen-Inhalte datengetrieben (Allgemein/Konto, DE/EN)
- **Branch:** `ui/menus-d2-einstellungen-inhalte` → `ui/menus-d2-einstellungen-geruest` (#162; 1 voraus, 0 hinter, `MERGEABLE`/`UNSTABLE`)
- **Alter:** 33 Tage (erstellt 24.10.2026 10:19 MESZ, zuletzt 06.11.2026 06:12 MEZ)
- **Checks:** rot/abgebrochen: EditMode + PlayMode und 2× „Geheimnisse suchen“ CANCELLED — Job hat 24 h auf einen Runner gewartet.
- **Kritiker:** nicht geprüft. Quinn: solide, Testbestätigung offen bis CI grün.
- **Duplikat/überholt:** nein; oberstes Glied der D2-Menü-Kette.
- **Empfehlung:** fixen — nach Merge der Basis (#151/#152/#162) Checks neu laufen lassen (Runner), dann mergen.

### [#162](https://github.com/Xenatosa/epodarien/pull/162) — UI: Einstellungen-Gerüst (15. D2-Menü, Tabs Allgemein/Konto)
- **Branch:** `ui/menus-d2-einstellungen-geruest` → `ui/menus-d2-geruest` (#152; 1 voraus, 0 hinter, `MERGEABLE`/`UNSTABLE`)
- **Alter:** 33 Tage (erstellt 24.10.2026 06:12 MESZ, zuletzt 06.11.2026 06:12 MEZ)
- **Checks:** rot/abgebrochen: EditMode + PlayMode und „Geheimnisse suchen“ CANCELLED (24 h kein Runner).
- **Kritiker:** nicht geprüft. Quinn: fokussiert und sauber, keine Blocker aus dem Diff.
- **Empfehlung:** fixen — Basis-Kette mergen, Checks wiederholen, dann mergen.

### [#161](https://github.com/Xenatosa/epodarien/pull/161) — test: Grundlagen-EditMode-Tests ergänzt
- **Branch:** `tests/qci-grundlagen-editmode-2310` → `main` (1 voraus, 0 hinter, `MERGEABLE`/`CLEAN`)
- **Alter:** 33 Tage (erstellt 23.10.2026 21:17 MESZ, zuletzt 10.11.2026 18:23 MEZ)
- **Checks:** nur 2× Gitleaks SUCCESS. Kein Unity-Lauf — Branch `tests/**` steht nicht in android.yml Z. 38–44. Compile und EditMode sind nie gelaufen.
- **Kritiker:** geprüft 26.11.2026, **Note 3/10** (`team/kritik/PRUEFNOTIZ_prs_159_160_161_2026-11-26.md`, Head `b6fe0b39`). Muss M-1–M-6: CS0104, CS1503, CS0102 sowie falsche Erwartungen bei Winter-Nahrung (1259 statt 1260), Unterhalt (Army nie befüllt) und `starter`. S-1: Trigger `tests/**` oder Lauf auf `ci/self-hosted-all`. Quinn-Review ist damit überholt.
- **Empfehlung:** fixen — M-1 bis M-6 beheben, Erwartungen gegen `data/` und GDD v1.7.17 prüfen, S-1 umsetzen, danach Unity-Lauf und Kritiker-Recheck (Pakete unter `team/qa/vorschlaege_lead_dev/`). Nicht mergen.

### [#160](https://github.com/Xenatosa/epodarien/pull/160) — docs: Abgleich Grundlagen 23.10.
- **Branch:** `nova/abgleich-grundlagen-2310` → `main` (1 voraus, 0 hinter, `MERGEABLE`/`CLEAN`)
- **Alter:** 33 Tage (erstellt 23.10.2026 20:25 MESZ, zuletzt 11.11.2026 14:17 MEZ)
- **Checks:** nur 2× Gitleaks SUCCESS. Kein Unity-Lauf — Branch `nova/**` steht nicht in android.yml Z. 38–44 (für reine Doku fachlich entbehrlich, darf aber nicht als Test-Grün gelten).
- **Kritiker:** geprüft 26.11.2026, **Note 9/10** (Notiz wie bei #161, Head `bec9d5bb`). Muss leer. Sollte S-1–S-5: Quelle/Stand auf GDD v1.7.17, Satz zu #155/#158 aktualisieren, `Apply`/validate_quests/Datumszeile präzisieren.
- **Empfehlung:** fixen — Sollte-Punkte einarbeiten, dann mergen möglich. Nicht auf das Gitleaks-Grün stützen.

### [#159](https://github.com/Xenatosa/epodarien/pull/159) — data: ranking_rewards_fallback shards → 0
- **Branch:** `data/ranking-fallback-shards-zero` → `main` (1 voraus, 0 hinter, `MERGEABLE`/`CLEAN`)
- **Alter:** 33 Tage (erstellt 23.10.2026 20:15 MESZ, zuletzt 11.11.2026 14:17 MEZ)
- **Checks:** nur 2× Gitleaks SUCCESS. Kein Unity-Lauf — Branch `data/**` steht nicht in android.yml Z. 38–44. Kein Check berührt die CSV.
- **Kritiker:** geprüft 26.11.2026, **Note 9/10** (Head `39c66e93`). Muss leer. Inhalt passt zu GDD v1.7.17 Z. 6140 / R.4.7. Sollte S-1–S-3: CRLF→LF im Diff nennen oder Zeilenenden behalten, Quelle auf v1.7.17 Z. 6140 (G3 offen) setzen, Importer-/Validate-Lauf vor Merge nennen.
- **Empfehlung:** fixen — Sollte-Punkte einarbeiten, dann mergen möglich. Nicht auf das Gitleaks-Grün stützen.

### [#158](https://github.com/Xenatosa/epodarien/pull/158) — quests: Epoche 1 K1–K3 — Quest-System v2, Timeline, Story-Romane
- **Branch:** `quests/kampagne-e1-k1-k3` → `main` (15 voraus, 0 hinter, `MERGEABLE`/`CLEAN`)
- **Alter:** 33 Tage (erstellt 23.10.2026 16:33 MESZ, zuletzt 11.11.2026 18:25 MEZ)
- **Checks:** nur 2× Gitleaks SUCCESS. Kein Unity-Lauf — Branch `quests/**` steht nicht in android.yml Z. 38–44. Der Diff ist Doku/Questtexte, kein C#.
- **Kritiker:** geprüft ja, Note 10/10 (Recheck 6, 23.10., `team/kritik/review_quest_timeline_e1_k1_k3.md`, HEAD `fbe7dcd`). Muss/Sollte geschlossen. Nachtrag 26.11.: #155 ist vollständig in diesem Head enthalten (alle 3 Commits und 8 Dateien von #155 sind Vorfahren bzw. byte-gleich; Notiz 26.11.).
- **Duplikat/überholt:** überlappt thematisch mit dem älteren Entwurf #155; #158 ist der jüngere, geprüfte Stand.
- **Empfehlung:** mergen als Quest-/Doku-Stand (Kritiker 10/10, #155 vollständig enthalten). Die Checks waren nur Gitleaks, kein Unity; das ist hier kein Blocker, weil kein Spielcode im Diff liegt. Merge-Commit bevorzugen, damit GitHub #155 als aufgegangen erkennt; andernfalls #155 danach als überholt schließen (nur auf Anweisung).

### [#157](https://github.com/Xenatosa/epodarien/pull/157) — campaign: Story-v2-Bosse statt GDD-E1-Bosse
- **Branch:** `campaign/story-v2-bosse` → `main` (1 voraus, 0 hinter, `MERGEABLE`/`CLEAN`)
- **Alter:** 34 Tage (erstellt 23.10.2026 07:08 MESZ, zuletzt 11.11.2026 18:25 MEZ)
- **Checks:** nur 2× Gitleaks SUCCESS. Kein Unity-Lauf (`campaign/**` steht nicht in android.yml Z. 38–44). Review-Entscheidung: `CHANGES_REQUESTED` (Quinn).
- **Kritiker:** keine eigene Kritikdatei zu #157. Quinn und ein Kampfreview (Kommentar Xenatosa, 10.11.2026) nennen denselben Blocker: `maps.csv` nutzt `boss_e1_knirsch` usw., die Wellen bleiben bei `unit_boss_*`; `AutoBattleSimulator.FindMappedBoss` matcht nicht, Bosse und Phasen greifen nicht.
- **Empfehlung:** fixen — Boss-ID-Namespace in Maps/Wellen/Simulator angleichen, danach Review aufheben und mergen.

### [#156](https://github.com/Xenatosa/epodarien/pull/156) — Dorf-HUD D2 erste Stufe
- **Branch:** `ui/hud-d2-dorf` → `main` (30 voraus, 4 hinter, divergiert, `MERGEABLE`/`UNSTABLE`)
- **Alter:** 34 Tage (erstellt 23.10.2026 06:57 MESZ, zuletzt 12.11.2026 18:36 MEZ)
- **Checks:** rot: EditMode + PlayMode FAILURE — Annotationen: Unity-Exit 1, zusätzlich „Artifact storage quota has been hit“; APK/Evidence skipped. Quinn-Review (Note 4/10): Compilerfehler in `HudD2LayoutTests.cs` Zeile 57 (Collection-Initializer mit Methodenketten).
- **Kritiker:** nicht als Epochen-Kritiker-Datei gefunden. Quinn: nicht mergen, bis Compiler und Gitleaks-Ignore geklärt sind.
- **Empfehlung:** fixen — Test kompilieren (`HudD2LayoutTests.cs:57`), Artifact-Kontingent räumen, `main` einholen.

### [#155](https://github.com/Xenatosa/epodarien/pull/155) — quests: System v2 mit Buch-1-Quests (Entwurf)
- **Branch:** `quests/system-v2-buch-1` → `main` (3 voraus, 0 hinter, `MERGEABLE`/`CLEAN`)
- **Alter:** 34 Tage (erstellt 23.10.2026 06:36 MESZ, zuletzt 23.10.2026 07:02 MESZ — danach keine Bewegung)
- **Checks:** nur 2× Gitleaks SUCCESS (push + pull_request). Kein Unity-Lauf (Head-Branch nicht in android.yml Z. 38–44).
- **Kritiker:** nicht geprüft.
- **Duplikat/überholt:** sehr wahrscheinlich durch #158 überholt (jüngerer Stand, Kritiker 10/10, 11.11. noch aktualisiert). Inhalt vor einem Schließen gegen #158 prüfen.
- **Empfehlung:** schließen als überholt — Kritiker 26.11.: #155 ist vollständig in #158 enthalten (Heads und 8 Dateien byte-gleich; #158 hat nur zusätzliche Timeline-Dateien). Nur auf Anweisung schließen; bei Squash-Merge von #158 erkennt GitHub #155 nicht automatisch als gemergt.

### [#153](https://github.com/Xenatosa/epodarien/pull/153) — Art: E1-Gebäude Variante B (gebaeude_neu_b)
- **Branch:** `art/gebaeude-neu-b` → `main` (1 voraus, 4 hinter, divergiert, `MERGEABLE`/`CLEAN`)
- **Alter:** 34 Tage (erstellt 22.10.2026 20:11 MESZ, zuletzt 12.11.2026 10:23 MEZ)
- **Checks:** fehlend (0 Check-Runs). Diff: 50 Binär-PNGs, 0 Textzeilen.
- **Kritiker:** nicht geprüft. Quinn: nur Binärdateien, keine Muss-Fixes aus dem Diff.
- **Empfehlung:** fixen — `main` einholen, Checks anstoßen, Art-Gültigkeit (Variante B ist laut Status die gültige Gebäudequelle) kurz bestätigen, dann mergen möglich.

### [#152](https://github.com/Xenatosa/epodarien/pull/152) — feat(ui): leere D2-Gerüste für 14 fehlende Menüs
- **Branch:** `ui/menus-d2-geruest` → `ui/menus-d2` (#151; 13 voraus, 0 hinter, `MERGEABLE`/`CLEAN`)
- **Alter:** 34 Tage (erstellt 22.10.2026 15:11 MESZ, zuletzt 12.11.2026 06:18 MEZ)
- **Checks:** EditMode + PlayMode SUCCESS, 2× Gitleaks SUCCESS, Build Android APK SKIPPED, Android Emulator Evidence SKIPPED (Branch `ui/**` löst den Test-Job aus, APK nur auf main / ci/self-hosted-all, Z. 99).
- **Kritiker:** geprüft, mehrere Rechecks in `team/kritik/review_pr152.md` und als Reviews von Xenatosa; Recheck 3 Note 9/10 (fachlich erledigt, zur 10 fehlte damals grüne CI — CI ist am Head `929b95c` inzwischen grün). Quinn (11.11., derselbe Head): Note 8/10, **Muss:** `android.yml` und `ci/Invoke-Unity.ps1` gehören nicht in diesen UI-PR (Paket markiert android.yml als tabu).
- **Empfehlung:** fixen — CI-Änderungen aus diesem PR nehmen oder in einen eigenen PR legen, dann mergen (nach bzw. mit #151).

### [#151](https://github.com/Xenatosa/epodarien/pull/151) — UI: D2 „Obsidian & Glut“ – Armee, Dock, Komponenten, Helden-Tabs
- **Branch:** `ui/menus-d2` → `main` (29 voraus, 4 hinter, divergiert, `MERGEABLE`/`UNSTABLE`)
- **Alter:** 34 Tage (erstellt 22.10.2026 14:10 MESZ, zuletzt 12.11.2026 06:23 MEZ)
- **Checks:** rot: EditMode + PlayMode FAILURE — Annotation: Artifact-Speicherquota erschöpft (CreateArtifact); kein zusätzlicher Testfehler in den Annotationen sichtbar. APK/Evidence skipped.
- **Kritiker:** geprüft, `team/kritik/review_pr151.md`, Recheck 7 am Head `7540aec`: vorläufig 9/10, 10/10 sobald APK/Emulator auf diesem Head grün sind.
- **Empfehlung:** fixen — Artifact-Kontingent räumen, `main` einholen, APK/Emulator anstoßen; Basis der Menü-Kette, nicht schließen.

### [#149](https://github.com/Xenatosa/epodarien/pull/149) — Story- und Heldendateien an Lore-Kanon angleichen
- **Branch:** `docs/story-auf-lore` → `main` (5 voraus, 4 hinter, divergiert, `MERGEABLE`/`UNSTABLE`)
- **Alter:** 34 Tage (erstellt 22.10.2026 10:11 MESZ, zuletzt 12.11.2026 10:23 MEZ)
- **Checks:** rot/abgebrochen: 2× „Geheimnisse suchen“ CANCELLED (24 h kein Runner).
- **Kritiker:** geprüft, `team/kritik/review_pr148_149.md`. Recheck an `a04b0f9`: Note 7/10, alte Muss 5/5, neuer Muss „Terwish auf epoch_3 statt epoch_17“. Follow-up-Commit `3d62b91` (22.10. 11:51 MESZ) „Fix lore review findings“; am Head steht Terwish in `heroes.csv` auf `epoch_17`. Kein dokumentierter Recheck nach diesem Commit. Letzter Commit `ed1250c` (04.11.) nur `.gitleaks.toml`.
- **Empfehlung:** fixen — kurzer Kritiker-Recheck gegen `3d62b91`/`ed1250c`, Checks wiederholen, `main` einholen, dann mergen möglich.

### [#148](https://github.com/Xenatosa/epodarien/pull/148) — Combat v2: formation slots and command tokens
- **Branch:** `gameplay/kampf-slots-tokens` → `main` (13 voraus, 4 hinter, divergiert, `MERGEABLE`/`UNSTABLE`)
- **Alter:** 34 Tage (erstellt 22.10.2026 10:05 MESZ, zuletzt 12.11.2026 10:23 MEZ)
- **Checks:** rot/abgebrochen: EditMode + PlayMode und 2× Gitleaks CANCELLED (24 h kein Runner).
- **Kritiker:** geprüft, Recheck an `92e98e2`: Note 8/10, Muss 6/6 (`team/kritik/review_pr148_149.md`).
- **Empfehlung:** fixen — `main` einholen, Checks wiederholen; fachlich mergen möglich nach bestätigter CI.

### [#145](https://github.com/Xenatosa/epodarien/pull/145) — chore(deps): bump actions/download-artifact 4.3.0 → 8.0.2
- **Branch:** Dependabot → `main` (1 voraus, 4 hinter, divergiert, `MERGEABLE`/`UNSTABLE`)
- **Alter:** 36 Tage (erstellt 20.10.2026 10:44 MESZ, zuletzt 12.11.2026 14:26 MEZ)
- **Checks:** rot/abgebrochen: 2× Gitleaks CANCELLED (24 h kein Runner).
- **Kritiker:** keine. `main` nutzt weiterhin download-artifact v4.3.0; der Bump ist also nicht durch `main` überholt.
- **Empfehlung:** fixen (rebase auf `main`, Checks neu) oder schließen und Dependabot aktuell neu öffnen lassen.

### [#144](https://github.com/Xenatosa/epodarien/pull/144) — feat: add fixed-footprint exploration world map
- **Branch:** `gameplay/weltkarte-fixed-footprint` → `main` (6 voraus, 4 hinter, divergiert, `MERGEABLE`/`UNSTABLE`)
- **Alter:** 37 Tage (erstellt 19.10.2026 21:50 MESZ, zuletzt 12.11.2026 14:27 MEZ)
- **Checks:** rot/abgebrochen: EditMode + PlayMode und 2× Gitleaks CANCELLED (24 h kein Runner).
- **Kritiker:** keine PR-Kritikdatei unter den offenen-PR-Reviews gefunden (es gibt eine separate Weltkarten-Kritik, ohne dass sie hier als Freigabe dieses PR-Heads belegt ist).
- **Empfehlung:** fixen — `main` einholen, Checks wiederholen, vor Merge eine klare Kritiker-/Design-Freigabe zum Head einholen.

### [#125](https://github.com/Xenatosa/epodarien/pull/125) — gameplay: Kampfsystem v2 Vorschau und General-Button
- **Branch:** `gameplay/kampfsystem-v2` → `main` (13 voraus, 57 hinter, divergiert, `MERGEABLE`/`CLEAN`)
- **Alter:** 40 Tage (erstellt 17.10.2026 08:30 MESZ, zuletzt 12.11.2026 18:33 MEZ)
- **Checks:** EditMode + PlayMode SUCCESS, 2× Gitleaks SUCCESS, Build Android APK SUCCESS, Android Emulator Evidence SKIPPED (Branch `gameplay/**` löst den Test-Job aus).
- **Kritiker:** keine eigene Datei zu #125 gefunden. Thematisch verwandt mit #148 und #106.
- **Empfehlung:** fixen — `main` einholen und gegen #148 abgrenzen (Reihenfolge/Überlappung), dann neu bewerten; nicht ungeprüft mergen, obwohl hier tatsächlich Unity-Tests grün sind.

### [#124](https://github.com/Xenatosa/epodarien/pull/124) — Event-Tokens: Option B als Config und Entwurf (Draft)
- **Branch:** `finanzen/event-tokens-option-b` → `main` (1 voraus, 68 hinter, divergiert, `MERGEABLE`/`CLEAN`)
- **Alter:** 40 Tage (erstellt und zuletzt 17.10.2026 08:23 MESZ)
- **Checks:** nur 2× Gitleaks SUCCESS (push + pull_request). Kein Unity-Lauf (Head-Branch nicht in android.yml Z. 38–44).
- **Kritiker:** nicht an diesem PR. Die Event-Kritik zu #84 (eigene Event-Marken, Kaufschleife) betrifft dasselbe Thema; ob Option B die Auflagen erfüllt, ist an diesem Head nicht nachgeprüft.
- **Empfehlung:** fixen — Draft belassen, `main` einholen, gegen die Event-/Währungsauflagen prüfen; nicht mergen ohne diese Prüfung.

### [#123](https://github.com/Xenatosa/epodarien/pull/123) — Recherche: PvP-Sternevergleich und Bonusdeckel
- **Branch:** `research/pvp-star-comparison-2026-10` → `main` (1 voraus, 68 hinter, divergiert, `MERGEABLE`/`CLEAN`)
- **Alter:** 40 Tage (erstellt und zuletzt 17.10.2026 08:19 MESZ)
- **Checks:** nur 2× Gitleaks SUCCESS (push + pull_request). Kein Unity-Lauf (Head-Branch nicht in android.yml Z. 38–44).
- **Kritiker:** nicht geprüft (Recherche-Paket, Queue-Zeile 12).
- **Empfehlung:** mergen als Recherche-Doku nach Einholen von `main` und kurzer Sichtprüfung (kein Spielcode). Checks waren nur Gitleaks, kein Unity — das ist hier kein Test-Beleg und auch kein Blocker. Nicht als „CI grün“ verbuchen.

### [#122](https://github.com/Xenatosa/epodarien/pull/122) — Gildenwährung und Saisonbeitrag vereinheitlichen
- **Branch:** `codex/gilden-waehrung` → `main` (1 voraus, 68 hinter, divergiert, `MERGEABLE`/`CLEAN`)
- **Alter:** 40 Tage (erstellt und zuletzt 17.10.2026 08:18 MESZ)
- **Checks:** nur 2× Gitleaks SUCCESS (push + pull_request). Kein Unity-Lauf (Head-Branch nicht in android.yml Z. 38–44).
- **Kritiker:** geprüft ja mit Auflagen (`team/kritik/kritik_2026-10-17_pr79_pr84_gilden.md`, Abschnitt Gilden): sichtbarer Beitragsbalken; keine Doppelwaren zu Chronik-/Sternstaub, Wochenlimits, 24-h-Hopping-Sperre. Ob der PR-Head diese Auflagen enthält, ist in den PR-Kommentaren nicht dokumentiert.
- **Empfehlung:** fixen — Auflagen am aktuellen Diff prüfen bzw. Kritiker-Recheck, `main` einholen, dann mergen möglich.

### [#121](https://github.com/Xenatosa/epodarien/pull/121) — [Entwurf] Währungs-Inventur und Zusammenlegungsvorschlag (Draft)
- **Branch:** `finanzen/waehrungen-inventur-v1` → `main` (2 voraus, 68 hinter, divergiert, `MERGEABLE`/`CLEAN`)
- **Alter:** 40 Tage (erstellt 17.10.2026 08:17 MESZ, zuletzt 08:18 MESZ)
- **Checks:** nur 2× Gitleaks SUCCESS (push + pull_request). Kein Unity-Lauf (Head-Branch nicht in android.yml Z. 38–44).
- **Kritiker:** nicht geprüft.
- **Empfehlung:** Draft belassen; fixen nur nach Finanz-/Kritiker-Prüfung, nicht ungeprüft mergen.

### [#111](https://github.com/Xenatosa/epodarien/pull/111) — Rechner: Beschwörungs-Bilanz v1 (Monte Carlo)
- **Branch:** `rechner/beschwoerung-bilanz-v1` → `main` (9 voraus, 86 hinter, divergiert, `MERGEABLE`/`CLEAN`)
- **Alter:** 40 Tage (erstellt 16.10.2026 23:32 MESZ, zuletzt 17.10.2026 06:45 MESZ)
- **Checks:** nur 2× Gitleaks SUCCESS (push + pull_request). Kein Unity-Lauf (Head-Branch nicht in android.yml Z. 38–44).
- **Kritiker:** Erstprüfung 17.10.: **nicht mergen**, v1.1 anfordern (`team/kritik/kritik_pr109_110_111.md`). Danach zwei Commits am 17.10. 06:44–06:45 MESZ: „Paket v1.1 … Featured ohne 50/50 … nur MANIFEST“ (`24c86b27`) und „T10 PvP-Deckel präzisiert“ (`0774994`). **Kein Recheck** in `team/kritik/` und keine PR-Kommentare gefunden.
- **Empfehlung:** fixen — Epochen Kritiker prüft v1.1 (`0774994`); erst danach mergen. Nicht auf Basis der alten „nicht mergen“-Wertung schließen, weil v1.1 bereits auf dem Branch liegt.

### [#110](https://github.com/Xenatosa/epodarien/pull/110) — Law: Moderationsauflagen umsetzen
- **Branch:** `law/moderation-auflagen` → `cursor/rechtsrecherche-play-e9e7` (nicht `main`; 4 voraus, 0 hinter dieser Basis, `MERGEABLE`/`CLEAN`)
- **Alter:** 40 Tage (erstellt und zuletzt 16.10.2026 23:10 MESZ — **vor** der Kritiker-Auflage)
- **Checks:** nur 2× Gitleaks SUCCESS (push + pull_request). Kein Unity-Lauf (Head-Branch nicht in android.yml Z. 38–44).
- **Kritiker:** freigegeben, mergen nach 1 Fix (`kritik_pr109_110_111.md`): `team/entscheidungen.md` nach `docs/law/launch-blocker.md` umbenennen; später zusätzlich Vertretung eintragen, 24 h bleibt fest. Der aktuelle Diff **legt `team/entscheidungen.md` weiterhin neu an** (4 Dateien, letzter Commit `824febaa` 16.10. 23:10 MESZ). Queue-Zeile 11 war am 17.10. 08:15 als gestartet markiert; auf dem Branch ist danach nichts gepusht.
- **Empfehlung:** fixen — Umbenennung und Vertretung committen, danach Kritiker-Endprüfung, dann mergen (Basis-Branch beachten, nicht still auf `main` annehmen).

### [#109](https://github.com/Xenatosa/epodarien/pull/109) — Recherche: Heldenbeschwörung erfolgreicher Mobile-Games
- **Branch:** `research/hero-summon-comparison-2026-10` → `main` (4 voraus, 85 hinter, divergiert, `MERGEABLE`/`CLEAN`), Head `a78a7d28`
- **Alter:** 40 Tage (erstellt 16.10.2026 23:04 MESZ, zuletzt 17.10.2026 08:18 MESZ)
- **Checks:** nur 2× Gitleaks SUCCESS (push + pull_request). Kein Unity-Lauf (Head-Branch nicht in android.yml Z. 38–44).
- **Kritiker:** Freigabe mit Auflagen am 17.10. gegen den Vor-P7-Stand; **kein Recheck** nach den drei P7-Commits. Keine GitHub-Reviews/Kommentare.
- **Empfehlung:** fixen — Whiteout/Last War nachziehen, PvP-Wortlaut an „deckeln, nicht komplett angleichen“ angleichen, Kritiker-Recheck, optional `main` einholen; erst dann mergen. Details im Abschnitt #109-Auflagen.

### [#108](https://github.com/Xenatosa/epodarien/pull/108) — Balancing P7: Beschwörungs-Pools prüfen
- **Branch:** `balancing/beschwoerung-pools-v1` → `cursor/gdd-v1614-1a71` (#88; 5 voraus, 44 hinter dieser Basis, divergiert, `MERGEABLE`/`UNSTABLE`)
- **Alter:** 40 Tage (erstellt 16.10.2026 22:12 MESZ, zuletzt 17.10.2026 08:15 MESZ)
- **Checks:** rot: 2× „Geheimnisse suchen“ FAILURE — Jobs starteten nicht wegen fehlgeschlagener Kontozahlungen bzw. Spending-Limit (Annotation), nicht wegen eines dokumentierten Leak-Fundes.
- **Kritiker:** Balancing-P7 wurde gesondert mit Auflagen freigegeben (Kritiker-Chat 17.10.); eine PR-bezogene Recheck-Datei zu diesem Head wurde nicht gefunden.
- **Empfehlung:** fixen — hängt an #88; Billing/Checks klären, Basis einholen, Head gegen die P7-Auflagen prüfen. Nicht isoliert nach `main` mergen.

### [#107](https://github.com/Xenatosa/epodarien/pull/107) — Balancing P6: Analyse zur Level-Rückholung
- **Branch:** `balancing/level-rueckholung-v1` → `main` (2 voraus, 86 hinter, divergiert, `MERGEABLE`/`CLEAN`)
- **Alter:** 40 Tage (erstellt 16.10.2026 21:54 MESZ, zuletzt 17.10.2026 08:14 MESZ)
- **Checks:** nur 2× Gitleaks SUCCESS (push + pull_request). Kein Unity-Lauf (Head-Branch nicht in android.yml Z. 38–44).
- **Kritiker:** P6-Übernahme wurde mit Auflagen freigegeben (u. a. Reset-Kosten festhalten); ob der PR-Head das enthält, ist hier nicht am Diff gegengeprüft.
- **Empfehlung:** fixen — `main` einholen, Auflagen am Diff prüfen, dann mergen möglich.

### [#106](https://github.com/Xenatosa/epodarien/pull/106) — docs: Kampfsystem v2 Abgleich mit Fabian-Nachträgen
- **Branch:** `docs/kampfsystem-v2-abgleich-fabian-20261016` → `main` (2 voraus, 86 hinter, divergiert, `MERGEABLE`/`CLEAN`)
- **Alter:** 40 Tage (erstellt 16.10.2026 21:39 MESZ, zuletzt 17.10.2026 08:11 MESZ)
- **Checks:** nur 2× Gitleaks SUCCESS (push + pull_request). Kein Unity-Lauf (Head-Branch nicht in android.yml Z. 38–44).
- **Kritiker:** nicht als Freigabe dieses PRs gefunden. Queue-Zeile 1 (3 Doku-Fixes) war am 17.10. 08:15 gestartet; letzter PR-Update 08:11, also vor oder ohne dokumentiertes Ende dieser Fixes.
- **Empfehlung:** fixen — prüfen, ob die drei Doku-Fixes im Head sind, `main` einholen, gegen #125/#148 halten.

### [#102](https://github.com/Xenatosa/epodarien/pull/102) — PvE-Kampfkonzept v1: Phasen P0–P6 (Draft)
- **Branch:** `pve/kampf-konzept-v1` → `main` (12 voraus, 86 hinter, **CONFLICTING** / `DIRTY`)
- **Alter:** 40 Tage (erstellt 16.10.2026 14:17 MESZ, zuletzt 16.10.2026 18:48 MESZ)
- **Checks:** nur 2× Gitleaks SUCCESS am alten Head, kein Unity-Lauf; nach einer neuen Konfliktlösung wäre das ohnehin neu zu belegen.
- **Kritiker:** nicht geprüft. Kommentar Xenatosa 16.10.: main wurde per Merge geholt (kein Force-Push), Konflikte in 25 Dateien damals gelöst; der aktuelle API-Status ist trotzdem `CONFLICTING` (main ist seither weitergegangen).
- **Empfehlung:** fixen — Konflikte erneut gegen heutiges `main` lösen oder als veralteten Draft schließen, falls durch spätere Kampf-PRs ersetzt (das Ersetzen ist nicht belegt).

### [#101](https://github.com/Xenatosa/epodarien/pull/101) — Glossar: Siegelscherbe und Lichtsiegel
- **Branch:** `loc/glossar-siegelscherbe` → `main` (5 voraus, 70 hinter, **CONFLICTING** / `DIRTY`)
- **Alter:** 40 Tage (erstellt 16.10.2026 13:02 MESZ, zuletzt 17.10.2026 07:51 MESZ)
- **Checks:** nur 2× Gitleaks SUCCESS (push + pull_request). Kein Unity-Lauf (Head-Branch nicht in android.yml Z. 38–44).
- **Kritiker:** nicht geprüft.
- **Empfehlung:** fixen — Konflikte lösen, dann mergen möglich (Lokalisierung, überschaubar) oder bei Überholung durch spätere Loc-PRs schließen (nicht belegt).

### [#100](https://github.com/Xenatosa/epodarien/pull/100) — feat: Epochenwechsel-Animation als wiederverwendbares Template
- **Branch:** `feature/epoch-transition-template` → `main` (6 voraus, 86 hinter, **CONFLICTING** / `DIRTY`)
- **Alter:** 40 Tage (erstellt 16.10.2026 13:02 MESZ, zuletzt 16.10.2026 18:55 MESZ)
- **Checks:** nur 2× Gitleaks SUCCESS (push + pull_request). Kein Unity-Lauf (Head-Branch nicht in android.yml Z. 38–44).
- **Kritiker:** nicht geprüft.
- **Empfehlung:** fixen — Konflikte gegen `main` lösen und fachlich prüfen; sonst als veralteter Feature-PR offen lassen, nicht mergen.

### [#97](https://github.com/Xenatosa/epodarien/pull/97) — Kampagne E1 v1.9: Brakka, Ausrüstung und Lore
- **Branch:** `kampagne/e1-v2-sammel` → `main` (5 voraus, 86 hinter, divergiert, `MERGEABLE`/`CLEAN`)
- **Alter:** 40 Tage (erstellt 16.10.2026 11:06 MESZ, zuletzt 17.10.2026 08:17 MESZ)
- **Checks:** nur 2× Gitleaks SUCCESS (push + pull_request). Kein Unity-Lauf (Head-Branch nicht in android.yml Z. 38–44).
- **Kritiker:** nicht geprüft. Thematisch überlappend mit #157/#149/#158 (Bosse, Lore, E1).
- **Empfehlung:** fixen — Überlappung mit #157/#149/#158 klären, bevor gemergt wird; `main` einholen. Nicht als Duplikat schließen ohne Diff-Abgleich.

### [#91](https://github.com/Xenatosa/epodarien/pull/91) — Testkonten: Grants nur für konfigurierte IDs (Draft)
- **Branch:** `backend/test-accounts` → `main` (2 voraus, 68 hinter, divergiert, `MERGEABLE`/`CLEAN`)
- **Alter:** 41 Tage (erstellt 15.10.2026 11:14 MESZ, zuletzt 17.10.2026 08:11 MESZ)
- **Checks:** 2× Gitleaks SUCCESS, Lint und Tests SUCCESS (Server), Nakama Compose SUCCESS (Server). Kein Unity-Lauf (`backend/**` steht nicht in android.yml Z. 38–44).
- **Kritiker:** nicht Epochen Kritiker. Epochen Security (Kommentar Xenatosa 17.10. 06:40 MESZ): **freigegeben, keine Blocker** (Tip `7d4aae5`).
- **Empfehlung:** fixen — laut Queue-Kopf erst nach #66 mergen; `main` einholen, Draft aufheben, dann mergen.

### [#88](https://github.com/Xenatosa/epodarien/pull/88) — docs: GDD v1.6.14 Shop, Kampfconfig, Energie-Events
- **Branch:** `cursor/gdd-v1614-1a71` → `main` (3 voraus, 68 hinter, divergiert, `MERGEABLE`/`UNSTABLE`)
- **Alter:** 41 Tage (erstellt 15.10.2026 11:10 MESZ, zuletzt 17.10.2026 08:36 MESZ)
- **Checks:** rot: 2× „Geheimnisse suchen“ FAILURE, Exit 1 (nicht der Billing-Text; Ursache in den Annotationen nur „Process completed with exit code 1“, kein Fundstellen-Text). EditMode + PlayMode SUCCESS.
- **Kritiker:** nicht geprüft. Gültiges GDD ist inzwischen v1.7.17; dieser PR beschreibt v1.6.14.
- **Empfehlung:** schließen oder klar als historischen Abgleich kennzeichnen und nicht nach `main` mergen — der Inhalt zielt auf eine überholte GDD-Fassung. Vor dem Schließen #108 (sitzt auf diesem Branch) umbiegen oder mitziehen. Gitleaks-Exit zusätzlich klären, falls der Branch weiterlebt.

### [#85](https://github.com/Xenatosa/epodarien/pull/85) — Lokalisierung: String-Tabellen DE/EN, Glossar, Quest-Texte
- **Branch:** `cursor/localization-package-b035` → `main` (2 voraus, 68 hinter, **CONFLICTING** / `DIRTY`)
- **Alter:** 41 Tage (erstellt 15.10.2026 11:06 MESZ, zuletzt 17.10.2026 08:13 MESZ)
- **Checks:** rot: EditMode + PlayMode FAILURE, Unity-Exit 1 (plus Node-20-Warnung). Gitleaks SUCCESS.
- **Kritiker:** nicht geprüft.
- **Empfehlung:** fixen — Konflikte und Unity-Fehler aus den Logs beheben, oder bei Überholung durch spätere Loc-Stände schließen (nicht belegt). Nicht mergen.

### [#79](https://github.com/Xenatosa/epodarien/pull/79) — Konzept: Stadt-Deko, Bevölkerung und Land (Draft)
- **Branch:** `cursor/stadt-deko-bevoelkerung-b759` → `main` (2 voraus, 111 hinter, divergiert, `MERGEABLE`/`UNSTABLE`)
- **Alter:** 41 Tage (erstellt 15.10.2026 10:59 MESZ, zuletzt 17.10.2026 08:14 MESZ)
- **Checks:** rot: 1× „Geheimnisse suchen“ FAILURE — Job startete nicht (Billing/Spending-Limit). EditMode SUCCESS, zweites Gitleaks SUCCESS.
- **Kritiker:** mergen nach 2 HOCH-Fixes (Kontur streichen, keine neue Überlauf-Währung). Commit `96c228a` 17.10.2026 08:14 MESZ: „PR #79: Kritiker-Fixes für Art-Stil und Überlauf“. Kein Recheck dokumentiert.
- **Empfehlung:** fixen — Kritiker-Recheck der zwei Fixes, `main` einholen, Draft aufheben; CI-Billing ist Infrastruktur.

### [#76](https://github.com/Xenatosa/epodarien/pull/76) — UI-Häuptlingsfeuer mit tauschbarer KI-Art
- **Branch:** `ui/center-ki-variant` → `main` (3 voraus, 68 hinter, **CONFLICTING** / `DIRTY`)
- **Alter:** 41 Tage (erstellt 15.10.2026 10:57 MESZ, zuletzt 17.10.2026 08:14 MESZ)
- **Checks:** EditMode + PlayMode SUCCESS, 2× Gitleaks SUCCESS, Build Android APK SKIPPED, Android Emulator Evidence SKIPPED (Branch `ui/**`).
- **Kritiker:** nicht geprüft.
- **Empfehlung:** fixen — Konflikte lösen und fachlich prüfen; nicht mergen solange `DIRTY`. Unity-Tests waren am Head grün, ersetzen aber keine Konfliktlösung.

### [#67](https://github.com/Xenatosa/epodarien/pull/67) — Play-Kauf serverseitig prüfen und erstatten (Draft)
- **Branch:** `backend/play-purchase-verify-73e7` → `main` (7 voraus, 87 hinter, divergiert, `MERGEABLE`/`CLEAN`)
- **Alter:** 41 Tage (erstellt 15.10.2026 10:38 MESZ, zuletzt 16.10.2026 15:23 MESZ)
- **Checks:** 2× Gitleaks SUCCESS, Lint und Tests SUCCESS (Server), Nakama Compose SUCCESS (Server). Kein Unity-Lauf (`backend/**` steht nicht in android.yml Z. 38–44).
- **Kritiker:** nicht Epochen Kritiker. Cursor-Kommentare: lokale Nakama-Tests grün; Queue: Security-Fix `applyVoid` erst starten, wenn #66 und #91 gemergt sind — ob dieser Fix im Head ist, wurde hier nicht am Diff geprüft.
- **Empfehlung:** fixen — Reihenfolge #66 → #91 → #67 einhalten, `main` einholen, offenen Security-Fix bestätigen, dann mergen.

### [#66](https://github.com/Xenatosa/epodarien/pull/66) — U18-Monatslimit serverseitig (hart, UTC) (Draft)
- **Branch:** `backend/minor-spend-limit-73e7` → `main` (3 voraus, 68 hinter, divergiert, `MERGEABLE`/`CLEAN`)
- **Alter:** 41 Tage (erstellt 15.10.2026 10:17 MESZ, zuletzt 17.10.2026 08:11 MESZ)
- **Checks:** 2× Gitleaks SUCCESS, Lint und Tests SUCCESS (Server), Nakama Compose SUCCESS (Server). Kein Unity-Lauf (`backend/**` steht nicht in android.yml Z. 38–44).
- **Kritiker:** nicht Epochen Kritiker. Lokale Nakama-Kommentare (Cursor) berichten grüne Suites; Queue wollte zuerst main in #66/#91 einholen.
- **Empfehlung:** fixen — `main` einholen, Draft aufheben, dann als erstes der Backend-Kette mergen.

### [#62](https://github.com/Xenatosa/epodarien/pull/62) — PvE-Nerven über game_config lockern (Draft)
- **Branch:** `cursor/pve-nerve-fixes-ef52` → `main` (1 voraus, 111 hinter, **CONFLICTING** / `DIRTY`)
- **Alter:** 42 Tage (erstellt und zuletzt 15.10.2026 07:18 MESZ)
- **Checks:** rot: EditMode Unity-Exit 1; 2× Gitleaks starteten nicht (Billing).
- **Kritiker:** nicht geprüft.
- **Empfehlung:** fixen oder schließen — 42 Tage unverändert, Konflikte, Unity-Fehler; nur mergen nach Konfliktlösung und Begründung, dass der Stand noch gilt.

### [#60](https://github.com/Xenatosa/epodarien/pull/60) — Forschung mit Uhren statt Kristallen, plus Tageslimit (Draft)
- **Branch:** `cursor/research-clocks-daily-limit-7a28` → `main` (1 voraus, 111 hinter, **CONFLICTING** / `DIRTY`)
- **Alter:** 42 Tage (erstellt und zuletzt 15.10.2026 06:30 MESZ)
- **Checks:** rot: Gitleaks, Lint und Tests, Nakama Compose — durchgängig „Job was not started“ wegen Billing/Spending-Limit. EditMode SUCCESS.
- **Kritiker:** nicht geprüft. Forschung/Uhren ist seither in GDD-Entwürfen weitergegangen; eine Überholung dieses konkreten PRs ist nicht belegt.
- **Empfehlung:** fixen (Konflikte, `main`, inhaltlich gegen den gültigen GDD-Stand v1.7.17 prüfen) oder schließen, wenn der Ansatz verworfen wurde. Nicht mergen.

### [#59](https://github.com/Xenatosa/epodarien/pull/59) — Nakama: Testkäufe nur für Konten aus der Server-Liste (Draft)
- **Branch:** `cursor/nakama-test-admin-b7c0` → `main` (1 voraus, 111 hinter, divergiert, `MERGEABLE`/`UNSTABLE`)
- **Alter:** 42 Tage (erstellt und zuletzt 15.10.2026 06:25 MESZ)
- **Checks:** rot: dieselben Billing-Startverweigerungen (Gitleaks, Lint, Nakama); EditMode SUCCESS.
- **Kritiker:** nicht geprüft. Thematisch verwandt mit #91 (Testkonten), das später liegt und Security-Freigabe hat.
- **Duplikat/überholt:** möglicherweise durch #91 überholt; ohne Diff-Abgleich nicht als Duplikat geschlossen.
- **Empfehlung:** fixen — gegen #91 abgleichen; falls enthalten, schließen; sonst `main` einholen und bewusst führen.

### [#57](https://github.com/Xenatosa/epodarien/pull/57) — Doku: PowerShell 7 und Unity 6000.3.26f1 als Runner-Voraussetzungen
- **Branch:** `cursor/self-hosted-runner-pwsh-9906` → `main` (3 voraus, 75 hinter, divergiert, `MERGEABLE`/`CLEAN`)
- **Alter:** 42 Tage (erstellt 14.10.2026 17:58 MESZ, zuletzt 16.10.2026 23:24 MESZ)
- **Checks:** EditMode + PlayMode SUCCESS, 2× Gitleaks SUCCESS, Build Android APK SKIPPED, Android Emulator Evidence SKIPPED. Branch `cursor/**` steht in android.yml Z. 41; Unity ist hier tatsächlich gelaufen (im Gegensatz zu #159–#161).
- **Kritiker:** nicht geprüft (Doku).
- **Empfehlung:** mergen möglich nach Einholen von `main` und kurzer Prüfung, ob die Runner-Daten noch stimmen. Empfehlung unverändert, nur die Check-Angabe präzisiert.

### [#5](https://github.com/Xenatosa/epodarien/pull/5) — Bump actions/checkout 4.4.0 → 7.0.1
- **Branch:** Dependabot → `main` (1 voraus, 89 hinter, divergiert, `MERGEABLE`/`UNSTABLE`)
- **Alter:** 43 Tage (erstellt 13.10.2026 20:54 MESZ, zuletzt 16.10.2026 14:22 MESZ)
- **Checks:** rot: Nakama Compose FAILURE, Exit 1 (Annotation ohne Fehlersatz, plus Node-20-Warnung). Gitleaks und Lint SUCCESS.
- **Kritiker:** keine. `main` pinnt weiterhin checkout v4.4.0.
- **Empfehlung:** fixen (rebase, Nakama-Log lesen) oder schließen und Dependabot neu öffnen lassen.

### [#3](https://github.com/Xenatosa/epodarien/pull/3) — Bump actions/cache 4.3.0 → 6.1.0
- **Branch:** Dependabot → `main` (1 voraus, 111 hinter, divergiert, `MERGEABLE`/`UNSTABLE`)
- **Alter:** 43 Tage (erstellt 13.10.2026 20:53 MESZ, zuletzt 14.10.2026 19:51 MESZ)
- **Checks:** rot: 2× Gitleaks FAILURE — Jobs starteten nicht (Billing/Spending-Limit).
- **Empfehlung:** fixen (rebase nach Billing) oder schließen und neu öffnen lassen. `main` pinnt weiterhin cache v4.3.0.

### [#2](https://github.com/Xenatosa/epodarien/pull/2) — Bump actions/upload-artifact 4.6.2 → 7.0.2
- **Branch:** Dependabot → `main` (1 voraus, 111 hinter, divergiert, `MERGEABLE`/`UNSTABLE`)
- **Alter:** 43 Tage (erstellt 13.10.2026 20:53 MESZ, zuletzt 14.10.2026 19:51 MESZ)
- **Checks:** rot: 2× Gitleaks FAILURE — Jobs starteten nicht (Billing/Spending-Limit).
- **Empfehlung:** fixen (rebase nach Billing) oder schließen und neu öffnen lassen. `main` pinnt weiterhin upload-artifact v4.6.2. Hinweis: mehrere PRs scheitern bereits an der Artifact-Quota; ein Major-Bump allein löst das Kontingent nicht.

## Abschnitt #109 — Kritiker-Auflagen

**Quellen für den Wortlaut**

- `team/kritik/kritik_pr109_110_111.md` (17.10.2026, Epochen Kritiker): „PR #109 … freigegeben mit Auflagen, mergen“, plus vier nummerierte Auflagen.
- Kritiker-Chat (Agent `9463301f-…`): dieselbe Wertung und die spätere Arbeitsanweisung nach Fabians Entscheidungen.
- Arbeitspaket `/workspace/uploads/paket_pr109_abschnitt7_p7.md` (identisch mit `team/recherche/paket_pr109_abschnitt7_p7.md`).
- In den GitHub-Reviews und Issue-Kommentaren von #109 steht **nichts** (0 Reviews, 0 Kommentare).

**Wortlaut der Auflagen** (Kritikdatei, gekürzt nur um die Überschrift; Kernsätze wörtlich):

1. **HOCH:** „Die Epodarien-Basis ist veraltet (GDD v1.6.13 mit Echo-Splittern und 40 Fragmenten). P7 gilt: Chronikstaub, 60 Fragmente, Spezial-Pity 30. Abschnitt 7 auf P7 umstellen.“
2. **HOCH (Design):** „Featured-50/50 mit 160 Zügen ist nur 20 Züge besser als bei Genshin, obwohl Epodarien nur rund halb so viele F2P-Züge gibt (21 statt 37–48 pro Monat). Vorschlag: Featured ohne 50/50 wie bei AFK Journey oder Epic Seven, Garantie bei 80, oder Capturing-Radiance-artig.“
3. **MITTEL:** „Für Epodarien braucht ein Held bis 5★ 12 Kopien, bei Genshin ist C0 voll spielbar. Mit Sterne-Kampfkraft in PvP ist das ein P2W-Risiko.“
4. **NIEDRIG:** „Aufbauspiel-Konkurrenz (Whiteout Survival, Last War) fehlt, das ist Fabians eigentliches Genre.“

Nach Fabians Entscheidungen vom 17.10. präzisierte der Kritiker die Umsetzung so (Chat, Arbeitsauftrag an Recherche): Echo-Splitter und 40 Fragmente entfernen; neu Chronikstaub, 60 Fragmente zum Freischalten, 600 bis 5★, 12 Kopien; Featured ohne 50/50, Garantie spätestens bei Zug 80; Sterne-Boni im PvP deckeln oder angleichen; niedrige Priorität Whiteout Survival und Last War. Fabian präzisierte (b) später: **deckeln, nicht komplett angleichen**.

**Stand des Heads `a78a7d28`** (Dateien `team/recherche/beschwoerung_vergleich.md` / `.csv`; P7-Commits `303f0ce`, `698b8dc`, `a78a7d2` am 17.10.2026 08:17:51–08:18:28 MESZ):

| Auflage | Urteil | Beleg |
|---|---|---|
| 1 P7-Werte, Echo/40 weg, Abschnitt 7 | **Erfüllt** (mit Hinweis zu Spezial-Pity 30) | Echo-Splitter / „40 Fragmente“ kommen im aktuellen md/csv nicht mehr vor. Abschnitt 7 (`beschwoerung_vergleich.md` Z. 117–129, 125–126): Chronikstaub, 60 Fragmente zum Freischalten, 600 bis 5★, 12 Kopien. CSV-Zeilen Featured-Garantie 80, Duplikatfragmente 60/600, Chronikstaub-Umwandlung (Commit `303f0ce` ersetzt u. a. „Echo-Shop, 40 Fragmente“). **Spezial-Pity 30:** in #109 nicht genannt. In `team/helden/beschwoerung-pools-v1.md` Z. 112 und 116 (Finanzen-Korrektur 17.10.) ist der Vorschlag Pity 30/50 zurückgezogen, Spezial-Banner bleibt Hard Pity 80. Damit ist das Fehlen von Pity 30 kein offener P7-Widerspruch mehr. |
| 2 Featured ohne 50/50, Garantie 80 | **Erfüllt** | Z. 10, 124, 136: „kein 50/50“, „spätestens bei Zug 80“. CSV: Featured-Garantie von 160/50 % auf 80 / „keine 50/50“ (`303f0ce`). Commit `a78a7d2` erhält den Pity-Übertrag zwischen Featured-Bannern (Z. 124, 154). |
| 3 12 Kopien / P2W-Risiko, später PvP-Deckel | **Erfüllt mit offenem Rest** | 12 Kopien und der Unterschied zu C0/E0 stehen in Z. 125 und 140. Z. 127 und 147: P7-Beschluss deckelt bzw. gleicht Stern-Boni im PvP an, nennt aber keinen Zahlenwert; alte GDD-Staffel darf nicht als P7-Wert gelten. **Unklar/teilweise:** Der Wortlaut „deckt bzw. gleicht … an“ bildet Fabians spätere Präzisierung „deckeln, nicht komplett angleichen“ nicht scharf ab. Ein Zahlen-Deckel fehlt bewusst (im Dokument offengelegt). |
| 4 Whiteout Survival, Last War | **Nicht erfüllt** | In md-Tabellen und CSV kommen diese Spiele nicht vor. Die Vergleichstabellen enthalten weiterhin die ursprünglichen 9 Spiele (AFK Arena/Journey, Genshin, HSR, RoK, Summoners War, Epic Seven, Raid, Call of Dragons). Paketpunkt 3 (niedrige Priorität) ist offen. |

Weitere Lücken, die keine der vier Auflagen sind, aber im Paket standen: keine „kurze Änderungsliste im PR-Kommentar“ (0 Kommentare); der Kritiker wollte das Ergebnis danach erneut prüfen — ein Recheck ist nicht auffindbar. `main` ist 85 Commits voraus; Konflikte gibt es trotzdem keine (`MERGEABLE`).

## Abschnitt P7-Ursache (Queue-Zeile 10)

**Queue-Text** (`/workspace/uploads/codex_queue.md`, Zeile 10, Stand dieser Prüfung unverändert `[GESTARTET]`, nie `[ERLEDIGT]`):

> 10. [GESTARTET 17.10. 08:15 https://chatgpt.com/local/01a1487d-6546-7570-8c15-aee24034005f] paket_pr109_abschnitt7_p7.md + beschwoerung-pools-v1.md \| Abschnitt 7 von PR #109 auf P7-Werte umstellen laut Paket, auf den PR-Branch von #109 pushen. Neu entschieden: Featured ohne 50/50, Garantie spaetestens bei 80; Sterne-Boni im PvP gedeckelt.

Die Formulierung „nichts gepusht“ stammt aus der Meldung von Epochen Recherche an New Bot am 26.11. (Nebenbemerkung zu #109 und Zeile 10), nicht aus einem Logeintrag in der Queue selbst.

**Befund: Auf den PR-Branch wurde sehr wohl gepusht.** Remote `origin/research/hero-summon-comparison-2026-10` und PR-Head sind `a78a7d28`. Nach dem Ursprungs-Commit `5b2939b` (16.10.2026 23:03:56 MESZ) folgen genau die drei P7-Commits, Autor/Committer Xenatosa, Zeitzone `+0200`:

- `303f0ce` 17.10.2026 08:17:51 MESZ — „align summon comparison with P7 decisions“
- `698b8dc` 17.10.2026 08:17:58 MESZ — „align summon metrics with P7 values“
- `a78a7d2` 17.10.2026 08:18:28 MESZ — „preserve featured pity carry“

Das liegt 2–3 Minuten nach dem in der Queue notierten Start 17.10. 08:15. Der Diff `5b2939b…a78a7d28` ändert genau die beiden Recherche-Dateien und setzt die P7-Werte um (siehe Abschnitt #109). `git` im lokalen Klon `/workspace/epodarien` zeigt denselben Remote-Stand; ein zusätzlicher lokaler, nicht gepushter Branch dieser Arbeit wurde nicht gefunden. Der PR wurde zuletzt am 17.10.2026 08:18 MESZ aktualisiert, passend zum letzten Commit.

**Warum die Queue „nichts gepusht“ suggeriert**

Wahrscheinlichste Ursache: Die Zeile blieb auf `[GESTARTET]` stehen. Es gibt keinen `[ERLEDIGT]`-Eintrag, keinen PR-Kommentar (den das Paket verlangt hätte) und kein Recheck. Recherche hat am 26.11. den Queue-Status gelesen und daraus „nichts gepusht“ geschlossen. Das widerspricht dem GitHub-Stand.

Nicht belegt als Push-Fehler: Auth-Ablehnung, Merge-Konflikt beim Push, Abbruch nach den drei Commits oder „Job nie gestartet“. Der Job ist in der Queue als gestartet geführt, und die Commits existieren auf dem Remote.

**Was zur vollen Rekonstruktion fehlt:** Das ChatGPT-Local-Sitzungsprotokoll `01a1487d-6546-7570-8c15-aee24034005f` liegt nicht auf dieser Box. Unter `/home/box/.codex/sessions/2026/10/17/` beginnen die vorhandenen Codex-Rollouts erst später am selben Tag und tragen andere IDs. Damit ist nicht unabhängig aus einem Job-Log belegbar, ob der Lauf nach den drei Commits noch Whiteout/Last War oder den PR-Kommentar versuchen sollte und dort endete — nur, dass genau diese Reste im Ergebnis fehlen und der Git-Push der P7-Kernänderung stattgefunden hat.

## Kostenzeile

Erstfassung 26.11.2026 **08:04–08:18 MEZ**, 0 €, ohne Codex.  
Korrektur der Check-Angaben, Kritiker-Noten #159/#160/#161 und Codex-Pakete: **08:27–08:34 MEZ**, 0 €, ohne Codex.
