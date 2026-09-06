---
title: "循环 Transformer 与循环深度：从 Universal Transformer 到 GPT-6 Astra 的八年（2018–2026）"
subtitle: "五篇核心论文深度解读 · 六十余篇相关文献图谱 · 十条趋势洞察"
author: "awesome_loop_transformer 项目组"
date: "2026-09-06"
---

# 摘要

同一组参数在深度方向上重复使用——这个 2018 年由 Universal Transformer 提出的想法，在 2025–2026 年成为大模型架构研究里增长最快的方向之一，并在 2026 年 9 月随着 The Information 关于 GPT-6 Astra 使用"recurrent depth"的报道进入公众视野。本报告以微信文章《刚刚，GPT-6 Astra 背后的 Loop 技术全被挖出来了》串起的五篇论文为骨架，逐篇核对原文，补齐被二次传播省略的前提和数字；再以 arXiv 全量检索为基础，把 2018–2026 年约 60 篇直接相关的工作按十个主题归类，提炼出十条趋势判断。核心结论有三：第一，循环深度已经在**实测算力匹配**的条件下第一次战胜普通 MoE Transformer（Loopie，2026-07），但胜利发生在"两步、逐层、MoE"这个窄配置里；第二，"循环几次"这个问题分裂成两个 regime——预训练算力受限时答案是 2，推理时算力可变时答案是"越多越好但要自适应"——LoopCoder-v2 的"三次以上回退"是并行循环设计的代价，不是循环深度的普适上限；第三，隐式循环与显式思维链是互补而非替代的两条测试时算力轴，二者叠加的收益超过各自之和。

# 1. 为什么现在讨论这件事

2026 年 9 月 2 日，The Information 报道 OpenAI 新发布的 GPT-6 Astra 使用了一种被称为 recurrent depth（循环深度）的架构技术。随后研究者 @nrehiew_ 在 X 上用五篇论文梳理了这条技术线的脉络，微信公众号 PaperAgent 将其整理为中文长文。本报告的直接目标是把这五篇论文读透，并把它们放回更大的文献图谱里。

关于 Astra 本身，本报告只做一件事：把可以核实的与不能核实的分开。**可以核实的**是五篇论文的内容、数字和相互关系。**不能核实的**是 Astra 究竟用了哪种循环、循环几次、如何训练——OpenAI 的发布页没有公开架构细节，The Information 的报道基于匿名信源，本文作者也无法访问这两份原始材料。凡涉及 Astra 的判断，本报告一律标注为推断。

# 2. 概念与分类

## 2.1 什么是循环 Transformer

标准 Transformer 的一次前向里，每层参数只用一次，深度等于参数量除以每层参数。**循环 Transformer**（looped / recurrent-depth / weight-tied / universal transformer）让同一组参数被反复应用，深度与参数量解耦：一个 4 层的块循环 32 次，就是 128 层的有效深度。

## 2.2 四种循环粒度

| 粒度 | 定义 | 代表 |
|------|-----------|--------------|
| 整模型循环（model-loop） | 整个层栈的输出再作为输入喂回 | Universal Transformer、Huginn（核心块）、Ouro |
| 块循环（block-loop） | 只循环中间一段连续层，首尾层不循环 | Huginn 的 prelude–core–coda、Hyperloop、Training-Free Looped、SMELT |
| 逐层循环（layer-loop） | 每一层先各自重复 K 次再传给下一层 | Loopie、Training-Free 的 layer-mode、MixerLoop（只循环 mixer） |
| 潜变量条件化 | 上一次循环（或上一个 token）的隐状态作为条件注入 | Coconut、PLT 的 CLP、Latent Recurrent Transformer |

四种粒度不互斥。Loopie 是 layer-loop；Huginn 是 block-loop 意义上的三段式、核心块内部是 model-loop；PLT 是 model-loop 加潜变量条件化（偏移一位的上轮状态）。

## 2.3 三个正交维度

除粒度外，还有三条彼此独立的设计轴：

1. **循环次数固定还是自适应。** 固定（每个 token 同样算力：Loopie、LoopCoder-v2）；训练时随机、推理时任选（Huginn）；逐 token 自适应停机（UT 的 ACT、Mixture-of-Recursions、Think-at-Hard、RecurTrace）。
2. **从头训练、改造、还是免训练。** 从头预训练（Huginn、Ouro、Loopie、Nanbeige4.2）；把已有模型改造成循环模型并继续训练（Relaxed Recursive Transformers、Retrofitted Recurrence）；完全不训练、推理时包一层（Training-Free Looped Transformers、Program-of-Layers）。
3. **训练目标把循环当什么。** 截断展开的普通语言建模（Huginn）；不动点/均衡（DEQ、Attractor Models、Fixed-Point Reasoners、STARS）；ODE 积分的细化（Training-Free）；带中间监督的潜在 CoT（LOTUS、LoopMTP）；带循环步奖励的 RL（RLTT、LoopRPT）。

