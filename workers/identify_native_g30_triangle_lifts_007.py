#!/usr/bin/env python3
"""Identify native G30 triangle pairs with G15 quotient triangles."""

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

DECK_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_central_deck_geometry_003.json"
)

TRIANGLE_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_triangle_action_006.json"
)

OUTPUT = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_triangle_lifts_007.json"
)


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


def main():
    graph_source = json.loads(GRAPH_SOURCE.read_text())
    deck_source = json.loads(DECK_SOURCE.read_text())
    triangle_source = json.loads(
        TRIANGLE_SOURCE.read_text()
    )

    g30_vertices = tuple(graph_source["vertices"])
    g30_edges = tuple(
        tuple(edge)
        for edge in graph_source["edges"]
    )

    g30_triangles = tuple(
        tuple(triangle)
        for triangle in triangle_source["triangles"]
    )

    central_involution = tuple(
        deck_source["central_involution"]
    )

    central_pairs = tuple(
        tuple(pair)
        for pair in deck_source["central_pair_orbits"]
    )

    vertex_to_quotient = {}

    for quotient_vertex, pair in enumerate(central_pairs):
        for vertex in pair:
            vertex_to_quotient[vertex] = quotient_vertex

    quotient_vertices = tuple(range(len(central_pairs)))

    quotient_edge_multiplicity = Counter()

    for left, right in g30_edges:
        quotient_edge = tuple(sorted((
            vertex_to_quotient[left],
            vertex_to_quotient[right],
        )))

        quotient_edge_multiplicity[quotient_edge] += 1

    quotient_edges = tuple(sorted(
        edge
        for edge in quotient_edge_multiplicity
        if edge[0] != edge[1]
    ))

    quotient_triangles = triangle_set(
        quotient_vertices,
        quotient_edges,
    )

    g30_triangle_to_quotient = {}

    for triangle in g30_triangles:
        image = tuple(sorted(
            vertex_to_quotient[vertex]
            for vertex in triangle
        ))

        g30_triangle_to_quotient[triangle] = image

    quotient_triangle_lifts = {
        triangle: []
        for triangle in quotient_triangles
    }

    for g30_triangle, quotient_triangle in (
        g30_triangle_to_quotient.items()
    ):
        if quotient_triangle in quotient_triangle_lifts:
            quotient_triangle_lifts[
                quotient_triangle
            ].append(g30_triangle)

    lift_rows = []

    for quotient_triangle in quotient_triangles:
        lifts = tuple(sorted(
            quotient_triangle_lifts[quotient_triangle]
        ))

        if len(lifts) == 2:
            first, second = lifts

            deck_related = (
                tuple(sorted(
                    central_involution[vertex]
                    for vertex in first
                ))
                == second
            )
        else:
            deck_related = False

        lift_rows.append({
            "quotient_triangle": list(quotient_triangle),
            "lift_count": len(lifts),
            "g30_triangle_lifts": [
                list(triangle)
                for triangle in lifts
            ],
            "deck_related": deck_related,
            "lifts_are_vertex_disjoint": (
                len(lifts) == 2
                and set(lifts[0]).isdisjoint(lifts[1])
            ),
            "lift_union_size": (
                len(set().union(*(
                    set(triangle)
                    for triangle in lifts
                )))
                if lifts
                else 0
            ),
        })

    g30_projection_multiplicity = Counter(
        g30_triangle_to_quotient.values()
    )

    projected_images_are_triangles = all(
        image in set(quotient_triangles)
        for image in g30_triangle_to_quotient.values()
    )

    all_lifted_triangles = {
        triangle
        for row in lift_rows
        for triangle in (
            tuple(lift)
            for lift in row["g30_triangle_lifts"]
        )
    }

    checks = {
        "triangle_source_audit_pass": (
            triangle_source["audit_pass"]
        ),
        "central_involution_is_fixed_point_free": (
            deck_source[
                "central_involution_fixed_point_count"
            ]
            == 0
        ),
        "g30_triangle_count_is_20": (
            len(g30_triangles) == 20
        ),
        "quotient_triangle_count_is_10": (
            len(quotient_triangles) == 10
        ),
        "every_g30_triangle_projects_to_three_vertices": all(
            len(set(image)) == 3
            for image in g30_triangle_to_quotient.values()
        ),
        "every_g30_triangle_projects_to_quotient_triangle": (
            projected_images_are_triangles
        ),
        "every_quotient_triangle_has_two_lifts": all(
            row["lift_count"] == 2
            for row in lift_rows
        ),
        "every_lift_pair_is_deck_related": all(
            row["deck_related"]
            for row in lift_rows
        ),
        "every_lift_pair_is_vertex_disjoint": all(
            row["lifts_are_vertex_disjoint"]
            for row in lift_rows
        ),
        "every_lift_pair_uses_six_vertices": all(
            row["lift_union_size"] == 6
            for row in lift_rows
        ),
        "projection_multiplicity_is_uniformly_two": (
            set(g30_projection_multiplicity.values()) == {2}
            and len(g30_projection_multiplicity) == 10
        ),
        "all_20_g30_triangles_accounted_for": (
            all_lifted_triangles == set(g30_triangles)
        ),
    }

    payload = {
        "certificate_id": (
            "native_g30_triangle_lifts_007"
        ),
        "graph_source": str(
            GRAPH_SOURCE.relative_to(ROOT)
        ),
        "deck_source": str(
            DECK_SOURCE.relative_to(ROOT)
        ),
        "triangle_source": str(
            TRIANGLE_SOURCE.relative_to(ROOT)
        ),
        "g30_vertex_count": len(g30_vertices),
        "g30_triangle_count": len(g30_triangles),
        "quotient_vertex_count": len(quotient_vertices),
        "quotient_edge_count": len(quotient_edges),
        "quotient_triangle_count": len(quotient_triangles),
        "quotient_triangles": [
            list(triangle)
            for triangle in quotient_triangles
        ],
        "triangle_lifts": lift_rows,
        "g30_to_quotient_triangle_multiplicity_profile": {
            str(count): multiplicity
            for count, multiplicity in sorted(
                Counter(
                    g30_projection_multiplicity.values()
                ).items()
            )
        },
        "lifting_result": (
            "Each of the 10 quotient triangles has exactly "
            "two vertex-disjoint G30 triangle lifts, exchanged "
            "by the central deck involution."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "triangle_lifting_law_derived": True,
            "quotient_triangle_count_derived": True,
            "quotient_explicitly_identified_as_line_petersen": False,
            "triangle_stabilizer_structure_not_yet_classified": True,
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
        "g30_triangle_count:",
        payload["g30_triangle_count"],
    )
    print(
        "quotient_triangle_count:",
        payload["quotient_triangle_count"],
    )
    print(
        "triangle_multiplicity_profile:",
        payload[
            "g30_to_quotient_triangle_multiplicity_profile"
        ],
    )
    print(
        "all_pairs_deck_related:",
        checks["every_lift_pair_is_deck_related"],
    )
    print(
        "all_pairs_vertex_disjoint:",
        checks[
            "every_lift_pair_is_vertex_disjoint"
        ],
    )
    print("lifting_result:", payload["lifting_result"])


if __name__ == "__main__":
    main()
