#!/usr/bin/env python3
"""Identify each fourfold reflection register as an affine plane."""

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

PARTNER_SOURCE = (
    ROOT / "artifacts/json/"
    "native_g60_twist_center_partner_law_035.json"
)

REFLECTION_SOURCE = (
    ROOT / "artifacts/json/"
    "native_g60_cube_dihedral_reflections_037.json"
)

OUTPUT = (
    ROOT / "artifacts/json/"
    "native_g60_cube_reflection_affine_plane_038.json"
)


def identity(size):
    return tuple(range(size))


def compose(left, right):
    return tuple(
        left[right[index]]
        for index in range(len(left))
    )


def generated_subgroup(generators):
    unit = identity(len(generators[0]))
    subgroup = {unit}
    frontier = [unit]

    while frontier:
        current = frontier.pop()

        for generator in generators:
            product = compose(
                generator,
                current,
            )

            if product in subgroup:
                continue

            subgroup.add(product)
            frontier.append(product)

    return frozenset(subgroup)


def main():
    aut_source = json.loads(
        AUT_SOURCE.read_text()
    )

    cube_source = json.loads(
        CUBE_SOURCE.read_text()
    )

    partner_source = json.loads(
        PARTNER_SOURCE.read_text()
    )

    reflection_source = json.loads(
        REFLECTION_SOURCE.read_text()
    )

    identity30 = identity(30)

    aut_row_by_index = {
        int(row["index"]): row
        for row in aut_source["automorphisms"]
    }

    aut_index_by_permutation = {
        tuple(row["permutation"]): int(row["index"])
        for row in aut_source["automorphisms"]
    }

    cube_elements_by_index = {
        int(row["cube_index"]): {
            tuple(element)
            for element in row["elements"]
        }
        for row in cube_source["cube_rows"]
    }

    partner_by_vertex = {
        int(row["petersen_vertex_index"]): row
        for row in partner_source["partner_rows"]
    }

    central_deck = tuple(
        cube_source["central_deck"]
    )

    central_deck_index = (
        aut_index_by_permutation[
            central_deck
        ]
    )

    reflection_rows_by_cube = {
        int(row["cube_index"]): row
        for row in reflection_source["cube_rows"]
    }

    endpoint_rows_by_cube = {
        int(row["cube_index"]): row
        for row in partner_source[
            "cube_endpoint_rows"
        ]
    }

    cube_rows = []

    for cube_index in range(15):
        endpoint_vertices = tuple(
            int(value)
            for value in endpoint_rows_by_cube[
                cube_index
            ]["petersen_endpoint_vertices"]
        )

        left_vertex, right_vertex = (
            endpoint_vertices
        )

        left_center = tuple(
            partner_by_vertex[left_vertex][
                "six_fixed_center_permutation"
            ]
        )

        right_center = tuple(
            partner_by_vertex[right_vertex][
                "six_fixed_center_permutation"
            ]
        )

        fourth = compose(
            central_deck,
            compose(
                left_center,
                right_center,
            ),
        )

        predicted_elements = {
            central_deck,
            left_center,
            right_center,
            fourth,
        }

        predicted_indices = sorted(
            aut_index_by_permutation[element]
            for element in predicted_elements
        )

        observed_indices = sorted(
            int(value)
            for value in reflection_rows_by_cube[
                cube_index
            ]["reflection_candidate_indices"]
        )

        observed_elements = {
            tuple(
                aut_row_by_index[index][
                    "permutation"
                ]
            )
            for index in observed_indices
        }

        translated_elements = {
            compose(
                central_deck,
                element,
            )
            for element in observed_elements
        }

        translated_subgroup = (
            generated_subgroup(
                tuple(translated_elements)
            )
        )

        cube_elements = (
            cube_elements_by_index[
                cube_index
            ]
        )

        cube_rows.append({
            "cube_index": cube_index,
            "native_g15_label": int(
                reflection_rows_by_cube[
                    cube_index
                ]["native_g15_label"]
            ),
            "petersen_endpoint_vertices": list(
                endpoint_vertices
            ),
            "central_deck_index": (
                central_deck_index
            ),
            "left_center_index": (
                aut_index_by_permutation[
                    left_center
                ]
            ),
            "right_center_index": (
                aut_index_by_permutation[
                    right_center
                ]
            ),
            "fourth_reflection_index": (
                aut_index_by_permutation[
                    fourth
                ]
            ),
            "predicted_reflection_indices": (
                predicted_indices
            ),
            "observed_reflection_indices": (
                observed_indices
            ),
            "predicted_equals_observed": (
                predicted_indices
                == observed_indices
            ),
            "identity_in_reflection_set": (
                identity30
                in observed_elements
            ),
            "reflection_set_closed": all(
                compose(left, right)
                in observed_elements
                for left in observed_elements
                for right in observed_elements
            ),
            "translated_by_z_contains_identity": (
                identity30
                in translated_elements
            ),
            "translated_by_z_size": len(
                translated_elements
            ),
            "translated_by_z_generated_order": (
                len(translated_subgroup)
            ),
            "translated_by_z_is_order4_subgroup": (
                translated_elements
                == set(translated_subgroup)
                and len(
                    translated_subgroup
                )
                == 4
            ),
            "reflection_set_is_z_coset": (
                {
                    compose(
                        central_deck,
                        element,
                    )
                    for element
                    in translated_subgroup
                }
                == observed_elements
            ),
            "all_reflections_lie_in_cube": (
                observed_elements
                <= cube_elements
            ),
        })

    predicted_match_profile = Counter(
        row["predicted_equals_observed"]
        for row in cube_rows
    )

    affine_plane_profile = Counter(
        row[
            "translated_by_z_is_order4_subgroup"
        ]
        for row in cube_rows
    )

    fourth_indices = {
        row["fourth_reflection_index"]
        for row in cube_rows
    }

    center_indices = {
        int(
            row[
                "six_fixed_center_automorphism_index"
            ]
        )
        for row in partner_source[
            "partner_rows"
        ]
    }

    checks = {
        "automorphism_source_audit_pass": (
            aut_source["audit_pass"]
        ),
        "cube_source_audit_pass": (
            cube_source["audit_pass"]
        ),
        "partner_source_audit_pass": (
            partner_source["audit_pass"]
        ),
        "reflection_source_audit_pass": (
            reflection_source["audit_pass"]
        ),
        "central_deck_index_is_66": (
            central_deck_index == 66
        ),
        "fifteen_cube_rows_constructed": (
            len(cube_rows) == 15
        ),
        "every_reflection_set_matches_z_cu_cv_zcucv": all(
            row["predicted_equals_observed"]
            for row in cube_rows
        ),
        "no_reflection_set_contains_identity": all(
            not row["identity_in_reflection_set"]
            for row in cube_rows
        ),
        "no_reflection_set_is_subgroup": all(
            not row["reflection_set_closed"]
            for row in cube_rows
        ),
        "every_z_translate_is_order4_subgroup": all(
            row[
                "translated_by_z_is_order4_subgroup"
            ]
            for row in cube_rows
        ),
        "every_reflection_set_is_z_coset": all(
            row["reflection_set_is_z_coset"]
            for row in cube_rows
        ),
        "all_reflection_elements_lie_in_cube": all(
            row["all_reflections_lie_in_cube"]
            for row in cube_rows
        ),
        "fifteen_distinct_fourth_reflections": (
            len(fourth_indices) == 15
        ),
        "fourth_reflections_are_not_vertex_centers": (
            fourth_indices.isdisjoint(
                center_indices
            )
        ),
    }

    payload = {
        "certificate_id": (
            "native_g60_cube_reflection_affine_plane_038"
        ),
        "automorphism_source": str(
            AUT_SOURCE.relative_to(ROOT)
        ),
        "cube_source": str(
            CUBE_SOURCE.relative_to(ROOT)
        ),
        "partner_source": str(
            PARTNER_SOURCE.relative_to(ROOT)
        ),
        "reflection_source": str(
            REFLECTION_SOURCE.relative_to(ROOT)
        ),
        "central_deck_index": (
            central_deck_index
        ),
        "reflection_formula": (
            "For the cube corresponding to Petersen edge "
            "{u,v}, the four downstairs directions with "
            "involutory G60 lifts that invert an endpoint "
            "twist are exactly {z, c_u, c_v, z c_u c_v}. "
            "This four-set is not a subgroup. Translating it "
            "by z produces an order-4 subgroup, so the "
            "reflection register is an affine plane inside "
            "the downstairs C2^3 cube."
        ),
        "predicted_match_profile": {
            str(status).lower(): count
            for status, count in sorted(
                predicted_match_profile.items()
            )
        },
        "affine_plane_profile": {
            str(status).lower(): count
            for status, count in sorted(
                affine_plane_profile.items()
            )
        },
        "distinct_fourth_reflection_count": (
            len(fourth_indices)
        ),
        "cube_rows": cube_rows,
        "classification_result": (
            "Index 66 is the universal central deck direction "
            "z. For every Petersen edge cube {u,v}, its four "
            "dihedral reflection directions are precisely "
            "z, the two endpoint centers c_u and c_v, and "
            "the fourth element z c_u c_v. These four elements "
            "form an affine plane, namely a z-coset of an "
            "order-4 subgroup of the affine cube. The fifteen "
            "fourth elements are distinct and edge-local."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "universal_reflection_identified_as_z": True,
            "fourfold_reflection_formula_proved": True,
            "reflection_affine_plane_proved": True,
            "fifteen_edge_local_fourth_reflections_identified": True,
            "upstairs_reflection_lift_selection_not_canonical": True,
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
        "central_deck_index:",
        payload["central_deck_index"],
    )
    print(
        "predicted_match_profile:",
        payload["predicted_match_profile"],
    )
    print(
        "affine_plane_profile:",
        payload["affine_plane_profile"],
    )
    print(
        "distinct_fourth_reflection_count:",
        payload[
            "distinct_fourth_reflection_count"
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
            "reflections:",
            row["observed_reflection_indices"],
            "formula:",
            row["predicted_equals_observed"],
            "affine:",
            row[
                "translated_by_z_is_order4_subgroup"
            ],
        )

    print(
        "classification_result:",
        payload["classification_result"],
    )


if __name__ == "__main__":
    main()