# 3. 八年时间线

| 时间 | 事件 |
|-----|-------------------------|
| 2016 | Neural GPU（Kaiser & Sutskever）、Adaptive Computation Time（Graves）：循环 + 自适应停机的前身 |
| 2018-07 | **Universal Transformers**（Dehghani et al.）：跨时间步共享参数、坐标嵌入、ACT；ICLR 2019 |
| 2019 | ALBERT 把跨层共享用于压缩；Deep Equilibrium Models 用不动点求解代替显式展开 |
| 2021–2022 | Deep thinking 系列（Schwarzschild、Bansal）：随机展开 + 输入注入让循环网络从易到难外推；路径独立均衡模型（Anil） |
| 2023 | Looped Transformers as Programmable Computers（Giannou）：13 层循环 Transformer 模拟通用计算机；Looped Transformers are Better at Learning Learning Algorithms（Yang）：不到 10% 参数匹敌标准模型的 ICL；Sparse Universal Transformer |
| 2024 | MoEUT 首次让共享层模型在语言建模上略胜标准 Transformer；Relaxed Recursive Transformers（逐层 LoRA）；Looped Transformers for Length Generalization；Coconut 在连续空间推理 |
| 2025-02 | **Scaling up Test-Time Compute with Latent Reasoning**（Geiping et al.）：Huginn-3.5B，800B token，定名 recurrent depth；Reasoning with Latent Thoughts（Saunshi）证明 k 层循环 L 次≈kL 层 |
| 2025-05 | To CoT or To Loop（Xu & Sato）：循环擅长 DAG 求值，CoT 擅长自约化问题 |
| 2025-06–10 | HRM（27M 参数解数独/ARC）、Mixture-of-Recursions、TRM、Ouro（2.6B、7.7T token）、Parallel Loop Transformer、并行采样器（循环模型≈扩散语言模型） |
| 2025-11 | Retrofitted Recurrence（McLeish）；Think-at-Hard（只在难 token 上循环） |
| 2026-01–04 | LoopFormer（ICLR）、Depth-Recurrent Attention Mixtures、RLTT（ICML）、LoopRPT、Adaptive Loops and Memory、Hyperloop Transformers、迭代深度扩展律（φ=0.46）、Loop-Think-Generalize（COLM） |
| 2026-05 | **Training-Free Looped Transformers**（UT Austin）；MELT、LT2、LoopQ、STARS（ICML）、Fully Looped Transformer、Attractor Models、Dual-Path |
| 2026-06 | **LoopCoder-v2**（7B PLT，18T token，"只循环一次"）；Fixed-Point Reasoners；残差缩放 1/N 理论；LOTUS 弥合潜在 CoT 与显式 CoT 差距；Program-of-Layers（ICML） |
| 2026-07 | **Loop the Loopies!**（Loopie-20B-A2B，算力匹配首胜）；DeepLoop；Looped Latent Attention（KV 32× 压缩）；Nanbeige4.2-3B（28T token 循环模型进入 agentic 产品）；Hidden Decoding（微信 WeLM 617B 走序列长度路线） |
| 2026-08 | MixerLoop（只循环 mixer）、Gated Recurrent Transformers、Looped LMs 改善组合式工具调用、Think Shallow Solve Deep（稳定/漂移分类） |
| 2026-09 | **SMELT**：算力匹配 MoE 循环的 Chinchilla 式扩展律，节省 6.8–18% 训练 FLOPs；RecurTrace；GPT-6 Astra 发布，The Information 报道其使用 recurrent depth |

# 4. 五篇核心论文速览

详细解读见本仓库 `reports/zh/01–05`。这里给一张对照表。

