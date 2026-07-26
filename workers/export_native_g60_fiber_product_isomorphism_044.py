#!/usr/bin/env python3
"""Export an explicit isomorphism from Aut(G60) to the S5-D8 fiber product."""

import hashlib
import itertools
import json
import math
import sys
import time
from collections import deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

FULL_SOURCE = (
    ROOT / "artifacts/json/"
    "native_g60_full_automorphism_group_042.json"
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

    raise RuntimeError("permutation order exceeded bound")


def closure(generators):
    generators = tuple(generators)

    expanded = tuple(dict.fromkeys(
        generators
        + tuple(inverse(generator) for generator in generators)
    ))

    unit = identity(len(generators[0]))
    subgroup = {unit}
    frontier = [unit]

    while frontier:
        current = frontier.pop()

        for generator in expanded:
            product = compose(generator, current)

            if product not in subgroup:
                subgroup.add(product)
                frontier.append(product)

    return frozenset(subgroup)


def greedy_generators(group):
    group = frozenset(group)
    unit = identity(len(next(iter(group))))
    generators = []
    generated = frozenset({unit})

    for candidate in sorted(group):
        if candidate in generated:
            continue

        generators.append(candidate)
        generated = closure(generators)

        if generated == group:
            break

    return tuple(generators)


def power(element, exponent, multiply, unit):
    result = unit

    for _ in range(exponent):
        result = multiply(element, result)

    return result


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
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(5)
        for right in range(left + 1, 5)
    )

    return inversions % 2


def s5_order(permutation):
    unit = tuple(range(5))
    current = unit

    for order in range(1, 100):
        current = s5_multiply(permutation, current)

        if current == unit:
            return order

    raise RuntimeError("S5 order exceeded bound")


def d8_multiply(left, right):
    left_rotation, left_flip = left
    right_rotation, right_flip = right

    signed_rotation = (
        right_rotation
        if left_flip == 0
        else -right_rotation
    )

    return (
        (left_rotation + signed_rotation) % 4,
        (left_flip + right_flip) % 2,
    )


def d8_inverse(element):
    for candidate in (
        (rotation, flip)
        for rotation in range(4)
        for flip in range(2)
    ):
        if (
            d8_multiply(element, candidate) == (0, 0)
            and d8_multiply(candidate, element) == (0, 0)
        ):
            return candidate

    raise RuntimeError("D8 inverse not found")


def d8_order(element):
    unit = (0, 0)
    current = unit

    for order in range(1, 20):
        current = d8_multiply(element, current)

        if current == unit:
            return order

    raise RuntimeError("D8 order exceeded bound")


def model_multiply(left, right):
    return (
        s5_multiply(left[0], right[0]),
        d8_multiply(left[1], right[1]),
    )


def model_inverse(element):
    return (
        s5_inverse(element[0]),
        d8_inverse(element[1]),
    )


def model_order(element):
    return math.lcm(
        s5_order(element[0]),
        d8_order(element[1]),
    )


def model_closure(generators):
    generators = tuple(generators)
    unit = (tuple(range(5)), (0, 0))

    expanded = tuple(dict.fromkeys(
        generators
        + tuple(model_inverse(generator) for generator in generators)
    ))

    subgroup = {unit}
    frontier = [unit]

    while frontier:
        current = frontier.pop()

        for generator in expanded:
            product = model_multiply(generator, current)

            if product not in subgroup:
                subgroup.add(product)
                frontier.append(product)

    return frozenset(subgroup)


def build_model_group():
    return frozenset(
        (permutation, (rotation, flip))
        for permutation in itertools.permutations(range(5))
        for rotation in range(4)
        for flip in range(2)
        if s5_sign(permutation) == rotation % 2
    )


