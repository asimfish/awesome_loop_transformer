"""Fetch arXiv metadata for the curated paper list and write data/papers.csv.

The curated list (categories, venues, notes) lives in CURATED below; titles and authors are
pulled from the arXiv API so they stay exact. Re-run after adding IDs, then run src/generator.py.
"""
import csv, json, pathlib, sys, time, urllib.request, xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "data/papers.csv"
NS = {"a": "http://www.w3.org/2005/Atom", "ar": "http://arxiv.org/schemas/atom"}

# (arxiv_id, categories ';'-separated, venue, year, code_url, note)
CURATED = [
    # --- Core papers (the five in the WeChat / @nrehiew_ thread) ---
    ("1807.03819", "Core Papers;Foundations & Precursors", "ICLR", 2019, "https://github.com/tensorflow/tensor2tensor", "core"),
    ("2502.05171", "Core Papers;Scaled Pretraining", "arXiv", 2025, "https://github.com/seal-rg/recurrent-pretraining", "core"),
    ("2605.23872", "Core Papers;Retrofitting & Training-Free", "arXiv", 2026, "", "core"),
    ("2606.18023", "Core Papers;Scaled Pretraining", "arXiv", 2026, "https://huggingface.co/Multilingual-Multimodal-NLP/LoopCoder-V2", "core"),
    ("2607.16051", "Core Papers;Scaled Pretraining", "arXiv", 2026, "", "core"),
    # --- Surveys ---
    ("2507.06203", "Surveys", "arXiv", 2025, "https://github.com/multimodal-art-projection/LatentCoT-Horizon/", ""),
    # --- Foundations & precursors ---
    ("1511.08228", "Foundations & Precursors", "ICLR", 2016, "", ""),
    ("1603.08983", "Foundations & Precursors", "arXiv", 2016, "", ""),
    ("1909.01377", "Foundations & Precursors", "NeurIPS", 2019, "", ""),
    ("1909.11942", "Foundations & Precursors", "ICLR", 2020, "", ""),
    ("2107.05407", "Foundations & Precursors;Adaptive Computation & Halting", "ICML Workshop", 2021, "", ""),
    ("2106.04537", "Foundations & Precursors", "NeurIPS", 2021, "", ""),
    ("2202.05826", "Foundations & Precursors", "NeurIPS", 2022, "", ""),
    ("2211.09961", "Foundations & Precursors", "NeurIPS", 2022, "", ""),
    ("2104.06022", "Foundations & Precursors", "arXiv", 2023, "", ""),
    ("2310.07096", "Foundations & Precursors", "EMNLP", 2023, "", ""),
    ("2310.10845", "Foundations & Precursors;Adaptive Computation & Halting", "ICLR", 2025, "", ""),
    ("2405.16039", "Foundations & Precursors;Scaled Pretraining", "NeurIPS", 2024, "", ""),
    ("2410.20672", "Foundations & Precursors;Retrofitting & Training-Free", "ICLR", 2025, "", ""),
    # --- Theory ---
    ("2301.13196", "Theory: Expressivity, ICL & Length Generalization", "ICML", 2023, "", ""),
    ("2311.12424", "Theory: Expressivity, ICL & Length Generalization", "ICLR", 2024, "", ""),
    ("2402.01107", "Theory: Expressivity, ICL & Length Generalization", "ICML", 2024, "", ""),
    ("2410.08292", "Theory: Expressivity, ICL & Length Generalization", "ICML", 2024, "", ""),
    ("2410.21698", "Theory: Expressivity, ICL & Length Generalization", "arXiv", 2024, "", ""),
    ("2410.09375", "Theory: Expressivity, ICL & Length Generalization", "arXiv", 2024, "", ""),
    ("2410.01405", "Theory: Expressivity, ICL & Length Generalization", "arXiv", 2024, "", ""),
    ("2410.11268", "Theory: Expressivity, ICL & Length Generalization", "AISTATS", 2025, "", ""),
    ("2409.15647", "Theory: Expressivity, ICL & Length Generalization", "ICLR", 2025, "", ""),
    ("2502.17416", "Theory: Expressivity, ICL & Length Generalization", "ICLR", 2025, "", ""),
    ("2505.19245", "Theory: Expressivity, ICL & Length Generalization", "arXiv", 2025, "", ""),
    ("2510.10089", "Theory: Expressivity, ICL & Length Generalization", "arXiv", 2025, "", ""),
    ("2604.07822", "Theory: Expressivity, ICL & Length Generalization", "COLM", 2026, "", ""),
    ("2603.21676", "Theory: Expressivity, ICL & Length Generalization", "arXiv", 2026, "", ""),
    ("2602.11698", "Theory: Expressivity, ICL & Length Generalization", "arXiv", 2026, "", ""),
    ("2604.15259", "Theory: Expressivity, ICL & Length Generalization", "arXiv", 2026, "", ""),
    ("2605.26035", "Theory: Expressivity, ICL & Length Generalization", "arXiv", 2026, "", ""),
    ("2605.30757", "Theory: Expressivity, ICL & Length Generalization", "arXiv", 2026, "", ""),
    ("2606.00605", "Theory: Expressivity, ICL & Length Generalization", "arXiv", 2026, "", ""),
    ("2607.00341", "Theory: Expressivity, ICL & Length Generalization", "arXiv", 2026, "", ""),
    ("2607.20594", "Theory: Expressivity, ICL & Length Generalization", "arXiv", 2026, "", ""),
    ("2604.21999", "Theory: Expressivity, ICL & Length Generalization", "arXiv", 2026, "", ""),
    ("2608.31067", "Theory: Expressivity, ICL & Length Generalization", "arXiv", 2026, "", ""),
    # --- Scaled pretraining ---
    ("2510.25741", "Scaled Pretraining", "arXiv", 2025, "http://ouro-llm.github.io", ""),
    ("2510.24824", "Scaled Pretraining;Efficiency: Latency, KV Cache & Quantization", "arXiv", 2025, "", ""),
    ("2607.22083", "Scaled Pretraining;Applications & Cross-Modal", "arXiv", 2026, "", ""),
    ("2609.01343", "Scaled Pretraining", "arXiv", 2026, "", ""),
    ("2604.21106", "Scaled Pretraining;Theory: Expressivity, ICL & Length Generalization", "arXiv", 2026, "", ""),
    ("2605.26797", "Scaled Pretraining", "arXiv", 2026, "", ""),
    ("2601.21582", "Scaled Pretraining", "arXiv", 2026, "", ""),
    ("2604.21254", "Scaled Pretraining;Efficiency: Latency, KV Cache & Quantization", "arXiv", 2026, "", ""),
    ("2605.30202", "Scaled Pretraining", "arXiv", 2026, "", ""),
    ("2603.08391", "Scaled Pretraining;Adaptive Computation & Halting", "ICLR Workshop", 2026, "", ""),
    ("2608.18230", "Scaled Pretraining", "arXiv", 2026, "", ""),
    ("2608.15062", "Scaled Pretraining", "arXiv", 2026, "", ""),
    ("2607.08186", "Scaled Pretraining", "arXiv", 2026, "", "contrast: sequence-length scaling"),
    # --- Efficiency ---
    ("2510.14961", "Efficiency: Latency, KV Cache & Quantization", "arXiv", 2025, "https://github.com/seal-rg/recurrent-pretraining", ""),
    ("2605.07721", "Efficiency: Latency, KV Cache & Quantization", "arXiv", 2026, "", ""),
    ("2607.15456", "Efficiency: Latency, KV Cache & Quantization", "arXiv", 2026, "", ""),
    ("2605.20670", "Efficiency: Latency, KV Cache & Quantization", "arXiv", 2026, "", ""),
    ("2605.16343", "Efficiency: Latency, KV Cache & Quantization", "arXiv", 2026, "", ""),
    ("2607.10110", "Efficiency: Latency, KV Cache & Quantization", "arXiv", 2026, "", ""),
    ("2608.13987", "Efficiency: Latency, KV Cache & Quantization", "arXiv", 2026, "https://github.com/johnhalloran321/Nanbeige4.2-3B-mps-fix", ""),
    # --- Stability & training theory ---
    ("2606.18524", "Stability & Training Theory", "arXiv", 2026, "", ""),
    ("2607.13491", "Stability & Training Theory", "arXiv", 2026, "", ""),
    ("2605.18797", "Stability & Training Theory", "arXiv", 2026, "", ""),
    ("2605.26733", "Stability & Training Theory", "ICML", 2026, "", ""),
    ("2606.18206", "Stability & Training Theory;Tiny Recursive Reasoners", "arXiv", 2026, "https://github.com/nilskiKonjIzDunava/fprm", ""),
    ("2608.18222", "Stability & Training Theory", "arXiv", 2026, "", ""),
    ("2606.29983", "Stability & Training Theory;Adaptive Computation & Halting", "arXiv", 2026, "", ""),
    ("2605.12466", "Stability & Training Theory;Tiny Recursive Reasoners", "arXiv", 2026, "", ""),
    ("2607.10681", "Stability & Training Theory", "arXiv", 2026, "", ""),
    ("2603.10544", "Stability & Training Theory", "arXiv", 2026, "", ""),
    # --- Adaptive computation ---
    ("2507.10524", "Adaptive Computation & Halting;Efficiency: Latency, KV Cache & Quantization", "NeurIPS", 2025, "https://github.com/raymin0223/mixture_of_recursions", ""),
    ("2511.08577", "Adaptive Computation & Halting", "ICML", 2026, "https://github.com/thu-nics/TaH", ""),
    ("2602.11451", "Adaptive Computation & Halting", "ICLR", 2026, "", ""),
    ("2609.03379", "Adaptive Computation & Halting", "arXiv", 2026, "", ""),
    ("2607.20519", "Adaptive Computation & Halting", "arXiv", 2026, "", ""),
    ("2509.23314", "Adaptive Computation & Halting;Interpretability & Latent Dynamics", "arXiv", 2025, "", ""),
    ("2607.14427", "Adaptive Computation & Halting", "arXiv", 2026, "", ""),
    # --- Retrofitting & training-free ---
    ("2511.07384", "Retrofitting & Training-Free", "arXiv", 2025, "https://github.com/mcleish7/retrofitting-recurrence", ""),
    ("2606.06574", "Retrofitting & Training-Free", "ICML", 2026, "", ""),
    ("2608.11233", "Retrofitting & Training-Free", "arXiv", 2026, "", ""),
    ("2512.12880", "Retrofitting & Training-Free", "arXiv", 2025, "", ""),
    ("2604.02051", "Retrofitting & Training-Free", "arXiv", 2026, "", ""),
    # --- Post-training & RL ---
    ("2602.10520", "Post-Training & RL for Looped Models", "ICML", 2026, "https://github.com/jonwill8/RLTT", ""),
    ("2603.19714", "Post-Training & RL for Looped Models", "arXiv", 2026, "", ""),
    ("2606.31779", "Post-Training & RL for Looped Models", "arXiv", 2026, "https://github.com/yingfan-bot/lotus", ""),
    ("2608.03624", "Post-Training & RL for Looped Models", "arXiv", 2026, "", ""),
    ("2606.24898", "Post-Training & RL for Looped Models", "arXiv", 2026, "", ""),
    ("2606.13106", "Post-Training & RL for Looped Models", "arXiv", 2026, "", ""),
    ("2502.08482", "Post-Training & RL for Looped Models", "arXiv", 2025, "", ""),
    # --- Interpretability ---
    ("2507.02199", "Interpretability & Latent Dynamics", "Workshop", 2025, "https://github.com/wenquanlu/huginn-latent-cot", ""),
    ("2609.01924", "Interpretability & Latent Dynamics", "arXiv", 2026, "", ""),
    ("2606.12689", "Interpretability & Latent Dynamics", "arXiv", 2026, "", ""),
    ("2602.10097", "Interpretability & Latent Dynamics", "arXiv", 2026, "", ""),
    ("2601.10242", "Interpretability & Latent Dynamics", "arXiv", 2026, "", ""),
    # --- Tiny recursive reasoners ---
    ("2506.21734", "Tiny Recursive Reasoners", "arXiv", 2025, "", ""),
    ("2510.04871", "Tiny Recursive Reasoners", "arXiv", 2025, "", ""),
    ("2510.00355", "Tiny Recursive Reasoners", "arXiv", 2025, "", ""),
    ("2601.10679", "Tiny Recursive Reasoners", "arXiv", 2026, "", ""),
    ("2604.18839", "Tiny Recursive Reasoners", "arXiv", 2026, "", ""),
    ("2511.16886", "Tiny Recursive Reasoners", "arXiv", 2025, "", ""),
    ("2603.22871", "Tiny Recursive Reasoners", "arXiv", 2026, "", ""),
    # --- Applications & cross-modal ---
    ("2602.02156", "Applications & Cross-Modal", "arXiv", 2026, "https://github.com/WenjieShu/LoopViT", ""),
    ("2602.07845", "Applications & Cross-Modal", "arXiv", 2026, "https://rd-vla.github.io/", ""),
    ("2605.03999", "Applications & Cross-Modal", "arXiv", 2026, "", ""),
    ("2604.09168", "Applications & Cross-Modal", "arXiv", 2026, "", ""),
    ("2605.30215", "Applications & Cross-Modal", "arXiv", 2026, "", ""),
    ("2606.04678", "Applications & Cross-Modal", "arXiv", 2026, "", ""),
    ("2608.18171", "Applications & Cross-Modal", "arXiv", 2026, "", ""),
    ("2602.09080", "Applications & Cross-Modal", "arXiv", 2026, "", ""),
    ("2607.28751", "Applications & Cross-Modal", "arXiv", 2026, "", ""),
    ("2512.19941", "Applications & Cross-Modal", "arXiv", 2025, "", ""),
    ("2607.18618", "Applications & Cross-Modal", "arXiv", 2026, "", ""),
    # --- Latent reasoning beyond looping (related) ---
    ("2412.06769", "Related: Latent Reasoning Beyond Looping", "COLM", 2025, "", ""),
    ("2412.13171", "Related: Latent Reasoning Beyond Looping", "arXiv", 2024, "", ""),
    ("2310.02226", "Related: Latent Reasoning Beyond Looping", "ICLR", 2024, "", ""),
    ("2404.02258", "Related: Latent Reasoning Beyond Looping", "arXiv", 2024, "", ""),
    ("2505.20674", "Related: Latent Reasoning Beyond Looping", "arXiv", 2025, "", ""),
    ("2510.07358", "Related: Latent Reasoning Beyond Looping", "arXiv", 2025, "", ""),
    ("2507.08567", "Related: Latent Reasoning Beyond Looping", "arXiv", 2025, "", ""),
    ("2511.21882", "Related: Latent Reasoning Beyond Looping", "arXiv", 2025, "", ""),
]

