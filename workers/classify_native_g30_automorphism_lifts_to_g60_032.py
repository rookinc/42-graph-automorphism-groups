#!/usr/bin/env python3
"""Classify which native G30 automorphisms lift through G60 -> G30."""

import json
from collections import Counter, deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

AUT_SOURCE = (
    ROOT
    / "artifacts/json/"
    "native_g30_full_automorphism_action_001.json"
)

CUBE_SOURCE = (
    ROOT
    / "artifacts/json/"
    "native_g30_c2_cube_conjugacy_census_026.json"
)

BRIDGE_SOURCE = (
    ROOT
    / "sources/"
    "project42_g60_to_g30_a_quotient_certificate_035.json"
)

OUTPUT = (
    ROOT
    / "artifacts/json/"
    "native_g30_automorphism_lifts_to_g60_032.json"
)


def canonical_edge(left, right):
    return tuple(sorted((int(left), int(right))))


def permutation_order(permutation):
    seen = set()
    result = 1

    def lcm(left, right):
        a, b = left, right

        while b:
            a, b = b, a % b

        return left * right // a

    for start in range(len(permutation)):
        if start in seen:
            continue

        current = start
        cycle_length = 0

        while current not in seen:
            seen.add(current)
            current = permutation[current]
            cycle_length += 1

        result = lcm(result, cycle_length)

    return result


def compose(left, right):
    return tuple(
        left[right[index]]
        for index in range(len(left))
    )


def build_voltage_data(bridge):
    fibers = {
        int(row["g30_vertex"]): tuple(
            int(vertex)
            for vertex in row["g60_vertices"]
        )
        for row in bridge["g30_fibers_from_g60"]
    }

    vertex_to_sheet = {}

    for base_vertex, fiber in fibers.items():
        if len(fiber) != 2:
            raise RuntimeError(
                f"fiber {base_vertex} does not have size 2"
            )

        vertex_to_sheet[fiber[0]] = (
            base_vertex,
            0,
        )
        vertex_to_sheet[fiber[1]] = (
            base_vertex,
            1,
        )

    g60_edges = {
        canonical_edge(*edge)
        for edge in bridge["g60_edges"]
    }

    base_edges = {
        canonical_edge(*edge)
        for edge in bridge["quotient_edges"]
    }

    voltage = {}
    matching_rows = []

    for left, right in sorted(base_edges):
        cross_edges = []

        for left_sheet, left_vertex in enumerate(
            fibers[left]
        ):
            for right_sheet, right_vertex in enumerate(
                fibers[right]
            ):
                if canonical_edge(
                    left_vertex,
                    right_vertex,
                ) in g60_edges:
                    cross_edges.append(
                        (
                            left_sheet,
                            right_sheet,
                        )
                    )

        if len(cross_edges) != 2:
            raise RuntimeError(
                f"base edge {(left, right)} has "
                f"{len(cross_edges)} lifted edges"
            )

        sigma_values = {
            left_sheet ^ right_sheet
            for left_sheet, right_sheet
            in cross_edges
        }

        if len(sigma_values) != 1:
            raise RuntimeError(
                f"base edge {(left, right)} is not "
                "a consistent two-sheet matching"
            )

        sigma = next(iter(sigma_values))
        voltage[(left, right)] = sigma

        matching_rows.append({
            "g30_edge": [left, right],
            "voltage": sigma,
            "sheet_pairs": [
                [left_sheet, right_sheet]
                for left_sheet, right_sheet
                in sorted(cross_edges)
            ],
        })

    return (
        fibers,
        vertex_to_sheet,
        g60_edges,
        base_edges,
        voltage,
        matching_rows,
    )


def solve_lift_switch(
    base_permutation,
    base_edges,
    voltage,
):
    adjacency = {
        vertex: []
        for vertex in range(30)
    }

    for left, right in base_edges:
        mapped_edge = canonical_edge(
            base_permutation[left],
            base_permutation[right],
        )

        rhs = (
            voltage[(left, right)]
            ^ voltage[mapped_edge]
        )

        adjacency[left].append((right, rhs))
        adjacency[right].append((left, rhs))

    switch = {}
    component_count = 0

    for start in range(30):
        if start in switch:
            continue

        component_count += 1
        switch[start] = 0
        queue = deque([start])

        while queue:
            current = queue.popleft()

            for neighbor, rhs in adjacency[current]:
                expected = switch[current] ^ rhs

                if neighbor in switch:
                    if switch[neighbor] != expected:
                        return None, component_count
                    continue

                switch[neighbor] = expected
                queue.append(neighbor)

    return tuple(
        switch[vertex]
        for vertex in range(30)
    ), component_count


