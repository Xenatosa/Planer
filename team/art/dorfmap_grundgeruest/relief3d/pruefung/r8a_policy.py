"""Shared, narrowly scoped R8a runout threshold policy.

The sole exception, ``R8a_ausnahme_rampe2_start``, is authorized by Fabian
([F] widget t166s961, 2026-11-13): 0.18 m for the 4 m runout pairs belonging
to the start of rampe_2 at map coordinate 126.51|31.62. All other endpoints
retain 0.10 m. The 1e-6 coordinate tolerance covers serialization noise; it
is not a spatial search radius.
"""
from __future__ import annotations

from math import isclose
from typing import Sequence

R8A_DEFAULT_LIMIT_M = 0.10
R8A_RAMPE2_START_LIMIT_M = 0.18
R8A_RAMPE2_START_EXCEPTION = "R8a_ausnahme_rampe2_start"
R8A_RAMPE2_START_ENDPOINT_ID = "rampe_2_anfang"
R8A_RAMPE2_START_XZ = (126.51, 31.62)
R8A_COORD_TOLERANCE_M = 1e-6


def r8a_exception_for_endpoint(wegend_id: str, point_xz: Sequence[float]) -> str | None:
    """Return the exception name only for the named endpoint at its exact start."""
    if wegend_id != R8A_RAMPE2_START_ENDPOINT_ID or len(point_xz) != 2:
        return None
    if all(isclose(float(actual), expected, rel_tol=0.0, abs_tol=R8A_COORD_TOLERANCE_M)
           for actual, expected in zip(point_xz, R8A_RAMPE2_START_XZ)):
        return R8A_RAMPE2_START_EXCEPTION
    return None


def r8a_pair_limit_m(wegend_id: str, point_xz: Sequence[float]) -> float:
    """Select the official limit for a pair measured inside this endpoint runout."""
    if r8a_exception_for_endpoint(wegend_id, point_xz) is not None:
        return R8A_RAMPE2_START_LIMIT_M
    return R8A_DEFAULT_LIMIT_M


def r8a_pair_is_hit(delta_m: float, wegend_id: str, point_xz: Sequence[float]) -> bool:
    """Apply the checker's strict greater-than comparison at the selected limit."""
    return float(delta_m) > r8a_pair_limit_m(wegend_id, point_xz)
