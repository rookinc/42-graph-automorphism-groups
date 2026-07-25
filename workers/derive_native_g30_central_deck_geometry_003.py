#!/usr/bin/env python3
"""Recover the central deck geometry of native G30."""

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
    / "native_g30_full_automorphism_action_001.json"
)

ANATOMY_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_group_anatomy_002.json"
)

OUTPUT = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_central_deck_geometry_003.json"
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


def generated_subgroup(generators, identity):
    expanded = set(generators)

    expanded.update(
        inverse(generator)
        for generator in generators
    )

    subgroup = {identity}
    queue = deque([identity])

    while queue:
        current = queue.popleft()

        for generator in expanded:
            product = compose(generator, current)

            if product in subgroup:
                continue

            subgroup.add(product)
            queue.append(product)

    return frozenset(subgroup)


def permutation_order(permutation):
    identity = tuple(range(len(permutation)))
    current = identity
    order = 0

    while True:
        order += 1
        current = compose(permutation, current)

        if current == identity:
            return order


def connected_component_sizes(vertices, edges):
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
        component = {start}
        queue = deque([start])
        unseen.remove(start)

        while queue:
            current = queue.popleft()

            for neighbor in adjacency[current]:
                if neighbor not in unseen:
                    continue

                unseen.remove(neighbor)
                component.add(neighbor)
                queue.append(neighbor)

        sizes.append(len(component))

    return tuple(sorted(sizes, reverse=True))


def triangle_count(vertices, edges):
    adjacency = {
        vertex: set()
        for vertex in vertices
    }

    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)

    count = 0

    for left in vertices:
        for middle in adjacency[left]:
            if middle <= left:
                continue

            for right in adjacency[left].intersection(
                adjacency[middle]
            ):
                if right > middle:
                    count += 1

    return count