| | Universal Transformers | Recurrent Depth (Huginn) | Training-Free Looped | LoopCoder-v2 | Loop the Loopies |
|------|---------|---------|---------|---------|---------|
| 时间 | 2018-07 | 2025-02 | 2026-05 | 2026-06 | 2026-07 |
| 机构 | UvA / DeepMind / Google | ELLIS / UMD / LLNL | UT Austin | 北航 / IQuest | IQuest |
| 循环粒度 | model-loop | block（三段式） | 中间 4 层，block 或 layer | model-loop（PLT） | layer-loop |
| 训练方式 | 从头 | 从头，800B token | **不训练** | 从头，18T token | 从头，3.5T token |
| 循环次数 | ACT 自适应 | 训练随机 r̄=32，推理任选 | K=3 级 RK | R=2（训练即推理） | R=2 |
| 规模 | ~65M | 3.5B 稠密 | 0.6B–30B（已有模型） | 7B 稠密 | 20B-A2B / 6B-A0.6B MoE |
| 关键数字 | bAbI 错误率 22.1→0.29 | r 4→32：ARC-E 49.1→69.9 | 45 格子 87% 非负，MMLU-Pro +2.64 | SWE-bench Verified 43.0→64.4→27.6 | 算力匹配 600B token 后反超 Qwen3-30B-A3B |
| 核心贡献 | 定义循环深度 + 停机 | 首次现代规模训成；隐空间轨道 | 层 = 欧拉步；子步而非重复 | 两步饱和的机制诊断；CoT 与循环超加 | Loopie Recipe；SPT |
| 最常被误读的点 | – | "同样 0.8T"基线实为 0.18T | 收益上限约 2–3 点 | 非单调是 PLT 特有 | "算力匹配"是实测步时，非 FLOPs |

## 4.1 五篇论文之间的逻辑关系

五篇论文构成一个完整的论证链：

1. UT 提出机制，但参数—计算比和训练稳定性未解。
2. Huginn 解决"能不能在现代规模训成"，代价是推理成本和知识容量。
3. Training-Free 解决"已有模型能不能白拿收益"，并给出 ODE 解释，同时发现 MoE 需要 layer-mode。
4. LoopCoder-v2 解决"部署时循环几次"，用 PLT 把延迟压平，发现 R=2 饱和并诊断原因。
5. Loopie 解决"算力匹配下能不能赢"，用 layer-loop + MoE + 实测步时匹配给出肯定答案，同样选 R=2。

# 5. 更广的文献图谱

以下分类基于 arXiv 检索（关键词 looped/recurrent-depth/depth-recurrent transformer、latent reasoning + loop 等），保留与语言模型架构直接相关的工作。完整列表见仓库 README 与 `data/papers.csv`。

## 5.1 理论：表达能力、ICL、长度泛化

- Giannou et al. 2023（ICML）：循环 Transformer 是可编程计算机。
- Yang et al. 2024（ICLR）：循环模型用 <10% 参数学会与标准模型同等的学习算法。
- Gatmiry et al. 2024（ICML）：循环 Transformer 能否学会多步梯度下降；Chen et al. 2025（AISTATS）：绕过指数依赖。
- Fan et al. 2025（ICLR）：自适应步数的循环 Transformer 显著改善长度泛化。
- Saunshi et al. 2025（ICLR）：许多推理问题需要深度而非参数；k 层循环 L 次≈kL 层；循环模型可模拟 T 步 CoT。
- Xu & Sato 2025：形式化分离——循环擅长确定性并行（DAG 求值），CoT 擅长自约化问题的近似推断。
- Gong et al. 2025：从损失景观解释——循环架构诱导 River-V-Valley 偏置。
- Zhang et al. 2026："预算律"：权重绑定循环模型学到的算法速度 v≈n_train/T_train，停机规则 T*=⌈n/v̂⌉。
- Wu et al. 2026：带 LayerNorm 的循环 Transformer 可证学会幂法。

## 5.2 规模化预训练

| 模型 | 规模 | Token | 循环 | 备注 |
|--------|-------|-----|---------|---------------|
| Huginn-0125 | 3.5B 稠密 | 0.8T | r̄=32，可任选 | 首个现代规模；公开 |
| Ouro 1.4B / 2.6B | 稠密 | 7.7T | 4 步 + 熵正则学习深度分配 | 匹敌 12B SOTA；优势来自知识操作而非存储；公开 |
| LoopCoder-v2 | 7B 稠密 PLT | 18T | 2 | 代码模型；公开 |
| Loopie-20B-A2B / 6B-A0.6B | MoE | 3.5T | 2（layer-loop） | 算力匹配首胜；公开 |
| Nanbeige4.2-3B | 3B | 28T | 2（层栈复用） | agentic 产品模型，超过 Qwen3.5-9B、Gemma4-12B |
| SMELT | MoE 至 54B 非嵌入参数 | – | 中间一半层 ×2 | 扩展律：省 6.8–18% 训练 FLOPs |

