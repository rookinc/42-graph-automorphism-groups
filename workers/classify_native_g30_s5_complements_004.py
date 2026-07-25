#!/usr/bin/env python3
"""Classify the S5 complements in Aut(native G30)."""

import json
from collections import Counter, deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

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

OUTPUT = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_s5_complement_classification_004.json"
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


def generated_subgroup(generators, identity):
    expanded = set(generators)

    expanded.update(
        inverse(generator)
        for generator in generators
    )

    subgroup = {identity}
    queue = deque([identity])

    while queue:
        current = queue.popleft()

        for generator in expanded:
            product = compose(generator, current)

            if product in subgroup:
                continue

            subgroup.add(product)
            queue.append(product)

    return frozenset(subgroup)


def commutator(left, right):
    return compose(
        compose(
            compose(
                inverse(left),
                inverse(right),
            ),
            left,
        ),
        right,
    )


def subgroup_order_profile(subgroup):
    return dict(sorted(
        Counter(
            permutation_order(element)
            for element in subgroup
        ).items()
    ))


def fixed_point_profile(subgroup, degree):
    return dict(sorted(
        Counter(
            sum(
                1
                for vertex in range(degree)
                if element[vertex] == vertex
            )
            for element in subgroup
        ).items()
    ))


def main():
    action_source = json.loads(ACTION_SOURCE.read_text())
    anatomy_source = json.loads(ANATOMY_SOURCE.read_text())

    group = frozenset(
        tuple(row["permutation"])
        for row in action_source["automorphisms"]
    )

    degree = action_source["vertex_count"]
    identity = tuple(range(degree))

    center = frozenset(
        tuple(permutation)
        for permutation in anatomy_source["center"]
    )

    central_involution = next(
        element
        for element in center
        if element != identity
    )

    commutators = {
        commutator(left, right)
        for left in group
        for right in group
    }

    derived = generated_subgroup(
        commutators,
        identity,
    )

    complements = set()

    for candidate in group:
        if candidate in derived:
            continue

        subgroup = generated_subgroup(
            tuple(derived) + (candidate,),
            identity,
        )

        if len(subgroup) != 120:
            continue

        if subgroup.intersection(center) != {identity}:
            continue

        complements.add(subgroup)

    complement_rows = []

    for index, complement in enumerate(
        sorted(
            complements,
            key=lambda subgroup: tuple(sorted(subgroup)),
        )
    ):
        orbit_0 = {
            element[0]
            for element in complement
        }

        stabilizer_0 = frozenset(
            element
            for element in complement
            if element[0] == 0
        )

        stabilizer_profile = subgroup_order_profile(
            stabilizer_0
        )

        if stabilizer_profile == {1: 1, 2: 3}:
            stabilizer_type = "V4"
        elif stabilizer_profile == {1: 1, 2: 1, 4: 2}:
            stabilizer_type = "C4"
        else:
            stabilizer_type = "other"

        sign_character_twist = frozenset(
            element
            if element in derived
            else compose(element, central_involution)
            for element in complement
        )

        complement_rows.append({
            "index": index,
            "order": len(complement),
            "element_order_profile": {
                str(order): count
                for order, count in subgroup_order_profile(
                    complement
                ).items()
            },
            "vertex_orbit_0_size": len(orbit_0),
            "vertex_stabilizer_0_order": len(stabilizer_0),
            "vertex_stabilizer_0_profile": {
                str(order): count
                for order, count in stabilizer_profile.items()
            },
            "vertex_stabilizer_0_type": stabilizer_type,
            "fixed_point_profile": {
                str(count): multiplicity
                for count, multiplicity in fixed_point_profile(
                    complement,
                    degree,
                ).items()
            },
            "sign_character_twist_is_another_complement": (
                sign_character_twist in complements
                and sign_character_twist != complement
            ),
            "elements": [
                list(element)
                for element in sorted(complement)
            ],
        })

    stabilizer_type_counts = Counter(
        row["vertex_stabilizer_0_type"]
        for row in complement_rows
    )

    expected_s5_profile = {
        "1": 1,
        "2": 25,
        "3": 20,
        "4": 30,
        "5": 24,
        "6": 20,
    }

    checks = {
        "source_action_audit_pass": (
            action_source["audit_pass"]
        ),
        "source_anatomy_audit_pass": (
            anatomy_source["audit_pass"]
        ),
        "group_order_is_240": len(group) == 240,
        "derived_subgroup_order_is_60": (
            len(derived) == 60
        ),
        "center_order_is_2": len(center) == 2,
        "s5_complement_count_is_2": (
            len(complement_rows) == 2
        ),
        "all_complements_have_s5_profile": all(
            row["element_order_profile"]
            == expected_s5_profile
            for row in complement_rows
        ),
        "all_complements_are_vertex_transitive": all(
            row["vertex_orbit_0_size"] == 30
            for row in complement_rows
        ),
        "one_complement_has_v4_stabilizer": (
            stabilizer_type_counts["V4"] == 1
        ),
        "one_complement_has_c4_stabilizer": (
            stabilizer_type_counts["C4"] == 1
        ),
        "sign_character_twist_exchanges_complements": all(
            row[
                "sign_character_twist_is_another_complement"
            ]
            for row in complement_rows
        ),
    }

    payload = {
        "certificate_id": (
            "native_g30_s5_complement_classification_004"
        ),
        "action_source": str(
            ACTION_SOURCE.relative_to(ROOT)
        ),
        "anatomy_source": str(
            ANATOMY_SOURCE.relative_to(ROOT)
        ),
        "group_order": len(group),
        "derived_subgroup_order": len(derived),
        "center_order": len(center),
        "s5_complement_count": len(complement_rows),
        "stabilizer_type_counts": dict(
            sorted(stabilizer_type_counts.items())
        ),
        "complements": complement_rows,
        "interpretation": (
            "Aut(native G30) has two transitive S5 complements, "
            "exchanged by the central sign-character twist: one "
            "has V4 vertex stabilizer and one has C4 vertex "
            "stabilizer."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "both_s5_complements_classified": True,
            "v4_stabilizer_mixed_label_proved": False,
            "c4_complement_geometric_role_proved": False,
            "triangle_action_analyzed": False,
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
        "s5_complement_count:",
        payload["s5_complement_count"],
    )
    print(
        "stabilizer_type_counts:",
        payload["stabilizer_type_counts"],
    )

    for row in complement_rows:
        print(
            "complement",
            row["index"],
            "stabilizer:",
            row["vertex_stabilizer_0_type"],
            row["vertex_stabilizer_0_profile"],
        )

    print("interpretation:", payload["interpretation"])


if __name__ == "__main__":
    main()
