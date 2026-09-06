#!/usr/bin/env bash
# Build the editable PPTX deck with ppt-master (https://github.com/hugohe3/ppt-master), Quick Generate route.
#
#   export PPT_MASTER_HOME=/path/to/ppt-master        # git clone of the skill repo
#   # inside it: uv venv -p 3.12 .venv && uv pip install -p .venv/bin/python -r skills/ppt-master/requirements.txt
#   bash scripts/build_pptx.sh
#
# Steps: emit page SVGs (scripts/build_pptx_svgs.py) -> compact styles -> final quality gate -> SVG->DrawingML export.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PM="${PPT_MASTER_HOME:-/tmp/skills/ppt-master}"
PY="$PM/.venv/bin/python"
SKILL="$PM/skills/ppt-master"
[ -x "$PY" ] || { echo "ppt-master venv not found at $PY (python>=3.10 with its requirements.txt)"; exit 1; }

PROJ="$(ls -d "$PM"/projects/loop_transformer_ppt169_* 2>/dev/null | head -1 || true)"
if [ -z "$PROJ" ]; then
  ( cd "$SKILL" && "$PY" scripts/project_manager.py init loop_transformer --quick-generate --format ppt169 >/dev/null )
  PROJ="$(ls -d "$PM"/projects/loop_transformer_ppt169_* | head -1)"
fi
echo "== project: $PROJ"
python3 "$ROOT/scripts/build_pptx_svgs.py" --out "$PROJ/svg_output"
cd "$SKILL"
"$PY" scripts/compact_svg_styles.py "$PROJ/svg_output" --inplace >/dev/null
"$PY" scripts/svg_quality_checker.py "$PROJ" --quick-generate --canonical-authoring --stage final --json | grep -E "Fully passed|With errors"
OUT="$ROOT/slides/pptx/awesome_loop_transformer_slides_zh.pptx"
mkdir -p "$ROOT/slides/pptx/svg_output"
"$PY" scripts/svg_to_pptx.py "$PROJ" --quick-generate --no-notes -o "$OUT" | grep -E "POSTFLIGHT|Saved"
cp "$PROJ"/svg_output/*.svg "$ROOT/slides/pptx/svg_output/"
cp "$PROJ"/validation/awesome_loop_transformer_slides_zh.report.json "$ROOT/slides/pptx/export_report.json"
# optional preview (LibreOffice); PowerPoint honours wrap="none", LibreOffice needs Microsoft YaHei installed for a faithful render
if command -v soffice >/dev/null; then
  tmp="$(mktemp -d)"; soffice --headless --convert-to pdf --outdir "$tmp" "$OUT" >/dev/null 2>&1 || true
  [ -f "$tmp/awesome_loop_transformer_slides_zh.pdf" ] && cp "$tmp/awesome_loop_transformer_slides_zh.pdf" "$ROOT/slides/pptx/awesome_loop_transformer_slides_zh.preview.pdf"
  rm -rf "$tmp"
fi
echo "== done: $OUT"
