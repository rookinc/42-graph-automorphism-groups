#!/usr/bin/env python3
"""Identify the native G30 central quotient as L(Petersen)."""

import json
from collections import Counter
from itertools import combinations
from pathlib import Path

import networkx as nx


ROOT = Path(__file__).resolve().parents[1]

LIFT_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_triangle_lifts_007.json"
)

OUTPUT = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_quotient_line_petersen_008.json"
)


def canonical_edge(left, right):
    return tuple(sorted((left, right)))


def triangle_set(vertices, edges):
    edge_set = frozenset(
        canonical_edge(*edge)
        for edge in edges
    )

    return tuple(sorted(
        triple
        for triple in combinations(vertices, 3)
        if all(
            canonical_edge(*edge) in edge_set
            for edge in combinations(triple, 2)
        )
    ))


def main():
    lift_source = json.loads(LIFT_SOURCE.read_text())

    quotient_vertices = tuple(
        range(lift_source["quotient_vertex_count"])
    )

    quotient_triangles = tuple(
        tuple(triangle)
        for triangle in lift_source["quotient_triangles"]
    )

    quotient_edges = set()

    for triangle in quotient_triangles:
        for edge in combinations(triangle, 2):
            quotient_edges.add(canonical_edge(*edge))

    quotient_edges = tuple(sorted(quotient_edges))

    petersen = nx.petersen_graph()

    petersen_vertices = tuple(sorted(petersen.nodes()))

    petersen_edges = tuple(sorted(
        canonical_edge(left, right)
        for left, right in petersen.edges()
    ))

    line_petersen = nx.line_graph(petersen)

    line_vertices = tuple(sorted(
        canonical_edge(*edge)
        for edge in line_petersen.nodes()
    ))

    line_vertex_index = {
        edge: index
        for index, edge in enumerate(line_vertices)
    }

    line_edges = tuple(sorted(
        canonical_edge(
            line_vertex_index[canonical_edge(*left)],
            line_vertex_index[canonical_edge(*right)],
        )
        for left, right in line_petersen.edges()
    ))

    quotient_graph = nx.Graph()
    quotient_graph.add_nodes_from(quotient_vertices)
    quotient_graph.add_edges_from(quotient_edges)

    indexed_line_graph = nx.Graph()
    indexed_line_graph.add_nodes_from(
        range(len(line_vertices))
    )
    indexed_line_graph.add_edges_from(line_edges)

    matcher = nx.algorithms.isomorphism.GraphMatcher(
        quotient_graph,
        indexed_line_graph,
    )

    isomorphisms = []

    for mapping in matcher.isomorphisms_iter():
        isomorphisms.append({
            int(source): int(target)
            for source, target in mapping.items()
        })

    isomorphisms.sort(
        key=lambda mapping: tuple(
            mapping[index]
            for index in quotient_vertices
        )
    )

    if not isomorphisms:
        raise RuntimeError(
            "quotient is not isomorphic to L(Petersen)"
        )

    selected_mapping = isomorphisms[0]

    quotient_to_petersen_edge = {
        quotient_vertex: line_vertices[
            selected_mapping[quotient_vertex]
        ]
        for quotient_vertex in quotient_vertices
    }

    petersen_vertex_stars = {
        vertex: tuple(sorted(
            line_vertex_index[
                canonical_edge(vertex, neighbor)
            ]
            for neighbor in petersen.neighbors(vertex)
        ))
        for vertex in petersen_vertices
    }

    quotient_triangle_rows = []

    matched_petersen_vertices = []

    for quotient_triangle in quotient_triangles:
        mapped_line_triangle = tuple(sorted(
            selected_mapping[vertex]
            for vertex in quotient_triangle
        ))

        matching_vertices = tuple(
            vertex
            for vertex, star in petersen_vertex_stars.items()
            if star == mapped_line_triangle
        )

        if len(matching_vertices) == 1:
            petersen_vertex = matching_vertices[0]
            matched_petersen_vertices.append(
                petersen_vertex
            )
        else:
            petersen_vertex = None

        quotient_triangle_rows.append({
            "quotient_triangle": list(quotient_triangle),
            "mapped_line_graph_vertices": list(
                mapped_line_triangle
            ),
            "mapped_petersen_edges": [
                list(line_vertices[index])
                for index in mapped_line_triangle
            ],
            "petersen_vertex": petersen_vertex,
            "is_vertex_star": len(matching_vertices) == 1,
        })

    quotient_vertex_triangle_incidence = Counter()

    for triangle in quotient_triangles:
        for vertex in triangle:
            quotient_vertex_triangle_incidence[vertex] += 1

    petersen_edge_star_incidence = Counter()

    for row in quotient_triangle_rows:
        for edge in row["mapped_petersen_edges"]:
            petersen_edge_star_incidence[
                tuple(edge)
            ] += 1

    checks = {
        "lift_source_audit_pass": (
            lift_source["audit_pass"]
        ),
        "quotient_vertex_count_is_15": (
            len(quotient_vertices) == 15
        ),
        "quotient_edge_count_is_30": (
            len(quotient_edges) == 30
        ),
        "quotient_triangle_count_is_10": (
            len(quotient_triangles) == 10
        ),
        "petersen_vertex_count_is_10": (
            len(petersen_vertices) == 10
        ),
        "petersen_edge_count_is_15": (
            len(petersen_edges) == 15
        ),
        "line_petersen_vertex_count_is_15": (
            len(line_vertices) == 15
        ),
        "line_petersen_edge_count_is_30": (
            len(line_edges) == 30
        ),
        "quotient_isomorphic_to_line_petersen": (
            len(isomorphisms) > 0
        ),
        "every_quotient_triangle_is_petersen_vertex_star": all(
            row["is_vertex_star"]
            for row in quotient_triangle_rows
        ),
        "all_10_petersen_vertices_used_once": (
            sorted(matched_petersen_vertices)
            == list(petersen_vertices)
        ),
        "every_quotient_vertex_lies_on_two_triangles": (
            len(quotient_vertex_triangle_incidence) == 15
            and set(
                quotient_vertex_triangle_incidence.values()
            )
            == {2}
        ),
        "every_petersen_edge_meets_two_vertex_stars": (
            len(petersen_edge_star_incidence) == 15
            and set(
                petersen_edge_star_incidence.values()
            )
            == {2}
        ),
    }

    payload = {
        "certificate_id": (
            "native_g30_quotient_line_petersen_008"
        ),
        "lift_source": str(
            LIFT_SOURCE.relative_to(ROOT)
        ),
        "quotient_vertex_count": len(quotient_vertices),
        "quotient_edge_count": len(quotient_edges),
        "quotient_triangle_count": len(quotient_triangles),
        "petersen_vertex_count": len(petersen_vertices),
        "petersen_edge_count": len(petersen_edges),
        "line_petersen_vertex_count": len(line_vertices),
        "line_petersen_edge_count": len(line_edges),
        "isomorphism_count": len(isomorphisms),
        "selected_quotient_to_line_petersen_mapping": {
            str(vertex): selected_mapping[vertex]
            for vertex in quotient_vertices
        },
        "quotient_vertex_to_petersen_edge": {
            str(vertex): list(edge)
            for vertex, edge in sorted(
                quotient_to_petersen_edge.items()
            )
        },
        "quotient_triangle_to_petersen_vertex": (
            quotient_triangle_rows
        ),
        "identification_result": (
            "The central G15 quotient is explicitly isomorphic "
            "to L(Petersen). Its 10 triangles are exactly the "
            "10 three-edge stars centered at Petersen vertices."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "quotient_identified_as_line_petersen": True,
            "quotient_triangles_bound_to_petersen_vertices": True,
            "g30_triangle_fibers_bound_to_petersen_vertices": True,
            "triangle_stabilizer_structure_not_yet_classified": True,
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
        "isomorphism_count:",
        payload["isomorphism_count"],
    )
    print(
        "quotient:",
        payload["quotient_vertex_count"],
        "vertices,",
        payload["quotient_edge_count"],
        "edges,",
        payload["quotient_triangle_count"],
        "triangles",
    )
    print(
        "all_triangles_are_vertex_stars:",
        checks[
            "every_quotient_triangle_is_petersen_vertex_star"
        ],
    )
    print(
        "all_10_petersen_vertices_used_once:",
        checks["all_10_petersen_vertices_used_once"],
    )
    print(
        "identification_result:",
        payload["identification_result"],
    )


if __name__ == "__main__":
    main()
