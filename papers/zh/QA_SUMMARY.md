# 中译 PDF 质量记录 · Translation QA Record

翻译引擎：[SuperTranslate](https://github.com/asimfish/super_translate)（native 引擎，DeepSeek 后端 `deepseek-v4-pro`，`--preserve-graphics-text`），命令见 `scripts/translate_papers.sh`。每份译文都经过 `pdf_zh_translator inspect` 逐页对象级审计，报告为同名 `*.zh.inspect.json`。

| arXiv | 论文 | 页数 | 翻译耗时 | inspect 结果 | 说明 |
|---|---|---|---|---|---|
| 2606.18023 | LoopCoder-v2 | 20 | 8.5 min | 0 issue | 通过 |
| 2605.23872 | Training-Free Looped Transformers | 32 | 8.6 min | 0 issue | 通过 |
| 1807.03819 | Universal Transformers | 23 | 4.7 min | 2 error `untranslated_block` (p3) | 两处均为公式行（`where head_i = Attention(...)`、`where A^t = LayerNorm(...)`），属于保护区内的数学文本，保留英文是预期行为，不影响阅读 |
| 2607.16051 | Loop the Loopies! | 38 | 8.3 min | 4 error `text_outside_frame` (p1, p10) | 首页与第 10 页柱状图的坐标轴刻度（`60`、`35%`）超出检测框 1.5–2 pt，为原图内文字，视觉核对无重叠 |
| 2502.05171 | Recurrent Depth (Huginn) | 37 | 9.1 min | 0 issue | 通过 |

已知的引擎级小瑕疵：行内数学符号（如 `$N$`）在部分正文段落中以占位字形显示；参考文献保持英文原样（设计如此，便于检索）。

Engine: SuperTranslate native engine (DeepSeek `deepseek-v4-pro`, graphics text preserved); see `scripts/translate_papers.sh`. Every output was audited page-by-page with `pdf_zh_translator inspect`; reports are the sibling `*.zh.inspect.json` files. Three of five papers pass with zero issues. The two remaining error flags are (a) two equation lines on UT page 3 that stay in English by design (protected math), and (b) four chart tick labels on Loopie pages 1 and 10 overrunning their detection box by under 2 pt — verified visually as non-overlapping.
