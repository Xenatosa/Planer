#!/usr/bin/env python3
"""Deterministic p3d29 work area and V3-guided Priority-Flood construction."""
from __future__ import annotations

import heapq
import base64

import numpy as np
from scipy import ndimage as ndi
from scipy.spatial import cKDTree

CELL_M = 1.2
ROUTE_PAIR_RADIUS_M = 4.5
P3D17_ROUTE_BAND_M = 1.81
ROUTE_FORM_BAND_M = 4.8
CROSSING_RADIUS_MAP = 4.0
RUNOUT_ALONG_MAP = (-1.0, 4.0)
RUNOUT_ACROSS_MAP = 2.5
RING_VARIANTS_M = {"3": 7.5}


def _bresenham(ix0: int, iz0: int, ix1: int, iz1: int) -> list[tuple[int, int]]:
    """Return every 8-connected raster node along a segment, including ends."""
    points: list[tuple[int, int]] = []
    x, z = ix0, iz0
    dx, dz = abs(ix1 - ix0), abs(iz1 - iz0)
    sx = 1 if ix0 < ix1 else -1
    sz = 1 if iz0 < iz1 else -1
    err = dx - dz
    while True:
        points.append((x, z))
        if x == ix1 and z == iz1:
            break
        twice = 2 * err
        if twice > -dz:
            err -= dz
            x += sx
        if twice < dx:
            err += dx
            z += sz
    return points


def _route_chain(profile: dict, x0: float, z0: float, x1: float, z1: float,
                 fs: int, width: int, height: int, active: np.ndarray,
                 flood_surface: np.ndarray) -> tuple[list[int], bool, list[float]]:
    coords = np.asarray(profile["coords"], dtype=np.float64)
    raw_inside = np.flatnonzero(
        (coords[:, 0] >= x0 - 1e-9) & (coords[:, 0] <= x1 + 1e-9)
        & (coords[:, 1] >= z0 - 1e-9) & (coords[:, 1] <= z1 + 1e-9)
    )
    if len(raw_inside) < 2:
        return [], False, []
    grid_nodes: list[int] = []
    raw_index_by_node: dict[int, int] = {}
    for k in raw_inside.tolist():
        ix = int(round((float(coords[k, 0]) - x0) * fs))
        iz = int(round((float(coords[k, 1]) - z0) * fs))
        if not (0 <= ix < width and 0 <= iz < height and active[iz, ix]):
            continue
        node = iz * width + ix
        if not grid_nodes or node != grid_nodes[-1]:
            grid_nodes.append(node)
            raw_index_by_node[node] = k
    if len(grid_nodes) < 2:
        return grid_nodes, False, []

    first_z, first_x = divmod(grid_nodes[0], width)
    last_z, last_x = divmod(grid_nodes[-1], width)
    first_h = float(flood_surface[first_z, first_x])
    last_h = float(flood_surface[last_z, last_x])
    downstream_is_first = first_h <= last_h
    ordered = list(reversed(grid_nodes)) if downstream_is_first else list(grid_nodes)
    low_node = ordered[-1]
    low_raw_index = raw_index_by_node[low_node]
    if downstream_is_first:
        interior_index = min(low_raw_index + 1, len(coords) - 1)
    else:
        interior_index = max(low_raw_index - 1, 0)
    q = coords[low_raw_index]
    direction = q - coords[interior_index]
    norm = float(np.hypot(*direction))
    if norm > 1e-12:
        direction /= norm
        extension = []
        previous = low_node
        for step in range(1, 121):  # at most 30 map units; stop at first work-area edge
            point = q + direction * (0.25 * step)
            ix = int(round((float(point[0]) - x0) * fs))
            iz = int(round((float(point[1]) - z0) * fs))
            if not (0 <= ix < width and 0 <= iz < height and active[iz, ix]):
                break
            node = iz * width + ix
            if node != previous:
                extension.append(node)
                previous = node
        ordered.extend(extension)

    # Fill any raster gap, retaining only nodes inside the already defined band.
    expanded: list[int] = []
    for node in ordered:
        if not expanded:
            expanded.append(node)
            continue
        pz, px = divmod(expanded[-1], width)
        nz, nx = divmod(node, width)
        segment = _bresenham(px, pz, nx, nz)
        for sx, sz in segment[1:]:
            if 0 <= sx < width and 0 <= sz < height and active[sz, sx]:
                idx = sz * width + sx
                if idx != expanded[-1]:
                    expanded.append(idx)
    ref_h = [float(flood_surface[divmod(i, width)]) for i in expanded]
    return expanded, downstream_is_first, ref_h


