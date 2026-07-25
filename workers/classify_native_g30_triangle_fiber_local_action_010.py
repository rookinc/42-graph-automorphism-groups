#!/usr/bin/env python3
"""Classify the local action on a native G30 triangle fiber."""

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ANATOMY_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_group_anatomy_002.json"
)

TRIANGLE_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_triangle_action_006.json"
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
    / "native_g30_triangle_fiber_local_action_010.json"
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


def image_of_subset(subset, permutation):
    return tuple(sorted(
        permutation[vertex]
        for vertex in subset
    ))


def restricted_action(element, ordered_vertices):
    vertex_to_local = {
        vertex: index
        for index, vertex in enumerate(ordered_vertices)
    }

    return tuple(
        vertex_to_local[element[vertex]]
        for vertex in ordered_vertices
    )


def local_kernel(group, ordered_vertices):
    return frozenset(
        element
        for element in group
        if all(
            element[vertex] == vertex
            for vertex in ordered_vertices
        )
    )


def main():
    anatomy_source = json.loads(ANATOMY_SOURCE.read_text())
    triangle_source = json.loads(TRIANGLE_SOURCE.read_text())
    stabilizer_source = json.loads(
        STABILIZER_SOURCE.read_text()
    )

    representative = tuple(
        stabilizer_source["representative_triangle"]
    )

    central_involution = next(
        tuple(element)
        for element in anatomy_source["center"]
        if tuple(element)
        != tuple(range(len(element)))
    )

    partner = image_of_subset(
        representative,
        central_involution,
    )

    fiber_vertices = tuple(
        representative + partner
    )

    full_stabilizer = frozenset(
        tuple(element)
        for element in stabilizer_source[
            "full_triangle_stabilizer"
        ]["elements"]
    )

    c4_stabilizer = frozenset(
        tuple(element)
        for element in stabilizer_source[
            "c4_complement_triangle_stabilizer"
        ]["elements"]
    )

    fiber_setwise_stabilizer = frozenset(
        element
        for element in full_stabilizer
        if {
            image_of_subset(representative, element),
            image_of_subset(partner, element),
        }
        == {
            representative,
            partner,
        }
    )

    representative_setwise_stabilizer = frozenset(
        element
        for element in fiber_setwise_stabilizer
        if image_of_subset(
            representative,
            element,
        )
        == representative
    )

    partner_setwise_stabilizer = frozenset(
        element
        for element in fiber_setwise_stabilizer
        if image_of_subset(
            partner,
            element,
        )
        == partner
    )

    sheet_swappers = frozenset(
        element
        for element in fiber_setwise_stabilizer
        if image_of_subset(
            representative,
            element,
        )
        == partner
    )

    full_local_image = frozenset(
        restricted_action(
            element,
            fiber_vertices,
        )
        for element in fiber_setwise_stabilizer
    )

    triangle_local_image = frozenset(
        tuple(
            representative.index(element[vertex])
            for vertex in representative
        )
        for element in representative_setwise_stabilizer
    )

    synchronized_rows = []

    for element in representative_setwise_stabilizer:
        action_on_first = tuple(
            representative.index(element[vertex])
            for vertex in representative
        )

        action_on_second = tuple(
            partner.index(element[vertex])
            for vertex in partner
        )

        synchronized_rows.append({
            "element": list(element),
            "first_triangle_action": list(
                action_on_first
            ),
            "second_triangle_action": list(
                action_on_second
            ),
            "actions_match": (
                action_on_first == action_on_second
            ),
        })

    full_kernel = local_kernel(
        fiber_setwise_stabilizer,
        fiber_vertices,
    )

    triangle_kernel = frozenset(
        element
        for element in representative_setwise_stabilizer
        if all(
            element[vertex] == vertex
            for vertex in representative
        )
    )

    sheet_swap_order_profile = Counter(
        permutation_order(element)
        for element in sheet_swappers
    )

    checks = {
        "source_triangle_audit_pass": (
            triangle_source["audit_pass"]
        ),
        "source_stabilizer_audit_pass": (
            stabilizer_source["audit_pass"]
        ),
        "representative_and_partner_are_disjoint": (
            set(representative).isdisjoint(partner)
        ),
        "fiber_has_six_vertices": (
            len(set(fiber_vertices)) == 6
        ),
        "full_triangle_stabilizer_order_is_12": (
            len(full_stabilizer) == 12
        ),
        "full_triangle_stabilizer_preserves_fiber": (
            fiber_setwise_stabilizer
            == full_stabilizer
        ),
        "representative_setwise_stabilizer_order_is_12": (
            len(representative_setwise_stabilizer) == 12
        ),
        "partner_setwise_stabilizer_order_is_12": (
            len(partner_setwise_stabilizer) == 12
        ),
        "no_element_of_triangle_stabilizer_swaps_sheets": (
            len(sheet_swappers) == 0
        ),
        "local_action_on_one_triangle_is_full_s3": (
            len(triangle_local_image) == 6
        ),
        "triangle_pointwise_kernel_order_is_2": (
            len(triangle_kernel) == 2
        ),
        "local_action_on_six_vertices_is_faithful": (
            len(full_kernel) == 1
        ),
        "local_image_order_is_12": (
            len(full_local_image) == 12
        ),
        "actions_on_paired_triangles_are_synchronized": all(
            row["actions_match"]
            for row in synchronized_rows
        ),
        "c4_s3_stabilizer_is_triangle_action_complement": (
            len(c4_stabilizer) == 6
            and len({
                tuple(
                    representative.index(
                        element[vertex]
                    )
                    for vertex in representative
                )
                for element in c4_stabilizer
            })
            == 6
        ),
    }

    payload = {
        "certificate_id": (
            "native_g30_triangle_fiber_local_action_010"
        ),
        "anatomy_source": str(
            ANATOMY_SOURCE.relative_to(ROOT)
        ),
        "triangle_source": str(
            TRIANGLE_SOURCE.relative_to(ROOT)
        ),
        "stabilizer_source": str(
            STABILIZER_SOURCE.relative_to(ROOT)
        ),
        "representative_triangle": list(representative),
        "paired_triangle": list(partner),
        "triangle_fiber_vertices": list(fiber_vertices),
        "fiber_setwise_stabilizer_order": len(
            fiber_setwise_stabilizer
        ),
        "representative_setwise_stabilizer_order": len(
            representative_setwise_stabilizer
        ),
        "partner_setwise_stabilizer_order": len(
            partner_setwise_stabilizer
        ),
        "sheet_swap_count_inside_triangle_stabilizer": len(
            sheet_swappers
        ),
        "sheet_swap_order_profile": {
            str(order): count
            for order, count in sorted(
                sheet_swap_order_profile.items()
            )
        },
        "triangle_local_image_order": len(
            triangle_local_image
        ),
        "triangle_pointwise_kernel_order": len(
            triangle_kernel
        ),
        "six_vertex_local_image_order": len(
            full_local_image
        ),
        "six_vertex_local_kernel_order": len(
            full_kernel
        ),
        "paired_triangle_actions_synchronized": all(
            row["actions_match"]
            for row in synchronized_rows
        ),
        "synchronized_action_rows": synchronized_rows,
        "local_action_result": (
            "The S3 x C2 triangle stabilizer preserves each "
            "lifted triangle separately. Its S3 quotient acts "
            "faithfully and synchronously on both three-vertex "
            "triangles, while its central kernel of order 2 "
            "fixes the first triangle pointwise and acts "
            "nontrivially on the paired triangle."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "six_vertex_triangle_fiber_action_classified": True,
            "triangle_local_s3_action_derived": True,
            "sheet_exchange_inside_triangle_stabilizer": False,
            "kernel_action_on_partner_requires_explicit_label": True,
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
        "representative_triangle:",
        payload["representative_triangle"],
    )
    print(
        "paired_triangle:",
        payload["paired_triangle"],
    )
    print(
        "fiber_setwise_stabilizer_order:",
        payload["fiber_setwise_stabilizer_order"],
    )
    print(
        "sheet_swap_count_inside_triangle_stabilizer:",
        payload[
            "sheet_swap_count_inside_triangle_stabilizer"
        ],
    )
    print(
        "triangle_local_image_order:",
        payload["triangle_local_image_order"],
    )
    print(
        "triangle_pointwise_kernel_order:",
        payload[
            "triangle_pointwise_kernel_order"
        ],
    )
    print(
        "six_vertex_local_image_order:",
        payload["six_vertex_local_image_order"],
    )
    print(
        "paired_triangle_actions_synchronized:",
        payload[
            "paired_triangle_actions_synchronized"
        ],
    )
    print(
        "local_action_result:",
        payload["local_action_result"],
    )


if __name__ == "__main__":
    main()
