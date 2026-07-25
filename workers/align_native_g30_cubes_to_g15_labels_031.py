#!/usr/bin/env python3
"""Align the fifteen intrinsic G30 cubes to native G15 quotient labels."""

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

QUOTIENT_SOURCE = (
    ROOT
    / "artifacts/json/"
    "native_g30_quotient_line_petersen_008.json"
)

CUBE_SOURCE = (
    ROOT
    / "artifacts/json/"
    "native_g30_petersen_from_cube_centers_029.json"
)

CUBE_GRAPH_SOURCE = (
    ROOT
    / "artifacts/json/"
    "native_g30_fifteen_cube_graph_027.json"
)

OUTPUT = (
    ROOT
    / "artifacts/json/"
    "native_g30_cube_to_g15_label_alignment_031.json"
)


def canonical_edge(edge):
    return tuple(sorted(int(value) for value in edge))


def main():
    quotient = json.loads(QUOTIENT_SOURCE.read_text())
    cube_source = json.loads(CUBE_SOURCE.read_text())
    cube_graph = json.loads(CUBE_GRAPH_SOURCE.read_text())

    center_to_petersen = {
        int(center): int(vertex)
        for center, vertex in cube_source[
            "representative_isomorphism_to_petersen"
        ].items()
    }

    quotient_to_petersen_edge = {
        int(label): canonical_edge(edge)
        for label, edge in quotient[
            "quotient_vertex_to_petersen_edge"
        ].items()
    }

    petersen_edge_to_quotient = {
        edge: label
        for label, edge in quotient_to_petersen_edge.items()
    }

    cube_rows = []

    for row in cube_source["cube_edge_rows"]:
        cube_index = int(row["cube_index"])
        intrinsic_centers = tuple(
            int(value)
            for value in row["incident_centers"]
        )

        mapped_petersen_edge = canonical_edge(
            center_to_petersen[center]
            for center in intrinsic_centers
        )

        quotient_label = petersen_edge_to_quotient.get(
            mapped_petersen_edge
        )

        cube_rows.append({
            "cube_index": cube_index,
            "intrinsic_center_indices": list(
                intrinsic_centers
            ),
            "mapped_petersen_edge": list(
                mapped_petersen_edge
            ),
            "native_g15_label": quotient_label,
        })

    cube_rows.sort(
        key=lambda row: row["cube_index"]
    )

    cube_to_g15 = {
        row["cube_index"]: row["native_g15_label"]
        for row in cube_rows
    }

    g15_to_cube = {
        label: cube
        for cube, label in cube_to_g15.items()
        if label is not None
    }

    cube_edges = {
        canonical_edge(edge)
        for edge in cube_graph["edges"]
    }

    quotient_edges = set()

    quotient_triangles = [
        tuple(sorted(
            int(value)
            for value in row["quotient_triangle"]
        ))
        for row in quotient[
            "quotient_triangle_to_petersen_vertex"
        ]
    ]

    for triangle in quotient_triangles:
        for index in range(3):
            for other in range(index + 1, 3):
                quotient_edges.add(
                    canonical_edge(
                        (
                            triangle[index],
                            triangle[other],
                        )
                    )
                )

    mapped_cube_edges = {
        canonical_edge(
            (
                cube_to_g15[left],
                cube_to_g15[right],
            )
        )
        for left, right in cube_edges
    }

    cube_triangles_to_g15 = []

    quotient_triangle_set = set(
        quotient_triangles
    )

    for triangle in cube_graph["triangles"]:
        mapped_triangle = tuple(sorted(
            cube_to_g15[int(cube)]
            for cube in triangle
        ))

        matching_row = next(
            (
                row
                for row in quotient[
                    "quotient_triangle_to_petersen_vertex"
                ]
                if tuple(sorted(
                    int(value)
                    for value in row[
                        "quotient_triangle"
                    ]
                ))
                == mapped_triangle
            ),
            None,
        )

        cube_triangles_to_g15.append({
            "cube_triangle": [
                int(value)
                for value in triangle
            ],
            "mapped_g15_triangle": list(
                mapped_triangle
            ),
            "matches_native_quotient_triangle": (
                mapped_triangle
                in quotient_triangle_set
            ),
            "petersen_vertex": (
                matching_row["petersen_vertex"]
                if matching_row is not None
                else None
            ),
        })

    label_profile = Counter(
        row["native_g15_label"]
        for row in cube_rows
    )

    checks = {
        "quotient_source_audit_pass": (
            quotient["audit_pass"]
        ),
        "cube_source_audit_pass": (
            cube_source["audit_pass"]
        ),
        "cube_graph_source_audit_pass": (
            cube_graph["audit_pass"]
        ),
        "center_to_petersen_map_has_10_entries": (
            len(center_to_petersen) == 10
        ),
        "quotient_to_petersen_edge_map_has_15_entries": (
            len(quotient_to_petersen_edge) == 15
        ),
        "all_cubes_receive_g15_label": all(
            row["native_g15_label"] is not None
            for row in cube_rows
        ),
        "cube_to_g15_alignment_is_bijective": (
            len(cube_to_g15) == 15
            and len(g15_to_cube) == 15
            and set(g15_to_cube) == set(range(15))
        ),
        "cube_graph_edges_map_exactly_to_quotient_edges": (
            mapped_cube_edges == quotient_edges
        ),
        "all_cube_triangles_map_to_native_quotient_triangles": all(
            row[
                "matches_native_quotient_triangle"
            ]
            for row in cube_triangles_to_g15
        ),
        "all_10_native_quotient_triangles_used_once": (
            {
                tuple(row["mapped_g15_triangle"])
                for row in cube_triangles_to_g15
            }
            == quotient_triangle_set
        ),
    }

    payload = {
        "certificate_id": (
            "native_g30_cube_to_g15_label_alignment_031"
        ),
        "quotient_source": str(
            QUOTIENT_SOURCE.relative_to(ROOT)
        ),
        "cube_source": str(
            CUBE_SOURCE.relative_to(ROOT)
        ),
        "cube_graph_source": str(
            CUBE_GRAPH_SOURCE.relative_to(ROOT)
        ),
        "alignment_method": (
            "compose the selected intrinsic-center to standard "
            "Petersen isomorphism from artifact 029 with the "
            "standard Petersen-edge to native quotient-label "
            "identification from artifact 008"
        ),
        "center_to_standard_petersen_vertex": {
            str(center): vertex
            for center, vertex in sorted(
                center_to_petersen.items()
            )
        },
        "cube_rows": cube_rows,
        "cube_to_native_g15_label": {
            str(cube): label
            for cube, label in sorted(
                cube_to_g15.items()
            )
        },
        "native_g15_label_to_cube": {
            str(label): cube
            for label, cube in sorted(
                g15_to_cube.items()
            )
        },
        "cube_triangle_rows": (
            cube_triangles_to_g15
        ),
        "native_g15_label_profile": {
            str(label): count
            for label, count in sorted(
                label_profile.items(),
                key=lambda item: (
                    item[0] is None,
                    item[0],
                ),
            )
        },
        "alignment_result": (
            "The fifteen intrinsic affine cubes are now "
            "bijectively aligned with the existing native G15 "
            "quotient labels 0 through 14. Under this binding, "
            "order-4 cube intersections reproduce exactly the "
            "native quotient edge relation, and the ten cube "
            "triangles reproduce exactly the ten labeled "
            "quotient triangles already identified as Petersen "
            "vertex stars."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "intrinsic_cube_to_native_g15_label_binding": True,
            "native_g15_edge_relation_reproduced": True,
            "native_g15_triangle_system_reproduced": True,
            "selected_alignment_depends_on_selected_petersen_isomorphisms": True,
            "alignment_uniqueness_claim": False,
            "g60_lift_open": True,
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
        "cube_to_native_g15_label:",
        payload["cube_to_native_g15_label"],
    )
    print(
        "mapped_cube_edge_count:",
        len(mapped_cube_edges),
    )
    print(
        "native_quotient_edge_count:",
        len(quotient_edges),
    )
    print(
        "cube_triangle_count:",
        len(cube_triangles_to_g15),
    )
    print(
        "alignment_result:",
        payload["alignment_result"],
    )


if __name__ == "__main__":
    main()
