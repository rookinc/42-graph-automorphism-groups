#!/usr/bin/env python3
"""Derive the abstract anatomy of Aut(native G30)."""

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SOURCE = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_full_automorphism_action_001.json"
)

OUTPUT = (
    ROOT
    / "artifacts"
    / "json"
    / "native_g30_group_anatomy_002.json"
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
    generators = tuple(set(generators))

    if not generators:
        return frozenset((identity,))

    expanded_generators = tuple(
        set(generators)
        | {
            inverse(generator)
            for generator in generators
        }
    )

    subgroup = {identity}
    queue = [identity]

    while queue:
        current = queue.pop()

        for generator in expanded_generators:
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


def cosets(group, subgroup):
    unseen = set(group)
    rows = []

    while unseen:
        representative = min(unseen)
        coset = frozenset(
            compose(representative, element)
            for element in subgroup
        )

        rows.append(
            (
                representative,
                coset,
            )
        )

        unseen -= coset

    rows.sort(
        key=lambda row: row[0]
    )

    return tuple(rows)


def quotient_order_profile(group, center):
    quotient_cosets = cosets(group, center)

    element_to_coset = {}

    for index, (_, coset) in enumerate(quotient_cosets):
        for element in coset:
            element_to_coset[element] = index

    identity = tuple(range(len(next(iter(group)))))
    identity_coset = element_to_coset[identity]

    def quotient_element_order(representative):
        current = identity
        order = 0

        while True:
            order += 1
            current = compose(representative, current)

            if element_to_coset[current] == identity_coset:
                return order

    profile = Counter(
        quotient_element_order(representative)
        for representative, _ in quotient_cosets
    )

    return quotient_cosets, profile


def find_order_120_complement(
    group,
    center,
    identity,
):
    central_nonidentity = next(
        element
        for element in center
        if element != identity
    )

    candidates = tuple(
        element
        for element in group
        if element not in center
    )

    subgroup = frozenset((identity,))
    generators = []

    while len(subgroup) < 120:
        best = None

        for candidate in candidates:
            if candidate in subgroup:
                continue

            trial = generated_subgroup(
                tuple(generators) + (candidate,),
                identity,
            )

            if central_nonidentity in trial:
                continue

            if len(trial) > 120:
                continue

            if best is None or len(trial) > len(best[0]):
                best = (
                    trial,
                    candidate,
                )

        if best is None:
            return None, ()

        subgroup, generator = best
        generators.append(generator)

    if len(subgroup) != 120:
        return None, ()

    if subgroup.intersection(center) != {identity}:
        return None, ()

    return subgroup, tuple(generators)


def main():
    source = json.loads(SOURCE.read_text())

    group = tuple(
        tuple(row["permutation"])
        for row in source["automorphisms"]
    )

    group_set = frozenset(group)
    degree = source["vertex_count"]
    identity = tuple(range(degree))

    center = frozenset(
        permutation
        for permutation in group
        if all(
            compose(permutation, other)
            == compose(other, permutation)
            for other in group
        )
    )

    commutators = {
        commutator(left, right)
        for left in group
        for right in group
    }

    derived_subgroup = generated_subgroup(
        tuple(commutators),
        identity,
    )

    quotient_cosets, quotient_profile = (
        quotient_order_profile(
            group_set,
            center,
        )
    )

    complement, complement_generators = (
        find_order_120_complement(
            group_set,
            center,
            identity,
        )
    )

    complement_exists = complement is not None

    if complement_exists:
        complement_profile = Counter(
            permutation_order(element)
            for element in complement
        )

        product_set = {
            compose(left, right)
            for left in complement
            for right in center
        }
    else:
        complement_profile = Counter()
        product_set = set()

    expected_s5_profile = {
        1: 1,
        2: 25,
        3: 20,
        4: 30,
        5: 24,
        6: 20,
    }

    checks = {
        "source_audit_pass": source["audit_pass"],
        "group_order_is_240": len(group_set) == 240,
        "center_order_is_2": len(center) == 2,
        "derived_subgroup_order_is_60": (
            len(derived_subgroup) == 60
        ),
        "center_quotient_order_is_120": (
            len(quotient_cosets) == 120
        ),
        "center_quotient_profile_is_S5": (
            dict(sorted(quotient_profile.items()))
            == expected_s5_profile
        ),
        "order_120_complement_exists": complement_exists,
        "complement_profile_is_S5": (
            dict(sorted(complement_profile.items()))
            == expected_s5_profile
        ),
        "complement_intersects_center_trivially": (
            complement_exists
            and complement.intersection(center)
            == {identity}
        ),
        "complement_times_center_is_full_group": (
            complement_exists
            and product_set == set(group_set)
        ),
    }

    payload = {
        "certificate_id": (
            "native_g30_group_anatomy_002"
        ),
        "source": str(SOURCE.relative_to(ROOT)),
        "group_order": len(group_set),
        "center_order": len(center),
        "center": [
            list(permutation)
            for permutation in sorted(center)
        ],
        "derived_subgroup_order": len(derived_subgroup),
        "derived_subgroup_element_order_profile": {
            str(order): count
            for order, count in sorted(
                Counter(
                    permutation_order(element)
                    for element in derived_subgroup
                ).items()
            )
        },
        "center_quotient_order": len(quotient_cosets),
        "center_quotient_element_order_profile": {
            str(order): count
            for order, count in sorted(
                quotient_profile.items()
            )
        },
        "order_120_complement_exists": complement_exists,
        "complement_generator_count": len(
            complement_generators
        ),
        "complement_generators": [
            list(generator)
            for generator in complement_generators
        ],
        "complement_element_order_profile": {
            str(order): count
            for order, count in sorted(
                complement_profile.items()
            )
        },
        "abstract_group_identification": (
            "S5 x C2"
            if all(checks.values())
            else None
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "group_identified_from_explicit_action": True,
            "mixed_v4_homogeneous_space_proved": False,
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
    print("group_order:", payload["group_order"])
    print("center_order:", payload["center_order"])
    print(
        "derived_subgroup_order:",
        payload["derived_subgroup_order"],
    )
    print(
        "center_quotient_order:",
        payload["center_quotient_order"],
    )
    print(
        "order_120_complement_exists:",
        payload["order_120_complement_exists"],
    )
    print(
        "abstract_group_identification:",
        payload["abstract_group_identification"],
    )
    print(
        "center_quotient_profile:",
        payload[
            "center_quotient_element_order_profile"
        ],
    )
    print(
        "complement_profile:",
        payload[
            "complement_element_order_profile"
        ],
    )


if __name__ == "__main__":
    main()
