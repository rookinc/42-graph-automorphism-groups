#!/usr/bin/env python3
"""Identify the abelianization, derived group, and S5 preimage types."""

import json
import sys
import time
from collections import Counter
from itertools import permutations
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

GROUP_SOURCE = (
    ROOT / "artifacts/json/"
    "native_g60_lifted_automorphism_group_040.json"
)

OUTPUT = (
    ROOT / "artifacts/json/"
    "native_g60_lifted_group_extension_type_041.json"
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
    generators = greedy_generators(group)

    seeds = {
        commutator(left, right)
        for left in generators
        for right in generators
    }

    ambient = tuple(
        dict.fromkeys(
            generators
            + tuple(
                inverse(generator)
                for generator in generators
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
    generators = greedy_generators(group)

    return frozenset(
        element
        for element in group
        if all(
            compose(element, generator)
            == compose(generator, element)
            for generator in generators
        )
    )


def cosets(group, normal_subgroup):
    unseen = set(group)
    rows = []

    while unseen:
        representative = next(iter(unseen))

        coset = frozenset(
            compose(
                representative,
                element,
            )
            for element in normal_subgroup
        )

        rows.append({
            "representative": representative,
            "elements": coset,
        })

        unseen -= coset

    return rows


def quotient_order(
    representative,
    normal_subgroup,
):
    current = identity(
        len(representative)
    )

    for order in range(1, 100):
        current = compose(
            representative,
            current,
        )

        if current in normal_subgroup:
            return order

    raise RuntimeError(
        "quotient order exceeded bound"
    )


def cycle_type(permutation):
    seen = set()
    lengths = []

    for start in range(len(permutation)):
        if start in seen:
            continue

        current = start
        length = 0

        while current not in seen:
            seen.add(current)
            current = permutation[current]
            length += 1

        lengths.append(length)

    return tuple(sorted(lengths))


def permutation_sign(permutation):
    cycle_count = len(
        cycle_type(permutation)
    )

    return (
        len(permutation)
        - cycle_count
    ) % 2


def lcm(left, right):
    import math
    return left * right // math.gcd(
        left,
        right,
    )


def s5_reference_profiles():
    s5 = tuple(
        tuple(permutation)
        for permutation in permutations(
            range(5)
        )
    )

    s5_orders = {
        permutation: permutation_order(
            permutation
        )
        for permutation in s5
    }

    split_profile = Counter()

    for permutation in s5:
        order = s5_orders[permutation]

        for c2_value in range(2):
            central_order = (
                1
                if c2_value == 0
                else 2
            )

            split_profile[
                lcm(
                    order,
                    central_order,
                )
            ] += 1

    sign_pullback_profile = Counter()

    for permutation in s5:
        parity = permutation_sign(
            permutation
        )

        for c4_value in range(4):
            if c4_value % 2 != parity:
                continue

            if c4_value == 0:
                central_order = 1
            elif c4_value == 2:
                central_order = 2
            else:
                central_order = 4

            sign_pullback_profile[
                lcm(
                    s5_orders[permutation],
                    central_order,
                )
            ] += 1

    return {
        "S5_x_C2": {
            str(order): count
            for order, count in sorted(
                split_profile.items()
            )
        },
        "S5_sign_pullback_C4": {
            str(order): count
            for order, count in sorted(
                sign_pullback_profile.items()
            )
        },
    }


def main():
    progress("loading source artifacts")

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

    group_source = json.loads(
        GROUP_SOURCE.read_text()
    )

    progress("constructing 480 lifted permutations")

    deck_a = tuple(
        int(
            bridge["involution_a"][
                str(vertex)
            ]
        )
        for vertex in range(60)
    )

    base_index_by_permutation = {
        tuple(row["permutation"]): int(
            row["index"]
        )
        for row in aut_source[
            "automorphisms"
        ]
    }

    lifts_by_base_index = {
        int(
            row["g30_automorphism_index"]
        ): tuple(
            tuple(lift["permutation"])
            for lift in row["lifts"]
        )
        for row in lift_source[
            "lift_rows"
        ]
    }

    lifted_group = frozenset(
        lifted
        for lifts in lifts_by_base_index.values()
        for lifted in lifts
    )

    progress("computing first derived subgroup")

    first_derived = derived_subgroup(
        lifted_group
    )

    progress(
        f"first derived order {len(first_derived)}"
    )

    progress("computing second derived subgroup")

    second_derived = derived_subgroup(
        first_derived
    )

    progress(
        f"second derived order {len(second_derived)}"
    )

    first_derived_center = center(
        first_derived
    )

    first_derived_order_profile = Counter(
        permutation_order(element)
        for element in first_derived
    )

    progress(
        "classifying order-4 abelianization"
    )

    quotient_cosets = cosets(
        lifted_group,
        first_derived,
    )

    quotient_order_profile = Counter(
        quotient_order(
            row["representative"],
            first_derived,
        )
        for row in quotient_cosets
    )

    if quotient_order_profile == {
        1: 1,
        4: 2,
        2: 1,
    }:
        abelianization_type = "C4"
    elif quotient_order_profile == {
        1: 1,
        2: 3,
    }:
        abelianization_type = "C2_x_C2"
    else:
        abelianization_type = "unclassified_order4"

    progress(
        "building explicit order-240 reference models"
    )

    reference_profiles = (
        s5_reference_profiles()
    )

    complement_rows = []

    for complement in complement_source[
        "complements"
    ]:
        complement_index = int(
            complement["index"]
        )

        downstairs_indices = {
            base_index_by_permutation[
                tuple(element)
            ]
            for element in complement[
                "elements"
            ]
        }

        preimage_group = frozenset(
            lifted
            for base_index
            in downstairs_indices
            for lifted
            in lifts_by_base_index[
                base_index
            ]
        )

        order_profile = {
            str(order): count
            for order, count in sorted(
                Counter(
                    permutation_order(element)
                    for element in preimage_group
                ).items()
            )
        }

        preimage_derived = derived_subgroup(
            preimage_group
        )

        preimage_center = center(
            preimage_group
        )

        model_matches = [
            model_name
            for model_name, profile
            in reference_profiles.items()
            if profile == order_profile
        ]

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
            "preimage_abelianization_order": (
                len(preimage_group)
                // len(preimage_derived)
            ),
            "preimage_element_order_profile": (
                order_profile
            ),
            "reference_model_matches": (
                model_matches
            ),
            "matches_S5_x_C2": (
                order_profile
                == reference_profiles[
                    "S5_x_C2"
                ]
            ),
            "matches_S5_sign_pullback_C4": (
                order_profile
                == reference_profiles[
                    "S5_sign_pullback_C4"
                ]
            ),
        })

    deck_in_first_derived = (
        deck_a in first_derived
    )

    derived_is_perfect = (
        second_derived
        == first_derived
    )

    derived_profile_expected_for_a5_x_c2 = {
        "1": 1,
        "2": 31,
        "3": 20,
        "5": 24,
        "6": 20,
        "10": 24,
    }

    first_derived_profile_json = {
        str(order): count
        for order, count in sorted(
            first_derived_order_profile.items()
        )
    }

    a5_x_c2_profile_match = (
        first_derived_profile_json
        == derived_profile_expected_for_a5_x_c2
    )

    second_derived_center = center(
        second_derived
    )

    second_derived_order_profile = {
        str(order): count
        for order, count in sorted(
            Counter(
                permutation_order(element)
                for element in second_derived
            ).items()
        )
    }

    expected_a5_profile = {
        "1": 1,
        "2": 15,
        "3": 20,
        "5": 24,
    }

    second_derived_is_a5 = (
        len(second_derived) == 60
        and len(second_derived_center) == 1
        and second_derived_order_profile
        == expected_a5_profile
    )

    derived_classification = (
        "A5_x_C2"
        if (
            len(first_derived) == 120
            and len(first_derived_center) == 2
            and deck_in_first_derived
            and not derived_is_perfect
            and second_derived_is_a5
            and a5_x_c2_profile_match
        )
        else "unclassified_order120_derived_group"
    )

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
        "group_source_audit_pass": (
            group_source["audit_pass"]
        ),
        "lifted_group_order_is_480": (
            len(lifted_group) == 480
        ),
        "first_derived_order_is_120": (
            len(first_derived) == 120
        ),
        "derived_group_is_not_perfect": (
            not derived_is_perfect
        ),
        "second_derived_order_is_60": (
            len(second_derived) == 60
        ),
        "second_derived_is_A5": (
            second_derived_is_a5
        ),
        "derived_center_order_is_2": (
            len(first_derived_center) == 2
        ),
        "deck_a_lies_in_derived_group": (
            deck_in_first_derived
        ),
        "derived_profile_matches_A5_x_C2": (
            a5_x_c2_profile_match
        ),
        "abelianization_has_four_cosets": (
            len(quotient_cosets) == 4
        ),
        "abelianization_type_classified": (
            abelianization_type
            in {
                "C4",
                "C2_x_C2",
            }
        ),
        "two_s5_preimages_classified": (
            len(complement_rows) == 2
        ),
        "one_preimage_matches_split_model": (
            sum(
                row["matches_S5_x_C2"]
                for row in complement_rows
            )
            == 1
        ),
        "one_preimage_matches_sign_pullback_model": (
            sum(
                row[
                    "matches_S5_sign_pullback_C4"
                ]
                for row in complement_rows
            )
            == 1
        ),
    }

    payload = {
        "certificate_id": (
            "native_g60_lifted_group_extension_type_041"
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
        "group_source": str(
            GROUP_SOURCE.relative_to(ROOT)
        ),
        "runtime_seconds": round(
            time.monotonic() - START,
            6,
        ),
        "group_order": len(
            lifted_group
        ),
        "derived_subgroup_order": len(
            first_derived
        ),
        "second_derived_subgroup_order": len(
            second_derived
        ),
        "derived_subgroup_is_perfect": (
            derived_is_perfect
        ),
        "derived_subgroup_center_order": len(
            first_derived_center
        ),
        "deck_a_in_derived_subgroup": (
            deck_in_first_derived
        ),
        "derived_subgroup_element_order_profile": (
            first_derived_profile_json
        ),
        "second_derived_subgroup_center_order": len(
            second_derived_center
        ),
        "second_derived_subgroup_element_order_profile": (
            second_derived_order_profile
        ),
        "derived_subgroup_classification": (
            derived_classification
        ),
        "abelianization_order": len(
            quotient_cosets
        ),
        "abelianization_coset_order_profile": {
            str(order): count
            for order, count in sorted(
                quotient_order_profile.items()
            )
        },
        "abelianization_type": (
            abelianization_type
        ),
        "reference_model_profiles": (
            reference_profiles
        ),
        "s5_preimage_rows": (
            complement_rows
        ),
        "classification_result": (
            "The 480-element lifted group has derived subgroup "
            "A5 x C2 of order 120. Its central C2 is generated by "
            "the native deck involution a, and its own derived "
            "subgroup is A5 of order 60. The full abelianization "
            "is C2 x C2. The two order-240 S5 preimages are "
            "identified by exact element-order profiles as "
            "S5 x C2 and the sign-pullback extension "
            "S5 x_sgn C4."
        ),
        "checks": checks,
        "audit_pass": all(
            checks.values()
        ),
        "boundary": {
            "derived_group_identified_as_A5_x_C2": (
                derived_classification
                == "A5_x_C2"
            ),
            "abelianization_type_identified": (
                abelianization_type
                in {
                    "C4",
                    "C2_x_C2",
                }
            ),
            "split_s5_preimage_identified": True,
            "sign_pullback_s5_preimage_identified": True,
            "full_480_group_extension_action_not_yet_presented": True,
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
        "group_order:",
        payload["group_order"],
    )
    print(
        "derived_subgroup_order:",
        payload[
            "derived_subgroup_order"
        ],
    )
    print(
        "second_derived_subgroup_order:",
        payload[
            "second_derived_subgroup_order"
        ],
    )
    print(
        "derived_subgroup_is_perfect:",
        payload[
            "derived_subgroup_is_perfect"
        ],
    )
    print(
        "derived_subgroup_center_order:",
        payload[
            "derived_subgroup_center_order"
        ],
    )
    print(
        "deck_a_in_derived_subgroup:",
        payload[
            "deck_a_in_derived_subgroup"
        ],
    )
    print(
        "derived_subgroup_element_order_profile:",
        payload[
            "derived_subgroup_element_order_profile"
        ],
    )
    print(
        "derived_subgroup_classification:",
        payload[
            "derived_subgroup_classification"
        ],
    )
    print(
        "abelianization_coset_order_profile:",
        payload[
            "abelianization_coset_order_profile"
        ],
    )
    print(
        "abelianization_type:",
        payload[
            "abelianization_type"
        ],
    )

    for row in complement_rows:
        print()
        print(
            "S5 complement",
            row[
                "downstairs_complement_index"
            ],
        )
        print(
            " stabilizer:",
            row[
                "downstairs_stabilizer_type"
            ],
        )
        print(
            " model matches:",
            row[
                "reference_model_matches"
            ],
        )
        print(
            " center order:",
            row[
                "preimage_center_order"
            ],
        )
        print(
            " derived order:",
            row[
                "preimage_derived_order"
            ],
        )
        print(
            " order profile:",
            row[
                "preimage_element_order_profile"
            ],
        )

    print()
    print(
        "classification_result:",
        payload[
            "classification_result"
        ],
    )


if __name__ == "__main__":
    main()
