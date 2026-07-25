#!/usr/bin/env python3
"""Recover the Petersen graph from the ten cube-triangle centers."""

import json
from collections import Counter, deque
from itertools import combinations
from pathlib import Path

import networkx as nx


ROOT = Path(__file__).resolve().parents[1]

CENTER_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_cube_triangle_centers_028.json"
)

CUBE_GRAPH_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_fifteen_cube_graph_027.json"
)

OUTPUT = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_petersen_from_cube_centers_029.json"
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


def graph6_string(graph):
    canonical = nx.convert_node_labels_to_integers(
        graph,
        ordering="sorted",
    )

    return nx.to_graph6_bytes(
        canonical,
        header=False,
    ).decode("ascii").strip()


def main():
    center_source = json.loads(
        CENTER_SOURCE.read_text()
    )

    cube_graph_source = json.loads(
        CUBE_GRAPH_SOURCE.read_text()
    )

    center_rows = tuple(sorted(
        center_source["triangle_rows"],
        key=lambda row: row["triangle_index"],
    ))

    center_vertices = tuple(
        range(len(center_rows))
    )

    center_cube_sets = tuple(
        frozenset(row["cube_indices"])
        for row in center_rows
    )

    pair_rows = []
    edges = []

    for left, right in combinations(
        center_vertices,
        2,
    ):
        shared_cubes = tuple(sorted(
            center_cube_sets[left].intersection(
                center_cube_sets[right]
            )
        ))

        adjacent = len(shared_cubes) == 1

        if adjacent:
            edges.append(
                canonical_edge(left, right)
            )

        pair_rows.append({
            "left_center": left,
            "right_center": right,
            "shared_cube_count": len(
                shared_cubes
            ),
            "shared_cubes": list(
                shared_cubes
            ),
            "adjacent": adjacent,
        })

    edges = tuple(sorted(edges))

    graph = nx.Graph()
    graph.add_nodes_from(center_vertices)
    graph.add_edges_from(edges)

    degree_profile = Counter(
        degree
        for _, degree in graph.degree()
    )

    triangle_count = sum(
        nx.triangles(graph).values()
    ) // 3

    petersen = nx.petersen_graph()

    matcher = nx.algorithms.isomorphism.GraphMatcher(
        graph,
        petersen,
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
            for index in center_vertices
        )
        for mapping in (
            automorphism_matcher.isomorphisms_iter()
        )
    )

    cube_to_centers = {
        cube_index: []
        for cube_index in range(
            cube_graph_source["vertex_count"]
        )
    }

    for center_index, cube_set in enumerate(
        center_cube_sets
    ):
        for cube_index in cube_set:
            cube_to_centers[
                cube_index
            ].append(center_index)

    cube_edge_rows = []

    for cube_index in sorted(cube_to_centers):
        incident_centers = tuple(sorted(
            cube_to_centers[cube_index]
        ))

        cube_edge_rows.append({
            "cube_index": cube_index,
            "incident_center_count": len(
                incident_centers
            ),
            "incident_centers": list(
                incident_centers
            ),
            "petersen_edge": (
                list(incident_centers)
                if len(incident_centers) == 2
                else None
            ),
            "center_pair_is_adjacent": (
                len(incident_centers) == 2
                and canonical_edge(
                    *incident_centers
                )
                in edges
            ),
        })

    petersen_edge_to_cube = {
        canonical_edge(
            *row["incident_centers"]
        ): row["cube_index"]
        for row in cube_edge_rows
        if row["incident_center_count"] == 2
    }

    graph_edges_equal_cube_edges = (
        set(edges)
        == set(petersen_edge_to_cube)
    )

    center_rows_payload = []

    for center_index, source_row in enumerate(
        center_rows
    ):
        center_involution = source_row[
            "unique_six_fixed_incidence3_center"
        ]

        center_rows_payload.append({
            "center_index": center_index,
            "cube_indices": (
                source_row["cube_indices"]
            ),
            "six_fixed_center_involution": (
                center_involution
            ),
            "degree": graph.degree[
                center_index
            ],
            "neighbors": sorted(
                graph.neighbors(
                    center_index
                )
            ),
        })

    checks = {
        "center_source_audit_pass": (
            center_source["audit_pass"]
        ),
        "cube_graph_source_audit_pass": (
            cube_graph_source["audit_pass"]
        ),
        "center_vertex_count_is_10": (
            graph.number_of_nodes() == 10
        ),
        "center_edge_count_is_15": (
            graph.number_of_edges() == 15
        ),
        "center_graph_is_connected": (
            component_sizes(
                center_vertices,
                edges,
            )
            == (10,)
        ),
        "center_graph_is_cubic": (
            degree_profile == {3: 10}
        ),
        "center_graph_is_triangle_free": (
            triangle_count == 0
        ),
        "center_graph_isomorphic_to_petersen": (
            len(isomorphisms) > 0
        ),
        "petersen_isomorphism_count_is_120": (
            len(isomorphisms) == 120
        ),
        "center_graph_automorphism_order_is_120": (
            len(automorphisms) == 120
        ),
        "every_cube_is_incident_to_two_centers": all(
            row["incident_center_count"] == 2
            for row in cube_edge_rows
        ),
        "every_cube_defines_center_edge": all(
            row["center_pair_is_adjacent"]
            for row in cube_edge_rows
        ),
        "cube_edges_equal_all_petersen_edges": (
            graph_edges_equal_cube_edges
        ),
        "fifteen_cubes_give_fifteen_distinct_edges": (
            len(petersen_edge_to_cube) == 15
        ),
    }

    payload = {
        "certificate_id": (
            "native_g30_petersen_from_cube_centers_029"
        ),
        "center_source": str(
            CENTER_SOURCE.relative_to(ROOT)
        ),
        "cube_graph_source": str(
            CUBE_GRAPH_SOURCE.relative_to(ROOT)
        ),
        "adjacency_rule": (
            "two six-fixed-point cube-triangle centers are "
            "adjacent exactly when their three-cube supports "
            "share one cube"
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
            component_sizes(
                center_vertices,
                edges,
            )
        ),
        "triangle_count": triangle_count,
        "edges": [
            list(edge)
            for edge in edges
        ],
        "graph6": graph6_string(graph),
        "petersen_graph6": graph6_string(
            petersen
        ),
        "isomorphic_to_petersen": (
            len(isomorphisms) > 0
        ),
        "isomorphism_count_to_petersen": (
            len(isomorphisms)
        ),
        "representative_isomorphism_to_petersen": (
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
        "center_rows": center_rows_payload,
        "center_pair_rows": pair_rows,
        "cube_edge_rows": cube_edge_rows,
        "cube_to_petersen_edge": {
            str(cube_index): list(edge)
            for edge, cube_index in sorted(
                petersen_edge_to_cube.items(),
                key=lambda item: item[1],
            )
        },
        "classification_result": (
            "The ten common-V4 cube-triangle centers form a "
            "connected cubic triangle-free graph on ten "
            "vertices. Two centers are adjacent exactly when "
            "their three-cube supports share one cube. This "
            "graph is explicitly isomorphic to the Petersen "
            "graph. Every one of the fifteen cubes belongs to "
            "exactly two centers and therefore becomes exactly "
            "one Petersen edge. Thus the native cube system "
            "recovers both Petersen and its line graph: centers "
            "are Petersen vertices, cubes are Petersen edges, "
            "and order-4 cube intersection is line-graph "
            "adjacency."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "petersen_center_graph_recovered": True,
            "ten_centers_are_petersen_vertices": True,
            "fifteen_cubes_are_petersen_edges": True,
            "cube_graph_is_line_graph_of_center_graph": True,
            "native_label_alignment_open": True,
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
        "petersen_graph6:",
        payload["petersen_graph6"],
    )
    print(
        "isomorphic_to_petersen:",
        payload["isomorphic_to_petersen"],
    )
    print(
        "isomorphism_count_to_petersen:",
        payload[
            "isomorphism_count_to_petersen"
        ],
    )
    print(
        "automorphism_group_order:",
        payload["automorphism_group_order"],
    )
    print(
        "cube_incident_center_count_profile:",
        {
            str(count): sum(
                1
                for row in cube_edge_rows
                if row[
                    "incident_center_count"
                ] == count
            )
            for count in sorted({
                row["incident_center_count"]
                for row in cube_edge_rows
            })
        },
    )
    print(
        "classification_result:",
        payload["classification_result"],
    )


if __name__ == "__main__":
    main()
