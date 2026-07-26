#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

OUTPUT = (
    ROOT
    / "artifacts/json"
    / "project42_release_manifest_049.json"
)

APPENDIX = (
    ROOT
    / "paper42/appendices"
    / "app-f-manifest.tex"
)

APPENDIX_RELATIVE = Path(
    "paper42/appendices/app-f-manifest.tex"
)

SOURCE_DIR = ROOT / "sources/project41-paper42"

GENERATED_CERTIFICATES = [
    Path(
        "artifacts/json/"
        "project42_kneser_label_bridge_045.json"
    ),
    Path(
        "artifacts/json/"
        "project42_group_orbital_certificate_046.json"
    ),
    Path(
        "artifacts/json/"
        "project42_cohomology_certificate_047.json"
    ),
    Path(
        "artifacts/json/"
        "project42_cover_class_certificate_048.json"
    ),
]

EXPORTERS = [
    Path(
        "scripts/"
        "export_project42_kneser_label_bridge_045.py"
    ),
    Path(
        "scripts/"
        "export_project42_group_orbital_certificate_046.py"
    ),
    Path(
        "scripts/"
        "export_project42_cohomology_certificate_047.py"
    ),
    Path(
        "scripts/"
        "export_project42_cover_class_certificate_048.py"
    ),
    Path(
        "scripts/"
        "export_project42_release_manifest_049.py"
    ),
]

