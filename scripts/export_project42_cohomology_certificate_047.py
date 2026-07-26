#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]

COVER_PATH = (
    ROOT
    / "sources/project41-paper42"
    / "project42_invariant_cover_square_certificate_032.json"
)

VOLTAGE_PATH = (
    ROOT
    / "sources/project41-paper42"
    / "project42_native_voltage_derivation_certificate_033.json"
)

ACTION_PATH = (
    ROOT
    / "sources/project41-paper42"
    / "project42_full_carrier_action_certificate_031.json"
)

OUTPUT = (
    ROOT
    / "artifacts/json"
    / "project42_cohomology_certificate_047.json"
)


Vector = tuple[int, ...]
Permutation = tuple[int, ...]
Edge = tuple[int, int]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_edge(left: int, right: int) -> Edge:
    return tuple(sorted((left, right)))


def xor(left: Vector, right: Vector) -> Vector:
    return tuple(a ^ b for a, b in zip(left, right))


def dot(left: Vector, right: Vector) -> int:
    value = 0

    for a, b in zip(left, right):
        value ^= a & b

    return value


def gf2_rank(rows: Iterable[Vector]) -> int:
    work = [
        list(row)
        for row in rows
        if any(row)
    ]

    if not work:
        return 0

    column_count = len(work[0])
    rank = 0

    for column in range(column_count):
        pivot = next(
            (
                row_index
                for row_index in range(rank, len(work))
                if work[row_index][column]
            ),
            None,
        )

        if pivot is None:
            continue

        work[rank], work[pivot] = work[pivot], work[rank]

        for row_index in range(len(work)):
            if row_index == rank:
                continue

            if work[row_index][column]:
                work[row_index] = [
                    a ^ b
                    for a, b in zip(
                        work[row_index],
                        work[rank],
                    )
                ]

        rank += 1

        if rank == len(work):
            break

    return rank


def greedy_independent_basis(
    vectors: Iterable[Vector],
) -> tuple[Vector, ...]:
    basis: list[Vector] = []
    rank = 0

    for vector in sorted(set(vectors)):
        candidate_rank = gf2_rank(basis + [vector])

        if candidate_rank > rank:
            basis.append(vector)
            rank = candidate_rank

    return tuple(basis)


def spanning_tree(
    vertex_count: int,
    edges: tuple[Edge, ...],
) -> tuple[Edge, ...]:
    parent = list(range(vertex_count))

    def find(value: int) -> int:
        while parent[value] != value:
            parent[value] = parent[parent[value]]
            value = parent[value]

        return value

    selected: list[Edge] = []

    for edge in edges:
        left, right = edge
        root_left = find(left)
        root_right = find(right)

        if root_left == root_right:
            continue

        parent[root_right] = root_left
        selected.append(edge)

    if len(selected) != vertex_count - 1:
        raise RuntimeError("base graph is not connected")

    return tuple(selected)


def tree_parent_data(
    vertex_count: int,
    tree_edges: tuple[Edge, ...],
    root: int,
) -> tuple[tuple[int | None, ...], tuple[int | None, ...]]:
    adjacency = {
        vertex: []
        for vertex in range(vertex_count)
    }

    for edge_index, (left, right) in enumerate(tree_edges):
        adjacency[left].append((right, edge_index))
        adjacency[right].append((left, edge_index))

    parent: list[int | None] = [None] * vertex_count
    parent_edge: list[int | None] = [None] * vertex_count
    parent[root] = root
    queue = [root]

    while queue:
        current = queue.pop(0)

        for neighbor, edge_index in sorted(adjacency[current]):
            if parent[neighbor] is not None:
                continue

            parent[neighbor] = current
            parent_edge[neighbor] = edge_index
            queue.append(neighbor)

    if any(value is None for value in parent):
        raise RuntimeError("tree traversal did not reach every vertex")

    return tuple(parent), tuple(parent_edge)


