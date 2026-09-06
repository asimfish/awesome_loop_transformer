"""Export slides/html/index.html to PDF and a few PNG previews with Playwright (Chromium).

Usage: python scripts/export_slides.py  (needs `pip install playwright && playwright install chromium`)
"""
import pathlib, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[1]
HTML = ROOT / "slides/html/index.html"
PDF = ROOT / "slides/html/awesome_loop_transformer_slides_zh.pdf"
PREVIEW_DIR = ROOT / "assets/figures"
PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
PREVIEW_SLIDES = [1, 2, 5, 9, 10, 14]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 720}, device_scale_factor=1)
    page.goto(HTML.as_uri())
    page.wait_for_timeout(500)
    for n in PREVIEW_SLIDES:
        page.goto(HTML.as_uri() + f"#{n}")
        page.wait_for_timeout(300)
        page.screenshot(path=str(PREVIEW_DIR / f"slide_{n:02d}.png"), full_page=False)
    page.emulate_media(media="print")
    page.pdf(path=str(PDF), width="1280px", height="720px", print_background=True,
             margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}, prefer_css_page_size=True)
    browser.close()
print("wrote", PDF, "and previews", PREVIEW_SLIDES)
