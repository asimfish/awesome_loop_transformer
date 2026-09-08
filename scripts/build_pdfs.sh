#!/usr/bin/env bash
# Build the Chinese and English report PDFs (survey + five paper reports) with pandoc + XeLaTeX.
# Requires: pandoc >= 3, TeX Live with xelatex (xeCJK), macOS CJK fonts (or set CJK_FONT / CJK_SANS).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/reports/pdf"
mkdir -p "$OUT"
HDR="$ROOT/scripts/pandoc_header.tex"
CJK_FONT="${CJK_FONT:-Songti SC}"
CJK_SANS="${CJK_SANS:-PingFang SC}"
MAIN_FONT="${MAIN_FONT:-Times New Roman}"
SANS_FONT="${SANS_FONT:-Helvetica Neue}"
MONO_FONT="${MONO_FONT:-Menlo}"

common=(--toc --toc-depth=2 -H "$HDR"
        -V geometry:margin=2.2cm -V fontsize=10.5pt -V linkcolor=accent -V urlcolor=accent -V toccolor=accent
        -V mainfont="$MAIN_FONT" -V sansfont="$SANS_FONT" -V monofont="$MONO_FONT"
        -V colorlinks=true --syntax-highlighting=tango -f markdown+tex_math_dollars+pipe_tables+yaml_metadata_block)

pagebreak="$ROOT/scripts/_pagebreak.md"
printf '\n\\newpage\n\n' > "$pagebreak"

strip_yaml() {  # copy a markdown file without its leading YAML block
  python3 - "$1" "$2" <<'PY'
import sys
src,dst=sys.argv[1],sys.argv[2]
t=open(src,encoding='utf-8').read()
if t.startswith('---\n'):
    end=t.find('\n---\n',4)
    if end!=-1: t=t[end+5:]
open(dst,'w',encoding='utf-8').write(t)
PY
}

build() {  # lang out title subtitle files...
  local lang="$1"; shift
  local out="$1"; shift
  local title="$1"; shift
  local subtitle="$1"; shift
  local meta="$ROOT/scripts/_meta_$lang.md"
  printf -- '---\ntitle: "%s"\nsubtitle: "%s"\nauthor: "awesome_loop_transformer · https://github.com/asimfish/awesome_loop_transformer"\ndate: "2026-09-06"\n---\n\n' "$title" "$subtitle" > "$meta"
  local tmpdir; tmpdir="$(mktemp -d)"
  local inputs=("$meta")
  local first=1
  for f in "$@"; do
    if [ $first -eq 0 ]; then inputs+=("$pagebreak"); fi
    local b="$tmpdir/$(basename "$f")"
    strip_yaml "$f" "$b"
    inputs+=("$b"); first=0
  done
  local langopts=()
  if [ "$lang" = "zh" ]; then
    langopts=(-V CJKmainfont="$CJK_FONT" -V CJKsansfont="$CJK_SANS" -V lang=zh-CN)
  else
    langopts=(-V lang=en-US)
  fi
  echo "== building $out"
  # pandoc -> standalone TeX; drop the "\noalign{}" tokens pandoc emits inside longtable
  # (they trigger "Infinite glue shrinkage" with longtable >= 4.24), then 2x XeLaTeX for the TOC.
  local texname="report_$lang"
  pandoc "${inputs[@]}" "${common[@]}" "${langopts[@]}" --resource-path="$ROOT/reports/$lang:$ROOT/survey/$lang:$ROOT" -s -t latex -o "$tmpdir/$texname.tex"
  sed -i '' 's/\\noalign{}//g' "$tmpdir/$texname.tex"
  # image links are relative to the markdown files; make them absolute for the temp build dir
  sed -i '' "s#{\.\./\.\./assets/#{$ROOT/assets/#g" "$tmpdir/$texname.tex"
  # Run in non-stop mode: MiKTeX's longtable 4.24 raises a recoverable "Infinite glue shrinkage"
  # error whenever a table spans a page (TeX itself reports it is safe to proceed). Any other
  # LaTeX error ("!" lines not about that glue) is treated as fatal.
  ( cd "$tmpdir" && xelatex -interaction=nonstopmode "$texname.tex" >/dev/null 2>&1; \
                    xelatex -interaction=nonstopmode "$texname.tex" >/dev/null 2>&1 ) || true
  if grep -E "^!" "$tmpdir/$texname.log" | grep -vqE "Infinite glue shrinkage|Infinite shrink error"; then
    echo "   xelatex reported errors:"; grep -E "^!" "$tmpdir/$texname.log" | grep -vE "Infinite glue|Infinite shrink" | head -5; exit 1
  fi
  [ -f "$tmpdir/$texname.pdf" ] || { echo "   no PDF produced; see $tmpdir/$texname.log"; exit 1; }
  cp "$tmpdir/$texname.pdf" "$out"
  rm -rf "$tmpdir"
  echo "   -> $(du -h "$out" | cut -f1)  pages=$(python3 -c "import fitz,sys;print(fitz.open(sys.argv[1]).page_count)" "$out" 2>/dev/null || echo '?')"
}

build zh "$OUT/awesome_loop_transformer_report_zh.pdf" \
  "循环 Transformer 与循环深度：完整解读报告" \
  "GPT-6 Astra 背后的 Loop 技术 · 五篇核心论文深度解读与趋势洞察（2018–2026）" \
  "$ROOT/survey/zh/survey_zh.md" \
  "$ROOT/reports/zh/01_universal_transformers.md" \
  "$ROOT/reports/zh/02_recurrent_depth_huginn.md" \
  "$ROOT/reports/zh/03_training_free_looped.md" \
  "$ROOT/reports/zh/04_loopcoder_v2.md" \
  "$ROOT/reports/zh/05_loop_the_loopies.md"

build en "$OUT/awesome_loop_transformer_report_en.pdf" \
  "Looped Transformers and Recurrent Depth: The Full Report" \
  "The Loop technology behind GPT-6 Astra · five core papers in depth and trend insights (2018–2026)" \
  "$ROOT/survey/en/survey_en.md" \
  "$ROOT/reports/en/01_universal_transformers.md" \
  "$ROOT/reports/en/02_recurrent_depth_huginn.md" \
  "$ROOT/reports/en/03_training_free_looped.md" \
  "$ROOT/reports/en/04_loopcoder_v2.md" \
  "$ROOT/reports/en/05_loop_the_loopies.md"

build zh "$ROOT/survey/zh/survey_zh.pdf" \
  "循环 Transformer 与循环深度：从 Universal Transformer 到 GPT-6 Astra 的八年" \
  "五篇核心论文速览 · 六十余篇相关文献图谱 · 十条趋势洞察" \
  "$ROOT/survey/zh/survey_zh.md"

build en "$ROOT/survey/en/survey_en.pdf" \
  "Looped Transformers and Recurrent Depth: Eight Years from Universal Transformers to GPT-6 Astra" \
  "Five core papers · a map of sixty related works · ten trend insights" \
  "$ROOT/survey/en/survey_en.md"

rm -f "$pagebreak" "$ROOT"/scripts/_meta_*.md
echo "== done"
