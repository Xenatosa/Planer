#!/usr/bin/env python3
"""Run the p3d27 V3 official-checker-in-the-loop probe, serially."""
from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
RELIEF3D = ROOT / "team/art/dorfmap_grundgeruest/relief3d"
TOOLS = ROOT / "codex_jobs/tools/p3d27"
RESULTS = TOOLS / "results"
BASE_CUTS = ROOT / "codex_jobs/tools/p3d20_r3/event_cuts_cumulative05.json"
DERIVER = ROOT / "codex_jobs/tools/p3d20_r3/derive_event_cuts.py"
G11_KINDS = ("baeume", "felsen", "findlinge", "steine", "felsbloecke")
BASELINE_RULES = ROOT / "codex_jobs/tools/p3d20_r3/official_gates/p3d17_reference_regeln_current_schema.json"
TRANSFER = RELIEF3D / "neu/p3d21_transfer_base_route3_v29.json"
SOURCE = Path("/tmp/p3d22_v3_source.json.gz")
EMPTY_CUTS = RESULTS / "p3d27_V3_R00_cuts.json"
EXPECTED_SOURCE_SHA256 = "b1e347e048d1f26d79b812b795645bf348ef83e831209669cf5cbd2f7717b4a6"
EXPECTED_TRANSFER_SHA256 = "07c140cffa97df408f2c688ee910b4085e429e986b047f15b62551727ea69287"


def checked(args: list[str], *, label: str) -> subprocess.CompletedProcess[str]:
    run = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    if run.returncode != 0:
        raise RuntimeError(f"{label} failed ({run.returncode}): {run.stderr[-2000:]} {run.stdout[-1000:]}")
    return run


def dump(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def output_document(rounds: list[dict], best_round, best_score, cuts_count: int,
                    status: str, baseline_d1_g11: int) -> dict:
    return {
        "tag": "p3d27", "geometry": "V3", "baseline_D1_G11_hits": baseline_d1_g11,
        "start_event_cut_count": len(json.loads(BASE_CUTS.read_text(encoding="utf-8"))),
        "rounds": rounds, "best_round": best_round, "best_score": best_score,
        "final_cut_count": cuts_count, "status": status,
        "method": "serial all-family V3 Float32 official checker-in-the-loop; no mesh build",
    }


def _tile_total(by_tile: dict, tile: str) -> int:
    return sum(int(value) for value in by_tile.get(tile, {}).values())


def write_report_progress(rounds: list[dict], status: str) -> None:
    report = RELIEF3D / "pruefung/ERGEBNIS_p3d27.md"
    content = report.read_text(encoding="utf-8")
    section = content.index("## 1. V3 Float32-Gate-Probe\n")
    table_start = content.index("| Runde |", section)
    section_end = content.index("\n\n## 2. Mesh-Gate", table_start)
    intro = (
        f"`[S]` Status: {status} Maximal sechs serielle Solve-Runden zu höchstens 600 s; "
        "V3, alle Familien und unveränderte Prüfer. Die Quelle und Transferbasis haben "
        "die im Abschnitt 0 angegebenen Hashes. Frische offizielle G5-/R5-Loch-/G11- "
        "Ereignisse werden nach jeder Probe ergänzt.\n\n"
    )
    lines = [
        "| Runde | `pruefe_regeln` gesamt (D1/G1/D2) | R8 gesamt (D1/G1/D2) | R9 gesamt (D1/G1/D2) | Ziele / Beleg |",
        "|---:|---|---|---|---|",
    ]
    for record in rounds:
        round_no = int(record["round"])
        probe_path = record.get("probe_json")
        if probe_path:
            rules = record.get("official_rules_by_tile_D1_G1_D2", {})
            r8 = record.get("official_R8_by_tile_D1_G1_D2", {})
            r9 = record.get("official_R9_by_tile_D1_G1_D2", {})
            rtuple = lambda data: f"{int(record.get('official_rules_total', 0))} (" + "/".join(
                str(_tile_total(data, t)) for t in ("D1", "G1", "D2")) + ")"
            r8tuple = f"{int(record.get('official_R8_total_by_rule', {}).get('total', 0))} (" + "/".join(
                str(_tile_total(r8, t)) for t in ("D1", "G1", "D2")) + ")"
            r9tuple = f"{int(record.get('official_R9_total_by_rule', {}).get('total', 0))} (" + "/".join(
                str(_tile_total(r9, t)) for t in ("D1", "G1", "D2")) + ")"
            excess = record.get("hard_target_excess", {})
            missed = [name.removeprefix("target:") for name, value in excess.items()
                      if float(value) > 1e-9]
            verdict = "alle Ziele erfüllt" if not missed else "offen: " + ", ".join(missed)
            basename = Path(probe_path).name
            evidence = f"{verdict}; [JSON](../../../../../codex_jobs/tools/p3d27/results/{basename})"
            lines.append(f"| {round_no} | {rtuple(rules)} | {r8tuple} | {r9tuple} | {evidence} |")
        else:
            lines.append(f"| {round_no} | kein Probe-Relief | – | – | Solverstatus: {record.get('model_status')} |")
    replacement = intro + "\n".join(lines)
    content = content[:section] + "## 1. V3 Float32-Gate-Probe\n\n" + replacement + content[section_end:]
    report.write_text(content, encoding="utf-8")


def checkpoint(round_no: int) -> None:
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT,
                            capture_output=True, text=True, check=True).stdout.strip()
    if branch != "art/dorfmap-p3d27":
        raise RuntimeError(f"Unerwarteter Branch für p3d27-Checkpoint: {branch}")
    checked(["git", "add", "--", "codex_jobs/tools/p3d27/results",
             "team/art/dorfmap_grundgeruest/relief3d/pruefung/ERGEBNIS_p3d27.md"],
            label=f"git add round {round_no}")
    checked(["git", "commit", "-m", f"p3d27: record V3 Float32 probe round {round_no:02d}"],
            label=f"git commit round {round_no}")
    checked(["git", "push", "origin", "art/dorfmap-p3d27"], label=f"git push round {round_no}")


