
## Industry Reports & Threads

1. **GPT-6 Astra.** OpenAI, 2026-09. [page](https://openai.com/index/gpt-6-astra/) — release page; no architectural details disclosed.
2. **Secret Technique Behind OpenAI's Astra Model Sparks Security Concerns.** The Information, 2026-09-02. Stephanie Palazzolo — reports Astra uses "recurrent depth" (anonymously sourced; paywalled, not accessed for this repository).
3. **Thread: five papers behind recurrent depth.** X, 2026-09. [@nrehiew_](https://x.com/nrehiew_/status/2095115984873062675) · [@kimmonismus](https://x.com/kimmonismus/status/2095045887131087357).
4. **刚刚，GPT-6 Astra 背后的 Loop 技术全被挖出来了.** 微信公众号 PaperAgent, 2026-09. [article](https://mp.weixin.qq.com/s/7vEMyFVpf2O9WL4Lu4gSFQ) — the Chinese write-up this repository started from; a snapshot is kept in [`source/`](source/).

## Open Models

| Model | Params | Tokens | Loops | Link |
|---|---|---|---|---|
| Huginn-0125 | 3.5B dense | 0.8T | random at train, free at test (r̄=32) | [HF](https://huggingface.co/tomg-group-umd/huginn-0125) · [code](https://github.com/seal-rg/recurrent-pretraining) |
| Ouro 1.4B / 2.6B (+Thinking) | dense | 7.7T | 4 | [site](http://ouro-llm.github.io) |
| LoopCoder-V2 | 7B dense PLT | 18T | 2 | [HF](https://huggingface.co/Multilingual-Multimodal-NLP/LoopCoder-V2) |
| Loopie-20B-A2B / 6B-A0.6B | MoE | 3.5T | 2 (layer-loop) | see paper [2607.16051](https://arxiv.org/abs/2607.16051) (megatron-loopie, vllm-loopie) |
| Nanbeige4.2-3B | 3B | 28T | 2 | see paper [2607.22083](https://arxiv.org/abs/2607.22083) |

## Reproducing the artifacts

```bash
# 1. Paper list -> README
python3 src/fetch_metadata.py      # refresh titles/authors from arXiv into data/papers.csv
python3 src/generator.py           # regenerate README.md from data/header.md + papers.csv + footer.md

# 2. Chinese translations (SuperTranslate, https://github.com/asimfish/super_translate)
export PAPER_CHINA_DEEPSEEK_API_KEY=...   # never on the command line
export SUPER_TRANSLATE_HOME=/path/to/super_translate   # after `uv sync` there
bash scripts/translate_papers.sh          # -> papers/zh/*.zh.pdf + *.inspect.json

# 3. Report PDFs (pandoc + XeLaTeX; macOS CJK fonts by default, override with CJK_FONT / CJK_SANS)
bash scripts/build_pdfs.sh

# 4. Slides
open slides/html/index.html               # arrow keys / space to navigate, P to print
python3 scripts/export_slides.py          # HTML -> PDF + PNG previews with headless Chromium (set CHROME_BIN if needed)
cd slides/beamer && xelatex loop_transformer_slides.tex && xelatex loop_transformer_slides.tex

# 5. Editable PPTX through ppt-master (https://github.com/hugohe3/ppt-master; python>=3.10 + its requirements.txt)
export PPT_MASTER_HOME=/path/to/ppt-master
bash scripts/build_pptx.sh                # page SVGs -> quality gate -> SVG-to-DrawingML export -> slides/pptx/
```

## How this was made

- **Reading.** Each core paper was read in full from the arXiv PDF and HTML text; every number in the reports carries its table or section reference, and an appendix in the survey lists five claims from secondary coverage that the papers do not support.
- **Translation.** [SuperTranslate](https://github.com/asimfish/super_translate) native engine (layout-preserving, formulas and figures frozen, DeepSeek backend) followed by its object-level `inspect` QA. Three of five PDFs pass with zero issues; the remaining flags are documented in [`papers/zh/QA_SUMMARY.md`](papers/zh/QA_SUMMARY.md).
- **Literature search.** arXiv API queries on 2026-09-06 for looped / recurrent-depth / depth-recurrent transformers, latent reasoning with loops or recursion, and named model families; abstracts of the 60 most relevant works are kept in [`data/related_abstracts.json`](data/related_abstracts.json).
- **Writing style.** Claims first, necessary limits stated once, numbers checkable in place — following [anti-defensive-writing](https://github.com/Kiterlin/anti-defensive-writing) and [说人话 shuorenhua](https://github.com/MrGeDiao/shuorenhua).
- **Layout.** Report PDFs via pandoc + XeLaTeX with a shared header (`scripts/pandoc_header.tex`); the Beamer deck follows the [beamer-skill](https://github.com/Noi1r/beamer-skill) rules (16:9, 10pt, no overlays, semantic color-blind-safe palette, references and backup slides); the HTML deck and the PPTX follow the `technical-deepdive` style contract of [ppt-master](https://github.com/hugohe3/ppt-master) (problem → mechanism → trade-off → implication, blueprint palette, every number with its conditions); the PPTX itself is produced by ppt-master's Quick Generate route — `scripts/build_pptx_svgs.py` emits contract-conforming page SVGs (root bounds per module, one text frame per paragraph block, NBSP frame slack so renderers that ignore `wrap="none"` do not re-wrap), which pass its final quality gate and are exported to native DrawingML shapes. Paper-writing conventions were checked against [PaperOrchestra](https://github.com/Ar9av/PaperOrchestra).
- **Readability.** Each report opens with an at-a-glance box (problem / method / result / limits / plain words) and one explanatory diagram, and closes with a glossary; the survey has a reading guide for 5-minute, 30-minute and 2-hour readers. Diagrams are authored in `scripts/build_diagrams.py` (SVG) and rendered to PNG by `scripts/render_diagrams.sh`.
- **List format.** Follows [awesome-ml4co](https://github.com/Thinklab-SJTU/awesome-ml4co): `data/papers.csv` is the source of truth and `src/generator.py` renders the README.

## Contributing

Add a row to [`data/papers.csv`](data/papers.csv) (or an entry to `CURATED` in [`src/fetch_metadata.py`](src/fetch_metadata.py) and re-run it), then run `python3 src/generator.py` and open a pull request. Use `;` to list a paper under several categories. Please keep the venue field to the accepted venue or `arXiv`, and add a code link when one exists.

## Citation

```bibtex
@misc{awesome_loop_transformer_2026,
  title  = {Awesome Loop Transformer: Looped Transformers, Recurrent Depth and Latent Reasoning (2018--2026)},
  author = {{awesome\_loop\_transformer contributors}},
  year   = {2026},
  url    = {https://github.com/asimfish/awesome_loop_transformer}
}
```

## License

Text, reports, and slides in this repository are released under [CC BY 4.0](LICENSE); code under `src/` and `scripts/` under MIT. Original papers remain under their authors' licenses; PDFs in `papers/original/` are redistributed from arXiv, and the Chinese translations in `papers/zh/` are derived works provided for study.
