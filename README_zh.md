# Awesome Loop Transformer：循环 Transformer、循环深度与潜在推理

[English README](README.md) · 论文列表（122 篇、14 个主题）以英文维护在 README.md，本文件是中文导读。

这是一个围绕 **循环 Transformer（looped / recurrent-depth / weight-tied transformer）** 及其周边潜在推理工作的资料库，覆盖 2018 年的 Universal Transformer 到 2026 年在算力匹配下首次战胜普通 MoE 的循环模型——也就是 The Information 报道中 GPT-6 Astra 所用的 "recurrent depth" 技术路线。

起点是微信文章[《刚刚，GPT-6 Astra 背后的 Loop 技术全被挖出来了》](https://mp.weixin.qq.com/s/7vEMyFVpf2O9WL4Lu4gSFQ)（PaperAgent，整理自 [@nrehiew_](https://x.com/nrehiew_/status/2095115984873062675) 的推文串）。文章串起的五篇论文在 README 中加 ⭐ 标注，每篇都有逐篇深度解读、保版式中译 PDF，并有一份含十条趋势洞察的综述。其余文献来自 2026-09-06 的 arXiv 全量检索。

## 仓库内容

| 交付物 | 路径 |
|---|---|
| 五篇核心论文原文 PDF + arXiv 全文（Markdown） | [`papers/original/`](papers/original/)、[`papers/src/`](papers/src/) |
| 保版式中译 PDF + 对象级 QA 报告（SuperTranslate） | [`papers/zh/`](papers/zh/)（[QA 记录](papers/zh/QA_SUMMARY.md)） |
| 逐篇深度解读（中、英） | [`reports/zh/`](reports/zh/)、[`reports/en/`](reports/en/) |
| 完整报告 PDF（综述 + 五篇解读，中、英） | [`reports/pdf/awesome_loop_transformer_report_zh.pdf`](reports/pdf/awesome_loop_transformer_report_zh.pdf)、[`…_en.pdf`](reports/pdf/awesome_loop_transformer_report_en.pdf) |
| 趋势综述：分类、八年时间线、约 60 篇文献图谱、十条洞察、未解问题 | [`survey/zh/survey_zh.md`](survey/zh/survey_zh.md)（[PDF](survey/zh/survey_zh.pdf)）、[`survey/en/`](survey/en/) |
| HTML 演示（21 页，中文）+ PDF 导出 · [在线查看](https://asimfish.github.io/awesome_loop_transformer/slides/html/) | [`slides/html/index.html`](slides/html/index.html)、[`slides/html/awesome_loop_transformer_slides_zh.pdf`](slides/html/awesome_loop_transformer_slides_zh.pdf) |
| 可编辑 PPTX（中文，ppt-master 原生形状导出）+ 预览 PDF | [`slides/pptx/awesome_loop_transformer_slides_zh.pptx`](slides/pptx/awesome_loop_transformer_slides_zh.pptx)（[预览](slides/pptx/awesome_loop_transformer_slides_zh.preview.pdf)） |
| Beamer 学术幻灯（英文，16:9，含备用页） | [`slides/beamer/loop_transformer_slides.pdf`](slides/beamer/loop_transformer_slides.pdf)（[源码](slides/beamer/loop_transformer_slides.tex)） |
| 机器可读论文表与摘要 | [`data/papers.csv`](data/papers.csv)、[`data/related_abstracts.json`](data/related_abstracts.json) |

## 五篇核心论文一句话

| 论文 | 一句话 | 解读 |
|---|---|---|
| Universal Transformers（2018） | 把 N 层换成同一层重复 T 次，加 ACT 自适应停机；bAbI 联合训练错误率 22.1 → 0.29 | [zh](reports/zh/01_universal_transformers.md) · [中译](papers/zh/1807.03819.zh.pdf) |
| Recurrent Depth / Huginn-3.5B（2025-02） | 800B token 训成 3.5B 循环模型，r 从 4 到 32 时 ARC-E 49.1 → 69.9；定名 recurrent depth | [zh](reports/zh/02_recurrent_depth_huginn.md) · [中译](papers/zh/2502.05171.zh.pdf) |
| Training-Free Looped Transformers（2026-05） | 一层 = ODE 的一步欧拉，正确的循环是细分步长；不训练即让 Qwen3-4B MMLU-Pro +2.64 | [zh](reports/zh/03_training_free_looped.md) · [中译](papers/zh/2605.23872.zh.pdf) |
| LoopCoder-v2（2026-06） | 并行循环 Transformer 中第二次循环几乎是全部：SWE-bench Verified 43.0 → 64.4 → 27.6 | [zh](reports/zh/04_loopcoder_v2.md) · [中译](papers/zh/2606.18023.zh.pdf) |
| Loop the Loopies!（2026-07） | layer-loop + 实测步时匹配 + 两次循环，循环 MoE 第一次在算力匹配下反超 Qwen3-30B-A3B | [zh](reports/zh/05_loop_the_loopies.md) · [中译](papers/zh/2607.16051.zh.pdf) |

## 十条趋势洞察（简版）

1. **循环深度已跨过"算力匹配"这道门，但门很窄。** Loopie（实测步时匹配）与 SMELT（FLOPs / 参数 / KV 三重匹配）第一次战胜普通 MoE；胜利需要 MoE + 逐层或中段循环 + 两次循环，而且来自把省下的激活内存换成宽度，不是用循环替代参数（一次循环只值 r^0.46 份独立参数）。
2. **"循环几次"分裂成两个 regime。** 预训练算力受限 → 2（Loopie、LoopCoder-v2、SMELT、Nanbeige4.2）；推理算力可变 → 自适应且更深（Huginn 到 32–64）。LoopCoder-v2 的"三次以上回退"是 PLT 位置偏移的代价，不是循环的普适规律。
3. **循环粒度在变细、位置向中段收敛**（相对深度约 0.5）；MoE 必须 layer-mode。
4. **两种哲学**：把已训练模型的中段当 ODE 流（细分步长、保持终点）vs. 从头把循环训成不动点（STARS、Fixed-Point Reasoners、Attractor Models）。
5. **训练稳定性从经验教训变成定理**（残差缩放 1/N、DeepLoop 指数 1/2、学习率可跨循环数迁移）。
6. **推理成本被拆成延迟、KV 内存、量化三个子问题**，各有 2025–2026 年的方案（PLT、扩散式采样器、MELT、Looped Latent Attention 32×、LoopQ）。训练算力匹配 ≠ 推理成本匹配。
7. **隐式循环与显式 CoT 互补而非替代**：LoopCoder-v2 超加、LOTUS 弥合差距；标准 GRPO 与循环模型错配（RLTT、LoopRPT）。
8. **循环擅长"操作"知识，不擅长"存储"知识**——搭配检索、长上下文或 MoE 专家库。
9. **应用从数学谜题扩展到 agent 与具身智能**（SWE-bench、工具调用、VLA）。
10. **生产化已开始，工具链还没跟上。**

完整论证与出处见 [`survey/zh/survey_zh.md`](survey/zh/survey_zh.md)；被二次传播放大的五处说法与原文对照见综述附录 A。

## 复现

```bash
python3 src/fetch_metadata.py && python3 src/generator.py     # 论文表 -> README
export PAPER_CHINA_DEEPSEEK_API_KEY=...; export SUPER_TRANSLATE_HOME=/path/to/super_translate
bash scripts/translate_papers.sh                                # 保版式中译 + QA
bash scripts/build_pdfs.sh                                      # 报告 PDF（pandoc + XeLaTeX）
python3 scripts/export_slides.py                                # HTML 演示 -> PDF / 预览图
export PPT_MASTER_HOME=/path/to/ppt-master; bash scripts/build_pptx.sh   # 可编辑 PPTX
```

## 参与

在 [`data/papers.csv`](data/papers.csv) 加一行（或在 [`src/fetch_metadata.py`](src/fetch_metadata.py) 的 `CURATED` 里加 arXiv ID 后重跑），运行 `python3 src/generator.py`，提 PR。多个主题用 `;` 分隔。

## 许可

文字、报告、幻灯与数据：CC BY 4.0；`src/`、`scripts/` 代码：MIT。原论文版权归作者；`papers/zh/` 的中译为学习用途的衍生作品。
