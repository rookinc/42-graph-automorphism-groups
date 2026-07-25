#!/usr/bin/env python3
"""Classify the hidden triangle-fiber kernel involution."""

import json
from collections import Counter, deque
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

GRAPH_SOURCE = (
    ROOT
    / "sources"
    / "native_g30_graph_input_001.json"
)

ANATOMY_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_group_anatomy_002.json"
)

STABILIZER_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_triangle_stabilizers_009.json"
)

CONJUGACY_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_triangle_fiber_conjugacy_011.json"
)

OUTPUT = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_triangle_kernel_involution_012.json"
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


def permutation_cycles(permutation):
    unseen = set(range(len(permutation)))
    cycles = []

    while unseen:
        start = min(unseen)
        cycle = []
        current = start

        while current in unseen:
            unseen.remove(current)
            cycle.append(current)
            current = permutation[current]

        cycles.append(tuple(cycle))

    return tuple(sorted(
        cycles,
        key=lambda cycle: (
            len(cycle),
            cycle,
        ),
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


def image_of_subset(subset, permutation):
    return tuple(sorted(
        permutation[vertex]
        for vertex in subset
    ))


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


def main():
    graph_source = json.loads(GRAPH_SOURCE.read_text())
    anatomy_source = json.loads(ANATOMY_SOURCE.read_text())
    stabilizer_source = json.loads(
        STABILIZER_SOURCE.read_text()
    )
    conjugacy_source = json.loads(
        CONJUGACY_SOURCE.read_text()
    )

    vertices = tuple(graph_source["vertices"])
    edges = tuple(
        tuple(sorted(edge))
        for edge in graph_source["edges"]
    )

    triangles = triangle_set(vertices, edges)

    first_triangle = tuple(
        conjugacy_source["first_triangle"]
    )

    second_triangle = tuple(
        conjugacy_source["second_triangle"]
    )

    fiber_vertices = frozenset(
        first_triangle + second_triangle
    )

    full_stabilizer = frozenset(
        tuple(element)
        for element in stabilizer_source[
            "full_triangle_stabilizer"
        ]["elements"]
    )

    identity = tuple(range(len(vertices)))

    fiber_kernel = frozenset(
        element
        for element in full_stabilizer
        if all(
            element[vertex] == vertex
            for vertex in fiber_vertices
        )
    )

    kernel_involution = next(
        element
        for element in fiber_kernel
        if element != identity
    )

    central_involution = next(
        tuple(element)
        for element in anatomy_source["center"]
        if tuple(element) != identity
    )

    cycles = permutation_cycles(kernel_involution)

    fixed_vertices = tuple(
        cycle[0]
        for cycle in cycles
        if len(cycle) == 1
    )

    transpositions = tuple(
        cycle
        for cycle in cycles
        if len(cycle) == 2
    )

    fixed_vertex_set = frozenset(fixed_vertices)

    fixed_edges = tuple(
        edge
        for edge in edges
        if edge[0] in fixed_vertex_set
        and edge[1] in fixed_vertex_set
    )

    setwise_fixed_edges = tuple(
        edge
        for edge in edges
        if tuple(sorted((
            kernel_involution[edge[0]],
            kernel_involution[edge[1]],
        )))
        == edge
    )

    pointwise_fixed_triangles = tuple(
        triangle
        for triangle in triangles
        if all(
            kernel_involution[vertex] == vertex
            for vertex in triangle
        )
    )

    setwise_fixed_triangles = tuple(
        triangle
        for triangle in triangles
        if image_of_subset(
            triangle,
            kernel_involution,
        )
        == triangle
    )

    triangle_orbits = []
    unseen_triangles = set(triangles)

    while unseen_triangles:
        triangle = min(unseen_triangles)
        partner = image_of_subset(
            triangle,
            kernel_involution,
        )

        orbit = tuple(sorted({
            triangle,
            partner,
        }))

        triangle_orbits.append(orbit)
        unseen_triangles -= set(orbit)

    cycle_length_profile = Counter(
        len(cycle)
        for cycle in cycles
    )

    fixed_vertex_triangle_incidence = Counter()

    for triangle in pointwise_fixed_triangles:
        for vertex in triangle:
            fixed_vertex_triangle_incidence[vertex] += 1

    commutes_with_central = (
        compose(
            kernel_involution,
            central_involution,
        )
        == compose(
            central_involution,
            kernel_involution,
        )
    )

    kernel_times_central = compose(
        kernel_involution,
        central_involution,
    )

    checks = {
        "source_stabilizer_audit_pass": (
            stabilizer_source["audit_pass"]
        ),
        "source_conjugacy_audit_pass": (
            conjugacy_source["audit_pass"]
        ),
        "fiber_kernel_order_is_2": (
            len(fiber_kernel) == 2
        ),
        "kernel_nonidentity_order_is_2": (
            permutation_order(kernel_involution) == 2
        ),
        "kernel_fixes_all_six_fiber_vertices": all(
            kernel_involution[vertex] == vertex
            for vertex in fiber_vertices
        ),
        "cycle_lengths_are_only_1_or_2": (
            set(cycle_length_profile) <= {1, 2}
        ),
        "cycle_lengths_account_for_30_vertices": (
            sum(
                length * count
                for length, count
                in cycle_length_profile.items()
            )
            == 30
        ),
        "both_fiber_triangles_are_pointwise_fixed": (
            first_triangle in pointwise_fixed_triangles
            and second_triangle in pointwise_fixed_triangles
        ),
        "pointwise_fixed_triangle_count_is_2": (
            len(pointwise_fixed_triangles) == 2
        ),
        "setwise_fixed_triangle_count_is_8": (
            len(setwise_fixed_triangles) == 8
        ),
        "six_additional_triangles_are_setwise_fixed": (
            len(setwise_fixed_triangles)
            - len(pointwise_fixed_triangles)
            == 6
        ),
        "kernel_commutes_with_central_deck": (
            commutes_with_central
        ),
        "kernel_is_not_central_deck": (
            kernel_involution != central_involution
        ),
        "kernel_times_central_has_order_2": (
            permutation_order(kernel_times_central) == 2
        ),
    }

    payload = {
        "certificate_id": (
            "native_g30_triangle_kernel_involution_012"
        ),
        "graph_source": str(
            GRAPH_SOURCE.relative_to(ROOT)
        ),
        "anatomy_source": str(
            ANATOMY_SOURCE.relative_to(ROOT)
        ),
        "stabilizer_source": str(
            STABILIZER_SOURCE.relative_to(ROOT)
        ),
        "conjugacy_source": str(
            CONJUGACY_SOURCE.relative_to(ROOT)
        ),
        "kernel_involution": list(kernel_involution),
        "kernel_involution_order": (
            permutation_order(kernel_involution)
        ),
        "cycle_length_profile": {
            str(length): count
            for length, count in sorted(
                cycle_length_profile.items()
            )
        },
        "fixed_vertex_count": len(fixed_vertices),
        "fixed_vertices": list(fixed_vertices),
        "transposition_count": len(transpositions),
        "transpositions": [
            list(cycle)
            for cycle in transpositions
        ],
        "fixed_edge_count": len(fixed_edges),
        "fixed_edges": [
            list(edge)
            for edge in fixed_edges
        ],
        "setwise_fixed_edge_count": len(
            setwise_fixed_edges
        ),
        "fixed_subgraph_component_sizes": list(
            component_sizes(
                fixed_vertices,
                fixed_edges,
            )
        ),
        "pointwise_fixed_triangle_count": len(
            pointwise_fixed_triangles
        ),
        "pointwise_fixed_triangles": [
            list(triangle)
            for triangle in pointwise_fixed_triangles
        ],
        "setwise_fixed_triangle_count": len(
            setwise_fixed_triangles
        ),
        "setwise_fixed_triangles": [
            list(triangle)
            for triangle in setwise_fixed_triangles
        ],
        "setwise_nonpointwise_fixed_triangle_count": (
            len(setwise_fixed_triangles)
            - len(pointwise_fixed_triangles)
        ),
        "triangle_orbit_size_profile": {
            str(size): count
            for size, count in sorted(
                Counter(
                    len(orbit)
                    for orbit in triangle_orbits
                ).items()
            )
        },
        "commutes_with_central_deck": (
            commutes_with_central
        ),
        "kernel_times_central_order": (
            permutation_order(kernel_times_central)
        ),
        "classification_result": (
            "The hidden order-2 kernel fixes the entire "
            "six-vertex triangle fiber pointwise. Its fixed "
            "subgraph is exactly two disjoint triangles. It "
            "fixes two triangles pointwise and six additional "
            "triangles setwise, while exchanging the remaining "
            "12 triangles in six pairs. It commutes with but is "
            "distinct from the central deck involution."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "kernel_cycle_structure_classified": True,
            "kernel_fixed_subgraph_classified": True,
            "kernel_triangle_action_classified": True,
            "kernel_geometric_name_open": True,
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
        "cycle_length_profile:",
        payload["cycle_length_profile"],
    )
    print(
        "fixed_vertex_count:",
        payload["fixed_vertex_count"],
    )
    print(
        "transposition_count:",
        payload["transposition_count"],
    )
    print(
        "fixed_edge_count:",
        payload["fixed_edge_count"],
    )
    print(
        "fixed_subgraph_component_sizes:",
        payload["fixed_subgraph_component_sizes"],
    )
    print(
        "pointwise_fixed_triangle_count:",
        payload["pointwise_fixed_triangle_count"],
    )
    print(
        "triangle_orbit_size_profile:",
        payload["triangle_orbit_size_profile"],
    )
    print(
        "commutes_with_central_deck:",
        payload["commutes_with_central_deck"],
    )
    print(
        "classification_result:",
        payload["classification_result"],
    )


if __name__ == "__main__":
    main()
