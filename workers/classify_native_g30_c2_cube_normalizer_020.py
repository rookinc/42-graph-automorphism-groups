#!/usr/bin/env python3
"""Classify the normalizer of the local C2^3 subgroup in Aut(G30)."""

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

AUT_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_full_automorphism_action_001.json"
)

GROUP_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_generated_order8_subgroup_015.json"
)

ACTION_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_c2_cube_action_016.json"
)

WEIGHTED_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_weighted_orbit_skeleton_019.json"
)

OUTPUT = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_c2_cube_normalizer_020.json"
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


def conjugate(carrier, element):
    return compose(
        compose(carrier, element),
        inverse(carrier),
    )


def permutation_order(permutation):
    identity = tuple(range(len(permutation)))
    current = identity
    order = 0

    while True:
        order += 1
        current = compose(permutation, current)

        if current == identity:
            return order


def read_permutation_list(payload, candidate_keys):
    for key in candidate_keys:
        value = payload.get(key)

        if not isinstance(value, list) or not value:
            continue

        if all(
            isinstance(row, list)
            for row in value
        ):
            return tuple(
                tuple(row)
                for row in value
            )

        if all(
            isinstance(row, dict)
            and isinstance(row.get("permutation"), list)
            for row in value
        ):
            return tuple(
                tuple(row["permutation"])
                for row in value
            )

    raise KeyError(
        "No permutation list found under keys: "
        + ", ".join(candidate_keys)
    )


