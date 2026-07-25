#!/usr/bin/env python3
"""Identify which directions in each G30 cube acquire order 4 in G60."""

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

AUT_SOURCE = (
    ROOT
    / "artifacts/json/"
    "native_g30_full_automorphism_action_001.json"
)

CUBE_SOURCE = (
    ROOT
    / "artifacts/json/"
    "native_g30_c2_cube_conjugacy_census_026.json"
)

LIFT_SOURCE = (
    ROOT
    / "artifacts/json/"
    "native_g30_automorphism_lifts_to_g60_032.json"
)

PREIMAGE_SOURCE = (
    ROOT
    / "artifacts/json/"
    "native_g60_lifted_cube_preimages_033.json"
)

ALIGNMENT_SOURCE = (
    ROOT
    / "artifacts/json/"
    "native_g30_cube_to_g15_label_alignment_031.json"
)

BRIDGE_SOURCE = (
    ROOT
    / "sources/"
    "project42_g60_to_g30_a_quotient_certificate_035.json"
)

OUTPUT = (
    ROOT
    / "artifacts/json/"
    "native_g60_lifted_cube_twist_directions_034.json"
)


def identity(size):
    return tuple(range(size))


def compose(left, right):
    return tuple(
        left[right[index]]
        for index in range(len(left))
    )


def permutation_order(permutation):
    unit = identity(len(permutation))
    current = unit

    for order in range(1, 1000):
        current = compose(permutation, current)

        if current == unit:
            return order

    raise RuntimeError("permutation order search exceeded bound")


def fixed_point_count(permutation):
    return sum(
        1
        for index, image in enumerate(permutation)
        if index == image
    )


