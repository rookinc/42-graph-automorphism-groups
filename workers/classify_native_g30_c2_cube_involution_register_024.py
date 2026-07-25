#!/usr/bin/env python3
"""Classify all seven nonidentity elements of the local C2^3."""

import json
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

GRAPH_SOURCE = (
    ROOT
    / "sources"
    / "native_g30_graph_input_001.json"
)

LINEAR_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_c2_cube_linear_action_022.json"
)

PLANE_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_c2_cube_named_fixed_plane_023.json"
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
    / "native_g30_c2_cube_involution_register_024.json"
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


def fixed_vertices(permutation):
    return tuple(
        vertex
        for vertex, image in enumerate(permutation)
        if vertex == image
    )


def setwise_fixed_edges(permutation, edges):
    return tuple(
        edge
        for edge in edges
        if tuple(sorted((
            permutation[edge[0]],
            permutation[edge[1]],
        ))) == edge
    )


def pointwise_fixed_edges(permutation, edges):
    return tuple(
        edge
        for edge in edges
        if permutation[edge[0]] == edge[0]
        and permutation[edge[1]] == edge[1]
    )


def triangle_set(vertices, edges):
    edge_set = frozenset(edges)

    return tuple(sorted(
        triple
        for triple in combinations(vertices, 3)
        if all(
            tuple(sorted(edge)) in edge_set
            for edge in combinations(triple, 2)
        )
    ))


def image_of_subset(subset, permutation):
    return tuple(sorted(
        permutation[vertex]
        for vertex in subset
    ))


def fixed_triangles(permutation, triangles):
    setwise = tuple(
        triangle
        for triangle in triangles
        if image_of_subset(
            triangle,
            permutation,
        ) == triangle
    )

    pointwise = tuple(
        triangle
        for triangle in setwise
        if all(
            permutation[vertex] == vertex
            for vertex in triangle
        )
    )

    return pointwise, setwise


def provisional_name(
    coordinate,
    established_name,
    in_fixed_plane,
    in_local_v4,
    in_vertex_v4,
    fixed_vertex_count,
):
    if established_name is not None:
        return established_name

    if (
        in_fixed_plane
        and in_vertex_v4
        and fixed_vertex_count == 2
    ):
        return "fixed_plane_vertex_involution_d"

    if (
        in_vertex_v4
        and not in_fixed_plane
        and fixed_vertex_count == 6
    ):
        return "vertex_only_six_fixed_involution_u"

    if coordinate == (0, 1, 1):
        return "central_translate_zd"

    if coordinate == (1, 0, 1):
        return "central_translate_zu"

    return "unnamed"


