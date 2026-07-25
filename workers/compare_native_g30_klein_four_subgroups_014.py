#!/usr/bin/env python3
"""Compare the local triangle Klein four with V4_mixed."""

import json
from collections import Counter, deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ACTION_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_full_automorphism_action_001.json"
)

ANATOMY_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_group_anatomy_002.json"
)

COMPLEMENT_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_s5_complement_classification_004.json"
)

PARITY_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_stabilizer_parity_classification_005.json"
)

KERNEL_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_triangle_kernel_involution_012.json"
)

LOCAL_V4_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_local_klein_four_013.json"
)

OUTPUT = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_klein_four_comparison_014.json"
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


def conjugate(element, carrier):
    return compose(
        compose(carrier, element),
        inverse(carrier),
    )


def conjugate_subgroup(subgroup, carrier):
    return frozenset(
        conjugate(element, carrier)
        for element in subgroup
    )


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


def permutation_order(permutation):
    identity = tuple(range(len(permutation)))
    current = identity
    order = 0

    while True:
        order += 1
        current = compose(permutation, current)

        if current == identity:
            return order


def fixed_point_count(permutation):
    return sum(
        1
        for vertex, image in enumerate(permutation)
        if vertex == image
    )


def subgroup_profile(subgroup):
    return {
        "order": len(subgroup),
        "element_order_profile": {
            str(order): count
            for order, count in sorted(
                Counter(
                    permutation_order(element)
                    for element in subgroup
                ).items()
            )
        },
        "fixed_point_count_profile": {
            str(count): multiplicity
            for count, multiplicity in sorted(
                Counter(
                    fixed_point_count(element)
                    for element in subgroup
                    if permutation_order(element) == 2
                ).items()
            )
        },
        "elements": [
            list(element)
            for element in sorted(subgroup)
        ],
    }


