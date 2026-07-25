#!/usr/bin/env python3
"""Identify each G60 twist direction as z times its G30 triangle center."""

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

CENTER_SOURCE = (
    ROOT
    / "artifacts/json/"
    "native_g30_cube_triangle_centers_028.json"
)

PETERSEN_SOURCE = (
    ROOT
    / "artifacts/json/"
    "native_g30_petersen_from_cube_centers_029.json"
)

TWIST_SOURCE = (
    ROOT
    / "artifacts/json/"
    "native_g60_lifted_cube_twist_directions_034.json"
)

OUTPUT = (
    ROOT
    / "artifacts/json/"
    "native_g60_twist_center_partner_law_035.json"
)


def compose(left, right):
    return tuple(
        left[right[index]]
        for index in range(len(left))
    )


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

    center_source = json.loads(
        CENTER_SOURCE.read_text()
    )

    petersen_source = json.loads(
        PETERSEN_SOURCE.read_text()
    )

    twist_source = json.loads(
        TWIST_SOURCE.read_text()
    )

    central_deck = tuple(
        cube_source["central_deck"]
    )

    aut_index_by_permutation = {
        tuple(row["permutation"]): int(row["index"])
        for row in aut_source["automorphisms"]
    }

    involution_row_by_permutation = {
        tuple(row["permutation"]): row
        for row in cube_source["involution_rows"]
    }

    twisted_indices = {
        int(row["g30_automorphism_index"])
        for row in twist_source[
            "distinct_twisted_rows"
        ]
    }

    twisted_permutation_by_index = {
        int(row["index"]): tuple(row["permutation"])
        for row in aut_source["automorphisms"]
        if int(row["index"]) in twisted_indices
    }

    center_rows_by_index = {
        int(row["center_index"]): row
        for row in petersen_source["center_rows"]
    }

    partner_rows = []

    for triangle_row in center_source["triangle_rows"]:
        center_index = int(
            triangle_row["triangle_index"]
        )

        center = tuple(
            triangle_row[
                "unique_six_fixed_incidence3_center"
            ]
        )

        partner = compose(
            central_deck,
            center,
        )

        partner_index = aut_index_by_permutation[
            partner
        ]

        center_involution_row = (
            involution_row_by_permutation[
                center
            ]
        )

        partner_involution_row = (
            involution_row_by_permutation[
                partner
            ]
        )

        center_cube_indices = tuple(sorted(
            int(value)
            for value in triangle_row[
                "cube_indices"
            ]
        ))

        partner_cube_indices = tuple(sorted(
            int(value)
            for value in partner_involution_row[
                "cube_indices"
            ]
        ))

        petersen_row = center_rows_by_index[
            center_index
        ]

        partner_rows.append({
            "petersen_vertex_index": center_index,
            "petersen_neighbors": list(
                petersen_row["neighbors"]
            ),
            "incident_cube_indices": list(
                center_cube_indices
            ),
            "six_fixed_center_automorphism_index": (
                aut_index_by_permutation[
                    center
                ]
            ),
            "six_fixed_center_permutation": list(
                center
            ),
            "six_fixed_center_fixed_point_count": (
                fixed_point_count(center)
            ),
            "six_fixed_center_cube_incidence_count": (
                int(
                    center_involution_row[
                        "cube_incidence_count"
                    ]
                )
            ),
            "twisted_partner_automorphism_index": (
                partner_index
            ),
            "twisted_partner_permutation": list(
                partner
            ),
            "twisted_partner_fixed_point_count": (
                fixed_point_count(partner)
            ),
            "twisted_partner_cube_incidence_count": (
                int(
                    partner_involution_row[
                        "cube_incidence_count"
                    ]
                )
            ),
            "twisted_partner_cube_indices": list(
                partner_cube_indices
            ),
            "partner_equals_central_deck_times_center": True,
            "partner_is_exported_twisted_direction": (
                partner_index in twisted_indices
            ),
            "center_and_partner_have_same_cube_support": (
                center_cube_indices
                == partner_cube_indices
            ),
        })

    partner_rows.sort(
        key=lambda row: row[
            "petersen_vertex_index"
        ]
    )

    produced_partner_indices = {
        row[
            "twisted_partner_automorphism_index"
        ]
        for row in partner_rows
    }

    center_fixed_profile = Counter(
        row[
            "six_fixed_center_fixed_point_count"
        ]
        for row in partner_rows
    )

    partner_fixed_profile = Counter(
        row[
            "twisted_partner_fixed_point_count"
        ]
        for row in partner_rows
    )

    support_profile = Counter(
        len(row["incident_cube_indices"])
        for row in partner_rows
    )

    cube_endpoint_rows = []

    for cube_row in twist_source["cube_rows"]:
        cube_index = int(cube_row["cube_index"])

        incident_vertices = sorted(
            row["petersen_vertex_index"]
            for row in partner_rows
            if cube_index
            in row["incident_cube_indices"]
        )

        expected_twisted_indices = sorted(
            row[
                "twisted_partner_automorphism_index"
            ]
            for row in partner_rows
            if cube_index
            in row["incident_cube_indices"]
        )

        observed_twisted_indices = sorted(
            int(value)
            for value in cube_row[
                "twisted_g30_automorphism_indices"
            ]
        )

        cube_endpoint_rows.append({
            "cube_index": cube_index,
            "native_g15_label": int(
                cube_row["native_g15_label"]
            ),
            "petersen_endpoint_vertices": (
                incident_vertices
            ),
            "expected_twisted_partner_indices": (
                expected_twisted_indices
            ),
            "observed_twisted_direction_indices": (
                observed_twisted_indices
            ),
            "twisted_directions_equal_endpoint_partners": (
                expected_twisted_indices
                == observed_twisted_indices
            ),
        })

    checks = {
        "automorphism_source_audit_pass": (
            aut_source["audit_pass"]
        ),
        "cube_source_audit_pass": (
            cube_source["audit_pass"]
        ),
        "center_source_audit_pass": (
            center_source["audit_pass"]
        ),
        "petersen_source_audit_pass": (
            petersen_source["audit_pass"]
        ),
        "twist_source_audit_pass": (
            twist_source["audit_pass"]
        ),
        "ten_center_partner_rows_constructed": (
            len(partner_rows) == 10
        ),
        "every_center_fixes_six_vertices": all(
            row[
                "six_fixed_center_fixed_point_count"
            ]
            == 6
            for row in partner_rows
        ),
        "every_partner_is_fixed_point_free": all(
            row[
                "twisted_partner_fixed_point_count"
            ]
            == 0
            for row in partner_rows
        ),
        "every_center_and_partner_have_incidence_three": all(
            row[
                "six_fixed_center_cube_incidence_count"
            ]
            == 3
            and row[
                "twisted_partner_cube_incidence_count"
            ]
            == 3
            for row in partner_rows
        ),
        "every_partner_is_exported_twisted_direction": all(
            row[
                "partner_is_exported_twisted_direction"
            ]
            for row in partner_rows
        ),
        "every_center_and_partner_have_same_cube_support": all(
            row[
                "center_and_partner_have_same_cube_support"
            ]
            for row in partner_rows
        ),
        "center_partner_map_is_bijective_onto_all_twisted_directions": (
            len(produced_partner_indices) == 10
            and produced_partner_indices
            == twisted_indices
        ),
        "fifteen_cube_endpoint_rows_constructed": (
            len(cube_endpoint_rows) == 15
        ),
        "every_cube_has_two_petersen_endpoints": all(
            len(
                row[
                    "petersen_endpoint_vertices"
                ]
            )
            == 2
            for row in cube_endpoint_rows
        ),
        "every_cube_twist_pair_equals_endpoint_partner_pair": all(
            row[
                "twisted_directions_equal_endpoint_partners"
            ]
            for row in cube_endpoint_rows
        ),
    }

    payload = {
        "certificate_id": (
            "native_g60_twist_center_partner_law_035"
        ),
        "automorphism_source": str(
            AUT_SOURCE.relative_to(ROOT)
        ),
        "cube_source": str(
            CUBE_SOURCE.relative_to(ROOT)
        ),
        "center_source": str(
            CENTER_SOURCE.relative_to(ROOT)
        ),
        "petersen_source": str(
            PETERSEN_SOURCE.relative_to(ROOT)
        ),
        "twist_source": str(
            TWIST_SOURCE.relative_to(ROOT)
        ),
        "central_deck": list(
            central_deck
        ),
        "partner_law": (
            "For each Petersen vertex center c, its unique "
            "twisted fixed-point-free partner is t = z c, "
            "where z is the central deck involution of G30. "
            "The elements c and t lie in exactly the same "
            "three affine cubes."
        ),
        "center_fixed_point_profile": {
            str(count): multiplicity
            for count, multiplicity in sorted(
                center_fixed_profile.items()
            )
        },
        "partner_fixed_point_profile": {
            str(count): multiplicity
            for count, multiplicity in sorted(
                partner_fixed_profile.items()
            )
        },
        "common_cube_support_size_profile": {
            str(count): multiplicity
            for count, multiplicity in sorted(
                support_profile.items()
            )
        },
        "partner_rows": partner_rows,
        "cube_endpoint_rows": cube_endpoint_rows,
        "classification_result": (
            "The ten G60-twisted downstairs directions are "
            "exactly the central-deck translates zc of the "
            "ten six-fixed-point cube-triangle centers c. "
            "Each pair c and zc belongs to the same three "
            "cubes. Consequently, each affine cube carries "
            "the twisted partners of exactly its two Petersen "
            "endpoint centers. The order-4 lift twist is "
            "therefore the central-deck shadow of the native "
            "Petersen vertex-center system."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "twist_center_partner_law_proved": True,
            "twisted_register_identified_with_petersen_vertices": True,
            "cube_twist_pairs_identified_with_petersen_endpoints": True,
            "central_deck_translation_is_group_theoretic": True,
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
        "center_fixed_point_profile:",
        payload["center_fixed_point_profile"],
    )
    print(
        "partner_fixed_point_profile:",
        payload["partner_fixed_point_profile"],
    )
    print(
        "common_cube_support_size_profile:",
        payload[
            "common_cube_support_size_profile"
        ],
    )

    for row in partner_rows:
        print(
            "petersen vertex",
            row["petersen_vertex_index"],
            "center:",
            row[
                "six_fixed_center_automorphism_index"
            ],
            "twist:",
            row[
                "twisted_partner_automorphism_index"
            ],
            "cubes:",
            row["incident_cube_indices"],
        )

    print(
        "classification_result:",
        payload["classification_result"],
    )


if __name__ == "__main__":
    main()
