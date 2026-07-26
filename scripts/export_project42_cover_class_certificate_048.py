#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

COVER_PATH = (
    ROOT
    / "sources/project41-paper42"
    / "project42_invariant_cover_square_certificate_032.json"
)

COHOMOLOGY_PATH = (
    ROOT
    / "artifacts/json"
    / "project42_cohomology_certificate_047.json"
)

ORDER_PATH = (
    ROOT
    / "sources/project41-paper42"
    / "invariant_cover_square_automorphism_orders_audit_028m.json"
)

CLOSURE_PATH = (
    ROOT
    / "sources/project41-paper42"
    / "invariant_cover_square_closure_audit_028q.json"
)

OUTPUT = (
    ROOT
    / "artifacts/json"
    / "project42_cover_class_certificate_048.json"
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_edge_digest(edges: list[list[int]]) -> str:
    canonical = sorted(
        sorted((int(left), int(right)))
        for left, right in edges
    )

    payload = json.dumps(
        canonical,
        separators=(",", ":"),
    ).encode("ascii")

    return hashlib.sha256(payload).hexdigest()


def main() -> None:
    cover = json.loads(COVER_PATH.read_text())
    cohomology = json.loads(COHOMOLOGY_PATH.read_text())
    orders = json.loads(ORDER_PATH.read_text())
    closure = json.loads(CLOSURE_PATH.read_text())

    if not (
        cover.get("audit_pass") is True
        and cohomology.get("audit_pass") is True
        and orders.get("audit_pass") is True
        and closure.get("audit_pass") is True
    ):
        raise SystemExit("one or more source certificates do not pass")

    order_measurements = orders["measurements"]

    order_rows = {
        "zero": order_measurements["zero"],
        "native": order_measurements["native"],
        "alternative": order_measurements["alternative"],
        "all_one": {
            **order_measurements["all_one_initial_worker"],
            "full_aut_order":
                order_measurements["all_one_full_census"][
                    "automorphism_count"
                ],
            "exact_order_certificate": True,
        },
    }

    class_to_coordinates = {
        "zero": [0, 0],
        "native": [0, 1],
        "alternative": [1, 0],
        "all_one": [1, 1],
    }

    class_rows = []

    for source_row in cover["classes"]:
        class_id = source_row["class_id"]
        order_row = order_rows[class_id]
        graph_summary = order_row["graph_summary"]

        connected = len(source_row["component_sizes"]) == 1

        class_rows.append({
            "class_id": class_id,
            "class_coordinates":
                class_to_coordinates[class_id],
            "connected": connected,
            "component_sizes":
                source_row["component_sizes"],
            "bipartite":
                graph_summary["bipartite"],
            "triangle_count":
                source_row["triangle_count"],
            "odd_girth":
                graph_summary["odd_girth"],
            "cover_vertex_count":
                source_row["cover_vertex_count"],
            "cover_edge_count":
                source_row["cover_edge_count"],
            "automorphism_order":
                order_row["full_aut_order"],
            "automorphism_structure":
                order_row.get("Aut_structure"),
            "voltage_vector":
                cohomology["classes"][class_id][
                    "voltage_vector"
                ],
            "cohomology_coordinates":
                cohomology["classes"][class_id][
                    "cohomology_coordinates"
                ],
            "test_coordinates":
                cohomology["classes"][class_id][
                    "test_coordinates"
                ],
            "canonical_cover_edge_sha256":
                canonical_edge_digest(
                    source_row["cover_edges"]
                ),
            "cover_edges":
                sorted(
                    sorted((int(left), int(right)))
                    for left, right in source_row[
                        "cover_edges"
                    ]
                ),
        })

    class_rows.sort(
        key=lambda row: row["class_coordinates"]
    )

    checks = {
        "cover_source_pass":
            cover.get("audit_pass") is True,
        "cohomology_source_pass":
            cohomology.get("audit_pass") is True,
        "order_source_pass":
            orders.get("audit_pass") is True,
        "closure_source_pass":
            closure.get("audit_pass") is True,
        "class_count_4":
            len(class_rows) == 4,
        "coordinate_square_exact":
            [
                row["class_coordinates"]
                for row in class_rows
            ] == [
                [0, 0],
                [0, 1],
                [1, 0],
                [1, 1],
            ],
        "all_cover_vertex_counts_30":
            all(
                row["cover_vertex_count"] == 30
                for row in class_rows
            ),
        "all_cover_edge_counts_60":
            all(
                row["cover_edge_count"] == 60
                for row in class_rows
            ),
        "automorphism_orders_exact":
            {
                row["class_id"]:
                    row["automorphism_order"]
                for row in class_rows
            } == {
                "zero": 28800,
                "native": 240,
                "alternative": 240,
                "all_one": 720,
            },
        "all_one_is_unique_bipartite_class":
            [
                row["class_id"]
                for row in class_rows
                if row["bipartite"]
            ] == ["all_one"],
        "all_one_is_X":
            next(
                row
                for row in class_rows
                if row["class_id"] == "all_one"
            )["test_coordinates"] == {
                "triangle": 1,
                "pentagon": 1,
            },
        "voltage_vectors_length_30":
            all(
                len(row["voltage_vector"]) == 30
                for row in class_rows
            ),
        "cover_digests_unique":
            len({
                row["canonical_cover_edge_sha256"]
                for row in class_rows
            }) == 4,
    }

    payload = {
        "certificate_id":
            "project42_cover_class_certificate_048",
        "audit_pass":
            all(checks.values()),
        "sources": {
            "cover_square": {
                "path":
                    str(COVER_PATH.relative_to(ROOT)),
                "sha256":
                    sha256_file(COVER_PATH),
            },
            "cohomology": {
                "path":
                    str(COHOMOLOGY_PATH.relative_to(ROOT)),
                "sha256":
                    sha256_file(COHOMOLOGY_PATH),
            },
            "automorphism_orders": {
                "path":
                    str(ORDER_PATH.relative_to(ROOT)),
                "sha256":
                    sha256_file(ORDER_PATH),
            },
            "closure": {
                "path":
                    str(CLOSURE_PATH.relative_to(ROOT)),
                "sha256":
                    sha256_file(CLOSURE_PATH),
            },
        },
        "classes": class_rows,
        "checks": checks,
        "boundary": {
            "archived_G30_identified":
                closure["boundary"][
                    "archived_G30_identified"
                ],
            "connected_extension_splitting_for_native_and_alternative":
                closure["boundary"][
                    "connected_extension_splitting_for_native_and_alternative"
                ],
            "external_standard_graph_name_for_all_one":
                closure["boundary"][
                    "external_standard_graph_name_for_all_one"
                ],
            "historical_replay_used":
                closure["boundary"][
                    "historical_replay_used"
                ],
            "physics_claim":
                closure["boundary"]["physics_claim"],
            "abstract_cover_class_claim_changed":
                False,
        },
    }

    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True)
        + "\n"
    )

    print("output:", OUTPUT)
    print("audit_pass:", payload["audit_pass"])

    for row in class_rows:
        print(
            row["class_id"],
            "coordinates",
            row["class_coordinates"],
            "components",
            row["component_sizes"],
            "bipartite",
            row["bipartite"],
            "triangles",
            row["triangle_count"],
            "odd_girth",
            row["odd_girth"],
            "aut",
            row["automorphism_order"],
            "sha256",
            row["canonical_cover_edge_sha256"],
        )

    print("sha256:", sha256_file(OUTPUT))


if __name__ == "__main__":
    main()
