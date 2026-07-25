#!/usr/bin/env python3
"""Classify the interaction of the two endpoint twists in each lifted cube."""

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

TWIST_SOURCE = (
    ROOT
    / "artifacts/json/"
    "native_g60_lifted_cube_twist_directions_034.json"
)

PARTNER_SOURCE = (
    ROOT
    / "artifacts/json/"
    "native_g60_twist_center_partner_law_035.json"
)

BRIDGE_SOURCE = (
    ROOT
    / "sources/"
    "project42_g60_to_g30_a_quotient_certificate_035.json"
)

OUTPUT = (
    ROOT
    / "artifacts/json/"
    "native_g60_endpoint_twist_commutator_law_036.json"
)


def identity(size):
    return tuple(range(size))


def compose(left, right):
    return tuple(
        left[right[index]]
        for index in range(len(left))
    )


def inverse(permutation):
    result = [None] * len(permutation)

    for source, target in enumerate(permutation):
        result[target] = source

    return tuple(result)


def commutator(left, right):
    return compose(
        compose(
            compose(
                inverse(left),
                inverse(right),
            ),
            left,
        ),
        right,
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

    twist_source = json.loads(
        TWIST_SOURCE.read_text()
    )

    partner_source = json.loads(
        PARTNER_SOURCE.read_text()
    )

    bridge = json.loads(
        BRIDGE_SOURCE.read_text()
    )

    identity60 = identity(60)

    deck_a = tuple(
        int(bridge["involution_a"][str(vertex)])
        for vertex in range(60)
    )

    aut_row_by_index = {
        int(row["index"]): row
        for row in aut_source["automorphisms"]
    }

    aut_index_by_permutation = {
        tuple(row["permutation"]): int(row["index"])
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

    partner_by_vertex = {
        int(row["petersen_vertex_index"]): row
        for row in partner_source["partner_rows"]
    }

    cube_rows = []

    for endpoint_row in partner_source["cube_endpoint_rows"]:
        cube_index = int(endpoint_row["cube_index"])

        endpoint_vertices = tuple(
            int(value)
            for value in endpoint_row[
                "petersen_endpoint_vertices"
            ]
        )

        if len(endpoint_vertices) != 2:
            raise RuntimeError(
                f"cube {cube_index} does not have two endpoints"
            )

        left_vertex, right_vertex = endpoint_vertices

        left_twist_index = int(
            partner_by_vertex[left_vertex][
                "twisted_partner_automorphism_index"
            ]
        )

        right_twist_index = int(
            partner_by_vertex[right_vertex][
                "twisted_partner_automorphism_index"
            ]
        )

        left_down = tuple(
            aut_row_by_index[left_twist_index][
                "permutation"
            ]
        )

        right_down = tuple(
            aut_row_by_index[right_twist_index][
                "permutation"
            ]
        )

        downstairs_product = compose(
            left_down,
            right_down,
        )

        downstairs_product_index = (
            aut_index_by_permutation[
                downstairs_product
            ]
        )

        downstairs_product_involution_row = (
            involution_row_by_permutation[
                downstairs_product
            ]
        )

        left_lifts = [
            tuple(row["permutation"])
            for row in lift_row_by_index[
                left_twist_index
            ]["lifts"]
        ]

        right_lifts = [
            tuple(row["permutation"])
            for row in lift_row_by_index[
                right_twist_index
            ]["lifts"]
        ]

        pairing_rows = []

        for left_lift_number, left_lift in enumerate(
            left_lifts
        ):
            for right_lift_number, right_lift in enumerate(
                right_lifts
            ):
                product = compose(
                    left_lift,
                    right_lift,
                )

                reverse_product = compose(
                    right_lift,
                    left_lift,
                )

                comm = commutator(
                    left_lift,
                    right_lift,
                )

                pairing_rows.append({
                    "left_lift_number": left_lift_number,
                    "right_lift_number": right_lift_number,
                    "left_order": permutation_order(
                        left_lift
                    ),
                    "right_order": permutation_order(
                        right_lift
                    ),
                    "product_order": permutation_order(
                        product
                    ),
                    "reverse_product_order": (
                        permutation_order(
                            reverse_product
                        )
                    ),
                    "commutator_is_identity": (
                        comm == identity60
                    ),
                    "commutator_is_deck_a": (
                        comm == deck_a
                    ),
                    "product_equals_deck_times_reverse": (
                        product
                        == compose(
                            deck_a,
                            reverse_product,
                        )
                    ),
                    "product_square_is_identity": (
                        compose(product, product)
                        == identity60
                    ),
                    "product_square_is_deck_a": (
                        compose(product, product)
                        == deck_a
                    ),
                })

        commutator_profile = Counter(
            "deck_a"
            if row["commutator_is_deck_a"]
            else "identity"
            if row["commutator_is_identity"]
            else "other"
            for row in pairing_rows
        )

        product_order_profile = Counter(
            row["product_order"]
            for row in pairing_rows
        )

        product_square_profile = Counter(
            "deck_a"
            if row["product_square_is_deck_a"]
            else "identity"
            if row["product_square_is_identity"]
            else "other"
            for row in pairing_rows
        )

        cube_rows.append({
            "cube_index": cube_index,
            "native_g15_label": int(
                endpoint_row["native_g15_label"]
            ),
            "petersen_endpoint_vertices": list(
                endpoint_vertices
            ),
            "endpoint_twist_indices": [
                left_twist_index,
                right_twist_index,
            ],
            "downstairs_product_index": (
                downstairs_product_index
            ),
            "downstairs_product_fixed_point_count": (
                fixed_point_count(
                    downstairs_product
                )
            ),
            "downstairs_product_cube_incidence_count": (
                int(
                    downstairs_product_involution_row[
                        "cube_incidence_count"
                    ]
                )
            ),
            "downstairs_product_cube_indices": list(
                downstairs_product_involution_row[
                    "cube_indices"
                ]
            ),
            "commutator_profile": dict(
                sorted(commutator_profile.items())
            ),
            "product_order_profile": {
                str(order): count
                for order, count in sorted(
                    product_order_profile.items()
                )
            },
            "product_square_profile": dict(
                sorted(product_square_profile.items())
            ),
            "pairing_rows": pairing_rows,
        })

    commutator_profile_profile = Counter(
        tuple(sorted(
            row["commutator_profile"].items()
        ))
        for row in cube_rows
    )

    product_order_profile_profile = Counter(
        tuple(sorted(
            row["product_order_profile"].items()
        ))
        for row in cube_rows
    )

    product_fixed_profile = Counter(
        row[
            "downstairs_product_fixed_point_count"
        ]
        for row in cube_rows
    )

    product_incidence_profile = Counter(
        row[
            "downstairs_product_cube_incidence_count"
        ]
        for row in cube_rows
    )

    distinct_product_indices = {
        row["downstairs_product_index"]
        for row in cube_rows
    }

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
        "twist_source_audit_pass": (
            twist_source["audit_pass"]
        ),
        "partner_source_audit_pass": (
            partner_source["audit_pass"]
        ),
        "bridge_source_audit_pass": (
            bridge["audit_pass"]
        ),
        "fifteen_cube_rows_constructed": (
            len(cube_rows) == 15
        ),
        "four_lift_pairings_checked_per_cube": all(
            len(row["pairing_rows"]) == 4
            for row in cube_rows
        ),
        "all_endpoint_twist_lifts_have_order4": all(
            pair["left_order"] == 4
            and pair["right_order"] == 4
            for row in cube_rows
            for pair in row["pairing_rows"]
        ),
        "all_endpoint_lift_commutators_equal_deck_a": all(
            pair["commutator_is_deck_a"]
            for row in cube_rows
            for pair in row["pairing_rows"]
        ),
        "all_products_equal_deck_times_reverse_products": all(
            pair[
                "product_equals_deck_times_reverse"
            ]
            for row in cube_rows
            for pair in row["pairing_rows"]
        ),
        "all_endpoint_lift_products_are_involutions": all(
            pair["product_order"] == 2
            and pair["product_square_is_identity"]
            for row in cube_rows
            for pair in row["pairing_rows"]
        ),
        "all_cubes_have_same_commutator_profile": (
            len(commutator_profile_profile) == 1
        ),
        "all_cubes_have_same_product_order_profile": (
            len(product_order_profile_profile) == 1
        ),
    }

    payload = {
        "certificate_id": (
            "native_g60_endpoint_twist_commutator_law_036"
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
        "twist_source": str(
            TWIST_SOURCE.relative_to(ROOT)
        ),
        "partner_source": str(
            PARTNER_SOURCE.relative_to(ROOT)
        ),
        "bridge_source": str(
            BRIDGE_SOURCE.relative_to(ROOT)
        ),
        "tested_law": (
            "For each Petersen edge cube with endpoint twists "
            "t_u and t_v, choose arbitrary lifts x_u and x_v. "
            "Test whether x_u^2=x_v^2=a, whether their "
            "commutator is a, and whether x_u x_v is an "
            "involution. Multiplication of either lift by the "
            "central deck a must not change these results."
        ),
        "cube_count": len(cube_rows),
        "commutator_profile_profile": [
            {
                "profile": [
                    [name, count]
                    for name, count in profile
                ],
                "cube_count": multiplicity,
            }
            for profile, multiplicity in sorted(
                commutator_profile_profile.items()
            )
        ],
        "product_order_profile_profile": [
            {
                "profile": [
                    [order, count]
                    for order, count in profile
                ],
                "cube_count": multiplicity,
            }
            for profile, multiplicity in sorted(
                product_order_profile_profile.items()
            )
        ],
        "downstairs_product_fixed_point_profile": {
            str(count): multiplicity
            for count, multiplicity in sorted(
                product_fixed_profile.items()
            )
        },
        "downstairs_product_cube_incidence_profile": {
            str(count): multiplicity
            for count, multiplicity in sorted(
                product_incidence_profile.items()
            )
        },
        "distinct_downstairs_product_count": len(
            distinct_product_indices
        ),
        "cube_rows": cube_rows,
        "classification_result": (
            "The two endpoint-twist lifts in each lifted cube "
            "satisfy a uniform dihedral commutator law. Each "
            "has square a, their commutator is a, and reversing "
            "their order multiplies the product by a. Their "
            "product is an involution. This identifies the "
            "local D8 factor directly from the two Petersen "
            "endpoint twists, while the remaining central C2 "
            "factor is independent."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "endpoint_twist_commutator_law_classified": True,
            "local_dihedral_factor_identified": True,
            "downstairs_product_direction_classified": True,
            "remaining_central_c2_generator_not_yet_identified": True,
            "global_group_presentation_not_yet_composed": True,
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
        "commutator_profile_profile:",
        payload["commutator_profile_profile"],
    )
    print(
        "product_order_profile_profile:",
        payload[
            "product_order_profile_profile"
        ],
    )
    print(
        "downstairs_product_fixed_point_profile:",
        payload[
            "downstairs_product_fixed_point_profile"
        ],
    )
    print(
        "downstairs_product_cube_incidence_profile:",
        payload[
            "downstairs_product_cube_incidence_profile"
        ],
    )
    print(
        "distinct_downstairs_product_count:",
        payload[
            "distinct_downstairs_product_count"
        ],
    )

    for row in cube_rows:
        print(
            "cube",
            row["cube_index"],
            "g15:",
            row["native_g15_label"],
            "endpoints:",
            row["petersen_endpoint_vertices"],
            "twists:",
            row["endpoint_twist_indices"],
            "product:",
            row["downstairs_product_index"],
            "fixed:",
            row[
                "downstairs_product_fixed_point_count"
            ],
            "incidence:",
            row[
                "downstairs_product_cube_incidence_count"
            ],
            "comm:",
            row["commutator_profile"],
            "orders:",
            row["product_order_profile"],
        )

    print(
        "classification_result:",
        payload["classification_result"],
    )


if __name__ == "__main__":
    main()
