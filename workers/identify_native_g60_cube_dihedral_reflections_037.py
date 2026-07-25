#!/usr/bin/env python3
"""Identify the dihedral reflection directions in each lifted G60 cube."""

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

AUT_SOURCE = (
    ROOT / "artifacts/json/"
    "native_g30_full_automorphism_action_001.json"
)

CUBE_SOURCE = (
    ROOT / "artifacts/json/"
    "native_g30_c2_cube_conjugacy_census_026.json"
)

LIFT_SOURCE = (
    ROOT / "artifacts/json/"
    "native_g30_automorphism_lifts_to_g60_032.json"
)

PREIMAGE_SOURCE = (
    ROOT / "artifacts/json/"
    "native_g60_lifted_cube_preimages_033.json"
)

TWIST_SOURCE = (
    ROOT / "artifacts/json/"
    "native_g60_lifted_cube_twist_directions_034.json"
)

COMMUTATOR_SOURCE = (
    ROOT / "artifacts/json/"
    "native_g60_endpoint_twist_commutator_law_036.json"
)

OUTPUT = (
    ROOT / "artifacts/json/"
    "native_g60_cube_dihedral_reflections_037.json"
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


def conjugate(conjugator, element):
    return compose(
        compose(conjugator, element),
        inverse(conjugator),
    )


def permutation_order(permutation):
    unit = identity(len(permutation))
    current = unit

    for order in range(1, 1000):
        current = compose(permutation, current)

        if current == unit:
            return order

    raise RuntimeError("order search exceeded bound")


def main():
    aut_source = json.loads(AUT_SOURCE.read_text())
    cube_source = json.loads(CUBE_SOURCE.read_text())
    lift_source = json.loads(LIFT_SOURCE.read_text())
    preimage_source = json.loads(PREIMAGE_SOURCE.read_text())
    twist_source = json.loads(TWIST_SOURCE.read_text())
    commutator_source = json.loads(
        COMMUTATOR_SOURCE.read_text()
    )

    identity60 = identity(60)

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

    cube_row_by_index = {
        int(row["cube_index"]): row
        for row in cube_source["cube_rows"]
    }

    preimage_row_by_index = {
        int(row["cube_index"]): row
        for row in preimage_source["cube_rows"]
    }

    twist_row_by_index = {
        int(row["cube_index"]): row
        for row in twist_source["cube_rows"]
    }

    commutator_row_by_index = {
        int(row["cube_index"]): row
        for row in commutator_source["cube_rows"]
    }

    cube_rows = []

    for cube_index in range(15):
        downstairs_elements = {
            tuple(element)
            for element in cube_row_by_index[
                cube_index
            ]["elements"]
        }

        twisted_indices = set(
            int(value)
            for value in twist_row_by_index[
                cube_index
            ]["twisted_g30_automorphism_indices"]
        )

        product_index = int(
            commutator_row_by_index[
                cube_index
            ]["downstairs_product_index"]
        )

        untwisted_indices = sorted(
            aut_index_by_permutation[element]
            for element in downstairs_elements
            if element != tuple(range(30))
            and aut_index_by_permutation[element]
            not in twisted_indices
        )

        rotation_index = min(twisted_indices)

        rotation_lifts = [
            tuple(row["permutation"])
            for row in lift_row_by_index[
                rotation_index
            ]["lifts"]
        ]

        rotation = rotation_lifts[0]
        rotation_inverse = inverse(rotation)

        preimage_elements = {
            tuple(element)
            for element in preimage_row_by_index[
                cube_index
            ]["elements"]
        }

        candidate_rows = []

        for downstairs_index in untwisted_indices:
            downstairs = tuple(
                aut_row_by_index[
                    downstairs_index
                ]["permutation"]
            )

            lifts = [
                tuple(row["permutation"])
                for row in lift_row_by_index[
                    downstairs_index
                ]["lifts"]
            ]

            lift_rows = []

            for lift_number, lift in enumerate(lifts):
                order = permutation_order(lift)

                lift_rows.append({
                    "lift_number": lift_number,
                    "order": order,
                    "lies_in_cube_preimage": (
                        lift in preimage_elements
                    ),
                    "conjugates_rotation_to_inverse": (
                        conjugate(lift, rotation)
                        == rotation_inverse
                    ),
                    "commutes_with_rotation": (
                        compose(lift, rotation)
                        == compose(rotation, lift)
                    ),
                })

            candidate_rows.append({
                "g30_automorphism_index": (
                    downstairs_index
                ),
                "is_endpoint_product_direction": (
                    downstairs_index == product_index
                ),
                "lift_rows": lift_rows,
                "has_dihedral_reflection_lift": any(
                    row[
                        "order"
                    ] == 2
                    and row[
                        "lies_in_cube_preimage"
                    ]
                    and row[
                        "conjugates_rotation_to_inverse"
                    ]
                    for row in lift_rows
                ),
            })

        reflection_candidates = [
            row
            for row in candidate_rows
            if row["has_dihedral_reflection_lift"]
        ]

        cube_rows.append({
            "cube_index": cube_index,
            "native_g15_label": int(
                twist_row_by_index[
                    cube_index
                ]["native_g15_label"]
            ),
            "rotation_twist_index": rotation_index,
            "endpoint_product_index": product_index,
            "untwisted_direction_count": len(
                untwisted_indices
            ),
            "reflection_candidate_count": len(
                reflection_candidates
            ),
            "reflection_candidate_indices": [
                row["g30_automorphism_index"]
                for row in reflection_candidates
            ],
            "endpoint_product_is_reflection_candidate": any(
                row[
                    "is_endpoint_product_direction"
                ]
                for row in reflection_candidates
            ),
            "candidate_rows": candidate_rows,
        })

    candidate_count_profile = Counter(
        row["reflection_candidate_count"]
        for row in cube_rows
    )

    product_reflection_profile = Counter(
        row["endpoint_product_is_reflection_candidate"]
        for row in cube_rows
    )

    distinct_reflection_indices = {
        index
        for row in cube_rows
        for index in row[
            "reflection_candidate_indices"
        ]
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
        "preimage_source_audit_pass": (
            preimage_source["audit_pass"]
        ),
        "twist_source_audit_pass": (
            twist_source["audit_pass"]
        ),
        "commutator_source_audit_pass": (
            commutator_source["audit_pass"]
        ),
        "fifteen_cubes_classified": (
            len(cube_rows) == 15
        ),
        "five_untwisted_directions_per_cube": all(
            row["untwisted_direction_count"] == 5
            for row in cube_rows
        ),
        "every_cube_has_reflection_candidate": all(
            row["reflection_candidate_count"] > 0
            for row in cube_rows
        ),
    }

    payload = {
        "certificate_id": (
            "native_g60_cube_dihedral_reflections_037"
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
        "twist_source": str(
            TWIST_SOURCE.relative_to(ROOT)
        ),
        "commutator_source": str(
            COMMUTATOR_SOURCE.relative_to(ROOT)
        ),
        "tested_law": (
            "For each lifted cube, select one endpoint "
            "order-4 twist lift r. Search the five "
            "untwisted downstairs directions for involutory "
            "lifts s satisfying s r s^{-1} = r^{-1}."
        ),
        "reflection_candidate_count_profile": {
            str(count): multiplicity
            for count, multiplicity in sorted(
                candidate_count_profile.items()
            )
        },
        "endpoint_product_reflection_profile": {
            str(status).lower(): multiplicity
            for status, multiplicity in sorted(
                product_reflection_profile.items()
            )
        },
        "distinct_reflection_direction_count": len(
            distinct_reflection_indices
        ),
        "cube_rows": cube_rows,
        "classification_result": (
            "The audit identifies the untwisted downstairs "
            "directions whose involutory G60 lifts invert an "
            "endpoint order-4 twist lift. These are the "
            "reflections realizing the D8 conjugation law "
            "inside each non-split D8 x C2 cube preimage."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "dihedral_reflection_candidates_identified": True,
            "candidate_uniqueness_not_assumed": True,
            "global_reflection_register_not_yet_classified": True,
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
        "reflection_candidate_count_profile:",
        payload[
            "reflection_candidate_count_profile"
        ],
    )
    print(
        "endpoint_product_reflection_profile:",
        payload[
            "endpoint_product_reflection_profile"
        ],
    )
    print(
        "distinct_reflection_direction_count:",
        payload[
            "distinct_reflection_direction_count"
        ],
    )

    for row in cube_rows:
        print(
            "cube",
            row["cube_index"],
            "g15:",
            row["native_g15_label"],
            "rotation:",
            row["rotation_twist_index"],
            "product:",
            row["endpoint_product_index"],
            "reflections:",
            row["reflection_candidate_indices"],
            "product_is_reflection:",
            row[
                "endpoint_product_is_reflection_candidate"
            ],
        )

    print(
        "classification_result:",
        payload["classification_result"],
    )


if __name__ == "__main__":
    main()