def relation_signature_matches(h0, h1, h2, h3):
    model_unit = (tuple(range(5)), (0, 0))

    if [model_order(x) for x in (h0, h1, h2, h3)] != [2, 2, 4, 2]:
        return False

    if model_multiply(h0, h1) != model_multiply(h1, h0):
        return False

    if model_multiply(h1, h2) != model_multiply(h2, h1):
        return False

    if model_multiply(h0, h2) == model_multiply(h2, h0):
        return False

    if power(h2, 2, model_multiply, model_unit) != h1:
        return False

    required_orders = {
        (3, 0): 5,
        (3, 1): 6,
        (3, 2): 6,
    }

    generators = (h0, h1, h2, h3)

    for (left, right), required in required_orders.items():
        if model_order(
            model_multiply(generators[left], generators[right])
        ) != required:
            return False

    if model_order(
        model_multiply(
            model_multiply(h3, h0),
            h1,
        )
    ) != 10:
        return False

    if model_order(
        model_multiply(
            model_multiply(h3, h0),
            h2,
        )
    ) != 4:
        return False

    if model_order(
        model_multiply(
            model_multiply(h3, h1),
            h2,
        )
    ) != 6:
        return False

    if model_order(
        model_multiply(
            model_multiply(
                model_multiply(h3, h0),
                h1,
            ),
            h2,
        )
    ) != 12:
        return False

    return len(model_closure((h0, h1, h2, h3))) == 480


def find_canonical_model_generators(model_group):
    involutions = sorted(
        element
        for element in model_group
        if model_order(element) == 2
    )

    order_four = sorted(
        element
        for element in model_group
        if model_order(element) == 4
    )

    candidates = []

    for h0 in involutions:
        for h1 in involutions:
            if h1 == h0:
                continue

            if model_multiply(h0, h1) != model_multiply(h1, h0):
                continue

            if len(model_closure((h0, h1))) != 4:
                continue

            for h2 in order_four:
                if model_multiply(h1, h2) != model_multiply(h2, h1):
                    continue

                if model_multiply(h0, h2) == model_multiply(h2, h0):
                    continue

                if power(
                    h2,
                    2,
                    model_multiply,
                    (tuple(range(5)), (0, 0)),
                ) != h1:
                    continue

                if len(model_closure((h0, h1, h2))) != 8:
                    continue

                for h3 in involutions:
                    if relation_signature_matches(h0, h1, h2, h3):
                        candidates.append((h0, h1, h2, h3))

    candidates.sort()

    if not candidates:
        raise RuntimeError("no model generator tuple found")

    return candidates[0], len(candidates)


def extend_mapping(actual_generators, model_generators):
    actual_unit = identity(60)
    model_unit = (tuple(range(5)), (0, 0))

    paired = tuple(zip(actual_generators, model_generators))

    mapping = {
        actual_unit: model_unit,
    }

    reverse_mapping = {
        model_unit: actual_unit,
    }

    queue = deque([actual_unit])
    conflict_count = 0

    while queue:
        actual_element = queue.popleft()
        model_element = mapping[actual_element]

        for actual_generator, model_generator in paired:
            actual_product = compose(
                actual_generator,
                actual_element,
            )

            model_product = model_multiply(
                model_generator,
                model_element,
            )

            existing_model = mapping.get(actual_product)

            if existing_model is not None:
                if existing_model != model_product:
                    conflict_count += 1
                continue

            existing_actual = reverse_mapping.get(model_product)

            if existing_actual is not None and existing_actual != actual_product:
                conflict_count += 1
                continue

            mapping[actual_product] = model_product
            reverse_mapping[model_product] = actual_product
            queue.append(actual_product)

    return mapping, reverse_mapping, conflict_count


def serialize_model_element(element):
    return {
        "s5": list(element[0]),
        "d8": list(element[1]),
    }


