#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]

ACTION_PATH = (
    ROOT
    / "sources/project41-paper42"
    / "project42_full_carrier_action_certificate_031.json"
)

ORBITAL_PATH = (
    ROOT
    / "sources/project41-paper42"
    / "all_one_oriented_frame_identification_audit_028p.json"
)

GROUP_PATH = (
    ROOT
    / "sources/project41-paper42"
    / "all_one_group_anatomy_audit_028o.json"
)

OUTPUT = (
    ROOT
    / "artifacts/json"
    / "project42_group_orbital_certificate_046.json"
)


Permutation = tuple[int, ...]


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def compose(left: Permutation, right: Permutation) -> Permutation:
    return tuple(left[right[index]] for index in range(len(left)))


def inverse(permutation: Permutation) -> Permutation:
    result = [0] * len(permutation)

    for source, target in enumerate(permutation):
        result[target] = source

    return tuple(result)


def subgroup_generated(
    generators: Iterable[Permutation],
    degree: int,
) -> frozenset[Permutation]:
    generators = tuple(generators)
    moves = generators + tuple(inverse(g) for g in generators)

    identity = tuple(range(degree))
    group = {identity}
    queue = [identity]

    while queue:
        current = queue.pop()

        for move in moves:
            candidate = compose(current, move)

            if candidate in group:
                continue

            group.add(candidate)
            queue.append(candidate)

    return frozenset(group)


def greedy_generators(
    universe: Iterable[Permutation],
    degree: int,
) -> tuple[Permutation, ...]:
    ordered = sorted(set(universe))
    generators: list[Permutation] = []
    subgroup = subgroup_generated(generators, degree)

    for candidate in ordered:
        if candidate in subgroup:
            continue

        generators.append(candidate)
        subgroup = subgroup_generated(generators, degree)

        if len(subgroup) == len(ordered):
            break

    if len(subgroup) != len(ordered):
        raise RuntimeError("greedy generator search did not close")

    return tuple(generators)


def edge_orbit(
    seed: tuple[int, int],
    group: Iterable[Permutation],
) -> tuple[tuple[int, int], ...]:
    edges = {
        tuple(sorted((
            permutation[seed[0]],
            permutation[seed[1]],
        )))
        for permutation in group
    }

    return tuple(sorted(edges))


def edge_digest(edges: Iterable[tuple[int, int]]) -> str:
    payload = json.dumps(
        [list(edge) for edge in edges],
        separators=(",", ":"),
    ).encode("ascii")

    return sha256_bytes(payload)


def main() -> None:
    action = json.loads(ACTION_PATH.read_text())
    orbital = json.loads(ORBITAL_PATH.read_text())
    anatomy = json.loads(GROUP_PATH.read_text())

    if not (
        action.get("audit_pass") is True
        and orbital.get("audit_pass") is True
        and anatomy.get("audit_pass") is True
    ):
        raise SystemExit("one or more source certificates do not pass")

    automorphisms = tuple(
        tuple(row["carrier_permutation"])
        for row in action["automorphisms"]
    )

    kernel_indices = tuple(
        action["derived"]["partition_action_kernel_indices"]
    )

    kernel = tuple(automorphisms[index] for index in kernel_indices)

    full_generators = greedy_generators(automorphisms, 30)
    kernel_generators = greedy_generators(kernel, 30)

    candidates = orbital["measurements"]["degree4_orbital_candidates"]

    orbital_rows = []

    for candidate in candidates:
        seed = tuple(candidate["seed_pair"])
        edges = edge_orbit(seed, kernel)

        orbital_rows.append({
            "orbit_index": candidate["orbit_index"],
            "seed_pair": list(seed),
            "subdegree": 4,
            "edge_count": len(edges),
            "component_sizes": candidate["component_sizes"],
            "triangle_count": candidate["triangle_count"],
            "bipartite": candidate["bipartite"],
            "selected_graph_X": candidate["equals_all_one"],
            "canonical_edge_sha256": edge_digest(edges),
            "edges": [list(edge) for edge in edges],
        })

    measurements = anatomy["measurements"]

    checks = {
        "source_action_pass": action.get("audit_pass") is True,
        "source_orbital_pass": orbital.get("audit_pass") is True,
        "source_group_pass": anatomy.get("audit_pass") is True,
        "automorphism_count_720":
            len(automorphisms) == 720,
        "kernel_count_120":
            len(kernel) == 120,
        "full_generators_generate_720":
            len(subgroup_generated(full_generators, 30)) == 720,
        "kernel_generators_generate_120":
            len(subgroup_generated(kernel_generators, 30)) == 120,
        "quartic_orbital_count_4":
            len(orbital_rows) == 4,
        "all_orbital_edge_counts_60":
            all(row["edge_count"] == 60 for row in orbital_rows),
        "unique_selected_graph":
            sum(
                1
                for row in orbital_rows
                if row["selected_graph_X"]
            ) == 1,
        "group_structure_S5_x_S3":
            measurements["kernel_is_S5_pass"] is True
            and measurements["centralizer_is_S3_pass"] is True
            and measurements["kernel_centralizer_intersection_order"] == 1
            and measurements["kernel_times_centralizer_order"] == 720,
    }

    payload = {
        "certificate_id":
            "project42_group_orbital_certificate_046",
        "audit_pass":
            all(checks.values()),
        "sources": {
            "full_action": {
                "path": str(ACTION_PATH.relative_to(ROOT)),
                "sha256": sha256_file(ACTION_PATH),
            },
            "oriented_frame": {
                "path": str(ORBITAL_PATH.relative_to(ROOT)),
                "sha256": sha256_file(ORBITAL_PATH),
            },
            "group_anatomy": {
                "path": str(GROUP_PATH.relative_to(ROOT)),
                "sha256": sha256_file(GROUP_PATH),
            },
        },
        "group": {
            "automorphism_count": 720,
            "structure": "S5_x_S3",
            "center_order": measurements["center_order"],
            "derived_subgroup_order":
                measurements["derived_subgroup_order"],
            "derived_subgroup_structure": "A5_x_C3",
            "abelianization_order":
                measurements["abelianization_order"],
            "abelianization_structure": "C2_x_C2",
            "partition_action_kernel_order": 120,
            "kernel_structure": "S5",
            "kernel_centralizer_order": 6,
            "kernel_centralizer_structure": "S3",
            "kernel_centralizer_intersection_order": 1,
            "full_generator_count": len(full_generators),
            "full_generators": [list(g) for g in full_generators],
            "kernel_generator_count": len(kernel_generators),
            "kernel_generators": [list(g) for g in kernel_generators],
            "full_element_order_distribution":
                measurements["full_element_order_distribution"],
        },
        "quartic_orbitals": orbital_rows,
        "checks": checks,
        "boundary": {
            "quartic_orbital_census_only": True,
            "all_self_paired_orbitals_of_other_valencies_classified":
                False,
            "global_quotient_frame_completeness_claimed": False,
            "external_standard_graph_name_claimed": False,
            "abstract_group_claim_changed": False,
        },
    }

    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )

    print("output:", OUTPUT)
    print("audit_pass:", payload["audit_pass"])
    print("full_generator_count:", len(full_generators))
    print("kernel_generator_count:", len(kernel_generators))

    for row in orbital_rows:
        print(
            "orbital",
            row["orbit_index"],
            "seed",
            row["seed_pair"],
            "edges",
            row["edge_count"],
            "selected",
            row["selected_graph_X"],
            "sha256",
            row["canonical_edge_sha256"],
        )

    print("sha256:", sha256_file(OUTPUT))


if __name__ == "__main__":
    main()