def construct_lift(
    base_permutation,
    switch,
    fibers,
):
    lifted = [None] * 60

    for base_vertex in range(30):
        mapped_base = base_permutation[base_vertex]

        for sheet in (0, 1):
            source_vertex = fibers[
                base_vertex
            ][sheet]

            mapped_sheet = (
                sheet
                ^ switch[base_vertex]
            )

            target_vertex = fibers[
                mapped_base
            ][mapped_sheet]

            lifted[source_vertex] = target_vertex

    return tuple(lifted)


def is_graph_automorphism(
    permutation,
    edge_set,
):
    mapped_edges = {
        canonical_edge(
            permutation[left],
            permutation[right],
        )
        for left, right in edge_set
    }

    return mapped_edges == edge_set


def main():
    aut_source = json.loads(
        AUT_SOURCE.read_text()
    )

    cube_source = json.loads(
        CUBE_SOURCE.read_text()
    )

    bridge = json.loads(
        BRIDGE_SOURCE.read_text()
    )

    (
        fibers,
        vertex_to_sheet,
        g60_edges,
        base_edges,
        voltage,
        matching_rows,
    ) = build_voltage_data(bridge)

    base_automorphisms = [
        tuple(row["permutation"])
        for row in aut_source["automorphisms"]
    ]

    base_index = {
        permutation: index
        for index, permutation
        in enumerate(base_automorphisms)
    }

    lift_rows = []
    liftable_base_permutations = []
    all_lifted_permutations = set()

    for aut_row in aut_source["automorphisms"]:
        base_index_value = int(aut_row["index"])
        base_permutation = tuple(
            aut_row["permutation"]
        )

        switch, component_count = (
            solve_lift_switch(
                base_permutation,
                base_edges,
                voltage,
            )
        )

        liftable = switch is not None
        lifted_permutations = []

        if liftable:
            liftable_base_permutations.append(
                base_permutation
            )

            first_lift = construct_lift(
                base_permutation,
                switch,
                fibers,
            )

            complement_switch = tuple(
                value ^ 1
                for value in switch
            )

            second_lift = construct_lift(
                base_permutation,
                complement_switch,
                fibers,
            )

            for lifted in (
                first_lift,
                second_lift,
            ):
                if not is_graph_automorphism(
                    lifted,
                    g60_edges,
                ):
                    raise RuntimeError(
                        "constructed lift is not a "
                        "G60 automorphism"
                    )

                all_lifted_permutations.add(
                    lifted
                )

                lifted_permutations.append({
                    "order": permutation_order(
                        lifted
                    ),
                    "permutation": list(
                        lifted
                    ),
                })

        lift_rows.append({
            "g30_automorphism_index": (
                base_index_value
            ),
            "g30_order": int(
                aut_row["order"]
            ),
            "g30_central": bool(
                aut_row["central"]
            ),
            "liftable": liftable,
            "cover_constraint_component_count": (
                component_count
            ),
            "switch_solution": (
                list(switch)
                if switch is not None
                else None
            ),
            "lift_count": len(
                lifted_permutations
            ),
            "lifts": lifted_permutations,
        })

    liftable_set = set(
        liftable_base_permutations
    )

    liftable_index_set = {
        base_index[permutation]
        for permutation in liftable_set
    }

    liftable_order_profile = Counter(
        permutation_order(permutation)
        for permutation in liftable_set
    )

    lifted_order_profile = Counter(
        permutation_order(permutation)
        for permutation
        in all_lifted_permutations
    )

    cube_rows = []

    for cube_row in cube_source["cube_rows"]:
        cube_elements = {
            tuple(element)
            for element in cube_row["elements"]
        }

        liftable_elements = (
            cube_elements
            & liftable_set
        )

        cube_rows.append({
            "cube_index": int(
                cube_row["cube_index"]
            ),
            "cube_order": len(
                cube_elements
            ),
            "liftable_element_count": len(
                liftable_elements
            ),
            "all_elements_liftable": (
                liftable_elements
                == cube_elements
            ),
            "liftable_g30_automorphism_indices": sorted(
                base_index[element]
                for element in liftable_elements
            ),
            "nonliftable_g30_automorphism_indices": sorted(
                base_index[element]
                for element
                in cube_elements - liftable_elements
            ),
        })

    cube_liftable_count_profile = Counter(
        row["liftable_element_count"]
        for row in cube_rows
    )

    identity30 = tuple(range(30))
    identity60 = tuple(range(60))

    deck_a = tuple(
        int(bridge["involution_a"][str(vertex)])
        for vertex in range(60)
    )

    identity_base_row = next(
        row
        for row in lift_rows
        if row["g30_automorphism_index"]
        == base_index[identity30]
    )

    identity_base_lifts = {
        tuple(row["permutation"])
        for row in identity_base_row["lifts"]
    }

    liftable_closed = all(
        compose(left, right) in liftable_set
        for left in liftable_set
        for right in liftable_set
    )

    checks = {
        "automorphism_source_audit_pass": (
            aut_source["audit_pass"]
        ),
        "cube_source_audit_pass": (
            cube_source["audit_pass"]
        ),
        "bridge_source_audit_pass": (
            bridge["audit_pass"]
        ),
        "base_automorphism_count_is_240": (
            len(base_automorphisms) == 240
        ),
        "cover_has_30_two_vertex_fibers": (
            len(fibers) == 30
            and all(
                len(fiber) == 2
                for fiber in fibers.values()
            )
        ),
        "cover_voltage_defined_on_60_edges": (
            len(voltage) == 60
        ),
        "each_liftable_base_automorphism_has_two_lifts": all(
            row["lift_count"] == 2
            for row in lift_rows
            if row["liftable"]
        ),
        "each_nonliftable_base_automorphism_has_zero_lifts": all(
            row["lift_count"] == 0
            for row in lift_rows
            if not row["liftable"]
        ),
        "all_constructed_lifts_are_distinct": (
            len(all_lifted_permutations)
            == 2 * len(liftable_set)
        ),
        "identity_base_lifts_are_identity_and_deck_a": (
            identity_base_lifts
            == {identity60, deck_a}
        ),
        "liftable_base_automorphisms_form_subgroup": (
            liftable_closed
        ),
        "all_cube_rows_account_for_eight_elements": all(
            row["cube_order"] == 8
            for row in cube_rows
        ),
    }

    payload = {
        "certificate_id": (
            "native_g30_automorphism_lifts_to_g60_032"
        ),
        "automorphism_source": str(
            AUT_SOURCE.relative_to(ROOT)
        ),
        "cube_source": str(
            CUBE_SOURCE.relative_to(ROOT)
        ),
        "bridge_source": str(
            BRIDGE_SOURCE.relative_to(ROOT)
        ),
        "cover_model": (
            "G60 is represented as a connected Z2 cover "
            "of G30 using the ordered two-vertex fibers "
            "exported by certificate 035. A G30 "
            "automorphism lifts exactly when its transformed "
            "edge-voltage function differs from the native "
            "voltage by a vertex coboundary."
        ),
        "base_automorphism_count": len(
            base_automorphisms
        ),
        "liftable_base_automorphism_count": len(
            liftable_set
        ),
        "nonliftable_base_automorphism_count": (
            len(base_automorphisms)
            - len(liftable_set)
        ),
        "distinct_g60_lift_count": len(
            all_lifted_permutations
        ),
        "liftable_base_order_profile": {
            str(order): count
            for order, count in sorted(
                liftable_order_profile.items()
            )
        },
        "lifted_g60_order_profile": {
            str(order): count
            for order, count in sorted(
                lifted_order_profile.items()
            )
        },
        "liftable_g30_automorphism_indices": sorted(
            liftable_index_set
        ),
        "cover_edge_matching_rows": (
            matching_rows
        ),
        "lift_rows": lift_rows,
        "cube_rows": cube_rows,
        "cube_liftable_element_count_profile": {
            str(count): multiplicity
            for count, multiplicity in sorted(
                cube_liftable_count_profile.items()
            )
        },
        "classification_result": (
            "The audit classifies the exact subgroup of "
            "Aut(G30) preserving the native G60 double-cover "
            "class. Each preserving automorphism has exactly "
            "two explicit lifts differing by the deck "
            "involution a. The fifteen intrinsic C2^3 cubes "
            "are classified by how many of their eight "
            "elements belong to this liftable subgroup."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "g30_liftable_subgroup_classified": True,
            "explicit_g60_lifts_constructed": True,
            "cube_element_liftability_classified": True,
            "lifted_cube_subgroups_not_yet_constructed": True,
            "full_aut_g60_identification_not_claimed": True,
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
        "base_automorphism_count:",
        payload["base_automorphism_count"],
    )
    print(
        "liftable_base_automorphism_count:",
        payload[
            "liftable_base_automorphism_count"
        ],
    )
    print(
        "nonliftable_base_automorphism_count:",
        payload[
            "nonliftable_base_automorphism_count"
        ],
    )
    print(
        "distinct_g60_lift_count:",
        payload["distinct_g60_lift_count"],
    )
    print(
        "liftable_base_order_profile:",
        payload[
            "liftable_base_order_profile"
        ],
    )
    print(
        "lifted_g60_order_profile:",
        payload[
            "lifted_g60_order_profile"
        ],
    )
    print(
        "cube_liftable_element_count_profile:",
        payload[
            "cube_liftable_element_count_profile"
        ],
    )

    for row in cube_rows:
        print(
            "cube",
            row["cube_index"],
            "liftable:",
            row["liftable_element_count"],
            "/",
            row["cube_order"],
        )

    print(
        "classification_result:",
        payload["classification_result"],
    )


if __name__ == "__main__":
    main()
