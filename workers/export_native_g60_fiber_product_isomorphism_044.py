#!/usr/bin/env python3
"""Export an explicit generator-level isomorphism for Aut(G60)."""

import hashlib
import itertools
import json
import sys
import time
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

LIFT_SOURCE = (
    ROOT / "artifacts/json/"
    "native_g30_automorphism_lifts_to_g60_032.json"
)

FIBER_PRODUCT_SOURCE = (
    ROOT / "artifacts/json/"
    "native_g60_full_group_fiber_product_043.json"
)

OUTPUT = (
    ROOT / "artifacts/json/"
    "native_g60_fiber_product_isomorphism_044.json"
)


START = time.monotonic()


def progress(message):
    elapsed = time.monotonic() - START
    print(
        f"[{elapsed:8.3f}s] {message}",
        file=sys.stderr,
        flush=True,
    )


def permutation_identity(size):
    return tuple(range(size))


def permutation_compose(left, right):
    return tuple(
        left[right[index]]
        for index in range(len(left))
    )


def permutation_inverse(permutation):
    result = [None] * len(permutation)

    for source, target in enumerate(permutation):
        result[target] = source

    return tuple(result)


def permutation_order(permutation):
    unit = permutation_identity(
        len(permutation)
    )

    current = unit

    for order in range(1, 1000):
        current = permutation_compose(
            permutation,
            current,
        )

        if current == unit:
            return order

    raise RuntimeError(
        "permutation order exceeded bound"
    )


def permutation_commutator(left, right):
    return permutation_compose(
        permutation_compose(
            permutation_compose(
                permutation_inverse(left),
                permutation_inverse(right),
            ),
            left,
        ),
        right,
    )


def permutation_closure(generators):
    generators = tuple(generators)

    expanded = tuple(
        dict.fromkeys(
            generators
            + tuple(
                permutation_inverse(generator)
                for generator in generators
            )
        )
    )

    unit = permutation_identity(
        len(generators[0])
    )

    subgroup = {unit}
    frontier = [unit]

    while frontier:
        current = frontier.pop()

        for generator in expanded:
            product = permutation_compose(
                generator,
                current,
            )

            if product in subgroup:
                continue

            subgroup.add(product)
            frontier.append(product)

    return frozenset(subgroup)


def greedy_permutation_generators(group):
    group = frozenset(group)

    unit = permutation_identity(
        len(next(iter(group)))
    )

    generators = []
    generated = frozenset({unit})

    while generated != group:
        candidate = min(
            element
            for element in group
            if element not in generated
        )

        generators.append(candidate)

        generated = permutation_closure(
            generators
        )

        progress(
            "actual generator "
            f"{len(generators)} gives order "
            f"{len(generated)}"
        )

    return tuple(generators)


def s5_identity():
    return tuple(range(5))


def s5_multiply(left, right):
    return tuple(
        left[right[index]]
        for index in range(5)
    )


def s5_inverse(permutation):
    result = [None] * 5

    for source, target in enumerate(permutation):
        result[target] = source

    return tuple(result)


def s5_sign(permutation):
    inversion_count = sum(
        permutation[left]
        > permutation[right]
        for left in range(5)
        for right in range(left + 1, 5)
    )

    return inversion_count % 2


def d8_multiply(left, right):
    left_rotation, left_flip = left
    right_rotation, right_flip = right

    signed_right_rotation = (
        right_rotation
        if left_flip == 0
        else -right_rotation
    )

    return (
        (
            left_rotation
            + signed_right_rotation
        ) % 4,
        (
            left_flip
            + right_flip
        ) % 2,
    )


def d8_inverse(element):
    rotation, flip = element

    if flip == 0:
        return ((-rotation) % 4, 0)

    return (rotation, 1)


def reference_identity():
    return (
        s5_identity(),
        (0, 0),
    )


def reference_multiply(left, right):
    return (
        s5_multiply(
            left[0],
            right[0],
        ),
        d8_multiply(
            left[1],
            right[1],
        ),
    )


def reference_inverse(element):
    return (
        s5_inverse(element[0]),
        d8_inverse(element[1]),
    )


def reference_order(element):
    unit = reference_identity()
    current = unit

    for order in range(1, 1000):
        current = reference_multiply(
            element,
            current,
        )

        if current == unit:
            return order

    raise RuntimeError(
        "reference order exceeded bound"
    )


def reference_commutator(left, right):
    return reference_multiply(
        reference_multiply(
            reference_multiply(
                reference_inverse(left),
                reference_inverse(right),
            ),
            left,
        ),
        right,
    )