def gate_score(probe: dict, solution: dict) -> tuple[int, dict]:
    rules = probe.get("rules_by_rule", {})
    d1 = probe.get("rules_by_tile", {}).get("D1", {})
    r8 = probe.get("R8_by_rule", {})
    r9 = probe.get("R9_by_rule", {})
    # Compare against the p3d17 replay in the current checker schema. The
    # historical 596 total omits G11; current-schema rules absent from that
    # replay start at zero so newly emitted rule names are still bounded.
    baseline_rules = json.loads(BASELINE_RULES.read_text(encoding="utf-8")).get("je_regel", {})
    r3_limits = {"R3_laengs_m": 6, "R3_quer_pct": 17, "R3_woelb_m": 19}
    rule_limits = {k: int(baseline_rules.get(k, 0)) + 5
                   for k in sorted(set(baseline_rules) | set(rules))}
    r8_limits = {"R8_stufe": 14, "R8_gitter": 15, "R8_quer": 10, "R8a_wegende": 29}
    r9_limits = {"R8b_delle": 30, "R9_saegezahn": 39, "R9w_wellen": 280}
    excess = {}
    for name, limit in rule_limits.items():
        excess[f"rule:{name}"] = max(0, int(rules.get(name, 0)) - limit)
    for name, limit in r8_limits.items():
        excess[f"R8:{name}"] = max(0, int(r8.get(name, 0)) - limit)
    for name, limit in r9_limits.items():
        excess[f"R9:{name}"] = max(0, int(r9.get(name, 0)) - limit)
    for name, limit in r3_limits.items():
        excess[f"D1:{name}"] = max(0, int(d1.get(name, 0)) - limit)
    excess.update(hard_target_excess(probe, solution))
    return sum(excess.values()), excess


