"""Regenerate the English README and browser from data/papers.csv."""
from pathlib import Path
import runpy

if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).resolve().parents[1] / "scripts/build_site.py"), run_name="__main__")
