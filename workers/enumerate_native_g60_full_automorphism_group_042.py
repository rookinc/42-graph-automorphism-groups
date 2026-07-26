#!/usr/bin/env python3
"""Independently enumerate the full automorphism group of native G60."""

import json
import sys
import time
from pathlib import Path

import networkx as nx


ROOT = Path(__file__).resolve().parents[1]

GRAPH_SOURCE = (
    ROOT / "sources/"
    "project42_g60_to_g30_a_quotient_certificate_035.json"
)

LIFT_SOURCE = (
    ROOT / "artifacts/json/"
    "native_g30_automorphism_lifts_to_g60_032.json"
)

OUTPUT = (
    ROOT / "artifacts/json/"
    "native_g60_full_automorphism_group_042.json"
)


START = time.monotonic()


def progress(message):
    elapsed = time.monotonic() - START
    print(
        f"[{elapsed:8.3f}s] {message}",
        file=sys.stderr,
        flush=True,
    )


def identity(size):
    return tuple(range(size))


def compose(left, right):
    return tuple(
        left[right[index]]
        for index in range(len(left))
    )


def main():
    progress("loading exact native graph and lift receipts")

    graph_source = json.loads(
        GRAPH_SOURCE.read_text()
    )

    lift_source = json.loads(
        LIFT_SOURCE.read_text()
    )

    vertex_count = int(
        graph_source["g60_vertex_count"]
    )

    edges = [
        tuple(map(int, edge))
        for edge in graph_source["g60_edges"]
    ]

    deck_a = tuple(
        int(graph_source["involution_a"][str(vertex)])
        for vertex in range(vertex_count)
    )

    graph = nx.Graph()
    graph.add_nodes_from(range(vertex_count))
    graph.add_edges_from(edges)

    progress(
        "constructed graph "
        f"vertices={graph.number_of_nodes()} "
        f"edges={graph.number_of_edges()}"
    )

    matcher = nx.algorithms.isomorphism.GraphMatcher(
        graph,
        graph,
    )

    native_automorphisms = set()

    for count, mapping in enumerate(
        matcher.isomorphisms_iter(),
        start=1,
    ):
        permutation = tuple(
            int(mapping[index])
            for index in range(vertex_count)
        )

        native_automorphisms.add(
            permutation
        )

        if count % 50 == 0:
            progress(
                "enumerated "
                f"{count} isomorphisms; "
                f"distinct={len(native_automorphisms)}"
            )

    native_group = frozenset(
        native_automorphisms
    )

    progress(
        "native enumeration complete "
        f"order={len(native_group)}"
    )

    lifted_group = frozenset(
        tuple(lift["permutation"])
        for row in lift_source["lift_rows"]
        for lift in row["lifts"]
    )

    native_only = native_group - lifted_group
    lifted_only = lifted_group - native_group

    fibers = {
        frozenset((vertex, deck_a[vertex]))
        for vertex in range(vertex_count)
    }

    fiber_preservation_failures = []

    for permutation in native_group:
        for fiber in fibers:
            image = frozenset(
                permutation[vertex]
                for vertex in fiber
            )

            if image not in fibers:
                fiber_preservation_failures.append({
                    "permutation": list(permutation),
                    "fiber": sorted(fiber),
                    "image": sorted(image),
                })
                break

    deck_centrality_failures = [
        list(permutation)
        for permutation in native_group
        if compose(permutation, deck_a)
        != compose(deck_a, permutation)
    ]

    degree_profile = sorted(
        degree
        for _, degree in graph.degree()
    )

    checks = {
        "graph_source_audit_pass": (
            graph_source["audit_pass"]
        ),
        "lift_source_audit_pass": (
            lift_source["audit_pass"]
        ),
        "graph_has_60_vertices": (
            graph.number_of_nodes() == 60
        ),
        "graph_has_120_edges": (
            graph.number_of_edges() == 120
        ),
        "graph_is_connected": (
            nx.is_connected(graph)
        ),
        "graph_is_quartic": (
            degree_profile == [4] * 60
        ),
        "native_automorphism_count_is_480": (
            len(native_group) == 480
        ),
        "lifted_group_count_is_480": (
            len(lifted_group) == 480
        ),
        "native_group_equals_lifted_group": (
            not native_only
            and not lifted_only
        ),
        "every_native_automorphism_preserves_a_fibers": (
            not fiber_preservation_failures
        ),
        "every_native_automorphism_centralizes_deck_a": (
            not deck_centrality_failures
        ),
        "identity_is_present": (
            identity(vertex_count)
            in native_group
        ),
        "deck_a_is_present": (
            deck_a in native_group
        ),
    }

    output = {
        "certificate_id": (
            "native_g60_full_automorphism_group_042"
        ),
        "audit_pass": all(
            checks.values()
        ),
        "graph_source": str(
            GRAPH_SOURCE.relative_to(ROOT)
        ),
        "lift_source": str(
            LIFT_SOURCE.relative_to(ROOT)
        ),
        "runtime_seconds": round(
            time.monotonic() - START,
            6,
        ),
        "graph": {
            "vertex_count": (
                graph.number_of_nodes()
            ),
            "edge_count": (
                graph.number_of_edges()
            ),
            "connected": (
                nx.is_connected(graph)
            ),
            "degree_profile": (
                degree_profile
            ),
        },
        "native_automorphism_count": (
            len(native_group)
        ),
        "lifted_automorphism_count": (
            len(lifted_group)
        ),
        "native_only_count": (
            len(native_only)
        ),
        "lifted_only_count": (
            len(lifted_only)
        ),
        "fiber_preservation_failure_count": (
            len(fiber_preservation_failures)
        ),
        "deck_centrality_failure_count": (
            len(deck_centrality_failures)
        ),
        "deck_a": list(
            deck_a
        ),
        "native_automorphisms": [
            list(permutation)
            for permutation in sorted(
                native_group
            )
        ],
        "checks": checks,
        "classification_result": (
            "An independent NetworkX GraphMatcher enumeration of the "
            "exact native sixty-vertex graph returns exactly 480 "
            "automorphisms. The enumerated permutation set equals the "
            "480-element lifted group exactly. Every native "
            "automorphism preserves the canonical a-fiber partition "
            "and centralizes the deck involution a."
        ),
        "boundary": (
            "This receipt establishes completeness of the lifted "
            "automorphism group and invariance of the canonical deck "
            "fibers. It does not by itself identify the abstract "
            "480-element group."
        ),
    }

    OUTPUT.write_text(
        json.dumps(
            output,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )

    print("OUT ==")
    print(f"output: {OUTPUT}")
    print(f"audit_pass: {output['audit_pass']}")
    print(
        "native_automorphism_count: "
        f"{output['native_automorphism_count']}"
    )
    print(
        "lifted_automorphism_count: "
        f"{output['lifted_automorphism_count']}"
    )
    print(
        "native_only_count: "
        f"{output['native_only_count']}"
    )
    print(
        "lifted_only_count: "
        f"{output['lifted_only_count']}"
    )
    print(
        "fiber_preservation_failure_count: "
        f"{output['fiber_preservation_failure_count']}"
    )
    print(
        "deck_centrality_failure_count: "
        f"{output['deck_centrality_failure_count']}"
    )
    print(
        "runtime_seconds: "
        f"{output['runtime_seconds']}"
    )


if __name__ == "__main__":
    main()