def hard_target_excess(probe: dict, solution: dict) -> dict:
    rules = probe.get("rules_by_rule", {})
    tiles = probe.get("rules_by_tile", {})
    d1 = tiles.get("D1", {})
    r8_d1 = probe.get("R8_by_tile", {}).get("D1", {})
    r9_d1 = probe.get("R9_by_tile", {}).get("D1", {})
    crossing = probe.get("R8_crossing_gate", {})
    crossing_metrics = crossing.get("official_cluster", {})
    crossing_quer = crossing.get("R8_quer_hit")
    baseline = json.loads(BASELINE_RULES.read_text(encoding="utf-8"))
    baseline_d2 = {}
    for hit in baseline.get("treffer", []):
        if hit.get("feld") == "D2":
            rule = str(hit.get("regel", ""))
            baseline_d2[rule] = baseline_d2.get(rule, 0) + 1
    d2_now = tiles.get("D2", {})
    d2_new_hits = sum(max(0, int(count) - int(baseline_d2.get(rule, 0)))
                      for rule, count in d2_now.items())
    d2_r8 = probe.get("R8_by_tile", {}).get("D2", {})
    d2_r9 = probe.get("R9_by_tile", {}).get("D2", {})
    d2_r8r9_hits = sum(int(count) for count in d2_r8.values()) + sum(int(count) for count in d2_r9.values())
    endpoint_stage_violation = float(solution.get("family_max_relaxation_locations", {})
                                     .get("endpoint_stage", {})
                                     .get("maximum_violation_m", 0.0))
    return {
        "target:R5_spitze_D1": int(d1.get("R5_spitze", 0)),
        "target:G6_D1": max(0, int(d1.get("G6_facette", 0)) - 3),
        "target:R8b_D1": max(0, int(r9_d1.get("R8b_delle", 0)) - 1),
        "target:G3_D1": max(0, int(d1.get("G3_spitze_unten", 0))
                              + int(d1.get("G3_spitze_unten_fein", 0)) - 1),
        "target:R9w_total": max(0, int(probe.get("R9_by_rule", {}).get("R9w_wellen", 0)) - 280),
        "target:G5_total": max(0, int(rules.get("G5_beule_klippe", 0)) - 69),
        "target:G5_D1": max(0, int(d1.get("G5_beule_klippe", 0)) - 2),
        "target:R5_loch_total": max(0, int(rules.get("R5_loch", 0)) - 22),
        "target:R5_loch_D1": max(0, int(d1.get("R5_loch", 0)) - 5),
        "target:R4_schlucht_D1": int(d1.get("R4_schlucht", 0)),
        "target:R8_crossing_stage": max(0, float(crossing_metrics.get("stufe", 0.0)) - 0.116),
        "target:R8_crossing_gitter": max(0, float(crossing_metrics.get("gitter", 0.0)) - 0.020),
        "target:R8_crossing_quer": (0 if crossing_quer is None
                                    else max(0, float(crossing_quer.get("wert", 0.0)) - 3.0)),
        "target:single_quer_over_20": max(0.0, float(solution.get("slack_values", {})
                                                     .get("safety_single_quer_extra_pp", 0.0)) - 0.5),
        "target:R8a_D1_unpermitted": int(r8_d1.get("R8a_wegende", 0)),
        "target:endpoint_stage_model_violation": max(0.0, endpoint_stage_violation),
        "target:D2_new_pruefe_regeln_hits": d2_new_hits,
        "target:D2_R8_R9_hits": d2_r8r9_hits,
        "target:G1_hash_changed": int(probe.get("G1_height_sha256")
                                       != "38afeb304c9aefec48cbfdc8a90fe11c7fa08e3080147730deb9be5d666a4bfb"),
        "target:D2_hash_changed": int(probe.get("D2_height_sha256")
                                       != "749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6"),
    }


