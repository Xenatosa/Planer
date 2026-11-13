"""Regression tests for the single p3d26 R8a runout exception."""
from __future__ import annotations

import gzip
import json
from pathlib import Path

from r8a_policy import (
    R8A_RAMPE2_START_ENDPOINT_ID,
    R8A_RAMPE2_START_XZ,
    R8A_RAMPE2_START_EXCEPTION,
    r8a_exception_for_endpoint,
    r8a_pair_is_hit,
    r8a_pair_limit_m,
)


def test_rampe2_start_exception_thresholds_and_exact_scope() -> None:
    endpoint = R8A_RAMPE2_START_ENDPOINT_ID
    point = R8A_RAMPE2_START_XZ
    assert r8a_exception_for_endpoint(endpoint, point) == R8A_RAMPE2_START_EXCEPTION
    assert r8a_pair_limit_m(endpoint, point) == 0.18
    assert not r8a_pair_is_hit(0.17, endpoint, point)
    assert r8a_pair_is_hit(0.19, endpoint, point)
    assert r8a_pair_limit_m(endpoint, (126.51, 31.62001)) == 0.10
    assert r8a_pair_is_hit(0.11, endpoint, (126.51, 31.62001))


def test_every_other_ramp_endpoint_keeps_the_010_m_limit() -> None:
    relief_path = Path(__file__).resolve().parents[1] / "relief_daten.json.gz"
    data = json.loads(gzip.decompress(relief_path.read_bytes()))
    rampe2_start = data["rampenwege"][2][0]
    assert all(abs(float(actual) - expected) <= 1e-6
               for actual, expected in zip(rampe2_start, R8A_RAMPE2_START_XZ))
    assert r8a_pair_limit_m("rampe_2_anfang", rampe2_start) == 0.18
    checked = []
    for index, route in enumerate(data["rampenwege"]):
        for label in ("anfang", "ende"):
            endpoint_id = f"rampe_{index}_{label}"
            if endpoint_id == R8A_RAMPE2_START_ENDPOINT_ID:
                continue
            coordinate = route[0] if label == "anfang" else route[-1]
            assert r8a_pair_limit_m(endpoint_id, coordinate) == 0.10
            assert r8a_pair_is_hit(0.11, endpoint_id, coordinate), endpoint_id
            checked.append(endpoint_id)
    assert checked