规模化预训练的共同点：**循环次数都很小（2–4）**，除 Huginn；**最新三个都是 layer-loop 或中段循环**；**MoE 骨干成为默认**。

## 5.3 效率：延迟、KV 内存、量化

- **延迟**：Parallel Loop Transformer（跨循环位置偏移，延迟≈单次前向）；Efficient Parallel Samplers（Geiping 2025）把循环模型视为扩散语言模型，diffusion-forcing 采样器免调参 5× 加速；Continuous Depth-wise Batching（Bae 2025）。
- **KV 内存**：Huginn 的循环 KV 共享（预算 4 不掉分）；Mixture-of-Recursions 的 KV 共享变体；MELT（跨循环共享单份 KV + 门控更新，Ouro 微调后常数内存）；**Looped Latent Attention**（发现跨循环 KV 轨迹低秩，SVD 编码器 32× 近无损，H200 上 Ouro-1.4B 批容量 32→768）；CHASE（循环 SSM 的跳出）。
- **注意力复杂度**：LT2（线性/稀疏注意力 + 循环，循环让线性注意力迭代精化记忆、让稀疏注意力扩大感受野；Ouro-hybrid-1.4B 约 1B token 转换）。
- **量化**：LoopQ（首个系统研究，W4A4 下相对最强 PTQ 基线平均精度 +68.8%）。
- **部署实录**：Halloran 2026 修复 Nanbeige4.2-3B 在 Apple Silicon 上的五个 bug，指出层复用使峰值注意力内存翻倍，分块预填充把可用上下文扩大 2.7×。

## 5.4 稳定性与训练理论

- Huginn 的两次失败（隐状态坍缩、循环坍缩）与三明治归一化。
- Wang et al. 2026（残差缩放）：权重共享使残差更新跨迭代相关，需要 ε=1/N 而非 1/√L；分解参数化 ε=λ/(N√L)；最优学习率只依赖唯一层数 L，可从小 N 直接迁移到大 N。
- DeepLoop：Post-LN DeepNorm 指数需从 1/4 升到 1/2，$\alpha=(2N)^{1/2}$，$\beta=(8N)^{-1/2}$。
- Fully Looped Transformer：把循环间信号分布到所有层 + 注意力注入，稳定训练到 12 次循环。
- STARS（ICML 2026）：雅可比谱半径正则化 + 随机循环采样，让潜在状态趋向渐近稳定不动点，缓解"某深度达峰后崩溃"。
- Fixed-Point Reasoners：pre-norm + 残差缩放 + 不动点收敛作为停机。
- Think Shallow, Solve Deep：算子的有限时间动力学 regime（settling / marginal / drifting）预测加深是否安全；单一终端不动点目标同时改变 regime 与深度行为；Huginn 属于 non-settling。
- Stabilizing Extrapolation via Learned Stochastic Stopping：训练时循环次数随机化大幅降低 OOD 方差。

## 5.5 自适应计算与停机

- 经典：ACT（2016）、PonderNet（2021）、CALM（2022）。
- Mixture-of-Recursions（NeurIPS 2025）：轻量路由器给每个 token 分配递归深度，只对活跃 token 做注意力和 KV 缓存，135M–1.7B 形成新 Pareto 前沿。
- Think-at-Hard（ICML 2026）："潜在过思考"——多数 token 第一遍已对，后续迭代反而改错；只在 93% 之外的难 token 上循环，+3.8–4.4%。
- LoopFormer（ICLR 2026）：shortcut-consistency 训练让不同长度轨迹对齐，按预算弹性推理。
- RecurTrace（2026-09）：循环记忆注意力（沿循环时间轴回看自己的历史状态）+ oracle 监督的停机头；MathQA 平均 2.0 次循环达 56.9%，ACT/PonderNet 坍缩到 1 次。
- Adaptive Depth in Looped Transformers（Popescu）：诊断学到的停机门。
- Two-Scale Latent Dynamics：基于步长二阶差分的提前退出优于 Huginn 的 KL 准则。

## 5.6 改造与免训练

- Relaxed Recursive Transformers（ICLR 2025）：把 Gemma 2B 等改造为共享块 + 逐层 LoRA，恢复大部分性能。
- Retrofitted Recurrence（McLeish 2025）：课程式逐步增加循环次数，数学任务上优于直接后训练原模型。
- Training-Free Looped Transformers（2026）：零训练，中间 4 层 RK 子步。
- Program-of-Layers（ICML 2026）：学一个小网络为每个输入生成"跳过/重复哪些层"的程序，常以更少层数取得更高精度。
- Retrofitting Recurrent Depth（Shapiro 2026）：两个参数预算下的安装、外推、迁移、保留研究。