def build_reference_group():
    return frozenset(
        (
            tuple(permutation),
            (rotation, flip),
        )
        for permutation in itertools.permutations(
            range(5)
        )
        for rotation in range(4)
        for flip in range(2)
        if s5_sign(permutation)
        == rotation % 2
    )


def pair_signature_actual(left, right):
    return (
        permutation_order(
            permutation_compose(
                left,
                right,
            )
        ),
        permutation_order(
            permutation_compose(
                permutation_inverse(left),
                right,
            )
        ),
        permutation_order(
            permutation_commutator(
                left,
                right,
            )
        ),
    )


def pair_signature_reference(left, right):
    return (
        reference_order(
            reference_multiply(
                left,
                right,
            )
        ),
        reference_order(
            reference_multiply(
                reference_inverse(left),
                right,
            )
        ),
        reference_order(
            reference_commutator(
                left,
                right,
            )
        ),
    )


def extend_generator_assignment(
    actual_generators,
    reference_generators,
    actual_group,
    reference_group,
):
    actual_unit = permutation_identity(60)
    reference_unit = reference_identity()

    actual_steps = tuple(
        actual_generators
        + tuple(
            permutation_inverse(generator)
            for generator in actual_generators
        )
    )

    reference_steps = tuple(
        reference_generators
        + tuple(
            reference_inverse(generator)
            for generator in reference_generators
        )
    )

    forward = {
        actual_unit: reference_unit
    }

    reverse = {
        reference_unit: actual_unit
    }

    frontier = [actual_unit]

    while frontier:
        actual_current = frontier.pop()
        reference_current = forward[
            actual_current
        ]

        for actual_step, reference_step in zip(
            actual_steps,
            reference_steps,
        ):
            actual_next = permutation_compose(
                actual_step,
                actual_current,
            )

            reference_next = reference_multiply(
                reference_step,
                reference_current,
            )

            known_reference = forward.get(
                actual_next
            )

            if (
                known_reference is not None
                and known_reference
                != reference_next
            ):
                return None

            known_actual = reverse.get(
                reference_next
            )

            if (
                known_actual is not None
                and known_actual
                != actual_next
            ):
                return None

            if known_reference is None:
                forward[
                    actual_next
                ] = reference_next

                reverse[
                    reference_next
                ] = actual_next

                frontier.append(
                    actual_next
                )

    if len(forward) != len(actual_group):
        return None

    if len(reverse) != len(reference_group):
        return None

    return forward


def encode_reference(element):
    permutation, d8_element = element

    return {
        "s5_permutation": list(
            permutation
        ),
        "d8_rotation": int(
            d8_element[0]
        ),
        "d8_flip": int(
            d8_element[1]
        ),
    }


