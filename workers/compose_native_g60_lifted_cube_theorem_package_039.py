#!/usr/bin/env python3
"""Compose the native G60 lifted-cube theorem package."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SOURCE_PATHS = [
    ROOT / "artifacts/json/native_g30_automorphism_lifts_to_g60_032.json",
    ROOT / "artifacts/json/native_g60_lifted_cube_preimages_033.json",
    ROOT / "artifacts/json/native_g60_lifted_cube_twist_directions_034.json",
    ROOT / "artifacts/json/native_g60_twist_center_partner_law_035.json",
    ROOT / "artifacts/json/native_g60_endpoint_twist_commutator_law_036.json",
    ROOT / "artifacts/json/native_g60_cube_dihedral_reflections_037.json",
    ROOT / "artifacts/json/native_g60_cube_reflection_affine_plane_038.json",
]

OUTPUT = (
    ROOT
    / "artifacts/json/"
    "native_g60_lifted_cube_theorem_package_039.json"
)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    sources = {
        path.stem: json.loads(path.read_text())
        for path in SOURCE_PATHS
    }

    receipts = [
        {
            "path": str(path.relative_to(ROOT)),
            "sha256": sha256(path),
            "certificate_id": sources[path.stem]["certificate_id"],
            "audit_pass": sources[path.stem]["audit_pass"],
        }
        for path in SOURCE_PATHS
    ]

    s032 = sources[
        "native_g30_automorphism_lifts_to_g60_032"
    ]
    s033 = sources[
        "native_g60_lifted_cube_preimages_033"
    ]
    s034 = sources[
        "native_g60_lifted_cube_twist_directions_034"
    ]
    s035 = sources[
        "native_g60_twist_center_partner_law_035"
    ]
    s036 = sources[
        "native_g60_endpoint_twist_commutator_law_036"
    ]
    s037 = sources[
        "native_g60_cube_dihedral_reflections_037"
    ]
    s038 = sources[
        "native_g60_cube_reflection_affine_plane_038"
    ]

    theorem_statements = [
        {
            "theorem_id": "T039-1",
            "statement": (
                "Every automorphism of G30 preserves the native "
                "G60 double-cover class and has exactly two lifts "
                "differing by the deck involution a."
            ),
            "evidence": [
                "native_g30_automorphism_lifts_to_g60_032"
            ],
        },
        {
            "theorem_id": "T039-2",
            "statement": (
                "The resulting lifted automorphism group contains "
                "480 explicitly constructed permutations of G60."
            ),
            "evidence": [
                "native_g30_automorphism_lifts_to_g60_032"
            ],
        },
        {
            "theorem_id": "T039-3",
            "statement": (
                "The full preimage of each of the fifteen affine "
                "C2^3 cubes has order 16 and abstract type D8 x C2."
            ),
            "evidence": [
                "native_g60_lifted_cube_preimages_033"
            ],
        },
        {
            "theorem_id": "T039-4",
            "statement": (
                "Each central extension 1 -> <a> -> E_tilde -> "
                "C2^3 -> 1 is non-split."
            ),
            "evidence": [
                "native_g60_lifted_cube_preimages_033"
            ],
        },
        {
            "theorem_id": "T039-5",
            "statement": (
                "Each downstairs cube has exactly two twisted "
                "directions whose lifts have order 4 and square a."
            ),
            "evidence": [
                "native_g60_lifted_cube_twist_directions_034"
            ],
        },
        {
            "theorem_id": "T039-6",
            "statement": (
                "The ten twisted directions are exactly zc, where "
                "c ranges over the ten six-fixed-point Petersen "
                "vertex centers and z is the central deck of G30."
            ),
            "evidence": [
                "native_g60_twist_center_partner_law_035"
            ],
        },
        {
            "theorem_id": "T039-7",
            "statement": (
                "The two endpoint twist lifts commute, each squares "
                "to a, and their product is an involution. They "
                "generate C4 x C2 rather than the D8 factor."
            ),
            "evidence": [
                "native_g60_endpoint_twist_commutator_law_036"
            ],
        },
        {
            "theorem_id": "T039-8",
            "statement": (
                "Each lifted cube has four downstairs reflection "
                "directions with involutory lifts that invert an "
                "endpoint order-4 twist."
            ),
            "evidence": [
                "native_g60_cube_dihedral_reflections_037"
            ],
        },
        {
            "theorem_id": "T039-9",
            "statement": (
                "For Petersen edge {u,v}, the reflection register is "
                "{z, c_u, c_v, z c_u c_v}, an affine plane inside "
                "the downstairs C2^3 cube."
            ),
            "evidence": [
                "native_g60_cube_reflection_affine_plane_038"
            ],
        },
    ]

    checks = {
        "all_sources_exist": all(
            path.exists()
            for path in SOURCE_PATHS
        ),
        "all_source_audits_pass": all(
            receipt["audit_pass"]
            for receipt in receipts
        ),
        "all_240_g30_automorphisms_lift": (
            s032["liftable_base_automorphism_count"] == 240
        ),
        "constructed_lift_count_is_480": (
            s032["distinct_g60_lift_count"] == 480
        ),
        "fifteen_preimages_are_d8_x_c2": (
            s033["abstract_group_type_profile"]
            == {"D8_x_C2": 15}
        ),
        "all_extensions_are_nonsplit": (
            s033["split_status_profile"]
            == {"false": 15}
        ),
        "two_twisted_directions_per_cube": (
            s034["twisted_direction_count_profile"]
            == {"2": 15}
        ),
        "ten_twisted_directions_total": (
            s034["distinct_twisted_downstairs_element_count"]
            == 10
        ),
        "twist_partner_law_passes": (
            s035["audit_pass"]
        ),
        "endpoint_twists_commute": (
            s036["commutator_profile_profile"]
            == [{
                "profile": [["identity", 4]],
                "cube_count": 15,
            }]
        ),
        "four_reflections_per_cube": (
            s037["reflection_candidate_count_profile"]
            == {"4": 15}
        ),
        "reflection_formula_matches_all_cubes": (
            s038["predicted_match_profile"]
            == {"true": 15}
        ),
        "reflection_registers_are_affine_planes": (
            s038["affine_plane_profile"]
            == {"true": 15}
        ),
    }

    payload = {
        "certificate_id": (
            "native_g60_lifted_cube_theorem_package_039"
        ),
        "title": (
            "Native G60 lifted-cube extension and reflection geometry"
        ),
        "source_receipts": receipts,
        "theorem_statements": theorem_statements,
        "summary_counts": {
            "g30_automorphism_count": 240,
            "constructed_g60_lift_count": 480,
            "downstairs_cube_count": 15,
            "downstairs_cube_type": "C2_x_C2_x_C2",
            "lifted_cube_preimage_order": 16,
            "lifted_cube_preimage_type": "D8_x_C2",
            "twisted_direction_count_per_cube": 2,
            "distinct_twisted_direction_count": 10,
            "reflection_direction_count_per_cube": 4,
            "distinct_edge_local_fourth_reflection_count": 15,
        },
        "local_presentation": {
            "deck": "a",
            "central_downstairs_direction": "z",
            "endpoint_centers": ["c_u", "c_v"],
            "endpoint_twists": ["t_u = z c_u", "t_v = z c_v"],
            "lift_relations": [
                "x_u^2 = a",
                "x_v^2 = a",
                "[x_u, x_v] = 1",
                "(x_u x_v)^2 = 1",
            ],
            "reflection_register": [
                "z",
                "c_u",
                "c_v",
                "z c_u c_v",
            ],
        },
        "theorem_result": (
            "The native G60 double cover lifts all 240 automorphisms "
            "of G30 to 480 explicit G60 automorphisms. Each of the "
            "fifteen affine C2^3 cubes has a non-split order-16 "
            "preimage isomorphic to D8 x C2. Its two Petersen endpoint "
            "twists lift to commuting order-4 elements squaring to "
            "the deck involution a. The four directions admitting "
            "dihedral reflection lifts form the affine plane "
            "{z, c_u, c_v, z c_u c_v}. Thus the Petersen endpoint "
            "geometry controls both the twist support and reflection "
            "geometry of every lifted cube."
        ),
        "checks": checks,
        "audit_pass": all(checks.values()),
        "boundary": {
            "finite_group_theorem_package": True,
            "all_g30_automorphisms_lift": True,
            "lifted_cube_extension_geometry_complete": True,
            "full_480_group_abstract_type_open": True,
            "full_aut_g60_equality_open": True,
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
        "source_receipt_count:",
        len(payload["source_receipts"]),
    )
    print(
        "theorem_statement_count:",
        len(payload["theorem_statements"]),
    )
    print(
        "summary_counts:",
        payload["summary_counts"],
    )
    print(
        "theorem_result:",
        payload["theorem_result"],
    )


if __name__ == "__main__":
    main()