def main():
    graph_source = json.loads(GRAPH_SOURCE.read_text())
    linear_source = json.loads(
        LINEAR_SOURCE.read_text()
    )
    plane_source = json.loads(
        PLANE_SOURCE.read_text()
    )
    local_source = json.loads(
        LOCAL_V4_SOURCE.read_text()
    )
    comparison_source = json.loads(
        COMPARISON_SOURCE.read_text()
    )

    vertices = tuple(graph_source["vertices"])
    edges = tuple(sorted(
        tuple(sorted(edge))
        for edge in graph_source["edges"]
    ))
    triangles = triangle_set(vertices, edges)

    coordinate_to_element = {
        tuple(row["coordinate"]): tuple(row["permutation"])
        for row in linear_source["coordinate_table"]
    }

    element_to_coordinate = {
        element: coordinate
        for coordinate, element
        in coordinate_to_element.items()
    }

    established_element_names = {
        tuple(row["permutation"]): row["label"]
        for row in local_source[
            "nonidentity_element_anatomy"
        ]
    }

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

    fixed_plane = frozenset(
        tuple(vector)
        for vector in linear_source[
            "fixed_nonzero_vectors"
        ]
    )

    matrix = tuple(
        tuple(row)
        for row in linear_source[
            "nontrivial_matrix"
        ]
    )

    rows = []

    for coordinate in sorted(coordinate_to_element):
        if not any(coordinate):
            continue

        element = coordinate_to_element[coordinate]
        fixed = fixed_vertices(element)
        pointwise_edges = pointwise_fixed_edges(
            element,
            edges,
        )
        setwise_edges = setwise_fixed_edges(
            element,
            edges,
        )
        pointwise_triangles, setwise_triangles = (
            fixed_triangles(
                element,
                triangles,
            )
        )

        image_coordinate = matrix_apply(
            matrix,
            coordinate,
        )

        established_name = (
            established_element_names.get(element)
        )

        name = provisional_name(
            coordinate=coordinate,
            established_name=established_name,
            in_fixed_plane=coordinate in fixed_plane,
            in_local_v4=element in local_v4,
            in_vertex_v4=element in vertex_v4,
            fixed_vertex_count=len(fixed),
        )

        rows.append({
            "coordinate": list(coordinate),
            "name": name,
            "established_name": established_name,
            "fixed_plane_member": (
                coordinate in fixed_plane
            ),
            "local_triangle_v4_member": (
                element in local_v4
            ),
            "vertex_stabilizer_v4_member": (
                element in vertex_v4
            ),
            "fixed_vertex_count": len(fixed),
            "fixed_vertices": list(fixed),
            "pointwise_fixed_edge_count": len(
                pointwise_edges
            ),
            "setwise_fixed_edge_count": len(
                setwise_edges
            ),
            "pointwise_fixed_triangle_count": len(
                pointwise_triangles
            ),
            "setwise_fixed_triangle_count": len(
                setwise_triangles
            ),
            "transvection_image_coordinate": list(
                image_coordinate
            ),
            "transvection_fixed": (
                image_coordinate == coordinate
            ),
            "permutation": list(element),
        })

    row_by_coordinate = {
        tuple(row["coordinate"]): row
        for row in rows
    }

    for row in rows:
        partner_coordinate = tuple(
            row["transvection_image_coordinate"]
        )
        row["transvection_partner_name"] = (
            row_by_coordinate[
                partner_coordinate
            ]["name"]
        )

    fixed_rows = tuple(
        row
        for row in rows
        if row["transvection_fixed"]
    )

    swapped_pairs = []
    seen = set()

    for row in rows:
        coordinate = tuple(row["coordinate"])

        if coordinate in seen:
            continue

        partner = tuple(
            row["transvection_image_coordinate"]
        )

        seen.add(coordinate)
        seen.add(partner)

        if partner == coordinate:
            continue

        swapped_pairs.append({
            "left_coordinate": list(
                min(coordinate, partner)
            ),
            "right_coordinate": list(
                max(coordinate, partner)
            ),
            "left_name": row_by_coordinate[
                min(coordinate, partner)
            ]["name"],
            "right_name": row_by_coordinate[
                max(coordinate, partner)
            ]["name"],
        })

    name_to_coordinate = {
        row["name"]: row["coordinate"]
        for row in rows
    }

    checks = {
        "linear_source_audit_pass": (
            linear_source["audit_pass"]
        ),
        "plane_source_audit_pass": (
            plane_source["audit_pass"]
        ),
        "local_source_audit_pass": (
            local_source["audit_pass"]
        ),
        "comparison_source_audit_pass": (
            comparison_source["audit_pass"]
        ),
        "seven_nonidentity_rows_recorded": (
            len(rows) == 7
        ),
        "three_transvection_fixed_nonidentity_rows": (
            len(fixed_rows) == 3
        ),
        "two_transvection_swapped_pairs": (
            len(swapped_pairs) == 2
        ),
        "central_deck_coordinate_matches_023": (
            name_to_coordinate["central_deck"]
            == plane_source["named_coordinates"][
                "central_deck"
            ]
        ),
        "triangle_kernel_coordinate_matches_023": (
            name_to_coordinate["triangle_kernel"]
            == plane_source["named_coordinates"][
                "triangle_kernel"
            ]
        ),
        "deck_times_kernel_coordinate_matches_023": (
            name_to_coordinate["deck_times_kernel"]
            == plane_source["named_coordinates"][
                "deck_times_kernel"
            ]
        ),
        "d_is_fixed_plane_vertex_v4_element": (
            name_to_coordinate[
                "fixed_plane_vertex_involution_d"
            ]
            == [0, 1, 0]
        ),
        "u_is_vertex_only_six_fixed_element": (
            name_to_coordinate[
                "vertex_only_six_fixed_involution_u"
            ]
            == [1, 0, 0]
        ),
        "u_and_kernel_are_transvection_pair": (
            row_by_coordinate[(1, 0, 0)][
                "transvection_image_coordinate"
            ]
            == [1, 1, 0]
        ),
        "zu_and_zk_are_transvection_pair": (
            row_by_coordinate[(1, 0, 1)][
                "transvection_image_coordinate"
            ]
            == [1, 1, 1]
        ),
    }

    payload = {
        "certificate_id": (
            "native_g30_c2_cube_involution_register_024"
        ),
        "graph_source": str(
            GRAPH_SOURCE.relative_to(ROOT)
        ),
        "linear_source": str(
            LINEAR_SOURCE.relative_to(ROOT)
        ),
        "plane_source": str(
            PLANE_SOURCE.relative_to(ROOT)
        ),
        "local_v4_source": str(
            LOCAL_V4_SOURCE.relative_to(ROOT)
        ),
        "comparison_source": str(
            COMPARISON_SOURCE.relative_to(ROOT)
        ),
        "group_order": len(coordinate_to_element),
        "nonidentity_element_count": len(rows),
        "involution_rows": rows,
        "transvection_fixed_names": [
            row["name"]
            for row in fixed_rows
        ],
        "transvection_swapped_pairs": swapped_pairs,
        "name_to_coordinate": name_to_coordinate,
        "classification_result": (
            "The seven nonidentity elements of E=C2^3 now "
            "have a single source-bound register. The fixed "
            "plane contains z, d, and zd. The two outside "
            "transvection pairs are u<->k and zu<->zk. "
            "Membership in the triangle-local and "
            "vertex-stabilizer Klein fours, together with "
            "fixed vertex, edge, and triangle anatomy, is "
            "recorded for every involution."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "seven_involution_register_complete": True,
            "established_names_preserved": True,
            "provisional_d_u_names_introduced": True,
            "canonical_geometric_names_for_d_u_open": True,
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
        "transvection_fixed_names:",
        payload["transvection_fixed_names"],
    )
    print(
        "transvection_swapped_pairs:",
        payload["transvection_swapped_pairs"],
    )

    for row in rows:
        print(
            row["coordinate"],
            row["name"],
            "fixed vertices:",
            row["fixed_vertex_count"],
            "fixed edges:",
            row["pointwise_fixed_edge_count"],
            "fixed triangles:",
            row["setwise_fixed_triangle_count"],
            "local_v4:",
            row["local_triangle_v4_member"],
            "vertex_v4:",
            row["vertex_stabilizer_v4_member"],
            "partner:",
            row["transvection_partner_name"],
        )

    print(
        "classification_result:",
        payload["classification_result"],
    )


if __name__ == "__main__":
    main()
