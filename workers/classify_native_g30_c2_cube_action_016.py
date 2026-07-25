#!/usr/bin/env python3
"""Classify the C2^3 action on native G30 vertices and triangles."""

import json
from collections import Counter
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

GRAPH_SOURCE = (
    ROOT
    / "sources"
    / "native_g30_graph_input_001.json"
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
    / "native_g30_c2_cube_action_016.json"
)


def compose(left, right):
    return tuple(
        left[right[index]]
        for index in range(len(left))
    )


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


def triangle_set(vertices, edges):
    edge_set = frozenset(
        tuple(sorted(edge))
        for edge in edges
    )

    return tuple(sorted(
        triple
        for triple in combinations(vertices, 3)
        if all(
            tuple(sorted(edge)) in edge_set
            for edge in combinations(triple, 2)
        )
    ))


def set_orbits(objects, group, image_function):
    unseen = set(objects)
    orbits = []

    while unseen:
        representative = min(unseen)

        orbit = frozenset(
            image_function(representative, element)
            for element in group
        )

        orbits.append(tuple(sorted(orbit)))
        unseen -= set(orbit)

    return tuple(sorted(
        orbits,
        key=lambda orbit: (
            len(orbit),
            orbit,
        ),
    ))


def vertex_stabilizer(vertex, group):
    return frozenset(
        element
        for element in group
        if element[vertex] == vertex
    )


def subset_stabilizer(subset, group):
    return frozenset(
        element
        for element in group
        if image_of_subset(subset, element) == subset
    )


def pointwise_subset_stabilizer(subset, group):
    return frozenset(
        element
        for element in group
        if all(
            element[vertex] == vertex
            for vertex in subset
        )
    )


def induced_edges(vertex_set, edges):
    vertex_set = frozenset(vertex_set)

    return tuple(
        edge
        for edge in edges
        if edge[0] in vertex_set
        and edge[1] in vertex_set
    )


def crossing_edges(left_vertices, right_vertices, edges):
    left_vertices = frozenset(left_vertices)
    right_vertices = frozenset(right_vertices)

    return tuple(
        edge
        for edge in edges
        if (
            edge[0] in left_vertices
            and edge[1] in right_vertices
        )
        or (
            edge[1] in left_vertices
            and edge[0] in right_vertices
        )
    )


def fixed_point_count(element):
    return sum(
        1
        for vertex, image in enumerate(element)
        if vertex == image
    )


