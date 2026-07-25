#!/usr/bin/env python3
"""Compare the fixed subgraphs of the paired involutions u and k."""

import json
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

GRAPH_SOURCE = (
    ROOT
    / "sources"
    / "native_g30_graph_input_001.json"
)

REGISTER_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_c2_cube_involution_register_024.json"
)

NORMALIZER_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_c2_cube_normalizer_020.json"
)

OUTPUT = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_u_k_fixed_subgraph_comparison_025.json"
)


def canonical_edge(left, right):
    return tuple(sorted((left, right)))


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


def image_of_subset(subset, permutation):
    return tuple(sorted(
        permutation[vertex]
        for vertex in subset
    ))


def triangle_set(vertices, edges):
    edge_set = frozenset(edges)

    return tuple(sorted(
        triple
        for triple in combinations(vertices, 3)
        if all(
            canonical_edge(*edge) in edge_set
            for edge in combinations(triple, 2)
        )
    ))


def fixed_vertices(permutation):
    return tuple(
        vertex
        for vertex, image in enumerate(permutation)
        if vertex == image
    )


def induced_edges(vertex_set, edges):
    vertex_set = frozenset(vertex_set)

    return tuple(
        edge
        for edge in edges
        if edge[0] in vertex_set
        and edge[1] in vertex_set
    )


def setwise_fixed_triangles(permutation, triangles):
    return tuple(
        triangle
        for triangle in triangles
        if image_of_subset(
            triangle,
            permutation,
        ) == triangle
    )


def pointwise_fixed_triangles(permutation, triangles):
    return tuple(
        triangle
        for triangle in triangles
        if all(
            permutation[vertex] == vertex
            for vertex in triangle
        )
    )


def component_sizes(vertices, edges):
    adjacency = {
        vertex: set()
        for vertex in vertices
    }

    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)

    unseen = set(vertices)
    sizes = []

    while unseen:
        start = min(unseen)
        stack = [start]
        unseen.remove(start)
        size = 0

        while stack:
            current = stack.pop()
            size += 1

            for neighbor in adjacency[current]:
                if neighbor not in unseen:
                    continue

                unseen.remove(neighbor)
                stack.append(neighbor)

        sizes.append(size)

    return tuple(sorted(sizes, reverse=True))


def degree_profile(vertices, edges):
    degree = {
        vertex: 0
        for vertex in vertices
    }

    for left, right in edges:
        degree[left] += 1
        degree[right] += 1

    profile = {}

    for value in degree.values():
        profile[value] = profile.get(value, 0) + 1

    return {
        str(key): profile[key]
        for key in sorted(profile)
    }


def fixed_structure(permutation, triangles, edges):
    vertices = fixed_vertices(permutation)
    fixed_edges = induced_edges(vertices, edges)

    return {
        "fixed_vertices": vertices,
        "fixed_edges": fixed_edges,
        "component_sizes": component_sizes(
            vertices,
            fixed_edges,
        ),
        "degree_profile": degree_profile(
            vertices,
            fixed_edges,
        ),
        "pointwise_fixed_triangles": (
            pointwise_fixed_triangles(
                permutation,
                triangles,
            )
        ),
        "setwise_fixed_triangles": (
            setwise_fixed_triangles(
                permutation,
                triangles,
            )
        ),
    }


