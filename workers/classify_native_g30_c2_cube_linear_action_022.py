#!/usr/bin/env python3
"""Classify the normalizer conjugation action on E = C2^3."""

import json
from collections import Counter
from itertools import product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

NORMALIZER_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_c2_cube_normalizer_020.json"
)

GROUP_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_generated_order8_subgroup_015.json"
)

OUTPUT = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_c2_cube_linear_action_022.json"
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


def conjugate(carrier, element):
    return compose(
        compose(carrier, element),
        inverse(carrier),
    )


def vector_add(left, right):
    return tuple(
        a ^ b
        for a, b in zip(left, right)
    )


def matrix_apply(matrix, vector):
    dimension = len(vector)

    return tuple(
        sum(
            matrix[row][column] * vector[column]
            for column in range(dimension)
        )
        % 2
        for row in range(dimension)
    )


def matrix_multiply(left, right):
    dimension = len(left)

    return tuple(
        tuple(
            sum(
                left[row][middle] * right[middle][column]
                for middle in range(dimension)
            )
            % 2
            for column in range(dimension)
        )
        for row in range(dimension)
    )


def identity_matrix(dimension):
    return tuple(
        tuple(
            1 if row == column else 0
            for column in range(dimension)
        )
        for row in range(dimension)
    )


def matrix_rank_mod2(matrix):
    rows = [
        list(row)
        for row in matrix
    ]

    if not rows:
        return 0

    row_count = len(rows)
    column_count = len(rows[0])
    pivot_row = 0

    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(pivot_row, row_count)
                if rows[row][column] == 1
            ),
            None,
        )

        if pivot is None:
            continue

        rows[pivot_row], rows[pivot] = (
            rows[pivot],
            rows[pivot_row],
        )

        for row in range(row_count):
            if row == pivot_row:
                continue

            if rows[row][column] == 0:
                continue

            rows[row] = [
                left ^ right
                for left, right in zip(
                    rows[row],
                    rows[pivot_row],
                )
            ]

        pivot_row += 1

        if pivot_row == row_count:
            break

    return pivot_row


def matrix_difference(left, right):
    return tuple(
        tuple(
            a ^ b
            for a, b in zip(left_row, right_row)
        )
        for left_row, right_row in zip(left, right)
    )


def subgroup_from_basis(basis, identity):
    coordinate_to_element = {}

    for vector in product((0, 1), repeat=len(basis)):
        element = identity

        for bit, generator in zip(vector, basis):
            if bit:
                element = compose(generator, element)

        coordinate_to_element[tuple(vector)] = element

    return coordinate_to_element


def choose_basis(group, identity):
    nonidentity = tuple(sorted(
        element
        for element in group
        if element != identity
    ))

    basis = []
    generated = {identity}

    for candidate in nonidentity:
        if candidate in generated:
            continue

        basis.append(candidate)

        coordinate_to_element = subgroup_from_basis(
            tuple(basis),
            identity,
        )

        generated = set(
            coordinate_to_element.values()
        )

        if len(generated) == len(group):
            break

    return tuple(basis)


def matrix_from_basis_images(image_vectors):
    dimension = len(image_vectors)

    return tuple(
        tuple(
            image_vectors[column][row]
            for column in range(dimension)
        )
        for row in range(dimension)
    )