def main():
    action_source = json.loads(ACTION_SOURCE.read_text())
    anatomy_source = json.loads(ANATOMY_SOURCE.read_text())
    complement_source = json.loads(
        COMPLEMENT_SOURCE.read_text()
    )
    parity_source = json.loads(PARITY_SOURCE.read_text())
    kernel_source = json.loads(KERNEL_SOURCE.read_text())
    local_v4_source = json.loads(
        LOCAL_V4_SOURCE.read_text()
    )

    full_group = frozenset(
        tuple(row["permutation"])
        for row in action_source["automorphisms"]
    )

    degree = action_source["vertex_count"]
    identity = tuple(range(degree))

    center = frozenset(
        tuple(element)
        for element in anatomy_source["center"]
    )

    central_deck = next(
        element
        for element in center
        if element != identity
    )

    triangle_kernel = tuple(
        kernel_source["kernel_involution"]
    )

    local_klein_four = frozenset({
        identity,
        central_deck,
        triangle_kernel,
        compose(central_deck, triangle_kernel),
    })

    v4_complement_index = next(
        row["complement_index"]
        for row in parity_source["complement_stabilizers"]
        if row["refined_stabilizer_type"] == "V4_mixed"
    )

    v4_complement_row = next(
        row
        for row in complement_source["complements"]
        if row["index"] == v4_complement_index
    )

    v4_complement = frozenset(
        tuple(element)
        for element in v4_complement_row["elements"]
    )

    vertex_stabilizer_v4 = frozenset(
        element
        for element in v4_complement
        if element[0] == 0
    )

    intersection = (
        local_klein_four.intersection(vertex_stabilizer_v4)
    )

    generated = generated_subgroup(
        tuple(local_klein_four | vertex_stabilizer_v4),
        identity,
    )

    conjugating_elements = tuple(
        element
        for element in full_group
        if conjugate_subgroup(
            local_klein_four,
            element,
        )
        == vertex_stabilizer_v4
    )

    reverse_conjugating_elements = tuple(
        element
        for element in full_group
        if conjugate_subgroup(
            vertex_stabilizer_v4,
            element,
        )
        == local_klein_four
    )

    local_nonidentity = (
        local_klein_four.difference({identity})
    )

    vertex_nonidentity = (
        vertex_stabilizer_v4.difference({identity})
    )

    local_fixed_profile = Counter(
        fixed_point_count(element)
        for element in local_nonidentity
    )

    vertex_fixed_profile = Counter(
        fixed_point_count(element)
        for element in vertex_nonidentity
    )

    local_contains_center = (
        central_deck in local_klein_four
    )

    vertex_v4_contains_center = (
        central_deck in vertex_stabilizer_v4
    )

    checks = {
        "source_action_audit_pass": (
            action_source["audit_pass"]
        ),
        "source_anatomy_audit_pass": (
            anatomy_source["audit_pass"]
        ),
        "source_complement_audit_pass": (
            complement_source["audit_pass"]
        ),
        "source_parity_audit_pass": (
            parity_source["audit_pass"]
        ),
        "source_kernel_audit_pass": (
            kernel_source["audit_pass"]
        ),
        "source_local_v4_audit_pass": (
            local_v4_source["audit_pass"]
        ),
        "local_klein_four_order_is_4": (
            len(local_klein_four) == 4
        ),
        "vertex_stabilizer_v4_order_is_4": (
            len(vertex_stabilizer_v4) == 4
        ),
        "local_klein_four_contains_center": (
            local_contains_center
        ),
        "vertex_stabilizer_v4_excludes_center": (
            not vertex_v4_contains_center
        ),
        "subgroups_are_not_equal": (
            local_klein_four != vertex_stabilizer_v4
        ),
        "intersection_order_is_2": (
            len(intersection) == 2
        ),
        "intersection_is_generated_by_triangle_kernel": (
            intersection == {
                identity,
                triangle_kernel,
            }
        ),
        "generated_subgroup_order_is_8": (
            len(generated) == 8
        ),
        "subgroups_are_not_conjugate_in_full_group": (
            len(conjugating_elements) == 0
            and len(reverse_conjugating_elements) == 0
        ),
        "fixed_point_profiles_are_distinct": (
            local_fixed_profile != vertex_fixed_profile
        ),
    }

    payload = {
        "certificate_id": (
            "native_g30_klein_four_comparison_014"
        ),
        "action_source": str(
            ACTION_SOURCE.relative_to(ROOT)
        ),
        "anatomy_source": str(
            ANATOMY_SOURCE.relative_to(ROOT)
        ),
        "complement_source": str(
            COMPLEMENT_SOURCE.relative_to(ROOT)
        ),
        "parity_source": str(
            PARITY_SOURCE.relative_to(ROOT)
        ),
        "kernel_source": str(
            KERNEL_SOURCE.relative_to(ROOT)
        ),
        "local_v4_source": str(
            LOCAL_V4_SOURCE.relative_to(ROOT)
        ),
        "local_triangle_klein_four": subgroup_profile(
            local_klein_four
        ),
        "vertex_stabilizer_v4_mixed": subgroup_profile(
            vertex_stabilizer_v4
        ),
        "intersection_order": len(intersection),
        "intersection": [
            list(element)
            for element in sorted(intersection)
        ],
        "generated_subgroup_order": len(generated),
        "generated_subgroup_profile": subgroup_profile(
            generated
        ),
        "local_contains_central_deck": (
            local_contains_center
        ),
        "vertex_v4_contains_central_deck": (
            vertex_v4_contains_center
        ),
        "conjugating_element_count": len(
            conjugating_elements
        ),
        "reverse_conjugating_element_count": len(
            reverse_conjugating_elements
        ),
        "comparison_result": (
            "The triangle-local Klein four and the "
            "V4_mixed vertex stabilizer are distinct and are "
            "not conjugate in the full automorphism group. "
            "Their intersection is the order-2 subgroup "
            "generated by the triangle-kernel involution. The "
            "local Klein four contains the central deck "
            "involution, whereas the vertex stabilizer lies "
            "entirely in the S5 complement. Together they "
            "generate a subgroup of order 8."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "two_klein_four_subgroups_compared": True,
            "equality_decided": True,
            "intersection_decided": True,
            "full_group_conjugacy_decided": True,
            "shared_triangle_kernel_identified": True,
            "generated_order_8_group_not_yet_identified": True,
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
        "local_klein_four_order:",
        payload[
            "local_triangle_klein_four"
        ]["order"],
    )
    print(
        "vertex_stabilizer_v4_order:",
        payload[
            "vertex_stabilizer_v4_mixed"
        ]["order"],
    )
    print(
        "intersection_order:",
        payload["intersection_order"],
    )
    print(
        "generated_subgroup_order:",
        payload["generated_subgroup_order"],
    )
    print(
        "local_fixed_profile:",
        payload[
            "local_triangle_klein_four"
        ]["fixed_point_count_profile"],
    )
    print(
        "vertex_v4_fixed_profile:",
        payload[
            "vertex_stabilizer_v4_mixed"
        ]["fixed_point_count_profile"],
    )
    print(
        "conjugating_element_count:",
        payload["conjugating_element_count"],
    )
    print(
        "comparison_result:",
        payload["comparison_result"],
    )


if __name__ == "__main__":
    main()
