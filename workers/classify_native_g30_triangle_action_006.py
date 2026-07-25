#!/usr/bin/env python3
"""Classify the triangle action of native G30."""

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

COMPLEMENT_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_s5_complement_classification_004.json"
)

PARITY_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_stabilizer_parity_classification_005.json"
)

OUTPUT = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_triangle_action_006.json"
)


def image_of_subset(subset, permutation):
    return tuple(sorted(
        permutation[vertex]
        for vertex in subset
    ))


def set_orbits(objects, permutations):
    unseen = set(objects)
    rows = []

    while unseen:
        representative = min(unseen)

        orbit = frozenset(
            image_of_subset(representative, permutation)
            for permutation in permutations
        )

        rows.append({
            "representative": representative,
            "orbit": orbit,
        })

        unseen -= orbit

    rows.sort(
        key=lambda row: row["representative"]
    )

    return tuple(rows)


def stabilizer(subset, permutations):
    return frozenset(
        permutation
        for permutation in permutations
        if image_of_subset(subset, permutation) == subset
    )


def main():
    graph_source = json.loads(GRAPH_SOURCE.read_text())
    action_source = json.loads(ACTION_SOURCE.read_text())
    anatomy_source = json.loads(ANATOMY_SOURCE.read_text())
    complement_source = json.loads(
        COMPLEMENT_SOURCE.read_text()
    )
    parity_source = json.loads(PARITY_SOURCE.read_text())

    vertices = tuple(graph_source["vertices"])
    edges = frozenset(
        tuple(sorted(edge))
        for edge in graph_source["edges"]
    )

    triangles = tuple(sorted(
        triple
        for triple in combinations(vertices, 3)
        if all(
            tuple(sorted(edge)) in edges
            for edge in combinations(triple, 2)
        )
    ))

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

    refined_type_by_index = {
        row["complement_index"]:
        row["refined_stabilizer_type"]
        for row in parity_source["complement_stabilizers"]
    }

    complements = []

    for row in complement_source["complements"]:
        complements.append({
            "index": row["index"],
            "refined_type": refined_type_by_index[row["index"]],
            "elements": frozenset(
                tuple(element)
                for element in row["elements"]
            ),
        })

    full_orbits = set_orbits(triangles, group)

    complement_rows = []

    for complement in complements:
        orbit_rows = set_orbits(
            triangles,
            complement["elements"],
        )

        complement_rows.append({
            "complement_index": complement["index"],
            "refined_stabilizer_type": (
                complement["refined_type"]
            ),
            "triangle_orbit_count": len(orbit_rows),
            "triangle_orbit_sizes": sorted(
                len(row["orbit"])
                for row in orbit_rows
            ),
            "triangle_orbits": [
                {
                    "representative": list(
                        row["representative"]
                    ),
                    "orbit_size": len(row["orbit"]),
                    "stabilizer_order": len(
                        stabilizer(
                            row["representative"],
                            complement["elements"],
                        )
                    ),
                    "triangles": [
                        list(triangle)
                        for triangle in sorted(row["orbit"])
                    ],
                }
                for row in orbit_rows
            ],
        })

    central_triangle_pairs = []
    unseen_triangles = set(triangles)

    while unseen_triangles:
        triangle = min(unseen_triangles)
        partner = image_of_subset(
            triangle,
            central_involution,
        )

        orbit = tuple(sorted({
            triangle,
            partner,
        }))

        central_triangle_pairs.append(orbit)
        unseen_triangles -= set(orbit)

    central_triangle_pairs = tuple(
        sorted(central_triangle_pairs)
    )

    vertex_triangle_incidence = Counter()

    for triangle in triangles:
        for vertex in triangle:
            vertex_triangle_incidence[vertex] += 1

    full_orbit_sizes = sorted(
        len(row["orbit"])
        for row in full_orbits
    )

    v4_action = next(
        row
        for row in complement_rows
        if row["refined_stabilizer_type"] == "V4_mixed"
    )

    c4_action = next(
        row
        for row in complement_rows
        if row["refined_stabilizer_type"]
        == "C4_odd_generated"
    )

    v4_orbit_sets = tuple(
        frozenset(
            tuple(triangle)
            for triangle in orbit_row["triangles"]
        )
        for orbit_row in v4_action["triangle_orbits"]
    )

    central_exchanges_v4_orbits = (
        len(v4_orbit_sets) == 2
        and frozenset(
            image_of_subset(
                triangle,
                central_involution,
            )
            for triangle in v4_orbit_sets[0]
        )
        == v4_orbit_sets[1]
        and frozenset(
            image_of_subset(
                triangle,
                central_involution,
            )
            for triangle in v4_orbit_sets[1]
        )
        == v4_orbit_sets[0]
    )

    checks = {
        "source_action_audit_pass": (
            action_source["audit_pass"]
        ),
        "source_anatomy_audit_pass": (
            anatomy_source["audit_pass"]
        ),
        "source_complement_audit_pass": (
            complement_source["audit_pass"]
        ),
        "source_parity_audit_pass": (
            parity_source["audit_pass"]
        ),
        "triangle_count_is_20": len(triangles) == 20,
        "every_vertex_lies_on_two_triangles": (
            len(vertex_triangle_incidence) == 30
            and set(vertex_triangle_incidence.values()) == {2}
        ),
        "full_group_is_triangle_transitive": (
            full_orbit_sizes == [20]
        ),
        "full_triangle_stabilizer_order_is_12": (
            len(stabilizer(triangles[0], group)) == 12
        ),
        "central_involution_fixes_no_triangle": all(
            image_of_subset(
                triangle,
                central_involution,
            )
            != triangle
            for triangle in triangles
        ),
        "central_triangle_pair_count_is_10": (
            len(central_triangle_pairs) == 10
        ),
        "all_central_triangle_orbits_have_size_2": all(
            len(orbit) == 2
            for orbit in central_triangle_pairs
        ),
        "v4_complement_has_two_triangle_orbits_of_10": (
            v4_action["triangle_orbit_sizes"] == [10, 10]
        ),
        "v4_triangle_stabilizers_have_order_12": all(
            orbit_row["stabilizer_order"] == 12
            for orbit_row in v4_action["triangle_orbits"]
        ),
        "c4_complement_is_triangle_transitive": (
            c4_action["triangle_orbit_sizes"] == [20]
        ),
        "c4_triangle_stabilizer_has_order_6": (
            c4_action["triangle_orbits"][0][
                "stabilizer_order"
            ]
            == 6
        ),
        "central_involution_exchanges_v4_triangle_orbits": (
            central_exchanges_v4_orbits
        ),
    }

    payload = {
        "certificate_id": (
            "native_g30_triangle_action_006"
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
        "complement_source": str(
            COMPLEMENT_SOURCE.relative_to(ROOT)
        ),
        "parity_source": str(
            PARITY_SOURCE.relative_to(ROOT)
        ),
        "triangle_count": len(triangles),
        "triangles": [
            list(triangle)
            for triangle in triangles
        ],
        "vertex_triangle_incidence_profile": {
            str(count): multiplicity
            for count, multiplicity in sorted(
                Counter(
                    vertex_triangle_incidence.values()
                ).items()
            )
        },
        "full_group_triangle_orbit_count": len(
            full_orbits
        ),
        "full_group_triangle_orbit_sizes": (
            full_orbit_sizes
        ),
        "full_group_triangle_stabilizer_order": len(
            stabilizer(triangles[0], group)
        ),
        "central_triangle_pair_count": len(
            central_triangle_pairs
        ),
        "central_triangle_pairs": [
            [
                list(triangle)
                for triangle in orbit
            ]
            for orbit in central_triangle_pairs
        ],
        "s5_complement_triangle_actions": (
            complement_rows
        ),
        "interpretation": (
            "The full automorphism group is transitive on the "
            "20 triangles. The V4_mixed S5 complement splits "
            "them into two orbits of 10, exchanged by the "
            "central deck involution. The odd-generated C4 S5 "
            "complement is transitive on all 20 triangles. The "
            "central involution also pairs the triangles into "
            "10 disjoint two-triangle fibers."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "triangle_action_classified": True,
            "central_triangle_pairing_derived": True,
            "triangle_pairs_identified_with_g15_triangles": False,
            "v4_triangle_orbit_exchange_derived": True,
            "triangle_local_action_structure_derived": False,
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
    print("triangle_count:", payload["triangle_count"])
    print(
        "vertex_triangle_incidence_profile:",
        payload["vertex_triangle_incidence_profile"],
    )
    print(
        "full_group_triangle_orbit_sizes:",
        payload["full_group_triangle_orbit_sizes"],
    )
    print(
        "full_group_triangle_stabilizer_order:",
        payload[
            "full_group_triangle_stabilizer_order"
        ],
    )
    print(
        "central_triangle_pair_count:",
        payload["central_triangle_pair_count"],
    )

    for row in complement_rows:
        print(
            "complement",
            row["complement_index"],
            row["refined_stabilizer_type"],
            "triangle orbit sizes:",
            row["triangle_orbit_sizes"],
            "stabilizer:",
            row["triangle_orbits"][0][
                "stabilizer_order"
            ],
        )

    print("interpretation:", payload["interpretation"])


if __name__ == "__main__":
    main()