SUPPORT_FILES = [
    Path("scripts/zipit.sh"),
    Path("notes/source-ledger.md"),
    Path("README.md"),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def receipt(path: Path, category: str) -> dict:
    absolute = ROOT / path

    return {
        "category": category,
        "path": path.as_posix(),
        "size_bytes": absolute.stat().st_size,
        "sha256": sha256(absolute),
    }


def git_output(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    return result.stdout.strip()


def tex_escape_path(path: str) -> str:
    return path.replace("_", r"\_")


def wrap_digest(digest: str) -> str:
    return digest


def ledger_block(rows: list[dict]) -> str:
    lines = []

    for row in rows:
        lines.append(row["path"])
        lines.append(row["sha256"])
        lines.append("")

    return "\n".join(lines).rstrip()


def main() -> None:
    imported_sources = sorted(
        path.relative_to(ROOT)
        for path in SOURCE_DIR.iterdir()
        if path.is_file()
    )

    manuscript_files = sorted(
        path.relative_to(ROOT)
        for path in (ROOT / "paper42").rglob("*")
        if path.is_file()
        and path.relative_to(ROOT) != APPENDIX_RELATIVE
    )

    categories = {
        "imported_project41_sources": [
            receipt(path, "imported_project41_source")
            for path in imported_sources
        ],
        "generated_project42_certificates": [
            receipt(path, "generated_project42_certificate")
            for path in GENERATED_CERTIFICATES
        ],
        "exporter_scripts": [
            receipt(path, "exporter_script")
            for path in EXPORTERS
        ],
        "support_files": [
            receipt(path, "support_file")
            for path in SUPPORT_FILES
        ],
        "manuscript_files_excluding_appendix_f": [
            receipt(path, "manuscript_file")
            for path in manuscript_files
        ],
    }

    all_rows = [
        row
        for group in categories.values()
        for row in group
    ]

    checks = {
        "imported_source_count_17":
            len(categories[
                "imported_project41_sources"
            ]) == 17,
        "generated_certificate_count_4":
            len(categories[
                "generated_project42_certificates"
            ]) == 4,
        "exporter_count_5":
            len(categories["exporter_scripts"]) == 5,
        "support_file_count_3":
            len(categories["support_files"]) == 3,
        "manifest_paths_unique":
            len({
                row["path"]
                for row in all_rows
            }) == len(all_rows),
        "all_files_nonempty":
            all(
                row["size_bytes"] > 0
                for row in all_rows
            ),
        "all_digests_sha256_length":
            all(
                len(row["sha256"]) == 64
                for row in all_rows
            ),
        "appendix_f_excluded":
            APPENDIX_RELATIVE.as_posix()
            not in {
                row["path"]
                for row in all_rows
            },
        "archive_excluded":
            all(
                not row["path"].endswith(".zip")
                for row in all_rows
            ),
    }

    payload = {
        "certificate_id":
            "project42_release_manifest_049",
        "audit_pass":
            all(checks.values()),
        "record_identity": {
            "project": "Project 42",
            "repository_project":
                "42-graph-automorphism-groups",
            "original_evidence_baseline": "1604b16",
            "generation_head": git_output(
                "rev-parse",
                "HEAD",
            ),
            "generation_head_short": git_output(
                "rev-parse",
                "--short",
                "HEAD",
            ),
            "preprint_doi":
                "10.5281/zenodo.21480350",
            "author": "Scott Allen Cave",
            "affiliation": (
                "Center of Recursive Inquiry (CoRI), "
                "Matsqui Territory, Abbotsford, "
                "British Columbia, Canada"
            ),
        },
        "categories": categories,
        "counts": {
            key: len(rows)
            for key, rows in categories.items()
        },
        "total_embedded_receipt_count":
            len(all_rows),
        "checks": checks,
        "boundary": {
            "appendix_f_hash_embedded":
                False,
            "appendix_f_excluded_to_avoid_self_reference":
                True,
            "overleaf_archive_hash_embedded":
                False,
            "overleaf_archive_requires_external_release_manifest":
                True,
            "release_commit_finalized":
                False,
            "archive_generated_by":
                "scripts/zipit.sh",
            "expected_archive_path":
                "dist/project42_overleaf.zip",
            "historical_source_ledger_has_digest_entries":
                False,
            "physical_claim":
                False,
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

    if payload["audit_pass"] is not True:
        raise SystemExit(
            "release manifest certificate does not pass"
        )

    manifest_digest = sha256(OUTPUT)

    imported_block = ledger_block(
        categories["imported_project41_sources"]
    )

    certificate_block = ledger_block(
        categories[
            "generated_project42_certificates"
        ]
    )

    exporter_block = ledger_block(
        categories["exporter_scripts"]
    )

    support_block = ledger_block(
        categories["support_files"]
    )

    manuscript_block = ledger_block(
        categories[
            "manuscript_files_excluding_appendix_f"
        ]
    )

    appendix_text = r"""\section{Reproducibility manifest}

\subsection{Record identity}

\begin{tabular}{ll}
\toprule
Field & Value\\
\midrule
Project & Project 42\\
Repository project &
\texttt{42-graph-automorphism-groups}\\
Original evidence baseline & \texttt{1604b16}\\
Manifest generation head &
\texttt{""" + payload["record_identity"][
        "generation_head_short"
    ] + r"""}\\
Preprint DOI & \texttt{10.5281/zenodo.21480350}\\
Author & Scott Allen Cave\\
Affiliation &
Center of Recursive Inquiry (CoRI), Matsqui Territory, Abbotsford,
British Columbia, Canada\\
\bottomrule
\end{tabular}

\subsection{Manifest scope}

Certificate \(049\) records filesystem-derived SHA-256 receipts for the
authoritative imported Project 41 packet, generated Project 42
certificates \(045\)--\(048\), every exporter used to create certificates
\(045\)--\(049\), the packaging script, the preserved source-ledger note,
the repository README, and every manuscript file except this appendix.

Appendix F is excluded from its own embedded ledger to avoid
self-reference. The Overleaf archive is also excluded because an archive
cannot contain its own final digest. The release commit and archive
SHA-256 digest therefore belong to the external release manifest created
after the final commit and packaging step.

\subsection{Imported Project 41 sources}

\begin{verbatim}
""" + imported_block + r"""
\end{verbatim}

\subsection{Generated Project 42 certificates}

\begin{verbatim}
""" + certificate_block + r"""
\end{verbatim}

\subsection{Exporter scripts}

\begin{verbatim}
""" + exporter_block + r"""
\end{verbatim}

\subsection{Support and packaging files}

\begin{verbatim}
""" + support_block + r"""
\end{verbatim}

\subsection{Manuscript source ledger}

The following receipts cover every file beneath
\texttt{paper42/} except
\texttt{paper42/appendices/app-f-manifest.tex}.

\begin{verbatim}
""" + manuscript_block + r"""
\end{verbatim}

\subsection{Manifest certificate}

The machine-readable manifest is

\begin{verbatim}
artifacts/json/project42_release_manifest_049.json
\end{verbatim}

with SHA-256 digest

\begin{verbatim}
""" + manifest_digest + r"""
\end{verbatim}

At generation time it contained
""" + str(payload["total_embedded_receipt_count"]) + r"""
file receipts and passed every internal consistency check.

\subsection{External release boundary}

After the manuscript changes are committed, the release procedure is:

\begin{enumerate}

\item run \texttt{scripts/zipit.sh};

\item compute the SHA-256 digest of
\texttt{dist/project42\_overleaf.zip};

\item record the final Git commit and archive digest in an external
release manifest; and

\item verify the archive listing against the staged
\texttt{paper42/} tree.

\end{enumerate}

The external release manifest is deliberately not embedded in the archive
whose digest it records.
"""

    APPENDIX.write_text(appendix_text)

    print("certificate:", OUTPUT)
    print("appendix:", APPENDIX)
    print("audit_pass:", payload["audit_pass"])
    print(
        "total_embedded_receipt_count:",
        payload["total_embedded_receipt_count"],
    )
    print("manifest_sha256:", manifest_digest)
    print("counts:", payload["counts"])
    print("checks:", payload["checks"])
    print("boundary:", payload["boundary"])


if __name__ == "__main__":
    main()
