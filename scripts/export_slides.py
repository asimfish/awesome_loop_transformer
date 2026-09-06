#!/usr/bin/env python3
"""Export slides/html/index.html to PDF (+ PNG previews) with headless Chromium.

Looks for a Chromium binary in this order: $CHROME_BIN, Playwright's chrome-headless-shell cache,
google-chrome / chromium on PATH. PNG previews are rendered from the PDF with PyMuPDF.

Usage: python3 scripts/export_slides.py
"""
import glob, os, pathlib, shutil, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
HTML = ROOT / "slides/html/index.html"
PDF = ROOT / "slides/html/awesome_loop_transformer_slides_zh.pdf"
PREVIEW_DIR = ROOT / "assets/figures"
PREVIEW_SLIDES = [1, 2, 5, 9, 10, 14]

def find_chrome():
    if os.environ.get("CHROME_BIN"):
        return os.environ["CHROME_BIN"]
    cands = glob.glob(os.path.expanduser("~/Library/Caches/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-mac-arm64/chrome-headless-shell"))
    cands += glob.glob(os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-*/chrome-linux/headless_shell"))
    for c in sorted(cands, reverse=True):
        if os.path.exists(c):
            return c
    for name in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        p = shutil.which(name)
        if p:
            return p
    mac = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    return mac if os.path.exists(mac) else None

def main():
    chrome = find_chrome()
    if not chrome:
        sys.exit("no Chromium found; set CHROME_BIN")
    cmd = [chrome, "--headless", "--disable-gpu", "--no-sandbox", "--allow-file-access-from-files",
           "--run-all-compositor-stages-before-draw", "--virtual-time-budget=5000", "--no-pdf-header-footer",
           f"--print-to-pdf={PDF}", HTML.as_uri()]
    subprocess.run(cmd, check=True, capture_output=True, timeout=180)
    print("wrote", PDF)
    try:
        import fitz
    except ImportError:
        print("PyMuPDF not installed; skipping PNG previews"); return
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(str(PDF))
    for n in PREVIEW_SLIDES:
        if n <= doc.page_count:
            doc[n - 1].get_pixmap(matrix=fitz.Matrix(1.4, 1.4)).save(str(PREVIEW_DIR / f"slide_{n:02d}.png"))
    print("previews:", PREVIEW_SLIDES)

if __name__ == "__main__":
    main()
