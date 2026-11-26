# Codex-Paket: PR #161 Grundlagen-EditMode-Tests (Note 3/10)

**Modell:** wie in der lokalen Codex-Config (nicht ändern).  
**Auftraggeber:** Epochen QA, 26.11.2026, nach Kritiker-Notiz und New-Bot-Folgeauftrag.  
**Reihenfolge:** Dieses Paket zuerst. Danach Paket `paket_pr159_160_sollte_2026-11-26.md`. Der Unity-Lauf steht in `paket_pr159_160_161_unity_lauf_2026-11-26.md` und hängt an beiden.

## Ziel

Die sechs Muss-Punkte M-1 bis M-6 in PR #161 so beheben, dass `GrundlagenQaTests.cs` kompiliert und die Erwartungen zu Winter, Unterhalt und `starter` gegen die gültigen Daten in `data/` bzw. GDD v1.7.17 stimmen; außerdem S-1 umsetzen (Branch-Trigger `tests/**` in `android.yml`).

## Repo und Branch

- Repo: `github.com/Xenatosa/epodarien`, nur Konto Xenatosa.
- Weiterarbeiten auf dem bestehenden PR-Branch `tests/qci-grundlagen-editmode-2310` (PR #161, Head zum Zeitpunkt der Notiz `b6fe0b3980fe7231c954c52489d4c738b5e026ec`). Basis `main` einholen, falls nötig, nur per Merge, **kein Rebase mit Force**, **kein Force-Push**.
- Ergebnis als Commits auf diesen Branch pushen. Den PR nicht mergen, nicht schließen, keine Review-Kommentare schreiben. PR-Text darf per `gh pr edit` um den Hinweis ergänzt werden, dass Unity zuvor nie gelaufen ist und wie der Trigger jetzt greift.

## Quellen

- Kritiker-Notiz: `team/kritik/PRUEFNOTIZ_prs_159_160_161_2026-11-26.md` im Planer-Repo (lokal unter `/workspace/handygame-plan/`; nicht auf `origin/main` gefunden). Die IDs M-1…M-6 und S-1 gelten wörtlich aus dieser Notiz.
- Gültiges GDD: `/workspace/handygame-plan/team/gdd/GDD_v1.7.17.md` — **nur lesen, nicht ändern**.
- Daten und Code im Spielrepo: CSVs unter `Assets/_Project/Data/` bzw. `Assets/_Project/Data/CSV/`, dazu `TickService`, `ArmyManager`, Shop-/Sichtbarkeitsregeln, Vergleichstests derselben Familie (z. B. `QuestBoardTests`).

## Betroffene Dateien

- `Assets/_Project/Tests/EditMode/GrundlagenQaTests.cs` (und `.meta` nur, wenn unvermeidbar neu)
- `.github/workflows/android.yml` (nur der `push.branches`-Block, siehe S-1)

Keine anderen Workflows, kein Produktivcode, es sei denn, ein Test braucht eine vorhandene Test-API, die schon von anderen EditMode-Tests genutzt wird.

## Mängel (IDs aus der Notiz, umzusetzen)

**Muss**

- **M-1** `GrundlagenQaTests.cs` Z. 30 · `Object.DestroyImmediate(o)` bei `using System;` und `using UnityEngine;` → CS0104 (mehrdeutig). Die anderen Tests der Datei-Familie schreiben deshalb `UnityEngine.Object.` (z. B. QuestBoardTests Z. 26). · Lösung: `UnityEngine.Object.DestroyImmediate`. · Priorität hoch.
- **M-2** `GrundlagenQaTests.cs` Z. 140 und Z. 375 · `Db(new[] { new ConfigEntry … })`, die Signatur ist aber `Db(List<ConfigEntry> config = null)` (Z. 395) → CS1503, Array zu List. · Lösung: `new List<ConfigEntry> { … }` oder Parameter `IEnumerable<ConfigEntry>`. · hoch.
- **M-3** `GrundlagenQaTests.cs` Z. 358 und Z. 373 · verschachtelte Klasse `WinterRig` und Methode `WinterRig(...)` im selben Typ → CS0102 (doppelte Definition). · Lösung: Methode umbenennen (`BuildWinterRig`). · hoch.
- **M-4** `GrundlagenQaTests.cs` Z. 106–109 (`Winter_NahrungProduziertImWinterNurMitMehrwertfaktor`) · erwartet 1260. Nachgerechnet gegen `TickService.Advance`: Faktor `0.7f` (float, 0,699999988) × 3600/h, in 30 Minutenschritten mit Carry → 1259,99998 → `Math.Truncate` → **1259**. Der Test schlägt auch ohne Compile-Fehler fehl. · Lösung: Erwartung 1259 mit Kommentar zur float-Rundung, oder Faktor `0.5f`/Rate so wählen, dass exakt gerechnet wird. · hoch. **Vor dem Ändern neu gegen den aktuellen `TickService` und die gültigen Daten nachrechnen; nicht die Zahl 1259 ungeprüft übernehmen, falls sich Code oder CSV seit der Notiz geändert haben.**
- **M-5** `GrundlagenQaTests.cs` Z. 138–164 (`Winter_UnterhaltZiehtAbUndUeberlebenWirdGemeldet`) · `db.Units.Add(Unit("unit_club", upkeepPerHour: 360))` legt nur eine Definition an. `ArmyManager.UpkeepFoodPerHour` summiert aber nur gehaltene Truppen (`army`-Dictionary, ArmyManager Z. 75). Es wird nie eine Einheit trainiert oder wiederhergestellt. Unterhalt = 0 → Nahrung bleibt 1000 (erwartet 280), im Hunger-Fall bleibt 100 (erwartet 0), `IsHungry` ist false, `WinterSurvived` feuert auch im „starved“-Fall. · Lösung: Einheiten in die Armee bringen (`TryTrain` mit Kasernen-Setup oder `Restore`-Pfad), dann die Erwartung neu rechnen. · hoch. **Erwartung nach dem Setup gegen Code und Daten neu rechnen, nicht an 280/0 festkleben, wenn der gültige Unterhalt anders ist.**
- **M-6** `GrundlagenQaTests.cs` Z. 252 · `Assert.IsFalse(IsItemVisible(config, " starter ", "any"))`. Die Config verbirgt nur Kategorien `subscription, event_token, milestone` und Angebot `starter_hero_pack`; „starter“ steht nicht in den Kategorien → Ergebnis true, die Assertion schlägt fehl. Z. 253 behauptet das Gegenteil. · Lösung: `starter` in die Kategorienliste aufnehmen und die Z. 252/253 passend umdrehen oder trennen. · hoch. **Gegen die gültige U18-/Shop-Regel in GDD v1.7.17 und die CSVs prüfen, welche Verberge-Liste tatsächlich gilt.**

**Sollte (in diesem Paket nur S-1; S-2 bis S-4 dürfen mit, sind aber nachrangig)**

- **S-1** PR-Text · „Rein Test-Code“, aber kein Hinweis, dass die Tests nie ausgeführt wurden. Lösung: Branch-Trigger ergänzen (`tests/**`) oder den PR auf einen `ci/self-hosted-all`-Lauf prüfen; Ergebnis im PR-Text nennen. · hoch.

### Empfohlene Variante für S-1

**Empfohlen: In `android.yml` den Branch-Präfix `'tests/**'` in die bestehende `push.branches`-Liste aufnehmen (aktuell Z. 39–44: `main`, `cursor/**`, `gameplay/**`, `ui/**`, `ci/self-hosted-all`).**

Begründung:

1. Es gibt **keinen `paths:`-Filter**. `data/`, `nova/` und `tests/` bleiben stumm, weil der Head-Branch so heißt und nicht in der Branch-Liste steht, nicht weil der Dateipfad ausgefiltert würde. Ein paths-Filter wäre die falsche Stellschraube.
2. `tests/**` macht künftige Test-PRs automatisch sichtbar. Sonst bleibt „CI grün“ wieder nur Gitleaks, und Compile-Fehler wie M-1–M-3 kämen erst auf `main` zum Vorschein (die Notiz warnt genau davor).
3. `ci/self-hosted-all` bleibt der vorgesehene einmalige Prüfzweig (Kopf Z. 8) und ist der richtige Hebel für Paket 3 (alle drei PRs, auch `data/` und `nova/`). Er ersetzt aber nicht den dauerhaften Trigger für Test-Branches.
4. Kein `pull_request`-Trigger in diesem Paket (dafür gibt es das gesonderte, security-geprüfte Vorhaben `ci/unity-on-pr`). Keine Änderung an APK- oder Evidence-Jobs (`if` Z. 99 und Z. 172 bleibt).

Den tatsächlichen EditMode-/PlayMode-Lauf für #161 nicht in diesem Paket erzwingen; der folgt in Paket 3, sobald M-1–M-6 auf dem Branch sind. Nach dem Push von S-1 kann ein weiterer Push auf `tests/qci-grundlagen-editmode-2310` den Test-Job bereits selbst auslösen — das darf als Lauf für Paket 3 zählen, wenn Artefakt und Logs vollständig sind.

## Abnahmekriterien

- `GrundlagenQaTests.cs` kompiliert ohne CS0104, CS1503, CS0102.
- M-4, M-5, M-6: Assertions stimmen mit einem nachvollziehbaren Nachrechnen gegen aktuellen Code und gültige Daten/GDD v1.7.17 überein (Zahl und Begründung im Commit oder in einem kurzen Kommentar an der Assertion).
- `android.yml` enthält `'tests/**'` in `on.push.branches`; sonst unverändert in Trigger- und Job-Logik.
- Kein Force-Push, kein Merge, GDD v1.7.17 unangetastet, keine Secrets im Diff.
- Kurzer Nachweis im PR-Text oder in der Meldung: welche Erwartungen neu gerechnet wurden und gegen welche Datei/Zeile.

## Verbote

- Nichts mergen, den PR nicht schließen.
- Kein Force-Push, kein Rebase mit `--force`.
- Keine Secrets lesen, ausgeben oder committen.
- GDD v1.7.17 nicht anfassen (keine Edits in `/workspace/handygame-plan/team/gdd/` und keine „Aktualisierung“ des GDD im Spielrepo).
- Kein Produktivcode ändern, nur weil ein Test rot ist; erst Setup und Erwartung prüfen.
- `android.yml` nicht für APK/Evidence, Secrets oder `pull_request` umbauen.

## Prüfung

Lokal, soweit der Editor fehlt, mindestens: Datei gegen die Compiler-Punkte und die Nachrechnung lektorieren. Den echten Unity-Lauf übernimmt Paket 3.

## Meldeformat

- **Ergebnis:** was geändert wurde (Dateien, Commits, SHA), welche IDs erledigt sind, welche Erwartungen wie nachgerechnet wurden.
- **Kosten:** Beginn und Ende der Laufzeit in MEZ, Betrag (0 € ohne Extra-Kosten).
- **Geprüft:** was selbst geprüft wurde; Unity-Lauf ja/nein (nein, wenn Paket 3 noch aussteht).
- **Offene Fragen:** nur echte Blocker oder abweichende Datenlagen.
- **Nächster Empfänger:** nach Push Epochen QA; der Unity-Lauf geht an das Paket 3, danach Recheck an Epochen Kritiker.