## 5.7 后训练与强化学习

- LoopCoder-v2：Thinking（显式 CoT）叠加在 R=2 循环上，LiveCodeBench +26.9，超加。
- Loopie：SPT（SFT 掩码 + PT 规模，2T token 10 epoch 不过拟合、不遗忘）+ GSPO/DAPO RL。
- RLTT（ICML 2026）：标准 GRPO 只给最终潜在状态分配 credit，与循环模型内部计算错配；沿整条潜在轨迹分配奖励，Ouro-2.6B 数学 +10.9%。
- LoopRPT：把下一 token 预测重构为推理任务，用 EMA 教师给潜在步直接分配强化信号，压缩有效推理所需迭代数。
- LOTUS（Fan 2026）：并行处理 K 个潜在块、每个位置用金标 CoT token 交叉熵监督；首个在 3B 规模弥合潜在 CoT 与显式 CoT 差距的方法，思考阶段延迟降 2.5–6.9×。
- LoopMTP：第 t 次循环的隐状态软对齐到 t 步之后的 token 嵌入，稳定训练到 15 次循环。
- Dense Supervision Is Not Enough：循环模型的"读出盲区"。

## 5.8 可解释性与动力学

- Huginn 论文：轨道、滑块、不动点；路径独立。
- Lu et al. 2025：logit lens 探测 Huginn，可解释潜在 CoT 证据有限，探测结果高度依赖层与解码方式。
- Two-Scale Latent Dynamics：块内小步精化 + 块间大步漂移；训练中步长变小且趋于正交。
- Jacobian Lens（2026-09）：Ouro 每次循环重建"全局工作区"，线性传输无法跨循环边界；Huginn 跨 16 次循环携带内容，但读写只在约 2 次循环的滑动窗内起效。
- LoopCoder-v2：有效秩在第 2 次循环达峰后下降；更新方向震荡。
- Observable Patterns Are Not Explanations：对潜在推理模型的因果—几何分析，警示把可观察模式当解释。
- Step-resolved data attribution for looped transformers。

## 5.9 小型递归推理器

与 LLM 路线并行的另一支：不做语言建模，用几百万到几千万参数的循环网络解结构化难题。

- HRM（2025-06）：27M 参数、1000 样本，两个不同频率的递归模块，数独/迷宫近乎完美，ARC 超过更大模型。
- TRM（2025-10）：单个 2 层 7M 网络，ARC-AGI-1 45%、ARC-AGI-2 8%，超过多数 LLM。
- Attractor Models（2026-05）：不动点隐式微分，训练内存与有效深度无关；27M 参数数独 91.4%；770M 模型超过 2× token 的 1.3B Transformer；"均衡内化"现象——推理时可以去掉求解器。
- Denoising Recursion Models：多步去噪的递归训练，ARC-AGI 上超过 TRM。
- 批判性分析：Hierarchical Reasoning Models: Perspectives and Misconceptions；Are Your Reasoning Models Reasoning or Guessing。

## 5.10 跨模态与应用

- 视觉：LoopViT（18M 参数 ARC-AGI-1 65.8%，超过 73M 集成）、RD-ViT（语义分割）、ELT（视觉生成）、Déjà View（多视角 3D 重建）。
- 机器人：Recurrent-Depth VLA（单次迭代 0% 成功率的任务四次迭代 >90%，比基于 token 推理的 VLA 快 80×）。
- 语音：Depth-Conditioned Looped Transformers for ASR。
- Agent：Looped LMs Improve Compositional Tool Calling（多步工具调用随循环深度提升）；Nanbeige4.2-3B 的 agentic 部署。
- 多模态大模型：Looping Back to Move Forward（递归 LMM）。

# 6. 十条趋势洞察

## 洞察 1：循环深度跨过了"算力匹配"这道门，但只在窄门里

Loopie（2026-07）和 SMELT（2026-09）第一次在与普通模型**匹配训练成本**的条件下赢：前者按实测步时匹配，800B token 后反超 Qwen3-30B-A3B 复现版；后者在 FLOPs、参数、KV 三重匹配下拟合扩展律，节省 6.8–18% 训练 FLOPs，并且优势随规模不消失（SMELT 到 54B 非嵌入参数）。这两项结果把循环深度从"参数效率技巧"变成"算力效率技巧"。

