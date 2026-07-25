#!/usr/bin/env python3
"""Classify automorphisms of the full weighted C2^3 orbit skeleton."""

import json
from collections import Counter
from itertools import permutations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

QUOTIENT_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_c2_cube_orbit_quotient_017.json"
)

SIMPLE_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_c2_orbit_skeleton_018.json"
)

OUTPUT = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_weighted_orbit_skeleton_019.json"
)


def canonical_pair(left, right):
    return tuple(sorted((left, right)))


def permutation_order(permutation):
    identity = tuple(range(len(permutation)))
    current = identity
    order = 0

    while True:
        order += 1
        current = tuple(
            permutation[current[index]]
            for index in range(len(permutation))
        )

        if current == identity:
            return order


def main():
    quotient_source = json.loads(
        QUOTIENT_SOURCE.read_text()
    )

    simple_source = json.loads(
        SIMPLE_SOURCE.read_text()
    )

    vertices = tuple(
        range(quotient_source["quotient_vertex_count"])
    )

    orbit_size = {
        row["orbit_index"]: row["orbit_size"]
        for row in quotient_source["orbit_summaries"]
    }

    block_multiplicity = {}

    neighbor_count = {}

    for row in quotient_source["edge_blocks"]:
        pair = canonical_pair(
            row["left_orbit"],
            row["right_orbit"],
        )

        block_multiplicity[pair] = (
            row["edge_multiplicity"]
        )

        left = row["left_orbit"]
        right = row["right_orbit"]

        neighbor_count[(left, right)] = (
            row["neighbors_per_left_vertex"]
        )

        neighbor_count[(right, left)] = (
            row["neighbors_per_right_vertex"]
        )

    weighted_automorphisms = []

    for permutation in permutations(vertices):
        preserves_orbit_sizes = all(
            orbit_size[vertex]
            == orbit_size[permutation[vertex]]
            for vertex in vertices
        )

        if not preserves_orbit_sizes:
            continue

        preserves_blocks = True

        for left in vertices:
            for right in range(left, len(vertices)):
                source_pair = canonical_pair(left, right)
                target_pair = canonical_pair(
                    permutation[left],
                    permutation[right],
                )

                source_multiplicity = (
                    block_multiplicity.get(
                        source_pair,
                        0,
                    )
                )

                target_multiplicity = (
                    block_multiplicity.get(
                        target_pair,
                        0,
                    )
                )

                if source_multiplicity != target_multiplicity:
                    preserves_blocks = False
                    break

            if not preserves_blocks:
                break

        if not preserves_blocks:
            continue

        preserves_normalized_neighbor_counts = all(
            neighbor_count.get((left, right), 0)
            == neighbor_count.get(
                (
                    permutation[left],
                    permutation[right],
                ),
                0,
            )
            for left in vertices
            for right in vertices
        )

        if not preserves_normalized_neighbor_counts:
            continue

        weighted_automorphisms.append(
            tuple(permutation)
        )

    weighted_automorphisms = tuple(
        sorted(weighted_automorphisms)
    )

    order_profile = Counter(
        permutation_order(permutation)
        for permutation in weighted_automorphisms
    )

    vertex_orbits = []
    unseen = set(vertices)

    while unseen:
        vertex = min(unseen)

        orbit = tuple(sorted({
            permutation[vertex]
            for permutation in weighted_automorphisms
        }))

        vertex_orbits.append(orbit)
        unseen -= set(orbit)

    vertex_orbits = tuple(sorted(vertex_orbits))

    simple_automorphisms = tuple(
        tuple(permutation)
        for permutation in simple_source["automorphisms"]
    )

    weighted_is_subgroup_of_simple = (
        set(weighted_automorphisms)
        .issubset(set(simple_automorphisms))
    )

    simple_nonidentity = next(
        (
            permutation
            for permutation in simple_automorphisms
            if permutation != tuple(vertices)
        ),
        None,
    )

    simple_swap_preserves_weighted_data = (
        simple_nonidentity in weighted_automorphisms
        if simple_nonidentity is not None
        else False
    )

    checks = {
        "quotient_source_audit_pass": (
            quotient_source["audit_pass"]
        ),
        "simple_source_audit_pass": (
            simple_source["audit_pass"]
        ),
        "weighted_automorphism_group_nonempty": (
            len(weighted_automorphisms) > 0
        ),
        "identity_present": (
            tuple(vertices) in weighted_automorphisms
        ),
        "weighted_group_is_subgroup_of_simple_group": (
            weighted_is_subgroup_of_simple
        ),
        "weighted_automorphisms_preserve_orbit_sizes": all(
            all(
                orbit_size[vertex]
                == orbit_size[permutation[vertex]]
                for vertex in vertices
            )
            for permutation in weighted_automorphisms
        ),
    }

    payload = {
        "certificate_id": (
            "native_g30_weighted_orbit_skeleton_019"
        ),
        "quotient_source": str(
            QUOTIENT_SOURCE.relative_to(ROOT)
        ),
        "simple_source": str(
            SIMPLE_SOURCE.relative_to(ROOT)
        ),
        "vertex_count": len(vertices),
        "orbit_sizes": {
            str(vertex): orbit_size[vertex]
            for vertex in vertices
        },
        "weighted_automorphism_group_order": len(
            weighted_automorphisms
        ),
        "weighted_automorphism_element_order_profile": {
            str(order): count
            for order, count in sorted(
                order_profile.items()
            )
        },
        "weighted_automorphism_vertex_orbits": [
            list(orbit)
            for orbit in vertex_orbits
        ],
        "weighted_automorphisms": [
            list(permutation)
            for permutation in weighted_automorphisms
        ],
        "simple_skeleton_automorphism_group_order": (
            simple_source["automorphism_group_order"]
        ),
        "simple_nonidentity_automorphism": (
            list(simple_nonidentity)
            if simple_nonidentity is not None
            else None
        ),
        "simple_arm_swap_preserves_weighted_data": (
            simple_swap_preserves_weighted_data
        ),
        "classification_result": (
            "The full weighted orbit skeleton automorphism "
            "group has been enumerated while preserving orbit "
            "sizes, loops, edge multiplicities, and normalized "
            "neighbor counts."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "weighted_skeleton_automorphisms_classified": True,
            "simple_arm_swap_survival_decided": True,
            "lift_to_g30_normalizer_action_open": True,
            "physical_claim": False,
        },
    }

    OUTPUT.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )

    print("OUT ==")
    print("output:", OUTPUT)
    print("audit_pass:", payload["audit_pass"])
    print(
        "weighted_automorphism_group_order:",
        payload["weighted_automorphism_group_order"],
    )
    print(
        "weighted_automorphism_element_order_profile:",
        payload[
            "weighted_automorphism_element_order_profile"
        ],
    )
    print(
        "weighted_automorphism_vertex_orbits:",
        payload[
            "weighted_automorphism_vertex_orbits"
        ],
    )
    print(
        "simple_arm_swap_preserves_weighted_data:",
        payload[
            "simple_arm_swap_preserves_weighted_data"
        ],
    )
    print(
        "weighted_automorphisms:",
        payload["weighted_automorphisms"],
    )
    print(
        "classification_result:",
        payload["classification_result"],
    )


if __name__ == "__main__":
    main()
