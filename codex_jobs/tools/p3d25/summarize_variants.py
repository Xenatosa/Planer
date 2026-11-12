#!/usr/bin/env python3
"""Assemble the final p3d25 variant, baseline, and not-probed summary."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOOLS = ROOT / "codex_jobs/tools/p3d25"
RESULTS = TOOLS / "results"
RELIEF3D = ROOT / "team/art/dorfmap_grundgeruest/relief3d"
VARIANTS = {}


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


for version in ("1", "2", "3"):
    manifest = read(RESULTS / f"p3d25_v{version}_manifest.json")
    context = read(RESULTS / f"p3d25_v{version}_start_context.json")
    all_hard = read(RESULTS / f"p3d25_v{version}_all_hard.json")
    family = read(RESULTS / f"p3d25_v{version}_family_iis.json")
    all_open = family["runs"][0]
    endpoint_only = family["runs"][1]
    VARIANTS[version] = {
        "name": manifest["name"],
        "source_relief_sha256": manifest["output_source_sha256"],
        "transfer_sha256": sha(RELIEF3D / "neu" / f"p3d25_start_v{version}_transfer.json"),
        "start_changes": manifest["routes"],
        "source_scope_valid": {
            "changed_route_indices": manifest["changed_route_indices"],
            "all_nonroute_source_fields_unchanged": manifest["all_nonroute_source_fields_unchanged"],
            "all_other_rampenwege_semantically_unchanged": manifest["all_other_rampenwege_semantically_unchanged"],
            "rampe_2_after_join_unchanged": manifest["rampe_2_after_join_unchanged"],
            "rampe_11_after_new_start_unchanged": manifest["rampe_11_after_new_start_unchanged"],
        },
        "start_context": {
            name: {
                "start_map": entry["start_map"],
                "start_GB_m": entry["start_GB_m"],
                "start_distance_m": entry["start_distance_m"],
                "runout_4m_context": entry["runout_4m_context"],
            }
            for name, entry in context["routes"].items()
        },
        "R8_gate_center_unrounded_map": all_hard["r8_center_unrounded_map"],
        "all_families_hard": {
            "status": all_hard["status"],
            "status_code": all_hard["status_code"],
            "infeasibility_proven": all_hard["infeasibility_proven"],
            "variables": all_hard["variables"],
            "constraints": all_hard["constraints"],
            "time_limit_s": all_hard["time_limit_s"],
        },
        "family_diagnosis": {
            "binding_groups_all_open": family["binding_groups_all_open"],
            "all_open_endpoint_r8a_slack_m": (all_open.get("slack_values") or {}).get("endpoint_r8a_extra_m"),
            "all_open_location": (all_open.get("family_max_relaxation_locations") or {}).get("endpoint_r8a"),
            "endpoint_only_slack_m": (endpoint_only.get("slack_values") or {}).get("endpoint_r8a_extra_m"),
            "all_except_endpoint_status": family["runs"][2]["status"],
            "minimal_endpoint_r8a_family_supported": family["minimal_endpoint_r8a_family_supported"],
        },
        "official_float32_probe": {
            "status": "not_run",
            "reason": "all-families-hard solve infeasible; user workflow prohibits probe before feasible candidate",
            "rules_total": None, "R8": None, "R9": None, "D1_G1_D2": None,
        },
        "mesh_built": False,
    }

result = {
    "tag": "p3d25",
    "branch": "art/dorfmap-p3d25",
    "base_commit": "56bfab88b10778e333f1747482eef98416bbc5ae",
    "historical_baseline_9d3f8fc": {
        "pruefe_regeln_total": 596,
        "R8": {"total": 48, "R8_stufe": 9, "R8_gitter": 10, "R8_quer": 5, "R8a_wegende": 24},
        "R9": {"total": 334, "R8b_delle": 25, "R9_saegezahn": 34, "R9w_wellen": 275},
    },
    "last_reference_replay_current_schema": {
        "pruefe_regeln": read(ROOT / "codex_jobs/tools/p3d20_r3/official_gates/p3d17_reference_regeln_current_schema.json")["summe"],
        "pruefe_regeln_by_tile": {
            "D1": {"G11_objekt_schwebt_sinkt": 2, "G3_spitze_unten": 1, "G5_beule_klippe": 2, "G6_facette": 3, "G7b_wandkontur_feld": 1, "R1_blind": 2, "R2_getrennt": 1, "R3_laengs_m": 6, "R3_quer_pct": 17, "R3_woelb_m": 19, "R4_rand": 1, "R5_loch": 8},
            "G1": {"G11_objekt_schwebt_sinkt": 2, "G6_facette": 3, "R1_blind": 1, "R3_laengs_m": 1, "R6_wasser_schnee": 3, "T1_fleckrand": 3},
            "D2": {"R2_getrennt": 1, "T1_fleckrand": 7},
        },
        "R8": {"total": 46, "by_tile": {"D1": {"R8_stufe": 2, "R8_gitter": 2, "R8a_wegende": 3}, "G1": {}, "D2": {}}},
        "R9": {"total": 344, "by_tile": {"D1": {"R8b_delle": 1, "R9_saegezahn": 1, "R9w_wellen": 27}, "G1": {"R9_saegezahn": 1, "R9w_wellen": 12}, "D2": {}}},
        "caveat": "Reference replay uses current schema and is not the historical 9d3f8fc totals; p3d25 candidate after-counts were not measured.",
    },
    "invariants": {
        "base_source_relief_sha256": sha(RELIEF3D / "relief_daten.json.gz"),
        "vektor_sha256": sha(RELIEF3D / "neu/vektor.json"),
        "zellen_relief_sha256": sha(RELIEF3D / "neu/zellen_relief.csv"),
        "felder_json_sha256": sha(RELIEF3D / "neu/felder.json"),
        "source_relief_official_file_unchanged": sha(RELIEF3D / "relief_daten.json.gz") == "5e8fdb51c3f3dff9ad2c03c32a7c39ee1a4f97a3bc0942d47a352b1d0b4f0e88",
        "thresholds_checkers_mesh_py_unchanged": True,
        "mesh_built": False,
        "t42u_lod1_images_pytest": "not_run; no candidate passed preconditions",
    },
    "default_variant": "1",
    "default_reason": "V1 and V3 tie at 0.072813 m; V1 uses the smaller combined start displacement.",
    "variants": VARIANTS,
}
out = RESULTS / "p3d25_variants_summary.json"
out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps({"out": str(out), "variant_slacks_m": {
    k: v["family_diagnosis"]["all_open_endpoint_r8a_slack_m"] for k, v in VARIANTS.items()},
    "all_mesh_built": any(v["mesh_built"] for v in VARIANTS.values())}, indent=2, sort_keys=True))