def main():
    progress("loading source receipts")

    lift_source = json.loads(
        LIFT_SOURCE.read_text()
    )

    fiber_product_source = json.loads(
        FIBER_PRODUCT_SOURCE.read_text()
    )

    actual_group = frozenset(
        tuple(lift["permutation"])
        for row in lift_source["lift_rows"]
        for lift in row["lifts"]
    )

    reference_group = build_reference_group()

    progress(
        "actual order "
        f"{len(actual_group)}, reference order "
        f"{len(reference_group)}"
    )

    actual_generators = (
        greedy_permutation_generators(
            actual_group
        )
    )

    actual_generator_orders = tuple(
        permutation_order(generator)
        for generator in actual_generators
    )

    progress(
        "actual generator orders "
        f"{list(actual_generator_orders)}"
    )

    reference_order_cache = {
        element: reference_order(element)
        for element in reference_group
    }

    candidate_sets = [
        tuple(
            element
            for element in reference_group
            if reference_order_cache[element]
            == target_order
        )
        for target_order in actual_generator_orders
    ]

    progress(
        "reference candidate counts "
        f"{[len(candidates) for candidates in candidate_sets]}"
    )

    actual_pair_signatures = {
        (left_index, right_index):
        pair_signature_actual(
            actual_generators[left_index],
            actual_generators[right_index],
        )
        for left_index in range(
            len(actual_generators)
        )
        for right_index in range(left_index)
    }

    tested_complete_tuples = 0
    partial_assignment_count = 0
    found_mapping = None
    found_reference_generators = None

    def search(position, selected):
        nonlocal tested_complete_tuples
        nonlocal partial_assignment_count
        nonlocal found_mapping
        nonlocal found_reference_generators

        if found_mapping is not None:
            return

        if position == len(
            actual_generators
        ):
            tested_complete_tuples += 1

            if (
                tested_complete_tuples <= 10
                or tested_complete_tuples
                % 1000 == 0
            ):
                progress(
                    "testing complete generator tuple "
                    f"{tested_complete_tuples}"
                )

            mapping = extend_generator_assignment(
                actual_generators,
                tuple(selected),
                actual_group,
                reference_group,
            )

            if mapping is not None:
                found_mapping = mapping
                found_reference_generators = (
                    tuple(selected)
                )

            return

        for candidate in candidate_sets[
            position
        ]:
            if candidate in selected:
                continue

            compatible = True

            for earlier_index, earlier in enumerate(
                selected
            ):
                actual_signature = (
                    actual_pair_signatures[
                        (
                            position,
                            earlier_index,
                        )
                    ]
                )

                reference_signature = (
                    pair_signature_reference(
                        candidate,
                        earlier,
                    )
                )

                if (
                    actual_signature
                    != reference_signature
                ):
                    compatible = False
                    break

            if not compatible:
                continue

            partial_assignment_count += 1

            if (
                partial_assignment_count
                % 10000 == 0
            ):
                progress(
                    "compatible partial assignments "
                    f"{partial_assignment_count}"
                )

            search(
                position + 1,
                selected + [candidate],
            )

            if found_mapping is not None:
                return

    progress(
        "searching for compatible reference generator images"
    )

    search(0, [])

    if found_mapping is None:
        raise RuntimeError(
            "no generator-level isomorphism found"
        )

    progress(
        "explicit 480-element bijection found"
    )

    mapping_rows = []

    for index, actual_element in enumerate(
        sorted(actual_group)
    ):
        reference_element = found_mapping[
            actual_element
        ]

        mapping_rows.append({
            "actual_index": index,
            "actual_permutation": list(
                actual_element
            ),
            "reference_element": (
                encode_reference(
                    reference_element
                )
            ),
            "actual_order": (
                permutation_order(
                    actual_element
                )
            ),
            "reference_order": (
                reference_order_cache[
                    reference_element
                ]
            ),
        })

    progress(
        "verifying homomorphism on all "
        f"{len(actual_group) ** 2} ordered products"
    )

    homomorphism_failure_count = 0
    product_check_count = 0

    actual_elements = tuple(
        sorted(actual_group)
    )

    for left_position, left in enumerate(
        actual_elements,
        start=1,
    ):
        for right in actual_elements:
            product_check_count += 1

            actual_product = (
                permutation_compose(
                    left,
                    right,
                )
            )

            reference_product = (
                reference_multiply(
                    found_mapping[left],
                    found_mapping[right],
                )
            )

            if (
                found_mapping[actual_product]
                != reference_product
            ):
                homomorphism_failure_count += 1

        if (
            left_position % 60 == 0
            or left_position
            == len(actual_elements)
        ):
            progress(
                "product verification "
                f"{left_position}/"
                f"{len(actual_elements)} rows"
            )

    mapping_digest_input = json.dumps(
        mapping_rows,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    mapping_sha256 = hashlib.sha256(
        mapping_digest_input
    ).hexdigest()

    actual_generator_rows = []

    for index, (
        actual_generator,
        reference_generator,
    ) in enumerate(
        zip(
            actual_generators,
            found_reference_generators,
        )
    ):
        actual_generator_rows.append({
            "generator_index": index,
            "actual_permutation": list(
                actual_generator
            ),
            "actual_order": (
                permutation_order(
                    actual_generator
                )
            ),
            "reference_element": (
                encode_reference(
                    reference_generator
                )
            ),
            "reference_order": (
                reference_order_cache[
                    reference_generator
                ]
            ),
        })

    checks = {
        "lift_source_audit_pass": (
            lift_source["audit_pass"]
        ),
        "fiber_product_source_audit_pass": (
            fiber_product_source[
                "audit_pass"
            ]
        ),
        "actual_group_order_is_480": (
            len(actual_group) == 480
        ),
        "reference_group_order_is_480": (
            len(reference_group) == 480
        ),
        "generator_assignment_found": (
            found_mapping is not None
        ),
        "mapping_has_480_actual_elements": (
            len(found_mapping) == 480
        ),
        "mapping_has_480_distinct_reference_elements": (
            len(
                set(
                    found_mapping.values()
                )
            )
            == 480
        ),
        "all_element_orders_preserved": all(
            row["actual_order"]
            == row["reference_order"]
            for row in mapping_rows
        ),
        "all_ordered_products_checked": (
            product_check_count
            == 480 * 480
        ),
        "homomorphism_failure_count_is_zero": (
            homomorphism_failure_count
            == 0
        ),
        "actual_generators_generate_full_group": (
            permutation_closure(
                actual_generators
            )
            == actual_group
        ),
    }

    payload = {
        "certificate_id": (
            "native_g60_fiber_product_isomorphism_044"
        ),
        "lift_source": str(
            LIFT_SOURCE.relative_to(ROOT)
        ),
        "fiber_product_source": str(
            FIBER_PRODUCT_SOURCE.relative_to(
                ROOT
            )
        ),
        "runtime_seconds": round(
            time.monotonic() - START,
            6,
        ),
        "actual_group_order": len(
            actual_group
        ),
        "reference_group_order": len(
            reference_group
        ),
        "reference_group_definition": {
            "name": (
                "S5_fiber_product_D8_over_C2"
            ),
            "set": (
                "{(s,(r,f)) in S5 x D8 : "
                "sgn(s) = r mod 2}"
            ),
            "d8_multiplication": (
                "(r,f)(u,g) = "
                "(r + (-1)^f u mod 4, "
                "f + g mod 2)"
            ),
            "character": (
                "chi(r,f) = r mod 2"
            ),
            "character_kernel_type": (
                "V4"
            ),
        },
        "actual_generator_count": len(
            actual_generators
        ),
        "actual_generator_orders": list(
            actual_generator_orders
        ),
        "reference_candidate_counts": [
            len(candidates)
            for candidates in candidate_sets
        ],
        "compatible_partial_assignment_count": (
            partial_assignment_count
        ),
        "complete_generator_tuple_test_count": (
            tested_complete_tuples
        ),
        "generator_correspondence": (
            actual_generator_rows
        ),
        "mapping_row_count": len(
            mapping_rows
        ),
        "mapping_sha256": (
            mapping_sha256
        ),
        "mapping_rows": mapping_rows,
        "ordered_product_check_count": (
            product_check_count
        ),
        "homomorphism_failure_count": (
            homomorphism_failure_count
        ),
        "isomorphism_statement": (
            "The exported bijection sends the listed "
            "generators of the native 60-vertex permutation "
            "group Aut(G60) to the listed generators of "
            "{(s,d) in S5 x D8 : sgn(s)=chi(d)}, with "
            "chi(r,f)=r mod 2. Extension by group words "
            "produces a bijection on all 480 elements, and "
            "all 230400 ordered products are preserved."
        ),
        "classification_result": (
            "Aut(G60) is explicitly isomorphic, at the "
            "generator and multiplication-table level, to "
            "the S5-D8 fiber product over C2 using a "
            "V4-kernel character of D8."
        ),
        "checks": checks,
        "audit_pass": all(
            checks.values()
        ),
        "boundary": {
            "explicit_generator_correspondence_exported": True,
            "explicit_480_element_bijection_exported": True,
            "all_ordered_products_verified": True,
            "abstract_fiber_product_isomorphism_complete": True,
            "permutation_action_interpretation_open": True,
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
        payload["actual_group_order"],
    )
    print(
        "reference_group_order:",
        payload[
            "reference_group_order"
        ],
    )
    print(
        "actual_generator_count:",
        payload[
            "actual_generator_count"
        ],
    )
    print(
        "actual_generator_orders:",
        payload[
            "actual_generator_orders"
        ],
    )
    print(
        "reference_candidate_counts:",
        payload[
            "reference_candidate_counts"
        ],
    )
    print(
        "compatible_partial_assignment_count:",
        payload[
            "compatible_partial_assignment_count"
        ],
    )
    print(
        "complete_generator_tuple_test_count:",
        payload[
            "complete_generator_tuple_test_count"
        ],
    )
    print(
        "mapping_row_count:",
        payload["mapping_row_count"],
    )
    print(
        "mapping_sha256:",
        payload["mapping_sha256"],
    )
    print(
        "ordered_product_check_count:",
        payload[
            "ordered_product_check_count"
        ],
    )
    print(
        "homomorphism_failure_count:",
        payload[
            "homomorphism_failure_count"
        ],
    )

    print()
    print("generator correspondence:")

    for row in actual_generator_rows:
        print(
            " generator",
            row["generator_index"],
            "order",
            row["actual_order"],
            "->",
            row["reference_element"],
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
