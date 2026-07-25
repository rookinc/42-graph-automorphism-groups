#!/usr/bin/env python3
"""Classify the simple six-vertex C2^3 orbit skeleton."""

import json
from collections import Counter, deque
from itertools import permutations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_c2_cube_orbit_quotient_017.json"
)

OUTPUT = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_c2_orbit_skeleton_018.json"
)


def canonical_edge(left, right):
    return tuple(sorted((left, right)))


def adjacency(vertices, edges):
    result = {
        vertex: set()
        for vertex in vertices
    }

    for left, right in edges:
        result[left].add(right)
        result[right].add(left)

    return result


def connected_component_sizes(vertices, edges):
    graph = adjacency(vertices, edges)
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

            for neighbor in graph[current]:
                if neighbor not in unseen:
                    continue

                unseen.remove(neighbor)
                queue.append(neighbor)

        sizes.append(size)

    return tuple(sorted(sizes, reverse=True))


def cycle_rank(vertices, edges):
    components = len(
        connected_component_sizes(vertices, edges)
    )

    return len(edges) - len(vertices) + components


def permutation_order(permutation):
    identity = tuple(range(len(permutation)))
    current = identity
    order = 0

    while True:
        order += 1
        current = tuple(
            permutation[current[index]]
            for index in range(len(permutation))
        )

        if current == identity:
            return order


def enumerate_automorphisms(vertices, edges):
    edge_set = frozenset(edges)
    degree = Counter()

    for left, right in edges:
        degree[left] += 1
        degree[right] += 1

    rows = []

    for permutation in permutations(vertices):
        if any(
            degree[vertex] != degree[permutation[vertex]]
            for vertex in vertices
        ):
            continue

        mapped_edges = frozenset(
            canonical_edge(
                permutation[left],
                permutation[right],
            )
            for left, right in edges
        )

        if mapped_edges == edge_set:
            rows.append(tuple(permutation))

    return tuple(sorted(rows))


def graph6_string(vertices, edges):
    if len(vertices) > 62:
        raise ValueError("graph6 helper supports at most 62 vertices")

    bits = []

    for right in range(1, len(vertices)):
        for left in range(right):
            bits.append(
                1
                if canonical_edge(left, right) in edges
                else 0
            )

    while len(bits) % 6:
        bits.append(0)

    encoded = [
        chr(len(vertices) + 63)
    ]

    for index in range(0, len(bits), 6):
        value = 0

        for bit in bits[index:index + 6]:
            value = (value << 1) | bit

        encoded.append(chr(value + 63))

    return "".join(encoded)


def main():
    source = json.loads(SOURCE.read_text())

    vertices = tuple(
        range(source["quotient_vertex_count"])
    )

    edges = tuple(sorted(
        canonical_edge(*edge)
        for edge in source["quotient_edges"]
    ))

    graph = adjacency(vertices, edges)

    degree_profile = Counter(
        len(graph[vertex])
        for vertex in vertices
    )

    automorphisms = enumerate_automorphisms(
        vertices,
        edges,
    )

    automorphism_order_profile = Counter(
        permutation_order(permutation)
        for permutation in automorphisms
    )

    vertex_orbits = []
    unseen = set(vertices)

    while unseen:
        vertex = min(unseen)

        orbit = tuple(sorted({
            permutation[vertex]
            for permutation in automorphisms
        }))

        vertex_orbits.append(orbit)
        unseen -= set(orbit)

    vertex_orbits = tuple(sorted(vertex_orbits))

    triangles = []

    for left in vertices:
        for middle in graph[left]:
            if middle <= left:
                continue

            for right in graph[left].intersection(
                graph[middle]
            ):
                if right > middle:
                    triangles.append(
                        (left, middle, right)
                    )

    triangles = tuple(sorted(triangles))

    checks = {
        "source_audit_pass": source["audit_pass"],
        "vertex_count_is_6": len(vertices) == 6,
        "edge_count_is_7": len(edges) == 7,
        "connected": (
            connected_component_sizes(
                vertices,
                edges,
            )
            == (6,)
        ),
        "degree_profile_is_2x3_plus_4x2": (
            dict(sorted(degree_profile.items()))
            == {2: 4, 3: 2}
        ),
        "cycle_rank_is_2": (
            cycle_rank(vertices, edges) == 2
        ),
        "automorphism_group_enumerated": (
            len(automorphisms) > 0
        ),
    }

    payload = {
        "certificate_id": (
            "native_g30_c2_orbit_skeleton_018"
        ),
        "source": str(SOURCE.relative_to(ROOT)),
        "vertex_count": len(vertices),
        "edge_count": len(edges),
        "edges": [
            list(edge)
            for edge in edges
        ],
        "degree_profile": {
            str(degree): count
            for degree, count in sorted(
                degree_profile.items()
            )
        },
        "component_sizes": list(
            connected_component_sizes(
                vertices,
                edges,
            )
        ),
        "cycle_rank": cycle_rank(
            vertices,
            edges,
        ),
        "triangle_count": len(triangles),
        "triangles": [
            list(triangle)
            for triangle in triangles
        ],
        "graph6": graph6_string(
            vertices,
            frozenset(edges),
        ),
        "automorphism_group_order": len(
            automorphisms
        ),
        "automorphism_element_order_profile": {
            str(order): count
            for order, count in sorted(
                automorphism_order_profile.items()
            )
        },
        "automorphism_vertex_orbits": [
            list(orbit)
            for orbit in vertex_orbits
        ],
        "automorphisms": [
            list(permutation)
            for permutation in automorphisms
        ],
        "classification_result": (
            "The simple six-vertex orbit skeleton is recorded "
            "canonically by its edge set, graph6 string, cycle "
            "rank, and full automorphism action. No external "
            "graph name is assumed."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "simple_orbit_skeleton_classified": True,
            "automorphism_group_enumerated": True,
            "external_named_graph_identification_open": True,
            "weighted_loop_structure_not_discarded": True,
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
    print("edges:", payload["edges"])
    print("degree_profile:", payload["degree_profile"])
    print("cycle_rank:", payload["cycle_rank"])
    print("triangle_count:", payload["triangle_count"])
    print("graph6:", payload["graph6"])
    print(
        "automorphism_group_order:",
        payload["automorphism_group_order"],
    )
    print(
        "automorphism_element_order_profile:",
        payload[
            "automorphism_element_order_profile"
        ],
    )
    print(
        "automorphism_vertex_orbits:",
        payload["automorphism_vertex_orbits"],
    )
    print(
        "classification_result:",
        payload["classification_result"],
    )


if __name__ == "__main__":
    main()
