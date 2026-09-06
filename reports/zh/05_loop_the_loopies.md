# 解读 05 · Loop the Loopies!：在同等预训练算力下，循环 MoE 第一次赢了普通 MoE

| 项目 | 内容 |
|---|---|
| 论文 | Loop the Loopies! |
| arXiv | [2607.16051](https://arxiv.org/abs/2607.16051)（2026-07） |
| 作者 | Zitian Gao、Yilong Chen、Yihao Xiao、Xinyu Yang、Ran Tao、Joey Zhou、Bryan Dai（IQuest Research） |
| 模型 | Loopie-20B-A2B、Loopie-6B-A0.6B（Base / Thinking） |
| 本仓库 | 原文 `papers/original/2607.16051.pdf` · 中译 `papers/zh/2607.16051.zh.pdf` |

## 一句话

循环 Transformer 长期被一个质疑压着：给 $N$ 倍预训练算力，把参数扩大 $N$ 倍通常比循环 $N$ 次更划算。Loopie 用三件事回应它：（1）把"整模型循环"换成"逐层循环"（layer-loop），（2）一套按**实测训练步时**而非理论 FLOPs 匹配算力的配方（Loopie Recipe），（3）只循环两次。结果是 Loopie-20B-A2B 在与 Qwen3-30B-A3B 复现版**相同的每步墙钟时间**下训练 800B token，在约 600B token 后反超并保持领先；配合 3.5T 预训练 + 2T "监督预训练"（SPT）+ 数学/代码 RL，20B-A2B 的 Thinking 版本 MMLU 81.28、AIME24 92.09，用不到 Nemotron 3 Nano（25T token）七分之一的预训练 token 达到相当或更好的成绩。

## 1. 要解决的问题

论文引言里的核心提问：**在相同的预训练算力预算下，循环 Transformer 能否追平或超过普通 Transformer？**

此前的循环工作（Ouro、Huginn）主要把循环当作**参数效率**手段：同样参数量下更强。但循环 $N$ 次，训练算力也约乘 $N$。要证明循环是**算力效率**手段，就必须和"把同样算力花在更多独立参数上"的普通模型比——在这个比较下，以往的循环模型通常输（Csordás 2024、Frey 2026）。加上现代前沿模型几乎都是 MoE（Qwen3、Kimi K2.5、GLM-5、DeepSeek-V4、MiniMax-M2），一个只在稠密模型上有效的循环方案没有通向前沿的路。

## 2. 核心方法

### 2.1 Layer-loop：换一种循环顺序

三层、两步循环的例子：

- **model-loop**（Ouro、Huginn 的做法）：Layer1 → Layer2 → Layer3 → Layer1 → Layer2 → Layer3
- **layer-loop**（Loopie）：Layer1 → Layer1 → Layer2 → Layer2 → Layer3 → Layer3

每层先在隐状态上局部迭代，再把结果交给下一层。作者给了三个理由：

1. **实测扩展性更好。** Loopie-6B-A0.6B 上，layer-loop 早期略落后 model-loop，约 1.2T token 后反超并拉开（Figure 2）。
2. **对基础设施友好。** 同一层的重复应用在前向和反向图中相邻，参数与梯度的复用距离短，激活检查点和梯度累积更简单；流水线并行下，一层的所有循环都在同一个 stage 内完成，不需要把末尾 stage 的输出送回首个 stage——model-loop 会引入循环依赖、增加通信和流水线气泡。
3. **参数共享模式更自然。** 48 层模型做 2 步 model-loop，第 3 层同时要服务有效深度 3 和 51 两个位置；已有分析表明 Transformer 表示沿深度并非均匀分布，前后段与中段差异大。layer-loop 让一层只在相邻的有效深度上复用，共享更"局部"。

消融（Section 2.7，Figure 5）：同骨干、同数据、同 token、同计算预算，去掉 layer-loop 的 6B-A0.6B 明显更差。改进不能归因于额外计算，而在于循环的调度方式。

### 2.2 Loopie Recipe：按实测步时匹配算力

预训练主导项 $\mathcal C(D,L,R)\propto L D^2 R$（宽度 $D$、存储层数 $L$、循环数 $R$），激活内存主导项 $M_{\text{act}}\propto s\,b\,D\,L$——注意激活内存随**存储深度**而非执行深度增长（同一层的所有循环放在同一个检查点单元里）。配方三步：

1. 从非循环参考模型出发（Qwen3-like 30B-A3B：$D_0=2048$，$L_0=48$，$R_0=1$），**层数减半、循环两次**得到种子模型（2048, 24, 2）。块执行次数 $LR=48$ 不变，主导算力不变，激活内存减半。
2. 把省下的内存换成**每卡 micro-batch 翻倍**（$b_1=2b_0$，梯度累积步数减半，每步 token 数不变），实测得到训练效率增益 $S_{\text{mb}}$。
3. 把效率增益**再投资到模型容量**：在种子附近扫 $(D,L)$，保留能支持 2 倍 micro-batch 的候选，选**实测优化器步时**与参考模型最接近的一个。

| 配置 | $D$ | $L$ | $R$ | 归一化算力 $\widehat C$ | 归一化激活内存 |
|---|---|---|---|---|---|
| Qwen3 30B-A3B（参考） | 2048 | 48 | 1 | 1.00× | 1.00× |
| 种子 Loopie | 2048 | 24 | 2 | 1.00× | 0.50× |
| 候选 1 | 2176 | 25 | 2 | 1.18× | 0.55× |
| **候选 2 → Loopie-20B-A2B** | **2304** | **27** | **2** | **1.42×** | **0.63×** |
| 候选 3 | 2432 | 28 | 2 | 1.65× | 0.69× |

Loopie-20B-A2B 名义上多做 42% 的 Transformer 块计算，但在 Megatron-LM 里（EP=8、MBS=2 对比参考的 EP=8、MBS=1）每步墙钟时间与参考持平。**作者明确说这不是 FLOPs 相等，是实测训练成本相等**——效率增益全部来自 micro-batch 翻倍。

### 2.3 为什么只循环两次（Section 2.8）

固定存储参数和步数时，多循环几乎总能改善训练曲线，但那不是算力匹配的比较。在固定预算下，多循环意味着更少 token、更小模型、或面对更强的普通基线。作者用 $N\times$ layer-loop 对比 $N\times$ 存储层（250B token，Figure 6）：**循环的边际收益在 $R=2$ 处最大，之后快速衰减。**

作者同时声明：这不是说更大循环数无效——推理算力便宜、有自适应计算、或研究目的是循环推理本身时，大 $R$ 有其价值；但**前沿预训练的主约束是总算力，此时 $R=2$ 是迭代精化、吞吐和算力匹配扩展之间最好的折中。**

## 3. 关键结果

### 3.1 算力匹配对照（Section 2.5，Figure 3）

Loopie-20B-A2B 与自复现的 Qwen3-30B-A3B 在**同一预训练预算**下各训 800B token。Loopie 早期落后，**约 600B token 后反超**并保持优势（8 个下游基准平均：ARC-C/E、BoolQ、CSQA、HellaSwag、MMLU、OBQA、WinoGrande）。

### 3.2 扩展梯（Section 2.6，Figure 4）

四级：非循环基线 0.15B / 0.25B / 0.5B / 1B（激活参数）对应算力匹配的 Loopie 0.10B / … / 0.70B，各训 1000× 激活参数量的 token（150B / 250B / 500B / 500B，最后一级受算力限制）。**四级全部 Loopie 领先，且差距不随规模缩小。**

### 3.3 预训练配方（Section 3）

- 阶段 1：Nemotron-CC-v2-HQ 约 570B 唯一 token，**训 4 个 epoch**（2.28T）——高质量数据多轮训练优于低质量数据单轮。
- 阶段 2：1.26T 高质量退火数据（Nemotron SFT-v1 27.8%、Specialized-v1 21.9%、Code-v2 20.7%、CC-v2-HQ-Synthetic 15.6%、CC-Math-v1 10.0%……）。
- 合计约 3.5T。Qwen3 tokenizer；AdamW，$\epsilon=10^{-15}$，权重衰减 0.1，学习率 $5\times10^{-4}$（6B）/ $3\times10^{-4}$（20B），**warmup-stable 无衰减**；batch 1024 × 8192。
- 初始化：嵌入 $\mathcal N(0,d^{-1})$，块内参数 SmallInit $\mathcal N(0,\tfrac{2}{5d})$——与 Huginn 采用的 Takase 初始化同源。

### 3.4 后训练：监督预训练（SPT）+ RL（Section 4）

**SPT** 是本文第二个方法贡献：用 SFT 的损失掩码（只对目标 token 计损失）配 PT 的优化规模（global batch ≥1024、序列 ≥128K、每 batch ≥1.28 亿 token 位置、总量 2T token、约 10 个 epoch）。

| | SPT | SFT | PT |
|---|---|---|---|
| 计损失位置 | 目标 token | 目标 token | 全部非 padding |
| 预训练指标（MMLU、ARC-C） | ↑ | **↓** | ↑ |
| 推理指标 | ↑ | ↑ | ≈ |
| 多 epoch 过拟合 | 未观察到 | 2–4 epoch 出现 | 未观察到 |
| 每 batch token 位置 | ≥128M | 128K–1M | 8–32M |

SPT 同时提升两类指标、10 个 epoch 无 loss 断崖（Figure 9–11）。作者的解释：每次更新聚合上千条序列、上亿 token 位置的监督，抑制了小 batch SFT 里的快速特化和记忆。这一结果直接挑战"SFT 必然导致灾难性遗忘"的常识。

**RL**：GSPO（序列级长度归一化重要性比 + 序列级裁剪）加 DAPO 的 clip-higher 与动态采样；先数学后代码，Guru-RL 语料；32K → 64K 响应长度分阶段。

### 3.5 Thinking 模型成绩（Table 3、4）

Loopie-20B-A2B Thinking（3.5T 预训练 token）对比：

| | Qwen3-30B-A3B Thinking (36T) | Nemotron 3 Nano 30B-A3B (25T) | Nemotron Cascade 2 (25T) | GPT-OSS 20B-A2B | **Loopie-20B-A2B (3.5T)** |
|---|---|---|---|---|---|
| MMLU | 85.83 | 80.52 | 81.22 | 81.64 | **81.28** |
| ARC-Challenge | 96.67 | 91.96 | 93.86 | 92.42 | 93.52 |
| BBH | 86.59 | 68.76 | 75.86 | 84.76 | 82.28 |
| IFEval | 85.58 | 77.05 | 79.21 | 70.03 | 84.72 |
| HumanEval | 96.95 | 86.59 | 79.88 | 92.07 | 89.02 |
| AIME 24 (avg@8) | 90.10 | 85.00 | 93.33 | 88.33 | 92.09 |
| AIME 25 | 83.75 | 74.17 | 91.25 | 87.50 | 83.75 |
| AMC | 96.73 | 91.80 | 93.57 | 91.05 | 94.21 |

用 Nemotron 同源数据的两个 25T 模型作对照：Loopie 在 7 个知识/通用基准里 5 个超过两者，token 用量不到它们的 1/7。

Loopie-6B-A0.6B：MMLU 78.36、**AIME24 80.42、AIME25 70.83**（Ouro 2.6B Thinking 为 62.50 / 51.67）、MATH-500 93.80。0.6B 激活参数拿到 80 分的 AIME24 是这张表里最惹眼的数字。

## 4. 为什么重要

1. **第一次在算力匹配下赢。** 这是循环深度从"学术玩具"到"可规模化预训练范式"的分界。此前的比较不是参数匹配（对循环有利）就是 FLOPs 匹配（对循环不利）；Loopie 用"实测墙钟时间匹配"给出第三种、也是对工业界最有意义的标准。
2. **把循环和 MoE 结合。** Huginn 论文第 9 节预测"循环擅长推理、MoE 擅长存储、未来架构会同时包含两者"，Loopie 是这个预测的第一个大规模实证。
3. **Layer-loop 有独立于本文的旁证。** Training-Free Looped Transformers 在不训练的前提下发现 MoE 必须 layer-mode；SMELT（2609.01343）在 FLOPs/参数/KV 三重匹配下也得出"中间一半层循环两次"的配方。三篇论文、三种实验范式、同一个结论。
4. **SPT 可能是独立于循环的贡献。** 它没有理由只对循环模型有效；如果在稠密模型上复现，会改变后训练的默认做法。

## 5. 局限与需要小心的地方

- **"算力匹配"是实测步时匹配，Loopie 的名义 FLOPs 高 42%。** 这个口径对训练成本公平，对推理成本不公平：推理时 Loopie-20B-A2B 每 token 做 27×2=54 次块计算，参考模型 48 次，且循环 KV cache 更大。论文没有报告推理延迟对比。
- 与 Qwen3-30B-A3B 的对照是**自复现版**，训 800B token（官方 36T）；Table 3 里与官方 Qwen3 Thinking 的差距（MMLU 81 vs 86、BBH 82 vs 87）是真实的。
- 扩展梯最大只到 1B 激活参数；20B-A2B 的算力匹配对照只有一个。
- $N\times$ 循环 vs $N\times$ 层的 Figure 6 中，$2\times$ 层基线的实际算力"显著高于" $2\times$ 循环模型（作者自述），这张图不能读成"2 倍循环被 2 倍层压制"。
- 不公开预训练代码；数据全部来自 Nemotron 公开集，可复现性尚可。

## 6. 与本方向其他工作的关系

- 前驱：UT（layer-tying）、ALBERT、MoEUT（MoE + UT 的第一次结合，但只在小规模上与标准 Transformer 持平）、Relaxed Recursive Transformers。
- 同团队：LoopCoder-v2（PLT，$R=2$）。两篇论文分别从算力匹配与机制诊断给出 $R=2$。
- 后继 / 同期：SMELT（2609.01343）为算力匹配 MoE 循环拟合 Chinchilla 式扩展律，节省 6.8–18.0% 训练 FLOPs，并发现第二次访问会削弱注意力沉降（attention sink）；Schwethelm et al. 的 $\varphi=0.46$ 解释了为什么"纯参数换循环"在 FLOPs 匹配下会输——Loopie 的做法是不做这种交换，而是用内存红利买宽度。
- 与 Hidden Decoding（2607.08186，微信 WeLM 617B）形成对照：后者认为循环与流水线并行不兼容，转而在序列长度维度上加算力；Loopie 的 layer-loop 恰恰是为了解决流水线并行兼容性。这是当前"怎样给每个 token 加算力"的两条竞争路线。

## 7. 对从业者的启示

- 做循环模型的算力对照实验时，按实测步时匹配而不是按 FLOPs：激活内存的节省是循环架构真实存在的红利，应当计入。
- MoE 骨干上默认 layer-loop；从流水线并行的角度这也是更容易实现的选择。
- 在前沿预训练预算下 $R=2$；更大的 $R$ 留给推理时自适应计算。
- SPT 值得在任何模型上试：把 SFT 数据当预训练数据用（大 batch、长序列、多 epoch），同时看预训练指标是否不再下降。
- 循环模型的推理成本仍是未解问题，部署前要实测延迟和 KV cache。

## 附：关键数字速查

- Loopie-20B-A2B：$D=2304$，$L=27$，$R=2$，名义算力 1.42×，激活内存 0.63×，步时与 Qwen3-30B-A3B 持平（MBS 2 vs 1）。
- 算力匹配对照：800B token，约 600B 后反超。扩展梯 4 级全胜。
- 预训练 3.5T（2.28T × 4 epoch HQ + 1.26T 退火）；SPT 2T、10 epoch；RL GSPO+DAPO，32K→64K。
- 20B-A2B Thinking：MMLU 81.28、ARC-C 93.52、BBH 82.28、IFEval 84.72、AIME24 92.09、AMC 94.21。
- 6B-A0.6B Thinking：AIME24 80.42、AIME25 70.83、MATH-500 93.80。
