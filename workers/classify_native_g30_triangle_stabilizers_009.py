#!/usr/bin/env python3
"""Classify native G30 triangle stabilizer groups."""

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
    / "native_g30_triangle_stabilizers_009.json"
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


def image_of_triangle(triangle, permutation):
    return tuple(sorted(
        permutation[vertex]
        for vertex in triangle
    ))


def triangle_stabilizer(triangle, group):
    return frozenset(
        element
        for element in group
        if image_of_triangle(triangle, element) == triangle
    )


def order_profile(group):
    return dict(sorted(
        Counter(
            permutation_order(element)
            for element in group
        ).items()
    ))


def center(group):
    return frozenset(
        element
        for element in group
        if all(
            compose(element, other)
            == compose(other, element)
            for other in group
        )
    )


def derived_subgroup(group, identity):
    commutators = {
        commutator(left, right)
        for left in group
        for right in group
    }

    return generated_subgroup(
        commutators,
        identity,
    )


def classify_group(group, identity):
    profile = order_profile(group)
    group_center = center(group)
    derived = derived_subgroup(group, identity)

    if (
        len(group) == 12
        and profile == {1: 1, 2: 7, 3: 2, 6: 2}
        and len(group_center) == 2
        and len(derived) == 3
    ):
        group_type = "S3_x_C2"
    elif (
        len(group) == 12
        and profile == {1: 1, 2: 3, 3: 8}
        and len(group_center) == 1
        and len(derived) == 4
    ):
        group_type = "A4"
    elif (
        len(group) == 6
        and profile == {1: 1, 2: 3, 3: 2}
        and len(group_center) == 1
        and len(derived) == 3
    ):
        group_type = "S3"
    elif (
        len(group) == 6
        and profile == {1: 1, 2: 1, 3: 2, 6: 2}
    ):
        group_type = "C6"
    else:
        group_type = "unclassified"

    return {
        "order": len(group),
        "element_order_profile": {
            str(order): count
            for order, count in profile.items()
        },
        "center_order": len(group_center),
        "derived_subgroup_order": len(derived),
        "abelianization_order": (
            len(group) // len(derived)
        ),
        "abstract_group_type": group_type,
        "elements": [
            list(element)
            for element in sorted(group)
        ],
    }


