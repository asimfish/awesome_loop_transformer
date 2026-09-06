#!/usr/bin/env bash
# Translate the core papers into Chinese with SuperTranslate (layout-preserving),
# then run the object-level QA inspector on every output.
#
# Usage:
#   export PAPER_CHINA_DEEPSEEK_API_KEY=...        # never pass the key on the command line
#   export SUPER_TRANSLATE_HOME=/path/to/super_translate   # https://github.com/asimfish/super_translate
#   bash scripts/translate_papers.sh [arxiv_id ...]
#
# Outputs: papers/zh/<id>.zh.pdf, papers/zh/<id>.zh.inspect.json, papers/zh/<id>.zh.translation-cache.jsonl
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ST_HOME="${SUPER_TRANSLATE_HOME:-/tmp/skills/super_translate}"
PY="$ST_HOME/.venv/bin/python"
IN_DIR="$ROOT/papers/original"
OUT_DIR="$ROOT/papers/zh"
mkdir -p "$OUT_DIR"

if [ ! -x "$PY" ]; then
  echo "SuperTranslate venv not found at $PY. Run 'uv sync' inside $ST_HOME first." >&2
  exit 1
fi
if [ -z "${PAPER_CHINA_DEEPSEEK_API_KEY:-}" ]; then
  echo "PAPER_CHINA_DEEPSEEK_API_KEY is not set." >&2
  exit 1
fi

IDS=("$@")
if [ ${#IDS[@]} -eq 0 ]; then
  IDS=(2606.18023 2605.23872 1807.03819 2607.16051 2502.05171)
fi

cd "$ST_HOME"
for id in "${IDS[@]}"; do
  in="$IN_DIR/$id.pdf"
  out="$OUT_DIR/$id.zh.pdf"
  cache="$OUT_DIR/$id.zh.translation-cache.jsonl"
  report="$OUT_DIR/$id.zh.inspect.json"
  echo "=== [$(date +%H:%M:%S)] translate $id"
  "$PY" -m pdf_zh_translator translate "$in" "$out" \
    --api-mode deepseek \
    --api-key-env PAPER_CHINA_DEEPSEEK_API_KEY \
    --preserve-graphics-text \
    --cache-file "$cache" \
    --timeout 120 --retries 3
  echo "=== [$(date +%H:%M:%S)] inspect $id"
  set +e
  "$PY" -m pdf_zh_translator inspect "$in" "$out" --json-out "$report"
  rc=$?
  set -e
  echo "=== inspect exit=$rc -> $report"
done
echo "=== all done"
