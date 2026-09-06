# Awesome Loop Transformer: Looped Transformers, Recurrent Depth & Latent Reasoning

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re) [![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](LICENSE) ![Papers](https://img.shields.io/badge/papers-122-blue) ![Last update](https://img.shields.io/badge/updated-2026--09--06-green)

A curated, annotated list of papers on **looped / recurrent-depth / weight-tied transformers** and the latent-reasoning ideas around them, from Universal Transformers (2018) to the compute-matched looped MoE models of 2026 — the technique reported to sit behind GPT-6 Astra.

This repository started from the WeChat article [《刚刚，GPT-6 Astra 背后的 Loop 技术全被挖出来了》](https://mp.weixin.qq.com/s/7vEMyFVpf2O9WL4Lu4gSFQ) (PaperAgent, after a thread by [@nrehiew_](https://x.com/nrehiew_/status/2095115984873062675)). The five papers it threads together are marked with ⭐ below and are covered by full-length reports, layout-preserving Chinese translations, and a survey with ten trend insights. Everything else was collected through arXiv searches on 2026-09-06.

**中文说明见 [README_zh.md](README_zh.md)。** 五篇核心论文的逐篇深度解读在 [`reports/zh/`](reports/zh/)，保版式中译 PDF 在 [`papers/zh/`](papers/zh/)，趋势综述在 [`survey/zh/`](survey/zh/)，完整中文报告 PDF 见 [`reports/pdf/awesome_loop_transformer_report_zh.pdf`](reports/pdf/awesome_loop_transformer_report_zh.pdf)，HTML 演示见 [`slides/html/index.html`](slides/html/index.html)。

## What is in this repository

| Deliverable | Path |
|---|---|
| Five core papers, original PDFs + arXiv full text | [`papers/original/`](papers/original/), [`papers/src/`](papers/src/) |
| Layout-preserving Chinese translations with object-level QA reports | [`papers/zh/`](papers/zh/) ([QA record](papers/zh/QA_SUMMARY.md)) |
| Per-paper deep-dive reports, Chinese and English | [`reports/zh/`](reports/zh/), [`reports/en/`](reports/en/) |
| Full report PDFs (survey + five reports), Chinese and English | [`reports/pdf/awesome_loop_transformer_report_zh.pdf`](reports/pdf/awesome_loop_transformer_report_zh.pdf), [`reports/pdf/awesome_loop_transformer_report_en.pdf`](reports/pdf/awesome_loop_transformer_report_en.pdf) |
| Survey: taxonomy, timeline, ~60-paper map, ten trend insights, open problems | [`survey/zh/survey_zh.md`](survey/zh/survey_zh.md) ([PDF](survey/zh/survey_zh.pdf)), [`survey/en/survey_en.md`](survey/en/survey_en.md) ([PDF](survey/en/survey_en.pdf)) |
| HTML slide deck (21 slides, Chinese) + PDF export | [`slides/html/index.html`](slides/html/index.html), [`slides/html/awesome_loop_transformer_slides_zh.pdf`](slides/html/awesome_loop_transformer_slides_zh.pdf) |
| Beamer slide deck (English, 16:9, with backup slides) | [`slides/beamer/loop_transformer_slides.pdf`](slides/beamer/loop_transformer_slides.pdf) ([source](slides/beamer/loop_transformer_slides.tex)) |
| Editable PowerPoint deck (Chinese, 21 slides, native shapes via ppt-master) + LibreOffice preview | [`slides/pptx/awesome_loop_transformer_slides_zh.pptx`](slides/pptx/awesome_loop_transformer_slides_zh.pptx) ([preview PDF](slides/pptx/awesome_loop_transformer_slides_zh.preview.pdf), [page SVGs](slides/pptx/svg_output/)) |
| Machine-readable paper list and abstracts | [`data/papers.csv`](data/papers.csv), [`data/related_abstracts.json`](data/related_abstracts.json) |

Online slides: [asimfish.github.io/awesome_loop_transformer/slides/html/](https://asimfish.github.io/awesome_loop_transformer/slides/html/)

<p align="center">
  <a href="slides/html/index.html"><img src="assets/figures/slide_02.png" width="49%" alt="One-page conclusions slide"></a>
  <a href="slides/html/index.html"><img src="assets/figures/slide_10.png" width="49%" alt="LoopCoder-v2 slide"></a>
</p>

## Ten trend insights (short form)

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

