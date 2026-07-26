#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]

AUDIT019 = Path(
    "/data/data/com.termux/files/home/dev/cori/research/"
    "mathematics/thalean-graph-theory/"
    "41-order-4-dodecahedral-residue/artifacts/json/"
    "a5_v4_k22_four_slot_alignment_audit_019.json"
)

OUTPUT = (
    ROOT
    / "artifacts/json"
    / "project42_kneser_label_bridge_045.json"
)


def canonical_edge(left: int, right: int) -> tuple[int, int]:
    return tuple(sorted((left, right)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def standard_petersen_edges() -> set[tuple[int, int]]:
    edges: set[tuple[int, int]] = set()

    for index in range(5):
        edges.add(canonical_edge(index, (index + 1) % 5))

    edges.update(
        canonical_edge(left, right)
        for left, right in (
            (5, 7),
            (7, 9),
            (9, 6),
            (6, 8),
            (8, 5),
        )
    )

    edges.update((index, index + 5) for index in range(5))
    return edges


def kneser_labels() -> tuple[str, ...]:
    return (
        "12",
        "13",
        "14",
        "15",
        "23",
        "24",
        "25",
        "34",
        "35",
        "45",
    )


def label_subset(label: str) -> frozenset[int]:
    return frozenset(int(character) for character in label)


def kneser_edges(
    labels: Iterable[str],
) -> set[tuple[str, str]]:
    labels = tuple(labels)

    return {
        tuple(sorted((left, right)))
        for left, right in itertools.combinations(labels, 2)
        if label_subset(left).isdisjoint(label_subset(right))
    }


def image_edges(
    mapping: dict[int, str],
    edges: Iterable[tuple[int, int]],
) -> set[tuple[str, str]]:
    return {
        tuple(sorted((mapping[left], mapping[right])))
        for left, right in edges
    }


def main() -> None:
    audit = json.loads(AUDIT019.read_text())

    if audit.get("audit_pass") is not True:
        raise SystemExit("Audit 019 does not pass")

    labels = kneser_labels()
    standard_edges = standard_petersen_edges()
    target_edges = kneser_edges(labels)

    valid_mappings: list[tuple[str, ...]] = []

    for image_tuple in itertools.permutations(labels):
        mapping = dict(enumerate(image_tuple))

        if image_edges(mapping, standard_edges) == target_edges:
            valid_mappings.append(image_tuple)

    valid_mappings.sort()

    if not valid_mappings:
        raise SystemExit("no Petersen-to-Kneser isomorphism found")

    selected = valid_mappings[0]
    standard_to_kneser = {
        index: selected[index]
        for index in range(10)
    }

    alignment_rows = sorted(
        audit["measurements"]["alignment_rows"],
        key=lambda row: int(row["native_g15_state"]),
    )

    label_rows = []

    for row in alignment_rows:
        base = int(row["native_g15_state"])
        left, right = (
            int(value)
            for value in row["standard_petersen_edge"]
        )

        edge_labels = sorted((
            standard_to_kneser[left],
            standard_to_kneser[right],
        ))

        label_rows.append({
            "base_index": base,
            "standard_petersen_edge": [left, right],
            "kneser_edge": edge_labels,
            "sheet_0_coordinate": {
                "edge": edge_labels,
                "sheet": 0,
            },
            "sheet_0_integer": 2 * base,
            "sheet_1_coordinate": {
                "edge": edge_labels,
                "sheet": 1,
            },
            "sheet_1_integer": 2 * base + 1,
        })

    checks = {
        "audit019_pass": audit.get("audit_pass") is True,
        "standard_vertex_count_10":
            len(standard_to_kneser) == 10,
        "standard_edge_count_15":
            len(standard_edges) == 15,
        "kneser_vertex_count_10":
            len(labels) == 10,
        "kneser_edge_count_15":
            len(target_edges) == 15,
        "isomorphism_count_120":
            len(valid_mappings) == 120,
        "selected_mapping_preserves_edges":
            image_edges(
                standard_to_kneser,
                standard_edges,
            ) == target_edges,
        "label_row_count_15":
            len(label_rows) == 15,
        "integer_labels_cover_0_through_29":
            sorted(
                integer
                for row in label_rows
                for integer in (
                    row["sheet_0_integer"],
                    row["sheet_1_integer"],
                )
            ) == list(range(30)),
    }

    payload = {
        "certificate_id":
            "project42_kneser_label_bridge_045",
        "audit_pass":
            all(checks.values()),
        "source": {
            "audit019_path": str(AUDIT019),
            "audit019_sha256": sha256(AUDIT019),
        },
        "conventions": {
            "standard_petersen_model":
                "outer 0-1-2-3-4 cycle, inner 5-7-9-6-8 cycle, spokes i-(i+5)",
            "kneser_vertex_order": list(labels),
            "kneser_adjacency":
                "two 2-subsets of {1,2,3,4,5} are adjacent iff disjoint",
            "selection_rule":
                "lexicographically least image tuple among all graph isomorphisms",
            "cover_integer_law":
                "integer_vertex = 2 * base_index + sheet",
        },
        "isomorphism_count": len(valid_mappings),
        "selected_standard_to_kneser": {
            str(index): standard_to_kneser[index]
            for index in range(10)
        },
        "label_rows": label_rows,
        "checks": checks,
        "boundary": {
            "project41_alignment_reused": True,
            "project41_supplied_kneser_label_map": False,
            "kneser_bridge_is_project42_editorial_coordinate_choice": True,
            "abstract_graph_or_group_claim_changed": False,
        },
    }

    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )

    print("output:", OUTPUT)
    print("audit_pass:", payload["audit_pass"])
    print("isomorphism_count:", len(valid_mappings))
    print("selected_mapping:", payload["selected_standard_to_kneser"])
    print("sha256:", sha256(OUTPUT))


if __name__ == "__main__":
    main()