def fetch(ids):
    out = {}
    for i in range(0, len(ids), 50):
        chunk = ids[i:i+50]
        url = "https://export.arxiv.org/api/query?id_list=" + ",".join(chunk) + f"&max_results={len(chunk)}"
        req = urllib.request.Request(url, headers={"User-Agent": "awesome_loop_transformer/1.0"})
        xml = urllib.request.urlopen(req, timeout=60).read()
        for e in ET.fromstring(xml).findall("a:entry", NS):
            aid = e.find("a:id", NS).text.split("/abs/")[-1]
            base = aid.split("v")[0]
            out[base] = {
                "title": " ".join(e.find("a:title", NS).text.split()),
                "authors": ", ".join(x.find("a:name", NS).text for x in e.findall("a:author", NS)),
                "published": e.find("a:published", NS).text[:10],
            }
        time.sleep(3)
    return out

def main():
    ids = [c[0] for c in CURATED]
    meta = fetch(ids)
    missing = [i for i in ids if i not in meta]
    if missing:
        print("missing metadata for", missing, file=sys.stderr)
    rows = []
    for aid, cats, venue, year, code, note in CURATED:
        m = meta.get(aid)
        if not m:
            continue
        rows.append({
            "category": cats, "title": m["title"], "publisher": venue, "year": year,
            "type": "paper", "link": f"https://arxiv.org/abs/{aid}", "authors": m["authors"],
            "code": code, "arxiv": aid, "published": m["published"], "note": note,
        })
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["category", "title", "publisher", "year", "type", "link", "authors", "code", "arxiv", "published", "note"])
        w.writeheader(); w.writerows(rows)
    print("wrote", OUT, len(rows), "rows")

if __name__ == "__main__":
    main()
