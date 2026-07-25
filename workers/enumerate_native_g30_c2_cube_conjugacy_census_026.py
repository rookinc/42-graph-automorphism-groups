#!/usr/bin/env python3
"""Enumerate the 15 conjugate C2^3 cube subgroups in Aut(G30)."""

import json
from collections import Counter
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

AUT_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_full_automorphism_action_001.json"
)

CUBE_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_generated_order8_subgroup_015.json"
)

NORMALIZER_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_c2_cube_normalizer_020.json"
)

LOCAL_V4_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_local_klein_four_013.json"
)

OUTPUT = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_c2_cube_conjugacy_census_026.json"
)


def compose(left, right):
    return tuple(
        left[right[index]]
        for index in range(len(left))
    )


def inverse(permutation):
    result = [0] * len(permutation)

    for source, target in enumerate(permutation):
        result[target] = source

    return tuple(result)


def conjugate(carrier, element):
    return compose(
        compose(carrier, element),
        inverse(carrier),
    )


def permutation_order(permutation):
    identity = tuple(range(len(permutation)))
    current = identity
    order = 0

    while True:
        order += 1
        current = compose(permutation, current)

        if current == identity:
            return order


def fixed_point_count(permutation):
    return sum(
        1
        for vertex, image in enumerate(permutation)
        if vertex == image
    )


def canonical_subgroup(elements):
    return tuple(sorted(elements))


