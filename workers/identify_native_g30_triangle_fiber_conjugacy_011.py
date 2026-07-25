#!/usr/bin/env python3
"""Identify the conjugacy between paired triangle local actions."""

import json
from itertools import permutations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_triangle_fiber_local_action_010.json"
)

STABILIZER_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_triangle_stabilizers_009.json"
)

OUTPUT = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_triangle_fiber_conjugacy_011.json"
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


def conjugate(permutation, relabeling):
    return compose(
        compose(
            relabeling,
            permutation,
        ),
        inverse(relabeling),
    )


def local_action(element, ordered_vertices):
    vertex_to_local = {
        vertex: index
        for index, vertex in enumerate(ordered_vertices)
    }

    return tuple(
        vertex_to_local[element[vertex]]
        for vertex in ordered_vertices
    )


def main():
    source = json.loads(SOURCE.read_text())
    stabilizer_source = json.loads(
        STABILIZER_SOURCE.read_text()
    )

    first_triangle = tuple(
        source["representative_triangle"]
    )

    second_triangle = tuple(
        source["paired_triangle"]
    )

    fiber_vertices = tuple(
        source["triangle_fiber_vertices"]
    )

    full_stabilizer = frozenset(
        tuple(element)
        for element in stabilizer_source[
            "full_triangle_stabilizer"
        ]["elements"]
    )

    first_actions = {
        element: local_action(
            element,
            first_triangle,
        )
        for element in full_stabilizer
    }

    second_actions = {
        element: local_action(
            element,
            second_triangle,
        )
        for element in full_stabilizer
    }

    first_kernel = frozenset(
        element
        for element in full_stabilizer
        if first_actions[element] == (0, 1, 2)
    )

    second_kernel = frozenset(
        element
        for element in full_stabilizer
        if second_actions[element] == (0, 1, 2)
    )

    fiber_kernel = frozenset(
        element
        for element in full_stabilizer
        if all(
            element[vertex] == vertex
            for vertex in fiber_vertices
        )
    )

    conjugating_relabelings = []

    for relabeling in permutations(range(3)):
        relabeling = tuple(relabeling)

        if all(
            conjugate(
                first_actions[element],
                relabeling,
            )
            == second_actions[element]
            for element in full_stabilizer
        ):
            conjugating_relabelings.append(
                relabeling
            )

    conjugating_relabelings = tuple(
        sorted(conjugating_relabelings)
    )

    selected_relabeling = (
        conjugating_relabelings[0]
        if conjugating_relabelings
        else None
    )

    paired_vertex_bijection = (
        {
            str(first_triangle[index]):
            second_triangle[selected_relabeling[index]]
            for index in range(3)
        }
        if selected_relabeling is not None
        else {}
    )

    first_image = frozenset(
        first_actions.values()
    )

    second_image = frozenset(
        second_actions.values()
    )

    checks = {
        "source_stabilizer_audit_pass": (
            stabilizer_source["audit_pass"]
        ),
        "full_stabilizer_order_is_12": (
            len(full_stabilizer) == 12
        ),
        "first_local_image_is_s3": (
            len(first_image) == 6
        ),
        "second_local_image_is_s3": (
            len(second_image) == 6
        ),
        "first_kernel_order_is_2": (
            len(first_kernel) == 2
        ),
        "second_kernel_order_is_2": (
            len(second_kernel) == 2
        ),
        "first_and_second_kernels_are_equal": (
            first_kernel == second_kernel
        ),
        "fiber_kernel_order_is_2": (
            len(fiber_kernel) == 2
        ),
        "fiber_kernel_equals_triangle_kernels": (
            fiber_kernel
            == first_kernel
            == second_kernel
        ),
        "conjugating_relabeling_exists": (
            len(conjugating_relabelings) > 0
        ),
        "conjugating_relabeling_is_unique": (
            len(conjugating_relabelings) == 1
        ),
        "paired_vertex_bijection_has_three_rows": (
            len(paired_vertex_bijection) == 3
        ),
    }

    payload = {
        "certificate_id": (
            "native_g30_triangle_fiber_conjugacy_011"
        ),
        "source": str(
            SOURCE.relative_to(ROOT)
        ),
        "stabilizer_source": str(
            STABILIZER_SOURCE.relative_to(ROOT)
        ),
        "first_triangle": list(first_triangle),
        "second_triangle": list(second_triangle),
        "full_stabilizer_order": len(
            full_stabilizer
        ),
        "first_local_image_order": len(
            first_image
        ),
        "second_local_image_order": len(
            second_image
        ),
        "first_kernel_order": len(
            first_kernel
        ),
        "second_kernel_order": len(
            second_kernel
        ),
        "fiber_kernel_order": len(
            fiber_kernel
        ),
        "conjugating_relabeling_count": len(
            conjugating_relabelings
        ),
        "conjugating_relabelings": [
            list(relabeling)
            for relabeling in conjugating_relabelings
        ],
        "selected_conjugating_relabeling": (
            list(selected_relabeling)
            if selected_relabeling is not None
            else None
        ),
        "paired_vertex_bijection": (
            paired_vertex_bijection
        ),
        "conjugacy_result": (
            "The two triangle actions factor through the same "
            "S3 quotient and are conjugate by a unique vertex "
            "bijection. Their common order-2 kernel fixes all "
            "six vertices of the triangle fiber pointwise."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "paired_triangle_action_conjugacy_derived": True,
            "common_pointwise_kernel_derived": True,
            "kernel_action_outside_triangle_fiber_open": True,
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
        "first_local_image_order:",
        payload["first_local_image_order"],
    )
    print(
        "second_local_image_order:",
        payload["second_local_image_order"],
    )
    print(
        "fiber_kernel_order:",
        payload["fiber_kernel_order"],
    )
    print(
        "conjugating_relabeling_count:",
        payload["conjugating_relabeling_count"],
    )
    print(
        "selected_conjugating_relabeling:",
        payload["selected_conjugating_relabeling"],
    )
    print(
        "paired_vertex_bijection:",
        payload["paired_vertex_bijection"],
    )
    print(
        "conjugacy_result:",
        payload["conjugacy_result"],
    )


if __name__ == "__main__":
    main()