def _assert_acyclic(parent: np.ndarray, active: np.ndarray, width: int) -> None:
    height = active.shape[0]
    state = np.zeros(len(parent), dtype=np.uint8)
    for start in np.flatnonzero(active.ravel()):
        if state[start] == 2:
            continue
        path: list[int] = []
        node = int(start)
        while node >= 0 and state[node] == 0:
            state[node] = 1
            path.append(node)
            nxt = int(parent[node])
            if nxt >= len(parent):
                raise RuntimeError("Priority-Flood parent index is outside the D1 grid")
            if nxt >= 0:
                nz, nx = divmod(nxt, width)
                if not (0 <= nz < height and 0 <= nx < width and active[nz, nx]):
                    raise RuntimeError("Priority-Flood edge leaves the active work area")
            node = nxt
        if node >= 0 and state[node] == 1:
            raise RuntimeError(f"Drainage parent cycle reaches flat index {node}")
        for item in path:
            state[item] = 2


def build(data: dict, profiles: list[dict], reference: np.ndarray,
          reference_full: np.ndarray, *, drainage_surface: np.ndarray,
          transfer_support: np.ndarray,
          endpoint_support: np.ndarray,
          x0: float, z0: float,
          x1: float, z1: float, fs: int, ring_variant: str,
          drainage_eps_m: float) -> dict:
    if ring_variant not in RING_VARIANTS_M:
        raise ValueError(f"P3D29_CONSTRUCTION_VARIANT muss 1, 2 oder 3 sein, nicht {ring_variant!r}")
    if drainage_eps_m <= 0.0:
        raise ValueError("P3D29_DRAINAGE_EPS_M muss positiv sein")
    ring_width_m = RING_VARIANTS_M[ring_variant]
    height, width = reference.shape
    x_values = x0 + np.arange(width, dtype=np.float64) / fs
    z_values = z0 + np.arange(height, dtype=np.float64) / fs
    mz, mx = np.meshgrid(z_values, x_values, indexing="ij")

    route_points = []
    for profile in profiles:
        coords = np.asarray(profile["coords"], dtype=np.float64)
        inside = ((coords[:, 0] >= x0 - 1e-9) & (coords[:, 0] <= x1 + 1e-9)
                  & (coords[:, 1] >= z0 - 1e-9) & (coords[:, 1] <= z1 + 1e-9))
        route_points.extend(coords[inside].tolist())
    if not route_points:
        raise RuntimeError("V3 route axes do not intersect the D1 mesh")
    tree = cKDTree(np.asarray(route_points, dtype=np.float64) * CELL_M)
    route_distance_m = tree.query(np.column_stack((mx.ravel(), mz.ravel())) * CELL_M,
                                  k=1, workers=1)[0].reshape(reference.shape)
    route_core = route_distance_m <= ROUTE_PAIR_RADIUS_M + 1e-9
    crossing_distance_map = np.hypot(mx - 152.6292918620858, mz - 28.353590994151514)
    crossing_mask = crossing_distance_map <= CROSSING_RADIUS_MAP + 1e-9

    outflow_mask = np.zeros_like(route_core)
    for profile in profiles:
        coords = np.asarray(profile["coords"], dtype=np.float64)
        if len(coords) < 2:
            continue
        for at_start in (True, False):
            q = coords[0] if at_start else coords[-1]
            inside = coords[min(8, len(coords) - 1)] if at_start else coords[max(0, len(coords) - 9)]
            direction = q - inside
            direction /= max(float(np.hypot(*direction)), 1e-12)
            normal = np.array([-direction[1], direction[0]])
            dx, dz = mx - q[0], mz - q[1]
            along = dx * direction[0] + dz * direction[1]
            across = dx * normal[0] + dz * normal[1]
            outflow_mask |= ((along >= RUNOUT_ALONG_MAP[0] - 1e-9)
                             & (along <= RUNOUT_ALONG_MAP[1] + 1e-9)
                             & (np.abs(across) <= RUNOUT_ACROSS_MAP + 1e-9))
    if transfer_support.shape != reference.shape or endpoint_support.shape != reference.shape:
        raise RuntimeError("Transfer-/Endstuetze und D1-Referenz haben unterschiedliche Form")
    if drainage_surface.shape != reference.shape:
        raise RuntimeError("p3d26-Loesung und D1-Referenz haben unterschiedliche Form")
    # The exact nonzero V3 transfer support is recorded separately. Its broad
    # fade is not itself the construction work area: outside the family-derived
    # road/crossing/runout core and its transition ring, final heights are
    # pinned to p3d17, including where the unchanged transfer has support.
    transfer_mask = transfer_support > 0.0
    endpoint_mask = endpoint_support > 1e-6
    core = route_core | crossing_mask | outflow_mask | endpoint_mask
    ring_distance_m = ndi.distance_transform_edt(
        ~core, sampling=(CELL_M / fs, CELL_M / fs),
    )
    ring = (~core) & (ring_distance_m <= ring_width_m + 1e-9)
    active = core | ring
    ring_tolerance_m = np.zeros_like(ring_distance_m)
    if ring.any():
        fraction = np.clip(ring_distance_m[ring] / ring_width_m, 0.0, 1.0)
        ring_tolerance_m[ring] = 0.001 + (0.020 - 0.001) * (1.0 - fraction)

    rs = int(data["rs"])
    ny, nx = int(data["ny"]), int(data["nx"])
    wega_full = np.frombuffer(base64.b64decode(data["WEGA"]), dtype=np.uint8)
    wega_full = wega_full.reshape(ny * rs + 1, nx * rs + 1)
    global_ix = np.rint(x_values * rs).astype(int)
    global_iz = np.rint(z_values * rs).astype(int)
    road_mask = wega_full[np.ix_(global_iz, global_ix)] > 20
    zero_eps_mask = (crossing_mask | outflow_mask | endpoint_mask | road_mask
                     | (route_distance_m <= P3D17_ROUTE_BAND_M + 1e-9))
    flood_model_mask = core | road_mask
    flood_surface = reference.astype(np.float64, copy=True)
    flood_surface[flood_model_mask] = drainage_surface[flood_model_mask]

    gy, gx = np.gradient(reference_full.astype(np.float64), 1.0 / rs)
    wall = np.hypot(gx, gy) > 1.0
    wall_distance_m = ndi.distance_transform_edt(~wall) / rs * CELL_M
    wall_x0, wall_z0 = int(round(x0 * rs)), int(round(z0 * rs))
    wall_crop = wall_distance_m[wall_z0:wall_z0 + height, wall_x0:wall_x0 + width]
    if wall_crop.shape != reference.shape:
        raise RuntimeError("p3d17 wall field does not cover the D1 mesh")
    cliff_zone = active & ((wall_crop <= 6.0 + 1e-9) | (route_distance_m <= 4.8 + 1e-9))

    # Priority-Flood outward from every work-area boundary node. Its helper
    # surface uses the p3d26 V3 heights in road/crossing/runout cells and the
    # p3d17 reference elsewhere. Boundary nodes are outlets.
    boundary = active & ~ndi.binary_erosion(active, structure=np.ones((3, 3), dtype=bool), border_value=0)
    active_flat = active.ravel()
    flood_flat = flood_surface.ravel()
    parent = np.full(height * width, -1, dtype=np.int64)
    visited = np.zeros(height * width, dtype=bool)
    heap: list[tuple[float, int]] = []
    for iz, ix in zip(*np.nonzero(boundary)):
        idx = int(iz * width + ix)
        visited[idx] = True
        heapq.heappush(heap, (float(flood_flat[idx]), idx))
    neighbors = tuple((dz, dx) for dz in (-1, 0, 1) for dx in (-1, 0, 1)
                      if dz or dx)
    while heap:
        key, idx = heapq.heappop(heap)
        iz, ix = divmod(idx, width)
        for dz, dx in neighbors:
            nz, nx_ = iz + dz, ix + dx
            if not (0 <= nz < height and 0 <= nx_ < width):
                continue
            ni = nz * width + nx_
            if not active_flat[ni] or visited[ni]:
                continue
            visited[ni] = True
            parent[ni] = idx
            heapq.heappush(heap, (max(key, float(flood_flat[ni])), ni))
    if not np.array_equal(visited, active_flat):
        missing = int(np.count_nonzero(active_flat & ~visited))
        raise RuntimeError(f"Priority-Flood left {missing} active D1 vertices unvisited")

    route_edges: dict[int, tuple[int, int]] = {}
    route_details = []
    for profile in sorted(profiles, key=lambda item: int(item["index"])):
        chain, downstream_is_first, chain_ref = _route_chain(
            profile, x0, z0, x1, z1, fs, width, height, active, flood_surface,
        )
        if len(chain) < 2:
            route_details.append({"route": int(profile["index"]), "chain_nodes": len(chain),
                                  "outlet_on_boundary": bool(chain and boundary.ravel()[chain[-1]])})
            continue
        for child, next_node in zip(chain[:-1], chain[1:]):
            candidate = (next_node, int(profile["index"]))
            old = route_edges.get(child)
            if old is None or (flood_flat[next_node], candidate[1]) < (flood_flat[old[0]], old[1]):
                route_edges[child] = candidate
        outlet = chain[-1]
        if not boundary.ravel()[outlet]:
            # A clipping or rasterization corner can end the straight extension
            # before the edge; retain its already valid Priority-Flood parent.
            route_edges.pop(outlet, None)
        else:
            parent[outlet] = -1
        route_details.append({
            "route": int(profile["index"]), "chain_nodes": len(chain),
            "downhill_endpoint_is_route_start": bool(downstream_is_first),
            "priority_flood_start_to_end_m": [float(chain_ref[-1]), float(chain_ref[0])],
            "outlet_xz": [float(x0 + (outlet % width) / fs),
                          float(z0 + (outlet // width) / fs)],
            "outlet_on_boundary": bool(boundary.ravel()[outlet]),
        })
    for child, (next_node, _route_id) in route_edges.items():
        parent[child] = next_node
    _assert_acyclic(parent, active, width)

    edges = []
    for child in np.flatnonzero(active_flat):
        nxt = int(parent[child])
        if nxt < 0:
            continue
        edges.append((int(child), nxt,
                      0.0 if zero_eps_mask.ravel()[child] or zero_eps_mask.ravel()[nxt]
                      else float(drainage_eps_m)))

    return {
        "x0": float(x0), "z0": float(z0), "x1": float(x1), "z1": float(z1),
        "fs": int(fs), "width": int(width), "height": int(height),
        "ring_variant": ring_variant, "ring_width_m": float(ring_width_m),
        "route_radius_m": ROUTE_PAIR_RADIUS_M,
        "crossing_radius_map": CROSSING_RADIUS_MAP,
        "transfer_support_vertices": int(transfer_mask.sum()),
        "endpoint_support_vertices": int(endpoint_mask.sum()),
        "transfer_support_outside_active_vertices": int((transfer_mask & ~active).sum()),
        "p3d17_band_m": P3D17_ROUTE_BAND_M,
        "runout_along_map": list(RUNOUT_ALONG_MAP),
        "runout_across_map": RUNOUT_ACROSS_MAP,
        "drainage_eps_m": float(drainage_eps_m),
        "priority_flood_reference": "p3d26 V3 on route/crossing/runout work cells; p3d17 elsewhere",
        "priority_flood_height_m": flood_surface.astype(np.float32).tolist(),
        "priority_flood_model_mask": flood_model_mask.astype(np.uint8).tolist(),
        "reference_height_m": reference.astype(np.float32).tolist(),
        "core_mask": core.astype(np.uint8).tolist(),
        "ring_mask": ring.astype(np.uint8).tolist(),
        "active_mask": active.astype(np.uint8).tolist(),
        "ring_distance_m": ring_distance_m.astype(np.float32).tolist(),
        "ring_tolerance_m": ring_tolerance_m.astype(np.float32).tolist(),
        "zero_eps_mask": zero_eps_mask.astype(np.uint8).tolist(),
        "wall_cliff_gorge_mask": cliff_zone.astype(np.uint8).tolist(),
        "curvature_l1_mask": ((route_distance_m <= ROUTE_FORM_BAND_M + 1e-9)
                               | crossing_mask | outflow_mask | endpoint_mask).astype(np.uint8).tolist(),
        "priority_parent_flat": parent.tolist(),
        "drainage_edges_child_parent_eps": [list(edge) for edge in edges],
        "outlet_flat_indices": [int(v) for v in np.flatnonzero(boundary.ravel())],
        "route_edges": [[int(child), int(next_node), int(route_id)]
                        for child, (next_node, route_id) in sorted(route_edges.items())],
        "routes": route_details,
        "counts": {
            "core_vertices": int(core.sum()), "ring_vertices": int(ring.sum()),
            "transfer_support_vertices": int(transfer_mask.sum()),
            "endpoint_support_vertices": int(endpoint_mask.sum()),
            "transfer_support_outside_active_vertices": int((transfer_mask & ~active).sum()),
            "active_vertices": int(active.sum()),
            "outside_pinned_vertices": int((~active).sum()),
            "zero_eps_vertices": int(zero_eps_mask.sum()),
            "priority_flood_model_vertices": int(flood_model_mask.sum()),
            "curvature_l1_vertices": int(np.count_nonzero(
                (route_distance_m <= ROUTE_FORM_BAND_M + 1e-9)
                | crossing_mask | outflow_mask | endpoint_mask)),
            "wall_cliff_gorge_vertices": int(cliff_zone.sum()),
            "priority_flood_boundary_outlets": int(boundary.sum()),
            "drainage_edges": int(len(edges)),
            "route_longitudinal_edges": int(len(route_edges)),
            "route_outlets_on_work_area_boundary": sum(bool(r.get("outlet_on_boundary")) for r in route_details),
        },
    }