def main():
    aut_source = json.loads(
        AUT_SOURCE.read_text()
    )

    cube_source = json.loads(
        CUBE_SOURCE.read_text()
    )

    lift_source = json.loads(
        LIFT_SOURCE.read_text()
    )

    preimage_source = json.loads(
        PREIMAGE_SOURCE.read_text()
    )

    alignment_source = json.loads(
        ALIGNMENT_SOURCE.read_text()
    )

    bridge = json.loads(
        BRIDGE_SOURCE.read_text()
    )

    identity30 = identity(30)
    identity60 = identity(60)

    deck_a = tuple(
        int(bridge["involution_a"][str(vertex)])
        for vertex in range(60)
    )

    aut_index_by_permutation = {
        tuple(row["permutation"]): int(row["index"])
        for row in aut_source["automorphisms"]
    }

    aut_row_by_index = {
        int(row["index"]): row
        for row in aut_source["automorphisms"]
    }

    lift_row_by_index = {
        int(row["g30_automorphism_index"]): row
        for row in lift_source["lift_rows"]
    }

    involution_row_by_permutation = {
        tuple(row["permutation"]): row
        for row in cube_source["involution_rows"]
    }

    cube_to_g15 = {
        int(cube): int(label)
        for cube, label in alignment_source[
            "cube_to_native_g15_label"
        ].items()
    }

    preimage_row_by_cube = {
        int(row["cube_index"]): row
        for row in preimage_source["cube_rows"]
    }

    cube_rows = []

    for cube_row in cube_source["cube_rows"]:
        cube_index = int(cube_row["cube_index"])

        direction_rows = []

        for base_element_list in cube_row["elements"]:
            base_element = tuple(base_element_list)

            if base_element == identity30:
                continue

            aut_index = aut_index_by_permutation[
                base_element
            ]

            aut_row = aut_row_by_index[aut_index]
            lift_row = lift_row_by_index[aut_index]

            lifts = [
                tuple(row["permutation"])
                for row in lift_row["lifts"]
            ]

            lift_orders = [
                permutation_order(lift)
                for lift in lifts
            ]

            lift_squares = [
                compose(lift, lift)
                for lift in lifts
            ]

            square_profile = Counter(
                "identity"
                if square == identity60
                else "deck_a"
                if square == deck_a
                else "other"
                for square in lift_squares
            )

            twisted = (
                lift_orders == [4, 4]
                and square_profile == {"deck_a": 2}
            )

            involution_row = (
                involution_row_by_permutation[
                    base_element
                ]
            )

            direction_rows.append({
                "g30_automorphism_index": aut_index,
                "g30_permutation": list(base_element),
                "g30_fixed_point_count": (
                    fixed_point_count(base_element)
                ),
                "g30_central": bool(
                    aut_row["central"]
                ),
                "cube_incidence_count": int(
                    involution_row[
                        "cube_incidence_count"
                    ]
                ),
                "cube_indices": list(
                    involution_row["cube_indices"]
                ),
                "lift_orders": lift_orders,
                "lift_square_profile": dict(
                    sorted(square_profile.items())
                ),
                "twisted_order4_direction": twisted,
            })

        direction_rows.sort(
            key=lambda row: (
                not row["twisted_order4_direction"],
                row["g30_fixed_point_count"],
                row["g30_automorphism_index"],
            )
        )

        twisted_rows = [
            row
            for row in direction_rows
            if row["twisted_order4_direction"]
        ]

        untwisted_rows = [
            row
            for row in direction_rows
            if not row["twisted_order4_direction"]
        ]

        twisted_fixed_profile = Counter(
            row["g30_fixed_point_count"]
            for row in twisted_rows
        )

        twisted_incidence_profile = Counter(
            row["cube_incidence_count"]
            for row in twisted_rows
        )

        preimage_row = preimage_row_by_cube[
            cube_index
        ]

        cube_rows.append({
            "cube_index": cube_index,
            "native_g15_label": cube_to_g15[
                cube_index
            ],
            "lifted_preimage_type": (
                preimage_row[
                    "abstract_group_type"
                ]
            ),
            "nonidentity_direction_count": len(
                direction_rows
            ),
            "twisted_direction_count": len(
                twisted_rows
            ),
            "untwisted_direction_count": len(
                untwisted_rows
            ),
            "twisted_g30_automorphism_indices": [
                row["g30_automorphism_index"]
                for row in twisted_rows
            ],
            "twisted_fixed_point_profile": {
                str(count): multiplicity
                for count, multiplicity in sorted(
                    twisted_fixed_profile.items()
                )
            },
            "twisted_cube_incidence_profile": {
                str(count): multiplicity
                for count, multiplicity in sorted(
                    twisted_incidence_profile.items()
                )
            },
            "direction_rows": direction_rows,
        })

    twisted_count_profile = Counter(
        row["twisted_direction_count"]
        for row in cube_rows
    )

    twisted_fixed_profile_profile = Counter(
        tuple(sorted(
            row[
                "twisted_fixed_point_profile"
            ].items()
        ))
        for row in cube_rows
    )

    twisted_incidence_profile_profile = Counter(
        tuple(sorted(
            row[
                "twisted_cube_incidence_profile"
            ].items()
        ))
        for row in cube_rows
    )

    twisted_element_to_cubes = {}

    for row in cube_rows:
        for aut_index in row[
            "twisted_g30_automorphism_indices"
        ]:
            twisted_element_to_cubes.setdefault(
                aut_index,
                [],
            ).append(row["cube_index"])

    distinct_twisted_indices = sorted(
        twisted_element_to_cubes
    )

    distinct_twisted_rows = []

    for aut_index in distinct_twisted_indices:
        aut_row = aut_row_by_index[aut_index]
        permutation = tuple(
            aut_row["permutation"]
        )

        involution_row = (
            involution_row_by_permutation[
                permutation
            ]
        )

        distinct_twisted_rows.append({
            "g30_automorphism_index": aut_index,
            "g30_fixed_point_count": (
                fixed_point_count(permutation)
            ),
            "cube_incidence_count": int(
                involution_row[
                    "cube_incidence_count"
                ]
            ),
            "cube_indices": sorted(
                twisted_element_to_cubes[
                    aut_index
                ]
            ),
        })

    distinct_twisted_fixed_profile = Counter(
        row["g30_fixed_point_count"]
        for row in distinct_twisted_rows
    )

    distinct_twisted_incidence_profile = Counter(
        row["cube_incidence_count"]
        for row in distinct_twisted_rows
    )

    checks = {
        "automorphism_source_audit_pass": (
            aut_source["audit_pass"]
        ),
        "cube_source_audit_pass": (
            cube_source["audit_pass"]
        ),
        "lift_source_audit_pass": (
            lift_source["audit_pass"]
        ),
        "preimage_source_audit_pass": (
            preimage_source["audit_pass"]
        ),
        "alignment_source_audit_pass": (
            alignment_source["audit_pass"]
        ),
        "bridge_source_audit_pass": (
            bridge["audit_pass"]
        ),
        "fifteen_cubes_classified": (
            len(cube_rows) == 15
        ),
        "every_cube_has_seven_nonidentity_directions": all(
            row[
                "nonidentity_direction_count"
            ]
            == 7
            for row in cube_rows
        ),
        "every_cube_has_exactly_two_twisted_directions": all(
            row["twisted_direction_count"] == 2
            for row in cube_rows
        ),
        "every_cube_has_exactly_five_untwisted_directions": all(
            row["untwisted_direction_count"] == 5
            for row in cube_rows
        ),
        "every_twisted_direction_has_two_order4_lifts": all(
            direction["lift_orders"] == [4, 4]
            and direction[
                "lift_square_profile"
            ]
            == {"deck_a": 2}
            for cube in cube_rows
            for direction in cube["direction_rows"]
            if direction[
                "twisted_order4_direction"
            ]
        ),
        "every_untwisted_direction_has_two_order2_lifts": all(
            direction["lift_orders"] == [2, 2]
            and direction[
                "lift_square_profile"
            ]
            == {"identity": 2}
            for cube in cube_rows
            for direction in cube["direction_rows"]
            if not direction[
                "twisted_order4_direction"
            ]
        ),
        "all_cubes_have_same_twisted_fixed_profile": (
            len(
                twisted_fixed_profile_profile
            )
            == 1
        ),
        "all_cubes_have_same_twisted_incidence_profile": (
            len(
                twisted_incidence_profile_profile
            )
            == 1
        ),
    }

    payload = {
        "certificate_id": (
            "native_g60_lifted_cube_twist_directions_034"
        ),
        "automorphism_source": str(
            AUT_SOURCE.relative_to(ROOT)
        ),
        "cube_source": str(
            CUBE_SOURCE.relative_to(ROOT)
        ),
        "lift_source": str(
            LIFT_SOURCE.relative_to(ROOT)
        ),
        "preimage_source": str(
            PREIMAGE_SOURCE.relative_to(ROOT)
        ),
        "alignment_source": str(
            ALIGNMENT_SOURCE.relative_to(ROOT)
        ),
        "bridge_source": str(
            BRIDGE_SOURCE.relative_to(ROOT)
        ),
        "twist_definition": (
            "A nonidentity direction x in a downstairs "
            "C2^3 cube is twisted when both of its G60 "
            "lifts have order 4 and square to the deck "
            "involution a. It is untwisted when both lifts "
            "have order 2 and square to the identity."
        ),
        "cube_count": len(cube_rows),
        "twisted_direction_count_profile": {
            str(count): multiplicity
            for count, multiplicity in sorted(
                twisted_count_profile.items()
            )
        },
        "twisted_fixed_profile_profile": [
            {
                "profile": [
                    [count, multiplicity]
                    for count, multiplicity
                    in profile
                ],
                "cube_count": multiplicity,
            }
            for profile, multiplicity in sorted(
                twisted_fixed_profile_profile.items()
            )
        ],
        "twisted_incidence_profile_profile": [
            {
                "profile": [
                    [count, multiplicity]
                    for count, multiplicity
                    in profile
                ],
                "cube_count": multiplicity,
            }
            for profile, multiplicity in sorted(
                twisted_incidence_profile_profile.items()
            )
        ],
        "distinct_twisted_downstairs_element_count": len(
            distinct_twisted_rows
        ),
        "distinct_twisted_fixed_point_profile": {
            str(count): multiplicity
            for count, multiplicity in sorted(
                distinct_twisted_fixed_profile.items()
            )
        },
        "distinct_twisted_cube_incidence_profile": {
            str(count): multiplicity
            for count, multiplicity in sorted(
                distinct_twisted_incidence_profile.items()
            )
        },
        "distinct_twisted_rows": (
            distinct_twisted_rows
        ),
        "cube_rows": cube_rows,
        "classification_result": (
            "Each of the fifteen downstairs affine cubes "
            "contains exactly two twisted nonidentity "
            "directions. Each twisted direction has two "
            "order-4 lifts whose square is the native deck "
            "involution a. The remaining five directions "
            "have two involutory lifts. These two twisted "
            "directions are the local support of the "
            "non-split D8 x C2 extension above each cube."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "twisted_downstairs_directions_identified": True,
            "order4_lift_pairs_identified": True,
            "deck_square_law_verified": True,
            "global_twist_geometry_not_yet_derived": True,
            "preferred_generating_pair_not_yet_selected": True,
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
        "twisted_direction_count_profile:",
        payload[
            "twisted_direction_count_profile"
        ],
    )
    print(
        "distinct_twisted_downstairs_element_count:",
        payload[
            "distinct_twisted_downstairs_element_count"
        ],
    )
    print(
        "distinct_twisted_fixed_point_profile:",
        payload[
            "distinct_twisted_fixed_point_profile"
        ],
    )
    print(
        "distinct_twisted_cube_incidence_profile:",
        payload[
            "distinct_twisted_cube_incidence_profile"
        ],
    )

    for row in cube_rows:
        print(
            "cube",
            row["cube_index"],
            "g15:",
            row["native_g15_label"],
            "twisted:",
            row[
                "twisted_g30_automorphism_indices"
            ],
            "fixed:",
            row[
                "twisted_fixed_point_profile"
            ],
            "incidence:",
            row[
                "twisted_cube_incidence_profile"
            ],
        )

    print(
        "classification_result:",
        payload["classification_result"],
    )


if __name__ == "__main__":
    main()