def main():
    aut_source = json.loads(AUT_SOURCE.read_text())
    cube_source = json.loads(CUBE_SOURCE.read_text())
    normalizer_source = json.loads(
        NORMALIZER_SOURCE.read_text()
    )
    local_v4_source = json.loads(
        LOCAL_V4_SOURCE.read_text()
    )

    full_group = frozenset(
        tuple(row["permutation"])
        for row in aut_source["automorphisms"]
    )

    seed_cube = frozenset(
        tuple(element)
        for element in cube_source["elements"]
    )

    degree = len(next(iter(full_group)))
    identity = tuple(range(degree))

    central_deck = tuple(
        next(
            row["permutation"]
            for row in local_v4_source[
                "nonidentity_element_anatomy"
            ]
            if row["label"] == "central_deck"
        )
    )

    conjugate_to_carriers = {}

    for carrier in sorted(full_group):
        conjugate_cube = frozenset(
            conjugate(carrier, element)
            for element in seed_cube
        )

        key = canonical_subgroup(conjugate_cube)

        conjugate_to_carriers.setdefault(
            key,
            [],
        ).append(carrier)

    cube_keys = tuple(sorted(
        conjugate_to_carriers
    ))

    cubes = tuple(
        frozenset(key)
        for key in cube_keys
    )

    cube_index = {
        key: index
        for index, key in enumerate(cube_keys)
    }

    cube_rows = []

    for index, key in enumerate(cube_keys):
        cube = frozenset(key)
        carriers = tuple(
            conjugate_to_carriers[key]
        )

        nonidentity = tuple(
            element
            for element in cube
            if element != identity
        )

        order_profile = Counter(
            permutation_order(element)
            for element in cube
        )

        fixed_point_profile = Counter(
            fixed_point_count(element)
            for element in nonidentity
        )

        cube_rows.append({
            "cube_index": index,
            "order": len(cube),
            "carrier_count": len(carriers),
            "representative_carrier": list(
                min(carriers)
            ),
            "contains_central_deck": (
                central_deck in cube
            ),
            "element_order_profile": {
                str(order): count
                for order, count in sorted(
                    order_profile.items()
                )
            },
            "nonidentity_fixed_point_count_profile": {
                str(count): multiplicity
                for count, multiplicity in sorted(
                    fixed_point_profile.items()
                )
            },
            "elements": [
                list(element)
                for element in key
            ],
        })

    pair_rows = []
    intersection_order_profile = Counter()

    for left_index, right_index in combinations(
        range(len(cubes)),
        2,
    ):
        left = cubes[left_index]
        right = cubes[right_index]
        intersection = frozenset(
            left.intersection(right)
        )

        intersection_order = len(intersection)
        intersection_order_profile[
            intersection_order
        ] += 1

        nonidentity_intersection = tuple(
            element
            for element in intersection
            if element != identity
        )

        fixed_profile = Counter(
            fixed_point_count(element)
            for element in nonidentity_intersection
        )

        pair_rows.append({
            "left_cube": left_index,
            "right_cube": right_index,
            "intersection_order": (
                intersection_order
            ),
            "intersection_nonidentity_count": (
                len(nonidentity_intersection)
            ),
            "intersection_contains_central_deck": (
                central_deck in intersection
            ),
            "intersection_nonidentity_fixed_point_profile": {
                str(count): multiplicity
                for count, multiplicity in sorted(
                    fixed_profile.items()
                )
            },
            "intersection_elements": [
                list(element)
                for element in sorted(intersection)
            ],
        })

    involution_to_cube_indices = {}

    for cube_index_value, cube in enumerate(cubes):
        for element in cube:
            if element == identity:
                continue

            involution_to_cube_indices.setdefault(
                element,
                [],
            ).append(cube_index_value)

    involution_rows = []

    for element, indices in sorted(
        involution_to_cube_indices.items()
    ):
        involution_rows.append({
            "permutation": list(element),
            "order": permutation_order(element),
            "fixed_point_count": fixed_point_count(
                element
            ),
            "central": element == central_deck,
            "cube_incidence_count": len(indices),
            "cube_indices": sorted(indices),
        })

    involution_cube_incidence_profile = Counter(
        row["cube_incidence_count"]
        for row in involution_rows
    )

    fixed_count_incidence_profile = {}

    for row in involution_rows:
        fixed_count = str(
            row["fixed_point_count"]
        )

        fixed_count_incidence_profile.setdefault(
            fixed_count,
            Counter(),
        )[row["cube_incidence_count"]] += 1

    fixed_count_incidence_payload = {
        fixed_count: {
            str(incidence): multiplicity
            for incidence, multiplicity in sorted(
                profile.items()
            )
        }
        for fixed_count, profile in sorted(
            fixed_count_incidence_profile.items(),
            key=lambda item: int(item[0]),
        )
    }

    all_cube_elements_are_involutions = all(
        permutation_order(element) == 2
        for cube in cubes
        for element in cube
        if element != identity
    )

    checks = {
        "automorphism_source_audit_pass": (
            aut_source["audit_pass"]
        ),
        "cube_source_audit_pass": (
            cube_source["audit_pass"]
        ),
        "normalizer_source_audit_pass": (
            normalizer_source["audit_pass"]
        ),
        "local_v4_source_audit_pass": (
            local_v4_source["audit_pass"]
        ),
        "full_group_order_is_240": (
            len(full_group) == 240
        ),
        "seed_cube_order_is_8": (
            len(seed_cube) == 8
        ),
        "normalizer_order_is_16": (
            normalizer_source[
                "normalizer_order"
            ]
            == 16
        ),
        "orbit_stabilizer_predicts_15_cubes": (
            len(full_group)
            // normalizer_source[
                "normalizer_order"
            ]
            == 15
        ),
        "conjugate_cube_count_is_15": (
            len(cubes) == 15
        ),
        "each_cube_has_16_conjugating_carriers": all(
            row["carrier_count"] == 16
            for row in cube_rows
        ),
        "each_cube_has_order_8": all(
            row["order"] == 8
            for row in cube_rows
        ),
        "all_nonidentity_cube_elements_are_involutions": (
            all_cube_elements_are_involutions
        ),
        "all_105_cube_pairs_recorded": (
            len(pair_rows) == 105
        ),
        "central_deck_lies_in_every_cube": all(
            row["contains_central_deck"]
            for row in cube_rows
        ),
        "every_pair_intersection_contains_identity": all(
            row["intersection_order"] >= 1
            for row in pair_rows
        ),
    }

    payload = {
        "certificate_id": (
            "native_g30_c2_cube_conjugacy_census_026"
        ),
        "automorphism_source": str(
            AUT_SOURCE.relative_to(ROOT)
        ),
        "cube_source": str(
            CUBE_SOURCE.relative_to(ROOT)
        ),
        "normalizer_source": str(
            NORMALIZER_SOURCE.relative_to(ROOT)
        ),
        "local_v4_source": str(
            LOCAL_V4_SOURCE.relative_to(ROOT)
        ),
        "full_automorphism_group_order": len(
            full_group
        ),
        "seed_cube_order": len(seed_cube),
        "normalizer_order": normalizer_source[
            "normalizer_order"
        ],
        "predicted_conjugacy_orbit_size": (
            len(full_group)
            // normalizer_source[
                "normalizer_order"
            ]
        ),
        "conjugate_cube_count": len(cubes),
        "cube_rows": cube_rows,
        "cube_pair_count": len(pair_rows),
        "intersection_order_profile": {
            str(order): count
            for order, count in sorted(
                intersection_order_profile.items()
            )
        },
        "cube_pair_rows": pair_rows,
        "distinct_involution_count_in_cube_union": (
            len(involution_rows)
        ),
        "involution_cube_incidence_profile": {
            str(incidence): count
            for incidence, count in sorted(
                involution_cube_incidence_profile.items()
            )
        },
        "fixed_point_count_by_cube_incidence_profile": (
            fixed_count_incidence_payload
        ),
        "involution_rows": involution_rows,
        "central_deck": list(central_deck),
        "central_deck_cube_incidence_count": next(
            row["cube_incidence_count"]
            for row in involution_rows
            if row["central"]
        ),
        "classification_result": (
            "The conjugacy orbit of the local E=C2^3 subgroup "
            "contains exactly 15 cubes, as predicted by the "
            "order-16 normalizer inside the order-240 "
            "automorphism group. All 105 pairwise intersections "
            "and all involution-to-cube incidences are exported "
            "without yet selecting an adjacency relation."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "fifteen_cube_census_complete": True,
            "pairwise_intersections_exported": True,
            "involution_cube_incidence_exported": True,
            "cube_adjacency_relation_not_yet_selected": True,
            "g15_identification_not_yet_claimed": True,
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
        "full_automorphism_group_order:",
        payload["full_automorphism_group_order"],
    )
    print(
        "normalizer_order:",
        payload["normalizer_order"],
    )
    print(
        "predicted_conjugacy_orbit_size:",
        payload[
            "predicted_conjugacy_orbit_size"
        ],
    )
    print(
        "conjugate_cube_count:",
        payload["conjugate_cube_count"],
    )
    print(
        "intersection_order_profile:",
        payload["intersection_order_profile"],
    )
    print(
        "distinct_involution_count_in_cube_union:",
        payload[
            "distinct_involution_count_in_cube_union"
        ],
    )
    print(
        "involution_cube_incidence_profile:",
        payload[
            "involution_cube_incidence_profile"
        ],
    )
    print(
        "fixed_point_count_by_cube_incidence_profile:",
        payload[
            "fixed_point_count_by_cube_incidence_profile"
        ],
    )
    print(
        "central_deck_cube_incidence_count:",
        payload[
            "central_deck_cube_incidence_count"
        ],
    )
    print(
        "classification_result:",
        payload["classification_result"],
    )


if __name__ == "__main__":
    main()