胜利的配置极窄：**MoE 骨干、layer-loop 或中段循环、循环两次**。Schwethelm et al. 的迭代深度扩展律解释了为什么窄：一次循环只值 $r^{0.46}$ 份独立参数（截断反传下更低到 0.38），所以用循环替代参数在 FLOPs 匹配下必输；Loopie 的胜利不是靠循环换参数，而是靠循环省下的**激活内存**换 micro-batch、再换宽度。这是一个基础设施层面的红利，理论 FLOPs 看不见它。

## 洞察 2："循环几次"分裂成两个 regime

把所有报告的最优循环次数放在一起：Loopie 2、LoopCoder-v2 2、SMELT 2、Nanbeige4.2 2、Ouro 4、Huginn 32（可到 64）、RecurTrace 平均 2.0、Think-at-Hard 在 93% 的 token 上 1。

分裂线是**算力约束在哪里**。预训练算力受限时，每多一次循环就是训练 FLOPs 乘一个系数，边际收益在 R=2 后衰减最快（Loopie Figure 6），答案是 2。推理时算力可变时，同一个模型可以在难题上多循环、易题上少循环（Huginn 的 ARC-C 随 few-shot 数从 8 次饱和到 32 次饱和），答案是"按需、自适应"。

LoopCoder-v2 的"三次以上回退"经常被引用为循环深度的普适上限。论文自己的解释是 PLT 的跨循环位置偏移（CLP）在每次循环都收一笔固定的位置税，税额是第 3 次以后边际收益的 30–45 倍；顺序循环没有这一项。它是**并行化设计的代价**，不是循环的性质。

## 洞察 3：循环的粒度在变细，位置在向中间收敛

从 UT 的整模型循环，到 Huginn 的三段式（首尾不循环），到 Loopie/Training-Free/SMELT 的逐层或中段循环，再到 MixerLoop 只循环序列混合器而 FFN 只做一次（保留 41.5% 收益、省 45.9% 循环 FLOPs），粒度一路变细。三条独立证据指向同一个位置规则：Training-Free 的深度分数规则（最优窗口中心在相对深度 0.43–0.71，众数 0.5）、SMELT 的"中间一半"、Huginn 的"首尾层与中间层功能不同"的设计依据。首尾层负责嵌入和读出、特化程度高，不宜复用；中间层同质、可复用。

对 MoE，layer-loop 还有一个硬理由：block-loop 下每次迭代路由到不同专家（routing thrash）。Training-Free（不训练）与 Loopie（从头训练）在这一点上独立一致。

## 洞察 4：循环是 ODE 流还是不动点迭代？两种哲学正在分化

Training-Free 论文的发现是预训练 Transformer 的中段"在任何有用的意义上都不是压缩映射"：Anderson、heavy-ball、Aitken 等不动点加速器都不如简单的 RK 子步。因此对**已训练好的**模型，正确的循环是把 [0,1] 积分得更细（阻尼欧拉 x←(1−1/K)x+(1/K)g(x)），而不是推进到 t=K。

另一支工作反过来**把循环训练成不动点迭代**：STARS 用雅可比谱半径正则化、Fixed-Point Reasoners 用不动点收敛作停机、Attractor Models 用隐式微分求均衡。它们的动机是稳定性：Viakhirev et al. 把算子分为 settling / marginal / drifting 三类，settling 算子加深不会变差，且一个终端不动点目标就能把 drifting 变成 settling；Huginn 属于 non-settling。

两种哲学对应两个场景：改造已有模型时顺着 ODE 流走；从头训练时可以把稳定性设计进目标里。LoopCoder-v2 观察到的"更新方向震荡（cos θ<0）"正是 non-settling 的表现。

## 洞察 5：训练稳定性从经验教训变成了理论

Huginn 两次失败的训练（隐状态坍缩、循环坍缩）在 2025 年是经验教训，到 2026 年成了定理：残差缩放需要 1/N 而非 1/√L（Wang et al.），DeepNorm 指数要从 1/4 升到 1/2（DeepLoop），最优学习率只依赖唯一层数、可跨循环次数迁移。工程上，Fully Looped Transformer 稳定训练到 12 次循环，LoopMTP 到 15 次。加上 SmallInit 与三明治归一化，"循环模型难训"这个 2018 年以来的障碍在 2026 年基本被拆除。

## 洞察 6：推理成本是最后一个大瓶颈，而且正在被分解为三个子问题