def main():
    progress("loading native and fiber-product receipts")

    full_source = json.loads(FULL_SOURCE.read_text())
    fiber_source = json.loads(FIBER_PRODUCT_SOURCE.read_text())

    actual_group = frozenset(
        tuple(row)
        for row in full_source["native_automorphisms"]
    )

    actual_generators = greedy_generators(actual_group)

    progress(
        "selected deterministic native generators "
        f"count={len(actual_generators)}"
    )

    model_group = build_model_group()

    model_generators, candidate_count = (
        find_canonical_model_generators(model_group)
    )

    progress(
        "selected canonical model tuple "
        f"from {candidate_count} valid tuples"
    )

    mapping, reverse_mapping, conflict_count = extend_mapping(
        actual_generators,
        model_generators,
    )

    progress(
        "extended generator map "
        f"domain={len(mapping)} "
        f"image={len(reverse_mapping)} "
        f"conflicts={conflict_count}"
    )

    multiplication_failure_count = 0
    first_failure = None

    sorted_actual_group = tuple(sorted(actual_group))

    for left_index, left in enumerate(sorted_actual_group):
        if left_index % 60 == 0:
            progress(
                "multiplication verification "
                f"left={left_index}/480"
            )

        for right in sorted_actual_group:
            actual_product = compose(left, right)

            model_product = model_multiply(
                mapping[left],
                mapping[right],
            )

            if mapping[actual_product] != model_product:
                multiplication_failure_count += 1

                if first_failure is None:
                    first_failure = {
                        "left": list(left),
                        "right": list(right),
                        "actual_product": list(actual_product),
                        "mapped_product": serialize_model_element(
                            mapping[actual_product]
                        ),
                        "model_product": serialize_model_element(
                            model_product
                        ),
                    }

    mapping_rows = [
        {
            "native_permutation": list(actual_element),
            "model_element": serialize_model_element(
                mapping[actual_element]
            ),
        }
        for actual_element in sorted_actual_group
    ]

    canonical_payload = {
        "character_name": "rotation_parity",
        "native_generators": [
            list(generator)
            for generator in actual_generators
        ],
        "model_generators": [
            serialize_model_element(generator)
            for generator in model_generators
        ],
        "mapping_rows": mapping_rows,
    }

    canonical_bytes = json.dumps(
        canonical_payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    mapping_sha256 = hashlib.sha256(
        canonical_bytes
    ).hexdigest()

    checks = {
        "full_source_audit_pass": full_source["audit_pass"],
        "fiber_product_source_audit_pass": fiber_source["audit_pass"],
        "actual_group_order_is_480": len(actual_group) == 480,
        "model_group_order_is_480": len(model_group) == 480,
        "native_generator_count_is_4": len(actual_generators) == 4,
        "valid_model_generator_tuple_count_is_480": candidate_count == 480,
        "mapping_domain_count_is_480": len(mapping) == 480,
        "mapping_image_count_is_480": len(reverse_mapping) == 480,
        "mapping_conflict_count_is_zero": conflict_count == 0,
        "multiplication_check_count_is_230400": (
            len(actual_group) * len(actual_group) == 230400
        ),
        "multiplication_failure_count_is_zero": (
            multiplication_failure_count == 0
        ),
    }

    output = {
        "certificate_id": "native_g60_fiber_product_isomorphism_044",
        "audit_pass": all(checks.values()),
        "full_source": str(FULL_SOURCE.relative_to(ROOT)),
        "fiber_product_source": str(
            FIBER_PRODUCT_SOURCE.relative_to(ROOT)
        ),
        "character_name": "rotation_parity",
        "character_kernel_type": "V4",
        "valid_model_generator_tuple_count": candidate_count,
        "native_generator_count": len(actual_generators),
        "native_generators": [
            {
                "index": index,
                "order": permutation_order(generator),
                "permutation": list(generator),
            }
            for index, generator in enumerate(actual_generators)
        ],
        "model_generators": [
            {
                "index": index,
                "order": model_order(generator),
                **serialize_model_element(generator),
            }
            for index, generator in enumerate(model_generators)
        ],
        "mapping_count": len(mapping_rows),
        "mapping_rows": mapping_rows,
        "mapping_sha256": mapping_sha256,
        "multiplication_check_count": 230400,
        "multiplication_failure_count": multiplication_failure_count,
        "first_multiplication_failure": first_failure,
        "checks": checks,
        "classification_result": (
            "A deterministic four-generator correspondence extends to "
            "an explicit bijection from the 480 native automorphisms of "
            "G60 to the rotation-parity S5-D8 fiber product. All 230400 "
            "ordered products preserve multiplication."
        ),
        "boundary": (
            "The exported isomorphism uses one canonical coordinate "
            "choice among 480 equivalent valid model generator tuples. "
            "The abstract isomorphism type is independent of that choice."
        ),
        "runtime_seconds": round(
            time.monotonic() - START,
            6,
        ),
    }

    OUTPUT.write_text(
        json.dumps(
            output,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )

    print("OUT ==")
    print(f"output: {OUTPUT}")
    print(f"audit_pass: {output['audit_pass']}")
    print(
        "valid_model_generator_tuple_count: "
        f"{output['valid_model_generator_tuple_count']}"
    )
    print(f"mapping_count: {output['mapping_count']}")
    print(
        "multiplication_check_count: "
        f"{output['multiplication_check_count']}"
    )
    print(
        "multiplication_failure_count: "
        f"{output['multiplication_failure_count']}"
    )
    print(f"mapping_sha256: {output['mapping_sha256']}")
    print(f"runtime_seconds: {output['runtime_seconds']}")


if __name__ == "__main__":
    main()