def source_object(data: dict, hit: dict) -> tuple[list, int]:
    kind = str(hit.get("art", ""))
    if kind not in G11_KINDS:
        raise RuntimeError(f"G11-Typ nicht erkannt: {kind!r}")
    x, z = float(hit["x"]), float(hit["z"])
    candidates = []
    for index, item in enumerate(data.get(kind, [])):
        try:
            dx, dz = float(item[0]) - x, float(item[2]) - z
        except (TypeError, ValueError, IndexError):
            continue
        candidates.append((dx * dx + dz * dz, index, item))
    if not candidates:
        raise RuntimeError(f"Kein Objekt fuer G11-Treffer {kind}@{x}|{z}")
    distance2, index, item = min(candidates)
    if distance2 > 0.006:
        raise RuntimeError(f"G11-Objektzuordnung zu ungenau: {kind}@{x}|{z}, d2={distance2}")
    return item, index


def g11_cuts(probe: dict, existing: list[dict]) -> tuple[list[dict], int]:
    relief_path = Path(probe["probe_relief"])
    data = json.loads(gzip.decompress(relief_path.read_bytes()))
    baseline = json.loads(BASELINE_RULES.read_text(encoding="utf-8"))
    old = [h for h in baseline.get("treffer", [])
           if h.get("feld") == "D1" and h.get("regel") == "G11_objekt_schwebt_sinkt"]
    old_keys = {(h.get("art"), round(float(h.get("x", 0)), 1), round(float(h.get("z", 0)), 1)) for h in old}
    seen = {(c.get("art"), round(float(c["point"][0]), 1), round(float(c["point"][1]), 1))
            for c in existing if c.get("kind") == "G11"}
    hits = [h for h in probe.get("rules_D1_hits", [])
            if h.get("regel") == "G11_objekt_schwebt_sinkt"]
    new = []
    for hit in sorted(hits, key=lambda h: (str(h.get("art")), float(h["x"]), float(h["z"]))):
        key = (hit.get("art"), round(float(hit["x"]), 1), round(float(hit["z"]), 1))
        if key in old_keys or key in seen:
            continue
        item, index = source_object(data, hit)
        cut = {
            "kind": "G11", "point": [float(item[0]), float(item[2])],
            "object_height_m": float(item[1]), "art": str(hit.get("art")),
            "source_object_index": int(index), "probe_hit": hit,
        }
        new.append(cut)
        seen.add(key)
    return new, len(hits)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != EXPECTED_SOURCE_SHA256:
        raise RuntimeError(f"V3-Reliefquelle fehlt oder hat unerwarteten Hash: {SOURCE}")
    if hashlib.sha256(TRANSFER.read_bytes()).hexdigest() != EXPECTED_TRANSFER_SHA256:
        raise RuntimeError(f"V3-Transferbasis hat unerwarteten Hash: {TRANSFER}")
    base = json.loads(BASE_CUTS.read_text(encoding="utf-8"))
    dump(EMPTY_CUTS, base)
    old = json.loads(BASELINE_RULES.read_text(encoding="utf-8"))
    baseline_d1_g11 = sum(h.get("feld") == "D1" and h.get("regel") == "G11_objekt_schwebt_sinkt"
                          for h in old.get("treffer", []))
    rounds = []
    all_cuts = list(base)
    seen_cut_hashes = set()
    best_score = None
    best_round = None
    no_improve = 0
    for round_index in range(1, 7):
        round_name = f"V3_round{round_index:02d}"
        cuts_path = RESULTS / f"p3d27_{round_name}_cuts.json"
        dump(cuts_path, all_cuts)
        solution_path = RESULTS / f"p3d27_{round_name}_model.json"
        solve_cmd = [
            sys.executable, str(TOOLS / "run_diagnostic.py"),
            "--geometry", "V3", "--scenario", "joint",
            "--source-relief", str(SOURCE), "--transfer-base", str(TRANSFER),
            "--r8-center", "152.6292918620858", "28.353590994151514",
            "--event-cuts", str(cuts_path), "--out", str(solution_path),
            "--time-limit", "600", "--keep-solution",
        ]
        checked(solve_cmd, label=f"solve {round_name}")
        solution = json.loads(solution_path.read_text(encoding="utf-8"))
        if not solution.get("primal_feasible"):
            record = {"round": round_index, "model_status": solution.get("status"),
                      "model_status_code": solution.get("status_code"),
                      "primal_feasible": False, "model_slack_values": solution.get("slack_values"),
                      "cuts_before": len(all_cuts), "solution_json": str(solution_path)}
            rounds.append(record)
            status = f"nach Runde {round_index} beendet: kein machbarer Modellpunkt ({solution.get('status')})"
            record["stop_reason"] = "no_primal_feasible_solution"
            dump(RESULTS / "p3d27_V3_checker_loop.json",
                 output_document(rounds, best_round, best_score, len(all_cuts), status, baseline_d1_g11))
            write_report_progress(rounds, status)
            checkpoint(round_index)
            break
        probe_path = RESULTS / f"p3d27_{round_name}_official_probe.json"
        checked([sys.executable, str(TOOLS / "probe_direct_transfer.py"), str(solution_path),
                 str(TRANSFER), str(probe_path)], label=f"official probe {round_name}")
        probe = json.loads(probe_path.read_text(encoding="utf-8"))
        derived_path = RESULTS / f"p3d27_{round_name}_derived_cuts.json"
        derivation = checked([sys.executable, str(DERIVER), str(probe_path), str(derived_path)],
                             label=f"component derivation {round_name}")
        derived = json.loads(derived_path.read_text(encoding="utf-8"))
        g5_r5_new = [cut for cut in derived if cut.get("kind") in {"G5", "R5"}]
        new_g11, g11_d1_count = g11_cuts(probe, all_cuts)
        next_cuts = [*all_cuts, *g5_r5_new, *new_g11]
        dedup = {}
        for cut in next_cuts:
            key = json.dumps(cut, sort_keys=True, separators=(",", ":"))
            dedup[key] = cut
        next_cuts = [dedup[key] for key in sorted(dedup)]
        score, score_parts = gate_score(probe, solution)
        g5 = probe.get("rules_by_rule", {}).get("G5_beule_klippe", 0)
        r5 = probe.get("rules_by_rule", {}).get("R5_loch", 0)
        g11 = probe.get("rules_by_rule", {}).get("G11_objekt_schwebt_sinkt", 0)
        d1 = probe.get("rules_by_tile", {}).get("D1", {})
        round_record = {
            "round": round_index, "model_status": solution.get("status"),
            "model_status_code": solution.get("status_code"),
            "primal_feasible": solution.get("primal_feasible"),
            "optimality_proven": solution.get("optimality_proven"),
            "model_weighted_l1": solution.get("weighted_l1_value"),
            "model_slack_values": solution.get("slack_values"),
            "model_maximum_normalized_slack": solution.get("maximum_normalized_slack"),
            "official_rules_total": probe.get("rules_total"),
            "official_G5_total_D1": [g5, d1.get("G5_beule_klippe", 0)],
            "official_R5_loch_total_D1": [r5, d1.get("R5_loch", 0)],
            "official_R4_schlucht_total_D1": [probe.get("rules_by_rule", {}).get("R4_schlucht", 0), d1.get("R4_schlucht", 0)],
            "official_G11_total_D1": [g11, g11_d1_count],
            "official_R8_total_by_rule": {"total": probe.get("R8_total"), **probe.get("R8_by_rule", {})},
            "official_R8_D1_by_rule": probe.get("R8_by_tile", {}).get("D1", {}),
            "official_R8_by_tile_D1_G1_D2": {
                tile: probe.get("R8_by_tile", {}).get(tile, {}) for tile in ("D1", "G1", "D2")
            },
            "official_R9_total_by_rule": {"total": probe.get("R9_total"), **probe.get("R9_by_rule", {})},
            "official_R9_D1_by_rule": probe.get("R9_by_tile", {}).get("D1", {}),
            "official_R9_by_tile_D1_G1_D2": {
                tile: probe.get("R9_by_tile", {}).get(tile, {}) for tile in ("D1", "G1", "D2")
            },
            "official_rules_by_tile_D1_G1_D2": {
                tile: probe.get("rules_by_tile", {}).get(tile, {}) for tile in ("D1", "G1", "D2")
            },
            "official_R3_D1": {k: int(d1.get(k, 0)) for k in ("R3_laengs_m", "R3_quer_pct", "R3_woelb_m")},
            "official_R8_D1_crossing_stage": [h for h in probe.get("R8_D1_hits", [])
                                                 if "stufe" in str(h.get("regel", "")).lower()],
            "official_R8_D1_endpoint": [h for h in probe.get("R8_D1_hits", [])
                                         if "wegende" in str(h.get("regel", "")).lower()],
            "R8_crossing_gate": probe.get("R8_crossing_gate", {}),
            "R8a_hits_by_tile": probe.get("R8a_hits_by_tile", {}),
            "endpoint_stage_model": solution.get("family_max_relaxation_locations", {}).get("endpoint_stage"),
            "single_quer_slack_pp": solution.get("slack_values", {}).get("safety_single_quer_extra_pp"),
            "hard_target_excess": hard_target_excess(probe, solution),
            "fresh_component_derivation": derivation.stdout,
            "new_G5_cuts": sum(c.get("kind") == "G5" for c in g5_r5_new),
            "new_R5_cuts": sum(c.get("kind") == "R5" for c in g5_r5_new),
            "new_G11_cuts": len(new_g11), "cuts_before": len(all_cuts),
            "cuts_after": len(next_cuts), "score": score, "score_excess_by_gate": score_parts,
            "solution_json": str(solution_path), "probe_json": str(probe_path),
            "cut_json": str(cuts_path), "derived_cut_json": str(derived_path),
        }
        rounds.append(round_record)
        if best_score is None or score < best_score:
            best_score, best_round, no_improve = score, round_index, 0
        else:
            no_improve += 1
        cut_hash = hashlib.sha256(json.dumps(next_cuts, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        stop_reason = None
        if score == 0:
            stop_reason = "all_targets_passed"
        elif cut_hash in seen_cut_hashes:
            stop_reason = "cut_cycle"
        elif len(next_cuts) == len(all_cuts):
            stop_reason = "no_new_cuts"
        elif no_improve >= 2:
            stop_reason = "two_rounds_without_score_improvement"
        elif round_index == 6:
            stop_reason = "six_round_limit"
        if stop_reason is not None:
            round_record["stop_reason"] = stop_reason
        else:
            all_cuts = next_cuts
        next_cuts_path = RESULTS / f"p3d27_{round_name}_next_cuts.json"
        dump(next_cuts_path, next_cuts)
        round_record["next_cut_json"] = str(next_cuts_path)
        if score == 0:
            status = f"alle angeforderten Gate-Ziele nach Runde {round_index} erfüllt"
        elif stop_reason:
            status = f"nach Runde {round_index} beendet ({stop_reason}); Zielabweichungen sind in der Tabelle aufgeführt"
        else:
            status = f"Runde {round_index} abgeschlossen; Checker-in-the-loop wird fortgesetzt"
        dump(RESULTS / "p3d27_V3_checker_loop.json",
             output_document(rounds, best_round, best_score, len(all_cuts), status, baseline_d1_g11))
        write_report_progress(rounds, status)
        checkpoint(round_index)
        if cut_hash in seen_cut_hashes:
            break
        seen_cut_hashes.add(cut_hash)
        if stop_reason is not None:
            break
    out = RESULTS / "p3d27_V3_checker_loop.json"
    print(json.dumps({"out": str(out), "rounds": len(rounds), "best_round": best_round,
                      "best_score": best_score, "last_model_status": rounds[-1].get("model_status") if rounds else None},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