循环模型的推理成本有三项：延迟（串行循环）、KV 内存（每次循环一份）、以及量化脆弱性。2025–2026 年每一项都有专门方案：延迟靠 PLT 的并行化或 Geiping 的扩散式并行采样器（5×）；KV 靠共享（Huginn、MoR、MELT）或压缩（Looped Latent Attention 发现跨循环 KV 低秩，32× 近无损）；量化靠 LoopQ。这些方案互相独立，可以叠加。

一个重要的度量口径问题：Loopie 的"算力匹配"是训练步时匹配，其推理时每 token 做 54 次块计算对比参考的 48 次，KV cache 更大，论文没报推理延迟。**训练算力匹配的胜利不自动等于推理成本匹配的胜利。**

## 洞察 7：隐式循环与显式 CoT 互补而非替代

三条证据：LoopCoder-v2 在 R=2 上叠加 thinking 模式，LiveCodeBench +26.9，远超两者单独贡献之和；LOTUS 用金标 CoT token 监督潜在位置，首次在 3B 规模追平显式 CoT 且思考延迟降 2.5–6.9×；Xu & Sato 的形式化分离说明两者各有擅长的问题类。

配套的发现是**标准 RL 与循环模型错配**：GRPO 只给最终潜在状态分配 credit（RLTT 指出这是 RL 改进循环模型屡次失败的原因），把奖励沿潜在轨迹分布后 Ouro-2.6B 数学 +10.9%；LoopRPT 进一步在预训练阶段就给潜在步分配强化信号。给循环模型做后训练需要重新设计目标，直接套用 CoT 时代的 RL 配方会浪费循环。

## 洞察 8：循环模型的能力剖面已经清楚——擅长"操作"知识，不擅长"存储"知识

Ouro 的对照实验把优势归因于知识操作而非知识容量；Huginn 闭卷弱、开卷强（OBQA +11.0）；Frey et al. 发现循环主要帮数学推理，记忆库主要帮常识任务，两者结合才能全面超过 iso-FLOP 基线；Dual-Path 把"深"（循环子层）和"宽"（大 FFN）作为并行通路，学到的门控显示标点、符号、算术 token 走深路，功能词和词汇内容走宽路。

这给出了循环模型的最佳搭档：**检索、长上下文、MoE 专家库**——任何把"存储"外置的机制。Loopie 与 SMELT 选 MoE 骨干，Adaptive Loops and Memory 加门控记忆库，都是这一逻辑。

## 洞察 9：应用面正在从数学谜题扩展到 agent 与具身智能

2025 年的循环模型证据集中在数独、迷宫、ARC、GSM8K；2026 年扩展到三类新场景：（1）**软件工程 agent**——LoopCoder-v2 的 SWE-bench Verified +21.4，Terminal-Bench 大幅提升；（2）**工具调用**——Popescu et al. 发现多步、有依赖的组合式工具调用随循环深度提升，Nanbeige4.2-3B 以 3B 参数在 agentic 基准上超过 Qwen3.5-9B；（3）**机器人**——RD-VLA 用循环动作头把某些任务从 0% 提到 >90%，比 token 推理 VLA 快 80×。共同点是这些任务都需要在一次前向内维护中间状态和依赖关系，正是循环的强项。

## 洞察 10：生产化已经开始，工具链还没跟上

开源的循环模型已有 Huginn、Ouro、LoopCoder-v2、Loopie、Nanbeige4.2-3B 五个家族，其中 Nanbeige4.2-3B 用 28T token 训练并作为产品发布。但 Halloran 的复现报告显示该模型在 Hugging Face transformers 上开箱即有五个 bug（包括被静默置零的 RoPE 缓冲区和已移除的 cache API 调用），修复后仍因层复用导致注意力内存翻倍。推理框架、量化工具、KV 管理都还没有为循环模型建立标准接口。Loopie 随论文发布了 megatron-loopie 与 vllm-loopie 两个分支，是往这个方向走的信号。

# 7. 关于 GPT-6 Astra 的推断（明确标注为推断）

以下判断基于本报告梳理的公开文献，**不基于**任何关于 Astra 的第一手信息。