def main():
    normalizer_source = json.loads(
        NORMALIZER_SOURCE.read_text()
    )

    group_source = json.loads(
        GROUP_SOURCE.read_text()
    )

    cube_group = frozenset(
        tuple(element)
        for element in group_source["elements"]
    )

    normalizer_rows = tuple(
        normalizer_source["normalizer_action_rows"]
    )

    normalizer = frozenset(
        tuple(row["carrier"])
        for row in normalizer_rows
    )

    degree = len(next(iter(cube_group)))
    identity = tuple(range(degree))

    basis = choose_basis(
        cube_group,
        identity,
    )

    coordinate_to_element = subgroup_from_basis(
        basis,
        identity,
    )

    element_to_coordinate = {
        element: coordinate
        for coordinate, element
        in coordinate_to_element.items()
    }

    dimension = len(basis)
    identity_linear = identity_matrix(dimension)

    action_rows = []

    for source_row in normalizer_rows:
        carrier = tuple(source_row["carrier"])

        basis_images = tuple(
            conjugate(carrier, generator)
            for generator in basis
        )

        image_vectors = tuple(
            element_to_coordinate[element]
            for element in basis_images
        )

        matrix = matrix_from_basis_images(
            image_vectors
        )

        action_rows.append({
            "carrier": list(carrier),
            "carrier_order": source_row[
                "carrier_order"
            ],
            "induced_orbit_permutation": source_row[
                "induced_orbit_permutation"
            ],
            "basis_image_coordinates": [
                list(vector)
                for vector in image_vectors
            ],
            "matrix": [
                list(row)
                for row in matrix
            ],
            "matrix_is_identity": (
                matrix == identity_linear
            ),
        })

    image_group = frozenset(
        tuple(
            tuple(row)
            for row in action_row["matrix"]
        )
        for action_row in action_rows
    )

    kernel = frozenset(
        tuple(row["carrier"])
        for row in action_rows
        if row["matrix_is_identity"]
    )

    nonidentity_matrices = tuple(
        matrix
        for matrix in image_group
        if matrix != identity_linear
    )

    nontrivial_matrix = (
        nonidentity_matrices[0]
        if len(nonidentity_matrices) == 1
        else None
    )

    all_vectors = tuple(
        product((0, 1), repeat=dimension)
    )

    nonzero_vectors = tuple(
        vector
        for vector in all_vectors
        if any(vector)
    )

    fixed_vectors = (
        tuple(
            vector
            for vector in all_vectors
            if matrix_apply(
                nontrivial_matrix,
                vector,
            )
            == vector
        )
        if nontrivial_matrix is not None
        else ()
    )

    fixed_nonzero_vectors = tuple(
        vector
        for vector in fixed_vectors
        if any(vector)
    )

    nonzero_vector_orbits = []
    unseen = set(nonzero_vectors)

    while unseen:
        vector = min(unseen)

        orbit = frozenset(
            matrix_apply(matrix, vector)
            for matrix in image_group
        )

        nonzero_vector_orbits.append(
            tuple(sorted(orbit))
        )

        unseen -= set(orbit)

    nonzero_vector_orbits = tuple(sorted(
        nonzero_vector_orbits,
        key=lambda orbit: (
            len(orbit),
            orbit,
        ),
    ))

    matrix_order_profile = Counter()

    for matrix in image_group:
        current = identity_linear
        order = 0

        while True:
            order += 1
            current = matrix_multiply(
                matrix,
                current,
            )

            if current == identity_linear:
                matrix_order_profile[order] += 1
                break

    orbit_identity = tuple(
        range(
            len(
                normalizer_rows[0][
                    "induced_orbit_permutation"
                ]
            )
        )
    )

    quotient_character_matches_linear_action = all(
        (
            tuple(row["induced_orbit_permutation"])
            == orbit_identity
        )
        == row["matrix_is_identity"]
        for row in action_rows
    )

    rank_m_minus_i = (
        matrix_rank_mod2(
            matrix_difference(
                nontrivial_matrix,
                identity_linear,
            )
        )
        if nontrivial_matrix is not None
        else None
    )

    fixed_space_dimension = (
        dimension - rank_m_minus_i
        if rank_m_minus_i is not None
        else None
    )

    nontrivial_matrix_squared = (
        matrix_multiply(
            nontrivial_matrix,
            nontrivial_matrix,
        )
        if nontrivial_matrix is not None
        else None
    )

    action_type = (
        "rank_1_transvection_over_F2"
        if (
            nontrivial_matrix is not None
            and nontrivial_matrix_squared
            == identity_linear
            and rank_m_minus_i == 1
        )
        else "unclassified"
    )

    checks = {
        "normalizer_source_audit_pass": (
            normalizer_source["audit_pass"]
        ),
        "cube_group_source_audit_pass": (
            group_source["audit_pass"]
        ),
        "cube_group_order_is_8": (
            len(cube_group) == 8
        ),
        "basis_dimension_is_3": (
            dimension == 3
        ),
        "basis_generates_cube_group": (
            set(coordinate_to_element.values())
            == set(cube_group)
        ),
        "normalizer_order_is_16": (
            len(normalizer) == 16
        ),
        "linear_image_order_is_2": (
            len(image_group) == 2
        ),
        "linear_kernel_order_is_8": (
            len(kernel) == 8
        ),
        "linear_kernel_equals_cube_group": (
            kernel == cube_group
        ),
        "unique_nonidentity_matrix_exists": (
            nontrivial_matrix is not None
        ),
        "nonidentity_matrix_has_order_2": (
            nontrivial_matrix_squared
            == identity_linear
        ),
        "nonidentity_matrix_is_rank_1_transvection": (
            rank_m_minus_i == 1
        ),
        "fixed_space_dimension_is_2": (
            fixed_space_dimension == 2
        ),
        "three_nonzero_vectors_are_fixed": (
            len(fixed_nonzero_vectors) == 3
        ),
        "orbit_and_linear_characters_agree": (
            quotient_character_matches_linear_action
        ),
    }

    payload = {
        "certificate_id": (
            "native_g30_c2_cube_linear_action_022"
        ),
        "normalizer_source": str(
            NORMALIZER_SOURCE.relative_to(ROOT)
        ),
        "cube_group_source": str(
            GROUP_SOURCE.relative_to(ROOT)
        ),
        "cube_group_order": len(cube_group),
        "vector_space_dimension": dimension,
        "basis_permutations": [
            list(generator)
            for generator in basis
        ],
        "coordinate_table": [
            {
                "coordinate": list(coordinate),
                "permutation": list(element),
            }
            for coordinate, element
            in sorted(coordinate_to_element.items())
        ],
        "normalizer_order": len(normalizer),
        "linear_image_order": len(image_group),
        "linear_image_element_order_profile": {
            str(order): count
            for order, count in sorted(
                matrix_order_profile.items()
            )
        },
        "linear_image_matrices": [
            [
                list(row)
                for row in matrix
            ]
            for matrix in sorted(image_group)
        ],
        "linear_kernel_order": len(kernel),
        "linear_kernel_equals_cube_group": (
            kernel == cube_group
        ),
        "nontrivial_matrix": (
            [
                list(row)
                for row in nontrivial_matrix
            ]
            if nontrivial_matrix is not None
            else None
        ),
        "nontrivial_matrix_rank_m_minus_i": (
            rank_m_minus_i
        ),
        "fixed_space_dimension": (
            fixed_space_dimension
        ),
        "fixed_vectors": [
            list(vector)
            for vector in fixed_vectors
        ],
        "fixed_nonzero_vectors": [
            list(vector)
            for vector in fixed_nonzero_vectors
        ],
        "nonzero_vector_orbits": [
            [
                list(vector)
                for vector in orbit
            ]
            for orbit in nonzero_vector_orbits
        ],
        "action_type": action_type,
        "weighted_orbit_swap_character_matches_linear_action": (
            quotient_character_matches_linear_action
        ),
        "action_rows": action_rows,
        "classification_result": (
            "The normalizer acts on E = C2^3 through an "
            "order-2 subgroup of GL(3,2). Its kernel is E "
            "itself. The unique nontrivial linear map is a "
            "rank-1 transvection over F2, fixing a 2-dimensional "
            "plane and acting by two swaps on the remaining "
            "four nonzero vectors. This linear character agrees "
            "exactly with the weighted orbit-arm swap character."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "normalizer_linear_action_classified": True,
            "cube_basis_exported": True,
            "transvection_fixed_plane_exported": True,
            "orbit_swap_linear_character_identified": True,
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
        "vector_space_dimension:",
        payload["vector_space_dimension"],
    )
    print(
        "linear_image_order:",
        payload["linear_image_order"],
    )
    print(
        "linear_image_element_order_profile:",
        payload[
            "linear_image_element_order_profile"
        ],
    )
    print(
        "linear_kernel_order:",
        payload["linear_kernel_order"],
    )
    print(
        "linear_kernel_equals_cube_group:",
        payload["linear_kernel_equals_cube_group"],
    )
    print(
        "nontrivial_matrix:",
        payload["nontrivial_matrix"],
    )
    print(
        "nontrivial_matrix_rank_m_minus_i:",
        payload[
            "nontrivial_matrix_rank_m_minus_i"
        ],
    )
    print(
        "fixed_space_dimension:",
        payload["fixed_space_dimension"],
    )
    print(
        "fixed_nonzero_vectors:",
        payload["fixed_nonzero_vectors"],
    )
    print(
        "nonzero_vector_orbits:",
        payload["nonzero_vector_orbits"],
    )
    print("action_type:", payload["action_type"])
    print(
        "weighted_orbit_swap_character_matches_linear_action:",
        payload[
            "weighted_orbit_swap_character_matches_linear_action"
        ],
    )
    print(
        "classification_result:",
        payload["classification_result"],
    )


if __name__ == "__main__":
    main()