def main():
    aut_source = json.loads(AUT_SOURCE.read_text())
    group_source = json.loads(GROUP_SOURCE.read_text())
    action_source = json.loads(ACTION_SOURCE.read_text())
    weighted_source = json.loads(
        WEIGHTED_SOURCE.read_text()
    )

    full_group = frozenset(
        read_permutation_list(
            aut_source,
            (
                "automorphisms",
                "elements",
                "full_automorphism_group",
            ),
        )
    )

    cube_group = frozenset(
        tuple(element)
        for element in group_source["elements"]
    )

    orbit_rows = tuple(sorted(
        action_source["vertex_orbits"],
        key=lambda row: row["orbit_index"],
    ))

    vertex_orbits = tuple(
        frozenset(row["vertices"])
        for row in orbit_rows
    )

    orbit_lookup = {
        orbit: index
        for index, orbit in enumerate(vertex_orbits)
    }

    normalizer = frozenset(
        carrier
        for carrier in full_group
        if frozenset(
            conjugate(carrier, element)
            for element in cube_group
        )
        == cube_group
    )

    centralizer = frozenset(
        carrier
        for carrier in full_group
        if all(
            compose(carrier, element)
            == compose(element, carrier)
            for element in cube_group
        )
    )

    induced_rows = []

    for carrier in sorted(normalizer):
        induced = tuple(
            orbit_lookup[
                frozenset(
                    carrier[vertex]
                    for vertex in orbit
                )
            ]
            for orbit in vertex_orbits
        )

        induced_rows.append({
            "carrier": list(carrier),
            "carrier_order": permutation_order(
                carrier
            ),
            "induced_orbit_permutation": list(
                induced
            ),
            "induced_order": permutation_order(
                induced
            ),
        })

    induced_group = frozenset(
        tuple(row["induced_orbit_permutation"])
        for row in induced_rows
    )

    identity_on_orbits = tuple(
        range(len(vertex_orbits))
    )

    action_kernel = frozenset(
        tuple(row["carrier"])
        for row in induced_rows
        if tuple(row["induced_orbit_permutation"])
        == identity_on_orbits
    )

    target_weighted_group = frozenset(
        tuple(permutation)
        for permutation in weighted_source[
            "weighted_automorphisms"
        ]
    )

    weighted_swap = next(
        permutation
        for permutation in target_weighted_group
        if permutation != identity_on_orbits
    )

    swap_lifts = tuple(
        row
        for row in induced_rows
        if tuple(row["induced_orbit_permutation"])
        == weighted_swap
    )

    normalizer_order_profile = Counter(
        permutation_order(element)
        for element in normalizer
    )

    centralizer_order_profile = Counter(
        permutation_order(element)
        for element in centralizer
    )

    induced_order_profile = Counter(
        permutation_order(element)
        for element in induced_group
    )

    kernel_order_profile = Counter(
        permutation_order(element)
        for element in action_kernel
    )

    checks = {
        "group_source_audit_pass": (
            group_source["audit_pass"]
        ),
        "action_source_audit_pass": (
            action_source["audit_pass"]
        ),
        "weighted_source_audit_pass": (
            weighted_source["audit_pass"]
        ),
        "full_automorphism_group_order_is_240": (
            len(full_group) == 240
        ),
        "cube_group_order_is_8": (
            len(cube_group) == 8
        ),
        "cube_group_is_contained_in_normalizer": (
            cube_group.issubset(normalizer)
        ),
        "centralizer_is_contained_in_normalizer": (
            centralizer.issubset(normalizer)
        ),
        "induced_group_preserves_weighted_skeleton": (
            induced_group.issubset(
                target_weighted_group
            )
        ),
        "normalizer_kernel_image_formula_holds": (
            len(normalizer)
            == len(action_kernel)
            * len(induced_group)
        ),
        "weighted_arm_swap_has_a_lift": (
            len(swap_lifts) > 0
        ),
    }

    payload = {
        "certificate_id": (
            "native_g30_c2_cube_normalizer_020"
        ),
        "automorphism_source": str(
            AUT_SOURCE.relative_to(ROOT)
        ),
        "cube_group_source": str(
            GROUP_SOURCE.relative_to(ROOT)
        ),
        "orbit_action_source": str(
            ACTION_SOURCE.relative_to(ROOT)
        ),
        "weighted_skeleton_source": str(
            WEIGHTED_SOURCE.relative_to(ROOT)
        ),
        "full_automorphism_group_order": len(
            full_group
        ),
        "cube_group_order": len(cube_group),
        "normalizer_order": len(normalizer),
        "normalizer_element_order_profile": {
            str(order): count
            for order, count in sorted(
                normalizer_order_profile.items()
            )
        },
        "centralizer_order": len(centralizer),
        "centralizer_element_order_profile": {
            str(order): count
            for order, count in sorted(
                centralizer_order_profile.items()
            )
        },
        "induced_orbit_action_order": len(
            induced_group
        ),
        "induced_orbit_action_element_order_profile": {
            str(order): count
            for order, count in sorted(
                induced_order_profile.items()
            )
        },
        "induced_orbit_action": [
            list(permutation)
            for permutation in sorted(induced_group)
        ],
        "orbit_action_kernel_order": len(
            action_kernel
        ),
        "orbit_action_kernel_element_order_profile": {
            str(order): count
            for order, count in sorted(
                kernel_order_profile.items()
            )
        },
        "weighted_arm_swap": list(weighted_swap),
        "weighted_arm_swap_lift_count": len(
            swap_lifts
        ),
        "weighted_arm_swap_lifts": list(
            swap_lifts
        ),
        "normalizer_action_rows": induced_rows,
        "classification_result": (
            "The normalizer of the local C2^3 subgroup has "
            "been enumerated inside Aut(G30), together with "
            "its kernel and image on the six orbit blocks. "
            "The weighted quotient arm swap lifts exactly when "
            "weighted_arm_swap_lift_count is positive."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "cube_group_normalizer_classified": True,
            "cube_group_centralizer_classified": True,
            "orbit_action_kernel_classified": True,
            "weighted_arm_swap_lift_decided": True,
            "normalizer_abstract_group_type_open": True,
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
        "full_automorphism_group_order:",
        payload["full_automorphism_group_order"],
    )
    print("cube_group_order:", payload["cube_group_order"])
    print("normalizer_order:", payload["normalizer_order"])
    print(
        "normalizer_element_order_profile:",
        payload["normalizer_element_order_profile"],
    )
    print("centralizer_order:", payload["centralizer_order"])
    print(
        "centralizer_element_order_profile:",
        payload["centralizer_element_order_profile"],
    )
    print(
        "induced_orbit_action_order:",
        payload["induced_orbit_action_order"],
    )
    print(
        "induced_orbit_action:",
        payload["induced_orbit_action"],
    )
    print(
        "orbit_action_kernel_order:",
        payload["orbit_action_kernel_order"],
    )
    print(
        "weighted_arm_swap_lift_count:",
        payload["weighted_arm_swap_lift_count"],
    )
    print(
        "weighted_arm_swap_lift_orders:",
        [
            row["carrier_order"]
            for row in swap_lifts
        ],
    )
    print(
        "classification_result:",
        payload["classification_result"],
    )


if __name__ == "__main__":
    main()
