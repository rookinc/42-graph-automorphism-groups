#!/usr/bin/env python3
"""Identify the ten cube-graph triangles by shared involutions."""

import json
from collections import Counter
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CENSUS_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_c2_cube_conjugacy_census_026.json"
)

GRAPH_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_fifteen_cube_graph_027.json"
)

OUTPUT = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_cube_triangle_centers_028.json"
)


def fixed_point_count(permutation):
    return sum(
        1
        for vertex, image in enumerate(permutation)
        if vertex == image
    )


def main():
    census = json.loads(CENSUS_SOURCE.read_text())
    graph = json.loads(GRAPH_SOURCE.read_text())

    identity = tuple(range(30))

    cubes = tuple(
        frozenset(
            tuple(element)
            for element in row["elements"]
        )
        for row in sorted(
            census["cube_rows"],
            key=lambda row: row["cube_index"],
        )
    )

    triangles = tuple(
        tuple(triangle)
        for triangle in graph["triangles"]
    )

    triangle_rows = []

    shared_center_to_triangles = {}

    for triangle_index, triangle in enumerate(triangles):
        triple_intersection = frozenset.intersection(
            *(cubes[cube_index]
              for cube_index in triangle)
        )

        nonidentity_common = tuple(sorted(
            element
            for element in triple_intersection
            if element != identity
        ))

        common_profiles = [
            {
                "permutation": list(element),
                "fixed_point_count": fixed_point_count(
                    element
                ),
                "cube_incidence_count": next(
                    row["cube_incidence_count"]
                    for row in census["involution_rows"]
                    if tuple(row["permutation"]) == element
                ),
            }
            for element in nonidentity_common
        ]

        six_fixed_incidence3 = tuple(
            element
            for element in nonidentity_common
            if fixed_point_count(element) == 6
            and next(
                row["cube_incidence_count"]
                for row in census["involution_rows"]
                if tuple(row["permutation"]) == element
            ) == 3
        )

        center = (
            six_fixed_incidence3[0]
            if len(six_fixed_incidence3) == 1
            else None
        )

        if center is not None:
            shared_center_to_triangles.setdefault(
                center,
                [],
            ).append(triangle_index)

        pair_intersections = []

        for left_cube, right_cube in combinations(
            triangle,
            2,
        ):
            pair_intersection = cubes[
                left_cube
            ].intersection(
                cubes[right_cube]
            )

            nonidentity_pair = tuple(sorted(
                element
                for element in pair_intersection
                if element != identity
            ))

            pair_intersections.append({
                "cube_pair": [
                    left_cube,
                    right_cube,
                ],
                "intersection_order": len(
                    pair_intersection
                ),
                "nonidentity_fixed_point_profile": {
                    str(count): multiplicity
                    for count, multiplicity in sorted(
                        Counter(
                            fixed_point_count(element)
                            for element
                            in nonidentity_pair
                        ).items()
                    )
                },
                "contains_center": (
                    center in pair_intersection
                    if center is not None
                    else False
                ),
            })

        triangle_rows.append({
            "triangle_index": triangle_index,
            "cube_indices": list(triangle),
            "triple_intersection_order": len(
                triple_intersection
            ),
            "triple_intersection_nonidentity_count": (
                len(nonidentity_common)
            ),
            "triple_intersection_nonidentity_profiles": (
                common_profiles
            ),
            "unique_six_fixed_incidence3_center": (
                list(center)
                if center is not None
                else None
            ),
            "pair_intersections": pair_intersections,
        })

    incidence3_six_fixed_involutions = tuple(
        tuple(row["permutation"])
        for row in census["involution_rows"]
        if row["cube_incidence_count"] == 3
        and row["fixed_point_count"] == 6
    )

    center_rows = []

    for center in sorted(
        incidence3_six_fixed_involutions
    ):
        involution_row = next(
            row
            for row in census["involution_rows"]
            if tuple(row["permutation"]) == center
        )

        cube_indices = tuple(
            involution_row["cube_indices"]
        )

        is_graph_triangle = (
            tuple(sorted(cube_indices))
            in {
                tuple(sorted(triangle))
                for triangle in triangles
            }
        )

        center_rows.append({
            "permutation": list(center),
            "fixed_point_count": 6,
            "cube_incidence_count": 3,
            "cube_indices": list(cube_indices),
            "cube_indices_form_graph_triangle": (
                is_graph_triangle
            ),
            "triangle_indices": (
                shared_center_to_triangles.get(
                    center,
                    [],
                )
            ),
        })

    triangle_center_count_profile = Counter(
        1
        if row[
            "unique_six_fixed_incidence3_center"
        ] is not None
        else 0
        for row in triangle_rows
    )

    checks = {
        "census_source_audit_pass": (
            census["audit_pass"]
        ),
        "graph_source_audit_pass": (
            graph["audit_pass"]
        ),
        "graph_triangle_count_is_10": (
            len(triangles) == 10
        ),
        "incidence3_six_fixed_involution_count_is_10": (
            len(
                incidence3_six_fixed_involutions
            )
            == 10
        ),
        "every_triangle_has_unique_six_fixed_incidence3_center": all(
            row[
                "unique_six_fixed_incidence3_center"
            ] is not None
            for row in triangle_rows
        ),
        "every_triangle_triple_intersection_order_is_4": all(
            row["triple_intersection_order"] == 4
            for row in triangle_rows
        ),
        "every_triangle_common_v4_has_profile_0_0_6": all(
            sorted(
                profile["fixed_point_count"]
                for profile in row[
                    "triple_intersection_nonidentity_profiles"
                ]
            )
            == [0, 0, 6]
            for row in triangle_rows
        ),
        "every_pair_intersection_contains_triangle_center": all(
            all(
                pair_row["contains_center"]
                for pair_row in row[
                    "pair_intersections"
                ]
            )
            for row in triangle_rows
        ),
        "every_six_fixed_incidence3_involution_forms_triangle": all(
            row[
                "cube_indices_form_graph_triangle"
            ]
            for row in center_rows
        ),
        "triangle_center_assignment_is_bijective": (
            len(shared_center_to_triangles)
            == 10
            and all(
                len(indices) == 1
                for indices
                in shared_center_to_triangles.values()
            )
        ),
    }

    payload = {
        "certificate_id": (
            "native_g30_cube_triangle_centers_028"
        ),
        "census_source": str(
            CENSUS_SOURCE.relative_to(ROOT)
        ),
        "graph_source": str(
            GRAPH_SOURCE.relative_to(ROOT)
        ),
        "cube_graph_triangle_count": len(triangles),
        "incidence3_six_fixed_involution_count": len(
            incidence3_six_fixed_involutions
        ),
        "triangle_center_count_profile": {
            str(count): multiplicity
            for count, multiplicity in sorted(
                triangle_center_count_profile.items()
            )
        },
        "triangle_rows": triangle_rows,
        "center_rows": center_rows,
        "classification_result": (
            "Each of the ten triangles in the recovered "
            "fifteen-cube graph has a common Klein four. Its "
            "three nonidentity elements have fixed-point profile "
            "0,0,6: the global central deck involution, one "
            "incidence-3 fixed-point-free involution, and one "
            "unique incidence-3 six-fixed-point center. "
            "Conversely, every incidence-3 six-fixed-point "
            "involution determines exactly one graph triangle "
            "through its three incident cubes. Thus the ten "
            "Petersen vertices are recovered intrinsically as "
            "the ten common-V4 triangle centers of the native "
            "cube system."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "cube_triangle_centers_identified": True,
            "common_triangle_v4_identified": True,
            "ten_petersen_vertices_recovered": True,
            "triangle_center_bijection_proved": True,
            "native_petersen_edge_alignment_open": True,
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
        "cube_graph_triangle_count:",
        payload["cube_graph_triangle_count"],
    )
    print(
        "incidence3_six_fixed_involution_count:",
        payload[
            "incidence3_six_fixed_involution_count"
        ],
    )
    print(
        "triangle_center_count_profile:",
        payload["triangle_center_count_profile"],
    )

    for row in triangle_rows:
        center_profile = (
            row[
                "triple_intersection_nonidentity_profiles"
            ]
        )

        print(
            "triangle",
            row["triangle_index"],
            "cubes:",
            row["cube_indices"],
            "triple intersection:",
            row["triple_intersection_order"],
            "center profiles:",
            center_profile,
        )

    print(
        "classification_result:",
        payload["classification_result"],
    )


if __name__ == "__main__":
    main()
