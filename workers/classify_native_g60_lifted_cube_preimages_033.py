#!/usr/bin/env python3
"""Construct and classify the order-16 G60 preimage of each G30 cube."""

import json
from collections import Counter
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

LIFT_SOURCE = (
    ROOT
    / "artifacts/json/"
    "native_g30_automorphism_lifts_to_g60_032.json"
)

CUBE_SOURCE = (
    ROOT
    / "artifacts/json/"
    "native_g30_c2_cube_conjugacy_census_026.json"
)

BRIDGE_SOURCE = (
    ROOT
    / "sources/"
    "project42_g60_to_g30_a_quotient_certificate_035.json"
)

OUTPUT = (
    ROOT
    / "artifacts/json/"
    "native_g60_lifted_cube_preimages_033.json"
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

    for order in range(1, 1000):
        current = compose(permutation, current)

        if current == unit:
            return order

    raise RuntimeError("permutation order search exceeded bound")


def generated_subgroup(generators):
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


def subgroup_intersection(left, right):
    return frozenset(
        set(left).intersection(right)
    )


def classify_order16_group(
    group,
    order_profile,
    center_order,
    derived_order,
    exponent,
    abelian,
):
    involution_count = order_profile.get(2, 0)
    order4_count = order_profile.get(4, 0)
    order8_count = order_profile.get(8, 0)

    if abelian:
        if exponent == 2 and involution_count == 15:
            return "C2_x_C2_x_C2_x_C2"

        if (
            exponent == 4
            and involution_count == 7
            and order4_count == 8
        ):
            return "C4_x_C2_x_C2"

        if (
            exponent == 4
            and involution_count == 3
            and order4_count == 12
        ):
            return "C4_x_C4"

        if (
            exponent == 8
            and involution_count == 3
            and order4_count == 4
            and order8_count == 8
        ):
            return "C8_x_C2"

        if (
            exponent == 16
            and involution_count == 1
        ):
            return "C16"

        return "unidentified_abelian_order16"

    if (
        center_order == 4
        and derived_order == 2
        and exponent == 4
        and involution_count == 11
        and order4_count == 4
    ):
        return "D8_x_C2"

    if (
        center_order == 4
        and derived_order == 2
        and exponent == 4
        and involution_count == 3
        and order4_count == 12
    ):
        return "Q8_x_C2"

    if (
        center_order == 4
        and derived_order == 2
        and exponent == 4
        and involution_count == 7
        and order4_count == 8
    ):
        return "central_product_D8_C4_candidate"

    if (
        center_order == 2
        and derived_order == 2
        and exponent == 8
    ):
        return "dihedral_or_quaternion_semidihedral_order16_candidate"

    return "unidentified_nonabelian_order16"


def main():
    lift_source = json.loads(
        LIFT_SOURCE.read_text()
    )

    cube_source = json.loads(
        CUBE_SOURCE.read_text()
    )

    bridge = json.loads(
        BRIDGE_SOURCE.read_text()
    )

    lift_rows_by_index = {
        int(row["g30_automorphism_index"]): row
        for row in lift_source["lift_rows"]
    }

    base_permutation_to_index = {}

    for row in lift_source["lift_rows"]:
        if not row["lifts"]:
            continue

        base_index = int(
            row["g30_automorphism_index"]
        )

        base_permutation_to_index[
            tuple(
                cube_element
                for cube_element
                in next(
                    aut["permutation"]
                    for aut in json.loads(
                        (
                            ROOT
                            / "artifacts/json/"
                            "native_g30_full_automorphism_action_001.json"
                        ).read_text()
                    )["automorphisms"]
                    if int(aut["index"]) == base_index
                )
            )
        ] = base_index

    deck_a = tuple(
        int(bridge["involution_a"][str(vertex)])
        for vertex in range(60)
    )

    identity60 = identity(60)

    cube_rows = []

    for cube_row in cube_source["cube_rows"]:
        cube_index = int(cube_row["cube_index"])

        base_elements = {
            tuple(element)
            for element in cube_row["elements"]
        }

        base_indices = sorted(
            base_permutation_to_index[element]
            for element in base_elements
        )

        lifted_elements = set()

        for base_index in base_indices:
            lift_row = lift_rows_by_index[
                base_index
            ]

            for lift in lift_row["lifts"]:
                lifted_elements.add(
                    tuple(lift["permutation"])
                )

        lifted_group = frozenset(
            lifted_elements
        )

        generated = generated_subgroup(
            tuple(lifted_group)
        )

        order_profile = Counter(
            permutation_order(element)
            for element in lifted_group
        )

        group_center = center(lifted_group)
        group_derived = derived_subgroup(
            lifted_group
        )

        exponent = max(
            order_profile
        )

        abelian = all(
            compose(left, right)
            == compose(right, left)
            for left, right in combinations(
                lifted_group,
                2,
            )
        )

        abstract_type = classify_order16_group(
            lifted_group,
            order_profile,
            len(group_center),
            len(group_derived),
            exponent,
            abelian,
        )

        complements = []

        for subset in combinations(
            sorted(lifted_group),
            8,
        ):
            subset = frozenset(subset)

            if identity60 not in subset:
                continue

            if deck_a in subset:
                continue

            if generated_subgroup(
                tuple(subset)
            ) != subset:
                continue

            if subgroup_intersection(
                subset,
                {identity60, deck_a},
            ) != {identity60}:
                continue

            complements.append(subset)

        cube_rows.append({
            "cube_index": cube_index,
            "base_cube_order": len(
                base_elements
            ),
            "base_automorphism_indices": (
                base_indices
            ),
            "lifted_preimage_order": len(
                lifted_group
            ),
            "generated_subgroup_order": len(
                generated
            ),
            "contains_identity": (
                identity60 in lifted_group
            ),
            "contains_deck_a": (
                deck_a in lifted_group
            ),
            "element_order_profile": {
                str(order): count
                for order, count in sorted(
                    order_profile.items()
                )
            },
            "exponent": exponent,
            "abelian": abelian,
            "center_order": len(
                group_center
            ),
            "derived_subgroup_order": len(
                group_derived
            ),
            "abstract_group_type": (
                abstract_type
            ),
            "complement_count": len(
                complements
            ),
            "extension_splits": (
                len(complements) > 0
            ),
            "elements": [
                list(element)
                for element in sorted(
                    lifted_group
                )
            ],
            "center_elements": [
                list(element)
                for element in sorted(
                    group_center
                )
            ],
            "derived_subgroup_elements": [
                list(element)
                for element in sorted(
                    group_derived
                )
            ],
        })

    abstract_type_profile = Counter(
        row["abstract_group_type"]
        for row in cube_rows
    )

    split_profile = Counter(
        row["extension_splits"]
        for row in cube_rows
    )

    order_profile_profile = Counter(
        tuple(sorted(
            row["element_order_profile"].items()
        ))
        for row in cube_rows
    )

    checks = {
        "lift_source_audit_pass": (
            lift_source["audit_pass"]
        ),
        "cube_source_audit_pass": (
            cube_source["audit_pass"]
        ),
        "bridge_source_audit_pass": (
            bridge["audit_pass"]
        ),
        "fifteen_cube_preimages_constructed": (
            len(cube_rows) == 15
        ),
        "every_base_cube_has_order_8": all(
            row["base_cube_order"] == 8
            for row in cube_rows
        ),
        "every_preimage_has_order_16": all(
            row["lifted_preimage_order"] == 16
            for row in cube_rows
        ),
        "every_preimage_is_closed_group": all(
            row["generated_subgroup_order"] == 16
            for row in cube_rows
        ),
        "every_preimage_contains_identity_and_deck": all(
            row["contains_identity"]
            and row["contains_deck_a"]
            for row in cube_rows
        ),
        "all_preimages_have_same_abstract_type": (
            len(abstract_type_profile) == 1
        ),
        "all_preimages_have_same_order_profile": (
            len(order_profile_profile) == 1
        ),
        "all_preimages_have_same_split_status": (
            len(split_profile) == 1
        ),
        "no_preimage_type_remains_unidentified": all(
            not row[
                "abstract_group_type"
            ].startswith("unidentified")
            for row in cube_rows
        ),
    }

    common_type = (
        next(iter(abstract_type_profile))
        if len(abstract_type_profile) == 1
        else None
    )

    common_split_status = (
        next(iter(split_profile))
        if len(split_profile) == 1
        else None
    )

    payload = {
        "certificate_id": (
            "native_g60_lifted_cube_preimages_033"
        ),
        "lift_source": str(
            LIFT_SOURCE.relative_to(ROOT)
        ),
        "cube_source": str(
            CUBE_SOURCE.relative_to(ROOT)
        ),
        "bridge_source": str(
            BRIDGE_SOURCE.relative_to(ROOT)
        ),
        "extension_sequence": (
            "1 -> <a> ~= C2 -> lifted cube preimage "
            "-> C2^3 -> 1"
        ),
        "cube_preimage_count": len(
            cube_rows
        ),
        "abstract_group_type_profile": dict(
            sorted(
                abstract_type_profile.items()
            )
        ),
        "split_status_profile": {
            str(status).lower(): count
            for status, count in sorted(
                split_profile.items()
            )
        },
        "common_abstract_group_type": (
            common_type
        ),
        "common_extension_splits": (
            common_split_status
        ),
        "cube_rows": cube_rows,
        "classification_result": (
            "For each of the fifteen intrinsic C2^3 cubes "
            "inside Aut(G30), the full inverse image under "
            "the native G60 lift projection is an explicit "
            "order-16 permutation group containing the deck "
            "involution a. The audit identifies the common "
            "abstract group type and determines whether the "
            "central extension by <a> splits."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "fifteen_lifted_cube_preimages_constructed": True,
            "order16_extension_types_classified": True,
            "extension_split_status_classified": True,
            "preferred_order8_lift_subgroups_not_selected": True,
            "full_aut_g60_identification_not_claimed": True,
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
        "cube_preimage_count:",
        payload["cube_preimage_count"],
    )
    print(
        "abstract_group_type_profile:",
        payload[
            "abstract_group_type_profile"
        ],
    )
    print(
        "split_status_profile:",
        payload["split_status_profile"],
    )
    print(
        "common_abstract_group_type:",
        payload[
            "common_abstract_group_type"
        ],
    )
    print(
        "common_extension_splits:",
        payload[
            "common_extension_splits"
        ],
    )

    for row in cube_rows:
        print(
            "cube",
            row["cube_index"],
            "type:",
            row["abstract_group_type"],
            "orders:",
            row["element_order_profile"],
            "center:",
            row["center_order"],
            "derived:",
            row["derived_subgroup_order"],
            "complements:",
            row["complement_count"],
        )

    print(
        "classification_result:",
        payload["classification_result"],
    )


if __name__ == "__main__":
    main()