def main():
    graph_source = json.loads(GRAPH_SOURCE.read_text())
    group_source = json.loads(GROUP_SOURCE.read_text())

    vertices = tuple(graph_source["vertices"])
    edges = tuple(
        tuple(sorted(edge))
        for edge in graph_source["edges"]
    )

    triangles = triangle_set(vertices, edges)

    group = frozenset(
        tuple(element)
        for element in group_source["elements"]
    )

    identity = tuple(range(len(vertices)))

    nonidentity = tuple(sorted(
        element
        for element in group
        if element != identity
    ))

    vertex_orbits = set_orbits(
        vertices,
        group,
        lambda vertex, element: element[vertex],
    )

    triangle_orbits = set_orbits(
        triangles,
        group,
        image_of_subset,
    )

    vertex_rows = []

    for index, orbit in enumerate(vertex_orbits):
        representative = orbit[0]
        stabilizer = vertex_stabilizer(
            representative,
            group,
        )

        orbit_edges = induced_edges(orbit, edges)

        fixing_involutions = tuple(
            element
            for element in nonidentity
            if all(
                element[vertex] == vertex
                for vertex in orbit
            )
        )

        setwise_elements = tuple(
            element
            for element in group
            if {
                element[vertex]
                for vertex in orbit
            }
            == set(orbit)
        )

        vertex_rows.append({
            "orbit_index": index,
            "representative": representative,
            "orbit_size": len(orbit),
            "vertices": list(orbit),
            "stabilizer_order": len(stabilizer),
            "pointwise_stabilizer_order": len(
                fixing_involutions
            ) + 1,
            "setwise_stabilizer_order": len(
                setwise_elements
            ),
            "induced_edge_count": len(orbit_edges),
            "induced_edges": [
                list(edge)
                for edge in orbit_edges
            ],
            "fixed_point_profiles_of_stabilizer": {
                str(count): multiplicity
                for count, multiplicity in sorted(
                    Counter(
                        fixed_point_count(element)
                        for element in stabilizer
                        if element != identity
                    ).items()
                )
            },
        })

    triangle_rows = []

    for index, orbit in enumerate(triangle_orbits):
        representative = orbit[0]

        setwise_stabilizer = subset_stabilizer(
            representative,
            group,
        )

        pointwise_stabilizer = (
            pointwise_subset_stabilizer(
                representative,
                group,
            )
        )

        support = tuple(sorted({
            vertex
            for triangle in orbit
            for vertex in triangle
        }))

        support_edges = induced_edges(
            support,
            edges,
        )

        triangle_rows.append({
            "orbit_index": index,
            "representative": list(representative),
            "orbit_size": len(orbit),
            "triangles": [
                list(triangle)
                for triangle in orbit
            ],
            "setwise_stabilizer_order": len(
                setwise_stabilizer
            ),
            "pointwise_stabilizer_order": len(
                pointwise_stabilizer
            ),
            "support_vertex_count": len(support),
            "support_vertices": list(support),
            "support_induced_edge_count": len(
                support_edges
            ),
        })

    vertex_orbit_pair_rows = []

    for left_index, right_index in combinations(
        range(len(vertex_orbits)),
        2,
    ):
        left_orbit = vertex_orbits[left_index]
        right_orbit = vertex_orbits[right_index]

        crossings = crossing_edges(
            left_orbit,
            right_orbit,
            edges,
        )

        if not crossings:
            continue

        vertex_orbit_pair_rows.append({
            "left_orbit_index": left_index,
            "right_orbit_index": right_index,
            "left_orbit_size": len(left_orbit),
            "right_orbit_size": len(right_orbit),
            "crossing_edge_count": len(crossings),
            "crossing_edges": [
                list(edge)
                for edge in crossings
            ],
        })

    vertex_orbit_size_profile = Counter(
        len(orbit)
        for orbit in vertex_orbits
    )

    triangle_orbit_size_profile = Counter(
        len(orbit)
        for orbit in triangle_orbits
    )

    involution_fixed_point_profile = Counter(
        fixed_point_count(element)
        for element in nonidentity
    )

    checks = {
        "source_group_audit_pass": (
            group_source["audit_pass"]
        ),
        "group_order_is_8": len(group) == 8,
        "all_nonidentity_elements_are_involutions": all(
            permutation_order(element) == 2
            for element in nonidentity
        ),
        "vertex_orbits_account_for_30_vertices": (
            sum(
                size * count
                for size, count
                in vertex_orbit_size_profile.items()
            )
            == 30
        ),
        "triangle_orbits_account_for_20_triangles": (
            sum(
                size * count
                for size, count
                in triangle_orbit_size_profile.items()
            )
            == 20
        ),
        "vertex_orbit_stabilizer_formula_holds": all(
            row["orbit_size"]
            * row["stabilizer_order"]
            == 8
            for row in vertex_rows
        ),
        "triangle_orbit_stabilizer_formula_holds": all(
            row["orbit_size"]
            * row["setwise_stabilizer_order"]
            == 8
            for row in triangle_rows
        ),
        "all_graph_edges_accounted_for": (
            sum(
                row["induced_edge_count"]
                for row in vertex_rows
            )
            + sum(
                row["crossing_edge_count"]
                for row in vertex_orbit_pair_rows
            )
            == len(edges)
        ),
    }

    payload = {
        "certificate_id": (
            "native_g30_c2_cube_action_016"
        ),
        "graph_source": str(
            GRAPH_SOURCE.relative_to(ROOT)
        ),
        "group_source": str(
            GROUP_SOURCE.relative_to(ROOT)
        ),
        "group_order": len(group),
        "vertex_count": len(vertices),
        "edge_count": len(edges),
        "triangle_count": len(triangles),
        "involution_fixed_point_count_profile": {
            str(count): multiplicity
            for count, multiplicity in sorted(
                involution_fixed_point_profile.items()
            )
        },
        "vertex_orbit_count": len(vertex_orbits),
        "vertex_orbit_size_profile": {
            str(size): count
            for size, count in sorted(
                vertex_orbit_size_profile.items()
            )
        },
        "vertex_orbits": vertex_rows,
        "vertex_orbit_crossings": (
            vertex_orbit_pair_rows
        ),
        "triangle_orbit_count": len(
            triangle_orbits
        ),
        "triangle_orbit_size_profile": {
            str(size): count
            for size, count in sorted(
                triangle_orbit_size_profile.items()
            )
        },
        "triangle_orbits": triangle_rows,
        "classification_result": (
            "The explicit C2^3 action has been decomposed into "
            "vertex and triangle orbits without assuming their "
            "sizes or induced geometry in advance."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "c2_cube_vertex_action_classified": True,
            "c2_cube_triangle_action_classified": True,
            "orbit_incidence_recorded": True,
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
        "involution_fixed_point_count_profile:",
        payload[
            "involution_fixed_point_count_profile"
        ],
    )
    print(
        "vertex_orbit_count:",
        payload["vertex_orbit_count"],
    )
    print(
        "vertex_orbit_size_profile:",
        payload["vertex_orbit_size_profile"],
    )
    print(
        "triangle_orbit_count:",
        payload["triangle_orbit_count"],
    )
    print(
        "triangle_orbit_size_profile:",
        payload["triangle_orbit_size_profile"],
    )

    for row in vertex_rows:
        print(
            "vertex orbit",
            row["orbit_index"],
            "size:",
            row["orbit_size"],
            "stabilizer:",
            row["stabilizer_order"],
            "induced edges:",
            row["induced_edge_count"],
            "vertices:",
            row["vertices"],
        )

    for row in triangle_rows:
        print(
            "triangle orbit",
            row["orbit_index"],
            "size:",
            row["orbit_size"],
            "stabilizer:",
            row["setwise_stabilizer_order"],
            "support:",
            row["support_vertex_count"],
        )

    print(
        "classification_result:",
        payload["classification_result"],
    )


if __name__ == "__main__":
    main()
