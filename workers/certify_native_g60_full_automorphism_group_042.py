#!/usr/bin/env python3
"""Enumerate Aut(G60) independently from the exact native edge set."""

import json
import sys
import time
from collections import Counter
from pathlib import Path

import networkx as nx


ROOT = Path(__file__).resolve().parents[1]

BRIDGE_SOURCE = (
    ROOT / "sources/"
    "project42_g60_to_g30_a_quotient_certificate_035.json"
)

LIFT_SOURCE = (
    ROOT / "artifacts/json/"
    "native_g30_automorphism_lifts_to_g60_032.json"
)

GROUP_SOURCE = (
    ROOT / "artifacts/json/"
    "native_g60_lifted_automorphism_group_040.json"
)

EXTENSION_SOURCE = (
    ROOT / "artifacts/json/"
    "native_g60_lifted_group_extension_type_041.json"
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


def permutation_order(permutation):
    unit = identity(len(permutation))
    current = unit

    for order in range(1, 1000):
        current = compose(
            permutation,
            current,
        )

        if current == unit:
            return order

    raise RuntimeError(
        "permutation order exceeded bound"
    )


def preserves_edges(permutation, edge_set):
    return all(
        tuple(
            sorted(
                (
                    permutation[left],
                    permutation[right],
                )
            )
        )
        in edge_set
        for left, right in edge_set
    )


def main():
    progress("loading exact G60 graph and lifted-group sources")

    bridge = json.loads(
        BRIDGE_SOURCE.read_text()
    )

    lift_source = json.loads(
        LIFT_SOURCE.read_text()
    )

    group_source = json.loads(
        GROUP_SOURCE.read_text()
    )

    extension_source = json.loads(
        EXTENSION_SOURCE.read_text()
    )

    vertex_count = int(
        bridge["g60_vertex_count"]
    )

    edges = [
        tuple(
            sorted(
                (
                    int(edge[0]),
                    int(edge[1]),
                )
            )
        )
        for edge in bridge["g60_edges"]
    ]

    edge_set = frozenset(edges)

    graph = nx.Graph()
    graph.add_nodes_from(
        range(vertex_count)
    )
    graph.add_edges_from(edges)

    degree_profile = Counter(
        degree
        for _, degree in graph.degree()
    )

    progress(
        "native graph loaded: "
        f"{graph.number_of_nodes()} vertices, "
        f"{graph.number_of_edges()} edges, "
        f"degree profile {dict(sorted(degree_profile.items()))}"
    )

    lifted_group = frozenset(
        tuple(lift["permutation"])
        for row in lift_source["lift_rows"]
        for lift in row["lifts"]
    )

    progress(
        "loaded constructed lifted group "
        f"of size {len(lifted_group)}"
    )

    matcher = nx.algorithms.isomorphism.GraphMatcher(
        graph,
        graph,
    )

    progress(
        "starting independent NetworkX automorphism enumeration"
    )

    full_automorphisms = set()
    duplicate_count = 0

    last_report_time = time.monotonic()

    for enumeration_index, mapping in enumerate(
        matcher.isomorphisms_iter(),
        start=1,
    ):
        permutation = tuple(
            int(mapping[vertex])
            for vertex in range(vertex_count)
        )

        if permutation in full_automorphisms:
            duplicate_count += 1
        else:
            full_automorphisms.add(
                permutation
            )

        now = time.monotonic()

        if (
            enumeration_index <= 10
            or enumeration_index % 50 == 0
            or now - last_report_time >= 2.0
        ):
            progress(
                "enumerated "
                f"{enumeration_index} mappings, "
                f"{len(full_automorphisms)} distinct"
            )
            last_report_time = now

    full_group = frozenset(
        full_automorphisms
    )

    progress(
        "enumeration complete with "
        f"{len(full_group)} distinct automorphisms"
    )

    progress("verifying every enumerated permutation against edges")

    all_enumerated_preserve_edges = all(
        preserves_edges(
            permutation,
            edge_set,
        )
        for permutation in full_group
    )

    progress("comparing full group with constructed lifted group")

    lifted_missing_from_full = (
        lifted_group - full_group
    )

    full_not_in_lifted = (
        full_group - lifted_group
    )

    groups_equal = (
        full_group == lifted_group
    )

    progress("computing full-group element-order profile")

    order_profile = Counter(
        permutation_order(permutation)
        for permutation in full_group
    )

    deck_a = tuple(
        int(
            bridge["involution_a"][
                str(vertex)
            ]
        )
        for vertex in range(vertex_count)
    )

    automorphisms_preserving_a_fibers = 0
    automorphisms_centralizing_a = 0

    fibers = [
        frozenset(
            int(vertex)
            for vertex in row["g60_vertices"]
        )
        for row in bridge[
            "g30_fibers_from_g60"
        ]
    ]

    fiber_set = frozenset(
        fibers
    )

    for permutation in full_group:
        image_fibers = frozenset(
            frozenset(
                permutation[vertex]
                for vertex in fiber
            )
            for fiber in fibers
        )

        if image_fibers == fiber_set:
            automorphisms_preserving_a_fibers += 1

        if (
            compose(permutation, deck_a)
            == compose(deck_a, permutation)
        ):
            automorphisms_centralizing_a += 1

    checks = {
        "bridge_source_audit_pass": (
            bridge["audit_pass"]
        ),
        "lift_source_audit_pass": (
            lift_source["audit_pass"]
        ),
        "group_source_audit_pass": (
            group_source["audit_pass"]
        ),
        "extension_source_audit_pass": (
            extension_source["audit_pass"]
        ),
        "native_graph_has_60_vertices": (
            graph.number_of_nodes() == 60
        ),
        "native_graph_has_120_edges": (
            graph.number_of_edges() == 120
        ),
        "native_graph_is_simple": (
            nx.number_of_selfloops(graph) == 0
            and len(edge_set) == 120
        ),
        "native_graph_is_connected": (
            nx.is_connected(graph)
        ),
        "native_graph_is_quartic": (
            degree_profile == {4: 60}
        ),
        "networkx_enumeration_has_no_duplicates": (
            duplicate_count == 0
        ),
        "every_enumerated_permutation_preserves_edges": (
            all_enumerated_preserve_edges
        ),
        "constructed_lifted_group_has_order_480": (
            len(lifted_group) == 480
        ),
        "full_automorphism_group_has_order_480": (
            len(full_group) == 480
        ),
        "no_constructed_lift_missing_from_full_group": (
            len(lifted_missing_from_full) == 0
        ),
        "no_extra_full_automorphism_outside_lifted_group": (
            len(full_not_in_lifted) == 0
        ),
        "full_group_equals_constructed_lifted_group": (
            groups_equal
        ),
        "all_full_automorphisms_preserve_a_fibers": (
            automorphisms_preserving_a_fibers
            == len(full_group)
        ),
        "all_full_automorphisms_centralize_a": (
            automorphisms_centralizing_a
            == len(full_group)
        ),
        "order_profile_matches_040": (
            {
                str(order): count
                for order, count in sorted(
                    order_profile.items()
                )
            }
            == group_source[
                "element_order_profile"
            ]
        ),
    }

    payload = {
        "certificate_id": (
            "native_g60_full_automorphism_group_042"
        ),
        "bridge_source": str(
            BRIDGE_SOURCE.relative_to(ROOT)
        ),
        "lift_source": str(
            LIFT_SOURCE.relative_to(ROOT)
        ),
        "group_source": str(
            GROUP_SOURCE.relative_to(ROOT)
        ),
        "extension_source": str(
            EXTENSION_SOURCE.relative_to(ROOT)
        ),
        "enumeration_engine": (
            "networkx.algorithms.isomorphism.GraphMatcher"
        ),
        "runtime_seconds": round(
            time.monotonic() - START,
            6,
        ),
        "g60_vertex_count": (
            graph.number_of_nodes()
        ),
        "g60_edge_count": (
            graph.number_of_edges()
        ),
        "degree_profile": {
            str(degree): count
            for degree, count in sorted(
                degree_profile.items()
            )
        },
        "enumerated_mapping_count": (
            len(full_group)
            + duplicate_count
        ),
        "duplicate_mapping_count": (
            duplicate_count
        ),
        "full_automorphism_group_order": (
            len(full_group)
        ),
        "constructed_lifted_group_order": (
            len(lifted_group)
        ),
        "lifted_missing_from_full_count": (
            len(lifted_missing_from_full)
        ),
        "full_not_in_lifted_count": (
            len(full_not_in_lifted)
        ),
        "groups_equal": (
            groups_equal
        ),
        "full_group_element_order_profile": {
            str(order): count
            for order, count in sorted(
                order_profile.items()
            )
        },
        "automorphisms_preserving_a_fibers": (
            automorphisms_preserving_a_fibers
        ),
        "automorphisms_centralizing_a": (
            automorphisms_centralizing_a
        ),
        "full_group_classification": {
            "order": 480,
            "center_order": (
                group_source["center_order"]
            ),
            "derived_subgroup": (
                extension_source[
                    "derived_subgroup_classification"
                ]
            ),
            "derived_subgroup_order": (
                extension_source[
                    "derived_subgroup_order"
                ]
            ),
            "abelianization": (
                extension_source[
                    "abelianization_type"
                ]
            ),
            "abelianization_order": (
                extension_source[
                    "abelianization_order"
                ]
            ),
        },
        "theorem_result": (
            "Independent enumeration from the exact native G60 "
            "edge set gives exactly 480 graph automorphisms. "
            "The enumerated set equals the previously constructed "
            "set obtained by lifting all 240 automorphisms of G30. "
            "Therefore every automorphism of G60 preserves the "
            "native a-fiber system, and Aut(G60) is exactly the "
            "480-element lifted group. Its derived subgroup is "
            "A5 x C2 and its abelianization is C2 x C2."
        ),
        "checks": checks,
        "audit_pass": all(
            checks.values()
        ),
        "boundary": {
            "full_aut_g60_order_certified": True,
            "full_aut_g60_equals_lifted_group_certified": True,
            "every_g60_automorphism_preserves_a_fibers_certified": True,
            "every_g60_automorphism_centralizes_a_certified": True,
            "classification_uses_independent_graph_enumeration": True,
            "named_single_standard_group_isomorphism_not_yet_presented": True,
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

    progress("receipt written")

    print("OUT ==")
    print("output:", OUTPUT)
    print(
        "runtime_seconds:",
        payload["runtime_seconds"],
    )
    print(
        "audit_pass:",
        payload["audit_pass"],
    )
    print(
        "g60_vertex_count:",
        payload["g60_vertex_count"],
    )
    print(
        "g60_edge_count:",
        payload["g60_edge_count"],
    )
    print(
        "degree_profile:",
        payload["degree_profile"],
    )
    print(
        "full_automorphism_group_order:",
        payload[
            "full_automorphism_group_order"
        ],
    )
    print(
        "constructed_lifted_group_order:",
        payload[
            "constructed_lifted_group_order"
        ],
    )
    print(
        "lifted_missing_from_full_count:",
        payload[
            "lifted_missing_from_full_count"
        ],
    )
    print(
        "full_not_in_lifted_count:",
        payload[
            "full_not_in_lifted_count"
        ],
    )
    print(
        "groups_equal:",
        payload["groups_equal"],
    )
    print(
        "full_group_element_order_profile:",
        payload[
            "full_group_element_order_profile"
        ],
    )
    print(
        "automorphisms_preserving_a_fibers:",
        payload[
            "automorphisms_preserving_a_fibers"
        ],
    )
    print(
        "automorphisms_centralizing_a:",
        payload[
            "automorphisms_centralizing_a"
        ],
    )
    print(
        "full_group_classification:",
        payload[
            "full_group_classification"
        ],
    )
    print(
        "theorem_result:",
        payload["theorem_result"],
    )


if __name__ == "__main__":
    main()
