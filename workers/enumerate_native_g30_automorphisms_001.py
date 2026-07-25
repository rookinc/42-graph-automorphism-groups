#!/usr/bin/env python3
"""Enumerate the full automorphism action of native G30."""

import json
from collections import Counter
from pathlib import Path

import networkx as nx


ROOT = Path(__file__).resolve().parents[1]

SOURCE = ROOT / "sources" / "native_g30_graph_input_001.json"

OUTPUT = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_full_automorphism_action_001.json"
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


def permutation_order(permutation):
    identity = tuple(range(len(permutation)))
    current = identity
    order = 0

    while True:
        order += 1
        current = compose(permutation, current)

        if current == identity:
            return order


def commutes(left, right):
    return compose(left, right) == compose(right, left)


def main():
    source = json.loads(SOURCE.read_text())

    vertices = tuple(
        int(vertex)
        for vertex in source["vertices"]
    )

    edges = tuple(
        tuple(int(value) for value in edge)
        for edge in source["edges"]
    )

    graph = nx.Graph()
    graph.add_nodes_from(vertices)
    graph.add_edges_from(edges)

    matcher = nx.algorithms.isomorphism.GraphMatcher(
        graph,
        graph,
    )

    automorphisms = []

    for mapping in matcher.isomorphisms_iter():
        automorphisms.append(
            tuple(
                int(mapping[vertex])
                for vertex in vertices
            )
        )

    automorphisms = tuple(
        sorted(set(automorphisms))
    )

    identity = tuple(range(len(vertices)))
    automorphism_set = set(automorphisms)

    if identity not in automorphism_set:
        raise RuntimeError("identity automorphism missing")

    order_profile = Counter(
        permutation_order(permutation)
        for permutation in automorphisms
    )

    orbit_0 = tuple(
        sorted({
            permutation[0]
            for permutation in automorphisms
        })
    )

    stabilizer_0 = tuple(
        permutation
        for permutation in automorphisms
        if permutation[0] == 0
    )

    center = tuple(
        permutation
        for permutation in automorphisms
        if all(
            commutes(permutation, other)
            for other in automorphisms
        )
    )

    inverse_checks = all(
        inverse(permutation) in automorphism_set
        for permutation in automorphisms
    )

    rows = [
        {
            "index": index,
            "permutation": list(permutation),
            "order": permutation_order(permutation),
            "fixes_vertex_0": permutation[0] == 0,
            "central": permutation in center,
        }
        for index, permutation in enumerate(automorphisms)
    ]

    checks = {
        "source_vertex_count_is_30": len(vertices) == 30,
        "source_edge_count_is_60": len(edges) == 60,
        "automorphism_count_is_240": len(automorphisms) == 240,
        "identity_present": identity in automorphism_set,
        "all_inverses_present": inverse_checks,
        "vertex_orbit_size_is_30": len(orbit_0) == 30,
        "vertex_stabilizer_order_is_8": len(stabilizer_0) == 8,
    }

    payload = {
        "certificate_id": (
            "native_g30_full_automorphism_action_001"
        ),
        "source": str(SOURCE.relative_to(ROOT)),
        "vertex_count": len(vertices),
        "edge_count": len(edges),
        "automorphism_count": len(automorphisms),
        "vertex_orbit_0": list(orbit_0),
        "vertex_orbit_0_size": len(orbit_0),
        "vertex_stabilizer_0_order": len(stabilizer_0),
        "center_order": len(center),
        "element_order_profile": {
            str(order): count
            for order, count in sorted(order_profile.items())
        },
        "automorphisms": rows,
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "full_action_enumerated": True,
            "abstract_group_structure_claimed": False,
            "derived_subgroup_computed": False,
            "mixed_v4_model_proved": False,
            "physical_claim": False,
        },
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )

    print("OUT ==")
    print("output:", OUTPUT)
    print("audit_pass:", payload["audit_pass"])
    print("automorphism_count:", payload["automorphism_count"])
    print("vertex_orbit_0_size:", payload["vertex_orbit_0_size"])
    print(
        "vertex_stabilizer_0_order:",
        payload["vertex_stabilizer_0_order"],
    )
    print("center_order:", payload["center_order"])
    print(
        "element_order_profile:",
        payload["element_order_profile"],
    )


if __name__ == "__main__":
    main()
