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

## Where to start

| You have | Read |
|---|---|
| 5 minutes | the ten insights below, then Appendix A of the survey (five popular claims the papers do not support) |
| 30 minutes | the [survey](survey/en/survey_en.md) §2–4 and §6, or the 21-slide [HTML deck](https://asimfish.github.io/awesome_loop_transformer/slides/html/) |
| 2 hours | the five [paper reports](reports/en/) — each opens with an at-a-glance box, a diagram, and closes with a glossary |
| a talk to give | the [Beamer deck](slides/beamer/loop_transformer_slides.pdf) (English) or the editable [PPTX](slides/pptx/awesome_loop_transformer_slides_zh.pptx) (Chinese) |

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

## [Content](#content)

<table>
<tr>
	<td>&emsp;<a href=#core-papers>1. Core Papers (5)</a></td>
	<td>&emsp;<a href=#surveys>2. Surveys (1)</a></td>
</tr>
<tr>
	<td>&emsp;<a href=#foundations-precursors>3. Foundations & Precursors (14)</a></td>
	<td>&emsp;<a href=#theory-expressivity-icl-length-generalization>4. Theory: Expressivity, ICL & Length Generalization (24)</a></td>
</tr>
<tr>
	<td>&emsp;<a href=#scaled-pretraining>5. Scaled Pretraining (17)</a></td>
	<td>&emsp;<a href=#efficiency-latency-kv-cache-quantization>6. Efficiency: Latency, KV Cache & Quantization (10)</a></td>
</tr>
<tr>
	<td>&emsp;<a href=#stability-training-theory>7. Stability & Training Theory (10)</a></td>
	<td>&emsp;<a href=#adaptive-computation-halting>8. Adaptive Computation & Halting (11)</a></td>
</tr>
<tr>
	<td>&emsp;<a href=#retrofitting-training-free>9. Retrofitting & Training-Free (7)</a></td>
	<td>&emsp;<a href=#post-training-rl-for-looped-models>10. Post-Training & RL for Looped Models (7)</a></td>
</tr>
<tr>
	<td>&emsp;<a href=#interpretability-latent-dynamics>11. Interpretability & Latent Dynamics (6)</a></td>
	<td>&emsp;<a href=#tiny-recursive-reasoners>12. Tiny Recursive Reasoners (9)</a></td>
</tr>
<tr>
	<td>&emsp;<a href=#applications-cross-modal>13. Applications & Cross-Modal (12)</a></td>
	<td>&emsp;<a href=#related-latent-reasoning-beyond-looping>14. Related: Latent Reasoning Beyond Looping (8)</a></td>
</tr>
<tr>
	<td>&emsp;<a href=#industry-reports-threads>15. Industry Reports & Threads</a></td>
	<td>&emsp;<a href=#open-models>16. Open Models</a></td>
</tr>
</table>

## [Core Papers](#content)

The five papers threaded together by the WeChat article / @nrehiew_ thread, in reading order. Each has a full report (ZH/EN) and a layout-preserving Chinese translation.

1. **⭐Universal Transformers.** ICLR, 2019. [paper](https://arxiv.org/abs/1807.03819), [code](https://github.com/tensorflow/tensor2tensor), [report-zh](reports/zh/01_universal_transformers.md), [report-en](reports/en/01_universal_transformers.md), [中译PDF](papers/zh/1807.03819.zh.pdf)

    *Mostafa Dehghani, Stephan Gouws, Oriol Vinyals, Jakob Uszkoreit, Łukasz Kaiser*
2. **⭐Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach.** arXiv, 2025. [paper](https://arxiv.org/abs/2502.05171), [code](https://github.com/seal-rg/recurrent-pretraining), [report-zh](reports/zh/02_recurrent_depth_huginn.md), [report-en](reports/en/02_recurrent_depth_huginn.md), [中译PDF](papers/zh/2502.05171.zh.pdf)

    *Jonas Geiping, Sean McLeish, Neel Jain, John Kirchenbauer, Siddharth Singh, Brian R. Bartoldson, Bhavya Kailkhura, Abhinav Bhatele, Tom Goldstein*
3. **⭐Training-Free Looped Transformers.** arXiv, 2026. [paper](https://arxiv.org/abs/2605.23872), [report-zh](reports/zh/03_training_free_looped.md), [report-en](reports/en/03_training_free_looped.md), [中译PDF](papers/zh/2605.23872.zh.pdf)

    *Lizhang Chen, Jonathan Li, Chen Liang, Ni Lao, Qiang Liu*
4. **⭐LoopCoder-v2: Only Loop Once for Efficient Test-Time Computation Scaling.** arXiv, 2026. [paper](https://arxiv.org/abs/2606.18023), [code](https://huggingface.co/Multilingual-Multimodal-NLP/LoopCoder-V2), [report-zh](reports/zh/04_loopcoder_v2.md), [report-en](reports/en/04_loopcoder_v2.md), [中译PDF](papers/zh/2606.18023.zh.pdf)

    *Jian Yang, Shawn Guo, Wei Zhang, Tianyu Zheng, Yaxin Du, Haau-Sing Li, Jiajun Wu, Yue Song, Yan Xing, Qingsong Cai, Zelong Huang, Chuan Hao, Ran Tao, Xianglong Liu, Wayne Xin Zhao, Mingjie Tang, Weifeng Lv, Ming Zhou, Bryan Dai*
5. **⭐Loop the Loopies!** arXiv, 2026. [paper](https://arxiv.org/abs/2607.16051), [report-zh](reports/zh/05_loop_the_loopies.md), [report-en](reports/en/05_loop_the_loopies.md), [中译PDF](papers/zh/2607.16051.zh.pdf)

    *Zitian Gao, Yilong Chen, Yihao Xiao, Xinyu Yang, Ran Tao, Joey Zhou, Bryan Dai*

## [Surveys](#content)

1. **A Survey on Latent Reasoning.** arXiv, 2025. [paper](https://arxiv.org/abs/2507.06203), [code](https://github.com/multimodal-art-projection/LatentCoT-Horizon/)

    *Rui-Jie Zhu, Tianhao Peng, Tianhao Cheng, Xingwei Qu, Jinfa Huang, Dawei Zhu, Hao Wang, Kaiwen Xue, Xuanliang Zhang, Yong Shan, Tianle Cai, Taylor Kergan, Assel Kembay, Andrew Smith, Chenghua Lin, Binh Nguyen, Yuqi Pan, Yuhong Chou, Zefan Cai, Zhenhe Wu, Yongchi Zhao, Tianyu Liu, Jian Yang, Wangchunshu Zhou, Chujie Zheng, Chongxuan Li, Yuyin Zhou, Zhoujun Li, Zhaoxiang Zhang, Jiaheng Liu, Ge Zhang, Wenhao Huang, Jason Eshraghian*

## [Foundations & Precursors](#content)

1. **Neural GPUs Learn Algorithms.** ICLR, 2016. [paper](https://arxiv.org/abs/1511.08228)

    *Łukasz Kaiser, Ilya Sutskever*
2. **Adaptive Computation Time for Recurrent Neural Networks.** arXiv, 2016. [paper](https://arxiv.org/abs/1603.08983)

    *Alex Graves*
3. **⭐Universal Transformers.** ICLR, 2019. [paper](https://arxiv.org/abs/1807.03819), [code](https://github.com/tensorflow/tensor2tensor), [report-zh](reports/zh/01_universal_transformers.md), [report-en](reports/en/01_universal_transformers.md), [中译PDF](papers/zh/1807.03819.zh.pdf)

    *Mostafa Dehghani, Stephan Gouws, Oriol Vinyals, Jakob Uszkoreit, Łukasz Kaiser*
4. **Deep Equilibrium Models.** NeurIPS, 2019. [paper](https://arxiv.org/abs/1909.01377)

    *Shaojie Bai, J. Zico Kolter, Vladlen Koltun*
5. **ALBERT: A Lite BERT for Self-supervised Learning of Language Representations.** ICLR, 2020. [paper](https://arxiv.org/abs/1909.11942)

    *Zhenzhong Lan, Mingda Chen, Sebastian Goodman, Kevin Gimpel, Piyush Sharma, Radu Soricut*
6. **Lessons on Parameter Sharing across Layers in Transformers.** arXiv, 2023. [paper](https://arxiv.org/abs/2104.06022)

    *Sho Takase, Shun Kiyono*
7. **Can You Learn an Algorithm? Generalizing from Easy to Hard Problems with Recurrent Networks.** NeurIPS, 2021. [paper](https://arxiv.org/abs/2106.04537)

    *Avi Schwarzschild, Eitan Borgnia, Arjun Gupta, Furong Huang, Uzi Vishkin, Micah Goldblum, Tom Goldstein*
8. **PonderNet: Learning to Ponder.** ICML Workshop, 2021. [paper](https://arxiv.org/abs/2107.05407)

    *Andrea Banino, Jan Balaguer, Charles Blundell*
9. **End-to-end Algorithm Synthesis with Recurrent Networks: Logical Extrapolation Without Overthinking.** NeurIPS, 2022. [paper](https://arxiv.org/abs/2202.05826)

    *Arpit Bansal, Avi Schwarzschild, Eitan Borgnia, Zeyad Emam, Furong Huang, Micah Goldblum, Tom Goldstein*
10. **Path Independent Equilibrium Models Can Better Exploit Test-Time Computation.** NeurIPS, 2022. [paper](https://arxiv.org/abs/2211.09961)

    *Cem Anil, Ashwini Pokle, Kaiqu Liang, Johannes Treutlein, Yuhuai Wu, Shaojie Bai, Zico Kolter, Roger Grosse*
11. **Sparse Universal Transformer.** EMNLP, 2023. [paper](https://arxiv.org/abs/2310.07096)

    *Shawn Tan, Yikang Shen, Zhenfang Chen, Aaron Courville, Chuang Gan*
12. **CoTFormer: A Chain-of-Thought Driven Architecture with Budget-Adaptive Computation Cost at Inference.** ICLR, 2025. [paper](https://arxiv.org/abs/2310.10845)

    *Amirkeivan Mohtashami, Matteo Pagliardini, Martin Jaggi*
13. **MoEUT: Mixture-of-Experts Universal Transformers.** NeurIPS, 2024. [paper](https://arxiv.org/abs/2405.16039)

    *Róbert Csordás, Kazuki Irie, Jürgen Schmidhuber, Christopher Potts, Christopher D. Manning*
14. **Relaxed Recursive Transformers: Effective Parameter Sharing with Layer-wise LoRA.** ICLR, 2025. [paper](https://arxiv.org/abs/2410.20672)

    *Sangmin Bae, Adam Fisch, Hrayr Harutyunyan, Ziwei Ji, Seungyeon Kim, Tal Schuster*

## [Theory: Expressivity, ICL & Length Generalization](#content)

1. **Looped Transformers as Programmable Computers.** ICML, 2023. [paper](https://arxiv.org/abs/2301.13196)

    *Angeliki Giannou, Shashank Rajput, Jy-yong Sohn, Kangwook Lee, Jason D. Lee, Dimitris Papailiopoulos*
2. **Looped Transformers are Better at Learning Learning Algorithms.** ICLR, 2024. [paper](https://arxiv.org/abs/2311.12424)

    *Liu Yang, Kangwook Lee, Robert Nowak, Dimitris Papailiopoulos*
3. **Simulation of Graph Algorithms with Looped Transformers.** ICML, 2024. [paper](https://arxiv.org/abs/2402.01107)

    *Artur Back de Luca, Kimon Fountoulakis*
4. **Looped Transformers for Length Generalization.** ICLR, 2025. [paper](https://arxiv.org/abs/2409.15647)

    *Ying Fan, Yilun Du, Kannan Ramchandran, Kangwook Lee*
5. **On Expressive Power of Looped Transformers: Theoretical Analysis and Enhancement via Timestep Encoding.** arXiv, 2024. [paper](https://arxiv.org/abs/2410.01405)

    *Kevin Xu, Issei Sato*
6. **Can Looped Transformers Learn to Implement Multi-step Gradient Descent for In-context Learning?** ICML, 2024. [paper](https://arxiv.org/abs/2410.08292)

    *Khashayar Gatmiry, Nikunj Saunshi, Sashank J. Reddi, Stefanie Jegelka, Sanjiv Kumar*
7. **Looped ReLU MLPs May Be All You Need as Practical Programmable Computers.** arXiv, 2024. [paper](https://arxiv.org/abs/2410.09375)

    *Yingyu Liang, Zhizhou Sha, Zhenmei Shi, Zhao Song, Yufa Zhou*
8. **Bypassing the Exponential Dependency: Looped Transformers Efficiently Learn In-context by Multi-step Gradient Descent.** AISTATS, 2025. [paper](https://arxiv.org/abs/2410.11268)

    *Bo Chen, Xiaoyu Li, Yingyu Liang, Zhenmei Shi, Zhao Song*
9. **On the Role of Depth and Looping for In-Context Learning with Task Diversity.** arXiv, 2024. [paper](https://arxiv.org/abs/2410.21698)

    *Khashayar Gatmiry, Nikunj Saunshi, Sashank J. Reddi, Stefanie Jegelka, Sanjiv Kumar*
10. **Reasoning with Latent Thoughts: On the Power of Looped Transformers.** ICLR, 2025. [paper](https://arxiv.org/abs/2502.17416)

    *Nikunj Saunshi, Nishanth Dikkala, Zhiyuan Li, Sanjiv Kumar, Sashank J. Reddi*
11. **To CoT or To Loop? A Formal Comparison Between Chain-of-Thought and Looped Transformers.** arXiv, 2025. [paper](https://arxiv.org/abs/2505.19245)

    *Kevin Xu, Issei Sato*
12. **What Makes Looped Transformers Perform Better Than Non-Recursive Ones.** arXiv, 2025. [paper](https://arxiv.org/abs/2510.10089)

    *Zixuan Gong, Yong Liu, Jiaye Teng*
13. **SpiralFormer: Looped Transformers Can Learn Hierarchical Dependencies via Multi-Resolution Recursion.** arXiv, 2026. [paper](https://arxiv.org/abs/2602.11698)

    *Chengting Yu, Xiaobo Shu, Yadao Wang, Yizhen Zhang, Haoyi Wu, You Wu, Rujiao Long, Ziheng Chen, Yuchi Xu, Wenbo Su, Bo Zheng*
14. **Thinking Deeper, Not Longer: Depth-Recurrent Transformers for Compositional Generalization.** arXiv, 2026. [paper](https://arxiv.org/abs/2603.21676)

    *Hung-Hsuan Chen*
15. **Loop, Think, & Generalize: Implicit Reasoning in Recurrent-Depth Transformers.** COLM, 2026. [paper](https://arxiv.org/abs/2604.07822)

    *Harsh Kohli, Srinivasan Parthasarathy, Huan Sun, Yuekun Yao*
16. **Stability and Generalization in Looped Transformers.** arXiv, 2026. [paper](https://arxiv.org/abs/2604.15259)

    *Asher Labovich*
17. **How Much Is One Recurrence Worth? Iso-Depth Scaling Laws for Looped Language Models.** arXiv, 2026. [paper](https://arxiv.org/abs/2604.21106)

    *Kristian Schwethelm, Daniel Rueckert, Georgios Kaissis*
18. **Universal Transformers Need Memory: Depth-State Trade-offs in Adaptive Recursive Reasoning.** arXiv, 2026. [paper](https://arxiv.org/abs/2604.21999)

    *Grigory Sapunov*
19. **Length Generalization with Log-Depth Recurrent Units.** arXiv, 2026. [paper](https://arxiv.org/abs/2605.26035)

    *Charles Pert, Dalal Alrajeh, Alessandra Russo*
20. **Chain-of-Thought and Compressed Looped Transformers: A Memory-Budget Separation.** arXiv, 2026. [paper](https://arxiv.org/abs/2605.30757)

    *Haozhou Zhang*
21. **Looped Transformers with Layer Normalization Provably Learn the Power Method.** arXiv, 2026. [paper](https://arxiv.org/abs/2606.00605)

    *Lyumin Wu, Chenyang Zhang, Yuan Cao*
22. **DiscoLoop: Looping Discrete Embeddings and Continuous Hidden States for Multi-hop Reasoning.** arXiv, 2026. [paper](https://arxiv.org/abs/2607.00341)

    *Hengyu Fu, Tianyu Guo, Zixuan Wang, Hanlin Zhu, Jason D. Lee, Jiantao Jiao, Stuart Russell, Song Mei*
23. **When Does Recurrence Become an Algorithm? Convergence Selection in Weight-Tied Looped Transformers.** arXiv, 2026. [paper](https://arxiv.org/abs/2607.20594)

    *Tong Zhang, Junhao Hu, Yun Peng, Tao Xie*
24. **Universal Transformers for Circuit Computations: Perfect Length Generalization in Tiny Transformers.** arXiv, 2026. [paper](https://arxiv.org/abs/2608.31067)

    *Takuya Ito, Ruchir Puri, Murray Campbell, Parikshit Ram*

## [Scaled Pretraining](#content)

1. **MoEUT: Mixture-of-Experts Universal Transformers.** NeurIPS, 2024. [paper](https://arxiv.org/abs/2405.16039)

    *Róbert Csordás, Kazuki Irie, Jürgen Schmidhuber, Christopher Potts, Christopher D. Manning*
2. **⭐Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach.** arXiv, 2025. [paper](https://arxiv.org/abs/2502.05171), [code](https://github.com/seal-rg/recurrent-pretraining), [report-zh](reports/zh/02_recurrent_depth_huginn.md), [report-en](reports/en/02_recurrent_depth_huginn.md), [中译PDF](papers/zh/2502.05171.zh.pdf)

    *Jonas Geiping, Sean McLeish, Neel Jain, John Kirchenbauer, Siddharth Singh, Brian R. Bartoldson, Bhavya Kailkhura, Abhinav Bhatele, Tom Goldstein*
3. **Parallel Loop Transformer for Efficient Test-Time Computation Scaling.** arXiv, 2025. [paper](https://arxiv.org/abs/2510.24824)

    *Bohong Wu, Mengzhao Chen, Xiang Luo, Shen Yan, Qifan Yu, Fan Xia, Tianqi Zhang, Hongrui Zhan, Zheng Zhong, Xun Zhou, Siyuan Qiao, Xingyan Bin*
4. **Scaling Latent Reasoning via Looped Language Models.** arXiv, 2025. [paper](https://arxiv.org/abs/2510.25741), [code](http://ouro-llm.github.io)

    *Rui-Jie Zhu, Zixuan Wang, Kai Hua, Tianyu Zhang, Ziniu Li, Haoran Que, Boyi Wei, Zixin Wen, Fan Yin, He Xing, Lu Li, Jiajun Shi, Kaijing Ma, Shanda Li, Taylor Kergan, Andrew Smith, Xingwei Qu, Mude Hui, Bohong Wu, Qiyang Min, Hongzhi Huang, Xun Zhou, Wei Ye, Jiaheng Liu, Jian Yang, Yunfeng Shi, Chenghua Lin, Enduo Zhao, Tianle Cai, Ge Zhang, Wenhao Huang, Yoshua Bengio, Jason Eshraghian*
5. **Depth-Recurrent Attention Mixtures: Giving Latent Reasoning the Attention it Deserves.** arXiv, 2026. [paper](https://arxiv.org/abs/2601.21582)

    *Jonas Knupp, Jan Hendrik Metzen, Jeremias Bohn, Georg Groh, Kristian Kersting*
6. **Adaptive Loops and Memory in Transformers: Think Harder or Know More?** ICLR Workshop, 2026. [paper](https://arxiv.org/abs/2603.08391)

    *Markus Frey, Behzad Shomali, Ali Hamza Bashir, David Berghaus, Joachim Koehler, Mehdi Ali*
7. **How Much Is One Recurrence Worth? Iso-Depth Scaling Laws for Looped Language Models.** arXiv, 2026. [paper](https://arxiv.org/abs/2604.21106)

    *Kristian Schwethelm, Daniel Rueckert, Georgios Kaissis*
8. **Hyperloop Transformers.** arXiv, 2026. [paper](https://arxiv.org/abs/2604.21254)

    *Abbas Zeitoun, Lucas Torroba-Hennigen, Yoon Kim*
9. **Latent Recurrent Transformer: Architecture Exploration, Training Strategies, and Scaling Behavior.** arXiv, 2026. [paper](https://arxiv.org/abs/2605.26797)

    *Zeyi Huang, Xuehai He, LiLiang Ren, Yiping Wang, Baolin Peng, Hao Cheng, Shuohang Wang, Pengcheng He, Jianfeng Gao, Yong Jae Lee, Yelong Shen*
10. **A Dual-Path Architecture for Scaling Compute and Capacity in LLMs.** arXiv, 2026. [paper](https://arxiv.org/abs/2605.30202)

    *Markus Frey, Behzad Shomali, Joachim Koehler, Mehdi Ali*
11. **⭐LoopCoder-v2: Only Loop Once for Efficient Test-Time Computation Scaling.** arXiv, 2026. [paper](https://arxiv.org/abs/2606.18023), [code](https://huggingface.co/Multilingual-Multimodal-NLP/LoopCoder-V2), [report-zh](reports/zh/04_loopcoder_v2.md), [report-en](reports/en/04_loopcoder_v2.md), [中译PDF](papers/zh/2606.18023.zh.pdf)

    *Jian Yang, Shawn Guo, Wei Zhang, Tianyu Zheng, Yaxin Du, Haau-Sing Li, Jiajun Wu, Yue Song, Yan Xing, Qingsong Cai, Zelong Huang, Chuan Hao, Ran Tao, Xianglong Liu, Wayne Xin Zhao, Mingjie Tang, Weifeng Lv, Ming Zhou, Bryan Dai*
12. **Hidden Decoding at Scale: Latent Computation Scaling for Large Language Models.** arXiv, 2026. [paper](https://arxiv.org/abs/2607.08186) — *contrast: sequence-length scaling*

    *Aiwei Liu, Cheng Shi, Chuhan Wu, Ci Lei, Di Lu, Donald He, Fan Zhang, Fanhao Kong, Feifei Zhang, Guan Wang, Haicheng Wang, Haoyu Liu, Houjin Yu, Jiachen Ding, Jiayi Feng, Jie Zhou, Jijun Chi, Jindi Shi, Jing Lei, Junjie Zhang, Laiyi Li, Le Tian, Linhao Zhang, Miao Fan, Sijun Zhang, Wei Jia, Weiwei Shi, Wenhan Li, Wentao Zhao, Wenteng Liang, Xiao Zhou, Xiaojin Zhou, Xihuai Wang, Xinyu Gao, Xuanliang Wang, Xuyang Ao, Yang Yu, Yangxiu You, Yinuo Zhao, Yufei Kuang, Yufei Wang, Yuan Liu, Yuan Liu, Yuwen Chen, Zhencong Tian, Zhongyin Zhao, Zilin Yu, Zitao Wang*
13. **⭐Loop the Loopies!** arXiv, 2026. [paper](https://arxiv.org/abs/2607.16051), [report-zh](reports/zh/05_loop_the_loopies.md), [report-en](reports/en/05_loop_the_loopies.md), [中译PDF](papers/zh/2607.16051.zh.pdf)

    *Zitian Gao, Yilong Chen, Yihao Xiao, Xinyu Yang, Ran Tao, Joey Zhou, Bryan Dai*
14. **Nanbeige4.2-3B: Unlocking Agentic Capabilities in a Compact Model.** arXiv, 2026. [paper](https://arxiv.org/abs/2607.22083)

    *Nanbeige Lab,  :, Chen Yang, Chengrui Huang, Fufeng Lan, Hanhui Chen, Hao Zhou, Huatong Song, Jiaqi Cao, Jiaying Zhu, Jinlin Niu, Kai Wang, Lisheng Huang, Qiliang Liang, Ran Le, Ruixiang Feng, Shuang Sun, Tao Gu, Tao Zhang, Tianyu Luo, Yang Song, Yun Xing, Yuntao Wen, Ziyao Xu, Zongchao Chen, Zongqiang Li*
15. **Gated Recurrent Transformers: Expressive Depth through Recurrent Modulation.** arXiv, 2026. [paper](https://arxiv.org/abs/2608.15062)

    *Amr Hegazy, Amr Alanwar, Mostafa Elhoushi*
16. **Allocating Recurrent Compute in Looped Language Models.** arXiv, 2026. [paper](https://arxiv.org/abs/2608.18230)

    *Ruhai Lin, Yiyang Guo, Rui-Jie Zhu, Hao Ye, Jason K. Eshraghian*
17. **SMELT: Scaling Laws for Compute-Matched MoE Looped Transformers.** arXiv, 2026. [paper](https://arxiv.org/abs/2609.01343)

    *Shaowen Wang, Ge Zhang, Kairong Luo, Yuhao Wu, Shaofan Liu, Jiaheng Liu, Wenhao Huang, Shen Yan, Jian Li*

## [Efficiency: Latency, KV Cache & Quantization](#content)

1. **Mixture-of-Recursions: Learning Dynamic Recursive Depths for Adaptive Token-Level Computation.** NeurIPS, 2025. [paper](https://arxiv.org/abs/2507.10524), [code](https://github.com/raymin0223/mixture_of_recursions)

    *Sangmin Bae, Yujin Kim, Reza Bayat, Sungnyun Kim, Jiyoun Ha, Tal Schuster, Adam Fisch, Hrayr Harutyunyan, Ziwei Ji, Aaron Courville, Se-Young Yun*
2. **Efficient Parallel Samplers for Recurrent-Depth Models and Their Connection to Diffusion Language Models.** arXiv, 2025. [paper](https://arxiv.org/abs/2510.14961), [code](https://github.com/seal-rg/recurrent-pretraining)

    *Jonas Geiping, Xinyu Yang, Guinan Su*
3. **Parallel Loop Transformer for Efficient Test-Time Computation Scaling.** arXiv, 2025. [paper](https://arxiv.org/abs/2510.24824)

    *Bohong Wu, Mengzhao Chen, Xiang Luo, Shen Yan, Qifan Yu, Fan Xia, Tianqi Zhang, Hongrui Zhan, Zheng Zhong, Xun Zhou, Siyuan Qiao, Xingyan Bin*
4. **Hyperloop Transformers.** arXiv, 2026. [paper](https://arxiv.org/abs/2604.21254)

    *Abbas Zeitoun, Lucas Torroba-Hennigen, Yoon Kim*
5. **Memory-Efficient Looped Transformer: Decoupling Compute from Memory in Looped Language Models.** arXiv, 2026. [paper](https://arxiv.org/abs/2605.07721)

    *Victor Conchello Vendrell, Arnau Padres Masdemont, Niccolò Grillo, Jordi Ros-Giralt, Arash Behboodi, Fabio Valerio Massoli*
6. **LoopQ: Quantization for Recursive Transformers.** arXiv, 2026. [paper](https://arxiv.org/abs/2605.16343)

    *Rui Fang, Hsi-Wen Chen, Ming-Syan Chen*
7. **LT2: Linear-Time Looped Transformers.** arXiv, 2026. [paper](https://arxiv.org/abs/2605.20670)

    *Chunyuan Deng, Yizhe Zhang, Rui-Jie Zhu, Yuanyuan Xu, Jiarui Liu, T. S. Eugene Ng, Hanjie Chen*
8. **CHASE: Cache-Hole-Adapted Skip Exit for Looped State-Space Language Models.** arXiv, 2026. [paper](https://arxiv.org/abs/2607.10110)

    *Zhenxuan Yu, Takeshi Kojima, Yutaka Matsuo, Yusuke Iwasawa*
9. **Looped Latent Attention: Cross-Loop KV Compression for Looped Transformers.** arXiv, 2026. [paper](https://arxiv.org/abs/2607.15456)

    *James O' Neill, Fergal Reid*
10. **Nanbeige4.2-3B on Apple Silicon: Fixing Deployment Bugs and Decreasing Looped Transformer Memory Overhead.** arXiv, 2026. [paper](https://arxiv.org/abs/2608.13987), [code](https://github.com/johnhalloran321/Nanbeige4.2-3B-mps-fix)

    *John T. Halloran*

## [Stability & Training Theory](#content)

1. **SCORE: Replacing Layer Stacking with Contractive Recurrent Depth.** arXiv, 2026. [paper](https://arxiv.org/abs/2603.10544)

    *Guillaume Godin*
2. **Simply Stabilizing the Loop via Fully Looped Transformer.** arXiv, 2026. [paper](https://arxiv.org/abs/2605.18797)

    *Rao Fu, Zixuan Yang, Jiankun Zhang, Jing Ma, Hechang Chen, Yu Li, Yi Chang*
3. **Solve the Loop: Attractor Models for Language and Reasoning.** arXiv, 2026. [paper](https://arxiv.org/abs/2605.12466)

    *Jacob Fein-Ashley, Paria Rashidinejad*
4. **Stabilizing Recurrent Dynamics for Test-Time Scalable Latent Reasoning in Looped Language Models.** ICML, 2026. [paper](https://arxiv.org/abs/2605.26733)

    *Xiao-Wen Yang, Ziyu Han, Xi-Hua Zhang, Wen-Da Wei, Jie-Jing Shao, Lan-Zhe Guo, Yu-Feng Li*
5. **On the Residual Scaling of Looped Transformers: Stability and Transferability.** arXiv, 2026. [paper](https://arxiv.org/abs/2606.18524)

    *Shaowen Wang, Bingrui Li, Ge Zhang, Wenhao Huang, Shen Yan, Jian Li*
6. **Fixed-Point Reasoners: Stable and Adaptive Deep Looped Transformers.** arXiv, 2026. [paper](https://arxiv.org/abs/2606.18206), [code](https://github.com/nilskiKonjIzDunava/fprm)

    *Sajad Movahedi, Vera Milovanović, Shlomo Libo Feigin, Alexander Theus, Thomas Hofmann, Valentina Boeva, T. Konstantin Rusch, Antonio Orvieto*
7. **Stabilizing Extrapolation in Looped Transformers via Learned Stochastic Stopping.** arXiv, 2026. [paper](https://arxiv.org/abs/2606.29983)

    *Hsun-Yu Kuo, El Mahdi Chayti, Patrik Reizinger, Wieland Brendel, Martin Jaggi*
8. **LayerNorm as Implicit Gain Control in Looped Transformers.** arXiv, 2026. [paper](https://arxiv.org/abs/2607.10681)

    *Matthias M. M. Buehlmaier*
9. **DeepLoop: Depth Scaling for Looped Transformers.** arXiv, 2026. [paper](https://arxiv.org/abs/2607.13491)

    *Shuzhen Li, Yifan Zhang, Jiacheng Guo, Quanquan Gu, Mengdi Wang*
10. **Think Shallow, Solve Deep: Controlling Recurrent Dynamics for Reliable Test-Time Depth.** arXiv, 2026. [paper](https://arxiv.org/abs/2608.18222)

    *Ivan Viakhirev, Kirill Borodin, Amirah Almutairi, Serguei Barannikov, Maxim Abramov, Grach Mkrtchian*

## [Adaptive Computation & Halting](#content)

1. **PonderNet: Learning to Ponder.** ICML Workshop, 2021. [paper](https://arxiv.org/abs/2107.05407)

    *Andrea Banino, Jan Balaguer, Charles Blundell*
2. **CoTFormer: A Chain-of-Thought Driven Architecture with Budget-Adaptive Computation Cost at Inference.** ICLR, 2025. [paper](https://arxiv.org/abs/2310.10845)

    *Amirkeivan Mohtashami, Matteo Pagliardini, Martin Jaggi*
3. **Mixture-of-Recursions: Learning Dynamic Recursive Depths for Adaptive Token-Level Computation.** NeurIPS, 2025. [paper](https://arxiv.org/abs/2507.10524), [code](https://github.com/raymin0223/mixture_of_recursions)

    *Sangmin Bae, Yujin Kim, Reza Bayat, Sungnyun Kim, Jiyoun Ha, Tal Schuster, Adam Fisch, Hrayr Harutyunyan, Ziwei Ji, Aaron Courville, Se-Young Yun*
4. **Two-Scale Latent Dynamics for Recurrent-Depth Transformers.** arXiv, 2025. [paper](https://arxiv.org/abs/2509.23314)

    *Francesco Pappone, Donato Crisostomi, Emanuele Rodolà*
5. **Think-at-Hard: Dynamic Looped Transformers for Improved Reasoning.** ICML, 2026. [paper](https://arxiv.org/abs/2511.08577), [code](https://github.com/thu-nics/TaH)

    *Tianyu Fu, Yichen You, Zekai Chen, Guohao Dai, Huazhong Yang, Yu Wang*
6. **LoopFormer: Elastic-Depth Looped Transformers for Latent Reasoning via Shortcut Modulation.** ICLR, 2026. [paper](https://arxiv.org/abs/2602.11451)

    *Ahmadreza Jeddi, Marco Ciccone, Babak Taati*
7. **Adaptive Loops and Memory in Transformers: Think Harder or Know More?** ICLR Workshop, 2026. [paper](https://arxiv.org/abs/2603.08391)

    *Markus Frey, Behzad Shomali, Ali Hamza Bashir, David Berghaus, Joachim Koehler, Mehdi Ali*
8. **Stabilizing Extrapolation in Looped Transformers via Learned Stochastic Stopping.** arXiv, 2026. [paper](https://arxiv.org/abs/2606.29983)

    *Hsun-Yu Kuo, El Mahdi Chayti, Patrik Reizinger, Wieland Brendel, Martin Jaggi*
9. **Adaptive Depth in Looped Transformers: Diagnosing Learned Halting Gates and Trajectory Readouts.** arXiv, 2026. [paper](https://arxiv.org/abs/2607.20519)

    *Andrei Cristian Popescu, Haitz Sáez de Ocáriz Borde, Pietro Liò*
10. **Per-Token Fixed-Point Convergence in Depth-Recurrent Transformers.** arXiv, 2026. [paper](https://arxiv.org/abs/2607.14427)

    *Joe Logan*
11. **RecurTrace: Adaptive Latent Reasoning with Loop-Time Memory.** arXiv, 2026. [paper](https://arxiv.org/abs/2609.03379)

    *Yuxiang Wang, Kunyu Feng, Yingda Shen, Haoning Xu, Junyu Wang, Zhizheng Wu*

## [Retrofitting & Training-Free](#content)

1. **Relaxed Recursive Transformers: Effective Parameter Sharing with Layer-wise LoRA.** ICLR, 2025. [paper](https://arxiv.org/abs/2410.20672)

    *Sangmin Bae, Adam Fisch, Hrayr Harutyunyan, Ziwei Ji, Seungyeon Kim, Tal Schuster*
2. **Teaching Pretrained Language Models to Think Deeper with Retrofitted Recurrence.** arXiv, 2025. [paper](https://arxiv.org/abs/2511.07384), [code](https://github.com/mcleish7/retrofitting-recurrence)

    *Sean McLeish, Ang Li, John Kirchenbauer, Dayal Singh Kalra, Brian R. Bartoldson, Bhavya Kailkhura, Avi Schwarzschild, Jonas Geiping, Tom Goldstein, Micah Goldblum*
3. **Improving Recursive Transformers with Mixture of LoRAs.** arXiv, 2025. [paper](https://arxiv.org/abs/2512.12880)

    *Mohammadmahdi Nouriborji, Morteza Rohanian, Omid Rohanian*
4. **Ouroboros: Dynamic Weight Generation for Recursive Transformers via Input-Conditioned LoRA Modulation.** arXiv, 2026. [paper](https://arxiv.org/abs/2604.02051)

    *Jaber Jaber, Osama Jaber*
5. **⭐Training-Free Looped Transformers.** arXiv, 2026. [paper](https://arxiv.org/abs/2605.23872), [report-zh](reports/zh/03_training_free_looped.md), [report-en](reports/en/03_training_free_looped.md), [中译PDF](papers/zh/2605.23872.zh.pdf)

    *Lizhang Chen, Jonathan Li, Chen Liang, Ni Lao, Qiang Liu*
6. **Skip a Layer or Loop It? Learning Program-of-Layers in LLMs.** ICML, 2026. [paper](https://arxiv.org/abs/2606.06574)

    *Ziyue Li, Yang Li, Tianyi Zhou*
7. **Retrofitting Recurrent Depth into a Pretrained Language Model: Installation, Extrapolation, Transfer, and Retention at Two Parameter Budgets.** arXiv, 2026. [paper](https://arxiv.org/abs/2608.11233)

    *Mark Shapiro*

## [Post-Training & RL for Looped Models](#content)

1. **Enhancing Auto-regressive Chain-of-Thought through Loop-Aligned Reasoning.** arXiv, 2025. [paper](https://arxiv.org/abs/2502.08482)

    *Qifan Yu, Zhenyu He, Sijie Li, Xun Zhou, Jun Zhang, Jingjing Xu, Di He*
2. **Prioritize the Process, Not Just the Outcome: Rewarding Latent Thought Trajectories Improves Reasoning in Looped Language Models.** ICML, 2026. [paper](https://arxiv.org/abs/2602.10520), [code](https://github.com/jonwill8/RLTT)

    *Jonathan Williams, Esin Tureci*
3. **LoopRPT: Reinforcement Pre-Training for Looped Language Models.** arXiv, 2026. [paper](https://arxiv.org/abs/2603.19714)

    *Guo Tang, Shixin Jiang, Heng Chang, Nuo Chen, Yuhan Li, Huiming Fan, Jia Li, Ming Liu, Bing Qin*
4. **Demystifying Hidden-State Recurrence: Switchable Latent Reasoning with On-Policy Reinforcement Learning.** arXiv, 2026. [paper](https://arxiv.org/abs/2606.13106)

    *Jiayu Yang, Chao Chen, Shengen Wu, Yinhong Liu, Yuxuan Fan, Lujundong Li, Songning Lai, Chengwei Qin, Zhijiang Guo*
5. **Dense Supervision Is Not Enough: The Readout Blind Spot in Looped Language Models.** arXiv, 2026. [paper](https://arxiv.org/abs/2606.24898)

    *Rituraj Sharma, Tu Vu*
6. **Bridging the Gap Between Latent and Explicit Reasoning with Looped Transformers.** arXiv, 2026. [paper](https://arxiv.org/abs/2606.31779), [code](https://github.com/yingfan-bot/lotus)

    *Ying Fan, Anej Svete, Kangwook Lee*
7. **LoopMTP: A looped transformer guided by latent multi-token prediction.** arXiv, 2026. [paper](https://arxiv.org/abs/2608.03624)

    *Behzad Shomali, Markus Frey, David Berghaus, Joachim Koehler, Mehdi Ali*

## [Interpretability & Latent Dynamics](#content)

1. **Latent Chain-of-Thought? Decoding the Depth-Recurrent Transformer.** Workshop, 2025. [paper](https://arxiv.org/abs/2507.02199), [code](https://github.com/wenquanlu/huginn-latent-cot)

    *Wenquan Lu, Yuechuan Yang, Kyle Lee, Yanshu Li, Enqi Liu*
2. **Two-Scale Latent Dynamics for Recurrent-Depth Transformers.** arXiv, 2025. [paper](https://arxiv.org/abs/2509.23314)

    *Francesco Pappone, Donato Crisostomi, Emanuele Rodolà*
3. **Loop as a Bridge: Can Looped Transformers Truly Link Representation Space and Natural Language Outputs?** arXiv, 2026. [paper](https://arxiv.org/abs/2601.10242)

    *Guanxu Chen, Dongrui Liu, Jing Shao*
4. **Step-resolved data attribution for looped transformers.** arXiv, 2026. [paper](https://arxiv.org/abs/2602.10097)

    *Georgios Kaissis, David Mildenberger, Juan Felipe Gomez, Martin J. Menten, Eleni Triantafillou*
5. **Observable Patterns Are Not Explanations: A Causal-Geometric Analysis of Latent Reasoning Models.** arXiv, 2026. [paper](https://arxiv.org/abs/2606.12689)

    *Darpan Aswal, Thomas Palmeira Ferraz, Yongxin Zhou, Maxime Peyrard*
6. **Looped Transformers under the Jacobian Lens: Does the Global Workspace Survive Recurrence?** arXiv, 2026. [paper](https://arxiv.org/abs/2609.01924)

    *Wenlong Wang, Fergal Reid*

## [Tiny Recursive Reasoners](#content)

1. **Hierarchical Reasoning Model.** arXiv, 2025. [paper](https://arxiv.org/abs/2506.21734)

    *Guan Wang, Jin Li, Yuhao Sun, Xing Chen, Changling Liu, Yue Wu, Meng Lu, Sen Song, Yasin Abbasi Yadkori*
2. **Hierarchical Reasoning Models: Perspectives and Misconceptions.** arXiv, 2025. [paper](https://arxiv.org/abs/2510.00355)

    *Renee Ge, Qianli Liao, Tomaso Poggio*
3. **Less is More: Recursive Reasoning with Tiny Networks.** arXiv, 2025. [paper](https://arxiv.org/abs/2510.04871)

    *Alexia Jolicoeur-Martineau*
4. **Latent Reasoning in TRMs is Secretly a Policy Improvement Operator.** arXiv, 2025. [paper](https://arxiv.org/abs/2511.16886)

    *Arip Asadulaev, Rayan Banerjee, Fakhri Karray, Martin Takac*
5. **Are Your Reasoning Models Reasoning or Guessing? A Mechanistic Analysis of Hierarchical Reasoning Models.** arXiv, 2026. [paper](https://arxiv.org/abs/2601.10679)

    *Zirui Ren, Ziming Liu*
6. **Dynamical Systems Theory Behind a Hierarchical Reasoning Model.** arXiv, 2026. [paper](https://arxiv.org/abs/2603.22871)

    *Vasiliy A. Es'kin, Mikhail E. Smorkalov*
7. **One Step Forward and K Steps Back: Better Reasoning with Denoising Recursion Models.** arXiv, 2026. [paper](https://arxiv.org/abs/2604.18839)

    *Chris Cameron, Wangzheng Wang, Nikita Ivanov, Ashmita Bhattacharyya, Didier Chételat, Yingxue Zhang*
8. **Solve the Loop: Attractor Models for Language and Reasoning.** arXiv, 2026. [paper](https://arxiv.org/abs/2605.12466)

    *Jacob Fein-Ashley, Paria Rashidinejad*
9. **Fixed-Point Reasoners: Stable and Adaptive Deep Looped Transformers.** arXiv, 2026. [paper](https://arxiv.org/abs/2606.18206), [code](https://github.com/nilskiKonjIzDunava/fprm)

    *Sajad Movahedi, Vera Milovanović, Shlomo Libo Feigin, Alexander Theus, Thomas Hofmann, Valentina Boeva, T. Konstantin Rusch, Antonio Orvieto*

## [Applications & Cross-Modal](#content)

1. **Block-Recurrent Dynamics in Vision Transformers.** arXiv, 2025. [paper](https://arxiv.org/abs/2512.19941)

    *Mozes Jacobs, Thomas Fel, Richard Hakim, Alessandra Brondetta, Demba Ba, T. Andy Keller*
2. **LoopViT: Scaling Visual ARC with Looped Transformers.** arXiv, 2026. [paper](https://arxiv.org/abs/2602.02156), [code](https://github.com/WenjieShu/LoopViT)

    *Wen-Jie Shu, Xuerui Qiu, Rui-Jie Zhu, Harold Haodong Chen, Yexin Liu, Harry Yang*
3. **Recurrent-Depth VLA: Implicit Test-Time Compute Scaling of Vision-Language-Action Models via Latent Iterative Reasoning.** arXiv, 2026. [paper](https://arxiv.org/abs/2602.07845), [code](https://rd-vla.github.io/)

    *Yalcin Tur, Jalal Naghiyev, Haoquan Fang, Wei-Chuan Tsai, Jiafei Duan, Dieter Fox, Ranjay Krishna*
4. **Looping Back to Move Forward: Recursive Transformers for Efficient and Flexible Large Multimodal Models.** arXiv, 2026. [paper](https://arxiv.org/abs/2602.09080)

    *Ruihan Xu, Yuting Gao, Lan Wang, Jianing Li, Weihao Chen, Qingpei Guo, Ming Yang, Shiliang Zhang*
5. **ELT: Elastic Looped Transformers for Visual Generation.** arXiv, 2026. [paper](https://arxiv.org/abs/2604.09168)

    *Sahil Goyal, Swayam Agrawal, Gautham Govind Anil, Prateek Jain, Sujoy Paul, Aditya Kusupati*
6. **RD-ViT: Recurrent-Depth Vision Transformer for Semantic Segmentation with Reduced Data Dependence Extending the Recurrent-Depth Transformer Architecture to Dense Prediction.** arXiv, 2026. [paper](https://arxiv.org/abs/2605.03999)

    *Renjie He*
7. **Déjà View: Looping Transformers for Multi-View 3D Reconstruction.** arXiv, 2026. [paper](https://arxiv.org/abs/2605.30215)

    *Alessandro Burzio, Tobias Fischer, Sven Elflein, Qunjie Zhou, Riccardo de Lutio, Jiawei Ren, Jiahui Huang, Shengyu Huang, Marc Pollefeys, Laura Leal-Taixé, Zan Gojcic, Haithem Turki*
8. **Test-Time Compute Scaling for ASR with Depth-Conditioned Looped Transformers.** arXiv, 2026. [paper](https://arxiv.org/abs/2606.04678)

    *Yacouba Kaloga, Shashi Kumar, Shakeel A. Sheikh, Driss Khalil, Petr Motlicek, Ina Kodrasi*
9. **LatentMT: Machine Translation with Latent Reasoning.** arXiv, 2026. [paper](https://arxiv.org/abs/2607.18618)

    *Wei-Rui Chen, Samar M. Magdy, Chiyu Zhang, Wenhui Zhu, Zhipeng Wang, Muhammad Abdul-Mageed*
10. **Nanbeige4.2-3B: Unlocking Agentic Capabilities in a Compact Model.** arXiv, 2026. [paper](https://arxiv.org/abs/2607.22083)

    *Nanbeige Lab,  :, Chen Yang, Chengrui Huang, Fufeng Lan, Hanhui Chen, Hao Zhou, Huatong Song, Jiaqi Cao, Jiaying Zhu, Jinlin Niu, Kai Wang, Lisheng Huang, Qiliang Liang, Ran Le, Ruixiang Feng, Shuang Sun, Tao Gu, Tao Zhang, Tianyu Luo, Yang Song, Yun Xing, Yuntao Wen, Ziyao Xu, Zongchao Chen, Zongqiang Li*
11. **ReLoop-UME: Recurrent Depth with Learnable Retrieval Registers for Universal Multimodal Embedding.** arXiv, 2026. [paper](https://arxiv.org/abs/2607.28751)

    *Shijie Wang, Xiangzhao Hao, Yueti Li, Guangyu Cao, Xinyu Tang, Haiyun Guo*
12. **Looped Language Models Improve Compositional Tool Calling.** arXiv, 2026. [paper](https://arxiv.org/abs/2608.18171)

    *Andrei Cristian Popescu, Haitz Sáez de Ocáriz Borde, Pietro Liò*

## [Related: Latent Reasoning Beyond Looping](#content)

1. **Think before you speak: Training Language Models With Pause Tokens.** ICLR, 2024. [paper](https://arxiv.org/abs/2310.02226)

    *Sachin Goyal, Ziwei Ji, Ankit Singh Rawat, Aditya Krishna Menon, Sanjiv Kumar, Vaishnavh Nagarajan*
2. **Mixture-of-Depths: Dynamically allocating compute in transformer-based language models.** arXiv, 2024. [paper](https://arxiv.org/abs/2404.02258)

    *David Raposo, Sam Ritter, Blake Richards, Timothy Lillicrap, Peter Conway Humphreys, Adam Santoro*
3. **Training Large Language Models to Reason in a Continuous Latent Space.** COLM, 2025. [paper](https://arxiv.org/abs/2412.06769)

    *Shibo Hao, Sainbayar Sukhbaatar, DiJia Su, Xian Li, Zhiting Hu, Jason Weston, Yuandong Tian*
4. **Compressed Chain of Thought: Efficient Reasoning Through Dense Representations.** arXiv, 2024. [paper](https://arxiv.org/abs/2412.13171)

    *Jeffrey Cheng, Benjamin Van Durme*
5. **PonderLM: Pretraining Language Models to Ponder in Continuous Space.** arXiv, 2025. [paper](https://arxiv.org/abs/2505.20674)

    *Boyi Zeng, Shixiang Song, Siyuan Huang, Yixuan Wang, He Li, Ziwei He, Xinbing Wang, Zhiyu Li, Zhouhan Lin*
6. **AbbIE: Autoregressive Block-Based Iterative Encoder for Efficient Sequence Modeling.** arXiv, 2025. [paper](https://arxiv.org/abs/2507.08567)

    *Preslav Aleksandrov, Meghdad Kurmanji, Fernando Garcia Redondo, David O'Shea, William Shen, Alex Iacob, Lorenzo Sani, Xinchi Qiu, Nicola Cancedda, Nicholas D. Lane*
7. **Encode, Think, Decode: Scaling test-time reasoning with recursive latent thoughts.** arXiv, 2025. [paper](https://arxiv.org/abs/2510.07358)

    *Yeskendir Koishekenov, Aldo Lipani, Nicola Cancedda*
8. **Closed-Loop Transformers: Autoregressive Modeling as Iterative Latent Equilibrium.** arXiv, 2025. [paper](https://arxiv.org/abs/2511.21882)

    *Akbar Anbar Jafari, Gholamreza Anbarjafari*

## [Industry Reports & Threads](#content)

1. **GPT-6 Astra.** OpenAI, 2026-09. [page](https://openai.com/index/gpt-6-astra/) — release page; no architectural details disclosed.
2. **Secret Technique Behind OpenAI's Astra Model Sparks Security Concerns.** The Information, 2026-09-02. Stephanie Palazzolo — reports Astra uses "recurrent depth" (anonymously sourced; paywalled, not accessed for this repository).
3. **Thread: five papers behind recurrent depth.** X, 2026-09. [@nrehiew_](https://x.com/nrehiew_/status/2095115984873062675) · [@kimmonismus](https://x.com/kimmonismus/status/2095045887131087357).
4. **刚刚，GPT-6 Astra 背后的 Loop 技术全被挖出来了.** 微信公众号 PaperAgent, 2026-09. [article](https://mp.weixin.qq.com/s/7vEMyFVpf2O9WL4Lu4gSFQ) — the Chinese write-up this repository started from; a snapshot is kept in [`source/`](source/).

## [Open Models](#content)

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
