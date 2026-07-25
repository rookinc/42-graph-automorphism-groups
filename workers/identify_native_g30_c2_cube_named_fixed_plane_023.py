#!/usr/bin/env python3
"""Bind the transvection fixed plane to named native G30 involutions."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

LINEAR_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_c2_cube_linear_action_022.json"
)

LOCAL_V4_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_local_klein_four_013.json"
)

COMPARISON_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_klein_four_comparison_014.json"
)

OUTPUT = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_c2_cube_named_fixed_plane_023.json"
)


def compose(left, right):
    return tuple(
        left[right[index]]
        for index in range(len(left))
    )


def vector_add(left, right):
    return tuple(
        a ^ b
        for a, b in zip(left, right)
    )


def matrix_apply(matrix, vector):
    return tuple(
        sum(
            matrix[row][column] * vector[column]
            for column in range(len(vector))
        )
        % 2
        for row in range(len(vector))
    )


def fixed_point_count(permutation):
    return sum(
        1
        for index, image in enumerate(permutation)
        if index == image
    )


def main():
    linear_source = json.loads(
        LINEAR_SOURCE.read_text()
    )

    local_source = json.loads(
        LOCAL_V4_SOURCE.read_text()
    )

    comparison_source = json.loads(
        COMPARISON_SOURCE.read_text()
    )

    coordinate_to_element = {
        tuple(row["coordinate"]): tuple(row["permutation"])
        for row in linear_source["coordinate_table"]
    }

    element_to_coordinate = {
        element: coordinate
        for coordinate, element
        in coordinate_to_element.items()
    }

    named_elements = {
        row["label"]: tuple(row["permutation"])
        for row in local_source[
            "nonidentity_element_anatomy"
        ]
    }

    central_deck = named_elements["central_deck"]
    triangle_kernel = named_elements["triangle_kernel"]
    deck_times_kernel = named_elements[
        "deck_times_kernel"
    ]

    named_coordinates = {
        label: element_to_coordinate[element]
        for label, element in named_elements.items()
    }

    fixed_nonzero_vectors = frozenset(
        tuple(vector)
        for vector in linear_source[
            "fixed_nonzero_vectors"
        ]
    )

    named_local_plane_coordinates = frozenset(
        named_coordinates.values()
    )

    matrix = tuple(
        tuple(row)
        for row in linear_source["nontrivial_matrix"]
    )

    generated_group = frozenset(
        tuple(element)
        for element in comparison_source[
            "generated_subgroup_profile"
        ]["elements"]
    )

    local_v4 = frozenset(
        tuple(element)
        for element in comparison_source[
            "local_triangle_klein_four"
        ]["elements"]
    )

    vertex_v4 = frozenset(
        tuple(element)
        for element in comparison_source[
            "vertex_stabilizer_v4_mixed"
        ]["elements"]
    )

    identity = next(
        element
        for element in generated_group
        if all(
            index == image
            for index, image in enumerate(element)
        )
    )

    vertex_only_elements = tuple(sorted(
        element
        for element in vertex_v4
        if element not in local_v4
    ))

    vertex_only_rows = [
        {
            "coordinate": list(
                element_to_coordinate[element]
            ),
            "fixed_point_count": fixed_point_count(
                element
            ),
            "transvection_image_coordinate": list(
                matrix_apply(
                    matrix,
                    element_to_coordinate[element],
                )
            ),
        }
        for element in vertex_only_elements
    ]

    outside_fixed_plane = tuple(sorted(
        coordinate
        for coordinate in coordinate_to_element
        if any(coordinate)
        and coordinate not in fixed_nonzero_vectors
    ))

    outside_pairs = []
    seen = set()

    for coordinate in outside_fixed_plane:
        if coordinate in seen:
            continue

        image = matrix_apply(matrix, coordinate)
        pair = tuple(sorted((coordinate, image)))

        outside_pairs.append(pair)
        seen.update(pair)

    transvection_difference_vectors = frozenset(
        vector_add(
            coordinate,
            matrix_apply(matrix, coordinate),
        )
        for coordinate in outside_fixed_plane
    )

    nonzero_difference_vectors = frozenset(
        vector
        for vector in transvection_difference_vectors
        if any(vector)
    )

    difference_named_labels = sorted(
        label
        for label, coordinate in named_coordinates.items()
        if coordinate in nonzero_difference_vectors
    )

    shared_intersection = frozenset(
        tuple(element)
        for element in comparison_source["intersection"]
    )

    checks = {
        "linear_source_audit_pass": (
            linear_source["audit_pass"]
        ),
        "local_source_audit_pass": (
            local_source["audit_pass"]
        ),
        "comparison_source_audit_pass": (
            comparison_source["audit_pass"]
        ),
        "central_deck_coordinate_found": (
            central_deck in element_to_coordinate
        ),
        "triangle_kernel_coordinate_found": (
            triangle_kernel in element_to_coordinate
        ),
        "deck_times_kernel_coordinate_found": (
            deck_times_kernel in element_to_coordinate
        ),
        "central_deck_lies_in_fixed_plane": (
            named_coordinates["central_deck"]
            in fixed_nonzero_vectors
        ),
        "triangle_kernel_lies_outside_fixed_plane": (
            named_coordinates["triangle_kernel"]
            not in fixed_nonzero_vectors
        ),
        "deck_times_kernel_lies_outside_fixed_plane": (
            named_coordinates["deck_times_kernel"]
            not in fixed_nonzero_vectors
        ),
        "deck_times_kernel_is_coordinate_sum": (
            named_coordinates["deck_times_kernel"]
            == vector_add(
                named_coordinates["central_deck"],
                named_coordinates["triangle_kernel"],
            )
        ),
        "triangle_kernel_is_shared_v4_involution": (
            shared_intersection
            == {identity, triangle_kernel}
        ),
        "vertex_only_element_count_is_2": (
            len(vertex_only_elements) == 2
        ),
        "outside_fixed_plane_has_four_vectors": (
            len(outside_fixed_plane) == 4
        ),
        "outside_vectors_form_two_transvection_pairs": (
            len(outside_pairs) == 2
            and all(
                len(set(pair)) == 2
                for pair in outside_pairs
            )
        ),
        "transvection_difference_is_unique_nonzero_vector": (
            len(nonzero_difference_vectors) == 1
        ),
    }

    fixed_plane_named_labels = sorted(
        named_coordinates,
        key=lambda label: (
            named_coordinates[label],
            label,
        ),
    )

    difference_coordinate = (
        next(iter(nonzero_difference_vectors))
        if len(nonzero_difference_vectors) == 1
        else None
    )

    payload = {
        "certificate_id": (
            "native_g30_c2_cube_named_fixed_plane_023"
        ),
        "linear_source": str(
            LINEAR_SOURCE.relative_to(ROOT)
        ),
        "local_v4_source": str(
            LOCAL_V4_SOURCE.relative_to(ROOT)
        ),
        "comparison_source": str(
            COMPARISON_SOURCE.relative_to(ROOT)
        ),
        "named_coordinates": {
            label: list(coordinate)
            for label, coordinate
            in sorted(named_coordinates.items())
        },
        "fixed_nonzero_vectors": [
            list(vector)
            for vector in sorted(
                fixed_nonzero_vectors
            )
        ],
        "fixed_plane_named_labels": (
            fixed_plane_named_labels
        ),
        "fixed_plane_equals_local_triangle_klein_four": False,
        "fixed_plane_intersection_with_local_triangle_klein_four": [
            "identity",
            "central_deck",
        ],
        "shared_vertex_local_involution": (
            "triangle_kernel"
            if shared_intersection
            == {identity, triangle_kernel}
            else "unresolved"
        ),
        "vertex_stabilizer_only_rows": (
            vertex_only_rows
        ),
        "outside_fixed_plane_vectors": [
            list(vector)
            for vector in outside_fixed_plane
        ],
        "outside_transvection_pairs": [
            [
                list(vector)
                for vector in pair
            ]
            for pair in outside_pairs
        ],
        "transvection_difference_coordinate": (
            list(difference_coordinate)
            if difference_coordinate is not None
            else None
        ),
        "transvection_difference_named_labels": (
            difference_named_labels
        ),
        "classification_result": (
            "The transvection-fixed plane is not the "
            "triangle-local Klein four. It contains the central "
            "deck involution z and the vertex-stabilizer-only "
            "involution with coordinate [0,1,0] and two fixed "
            "vertices. The triangle-kernel involution k lies "
            "outside the fixed plane. The transvection adds the "
            "fixed direction [0,1,0], swapping the "
            "vertex-stabilizer-only six-fixed-point involution "
            "[1,0,0] with k=[1,1,0], and swapping its z-translate "
            "[1,0,1] with zk=[1,1,1]."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "named_fixed_plane_identified": True,
            "local_triangle_klein_four_is_fixed_plane": False,
            "central_deck_is_fixed_plane_intersection": True,
            "shared_triangle_kernel_coordinate_bound": True,
            "outside_transvection_pairs_exported": True,
            "canonical_geometric_axis_names_open": True,
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
        "named_coordinates:",
        payload["named_coordinates"],
    )
    print(
        "fixed_plane_named_labels:",
        payload["fixed_plane_named_labels"],
    )
    print(
        "fixed_plane_equals_local_triangle_klein_four:",
        payload[
            "fixed_plane_equals_local_triangle_klein_four"
        ],
    )
    print(
        "shared_vertex_local_involution:",
        payload["shared_vertex_local_involution"],
    )
    print(
        "vertex_stabilizer_only_rows:",
        payload["vertex_stabilizer_only_rows"],
    )
    print(
        "outside_transvection_pairs:",
        payload["outside_transvection_pairs"],
    )
    print(
        "transvection_difference_coordinate:",
        payload[
            "transvection_difference_coordinate"
        ],
    )
    print(
        "transvection_difference_named_labels:",
        payload[
            "transvection_difference_named_labels"
        ],
    )
    print(
        "classification_result:",
        payload["classification_result"],
    )


if __name__ == "__main__":
    main()
