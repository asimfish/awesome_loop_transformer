"""Render README.md from data/header.md + data/papers.csv + data/footer.md, and README_zh.md from data/readme_zh.md.

Format follows Thinklab-SJTU/awesome-ml4co: a Content table, then one numbered list per category:
    N. **Title** `Venue Year` · [paper](link) · [code](url)<br><sub>Authors</sub>
Papers listed under several categories use ';' in the category column. Core papers (note == "core")
are marked with a star, the way awesome-ml4co marks its own group's work; papers whose `added` date
equals the latest update are marked 🆕.

header.md / footer.md / readme_zh.md may use these placeholders, filled from papers.csv:
    {{N_PAPERS}} {{N_NEW}} {{N_CATEGORIES}} {{UPDATED}} {{UPDATED_BADGE}}
"""
import csv, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV = ROOT / "data/papers.csv"
HEADER = ROOT / "data/header.md"
FOOTER = ROOT / "data/footer.md"
OUT = ROOT / "README.md"
ZH_TEMPLATE = ROOT / "data/readme_zh.md"
ZH_OUT = ROOT / "README_zh.md"

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

SCOPE = {  # one line under each category heading
    "Core Papers": "The five papers threaded together by the WeChat article / @nrehiew_ thread, in reading order. Each has a full report (ZH/EN) and a layout-preserving Chinese translation.",
    "Surveys": "Surveys that cover looped models as part of latent reasoning.",
    "Foundations & Precursors": "Weight sharing across depth, adaptive computation time, equilibrium models, and recurrent algorithm learners that later looped models build on.",
    "Theory: Expressivity, ICL & Length Generalization": "What looping adds in expressivity, in-context learning, and length or compositional generalization, and how it compares with chain-of-thought.",
    "Scaled Pretraining": "Looped and recurrent-depth language models pretrained at scale, their scaling laws, and compute-matched comparisons with standard transformers.",
    "Efficiency: Latency, KV Cache & Quantization": "The serving cost of looping: latency, KV-cache memory, linear-time variants, and quantization.",
    "Stability & Training Theory": "Why deep loops diverge and how to keep them stable: contraction, residual scaling, normalization, fixed points.",
    "Adaptive Computation & Halting": "How many loops per input or per token: halting, routing, and elastic depth.",
    "Retrofitting & Training-Free": "Turning pretrained non-looped models into looped ones with little or no extra training.",
    "Post-Training & RL for Looped Models": "SFT and RL for looped models, including credit assignment across latent iterations.",
    "Interpretability & Latent Dynamics": "What happens inside the loop: decoded latent trajectories, attractors, and attribution across steps.",
    "Tiny Recursive Reasoners": "Small recursive networks (HRM, TRM and successors) on puzzle-style reasoning such as Sudoku, mazes, and ARC.",
    "Applications & Cross-Modal": "Looping outside text language modeling: vision, 3D, speech, translation, embeddings, tool calling, and robotics.",
    "Related: Latent Reasoning Beyond Looping": "Latent-reasoning methods that add computation without looping weights: pause tokens, continuous thoughts, mixture-of-depths.",
}

CORE_REPORTS = {  # arxiv id -> (zh report, en report, zh pdf)
    "1807.03819": ("reports/zh/01_universal_transformers.md", "reports/en/01_universal_transformers.md", "papers/zh/1807.03819.zh.pdf"),
    "2502.05171": ("reports/zh/02_recurrent_depth_huginn.md", "reports/en/02_recurrent_depth_huginn.md", "papers/zh/2502.05171.zh.pdf"),
    "2605.23872": ("reports/zh/03_training_free_looped.md", "reports/en/03_training_free_looped.md", "papers/zh/2605.23872.zh.pdf"),
    "2606.18023": ("reports/zh/04_loopcoder_v2.md", "reports/en/04_loopcoder_v2.md", "papers/zh/2606.18023.zh.pdf"),
    "2607.16051": ("reports/zh/05_loop_the_loopies.md", "reports/en/05_loop_the_loopies.md", "papers/zh/2607.16051.zh.pdf"),
}

MAX_AUTHORS = 8  # longer author lists show the first six, then "et al."

def anchor(title: str) -> str:
    a = title.lower()
    a = re.sub(r"[^\w\s-]", "", a)
    return re.sub(r"\s+", "-", a.strip())

def load():
    with CSV.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))

def short_authors(authors: str) -> str:
    names = [a.strip() for a in authors.split(",") if a.strip() not in ("", ":")]
    if len(names) > MAX_AUTHORS:
        names = names[:6] + ["et al."]
    return ", ".join(names)

def render_entry(i, r, latest):
    title = r["title"].rstrip(".")
    mark = "⭐ " if r.get("note") == "core" else ""
    if latest and r.get("added") == latest:
        mark += "🆕 "
    links = [f"[paper]({r['link']})"]
    if r.get("code"):
        links.append(f"[code]({r['code']})")
    if r.get("arxiv") in CORE_REPORTS:
        zh, en, pdf = CORE_REPORTS[r["arxiv"]]
        links += [f"[report-en]({en})", f"[report-zh]({zh})", f"[中译PDF]({pdf})"]
    line = f"{i}. {mark}**{title}** `{r['publisher']} {r['year']}` · " + " · ".join(links)
    if r.get("note") and r["note"] != "core":
        line += f" — *{r['note']}*"
    return line + f"<br><sub>{short_authors(r['authors'])}</sub>\n"

def fill(text, values):
    for k, v in values.items():
        text = text.replace("{{" + k + "}}", str(v))
    left = re.findall(r"\{\{[A-Z_]+\}\}", text)
    if left:
        raise SystemExit(f"unfilled placeholders: {sorted(set(left))}")
    return text

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

    added = sorted({r.get("added") or "" for r in rows} - {""})
    latest = added[-1] if added else ""
    updated = latest or max(r.get("published") or "" for r in rows)
    values = {
        "N_PAPERS": len(rows),
        "N_NEW": sum(1 for r in rows if latest and r.get("added") == latest),
        "N_CATEGORIES": len(CATEGORY_ORDER),
        "UPDATED": updated,
        "UPDATED_BADGE": updated.replace("-", "--"),
    }

    out = [fill(HEADER.read_text(encoding="utf-8"), values).rstrip() + "\n\n"]
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
    out.append("⭐ core paper with a full report and a Chinese translation · 🆕 added in the latest update"
               f" ({updated}) · a paper can appear under several topics.\n\n")
    for name in CATEGORY_ORDER:
        out.append(f"## [{name}](#content)\n\n{SCOPE[name]}\n\n")
        for i, r in enumerate(by_cat[name], 1):
            out.append(render_entry(i, r, latest))
        out.append("\n")
    footer = fill(FOOTER.read_text(encoding="utf-8"), values)
    # make the footer's static sections link-anchored like the generated ones
    for name in STATIC_SECTIONS:
        footer = footer.replace(f"## {name}\n", f"## [{name}](#content)\n")
    out.append(footer.lstrip("\n"))
    OUT.write_text("".join(out), encoding="utf-8")
    ZH_OUT.write_text(fill(ZH_TEMPLATE.read_text(encoding="utf-8"), values), encoding="utf-8")
    print(f"wrote {OUT} with {values['N_PAPERS']} papers ({values['N_NEW']} new) in {values['N_CATEGORIES']} categories")

if __name__ == "__main__":
    main()