def main():
    graph_source = json.loads(GRAPH_SOURCE.read_text())
    action_source = json.loads(ACTION_SOURCE.read_text())
    anatomy_source = json.loads(ANATOMY_SOURCE.read_text())

    vertices = tuple(graph_source["vertices"])
    edges = tuple(
        tuple(edge)
        for edge in graph_source["edges"]
    )

    group = frozenset(
        tuple(row["permutation"])
        for row in action_source["automorphisms"]
    )

    center = frozenset(
        tuple(permutation)
        for permutation in anatomy_source["center"]
    )

    identity = tuple(range(len(vertices)))

    central_involution = next(
        permutation
        for permutation in center
        if permutation != identity
    )

    central_orbits = []
    unseen = set(vertices)

    while unseen:
        vertex = min(unseen)
        orbit = tuple(
            sorted({
                vertex,
                central_involution[vertex],
            })
        )

        central_orbits.append(orbit)
        unseen -= set(orbit)

    central_orbits = tuple(sorted(central_orbits))

    vertex_to_orbit = {}

    for orbit_index, orbit in enumerate(central_orbits):
        for vertex in orbit:
            vertex_to_orbit[vertex] = orbit_index

    quotient_edges_with_multiplicity = []

    for left, right in edges:
        quotient_left = vertex_to_orbit[left]
        quotient_right = vertex_to_orbit[right]

        quotient_edges_with_multiplicity.append(
            tuple(sorted((
                quotient_left,
                quotient_right,
            )))
        )

    quotient_edge_multiplicity = Counter(
        quotient_edges_with_multiplicity
    )

    quotient_edges = tuple(
        sorted(quotient_edge_multiplicity)
    )

    quotient_vertices = tuple(
        range(len(central_orbits))
    )

    quotient_degree = Counter()

    for left, right in quotient_edges:
        quotient_degree[left] += 1
        quotient_degree[right] += 1

    complement_generators = tuple(
        tuple(generator)
        for generator in anatomy_source[
            "complement_generators"
        ]
    )

    complement = generated_subgroup(
        complement_generators,
        identity,
    )

    full_stabilizer_0 = frozenset(
        permutation
        for permutation in group
        if permutation[0] == 0
    )

    complement_stabilizer_0 = frozenset(
        permutation
        for permutation in complement
        if permutation[0] == 0
    )

    complement_orbit_0 = frozenset(
        permutation[0]
        for permutation in complement
    )

    complement_stabilizer_profile = Counter(
        permutation_order(permutation)
        for permutation in complement_stabilizer_0
    )

    central_pair_of_0 = central_involution[0]

    central_pair_swap_count = sum(
        1
        for orbit in central_orbits
        if central_involution[orbit[0]] == orbit[1]
        and central_involution[orbit[1]] == orbit[0]
    )

    checks = {
        "source_action_audit_pass": (
            action_source["audit_pass"]
        ),
        "source_anatomy_audit_pass": (
            anatomy_source["audit_pass"]
        ),
        "center_order_is_2": len(center) == 2,
        "central_nonidentity_order_is_2": (
            permutation_order(central_involution) == 2
        ),
        "central_involution_has_no_fixed_points": all(
            central_involution[vertex] != vertex
            for vertex in vertices
        ),
        "central_orbit_count_is_15": (
            len(central_orbits) == 15
        ),
        "all_central_orbits_have_size_2": all(
            len(orbit) == 2
            for orbit in central_orbits
        ),
        "central_involution_swaps_all_15_pairs": (
            central_pair_swap_count == 15
        ),
        "no_quotient_loops": all(
            left != right
            for left, right in quotient_edges
        ),
        "quotient_vertex_count_is_15": (
            len(quotient_vertices) == 15
        ),
        "quotient_edge_count_is_30": (
            len(quotient_edges) == 30
        ),
        "every_quotient_edge_has_multiplicity_2": all(
            multiplicity == 2
            for multiplicity
            in quotient_edge_multiplicity.values()
        ),
        "quotient_is_quartic": (
            set(quotient_degree.values()) == {4}
            and len(quotient_degree) == 15
        ),
        "quotient_is_connected": (
            connected_component_sizes(
                quotient_vertices,
                quotient_edges,
            )
            == (15,)
        ),
        "quotient_triangle_count_is_10": (
            triangle_count(
                quotient_vertices,
                quotient_edges,
            )
            == 10
        ),
        "complement_order_is_120": (
            len(complement) == 120
        ),
        "complement_is_vertex_transitive": (
            len(complement_orbit_0) == 30
        ),
        "full_vertex_stabilizer_order_is_8": (
            len(full_stabilizer_0) == 8
        ),
        "complement_vertex_stabilizer_order_is_4": (
            len(complement_stabilizer_0) == 4
        ),
        "complement_stabilizer_is_v4": (
            dict(sorted(
                complement_stabilizer_profile.items()
            ))
            == {1: 1, 2: 3}
        ),
        "central_involution_not_in_full_stabilizer": (
            central_involution not in full_stabilizer_0
        ),
        "central_involution_maps_0_to_partner": (
            central_pair_of_0
            == next(
                vertex
                for vertex in central_orbits[
                    vertex_to_orbit[0]
                ]
                if vertex != 0
            )
        ),
    }

    payload = {
        "certificate_id": (
            "native_g30_central_deck_geometry_003"
        ),
        "graph_source": str(
            GRAPH_SOURCE.relative_to(ROOT)
        ),
        "action_source": str(
            ACTION_SOURCE.relative_to(ROOT)
        ),
        "anatomy_source": str(
            ANATOMY_SOURCE.relative_to(ROOT)
        ),
        "central_involution": list(central_involution),
        "central_involution_order": (
            permutation_order(central_involution)
        ),
        "central_involution_fixed_point_count": sum(
            1
            for vertex in vertices
            if central_involution[vertex] == vertex
        ),
        "central_pair_orbits": [
            list(orbit)
            for orbit in central_orbits
        ],
        "central_pair_orbit_count": len(central_orbits),
        "quotient_vertex_count": len(quotient_vertices),
        "quotient_edge_count": len(quotient_edges),
        "quotient_edges": [
            list(edge)
            for edge in quotient_edges
        ],
        "quotient_edge_multiplicity_profile": {
            str(multiplicity): count
            for multiplicity, count in sorted(
                Counter(
                    quotient_edge_multiplicity.values()
                ).items()
            )
        },
        "quotient_degree_profile": sorted(
            set(quotient_degree.values())
        ),
        "quotient_component_sizes": list(
            connected_component_sizes(
                quotient_vertices,
                quotient_edges,
            )
        ),
        "quotient_triangle_count": triangle_count(
            quotient_vertices,
            quotient_edges,
        ),
        "full_vertex_stabilizer_order": len(
            full_stabilizer_0
        ),
        "complement_order": len(complement),
        "complement_vertex_orbit_0_size": len(
            complement_orbit_0
        ),
        "complement_vertex_stabilizer_order": len(
            complement_stabilizer_0
        ),
        "complement_vertex_stabilizer_profile": {
            str(order): count
            for order, count in sorted(
                complement_stabilizer_profile.items()
            )
        },
        "homogeneous_action_result": (
            "30-point transitive S5 action with V4 stabilizer"
        ),
        "deck_geometry_result": (
            "central C2 is the fixed-point-free "
            "G30-to-G15 deck action"
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "central_deck_action_derived": True,
            "s5_complement_action_derived": True,
            "v4_stabilizer_derived_abstractly": True,
            "v4_mixed_label_proved": False,
            "quotient_explicitly_identified_as_line_petersen": False,
            "triangle_action_analyzed": False,
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
        "central_fixed_points:",
        payload["central_involution_fixed_point_count"],
    )
    print(
        "central_pair_orbits:",
        payload["central_pair_orbit_count"],
    )
    print(
        "quotient:",
        payload["quotient_vertex_count"],
        "vertices,",
        payload["quotient_edge_count"],
        "edges",
    )
    print(
        "quotient_triangle_count:",
        payload["quotient_triangle_count"],
    )
    print(
        "complement_order:",
        payload["complement_order"],
    )
    print(
        "complement_vertex_orbit_0_size:",
        payload["complement_vertex_orbit_0_size"],
    )
    print(
        "complement_vertex_stabilizer_order:",
        payload["complement_vertex_stabilizer_order"],
    )
    print(
        "complement_vertex_stabilizer_profile:",
        payload[
            "complement_vertex_stabilizer_profile"
        ],
    )
    print(
        "deck_geometry_result:",
        payload["deck_geometry_result"],
    )


if __name__ == "__main__":
    main()