def canonicalize_cochain(
    vector: Vector,
    edge_order: tuple[Edge, ...],
    tree_edges: tuple[Edge, ...],
    root: int = 0,
) -> Vector:
    edge_to_index = {
        edge: index
        for index, edge in enumerate(edge_order)
    }

    parent, parent_edge = tree_parent_data(
        15,
        tree_edges,
        root,
    )

    tree_values = [
        vector[edge_to_index[edge]]
        for edge in tree_edges
    ]

    potentials = [0] * 15
    ordered_vertices = [root]
    queue = [root]

    children = {
        vertex: []
        for vertex in range(15)
    }

    for vertex in range(15):
        if vertex == root:
            continue

        parent_vertex = parent[vertex]

        if parent_vertex is None:
            raise RuntimeError("missing tree parent")

        children[parent_vertex].append(vertex)

    while queue:
        current = queue.pop(0)

        for child in sorted(children[current]):
            edge_position = parent_edge[child]

            if edge_position is None:
                raise RuntimeError("missing parent edge")

            potentials[child] = (
                potentials[current]
                ^ tree_values[edge_position]
            )

            ordered_vertices.append(child)
            queue.append(child)

    coboundary = tuple(
        potentials[left] ^ potentials[right]
        for left, right in edge_order
    )

    canonical = xor(vector, coboundary)

    if any(
        canonical[edge_to_index[edge]]
        for edge in tree_edges
    ):
        raise RuntimeError("tree gauge canonicalization failed")

    return canonical


def quotient_coordinates(
    vector: Vector,
    edge_order: tuple[Edge, ...],
    tree_edges: tuple[Edge, ...],
) -> Vector:
    canonical = canonicalize_cochain(
        vector,
        edge_order,
        tree_edges,
    )

    tree_set = set(tree_edges)

    return tuple(
        canonical[index]
        for index, edge in enumerate(edge_order)
        if edge not in tree_set
    )


def apply_base_permutation(
    vector: Vector,
    permutation: Permutation,
    edge_order: tuple[Edge, ...],
) -> Vector:
    edge_to_index = {
        edge: index
        for index, edge in enumerate(edge_order)
    }

    result = [0] * len(edge_order)

    for source_index, (left, right) in enumerate(edge_order):
        image = canonical_edge(
            permutation[left],
            permutation[right],
        )

        result[edge_to_index[image]] = vector[source_index]

    return tuple(result)


def induced_base_permutation(
    carrier_permutation: Permutation,
) -> Permutation:
    result = []

    for base in range(15):
        image_pair = {
            carrier_permutation[2 * base] // 2,
            carrier_permutation[2 * base + 1] // 2,
        }

        if len(image_pair) != 1:
            raise RuntimeError(
                "kernel automorphism does not preserve a natural fiber"
            )

        result.append(next(iter(image_pair)))

    if sorted(result) != list(range(15)):
        raise RuntimeError("induced base action is not a permutation")

    return tuple(result)


def simple_cycles_of_length(
    vertex_count: int,
    edges: tuple[Edge, ...],
    length: int,
) -> tuple[tuple[int, ...], ...]:
    adjacency = {
        vertex: set()
        for vertex in range(vertex_count)
    }

    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)

    cycles = set()

    def canonical_cycle(cycle: tuple[int, ...]) -> tuple[int, ...]:
        rotations = []

        for orientation in (
            cycle,
            tuple(reversed(cycle)),
        ):
            for shift in range(len(cycle)):
                rotations.append(
                    orientation[shift:]
                    + orientation[:shift]
                )

        return min(rotations)

    for start in range(vertex_count):
        stack = [(start, (start,))]

        while stack:
            current, path = stack.pop()

            if len(path) == length:
                if start in adjacency[current]:
                    cycles.add(canonical_cycle(path))
                continue

            for neighbor in sorted(adjacency[current], reverse=True):
                if neighbor in path:
                    continue

                stack.append((neighbor, path + (neighbor,)))

    return tuple(sorted(cycles))


def cycle_vector(
    cycle: tuple[int, ...],
    edge_order: tuple[Edge, ...],
) -> Vector:
    edge_set = {
        canonical_edge(
            cycle[index],
            cycle[(index + 1) % len(cycle)],
        )
        for index in range(len(cycle))
    }

    return tuple(
        1 if edge in edge_set else 0
        for edge in edge_order
    )


