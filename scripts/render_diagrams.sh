#!/usr/bin/env bash
# Render assets/figures/diagrams/*.svg to 2x PNG with headless Chromium (set CHROME_BIN to override).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CH="${CHROME_BIN:-$(ls -d ~/Library/Caches/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-mac-arm64/chrome-headless-shell 2>/dev/null | sort | tail -1)}"
[ -x "$CH" ] || { echo "no Chromium found; set CHROME_BIN"; exit 1; }
for svg in "$ROOT"/assets/figures/diagrams/*.svg; do
  w=$(python3 -c "import re,sys;print(re.search(r'width=\"(\d+)\"',open(sys.argv[1]).read()).group(1))" "$svg")
  h=$(python3 -c "import re,sys;print(re.search(r'height=\"(\d+)\"',open(sys.argv[1]).read()).group(1))" "$svg")
  png="${svg%.svg}.png"
  "$CH" --headless --disable-gpu --no-sandbox --hide-scrollbars --force-device-scale-factor=2 \
        --window-size="${w},${h}" --screenshot="$png" "file://$svg" >/dev/null 2>&1
  echo "rendered $(basename "$png") (${w}x${h})"
done
