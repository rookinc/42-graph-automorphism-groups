#!/usr/bin/env python3
"""Derive the weighted quotient on the six C2^3 vertex orbits."""

import json
from collections import Counter, deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

GRAPH_SOURCE = (
    ROOT
    / "sources"
    / "native_g30_graph_input_001.json"
)

ACTION_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_c2_cube_action_016.json"
)

OUTPUT = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_c2_cube_orbit_quotient_017.json"
)


def component_sizes(vertices, edges):
    adjacency = {
        vertex: set()
        for vertex in vertices
    }

    for left, right in edges:
        if left == right:
            continue

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


def main():
    graph_source = json.loads(GRAPH_SOURCE.read_text())
    action_source = json.loads(ACTION_SOURCE.read_text())

    vertices = tuple(graph_source["vertices"])

    edges = tuple(
        tuple(sorted(edge))
        for edge in graph_source["edges"]
    )

    orbit_rows = tuple(
        sorted(
            action_source["vertex_orbits"],
            key=lambda row: row["orbit_index"],
        )
    )

    orbit_count = len(orbit_rows)
    quotient_vertices = tuple(range(orbit_count))

    vertex_to_orbit = {}

    for row in orbit_rows:
        orbit_index = row["orbit_index"]

        for vertex in row["vertices"]:
            vertex_to_orbit[vertex] = orbit_index

    edge_block_multiplicity = Counter()

    for left, right in edges:
        left_orbit = vertex_to_orbit[left]
        right_orbit = vertex_to_orbit[right]

        block = tuple(sorted((
            left_orbit,
            right_orbit,
        )))

        edge_block_multiplicity[block] += 1

    quotient_edges = tuple(sorted(
        block
        for block, multiplicity
        in edge_block_multiplicity.items()
        if block[0] != block[1]
        and multiplicity > 0
    ))

    quotient_loops = tuple(sorted(
        block[0]
        for block, multiplicity
        in edge_block_multiplicity.items()
        if block[0] == block[1]
        and multiplicity > 0
    ))

    block_rows = []

    for left_orbit in quotient_vertices:
        left_size = orbit_rows[left_orbit]["orbit_size"]

        for right_orbit in range(
            left_orbit,
            orbit_count,
        ):
            right_size = orbit_rows[
                right_orbit
            ]["orbit_size"]

            multiplicity = edge_block_multiplicity.get(
                (left_orbit, right_orbit),
                0,
            )

            if multiplicity == 0:
                continue

            if left_orbit == right_orbit:
                neighbor_count_from_left = (
                    2 * multiplicity
                ) // left_size

                neighbor_count_from_right = (
                    neighbor_count_from_left
                )
            else:
                neighbor_count_from_left = (
                    multiplicity // left_size
                )

                neighbor_count_from_right = (
                    multiplicity // right_size
                )

            block_rows.append({
                "left_orbit": left_orbit,
                "right_orbit": right_orbit,
                "left_size": left_size,
                "right_size": right_size,
                "edge_multiplicity": multiplicity,
                "neighbors_per_left_vertex": (
                    neighbor_count_from_left
                ),
                "neighbors_per_right_vertex": (
                    neighbor_count_from_right
                ),
                "internal_block": (
                    left_orbit == right_orbit
                ),
            })

    orbit_degree_contributions = {
        orbit_index: []
        for orbit_index in quotient_vertices
    }

    for row in block_rows:
        left = row["left_orbit"]
        right = row["right_orbit"]

        if left == right:
            orbit_degree_contributions[left].append({
                "neighbor_orbit": left,
                "neighbors_per_vertex": row[
                    "neighbors_per_left_vertex"
                ],
            })
        else:
            orbit_degree_contributions[left].append({
                "neighbor_orbit": right,
                "neighbors_per_vertex": row[
                    "neighbors_per_left_vertex"
                ],
            })

            orbit_degree_contributions[right].append({
                "neighbor_orbit": left,
                "neighbors_per_vertex": row[
                    "neighbors_per_right_vertex"
                ],
            })

    orbit_summary_rows = []

    for orbit_index in quotient_vertices:
        contributions = sorted(
            orbit_degree_contributions[orbit_index],
            key=lambda row: row["neighbor_orbit"],
        )

        orbit_summary_rows.append({
            "orbit_index": orbit_index,
            "orbit_size": orbit_rows[
                orbit_index
            ]["orbit_size"],
            "vertices": orbit_rows[
                orbit_index
            ]["vertices"],
            "induced_edge_count": orbit_rows[
                orbit_index
            ]["induced_edge_count"],
            "degree_contributions": contributions,
            "degree_sum": sum(
                row["neighbors_per_vertex"]
                for row in contributions
            ),
        })

    simple_degree = Counter()

    for left, right in quotient_edges:
        simple_degree[left] += 1
        simple_degree[right] += 1

    edge_multiplicity_profile = Counter(
        edge_block_multiplicity[edge]
        for edge in quotient_edges
    )

    internal_edge_profile = Counter(
        edge_block_multiplicity[(orbit, orbit)]
        for orbit in quotient_loops
    )

    checks = {
        "source_action_audit_pass": (
            action_source["audit_pass"]
        ),
        "orbit_count_is_6": orbit_count == 6,
        "all_30_vertices_assigned_once": (
            len(vertex_to_orbit) == 30
            and set(vertex_to_orbit) == set(vertices)
        ),
        "all_60_edges_accounted_for": (
            sum(edge_block_multiplicity.values())
            == len(edges)
            == 60
        ),
        "all_block_divisions_are_integral": all(
            (
                row["edge_multiplicity"]
                * (
                    2
                    if row["internal_block"]
                    else 1
                )
            )
            % row["left_size"]
            == 0
            and (
                row["edge_multiplicity"]
                * (
                    2
                    if row["internal_block"]
                    else 1
                )
            )
            % row["right_size"]
            == 0
            for row in block_rows
        ),
        "every_orbit_has_degree_sum_4": all(
            row["degree_sum"] == 4
            for row in orbit_summary_rows
        ),
        "simple_orbit_quotient_is_connected": (
            component_sizes(
                quotient_vertices,
                quotient_edges,
            )
            == (6,)
        ),
    }

    payload = {
        "certificate_id": (
            "native_g30_c2_cube_orbit_quotient_017"
        ),
        "graph_source": str(
            GRAPH_SOURCE.relative_to(ROOT)
        ),
        "action_source": str(
            ACTION_SOURCE.relative_to(ROOT)
        ),
        "original_vertex_count": len(vertices),
        "original_edge_count": len(edges),
        "orbit_count": orbit_count,
        "orbit_size_profile": (
            action_source["vertex_orbit_size_profile"]
        ),
        "quotient_vertex_count": orbit_count,
        "quotient_edge_count_without_loops": len(
            quotient_edges
        ),
        "quotient_loop_count": len(
            quotient_loops
        ),
        "quotient_edges": [
            list(edge)
            for edge in quotient_edges
        ],
        "quotient_loop_orbits": list(
            quotient_loops
        ),
        "simple_quotient_component_sizes": list(
            component_sizes(
                quotient_vertices,
                quotient_edges,
            )
        ),
        "simple_quotient_degree_profile": {
            str(degree): count
            for degree, count in sorted(
                Counter(
                    simple_degree.values()
                ).items()
            )
        },
        "cross_orbit_edge_multiplicity_profile": {
            str(multiplicity): count
            for multiplicity, count in sorted(
                edge_multiplicity_profile.items()
            )
        },
        "internal_edge_count_profile": {
            str(count): multiplicity
            for count, multiplicity in sorted(
                internal_edge_profile.items()
            )
        },
        "edge_blocks": block_rows,
        "orbit_summaries": orbit_summary_rows,
        "classification_result": (
            "The six C2^3 vertex orbits form a connected "
            "weighted quotient. Every orbit receives exactly "
            "four neighbors per vertex after internal and "
            "cross-orbit edge contributions are normalized."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "weighted_orbit_quotient_derived": True,
            "orbit_degree_law_derived": True,
            "quotient_graph_named_structure_open": True,
            "canonical_cube_coordinate_assignment_open": True,
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
        "orbit_size_profile:",
        payload["orbit_size_profile"],
    )
    print(
        "quotient_edges:",
        payload["quotient_edges"],
    )
    print(
        "quotient_loop_orbits:",
        payload["quotient_loop_orbits"],
    )
    print(
        "simple_quotient_degree_profile:",
        payload["simple_quotient_degree_profile"],
    )
    print(
        "cross_orbit_edge_multiplicity_profile:",
        payload[
            "cross_orbit_edge_multiplicity_profile"
        ],
    )

    for row in orbit_summary_rows:
        print(
            "orbit",
            row["orbit_index"],
            "size:",
            row["orbit_size"],
            "degree sum:",
            row["degree_sum"],
            "contributions:",
            row["degree_contributions"],
        )

    print(
        "classification_result:",
        payload["classification_result"],
    )


if __name__ == "__main__":
    main()
