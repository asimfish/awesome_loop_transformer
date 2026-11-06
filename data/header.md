<div align="center">

<a href="https://github.com/asimfish/awesome_loop_transformer"><img src="assets/banner.svg" alt="Awesome Loop Transformer: looped transformers, recurrent depth and latent reasoning" width="100%"></a>

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![Papers](https://img.shields.io/badge/papers-{{N_PAPERS}}-0173B2)](#content)
[![Updated](https://img.shields.io/badge/updated-{{UPDATED_BADGE}}-029E73)](#news)
[![Slides](https://img.shields.io/badge/slides-online-DE8F05)](https://asimfish.github.io/awesome_loop_transformer/slides/html/)
[![License: CC BY 4.0](https://img.shields.io/badge/license-CC%20BY%204.0-lightgrey)](LICENSE)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](CONTRIBUTING.md)
[![GitHub stars](https://img.shields.io/github/stars/asimfish/awesome_loop_transformer?style=social)](https://github.com/asimfish/awesome_loop_transformer/stargazers)

**English** · [中文导读](README_zh.md) · [Survey](survey/en/survey_en.md) · [Paper reports](reports/en/) · [Online slides](https://asimfish.github.io/awesome_loop_transformer/slides/html/) · [Contributing](CONTRIBUTING.md)

</div>

A curated list of **{{N_PAPERS}} papers** on **looped / recurrent-depth / weight-tied transformers** and the latent-reasoning work around them, from Universal Transformers (2018) to the compute-matched looped MoE models of 2026 — the technique reported to sit behind GPT-6 Astra. Papers are grouped into {{N_CATEGORIES}} categories; five core papers come with full-length reports, layout-preserving Chinese translations, and a survey with ten trend insights.

The repository started from the WeChat article [《刚刚，GPT-6 Astra 背后的 Loop 技术全被挖出来了》](https://mp.weixin.qq.com/s/7vEMyFVpf2O9WL4Lu4gSFQ) (PaperAgent, after a thread by [@nrehiew_](https://x.com/nrehiew_/status/2095115984873062675)). The list was first built from arXiv searches on 2026-09-06 and last updated on {{UPDATED}}.

## News

- **{{UPDATED}}** — Added {{N_NEW}} papers from September–November 2026 (marked 🆕) and a [what changed since September](#what-changed-since-september-2026) section; README redesigned (scope line per category, compact entries, venue tags).
- **2026-09-08** — Every report now opens with an at-a-glance box and a diagram and closes with a glossary; reading guides for 5-minute, 30-minute and 2-hour readers.
- **2026-09-06** — Editable PPTX deck (ppt-master) and Chinese README.
- **2026-09-06** — First release: 122 papers, five core-paper reports (ZH/EN), translated PDFs, a survey with ten trend insights, HTML and Beamer slides.

## What is in this repository

| Deliverable | Path |
|---|---|
| 📄 Five core papers, original PDFs + arXiv full text | [`papers/original/`](papers/original/), [`papers/src/`](papers/src/) |
| 🈶 Layout-preserving Chinese translations with object-level QA reports | [`papers/zh/`](papers/zh/) ([QA record](papers/zh/QA_SUMMARY.md)) |
| 🔬 Per-paper deep-dive reports, English and Chinese | [`reports/en/`](reports/en/), [`reports/zh/`](reports/zh/) |
| 📚 Full report PDFs (survey + five reports) | [English](reports/pdf/awesome_loop_transformer_report_en.pdf) · [中文](reports/pdf/awesome_loop_transformer_report_zh.pdf) |
| 🧭 Survey: taxonomy, timeline, ~60-paper map, ten trend insights, open problems | [`survey/en/survey_en.md`](survey/en/survey_en.md) ([PDF](survey/en/survey_en.pdf)) · [`survey/zh/survey_zh.md`](survey/zh/survey_zh.md) ([PDF](survey/zh/survey_zh.pdf)) |
| 🖥️ HTML slide deck (21 slides, Chinese) + PDF export | [online](https://asimfish.github.io/awesome_loop_transformer/slides/html/) · [`slides/html/`](slides/html/index.html) · [PDF](slides/html/awesome_loop_transformer_slides_zh.pdf) |
| 🎓 Beamer slide deck (English, 16:9, with backup slides) | [PDF](slides/beamer/loop_transformer_slides.pdf) ([source](slides/beamer/loop_transformer_slides.tex)) |
| ✏️ Editable PowerPoint deck (Chinese, native shapes via ppt-master) | [PPTX](slides/pptx/awesome_loop_transformer_slides_zh.pptx) ([preview PDF](slides/pptx/awesome_loop_transformer_slides_zh.preview.pdf), [page SVGs](slides/pptx/svg_output/)) |
| 🗂️ Machine-readable paper list and abstracts | [`data/papers.csv`](data/papers.csv), [`data/related_abstracts.json`](data/related_abstracts.json) |

<p align="center">
  <a href="https://asimfish.github.io/awesome_loop_transformer/slides/html/"><img src="assets/figures/slide_02.png" width="49%" alt="One-page conclusions slide"></a>
  <a href="https://asimfish.github.io/awesome_loop_transformer/slides/html/"><img src="assets/figures/slide_10.png" width="49%" alt="LoopCoder-v2 slide"></a>
</p>

## Where to start

| You have | Read |
|---|---|
| 5 minutes | the ten insights below, then Appendix A of the survey (five popular claims the papers do not support) |
| 30 minutes | the [survey](survey/en/survey_en.md) §2–4 and §6, or the 21-slide [HTML deck](https://asimfish.github.io/awesome_loop_transformer/slides/html/) |
| 2 hours | the five [paper reports](reports/en/) — each opens with an at-a-glance box and a diagram, and closes with a glossary |
| a talk to give | the [Beamer deck](slides/beamer/loop_transformer_slides.pdf) (English) or the editable [PPTX](slides/pptx/awesome_loop_transformer_slides_zh.pptx) (Chinese) |

## What changed since September 2026

{{N_NEW}} papers were added on {{UPDATED}}: 167 first submitted between 2026-09-01 and 2026-11-06, plus 44 from June–August that the first search missed. Every number below appears in the cited abstract.

1. **Looped models trained from scratch now beat matched baselines without MoE; looping an already-pretrained model is a mixed bet** (refines insight 1). Loopback reaches lower loss than standard Transformers with 40–75% of their Transformer parameters at matched tokens and executed depth ([2611.07226](https://arxiv.org/abs/2611.07226)). A scaling law fitted on about 600 runs finds that two fully trained loops beat the compute-optimal non-looped model with 27% fewer non-embedding parameters for 8% more compute ([2610.26030](https://arxiv.org/abs/2610.26030)). Looping pretrained Qwen3/Qwen3.5 models after the fact beats equal-parameter and equal-FLOPs baselines only at 0.8B ([2610.42030](https://arxiv.org/abs/2610.42030)), while RELOAD, which fine-tunes a damped middle-block loop, gains up to 23 points for encoders on longer reasoning chains ([2611.07736](https://arxiv.org/abs/2611.07736)).
2. **Two loops is the optimum of current designs, not a rule, and adaptive-halting savings are overstated** (revises insight 2). With bounded residual variance and per-loop routers, LOOM scales looped MoE to 9–12 loops, and its 700M model is best at 5 loops at near-iso-FLOPs ([2610.01153](https://arxiv.org/abs/2610.01153)); gated layer-wise looping of Qwen3-4B is best at three ([2610.25004](https://arxiv.org/abs/2610.25004)). Halting heads trained on mixed iterations run almost every iteration under the standard stopping rule, and batched generation removes most of the reported saving ([2610.32246](https://arxiv.org/abs/2610.32246)).
3. **Serving became the largest technical cluster, and looped models now run in production engines** (revises the toolchain half of insight 10, refines insight 6). Efficiency is the primary category of 26 of the 167 new papers. LoopVQ reaches up to 6.1× Ouro serving throughput in SGLang ([2611.05304](https://arxiv.org/abs/2611.05304)); LoopKV's fused vLLM kernel gets 1.7–2.2× the goodput of KIVI-4 on Ouro-1.4B ([2611.04137](https://arxiv.org/abs/2611.04137)). Caching only the last loop's keys and values ships in open checkpoints such as Dory1.0-4B ([2611.03998](https://arxiv.org/abs/2611.03998)), but recent-window KV sharing fails on Ouro-1.4B because its cost depends on how far late loops have converged ([2610.34436](https://arxiv.org/abs/2610.34436)).
4. **Loop depth changes safety behaviour, a dimension none of the ten insights covers.** At half depth, Ouro-1.4B-Thinking keeps 89% of its GSM8K accuracy while its rate of helping with harmful requests rises 5.3×; training at random depths restores refusal at every depth ([2610.15218](https://arxiv.org/abs/2610.15218)). Jailbreak success varies across recurrent depths and transfers between them ([2610.10625](https://arxiv.org/abs/2610.10625)). Post-training (insight 7) has to cover every depth a model may run at.
5. **"Loops manipulate knowledge, they do not store it" is turning into architecture: explicit memory and state channels inside the loop** (supports insight 8). Recurrence past the training horizon improves reasoning but degrades knowledge ([2609.36636](https://arxiv.org/abs/2609.36636)). In a synthetic edit study, factual edits propagate with addressable memory (0.71–0.96) but only weakly with loops alone (0.04–0.30) ([2606.20737](https://arxiv.org/abs/2606.20737)). A bounded gated cell lets LSTM-UT keep 99.7% exact-row accuracy at depth 60 after training to depth 12 ([2609.19521](https://arxiv.org/abs/2609.19521)).
6. **Applications spread to generative and scientific foundation models** (extends insight 9). A 260M Looped-DiT surpasses a 6.5× larger text-to-image model at 4.9× lower inference compute ([2609.40305](https://arxiv.org/abs/2609.40305)); Eco-RNA at four iterations surpasses Evo 2 40B on RNAGym fitness with 500× fewer parameters ([2610.13106](https://arxiv.org/abs/2610.13106)).

## Ten trend insights

<sub>As of 2026-09-06; the section above records what the September–November papers changed.</sub>

1. **Recurrent depth passed the compute-matching gate in 2026, through a narrow door.** Loopie (matched measured step time) and SMELT (matched FLOPs/params/KV) beat vanilla MoE transformers; the win needs MoE + layer/mid-stack looping + two loops, and comes from converting saved activation memory into width rather than from loops replacing parameters (one recurrence is worth $r^{0.46}$ unique parameters).
2. **"How many loops" splits into two regimes.** Fixed pretraining budget: 2 (Loopie, LoopCoder-v2, SMELT, Nanbeige4.2). Variable inference compute: adaptive and deep (Huginn to 32–64). LoopCoder-v2's "three regress" is the positional tax of the Parallel Loop Transformer, not a law.
3. **Loop granularity is shrinking and converging on the middle of the stack** (depth fraction ≈ 0.5); MoE requires layer-mode looping.
4. **Two philosophies:** treat a pretrained mid-stack as an ODE flow (sub-step, keep the endpoint) versus train the loop to be a fixed point (STARS, Fixed-Point Reasoners, Attractor Models).
5. **Training stability went from folklore to theorems** (residual scaling 1/N, DeepLoop exponent 1/2, LR transfer across loop counts).
6. **Inference cost decomposes into latency, KV memory, and quantization**, each with 2025–2026 fixes (PLT, diffusion-style samplers, MELT, Looped Latent Attention 32×, LoopQ). Matched training compute is not matched inference cost.
7. **Latent loops and explicit CoT are complements**: super-additive in LoopCoder-v2, gap-closing in LOTUS; standard GRPO mis-assigns credit to looped models (RLTT, LoopRPT).
8. **Loops manipulate knowledge, they do not store it** — pair them with retrieval, long context, or MoE expert banks.
9. **Applications moved from puzzles to agents and embodiment** (SWE-bench, tool calling, VLA).
10. **Productization has started; the toolchain has not caught up.**

Full text with sources: [`survey/en/survey_en.md`](survey/en/survey_en.md) · [`survey/zh/survey_zh.md`](survey/zh/survey_zh.md).
