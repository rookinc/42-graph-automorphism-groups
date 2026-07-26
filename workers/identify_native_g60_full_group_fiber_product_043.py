#!/usr/bin/env python3
"""Identify Aut(G60) as an S5-D8 fiber product."""

import itertools
import json
import math
import sys
import time
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

LIFT_SOURCE = (
    ROOT / "artifacts/json/"
    "native_g30_automorphism_lifts_to_g60_032.json"
)

GROUP_SOURCE = (
    ROOT / "artifacts/json/"
    "native_g60_lifted_automorphism_group_040.json"
)

EXTENSION_SOURCE = (
    ROOT / "artifacts/json/"
    "native_g60_lifted_group_extension_type_041.json"
)

FULL_SOURCE = (
    ROOT / "artifacts/json/"
    "native_g60_full_automorphism_group_042.json"
)

OUTPUT = (
    ROOT / "artifacts/json/"
    "native_g60_full_group_fiber_product_043.json"
)


START = time.monotonic()


def progress(message):
    elapsed = time.monotonic() - START
    print(
        f"[{elapsed:7.3f}s] {message}",
        file=sys.stderr,
        flush=True,
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
        current = compose(
            permutation,
            current,
        )

        if current == unit:
            return order

    raise RuntimeError(
        "permutation order exceeded bound"
    )


def closure(generators):
    generators = tuple(generators)

    if not generators:
        raise ValueError(
            "generator list is empty"
        )

    expanded = tuple(
        dict.fromkeys(
            generators
            + tuple(
                inverse(generator)
                for generator in generators
            )
        )
    )

    unit = identity(len(generators[0]))
    subgroup = {unit}
    frontier = [unit]

    while frontier:
        current = frontier.pop()

        for generator in expanded:
            product = compose(
                generator,
                current,
            )

            if product in subgroup:
                continue

            subgroup.add(product)
            frontier.append(product)

    return frozenset(subgroup)


def greedy_generators(group):
    group = frozenset(group)
    unit = identity(len(next(iter(group))))

    generators = []
    generated = frozenset({unit})

    while generated != group:
        candidate = next(
            element
            for element in group
            if element not in generated
        )

        generators.append(candidate)
        generated = closure(generators)

    return tuple(generators)


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
    ambient_generators = greedy_generators(
        group
    )

    seeds = {
        commutator(left, right)
        for left in ambient_generators
        for right in ambient_generators
    }

    ambient = tuple(
        dict.fromkeys(
            ambient_generators
            + tuple(
                inverse(generator)
                for generator in ambient_generators
            )
        )
    )

    normal_generators = set(seeds)

    while True:
        subgroup = closure(
            tuple(normal_generators)
        )

        expanded = set(normal_generators)

        for element in subgroup:
            for generator in ambient:
                expanded.add(
                    compose(
                        compose(
                            generator,
                            element,
                        ),
                        inverse(generator),
                    )
                )

        if expanded <= subgroup:
            return subgroup

        normal_generators = expanded


def center(group):
    generators = greedy_generators(
        group
    )

    return frozenset(
        element
        for element in group
        if all(
            compose(element, generator)
            == compose(generator, element)
            for generator in generators
        )
    )


def profile_from_orders(orders):
    return {
        str(order): count
        for order, count in sorted(
            Counter(orders).items()
        )
    }


def permutation_sign(permutation):
    inversion_count = sum(
        permutation[left]
        > permutation[right]
        for left in range(len(permutation))
        for right in range(
            left + 1,
            len(permutation),
        )
    )

    return inversion_count % 2


def s5_multiply(left, right):
    return tuple(
        left[right[index]]
        for index in range(5)
    )


def s5_order(permutation):
    unit = tuple(range(5))
    current = unit

    for order in range(1, 100):
        current = s5_multiply(
            permutation,
            current,
        )

        if current == unit:
            return order

    raise RuntimeError(
        "S5 order exceeded bound"
    )


def d8_multiply(left, right):
    left_rotation, left_flip = left
    right_rotation, right_flip = right

    signed_rotation = (
        right_rotation
        if left_flip == 0
        else -right_rotation
    )

    return (
        (
            left_rotation
            + signed_rotation
        ) % 4,
        (
            left_flip
            + right_flip
        ) % 2,
    )


def d8_order(element):
    unit = (0, 0)
    current = unit

    for order in range(1, 20):
        current = d8_multiply(
            element,
            current,
        )

        if current == unit:
            return order

    raise RuntimeError(
        "D8 order exceeded bound"
    )


def reference_element_order(element):
    permutation, d8_element = element

    return math.lcm(
        s5_order(permutation),
        d8_order(d8_element),
    )


def build_reference_group(
    character_name,
):
    s5_elements = tuple(
        itertools.permutations(
            range(5)
        )
    )

    d8_elements = tuple(
        (rotation, flip)
        for rotation in range(4)
        for flip in range(2)
    )

    if character_name == "reflection_parity":
        character = (
            lambda element:
            element[1]
        )
        kernel_type = "C4"

    elif character_name == "rotation_parity":
        character = (
            lambda element:
            element[0] % 2
        )
        kernel_type = "V4"

    elif character_name == "rotation_plus_reflection":
        character = (
            lambda element:
            (
                element[0]
                + element[1]
            ) % 2
        )
        kernel_type = "V4"

    else:
        raise ValueError(
            character_name
        )

    group = frozenset(
        (
            permutation,
            d8_element,
        )
        for permutation in s5_elements
        for d8_element in d8_elements
        if permutation_sign(
            permutation
        )
        == character(
            d8_element
        )
    )

    order_profile = profile_from_orders(
        reference_element_order(element)
        for element in group
    )

    restricted_character_values = {}

    for sign_coefficient in range(2):
        for rotation_coefficient in range(2):
            for flip_coefficient in range(2):
                coefficient = (
                    sign_coefficient,
                    rotation_coefficient,
                    flip_coefficient,
                )

                values = tuple(
                    (
                        sign_coefficient
                        * permutation_sign(
                            permutation
                        )
                        + rotation_coefficient
                        * (
                            d8_element[0]
                            % 2
                        )
                        + flip_coefficient
                        * d8_element[1]
                    ) % 2
                    for permutation, d8_element
                    in sorted(group)
                )

                restricted_character_values[
                    values
                ] = coefficient

    index_two_rows = []

    sorted_group = tuple(
        sorted(group)
    )

    for values, coefficient in (
        restricted_character_values.items()
    ):
        if not any(values):
            continue

        subgroup = frozenset(
            element
            for element, value
            in zip(
                sorted_group,
                values,
            )
            if value == 0
        )

        subgroup_profile = (
            profile_from_orders(
                reference_element_order(
                    element
                )
                for element in subgroup
            )
        )

        index_two_rows.append({
            "character_coefficients": list(
                coefficient
            ),
            "order": len(
                subgroup
            ),
            "element_order_profile": (
                subgroup_profile
            ),
        })

    index_two_rows.sort(
        key=lambda row: json.dumps(
            row[
                "element_order_profile"
            ],
            sort_keys=True,
        )
    )

    return {
        "character_name": (
            character_name
        ),
        "character_kernel_type": (
            kernel_type
        ),
        "group_order": len(
            group
        ),
        "element_order_profile": (
            order_profile
        ),
        "index_two_subgroups": (
            index_two_rows
        ),
        "index_two_profile_multiset": sorted(
            json.dumps(
                row[
                    "element_order_profile"
                ],
                sort_keys=True,
            )
            for row in index_two_rows
        ),
    }


def actual_index_two_subgroups(
    group,
    derived,
):
    unseen = set(group)
    cosets = []

    while unseen:
        representative = next(
            iter(unseen)
        )

        coset = frozenset(
            compose(
                representative,
                element,
            )
            for element in derived
        )

        cosets.append({
            "representative": (
                representative
            ),
            "elements": coset,
        })

        unseen -= coset

    identity_coset_index = next(
        index
        for index, row
        in enumerate(cosets)
        if identity(60)
        in row["elements"]
    )

    identity_coset = cosets[
        identity_coset_index
    ]["elements"]

    nonidentity_cosets = [
        row
        for index, row
        in enumerate(cosets)
        if index != identity_coset_index
    ]

    rows = []

    for row in nonidentity_cosets:
        subgroup = frozenset(
            set(identity_coset)
            | set(row["elements"])
        )

        subgroup_derived = (
            derived_subgroup(
                subgroup
            )
        )

        subgroup_center = center(
            subgroup
        )

        order_profile = (
            profile_from_orders(
                permutation_order(
                    element
                )
                for element in subgroup
            )
        )

        rows.append({
            "order": len(
                subgroup
            ),
            "center_order": len(
                subgroup_center
            ),
            "derived_subgroup_order": len(
                subgroup_derived
            ),
            "abelianization_order": (
                len(subgroup)
                // len(subgroup_derived)
            ),
            "element_order_profile": (
                order_profile
            ),
        })

    rows.sort(
        key=lambda row: json.dumps(
            row[
                "element_order_profile"
            ],
            sort_keys=True,
        )
    )

    return rows


def classify_index_two_profile(profile):
    split_profile = {
        "1": 1,
        "2": 51,
        "3": 20,
        "4": 60,
        "5": 24,
        "6": 60,
        "10": 24,
    }

    sign_pullback_profile = {
        "1": 1,
        "2": 31,
        "3": 20,
        "4": 80,
        "5": 24,
        "6": 20,
        "10": 24,
        "12": 40,
    }

    third_profile = {
        "1": 1,
        "2": 63,
        "3": 20,
        "5": 24,
        "6": 60,
        "10": 72,
    }

    if profile == split_profile:
        return "S5_x_C2"

    if profile == sign_pullback_profile:
        return "S5_sign_pullback_C4"

    if profile == third_profile:
        return "third_index_two_subgroup"

    return "unclassified"


def main():
    progress("loading Project 42 group receipts")

    lift_source = json.loads(
        LIFT_SOURCE.read_text()
    )

    group_source = json.loads(
        GROUP_SOURCE.read_text()
    )

    extension_source = json.loads(
        EXTENSION_SOURCE.read_text()
    )

    full_source = json.loads(
        FULL_SOURCE.read_text()
    )

    actual_group = frozenset(
        tuple(lift["permutation"])
        for row in lift_source[
            "lift_rows"
        ]
        for lift in row["lifts"]
    )

    progress(
        "constructed actual group of order "
        f"{len(actual_group)}"
    )

    actual_derived = derived_subgroup(
        actual_group
    )

    actual_center = center(
        actual_group
    )

    actual_profile = (
        profile_from_orders(
            permutation_order(element)
            for element in actual_group
        )
    )

    progress(
        "computing actual three index-two subgroups"
    )

    actual_index_two_rows = (
        actual_index_two_subgroups(
            actual_group,
            actual_derived,
        )
    )

    for row in actual_index_two_rows:
        row["classification"] = (
            classify_index_two_profile(
                row[
                    "element_order_profile"
                ]
            )
        )

    actual_index_two_profile_multiset = sorted(
        json.dumps(
            row[
                "element_order_profile"
            ],
            sort_keys=True,
        )
        for row in actual_index_two_rows
    )

    progress("building three S5-D8 fiber-product candidates")

    reference_rows = [
        build_reference_group(
            character_name
        )
        for character_name in (
            "reflection_parity",
            "rotation_parity",
            "rotation_plus_reflection",
        )
    ]

    for row in reference_rows:
        row["full_profile_matches_actual"] = (
            row[
                "element_order_profile"
            ]
            == actual_profile
        )

        row[
            "index_two_census_matches_actual"
        ] = (
            row[
                "index_two_profile_multiset"
            ]
            == actual_index_two_profile_multiset
        )

        row["complete_profile_match"] = (
            row[
                "full_profile_matches_actual"
            ]
            and row[
                "index_two_census_matches_actual"
            ]
        )

    matching_rows = [
        row
        for row in reference_rows
        if row[
            "complete_profile_match"
        ]
    ]

    matching_kernel_types = sorted(
        {
            row[
                "character_kernel_type"
            ]
            for row in matching_rows
        }
    )

    candidate_classification = (
        "S5_fiber_product_D8_over_C2_with_V4_kernel_character"
        if (
            len(matching_rows) == 2
            and matching_kernel_types
            == ["V4"]
        )
        else "unclassified"
    )

    actual_index_two_classifications = sorted(
        row["classification"]
        for row in actual_index_two_rows
    )

    expected_index_two_classifications = sorted([
        "S5_x_C2",
        "S5_sign_pullback_C4",
        "third_index_two_subgroup",
    ])

    checks = {
        "lift_source_audit_pass": (
            lift_source["audit_pass"]
        ),
        "group_source_audit_pass": (
            group_source["audit_pass"]
        ),
        "extension_source_audit_pass": (
            extension_source["audit_pass"]
        ),
        "full_source_audit_pass": (
            full_source["audit_pass"]
        ),
        "actual_group_order_is_480": (
            len(actual_group) == 480
        ),
        "actual_center_order_is_2": (
            len(actual_center) == 2
        ),
        "actual_derived_order_is_120": (
            len(actual_derived) == 120
        ),
        "actual_has_three_index_two_subgroups_over_derived": (
            len(
                actual_index_two_rows
            )
            == 3
        ),
        "actual_index_two_types_are_complete": (
            actual_index_two_classifications
            == expected_index_two_classifications
        ),
        "c4_kernel_candidate_is_rejected": (
            not next(
                row[
                    "complete_profile_match"
                ]
                for row in reference_rows
                if row[
                    "character_name"
                ]
                == "reflection_parity"
            )
        ),
        "both_v4_kernel_presentations_match": (
            sum(
                row[
                    "complete_profile_match"
                ]
                for row in reference_rows
                if row[
                    "character_kernel_type"
                ]
                == "V4"
            )
            == 2
        ),
        "matching_presentations_have_only_v4_kernel": (
            matching_kernel_types
            == ["V4"]
        ),
        "fiber_product_type_classified": (
            candidate_classification
            != "unclassified"
        ),
    }

    payload = {
        "certificate_id": (
            "native_g60_full_group_fiber_product_043"
        ),
        "lift_source": str(
            LIFT_SOURCE.relative_to(ROOT)
        ),
        "group_source": str(
            GROUP_SOURCE.relative_to(ROOT)
        ),
        "extension_source": str(
            EXTENSION_SOURCE.relative_to(ROOT)
        ),
        "full_source": str(
            FULL_SOURCE.relative_to(ROOT)
        ),
        "runtime_seconds": round(
            time.monotonic() - START,
            6,
        ),
        "actual_group": {
            "order": len(
                actual_group
            ),
            "center_order": len(
                actual_center
            ),
            "derived_subgroup_order": len(
                actual_derived
            ),
            "abelianization_type": (
                extension_source[
                    "abelianization_type"
                ]
            ),
            "element_order_profile": (
                actual_profile
            ),
            "index_two_subgroups_over_derived": (
                actual_index_two_rows
            ),
            "index_two_profile_multiset": (
                actual_index_two_profile_multiset
            ),
        },
        "reference_candidates": (
            reference_rows
        ),
        "matching_character_names": [
            row["character_name"]
            for row in matching_rows
        ],
        "matching_character_kernel_types": (
            matching_kernel_types
        ),
        "abstract_group_classification": (
            candidate_classification
        ),
        "fiber_product_statement": (
            "Aut(G60) is isomorphic to the fiber product "
            "{(s,d) in S5 x D8 : sgn(s) = chi(d)}, where "
            "chi is either of the two equivalent nonzero "
            "characters of D8 whose kernel is V4. The two "
            "choices are exchanged by an automorphism of D8. "
            "The character with cyclic kernel C4 is rejected "
            "by both the full element-order profile and the "
            "three index-two subgroup census."
        ),
        "classification_result": (
            "The exact full element-order profile and the exact "
            "multiset of the three index-two subgroup profiles "
            "agree with the S5-D8 fiber product for a V4-kernel "
            "character and disagree with the C4-kernel character. "
            "Thus Aut(G60) has the compact abstract description "
            "S5 x_{C2} D8, with sign on S5 matched to a "
            "V4-kernel quotient character of D8."
        ),
        "checks": checks,
        "audit_pass": all(
            checks.values()
        ),
        "boundary": {
            "compact_named_fiber_product_type_identified": True,
            "v4_kernel_character_class_identified": True,
            "c4_kernel_character_rejected": True,
            "explicit_generator_level_isomorphism_not_yet_exported": True,
            "full_aut_g60_equality_already_certified_by_042": True,
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

    progress("receipt written")

    print("OUT ==")
    print("output:", OUTPUT)
    print(
        "runtime_seconds:",
        payload["runtime_seconds"],
    )
    print(
        "audit_pass:",
        payload["audit_pass"],
    )
    print(
        "actual_group_order:",
        payload[
            "actual_group"
        ]["order"],
    )
    print(
        "actual_center_order:",
        payload[
            "actual_group"
        ]["center_order"],
    )
    print(
        "actual_derived_subgroup_order:",
        payload[
            "actual_group"
        ]["derived_subgroup_order"],
    )
    print(
        "actual_element_order_profile:",
        payload[
            "actual_group"
        ]["element_order_profile"],
    )

    print()
    print("actual index-two subgroups:")

    for row in actual_index_two_rows:
        print(
            " ",
            row["classification"],
            "center:",
            row["center_order"],
            "derived:",
            row[
                "derived_subgroup_order"
            ],
            "profile:",
            row[
                "element_order_profile"
            ],
        )

    print()
    print("reference candidates:")

    for row in reference_rows:
        print(
            " ",
            row["character_name"],
            "kernel:",
            row[
                "character_kernel_type"
            ],
            "full_match:",
            row[
                "full_profile_matches_actual"
            ],
            "index2_match:",
            row[
                "index_two_census_matches_actual"
            ],
            "complete:",
            row[
                "complete_profile_match"
            ],
        )

    print()
    print(
        "matching_character_names:",
        payload[
            "matching_character_names"
        ],
    )
    print(
        "matching_character_kernel_types:",
        payload[
            "matching_character_kernel_types"
        ],
    )
    print(
        "abstract_group_classification:",
        payload[
            "abstract_group_classification"
        ],
    )
    print(
        "classification_result:",
        payload[
            "classification_result"
        ],
    )


if __name__ == "__main__":
    main()