def main():
    graph_source = json.loads(
        GRAPH_SOURCE.read_text()
    )

    register_source = json.loads(
        REGISTER_SOURCE.read_text()
    )

    normalizer_source = json.loads(
        NORMALIZER_SOURCE.read_text()
    )

    vertices = tuple(graph_source["vertices"])

    edges = tuple(sorted(
        canonical_edge(*edge)
        for edge in graph_source["edges"]
    ))

    triangles = triangle_set(vertices, edges)

    rows_by_name = {
        row["name"]: row
        for row in register_source["involution_rows"]
    }

    u_row = rows_by_name[
        "vertex_only_six_fixed_involution_u"
    ]

    k_row = rows_by_name["triangle_kernel"]

    u = tuple(u_row["permutation"])
    k = tuple(k_row["permutation"])

    u_structure = fixed_structure(
        u,
        triangles,
        edges,
    )

    k_structure = fixed_structure(
        k,
        triangles,
        edges,
    )

    u_vertices = frozenset(
        u_structure["fixed_vertices"]
    )

    k_vertices = frozenset(
        k_structure["fixed_vertices"]
    )

    common_vertices = tuple(sorted(
        u_vertices.intersection(k_vertices)
    ))

    union_vertices = tuple(sorted(
        u_vertices.union(k_vertices)
    ))

    u_only_vertices = tuple(sorted(
        u_vertices - k_vertices
    ))

    k_only_vertices = tuple(sorted(
        k_vertices - u_vertices
    ))

    u_setwise_triangles = frozenset(
        u_structure["setwise_fixed_triangles"]
    )

    k_setwise_triangles = frozenset(
        k_structure["setwise_fixed_triangles"]
    )

    common_setwise_triangles = tuple(sorted(
        u_setwise_triangles.intersection(
            k_setwise_triangles
        )
    ))

    u_only_setwise_triangles = tuple(sorted(
        u_setwise_triangles - k_setwise_triangles
    ))

    k_only_setwise_triangles = tuple(sorted(
        k_setwise_triangles - u_setwise_triangles
    ))

    normalizer_rows = tuple(
        normalizer_source["normalizer_action_rows"]
    )

    u_to_k_lifts = []

    for row in normalizer_rows:
        carrier = tuple(row["carrier"])

        if conjugate(carrier, u) != k:
            continue

        mapped_u_vertices = image_of_subset(
            u_structure["fixed_vertices"],
            carrier,
        )

        mapped_u_edges = tuple(sorted(
            canonical_edge(
                carrier[left],
                carrier[right],
            )
            for left, right in u_structure[
                "fixed_edges"
            ]
        ))

        mapped_u_triangles = tuple(sorted(
            image_of_subset(
                triangle,
                carrier,
            )
            for triangle in u_structure[
                "setwise_fixed_triangles"
            ]
        ))

        u_to_k_lifts.append({
            "carrier": list(carrier),
            "carrier_order": row[
                "carrier_order"
            ],
            "induced_orbit_permutation": row[
                "induced_orbit_permutation"
            ],
            "maps_fixed_vertices_exactly": (
                mapped_u_vertices
                == k_structure["fixed_vertices"]
            ),
            "maps_fixed_edges_exactly": (
                mapped_u_edges
                == k_structure["fixed_edges"]
            ),
            "maps_setwise_fixed_triangles_exactly": (
                mapped_u_triangles
                == k_structure[
                    "setwise_fixed_triangles"
                ]
            ),
            "vertex_mapping": [
                [vertex, carrier[vertex]]
                for vertex in u_structure[
                    "fixed_vertices"
                ]
            ],
        })

    lift_order_profile = {}

    for row in u_to_k_lifts:
        order = str(row["carrier_order"])
        lift_order_profile[order] = (
            lift_order_profile.get(order, 0) + 1
        )

    same_fixed_vertex_set = (
        u_vertices == k_vertices
    )

    same_setwise_fixed_triangle_set = (
        u_setwise_triangles
        == k_setwise_triangles
    )

    checks = {
        "register_source_audit_pass": (
            register_source["audit_pass"]
        ),
        "normalizer_source_audit_pass": (
            normalizer_source["audit_pass"]
        ),
        "u_fixed_vertex_count_is_6": (
            len(u_vertices) == 6
        ),
        "k_fixed_vertex_count_is_6": (
            len(k_vertices) == 6
        ),
        "u_fixed_subgraph_is_two_triangles": (
            u_structure["component_sizes"]
            == (3, 3)
            and u_structure["degree_profile"]
            == {"2": 6}
        ),
        "k_fixed_subgraph_is_two_triangles": (
            k_structure["component_sizes"]
            == (3, 3)
            and k_structure["degree_profile"]
            == {"2": 6}
        ),
        "u_and_k_fixed_vertex_sets_are_distinct": (
            not same_fixed_vertex_set
        ),
        "u_and_k_setwise_fixed_triangle_sets_are_distinct": (
            not same_setwise_fixed_triangle_set
        ),
        "normalizer_lift_from_u_to_k_exists": (
            len(u_to_k_lifts) > 0
        ),
        "every_lift_maps_full_fixed_structure": all(
            row["maps_fixed_vertices_exactly"]
            and row["maps_fixed_edges_exactly"]
            and row[
                "maps_setwise_fixed_triangles_exactly"
            ]
            for row in u_to_k_lifts
        ),
    }

    payload = {
        "certificate_id": (
            "native_g30_u_k_fixed_subgraph_comparison_025"
        ),
        "graph_source": str(
            GRAPH_SOURCE.relative_to(ROOT)
        ),
        "register_source": str(
            REGISTER_SOURCE.relative_to(ROOT)
        ),
        "normalizer_source": str(
            NORMALIZER_SOURCE.relative_to(ROOT)
        ),
        "u_name": (
            "vertex_only_six_fixed_involution_u"
        ),
        "k_name": "triangle_kernel",
        "u_coordinate": u_row["coordinate"],
        "k_coordinate": k_row["coordinate"],
        "u_structure": {
            "fixed_vertices": list(
                u_structure["fixed_vertices"]
            ),
            "fixed_edges": [
                list(edge)
                for edge in u_structure["fixed_edges"]
            ],
            "component_sizes": list(
                u_structure["component_sizes"]
            ),
            "degree_profile": (
                u_structure["degree_profile"]
            ),
            "pointwise_fixed_triangles": [
                list(triangle)
                for triangle in u_structure[
                    "pointwise_fixed_triangles"
                ]
            ],
            "setwise_fixed_triangles": [
                list(triangle)
                for triangle in u_structure[
                    "setwise_fixed_triangles"
                ]
            ],
        },
        "k_structure": {
            "fixed_vertices": list(
                k_structure["fixed_vertices"]
            ),
            "fixed_edges": [
                list(edge)
                for edge in k_structure["fixed_edges"]
            ],
            "component_sizes": list(
                k_structure["component_sizes"]
            ),
            "degree_profile": (
                k_structure["degree_profile"]
            ),
            "pointwise_fixed_triangles": [
                list(triangle)
                for triangle in k_structure[
                    "pointwise_fixed_triangles"
                ]
            ],
            "setwise_fixed_triangles": [
                list(triangle)
                for triangle in k_structure[
                    "setwise_fixed_triangles"
                ]
            ],
        },
        "fixed_vertex_intersection_count": len(
            common_vertices
        ),
        "fixed_vertex_intersection": list(
            common_vertices
        ),
        "fixed_vertex_union_count": len(
            union_vertices
        ),
        "fixed_vertex_union": list(
            union_vertices
        ),
        "u_only_fixed_vertices": list(
            u_only_vertices
        ),
        "k_only_fixed_vertices": list(
            k_only_vertices
        ),
        "common_setwise_fixed_triangle_count": len(
            common_setwise_triangles
        ),
        "common_setwise_fixed_triangles": [
            list(triangle)
            for triangle in common_setwise_triangles
        ],
        "u_only_setwise_fixed_triangles": [
            list(triangle)
            for triangle in u_only_setwise_triangles
        ],
        "k_only_setwise_fixed_triangles": [
            list(triangle)
            for triangle in k_only_setwise_triangles
        ],
        "same_fixed_vertex_set": (
            same_fixed_vertex_set
        ),
        "same_setwise_fixed_triangle_set": (
            same_setwise_fixed_triangle_set
        ),
        "u_to_k_normalizer_lift_count": len(
            u_to_k_lifts
        ),
        "u_to_k_normalizer_lift_order_profile": (
            lift_order_profile
        ),
        "u_to_k_normalizer_lifts": (
            u_to_k_lifts
        ),
        "classification_result": (
            "The involutions u and k have isomorphic but "
            "distinct fixed subgraphs, each consisting of two "
            "disjoint triangles. Their fixed vertex and fixed "
            "triangle supports are compared explicitly. "
            "Normalizer elements inducing the transvection "
            "carry the entire fixed structure of u exactly "
            "onto that of k."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "u_k_fixed_subgraphs_compared": True,
            "fixed_support_overlap_exported": True,
            "normalizer_transport_witnesses_exported": True,
            "intrinsic_name_distinguishing_u_from_k_open": True,
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
        "u_fixed_vertices:",
        payload["u_structure"]["fixed_vertices"],
    )
    print(
        "k_fixed_vertices:",
        payload["k_structure"]["fixed_vertices"],
    )
    print(
        "fixed_vertex_intersection_count:",
        payload["fixed_vertex_intersection_count"],
    )
    print(
        "fixed_vertex_intersection:",
        payload["fixed_vertex_intersection"],
    )
    print(
        "common_setwise_fixed_triangle_count:",
        payload[
            "common_setwise_fixed_triangle_count"
        ],
    )
    print(
        "u_to_k_normalizer_lift_count:",
        payload["u_to_k_normalizer_lift_count"],
    )
    print(
        "u_to_k_normalizer_lift_order_profile:",
        payload[
            "u_to_k_normalizer_lift_order_profile"
        ],
    )
    print(
        "u_component_sizes:",
        payload["u_structure"]["component_sizes"],
    )
    print(
        "k_component_sizes:",
        payload["k_structure"]["component_sizes"],
    )
    print(
        "classification_result:",
        payload["classification_result"],
    )


if __name__ == "__main__":
    main()
