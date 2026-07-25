#!/usr/bin/env python3
"""Classify the 480-element lifted G60 automorphism group.

This version uses small generating sets and prints timestamped progress.
"""

import json
import sys
import time
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


START_TIME = time.monotonic()


def progress(message):
    elapsed = time.monotonic() - START_TIME
    print(
        f"[{elapsed:8.2f}s] {message}",
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
        "permutation order exceeded search bound"
    )


def closure_from_generators(generators):
    generators = tuple(generators)

    if not generators:
        raise ValueError(
            "generator list must not be empty"
        )

    all_generators = tuple(
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

        for generator in all_generators:
            product = compose(
                generator,
                current,
            )

            if product in subgroup:
                continue

            subgroup.add(product)
            frontier.append(product)

    return frozenset(subgroup)


def greedy_generators(group, label):
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
        generated = closure_from_generators(
            tuple(generators)
        )

        progress(
            f"{label}: generator {len(generators)} "
            f"gives subgroup order {len(generated)}"
        )

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


def normal_closure(seed_elements, ambient_generators):
    seed_elements = tuple(seed_elements)
    ambient_generators = tuple(ambient_generators)

    if not seed_elements:
        unit = identity(
            len(ambient_generators[0])
        )
        return frozenset({unit})

    ambient_with_inverses = tuple(
        dict.fromkeys(
            ambient_generators
            + tuple(
                inverse(generator)
                for generator in ambient_generators
            )
        )
    )

    normal_generators = set(seed_elements)
    last_order = 0
    round_index = 0

    while True:
        round_index += 1

        subgroup = closure_from_generators(
            tuple(normal_generators)
        )

        progress(
            "derived normal-closure round "
            f"{round_index}: subgroup order "
            f"{len(subgroup)}, seed count "
            f"{len(normal_generators)}"
        )

        conjugates = set(normal_generators)

        for element in subgroup:
            for generator in ambient_with_inverses:
                conjugates.add(
                    compose(
                        compose(
                            generator,
                            element,
                        ),
                        inverse(generator),
                    )
                )

        if (
            len(subgroup) == last_order
            and conjugates
            <= subgroup
        ):
            return subgroup

        last_order = len(subgroup)
        normal_generators = conjugates


def center_from_generators(group, generators):
    result = []

    total = len(group)

    for position, element in enumerate(
        group,
        start=1,
    ):
        if all(
            compose(element, generator)
            == compose(generator, element)
            for generator in generators
        ):
            result.append(element)

        if (
            position == total
            or position % 60 == 0
        ):
            progress(
                "center scan: "
                f"{position}/{total}"
            )

    return frozenset(result)


def find_generating_pair(group, label):
    group = frozenset(group)
    elements = tuple(group)
    orders = {
        element: permutation_order(element)
        for element in elements
    }

    preferred_pairs = []

    for left, right in combinations(
        elements,
        2,
    ):
        pair_orders = {
            orders[left],
            orders[right],
        }

        if (
            5 in pair_orders
            and (
                2 in pair_orders
                or 4 in pair_orders
            )
        ):
            preferred_pairs.append(
                (left, right)
            )

    fallback_pairs = combinations(
        elements,
        2,
    )

    tested = 0

    for left, right in (
        preferred_pairs
        if preferred_pairs
        else fallback_pairs
    ):
        tested += 1
        subgroup = closure_from_generators(
            (left, right)
        )

        if len(subgroup) == len(group):
            progress(
                f"{label}: generating pair found "
                f"after {tested} tests with orders "
                f"{orders[left]}, {orders[right]}"
            )

            return left, right

        if tested % 100 == 0:
            progress(
                f"{label}: tested {tested} "
                "candidate generating pairs"
            )

    progress(
        f"{label}: no generating pair found"
    )

    return None


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

    progress("source artifacts loaded")

    identity60 = identity(60)

    deck_a = tuple(
        int(
            bridge["involution_a"][
                str(vertex)
            ]
        )
        for vertex in range(60)
    )

    aut_rows = aut_source[
        "automorphisms"
    ]

    base_row_by_index = {
        int(row["index"]): row
        for row in aut_rows
    }

    base_index_by_permutation = {
        tuple(row["permutation"]): int(
            row["index"]
        )
        for row in aut_rows
    }

    lift_row_by_base_index = {
        int(
            row["g30_automorphism_index"]
        ): row
        for row in lift_source[
            "lift_rows"
        ]
    }

    lifts_by_base_index = {}

    all_lifts = set()

    for base_index, row in (
        lift_row_by_base_index.items()
    ):
        lifts = tuple(
            tuple(lift["permutation"])
            for lift in row["lifts"]
        )

        lifts_by_base_index[
            base_index
        ] = lifts

        all_lifts.update(lifts)

    lifted_group = frozenset(
        all_lifts
    )

    progress(
        "constructed lifted permutation set "
        f"of size {len(lifted_group)}"
    )

    lifted_generators = greedy_generators(
        lifted_group,
        "full lifted group",
    )

    reconstructed_group = (
        closure_from_generators(
            lifted_generators
        )
    )

    progress(
        "computing center from "
        f"{len(lifted_generators)} generators"
    )

    lifted_center = center_from_generators(
        lifted_group,
        lifted_generators,
    )

    progress(
        f"center order is {len(lifted_center)}"
    )

    generator_commutators = {
        commutator(left, right)
        for left in lifted_generators
        for right in lifted_generators
    }

    progress(
        "building derived subgroup from "
        f"{len(generator_commutators)} "
        "generator commutators"
    )

    lifted_derived = normal_closure(
        generator_commutators,
        lifted_generators,
    )

    progress(
        "derived subgroup order is "
        f"{len(lifted_derived)}"
    )

    progress(
        "computing full element-order profile"
    )

    lifted_orders = {}

    for position, element in enumerate(
        lifted_group,
        start=1,
    ):
        lifted_orders[element] = (
            permutation_order(element)
        )

        if (
            position == len(lifted_group)
            or position % 60 == 0
        ):
            progress(
                "order scan: "
                f"{position}/{len(lifted_group)}"
            )

    lifted_order_profile = Counter(
        lifted_orders.values()
    )

    lifted_center_order_profile = Counter(
        lifted_orders[element]
        for element in lifted_center
    )

    lifted_derived_order_profile = Counter(
        lifted_orders[element]
        for element in lifted_derived
    )

    lifted_orbit_0 = {
        element[0]
        for element in lifted_group
    }

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

        label = (
            f"S5 complement {complement_index}"
        )

        progress(
            f"{label}: constructing downstairs group"
        )

        downstairs_group = frozenset(
            tuple(element)
            for element in complement[
                "elements"
            ]
        )

        downstairs_pair = (
            find_generating_pair(
                downstairs_group,
                label,
            )
        )

        if downstairs_pair is None:
            raise RuntimeError(
                f"{label} has no generating pair"
            )

        downstairs_indices = {
            base_index_by_permutation[
                element
            ]
            for element in downstairs_group
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

        progress(
            f"{label}: preimage size "
            f"{len(preimage_group)}"
        )

        preimage_generators = (
            greedy_generators(
                preimage_group,
                f"{label} preimage",
            )
        )

        preimage_center = (
            center_from_generators(
                preimage_group,
                preimage_generators,
            )
        )

        preimage_commutators = {
            commutator(left, right)
            for left in preimage_generators
            for right in preimage_generators
        }

        preimage_derived = normal_closure(
            preimage_commutators,
            preimage_generators,
        )

        preimage_order_profile = Counter(
            lifted_orders[element]
            for element in preimage_group
        )

        lift_signature = defaultdict(
            Counter
        )

        for base_index in (
            downstairs_indices
        ):
            downstairs_order = int(
                base_row_by_index[
                    base_index
                ]["order"]
            )

            for lifted in (
                lifts_by_base_index[
                    base_index
                ]
            ):
                lift_signature[
                    downstairs_order
                ][
                    lifted_orders[lifted]
                ] += 1

        left_base, right_base = (
            downstairs_pair
        )

        left_index = (
            base_index_by_permutation[
                left_base
            ]
        )

        right_index = (
            base_index_by_permutation[
                right_base
            ]
        )

        splitting_lift_pairs = []

        for left_lift in (
            lifts_by_base_index[
                left_index
            ]
        ):
            for right_lift in (
                lifts_by_base_index[
                    right_index
                ]
            ):
                candidate = (
                    closure_from_generators(
                        (
                            left_lift,
                            right_lift,
                        )
                    )
                )

                progress(
                    f"{label}: lift-choice subgroup "
                    f"order {len(candidate)}"
                )

                if (
                    len(candidate) == 120
                    and deck_a not in candidate
                ):
                    splitting_lift_pairs.append({
                        "left_lift_order": (
                            lifted_orders[
                                left_lift
                            ]
                        ),
                        "right_lift_order": (
                            lifted_orders[
                                right_lift
                            ]
                        ),
                        "generated_order": (
                            len(candidate)
                        ),
                    })

        extension_splits = bool(
            splitting_lift_pairs
        )

        progress(
            f"{label}: extension splits = "
            f"{extension_splits}"
        )

        complement_rows.append({
            "downstairs_complement_index": (
                complement_index
            ),
            "downstairs_stabilizer_type": (
                complement[
                    "vertex_stabilizer_0_type"
                ]
            ),
            "downstairs_generating_pair_orders": [
                permutation_order(
                    left_base
                ),
                permutation_order(
                    right_base
                ),
            ],
            "preimage_order": len(
                preimage_group
            ),
            "preimage_generator_count": len(
                preimage_generators
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
            "preimage_element_order_profile": {
                str(order): count
                for order, count
                in sorted(
                    preimage_order_profile.items()
                )
            },
            "lift_order_signature_by_downstairs_order": {
                str(downstairs_order): {
                    str(upstairs_order): count
                    for upstairs_order, count
                    in sorted(
                        profile.items()
                    )
                }
                for downstairs_order, profile
                in sorted(
                    lift_signature.items()
                )
            },
            "splitting_lift_pair_count": len(
                splitting_lift_pairs
            ),
            "splitting_lift_pairs": (
                splitting_lift_pairs
            ),
            "extension_splits": (
                extension_splits
            ),
            "contains_deck_a": (
                deck_a in preimage_group
            ),
        })

    progress("assembling classification receipt")

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
        "small_generators_reconstruct_group": (
            reconstructed_group
            == lifted_group
        ),
        "deck_a_is_central": (
            deck_a in lifted_center
        ),
        "derived_subgroup_is_normal": all(
            compose(
                compose(
                    generator,
                    element,
                ),
                inverse(generator),
            )
            in lifted_derived
            for generator in lifted_generators
            for element in lifted_derived
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
        "s5_preimages_share_center_order": (
            len(preimage_center_profile)
            == 1
        ),
        "s5_preimages_share_derived_order": (
            len(preimage_derived_profile)
            == 1
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
        "runtime_seconds": round(
            time.monotonic() - START_TIME,
            6,
        ),
        "group_order": len(
            lifted_group
        ),
        "generator_count": len(
            lifted_generators
        ),
        "generator_orders": [
            lifted_orders[generator]
            for generator
            in lifted_generators
        ],
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
            for order, count
            in sorted(
                lifted_order_profile.items()
            )
        },
        "center_element_order_profile": {
            str(order): count
            for order, count
            in sorted(
                lifted_center_order_profile.items()
            )
        },
        "derived_element_order_profile": {
            str(order): count
            for order, count
            in sorted(
                lifted_derived_order_profile.items()
            )
        },
        "central_involution_count": sum(
            count
            for order, count
            in lifted_center_order_profile.items()
            if order == 2
        ),
        "vertex_orbit_0_size": len(
            lifted_orbit_0
        ),
        "vertex_stabilizer_0_order": len(
            lifted_stabilizer_0
        ),
        "s5_preimage_rows": (
            complement_rows
        ),
        "s5_preimage_order_profile": {
            str(order): count
            for order, count
            in sorted(
                preimage_order_profile.items()
            )
        },
        "s5_preimage_center_order_profile": {
            str(order): count
            for order, count
            in sorted(
                preimage_center_profile.items()
            )
        },
        "s5_preimage_derived_order_profile": {
            str(order): count
            for order, count
            in sorted(
                preimage_derived_profile.items()
            )
        },
        "s5_preimage_split_profile": {
            str(status).lower(): count
            for status, count
            in sorted(
                split_profile.items()
            )
        },
        "classification_result": (
            "The audit constructs the 480-element group "
            "obtained by lifting Aut(G30), classifies its "
            "center, derived subgroup, abelianization, "
            "element orders, and vertex stabilizer, and "
            "tests the central extension over each explicit "
            "S5 complement by lifting a generating pair."
        ),
        "checks": checks,
        "audit_pass": all(
            checks.values()
        ),
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
        "generator_count:",
        payload["generator_count"],
    )
    print(
        "generator_orders:",
        payload["generator_orders"],
    )
    print(
        "center_order:",
        payload["center_order"],
    )
    print(
        "derived_subgroup_order:",
        payload[
            "derived_subgroup_order"
        ],
    )
    print(
        "abelianization_order:",
        payload[
            "abelianization_order"
        ],
    )
    print(
        "element_order_profile:",
        payload[
            "element_order_profile"
        ],
    )
    print(
        "center_element_order_profile:",
        payload[
            "center_element_order_profile"
        ],
    )
    print(
        "vertex_orbit_0_size:",
        payload[
            "vertex_orbit_0_size"
        ],
    )
    print(
        "vertex_stabilizer_0_order:",
        payload[
            "vertex_stabilizer_0_order"
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
            " downstairs stabilizer:",
            row[
                "downstairs_stabilizer_type"
            ],
        )
        print(
            " downstairs generator orders:",
            row[
                "downstairs_generating_pair_orders"
            ],
        )
        print(
            " preimage order:",
            row["preimage_order"],
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
            " abelianization order:",
            row[
                "preimage_abelianization_order"
            ],
        )
        print(
            " extension splits:",
            row["extension_splits"],
        )
        print(
            " splitting lift pairs:",
            row[
                "splitting_lift_pair_count"
            ],
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

    print()
    print(
        "classification_result:",
        payload[
            "classification_result"
        ],
    )


if __name__ == "__main__":
    main()
