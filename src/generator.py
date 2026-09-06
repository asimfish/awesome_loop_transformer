"""Render README.md from data/header.md + data/papers.csv + data/footer.md.

Format follows Thinklab-SJTU/awesome-ml4co: a Content table, then one numbered list per category:
    N. **Title.** Venue, Year. [paper](link), [code](url)
        *Authors*
Papers listed under several categories use ';' in the category column. Core papers (note == "core")
are marked with a star, the way awesome-ml4co marks its own group's work.
"""
import csv, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV = ROOT / "data/papers.csv"
HEADER = ROOT / "data/header.md"
FOOTER = ROOT / "data/footer.md"
OUT = ROOT / "README.md"

CATEGORY_ORDER = [
    "Core Papers",
    "Surveys",
    "Foundations & Precursors",
    "Theory: Expressivity, ICL & Length Generalization",
    "Scaled Pretraining",
    "Efficiency: Latency, KV Cache & Quantization",
    "Stability & Training Theory",
    "Adaptive Computation & Halting",
    "Retrofitting & Training-Free",
    "Post-Training & RL for Looped Models",
    "Interpretability & Latent Dynamics",
    "Tiny Recursive Reasoners",
    "Applications & Cross-Modal",
    "Related: Latent Reasoning Beyond Looping",
]
STATIC_SECTIONS = ["Industry Reports & Threads", "Open Models"]  # rendered from footer.md

CORE_REPORTS = {  # arxiv id -> (zh report, en report, zh pdf)
    "1807.03819": ("reports/zh/01_universal_transformers.md", "reports/en/01_universal_transformers.md", "papers/zh/1807.03819.zh.pdf"),
    "2502.05171": ("reports/zh/02_recurrent_depth_huginn.md", "reports/en/02_recurrent_depth_huginn.md", "papers/zh/2502.05171.zh.pdf"),
    "2605.23872": ("reports/zh/03_training_free_looped.md", "reports/en/03_training_free_looped.md", "papers/zh/2605.23872.zh.pdf"),
    "2606.18023": ("reports/zh/04_loopcoder_v2.md", "reports/en/04_loopcoder_v2.md", "papers/zh/2606.18023.zh.pdf"),
    "2607.16051": ("reports/zh/05_loop_the_loopies.md", "reports/en/05_loop_the_loopies.md", "papers/zh/2607.16051.zh.pdf"),
}

def anchor(title: str) -> str:
    a = title.lower()
    a = re.sub(r"[^\w\s-]", "", a)
    return re.sub(r"\s+", "-", a.strip())

def load():
    with CSV.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))

def render_entry(i, r):
    title = r["title"].rstrip(".")
    end = "" if title.endswith(("!", "?")) else "."
    star = "⭐" if r.get("note") == "core" else ""
    links = [f"[paper]({r['link']})"]
    if r.get("code"):
        links.append(f"[code]({r['code']})")
    if r.get("arxiv") in CORE_REPORTS:
        zh, en, pdf = CORE_REPORTS[r["arxiv"]]
        links += [f"[report-zh]({zh})", f"[report-en]({en})", f"[中译PDF]({pdf})"]
    venue = r["publisher"]
    line = f"{i}. **{star}{title}{end}** {venue}, {r['year']}. " + ", ".join(links)
    if r.get("note") and r["note"] != "core":
        line += f" — *{r['note']}*"
    return line + f"\n\n    *{r['authors']}*\n"

def main():
    rows = load()
    by_cat = {c: [] for c in CATEGORY_ORDER}
    for r in rows:
        for c in [x.strip() for x in r["category"].split(";")]:
            if c not in by_cat:
                raise SystemExit(f"unknown category {c!r} for {r['title']}")
            by_cat[c].append(r)
    for c in by_cat:  # chronological within a section, core papers keep list order
        if c != "Core Papers":
            by_cat[c].sort(key=lambda r: (r.get("published") or str(r["year"])))

    out = [HEADER.read_text(encoding="utf-8").rstrip() + "\n\n"]
    # content table (two columns, like awesome-ml4co)
    out.append("## [Content](#content)\n\n<table>\n")
    sections = CATEGORY_ORDER + STATIC_SECTIONS
    for k in range(0, len(sections), 2):
        pair = sections[k:k+2]
        out.append("<tr>\n")
        for j, name in enumerate(pair):
            n = k + j + 1
            count = len(by_cat.get(name, []))
            label = f"{n}. {name}" + (f" ({count})" if count else "")
            out.append(f"\t<td>&emsp;<a href=#{anchor(name)}>{label}</a></td>\n")
        out.append("</tr>\n")
    out.append("</table>\n\n")
    for name in CATEGORY_ORDER:
        out.append(f"## [{name}](#content)\n\n")
        if name == "Core Papers":
            out.append("The five papers threaded together by the WeChat article / @nrehiew_ thread, in reading order. Each has a full report (ZH/EN) and a layout-preserving Chinese translation.\n\n")
        for i, r in enumerate(by_cat[name], 1):
            out.append(render_entry(i, r))
        out.append("\n")
    footer = FOOTER.read_text(encoding="utf-8")
    # make the footer's static sections link-anchored like the generated ones
    for name in STATIC_SECTIONS:
        footer = footer.replace(f"## {name}\n", f"## [{name}](#content)\n")
    out.append(footer.lstrip("\n"))
    OUT.write_text("".join(out), encoding="utf-8")
    total = len(rows)
    print(f"wrote {OUT} with {total} papers in {len(CATEGORY_ORDER)} categories")

if __name__ == "__main__":
    main()