def main():
    action_source = json.loads(ACTION_SOURCE.read_text())
    anatomy_source = json.loads(ANATOMY_SOURCE.read_text())
    complement_source = json.loads(
        COMPLEMENT_SOURCE.read_text()
    )
    parity_source = json.loads(PARITY_SOURCE.read_text())
    triangle_source = json.loads(
        TRIANGLE_SOURCE.read_text()
    )

    full_group = frozenset(
        tuple(row["permutation"])
        for row in action_source["automorphisms"]
    )

    degree = action_source["vertex_count"]
    identity = tuple(range(degree))

    central_involution = next(
        tuple(element)
        for element in anatomy_source["center"]
        if tuple(element) != identity
    )

    refined_type_by_index = {
        row["complement_index"]:
        row["refined_stabilizer_type"]
        for row in parity_source["complement_stabilizers"]
    }

    complements = {}

    for row in complement_source["complements"]:
        refined_type = refined_type_by_index[row["index"]]

        complements[refined_type] = frozenset(
            tuple(element)
            for element in row["elements"]
        )

    v4_group = complements["V4_mixed"]
    c4_group = complements["C4_odd_generated"]

    representative_triangle = tuple(
        triangle_source["triangles"][0]
    )

    full_stabilizer = triangle_stabilizer(
        representative_triangle,
        full_group,
    )

    v4_stabilizer = triangle_stabilizer(
        representative_triangle,
        v4_group,
    )

    c4_stabilizer = triangle_stabilizer(
        representative_triangle,
        c4_group,
    )

    full_classification = classify_group(
        full_stabilizer,
        identity,
    )

    v4_classification = classify_group(
        v4_stabilizer,
        identity,
    )

    c4_classification = classify_group(
        c4_stabilizer,
        identity,
    )

    c4_index_in_full = (
        len(full_stabilizer) // len(c4_stabilizer)
    )

    c4_normal_in_full = all(
        compose(
            compose(
                element,
                member,
            ),
            inverse(element),
        )
        in c4_stabilizer
        for element in full_stabilizer
        for member in c4_stabilizer
    )

    central_involution_fixes_triangle = (
        central_involution in full_stabilizer
    )

    full_minus_c4 = (
        full_stabilizer.difference(c4_stabilizer)
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
        "source_triangle_audit_pass": (
            triangle_source["audit_pass"]
        ),
        "full_triangle_stabilizer_order_is_12": (
            len(full_stabilizer) == 12
        ),
        "v4_triangle_stabilizer_order_is_12": (
            len(v4_stabilizer) == 12
        ),
        "c4_triangle_stabilizer_order_is_6": (
            len(c4_stabilizer) == 6
        ),
        "full_stabilizer_equals_v4_stabilizer": (
            full_stabilizer == v4_stabilizer
        ),
        "full_stabilizer_is_s3_times_c2": (
            full_classification["abstract_group_type"]
            == "S3_x_C2"
        ),
        "v4_stabilizer_is_s3_times_c2": (
            v4_classification["abstract_group_type"]
            == "S3_x_C2"
        ),
        "c4_stabilizer_is_s3": (
            c4_classification["abstract_group_type"]
            == "S3"
        ),
        "c4_stabilizer_has_index_2_in_full": (
            c4_index_in_full == 2
        ),
        "c4_stabilizer_is_normal_in_full": (
            c4_normal_in_full
        ),
        "central_involution_does_not_fix_triangle": (
            not central_involution_fixes_triangle
        ),
        "full_minus_c4_has_six_elements": (
            len(full_minus_c4) == 6
        ),
    }

    payload = {
        "certificate_id": (
            "native_g30_triangle_stabilizers_009"
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
        "triangle_source": str(
            TRIANGLE_SOURCE.relative_to(ROOT)
        ),
        "representative_triangle": list(
            representative_triangle
        ),
        "full_triangle_stabilizer": (
            full_classification
        ),
        "v4_mixed_complement_triangle_stabilizer": (
            v4_classification
        ),
        "c4_complement_triangle_stabilizer": (
            c4_classification
        ),
        "full_equals_v4_stabilizer": (
            full_stabilizer == v4_stabilizer
        ),
        "c4_stabilizer_index_in_full": (
            c4_index_in_full
        ),
        "c4_stabilizer_normal_in_full": (
            c4_normal_in_full
        ),
        "central_involution_fixes_representative_triangle": (
            central_involution_fixes_triangle
        ),
        "classification_result": (
            "The full stabilizer of a lifted triangle is "
            "S3 x C2 and is already contained in the "
            "V4_mixed S5 complement. The odd-generated C4 "
            "complement contributes a normal index-2 S3 "
            "triangle stabilizer."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "triangle_stabilizer_groups_classified": True,
            "full_and_v4_stabilizers_identified": True,
            "c4_index_two_stabilizer_identified": True,
            "local_permutation_action_on_triangle_vertices_open": True,
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
        "full_stabilizer:",
        full_classification["abstract_group_type"],
        full_classification["element_order_profile"],
    )
    print(
        "v4_stabilizer:",
        v4_classification["abstract_group_type"],
        v4_classification["element_order_profile"],
    )
    print(
        "c4_stabilizer:",
        c4_classification["abstract_group_type"],
        c4_classification["element_order_profile"],
    )
    print(
        "full_equals_v4_stabilizer:",
        payload["full_equals_v4_stabilizer"],
    )
    print(
        "c4_index_in_full:",
        payload["c4_stabilizer_index_in_full"],
    )
    print(
        "c4_normal_in_full:",
        payload["c4_stabilizer_normal_in_full"],
    )
    print(
        "classification_result:",
        payload["classification_result"],
    )


if __name__ == "__main__":
    main()
