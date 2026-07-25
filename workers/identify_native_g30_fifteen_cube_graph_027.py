#!/usr/bin/env python3
"""Identify the order-4 cube-intersection graph as L(Petersen)."""

import json
from collections import Counter, deque
from itertools import combinations
from pathlib import Path

import networkx as nx


ROOT = Path(__file__).resolve().parents[1]

CENSUS_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_c2_cube_conjugacy_census_026.json"
)

OUTPUT = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_fifteen_cube_graph_027.json"
)


def canonical_edge(left, right):
    return tuple(sorted((left, right)))


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
        unseen.remove(start)
        queue = deque([start])
        size = 0

        while queue:
            current = queue.popleft()
            size += 1

            for neighbor in adjacency[current]:
                if neighbor not in unseen:
                    continue

                unseen.remove(neighbor)
                queue.append(neighbor)

        sizes.append(size)

    return tuple(sorted(sizes, reverse=True))


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


def graph6_string(graph):
    graph = nx.convert_node_labels_to_integers(
        graph,
        ordering="sorted",
    )

    return nx.to_graph6_bytes(
        graph,
        header=False,
    ).decode("ascii").strip()


def main():
    census = json.loads(CENSUS_SOURCE.read_text())

    vertices = tuple(
        range(census["conjugate_cube_count"])
    )

    edges = tuple(sorted(
        canonical_edge(
            row["left_cube"],
            row["right_cube"],
        )
        for row in census["cube_pair_rows"]
        if row["intersection_order"] == 4
    ))

    graph = nx.Graph()
    graph.add_nodes_from(vertices)
    graph.add_edges_from(edges)

    degree_profile = Counter(
        degree
        for _, degree in graph.degree()
    )

    triangles = triangle_set(vertices, edges)

    petersen = nx.petersen_graph()
    line_petersen = nx.line_graph(petersen)
    line_petersen = nx.convert_node_labels_to_integers(
        line_petersen,
        ordering="sorted",
    )

    matcher = nx.algorithms.isomorphism.GraphMatcher(
        graph,
        line_petersen,
    )

    isomorphisms = tuple(
        {
            int(source): int(target)
            for source, target in mapping.items()
        }
        for mapping in matcher.isomorphisms_iter()
    )

    representative_isomorphism = (
        isomorphisms[0]
        if isomorphisms
        else None
    )

    automorphism_matcher = (
        nx.algorithms.isomorphism.GraphMatcher(
            graph,
            graph,
        )
    )

    automorphisms = tuple(
        tuple(
            mapping[index]
            for index in vertices
        )
        for mapping in (
            automorphism_matcher.isomorphisms_iter()
        )
    )

    automorphism_vertex_orbits = []
    unseen = set(vertices)

    while unseen:
        vertex = min(unseen)

        orbit = tuple(sorted({
            permutation[vertex]
            for permutation in automorphisms
        }))

        automorphism_vertex_orbits.append(orbit)
        unseen -= set(orbit)

    intersection_v4_rows = []

    for row in census["cube_pair_rows"]:
        if row["intersection_order"] != 4:
            continue

        nonidentity = [
            element
            for element in row["intersection_elements"]
            if any(
                index != image
                for index, image in enumerate(element)
            )
        ]

        fixed_profile = Counter(
            sum(
                1
                for index, image in enumerate(element)
                if index == image
            )
            for element in nonidentity
        )

        intersection_v4_rows.append({
            "left_cube": row["left_cube"],
            "right_cube": row["right_cube"],
            "nonidentity_fixed_point_profile": {
                str(count): multiplicity
                for count, multiplicity in sorted(
                    fixed_profile.items()
                )
            },
        })

    edge_intersection_profile = Counter(
        tuple(sorted(
            (
                int(count),
                multiplicity,
            )
            for count, multiplicity
            in row[
                "nonidentity_fixed_point_profile"
            ].items()
        ))
        for row in intersection_v4_rows
    )

    checks = {
        "census_source_audit_pass": (
            census["audit_pass"]
        ),
        "vertex_count_is_15": (
            graph.number_of_nodes() == 15
        ),
        "edge_count_is_30": (
            graph.number_of_edges() == 30
        ),
        "graph_is_connected": (
            component_sizes(vertices, edges) == (15,)
        ),
        "graph_is_quartic": (
            degree_profile == {4: 15}
        ),
        "triangle_count_is_10": (
            len(triangles) == 10
        ),
        "isomorphic_to_line_petersen": (
            len(isomorphisms) > 0
        ),
        "line_petersen_vertex_count_matches": (
            line_petersen.number_of_nodes() == 15
        ),
        "line_petersen_edge_count_matches": (
            line_petersen.number_of_edges() == 30
        ),
        "automorphism_group_order_is_120": (
            len(automorphisms) == 120
        ),
        "automorphism_action_is_vertex_transitive": (
            automorphism_vertex_orbits
            == [tuple(vertices)]
        ),
    }

    payload = {
        "certificate_id": (
            "native_g30_fifteen_cube_graph_027"
        ),
        "census_source": str(
            CENSUS_SOURCE.relative_to(ROOT)
        ),
        "adjacency_rule": (
            "two conjugate C2^3 cubes are adjacent exactly "
            "when their subgroup intersection has order 4"
        ),
        "vertex_count": graph.number_of_nodes(),
        "edge_count": graph.number_of_edges(),
        "degree_profile": {
            str(degree): count
            for degree, count in sorted(
                degree_profile.items()
            )
        },
        "component_sizes": list(
            component_sizes(vertices, edges)
        ),
        "triangle_count": len(triangles),
        "triangles": [
            list(triangle)
            for triangle in triangles
        ],
        "edges": [
            list(edge)
            for edge in edges
        ],
        "graph6": graph6_string(graph),
        "line_petersen_graph6": graph6_string(
            line_petersen
        ),
        "isomorphic_to_line_petersen": (
            len(isomorphisms) > 0
        ),
        "isomorphism_count_to_line_petersen": (
            len(isomorphisms)
        ),
        "representative_isomorphism_to_line_petersen": (
            {
                str(source): target
                for source, target in sorted(
                    representative_isomorphism.items()
                )
            }
            if representative_isomorphism is not None
            else None
        ),
        "automorphism_group_order": len(
            automorphisms
        ),
        "automorphism_vertex_orbits": [
            list(orbit)
            for orbit in automorphism_vertex_orbits
        ],
        "edge_intersection_v4_fixed_profile_counts": [
            {
                "profile": [
                    [count, multiplicity]
                    for count, multiplicity in profile
                ],
                "edge_count": count,
            }
            for profile, count in sorted(
                edge_intersection_profile.items()
            )
        ],
        "classification_result": (
            "The graph on the fifteen conjugate C2^3 cubes, "
            "with adjacency defined by order-4 subgroup "
            "intersection, is a connected quartic graph with "
            "15 vertices, 30 edges, and 10 triangles. It is "
            "explicitly isomorphic to the line graph of the "
            "Petersen graph. Thus G15 is recovered intrinsically "
            "as the order-4 intersection graph of the fifteen "
            "native affine cubes in Aut(G30)."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "fifteen_cube_graph_constructed": True,
            "order4_intersection_adjacency_selected": True,
            "line_petersen_isomorphism_proved": True,
            "g15_intrinsic_cube_recovery_proved": True,
            "cube_to_native_g15_label_alignment_open": True,
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
    print("vertex_count:", payload["vertex_count"])
    print("edge_count:", payload["edge_count"])
    print("degree_profile:", payload["degree_profile"])
    print("component_sizes:", payload["component_sizes"])
    print("triangle_count:", payload["triangle_count"])
    print("graph6:", payload["graph6"])
    print(
        "line_petersen_graph6:",
        payload["line_petersen_graph6"],
    )
    print(
        "isomorphic_to_line_petersen:",
        payload["isomorphic_to_line_petersen"],
    )
    print(
        "isomorphism_count_to_line_petersen:",
        payload[
            "isomorphism_count_to_line_petersen"
        ],
    )
    print(
        "automorphism_group_order:",
        payload["automorphism_group_order"],
    )
    print(
        "automorphism_vertex_orbits:",
        payload["automorphism_vertex_orbits"],
    )
    print(
        "edge_intersection_v4_fixed_profile_counts:",
        payload[
            "edge_intersection_v4_fixed_profile_counts"
        ],
    )
    print(
        "classification_result:",
        payload["classification_result"],
    )


if __name__ == "__main__":
    main()
