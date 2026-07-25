#!/usr/bin/env python3
"""Classify the two native G30 S5 vertex stabilizers by parity."""

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

COMPLEMENT_SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_s5_complement_classification_004.json"
)

OUTPUT = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_stabilizer_parity_classification_005.json"
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


def permutation_order(permutation):
    identity = tuple(range(len(permutation)))
    current = identity
    order = 0

    while True:
        order += 1
        current = compose(permutation, current)

        if current == identity:
            return order


def main():
    action_source = json.loads(ACTION_SOURCE.read_text())
    complement_source = json.loads(
        COMPLEMENT_SOURCE.read_text()
    )

    group = frozenset(
        tuple(row["permutation"])
        for row in action_source["automorphisms"]
    )

    degree = action_source["vertex_count"]
    identity = tuple(range(degree))

    commutators = {
        commutator(left, right)
        for left in group
        for right in group
    }

    derived = generated_subgroup(
        commutators,
        identity,
    )

    rows = []

    for complement_row in complement_source["complements"]:
        complement = frozenset(
            tuple(element)
            for element in complement_row["elements"]
        )

        stabilizer = frozenset(
            element
            for element in complement
            if element[0] == 0
        )

        even_part = stabilizer.intersection(derived)
        odd_part = stabilizer.difference(derived)

        even_order_profile = Counter(
            permutation_order(element)
            for element in even_part
        )

        odd_order_profile = Counter(
            permutation_order(element)
            for element in odd_part
        )

        abstract_type = complement_row[
            "vertex_stabilizer_0_type"
        ]

        if (
            abstract_type == "V4"
            and len(even_part) == 2
            and len(odd_part) == 2
            and dict(sorted(even_order_profile.items()))
            == {1: 1, 2: 1}
            and dict(sorted(odd_order_profile.items()))
            == {2: 2}
        ):
            refined_type = "V4_mixed"
        elif (
            abstract_type == "V4"
            and len(even_part) == 4
            and len(odd_part) == 0
        ):
            refined_type = "V4_even"
        elif (
            abstract_type == "C4"
            and len(even_part) == 2
            and len(odd_part) == 2
            and dict(sorted(even_order_profile.items()))
            == {1: 1, 2: 1}
            and dict(sorted(odd_order_profile.items()))
            == {4: 2}
        ):
            refined_type = "C4_odd_generated"
        else:
            refined_type = "unclassified"

        rows.append({
            "complement_index": complement_row["index"],
            "abstract_stabilizer_type": abstract_type,
            "refined_stabilizer_type": refined_type,
            "stabilizer_order": len(stabilizer),
            "even_part_order": len(even_part),
            "odd_part_order": len(odd_part),
            "even_element_order_profile": {
                str(order): count
                for order, count in sorted(
                    even_order_profile.items()
                )
            },
            "odd_element_order_profile": {
                str(order): count
                for order, count in sorted(
                    odd_order_profile.items()
                )
            },
            "stabilizer_elements": [
                {
                    "permutation": list(element),
                    "order": permutation_order(element),
                    "parity_class": (
                        "even"
                        if element in derived
                        else "odd"
                    ),
                }
                for element in sorted(stabilizer)
            ],
        })

    refined_type_counts = Counter(
        row["refined_stabilizer_type"]
        for row in rows
    )

    checks = {
        "source_action_audit_pass": (
            action_source["audit_pass"]
        ),
        "source_complement_audit_pass": (
            complement_source["audit_pass"]
        ),
        "derived_subgroup_order_is_60": (
            len(derived) == 60
        ),
        "two_complements_classified": len(rows) == 2,
        "one_stabilizer_is_v4_mixed": (
            refined_type_counts["V4_mixed"] == 1
        ),
        "no_stabilizer_is_v4_even": (
            refined_type_counts["V4_even"] == 0
        ),
        "one_stabilizer_is_odd_generated_c4": (
            refined_type_counts["C4_odd_generated"] == 1
        ),
        "no_unclassified_stabilizer": (
            refined_type_counts["unclassified"] == 0
        ),
    }

    payload = {
        "certificate_id": (
            "native_g30_stabilizer_parity_classification_005"
        ),
        "action_source": str(
            ACTION_SOURCE.relative_to(ROOT)
        ),
        "complement_source": str(
            COMPLEMENT_SOURCE.relative_to(ROOT)
        ),
        "derived_subgroup_order": len(derived),
        "refined_stabilizer_type_counts": dict(
            sorted(refined_type_counts.items())
        ),
        "complement_stabilizers": rows,
        "homogeneous_space_identification": (
            "V(native G30) is S5 / V4_mixed "
            "under the V4-stabilizer complement"
        ),
        "companion_action_identification": (
            "The second transitive S5 complement has an "
            "odd-generated C4 vertex stabilizer"
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "v4_mixed_label_derived": True,
            "c4_parity_structure_derived": True,
            "c4_geometric_object_not_yet_identified": True,
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
        "refined_stabilizer_type_counts:",
        payload["refined_stabilizer_type_counts"],
    )

    for row in rows:
        print(
            "complement",
            row["complement_index"],
            "refined type:",
            row["refined_stabilizer_type"],
            "even:",
            row["even_element_order_profile"],
            "odd:",
            row["odd_element_order_profile"],
        )

    print(
        "homogeneous_space_identification:",
        payload["homogeneous_space_identification"],
    )
    print(
        "companion_action_identification:",
        payload["companion_action_identification"],
    )


if __name__ == "__main__":
    main()
