#!/usr/bin/env python3
"""Identify the abstract group type of the C2^3 normalizer."""

import json
from collections import Counter, deque
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_c2_cube_normalizer_020.json"
)

OUTPUT = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_c2_cube_normalizer_group_021.json"
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


def permutation_order(permutation):
    identity = tuple(range(len(permutation)))
    current = identity
    order = 0

    while True:
        order += 1
        current = compose(permutation, current)

        if current == identity:
            return order


def generated_subgroup(generators, identity):
    expanded = set(generators)

    expanded.update(
        inverse(generator)
        for generator in generators
    )

    subgroup = {identity}
    queue = deque([identity])

    while queue:
        current = queue.popleft()

        for generator in expanded:
            product = compose(generator, current)

            if product in subgroup:
                continue

            subgroup.add(product)
            queue.append(product)

    return frozenset(subgroup)


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


def is_normal(subgroup, group):
    return all(
        compose(
            compose(carrier, element),
            inverse(carrier),
        )
        in subgroup
        for carrier in group
        for element in subgroup
    )


def main():
    source = json.loads(SOURCE.read_text())

    normalizer = frozenset(
        tuple(row["carrier"])
        for row in source["normalizer_action_rows"]
    )

    degree = len(next(iter(normalizer)))
    identity = tuple(range(degree))

    center = frozenset(
        element
        for element in normalizer
        if all(
            compose(element, other)
            == compose(other, element)
            for other in normalizer
        )
    )

    commutators = {
        commutator(left, right)
        for left in normalizer
        for right in normalizer
    }

    derived = generated_subgroup(
        tuple(commutators),
        identity,
    )

    order4_elements = tuple(sorted(
        element
        for element in normalizer
        if permutation_order(element) == 4
    ))

    involutions = tuple(sorted(
        element
        for element in normalizer
        if element != identity
        and permutation_order(element) == 2
    ))

    d8_candidates = []

    for rotation in order4_elements:
        for reflection in involutions:
            subgroup = generated_subgroup(
                (rotation, reflection),
                identity,
            )

            if len(subgroup) != 8:
                continue

            profile = Counter(
                permutation_order(element)
                for element in subgroup
            )

            if dict(sorted(profile.items())) != {
                1: 1,
                2: 5,
                4: 2,
            }:
                continue

            if compose(
                compose(reflection, rotation),
                reflection,
            ) != inverse(rotation):
                continue

            d8_candidates.append({
                "rotation": rotation,
                "reflection": reflection,
                "subgroup": subgroup,
            })

    direct_product_candidates = []

    for candidate in d8_candidates:
        d8 = candidate["subgroup"]

        for central_involution in center:
            if central_involution == identity:
                continue

            central_c2 = frozenset({
                identity,
                central_involution,
            })

            intersection = d8.intersection(central_c2)

            generated = generated_subgroup(
                tuple(d8 | central_c2),
                identity,
            )

            if intersection != {identity}:
                continue

            if generated != normalizer:
                continue

            direct_product_candidates.append({
                "rotation": candidate["rotation"],
                "reflection": candidate["reflection"],
                "d8": d8,
                "central_involution": central_involution,
                "central_c2": central_c2,
            })

    witness = (
        direct_product_candidates[0]
        if direct_product_candidates
        else None
    )

    normalizer_profile = Counter(
        permutation_order(element)
        for element in normalizer
    )

    center_profile = Counter(
        permutation_order(element)
        for element in center
    )

    derived_profile = Counter(
        permutation_order(element)
        for element in derived
    )

    abstract_type = (
        "D8_x_C2"
        if witness is not None
        else "unclassified"
    )

    checks = {
        "source_audit_pass": source["audit_pass"],
        "normalizer_order_is_16": (
            len(normalizer) == 16
        ),
        "normalizer_profile_matches_d8_x_c2": (
            dict(sorted(normalizer_profile.items()))
            == {1: 1, 2: 11, 4: 4}
        ),
        "center_order_is_4": len(center) == 4,
        "derived_subgroup_order_is_2": (
            len(derived) == 2
        ),
        "derived_subgroup_is_central": (
            derived.issubset(center)
        ),
        "d8_subgroup_found": (
            len(d8_candidates) > 0
        ),
        "internal_direct_product_witness_found": (
            witness is not None
        ),
        "d8_factor_is_normal": (
            witness is not None
            and is_normal(
                witness["d8"],
                normalizer,
            )
        ),
        "central_c2_factor_is_normal": (
            witness is not None
            and is_normal(
                witness["central_c2"],
                normalizer,
            )
        ),
    }

    payload = {
        "certificate_id": (
            "native_g30_c2_cube_normalizer_group_021"
        ),
        "source": str(SOURCE.relative_to(ROOT)),
        "normalizer_order": len(normalizer),
        "normalizer_element_order_profile": {
            str(order): count
            for order, count in sorted(
                normalizer_profile.items()
            )
        },
        "center_order": len(center),
        "center_element_order_profile": {
            str(order): count
            for order, count in sorted(
                center_profile.items()
            )
        },
        "derived_subgroup_order": len(derived),
        "derived_subgroup_element_order_profile": {
            str(order): count
            for order, count in sorted(
                derived_profile.items()
            )
        },
        "d8_candidate_count": len(
            d8_candidates
        ),
        "internal_direct_product_candidate_count": len(
            direct_product_candidates
        ),
        "abstract_group_type": abstract_type,
        "direct_product_witness": (
            {
                "rotation_order": permutation_order(
                    witness["rotation"]
                ),
                "reflection_order": permutation_order(
                    witness["reflection"]
                ),
                "rotation": list(
                    witness["rotation"]
                ),
                "reflection": list(
                    witness["reflection"]
                ),
                "d8_factor_order": len(
                    witness["d8"]
                ),
                "d8_factor_element_order_profile": {
                    str(order): count
                    for order, count in sorted(
                        Counter(
                            permutation_order(element)
                            for element in witness["d8"]
                        ).items()
                    )
                },
                "central_involution": list(
                    witness["central_involution"]
                ),
                "central_c2_factor_order": len(
                    witness["central_c2"]
                ),
                "factor_intersection_order": len(
                    witness["d8"].intersection(
                        witness["central_c2"]
                    )
                ),
                "factor_product_order": len(
                    generated_subgroup(
                        tuple(
                            witness["d8"]
                            | witness["central_c2"]
                        ),
                        identity,
                    )
                ),
            }
            if witness is not None
            else None
        ),
        "classification_result": (
            "The normalizer is explicitly identified as "
            "D8 x C2 by an internal direct-product witness: "
            "a normal dihedral subgroup of order 8 and a "
            "central order-2 subgroup with trivial "
            "intersection whose product is the full "
            "order-16 normalizer."
            if witness is not None
            else
            "No internal D8 x C2 direct-product witness "
            "was found."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "normalizer_abstract_group_type_identified": (
                witness is not None
            ),
            "internal_direct_product_witness_exported": (
                witness is not None
            ),
            "normalizer_action_on_cube_coordinates_open": True,
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
    print("normalizer_order:", payload["normalizer_order"])
    print(
        "normalizer_element_order_profile:",
        payload["normalizer_element_order_profile"],
    )
    print("center_order:", payload["center_order"])
    print(
        "center_element_order_profile:",
        payload["center_element_order_profile"],
    )
    print(
        "derived_subgroup_order:",
        payload["derived_subgroup_order"],
    )
    print(
        "d8_candidate_count:",
        payload["d8_candidate_count"],
    )
    print(
        "internal_direct_product_candidate_count:",
        payload[
            "internal_direct_product_candidate_count"
        ],
    )
    print(
        "abstract_group_type:",
        payload["abstract_group_type"],
    )
    print(
        "classification_result:",
        payload["classification_result"],
    )


if __name__ == "__main__":
    main()