1. 如果 Astra 确实使用 recurrent depth，公开文献中最接近"前沿规模 + 算力匹配"的配方是 Loopie/SMELT 路线：MoE 骨干、中段或逐层循环、循环次数很小。整模型循环 32 次的 Huginn 路线在前沿预训练预算下没有算力匹配的证据。
2. "OpenAI 找到了绕过两次饱和的办法"这一常见推测的前提不成立——两次饱和是 PLT 特有的现象。顺序循环模型（Huginn）本身就没有这个瓶颈；真正的瓶颈是推理成本，而 KV 压缩（32×）、扩散式并行采样（5×）等公开方案已经把它压低了一个量级。
3. The Information 报道提到的"安全担忧"与文献中的一个真实问题吻合：潜在推理不产生可读的中间 token，可解释性工作（Lu 2025、Jacobian Lens 2026）显示循环模型内部状态的探测结果依赖层与解码方式，监督其推理过程比监督 CoT 更难。
4. 时间点上，Loopie（7 月）、Looped Latent Attention（7 月）、SMELT（9 月 1 日）与 Astra（9 月初）密集出现，更合理的解读是这个方向在 2026 年上半年同时被多个团队推到可用，而不是某一篇论文直接导致了某个产品。

# 8. 未解问题

1. **多循环的算力匹配。** 所有算力匹配的胜利都在 R=2。R≥4 在预训练算力匹配下能否赢，没有公开证据。
2. **推理成本的完整账。** 需要同时报告训练步时、推理延迟、KV 峰值内存的对照；目前没有一篇论文三者齐全。
3. **循环模型的扩展律。** SMELT 拟合到 54B 非嵌入参数、Schwethelm 到 ~1B。两者的函数形式（Chinchilla 式加 $r^{\varphi}$ 项）是否在 100B+ 上成立未知。
4. **自适应停机在预训练规模上的收益。** MoR、TaH、RecurTrace 的结果都在 ≤8B；Ouro 的熵正则深度分配是唯一在 7.7T token 上验证过的。
5. **潜在推理的可监督性。** LOTUS 证明用金标 CoT 监督潜在位置有效，但这要求 CoT 数据；无 CoT 数据时如何让潜在轨迹可读、可审计，是安全层面的开放问题。
6. **layer-loop 的机制。** Loopie 给出的三个理由（扩展性、基础设施、共享局部性）中，只有扩展性有实验；SMELT 的"第二次访问削弱注意力沉降"是目前唯一的机制性解释。
7. **循环与序列长度扩展的取舍。** Hidden Decoding（WeLM 617B）走序列维度加算力并声称与流水线并行更兼容；Loopie 的 layer-loop 恰恰为兼容流水线并行而设计。两条路线在 100B+ 规模上尚无正面对比。

# 9. 结论

八年里，循环深度从一个解决 bAbI 过拟合的编码器—解码器技巧，变成了前沿模型架构的候选组件。2026 年上半年的三个转折——免训练循环让已有模型白拿 2 个点、PLT 让延迟不随循环增长、Loopie/SMELT 让循环 MoE 在算力匹配下第一次赢——共同把它推过了工程可行的门槛。剩下的问题集中在推理成本的完整核算、多循环的算力匹配、以及潜在推理的可监督性。对研究者，最有价值的空白是 R≥4 的算力匹配扩展律与循环专用的 RL 目标；对工程团队，最实用的结论是：中段循环、两次、layer-loop、MoE，并在部署前实测延迟和 KV。

# 附录 A：本报告核对过的传播误差

| 常见说法 | 原文事实 |
|----------|---------------|
| Huginn "同样 0.8T token"下循环模型碾压基线 | 非循环基线只训了 0.18T；同为 0.18T 时循环模型 ARC-E 53.62 vs 46.42 |
| "循环两次就够，三次以上回退"是循环 Transformer 的规律 | 是 PLT（跨循环位置偏移）特有的现象；Huginn 到 r=32 单调上升 |
| Loopie 与 Qwen3-30B-A3B "相同算力" | 相同实测优化器步时；Loopie 名义 FLOPs 高 42%，推理成本未报告 |
| Training-Free 让开源模型"变强" | 收益约 1–2.6 个百分点，集中在知识型多选题，小蒸馏模型可能掉分 |
| Huginn "3.5B 打出 50B 的表现" | FLOPs 等效，非基准等效；基准上接近 OLMo-7B、落后 OLMo-2 |

# 附录 B：方法与数据来源

- 五篇核心论文：arXiv 原文 PDF（`papers/original/`）与 arXiv HTML 全文（`papers/src/`），逐节核读。
- 中译：SuperTranslate 保版式翻译 + 对象级 QA（`papers/zh/`，QA 记录见 `QA_SUMMARY.md`）。
- 相关文献：arXiv API 检索（2026-09-06），关键词组合 looped/recurrent-depth/depth-recurrent transformer、latent reasoning ∧ (loop|recurrence|recursive)、命名模型；去重后保留 60 篇摘要于 `data/related_abstracts.json`。
- 写作规范：主张先行、必要限定只写一次、数字随处可核对；不引用无法访问的一手材料。