def vector_from_class(
    class_row: dict,
    edge_order: tuple[Edge, ...],
) -> Vector:
    bits = {
        canonical_edge(*row["edge"]): int(row["bit"])
        for row in class_row["voltage_rows"]
    }

    return tuple(bits[edge] for edge in edge_order)


def main() -> None:
    cover = json.loads(COVER_PATH.read_text())
    voltage = json.loads(VOLTAGE_PATH.read_text())
    action = json.loads(ACTION_PATH.read_text())

    if not (
        cover.get("audit_pass") is True
        and voltage.get("audit_pass") is True
        and action.get("audit_pass") is True
    ):
        raise SystemExit("one or more source certificates do not pass")

    edge_order = tuple(
        canonical_edge(*edge)
        for edge in cover["base_edges"]
    )

    if tuple(sorted(edge_order)) != edge_order:
        raise RuntimeError("base edge ordering is not lexicographic")

    edge_to_index = {
        edge: index
        for index, edge in enumerate(edge_order)
    }

    coboundary_matrix = tuple(
        tuple(
            1 if vertex in edge else 0
            for edge in edge_order
        )
        for vertex in range(15)
    )

    tree_edges = spanning_tree(15, edge_order)
    tree_set = set(tree_edges)

    cotree_edges = tuple(
        edge
        for edge in edge_order
        if edge not in tree_set
    )

    class_by_id = {
        row["class_id"]: row
        for row in cover["classes"]
    }

    voltage_vectors = {
        class_id: vector_from_class(
            class_by_id[class_id],
            edge_order,
        )
        for class_id in (
            "zero",
            "native",
            "alternative",
            "all_one",
        )
    }

    quotient_vectors = {
        class_id: quotient_coordinates(
            vector,
            edge_order,
            tree_edges,
        )
        for class_id, vector in voltage_vectors.items()
    }

    kernel_indices = tuple(
        action["derived"]["partition_action_kernel_indices"]
    )

    base_actions = tuple(sorted({
        induced_base_permutation(
            tuple(
                action["automorphisms"][index][
                    "carrier_permutation"
                ]
            )
        )
        for index in kernel_indices
    }))

    if len(base_actions) != 120:
        raise RuntimeError("induced base action does not have order 120")

    base_action_generators = []
    generated = {tuple(range(15))}

    def compose(left: Permutation, right: Permutation) -> Permutation:
        return tuple(left[right[index]] for index in range(len(left)))

    def generated_group(
        generators: list[Permutation],
    ) -> set[Permutation]:
        identity = tuple(range(15))
        group = {identity}
        queue = [identity]

        while queue:
            current = queue.pop()

            for generator in generators:
                candidate = compose(current, generator)

                if candidate not in group:
                    group.add(candidate)
                    queue.append(candidate)

        return group

    for candidate in base_actions:
        if candidate in generated:
            continue

        base_action_generators.append(candidate)
        generated = generated_group(base_action_generators)

        if len(generated) == 120:
            break

    if len(generated) != 120:
        raise RuntimeError("base action generators do not generate S5")

    fixed_coordinates = []

    for integer in range(1 << 16):
        coordinate = tuple(
            (integer >> index) & 1
            for index in range(16)
        )

        full_vector = [0] * 30

        for bit, edge in zip(coordinate, cotree_edges):
            full_vector[edge_to_index[edge]] = bit

        full_vector_tuple = tuple(full_vector)
        fixed = True

        for permutation in base_action_generators:
            image = apply_base_permutation(
                full_vector_tuple,
                permutation,
                edge_order,
            )

            image_coordinate = quotient_coordinates(
                image,
                edge_order,
                tree_edges,
            )

            if image_coordinate != coordinate:
                fixed = False
                break

        if fixed:
            fixed_coordinates.append(coordinate)

    fixed_coordinates = tuple(sorted(fixed_coordinates))

    triangles = simple_cycles_of_length(
        15,
        edge_order,
        3,
    )

    pentagons = simple_cycles_of_length(
        15,
        edge_order,
        5,
    )

    triangle_vectors = tuple(
        cycle_vector(cycle, edge_order)
        for cycle in triangles
    )

    alternative = voltage_vectors["alternative"]
    native = voltage_vectors["native"]

    selected_triangle = next(
        cycle
        for cycle in triangles
        if (
            dot(
                cycle_vector(cycle, edge_order),
                alternative,
            ) == 1
            and dot(
                cycle_vector(cycle, edge_order),
                native,
            ) == 0
        )
    )

    selected_pentagon = next(
        cycle
        for cycle in pentagons
        if (
            dot(
                cycle_vector(cycle, edge_order),
                alternative,
            ) == 0
            and dot(
                cycle_vector(cycle, edge_order),
                native,
            ) == 1
        )
    )

    selected_pentagon_orbit = tuple(sorted({
        tuple(
            permutation[vertex]
            for vertex in selected_pentagon
        )
        for permutation in base_actions
    }))

    selected_pentagon_orbit_vectors = tuple(
        cycle_vector(cycle, edge_order)
        for cycle in selected_pentagon_orbit
    )

    fixed_basis = greedy_independent_basis(
        fixed_coordinates
    )

    expected_fixed_set = {
        quotient_vectors["zero"],
        quotient_vectors["native"],
        quotient_vectors["alternative"],
        quotient_vectors["all_one"],
    }

    checks = {
        "cover_source_pass": cover.get("audit_pass") is True,
        "native_voltage_source_pass":
            voltage.get("audit_pass") is True,
        "full_action_source_pass":
            action.get("audit_pass") is True,
        "edge_count_30":
            len(edge_order) == 30,
        "vertex_count_15":
            len(coboundary_matrix) == 15,
        "coboundary_rank_14":
            gf2_rank(coboundary_matrix) == 14,
        "cohomology_dimension_16":
            len(cotree_edges) == 16,
        "base_action_order_120":
            len(base_actions) == 120,
        "fixed_class_count_4":
            len(fixed_coordinates) == 4,
        "fixed_dimension_2":
            len(fixed_basis) == 2,
        "fixed_classes_equal_cover_square":
            set(fixed_coordinates) == expected_fixed_set,
        "class_sum_native_plus_alternative_is_all_one":
            xor(
                quotient_vectors["native"],
                quotient_vectors["alternative"],
            ) == quotient_vectors["all_one"],
        "triangle_count_10":
            len(triangles) == 10,
        "triangle_span_rank_10":
            gf2_rank(triangle_vectors) == 10,
        "selected_triangle_coordinates_1_0":
            (
                dot(
                    cycle_vector(
                        selected_triangle,
                        edge_order,
                    ),
                    alternative,
                ),
                dot(
                    cycle_vector(
                        selected_triangle,
                        edge_order,
                    ),
                    native,
                ),
            ) == (1, 0),
        "selected_pentagon_coordinates_0_1":
            (
                dot(
                    cycle_vector(
                        selected_pentagon,
                        edge_order,
                    ),
                    alternative,
                ),
                dot(
                    cycle_vector(
                        selected_pentagon,
                        edge_order,
                    ),
                    native,
                ),
            ) == (0, 1),
        "triangle_plus_pentagon_orbit_rank_16":
            gf2_rank(
                triangle_vectors
                + selected_pentagon_orbit_vectors
            ) == 16,
        "four_voltage_vectors_have_length_30":
            all(
                len(vector) == 30
                for vector in voltage_vectors.values()
            ),
    }

    payload = {
        "certificate_id":
            "project42_cohomology_certificate_047",
        "audit_pass":
            all(checks.values()),
        "sources": {
            "cover_square": {
                "path": str(COVER_PATH.relative_to(ROOT)),
                "sha256": sha256(COVER_PATH),
            },
            "native_voltage": {
                "path": str(VOLTAGE_PATH.relative_to(ROOT)),
                "sha256": sha256(VOLTAGE_PATH),
            },
            "full_action": {
                "path": str(ACTION_PATH.relative_to(ROOT)),
                "sha256": sha256(ACTION_PATH),
            },
        },
        "edge_order": [list(edge) for edge in edge_order],
        "coboundary_matrix": [
            list(row)
            for row in coboundary_matrix
        ],
        "coboundary_rank": gf2_rank(coboundary_matrix),
        "spanning_tree_edges": [
            list(edge)
            for edge in tree_edges
        ],
        "cotree_edges": [
            list(edge)
            for edge in cotree_edges
        ],
        "cohomology_dimension": len(cotree_edges),
        "base_action_order": len(base_actions),
        "base_action_generator_count":
            len(base_action_generators),
        "base_action_generators": [
            list(permutation)
            for permutation in base_action_generators
        ],
        "fixed_subspace": {
            "dimension": len(fixed_basis),
            "coordinates": [
                list(vector)
                for vector in fixed_coordinates
            ],
            "basis": [
                list(vector)
                for vector in fixed_basis
            ],
        },
        "classes": {
            class_id: {
                "voltage_vector": list(
                    voltage_vectors[class_id]
                ),
                "cohomology_coordinates": list(
                    quotient_vectors[class_id]
                ),
                "test_coordinates": {
                    "triangle": dot(
                        cycle_vector(
                            selected_triangle,
                            edge_order,
                        ),
                        voltage_vectors[class_id],
                    ),
                    "pentagon": dot(
                        cycle_vector(
                            selected_pentagon,
                            edge_order,
                        ),
                        voltage_vectors[class_id],
                    ),
                },
            }
            for class_id in (
                "zero",
                "native",
                "alternative",
                "all_one",
            )
        },
        "test_cycles": {
            "triangle": {
                "vertices": list(selected_triangle),
                "edge_vector": list(
                    cycle_vector(
                        selected_triangle,
                        edge_order,
                    )
                ),
            },
            "pentagon": {
                "vertices": list(selected_pentagon),
                "edge_vector": list(
                    cycle_vector(
                        selected_pentagon,
                        edge_order,
                    )
                ),
                "orbit_size":
                    len(selected_pentagon_orbit),
            },
        },
        "cycle_span": {
            "triangle_count": len(triangles),
            "triangle_span_rank":
                gf2_rank(triangle_vectors),
            "triangle_plus_selected_pentagon_orbit_rank":
                gf2_rank(
                    triangle_vectors
                    + selected_pentagon_orbit_vectors
                ),
        },
        "checks": checks,
        "boundary": {
            "project41_explicit_cohomology_packet_found":
                False,
            "project42_deterministic_reconstruction":
                True,
            "uses_only_certified_graph_voltage_and_action_data":
                True,
            "abstract_cover_class_claim_changed":
                False,
            "physical_claim":
                False,
        },
    }

    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )

    print("output:", OUTPUT)
    print("audit_pass:", payload["audit_pass"])
    print("coboundary_rank:", payload["coboundary_rank"])
    print(
        "cohomology_dimension:",
        payload["cohomology_dimension"],
    )
    print(
        "fixed_dimension:",
        payload["fixed_subspace"]["dimension"],
    )
    print(
        "fixed_class_count:",
        len(payload["fixed_subspace"]["coordinates"]),
    )
    print(
        "selected_triangle:",
        payload["test_cycles"]["triangle"]["vertices"],
    )
    print(
        "selected_pentagon:",
        payload["test_cycles"]["pentagon"]["vertices"],
    )
    print(
        "triangle_span_rank:",
        payload["cycle_span"]["triangle_span_rank"],
    )
    print(
        "triangle_plus_pentagon_rank:",
        payload["cycle_span"][
            "triangle_plus_selected_pentagon_orbit_rank"
        ],
    )

    for class_id, row in payload["classes"].items():
        print(
            class_id,
            "test_coordinates",
            row["test_coordinates"],
        )

    print("sha256:", sha256(OUTPUT))


if __name__ == "__main__":
    main()
