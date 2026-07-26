#!/usr/bin/env python3
"""Classify the derived series and abelianization of the lifted G60 group."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

LIFT_SOURCE = (
    ROOT / "artifacts/json/"
    "native_g30_automorphism_lifts_to_g60_032.json"
)

GROUP_SOURCE = (
    ROOT / "artifacts/json/"
    "native_g60_lifted_automorphism_group_040.json"
)

OUTPUT = (
    ROOT / "artifacts/json/"
    "native_g60_lifted_group_extension_type_041.json"
)


def identity(size):
    return tuple(range(size))


def compose(left, right):
    return tuple(left[right[index]] for index in range(len(left)))


def inverse(permutation):
    result = [None] * len(permutation)
    for source, target in enumerate(permutation):
        result[target] = source
    return tuple(result)


def closure(generators):
    generators = tuple(generators)
    unit = identity(len(generators[0]))
    expanded = tuple(dict.fromkeys(
        generators + tuple(inverse(g) for g in generators)
    ))

    subgroup = {unit}
    frontier = [unit]

    while frontier:
        current = frontier.pop()
        for generator in expanded:
            product = compose(generator, current)
            if product not in subgroup:
                subgroup.add(product)
                frontier.append(product)

    return frozenset(subgroup)


def greedy_generators(group):
    group = frozenset(group)
    unit = identity(len(next(iter(group))))
    generators = []
    generated = frozenset({unit})

    while generated != group:
        candidate = next(element for element in group if element not in generated)
        generators.append(candidate)
        generated = closure(generators)

    return tuple(generators)


def commutator(left, right):
    return compose(
        compose(compose(inverse(left), inverse(right)), left),
        right,
    )


def derived_subgroup(group):
    ambient_generators = greedy_generators(group)

    seeds = {
        commutator(left, right)
        for left in ambient_generators
        for right in ambient_generators
    }

    ambient = tuple(dict.fromkeys(
        ambient_generators
        + tuple(inverse(generator) for generator in ambient_generators)
    ))

    normal_generators = set(seeds)

    while True:
        subgroup = closure(tuple(normal_generators))
        expanded = set(normal_generators)

        for element in subgroup:
            for generator in ambient:
                expanded.add(compose(
                    compose(generator, element),
                    inverse(generator),
                ))

        if expanded <= subgroup:
            return subgroup

        normal_generators = expanded


def cosets(group, subgroup):
    unseen = set(group)
    rows = []

    while unseen:
        representative = next(iter(unseen))
        coset = frozenset(
            compose(representative, element)
            for element in subgroup
        )
        rows.append(coset)
        unseen -= coset

    return rows


def quotient_element_order(coset_index, multiplication, identity_index):
    current = identity_index

    for order in range(1, 20):
        current = multiplication[current][coset_index]
        if current == identity_index:
            return order

    raise RuntimeError("quotient order exceeded bound")


def main():
    lift_source = json.loads(LIFT_SOURCE.read_text())
    group_source = json.loads(GROUP_SOURCE.read_text())

    group = frozenset(
        tuple(lift["permutation"])
        for row in lift_source["lift_rows"]
        for lift in row["lifts"]
    )

    derived = derived_subgroup(group)
    second_derived = derived_subgroup(derived)

    quotient_cosets = cosets(group, derived)
    element_to_coset = {
        element: index
        for index, coset in enumerate(quotient_cosets)
        for element in coset
    }

    representatives = [next(iter(coset)) for coset in quotient_cosets]

    multiplication = [
        [
            element_to_coset[compose(left, right)]
            for right in representatives
        ]
        for left in representatives
    ]

    unit = identity(60)
    identity_index = element_to_coset[unit]

    quotient_orders = sorted(
        quotient_element_order(
            index,
            multiplication,
            identity_index,
        )
        for index in range(len(quotient_cosets))
    )

    abelianization_type = (
        "C2_x_C2"
        if quotient_orders == [1, 2, 2, 2]
        else "C4"
        if quotient_orders == [1, 2, 4, 4]
        else "unclassified"
    )

    checks = {
        "lift_source_audit_pass": lift_source["audit_pass"],
        "group_source_audit_pass": group_source["audit_pass"],
        "group_order_is_480": len(group) == 480,
        "derived_order_is_120": len(derived) == 120,
        "second_derived_order_is_60": len(second_derived) == 60,
        "abelianization_order_is_4": len(quotient_cosets) == 4,
        "abelianization_is_C2_x_C2": abelianization_type == "C2_x_C2",
    }

    output = {
        "certificate_id": "native_g60_lifted_group_extension_type_041",
        "audit_pass": all(checks.values()),
        "lift_source": str(LIFT_SOURCE.relative_to(ROOT)),
        "group_source": str(GROUP_SOURCE.relative_to(ROOT)),
        "group_order": len(group),
        "derived_subgroup_order": len(derived),
        "second_derived_subgroup_order": len(second_derived),
        "abelianization_order": len(quotient_cosets),
        "abelianization_element_orders": quotient_orders,
        "abelianization_type": abelianization_type,
        "checks": checks,
        "classification_result": (
            "The lifted G60 automorphism group has derived subgroup of "
            "order 120, second derived subgroup of order 60, and "
            "abelianization C2 x C2."
        ),
        "boundary": (
            "This receipt classifies the derived series and abelianization "
            "of the constructed lifted group. It does not independently "
            "enumerate all native graph automorphisms."
        ),
    }

    OUTPUT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")

    print("OUT ==")
    print(f"output: {OUTPUT}")
    print(f"audit_pass: {output['audit_pass']}")
    print(f"group_order: {output['group_order']}")
    print(f"derived_subgroup_order: {output['derived_subgroup_order']}")
    print(
        "second_derived_subgroup_order: "
        f"{output['second_derived_subgroup_order']}"
    )
    print(f"abelianization_type: {output['abelianization_type']}")
    print(
        "abelianization_element_orders: "
        f"{output['abelianization_element_orders']}"
    )


if __name__ == "__main__":
    main()
