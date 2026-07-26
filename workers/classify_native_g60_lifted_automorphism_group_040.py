#!/usr/bin/env python3
"""Classify the 480-element lifted automorphism group acting on G60."""

import json
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

AUT_SOURCE = (
    ROOT / "artifacts/json/"
    "native_g30_full_automorphism_action_001.json"
)

COMPLEMENT_SOURCE = (
    ROOT / "artifacts/json/"
    "native_g30_s5_complement_classification_004.json"
)

LIFT_SOURCE = (
    ROOT / "artifacts/json/"
    "native_g30_automorphism_lifts_to_g60_032.json"
)

BRIDGE_SOURCE = (
    ROOT / "sources/"
    "project42_g60_to_g30_a_quotient_certificate_035.json"
)

OUTPUT = (
    ROOT / "artifacts/json/"
    "native_g60_lifted_automorphism_group_040.json"
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


def permutation_order(permutation):
    unit = identity(len(permutation))
    current = unit

    for order in range(1, 5000):
        current = compose(permutation, current)

        if current == unit:
            return order

    raise RuntimeError("permutation order search exceeded bound")


def generated_subgroup(generators):
    if not generators:
        raise ValueError("generator list is empty")

    unit = identity(len(generators[0]))
    subgroup = {unit}
    frontier = [unit]

    while frontier:
        current = frontier.pop()

        for generator in generators:
            for product in (
                compose(generator, current),
                compose(current, generator),
            ):
                if product in subgroup:
                    continue

                subgroup.add(product)
                frontier.append(product)

    return frozenset(subgroup)


def center(group):
    return frozenset(
        element
        for element in group
        if all(
            compose(element, other)
            == compose(other, element)
            for other in group
        )
    )


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


def derived_subgroup(group):
    commutators = {
        commutator(left, right)
        for left in group
        for right in group
    }

    return generated_subgroup(
        tuple(commutators)
    )


def subgroup_is_abelian(group):
    return all(
        compose(left, right)
        == compose(right, left)
        for left, right in combinations(
            group,
            2,
        )
    )


def orbit_of_point(group, point):
    return {
        element[point]
        for element in group
    }


def main():
    aut_source = json.loads(
        AUT_SOURCE.read_text()
    )

    complement_source = json.loads(
        COMPLEMENT_SOURCE.read_text()
    )

    lift_source = json.loads(
        LIFT_SOURCE.read_text()
    )

    bridge = json.loads(
        BRIDGE_SOURCE.read_text()
    )

    identity60 = identity(60)

    deck_a = tuple(
        int(bridge["involution_a"][str(vertex)])
        for vertex in range(60)
    )

    base_row_by_permutation = {
        tuple(row["permutation"]): row
        for row in aut_source["automorphisms"]
    }

    lift_row_by_base_index = {
        int(row["g30_automorphism_index"]): row
        for row in lift_source["lift_rows"]
    }

    all_lifts = set()

    for row in lift_source["lift_rows"]:
        for lift in row["lifts"]:
            all_lifts.add(
                tuple(lift["permutation"])
            )

    lifted_group = frozenset(all_lifts)

    lifted_center = center(lifted_group)
    lifted_derived = derived_subgroup(
        lifted_group
    )

    lifted_order_profile = Counter(
        permutation_order(element)
        for element in lifted_group
    )

    lifted_center_order_profile = Counter(
        permutation_order(element)
        for element in lifted_center
    )

    lifted_derived_order_profile = Counter(
        permutation_order(element)
        for element in lifted_derived
    )

    lifted_orbit_0 = orbit_of_point(
        lifted_group,
        0,
    )

    lifted_stabilizer_0 = {
        element
        for element in lifted_group
        if element[0] == 0
    }

    complement_rows = []

    for complement in complement_source[
        "complements"
    ]:
        complement_index = int(
            complement["index"]
        )

        downstairs_elements = {
            tuple(element)
            for element in complement["elements"]
        }

        downstairs_indices = {
            int(
                base_row_by_permutation[
                    element
                ]["index"]
            )
            for element in downstairs_elements
        }

        preimage_elements = set()

        lift_signature = defaultdict(
            Counter
        )

        for downstairs_index in downstairs_indices:
            base_row = next(
                row
                for row in aut_source[
                    "automorphisms"
                ]
                if int(row["index"])
                == downstairs_index
            )

            downstairs_order = int(
                base_row["order"]
            )

            lift_row = lift_row_by_base_index[
                downstairs_index
            ]

            for lift in lift_row["lifts"]:
                lifted = tuple(
                    lift["permutation"]
                )

                preimage_elements.add(
                    lifted
                )

                lift_signature[
                    downstairs_order
                ][
                    permutation_order(
                        lifted
                    )
                ] += 1

        preimage_group = frozenset(
            preimage_elements
        )

        preimage_center = center(
            preimage_group
        )

        preimage_derived = derived_subgroup(
            preimage_group
        )

        preimage_order_profile = Counter(
            permutation_order(element)
            for element in preimage_group
        )

        complement_candidates = []

        involutions = [
            element
            for element in preimage_group
            if permutation_order(element) == 2
            and element != identity60
            and element != deck_a
        ]

        for generator_count in range(2, 5):
            found = False

            for generators in combinations(
                involutions,
                generator_count,
            ):
                subgroup = generated_subgroup(
                    generators
                )

                if len(subgroup) != 120:
                    continue

                if deck_a in subgroup:
                    continue

                complement_candidates.append(
                    subgroup
                )
                found = True
                break

            if found:
                break

        unique_complements = {
            tuple(sorted(subgroup))
            for subgroup in complement_candidates
        }

        complement_rows.append({
            "downstairs_complement_index": (
                complement_index
            ),
            "downstairs_stabilizer_type": (
                complement[
                    "vertex_stabilizer_0_type"
                ]
            ),
            "preimage_order": len(
                preimage_group
            ),
            "preimage_center_order": len(
                preimage_center
            ),
            "preimage_derived_order": len(
                preimage_derived
            ),
            "preimage_abelian": (
                subgroup_is_abelian(
                    preimage_group
                )
            ),
            "preimage_element_order_profile": {
                str(order): count
                for order, count in sorted(
                    preimage_order_profile.items()
                )
            },
            "lift_order_signature_by_downstairs_order": {
                str(downstairs_order): {
                    str(upstairs_order): count
                    for upstairs_order, count
                    in sorted(profile.items())
                }
                for downstairs_order, profile
                in sorted(lift_signature.items())
            },
            "order120_complement_count_found": len(
                unique_complements
            ),
            "extension_splits": (
                len(unique_complements) > 0
            ),
            "contains_deck_a": (
                deck_a in preimage_group
            ),
        })

    preimage_order_profile = Counter(
        row["preimage_order"]
        for row in complement_rows
    )

    preimage_center_profile = Counter(
        row["preimage_center_order"]
        for row in complement_rows
    )

    preimage_derived_profile = Counter(
        row["preimage_derived_order"]
        for row in complement_rows
    )

    split_profile = Counter(
        row["extension_splits"]
        for row in complement_rows
    )

    central_involutions = [
        element
        for element in lifted_center
        if permutation_order(element) == 2
        and element != identity60
    ]

    checks = {
        "automorphism_source_audit_pass": (
            aut_source["audit_pass"]
        ),
        "complement_source_audit_pass": (
            complement_source["audit_pass"]
        ),
        "lift_source_audit_pass": (
            lift_source["audit_pass"]
        ),
        "bridge_source_audit_pass": (
            bridge["audit_pass"]
        ),
        "lifted_group_has_order_480": (
            len(lifted_group) == 480
        ),
        "lifted_group_is_closed": (
            generated_subgroup(
                tuple(lifted_group)
            )
            == lifted_group
        ),
        "deck_a_is_central": (
            deck_a in lifted_center
        ),
        "lifted_action_is_vertex_transitive": (
            len(lifted_orbit_0) == 60
        ),
        "vertex_stabilizer_order_is_8": (
            len(lifted_stabilizer_0) == 8
        ),
        "two_s5_preimages_constructed": (
            len(complement_rows) == 2
        ),
        "each_s5_preimage_has_order_240": all(
            row["preimage_order"] == 240
            for row in complement_rows
        ),
        "each_s5_preimage_contains_deck_a": all(
            row["contains_deck_a"]
            for row in complement_rows
        ),
        "all_s5_preimages_have_same_center_order": (
            len(preimage_center_profile) == 1
        ),
        "all_s5_preimages_have_same_derived_order": (
            len(preimage_derived_profile) == 1
        ),
    }

    payload = {
        "certificate_id": (
            "native_g60_lifted_automorphism_group_040"
        ),
        "automorphism_source": str(
            AUT_SOURCE.relative_to(ROOT)
        ),
        "complement_source": str(
            COMPLEMENT_SOURCE.relative_to(ROOT)
        ),
        "lift_source": str(
            LIFT_SOURCE.relative_to(ROOT)
        ),
        "bridge_source": str(
            BRIDGE_SOURCE.relative_to(ROOT)
        ),
        "group_order": len(
            lifted_group
        ),
        "center_order": len(
            lifted_center
        ),
        "derived_subgroup_order": len(
            lifted_derived
        ),
        "abelianization_order": (
            len(lifted_group)
            // len(lifted_derived)
        ),
        "element_order_profile": {
            str(order): count
            for order, count in sorted(
                lifted_order_profile.items()
            )
        },
        "center_element_order_profile": {
            str(order): count
            for order, count in sorted(
                lifted_center_order_profile.items()
            )
        },
        "derived_element_order_profile": {
            str(order): count
            for order, count in sorted(
                lifted_derived_order_profile.items()
            )
        },
        "central_involution_count": len(
            central_involutions
        ),
        "vertex_orbit_0_size": len(
            lifted_orbit_0
        ),
        "vertex_stabilizer_0_order": len(
            lifted_stabilizer_0
        ),
        "s5_preimage_rows": complement_rows,
        "s5_preimage_order_profile": {
            str(order): count
            for order, count in sorted(
                preimage_order_profile.items()
            )
        },
        "s5_preimage_center_order_profile": {
            str(order): count
            for order, count in sorted(
                preimage_center_profile.items()
            )
        },
        "s5_preimage_derived_order_profile": {
            str(order): count
            for order, count in sorted(
                preimage_derived_profile.items()
            )
        },
        "s5_preimage_split_profile": {
            str(status).lower(): count
            for status, count in sorted(
                split_profile.items()
            )
        },
        "classification_result": (
            "The audit constructs the full 480-element group "
            "of G60 automorphisms obtained by lifting all of "
            "Aut(G30). It exports its center, derived subgroup, "
            "abelianization, element-order profile, and action "
            "stabilizer. It also constructs the order-240 "
            "preimage of each of the two S5 complements in "
            "Aut(G30), records the lift-order signatures, and "
            "tests whether either central extension by the "
            "deck involution a splits."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "lifted_480_group_constructed": True,
            "center_and_derived_subgroup_classified": True,
            "two_s5_preimages_constructed": True,
            "s5_extension_split_status_tested": True,
            "schur_double_cover_sign_not_yet_named": True,
            "full_aut_g60_equality_not_yet_proved": True,
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
    print("group_order:", payload["group_order"])
    print("center_order:", payload["center_order"])
    print(
        "derived_subgroup_order:",
        payload["derived_subgroup_order"],
    )
    print(
        "abelianization_order:",
        payload["abelianization_order"],
    )
    print(
        "element_order_profile:",
        payload["element_order_profile"],
    )
    print(
        "center_element_order_profile:",
        payload[
            "center_element_order_profile"
        ],
    )
    print(
        "vertex_orbit_0_size:",
        payload["vertex_orbit_0_size"],
    )
    print(
        "vertex_stabilizer_0_order:",
        payload["vertex_stabilizer_0_order"],
    )

    for row in complement_rows:
        print()
        print(
            "S5 complement",
            row["downstairs_complement_index"],
        )
        print(
            " downstairs stabilizer:",
            row["downstairs_stabilizer_type"],
        )
        print(
            " preimage order:",
            row["preimage_order"],
        )
        print(
            " center:",
            row["preimage_center_order"],
        )
        print(
            " derived:",
            row["preimage_derived_order"],
        )
        print(
            " splits:",
            row["extension_splits"],
        )
        print(
            " order profile:",
            row[
                "preimage_element_order_profile"
            ],
        )
        print(
            " lift signature:",
            row[
                "lift_order_signature_by_downstairs_order"
            ],
        )

    print(
        "classification_result:",
        payload["classification_result"],
    )


if __name__ == "__main__":
    main()
