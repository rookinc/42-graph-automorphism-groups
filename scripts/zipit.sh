#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

PAPER_DIR="$PROJECT_DIR/paper42"
DIST_DIR="$PROJECT_DIR/dist"
BUILD_DIR="$PROJECT_DIR/build"
STAGE_DIR="$BUILD_DIR/overleaf_stage"

ZIP_BASENAME="${1:-project42_overleaf.zip}"
ZIP_PATH="$DIST_DIR/$ZIP_BASENAME"

echo "[info] project directory: $PROJECT_DIR"
echo "[info] manuscript:        $PAPER_DIR"
echo "[info] output:            $ZIP_PATH"

if [ ! -d "$PAPER_DIR" ]; then
    echo "[error] manuscript directory not found:"
    echo "        $PAPER_DIR"
    exit 1
fi

if ! command -v zip >/dev/null 2>&1; then
    echo "[error] zip command not found."
    echo "Run:"
    echo "    pkg install zip -y"
    exit 1
fi

rm -rf "$STAGE_DIR"
mkdir -p "$STAGE_DIR"
mkdir -p "$DIST_DIR"

echo "[info] staging manuscript..."
cp -R "$PAPER_DIR"/. "$STAGE_DIR"/

rm -f "$ZIP_PATH"

echo "[info] creating archive..."

(
    cd "$STAGE_DIR"

    zip -rq "$ZIP_PATH" . \
        -x \
        "*.aux" \
        "*.bbl" \
        "*.bcf" \
        "*.blg" \
        "*.fdb_latexmk" \
        "*.fls" \
        "*.log" \
        "*.out" \
        "*.run.xml" \
        "*.synctex.gz" \
        "*.toc" \
        "*.lof" \
        "*.lot" \
        "*.nav" \
        "*.snm" \
        "*.vrb" \
        "*.xdv" \
        "*.pdf" \
        ".DS_Store"
)

echo "[ok] wrote:"
echo "     $ZIP_PATH"

echo
ls -lh "$ZIP_PATH"

echo
echo "[info] archive contents:"
unzip -l "$ZIP_PATH"

echo
echo "[info] cleaning staging directory..."
rm -rf "$STAGE_DIR"

echo "[ok] staging directory removed"
echo
echo "status: overleaf_zip_written"
