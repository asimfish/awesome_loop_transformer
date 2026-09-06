# Report 05 · Loop the Loopies!: The First Compute-Matched Win for Looped MoE

| Item | Detail |
|---|---|
| Paper | Loop the Loopies! |
| arXiv | [2607.16051](https://arxiv.org/abs/2607.16051) (Jul 2026) |
| Authors | Zitian Gao, Yilong Chen, Yihao Xiao, Xinyu Yang, Ran Tao, Joey Zhou, Bryan Dai (IQuest Research) |
| Models | Loopie-20B-A2B, Loopie-6B-A0.6B (Base / Thinking) |
| In this repo | Original `papers/original/2607.16051.pdf` · Chinese `papers/zh/2607.16051.zh.pdf` |

## One sentence

Looped transformers have lived under one objection: given $N\times$ the pretraining compute, scaling parameters by $N$ usually beats looping $N$ times. Loopie answers with three moves — (1) replace whole-model looping with per-layer looping (layer-loop), (2) match compute by **measured optimizer-step wall-clock time** rather than theoretical FLOPs (the Loopie Recipe), (3) loop only twice. Loopie-20B-A2B, trained for 800B tokens at **the same per-step wall-clock time** as a reproduced Qwen3-30B-A3B, overtakes it after ~600B tokens and stays ahead; with 3.5T pretraining tokens, 2T tokens of "supervised pre-training" (SPT), and math/code RL, the 20B-A2B Thinking model reaches MMLU 81.28 and AIME24 92.09, matching or beating Nemotron 3 Nano (25T tokens) with less than one-seventh of its pretraining tokens.

## 1. The problem

The introduction's central question: **can looped transformers match or exceed vanilla transformers under the same pretraining compute budget?**

Earlier looped work (Ouro, Huginn) treated looping mainly as a **parameter-efficiency** device: stronger at equal parameter count. But looping $N$ times multiplies training compute by roughly $N$. To make looping a **compute-efficiency** device, it must beat a vanilla model that spends the same compute on more unique parameters — and under that comparison looped models had historically lost (Csordás 2024, Frey 2026). Since frontier models are now almost all MoE (Qwen3, Kimi K2.5, GLM-5, DeepSeek-V4, MiniMax-M2), a looping scheme that only works on dense backbones has no path to the frontier.

## 2. Method

### 2.1 Layer-loop: a different loop order

Three layers, two loop steps:

- **model-loop** (Ouro, Huginn): Layer1 → Layer2 → Layer3 → Layer1 → Layer2 → Layer3
- **layer-loop** (Loopie): Layer1 → Layer1 → Layer2 → Layer2 → Layer3 → Layer3

Each layer iterates locally on the hidden state, then hands the result to the next layer. Three reasons:

1. **Better measured scaling.** On Loopie-6B-A0.6B, layer-loop trails model-loop early and overtakes it after ~1.2T tokens, pulling away thereafter (Figure 2).
2. **Infrastructure-friendly.** Repeated applications of one layer are adjacent in the forward and backward graphs; parameter and gradient reuse distances are short, activation checkpointing and gradient accumulation are simpler. Under pipeline parallelism all loops of a layer stay on one stage; model-loop must route the last stage's output back to the first, creating cyclic dependencies, extra communication, and pipeline bubbles.
3. **A more natural sharing pattern.** A 48-layer model with 2 model-loop steps asks physical layer 3 to serve effective depths 3 and 51; transformer representations are known to be non-uniform across depth (early and late layers differ from the homogeneous middle). Layer-loop reuses a layer only at adjacent effective depths — more local sharing.

Ablation (§2.7, Figure 5): same backbone, data, tokens, and compute budget, but with layer-loop removed, the 6B-A0.6B model is clearly worse. The improvement cannot be attributed to extra computation; the schedule of recurrence matters.

### 2.2 The Loopie Recipe: match compute by measured step time

Leading-order pretraining compute $\mathcal C(D,L,R)\propto L D^2 R$ (width $D$, stored layers $L$, loops $R$); dominant activation memory $M_{\text{act}}\propto s\,b\,D\,L$ — it scales with **stored** depth, not executed depth, because all loops of a layer sit inside one checkpointing unit. Three steps:

1. From the non-recurrent reference (Qwen3-like 30B-A3B: $D_0=2048$, $L_0=48$, $R_0=1$), **halve the layers and loop twice** to get a seed (2048, 24, 2). Block executions $LR=48$ unchanged, leading compute unchanged, activation memory halved.
2. Spend the freed memory on **doubling the per-device micro-batch** ($b_1=2b_0$, gradient-accumulation steps halved, tokens per step unchanged) and measure the training-efficiency gain $S_{\text{mb}}$.
3. **Reinvest** the gain into capacity: sweep $(D,L)$ around the seed, keep candidates that still support 2× micro-batch, and select the one whose **measured optimizer-step time** is closest to the reference.

| Configuration | $D$ | $L$ | $R$ | Norm. compute $\widehat C$ | Norm. act. memory |
|---|---|---|---|---|---|
| Qwen3 30B-A3B (reference) | 2048 | 48 | 1 | 1.00× | 1.00× |
| Seed Loopie | 2048 | 24 | 2 | 1.00× | 0.50× |
| Candidate 1 | 2176 | 25 | 2 | 1.18× | 0.55× |
| **Candidate 2 → Loopie-20B-A2B** | **2304** | **27** | **2** | **1.42×** | **0.63×** |
| Candidate 3 | 2432 | 28 | 2 | 1.65× | 0.69× |

Loopie-20B-A2B nominally does 42% more transformer-block work, yet in Megatron-LM (EP=8, MBS=2 vs. the reference's EP=8, MBS=1) its per-step wall-clock matches the reference. **The authors state explicitly that this is not FLOP equality but measured-cost equality** — the entire efficiency gain comes from the doubled micro-batch.

### 2.3 Why only two loops (§2.8)

At fixed stored parameters and step count, more loops almost always improve the training curve — but that is not compute-matched. Under a fixed budget, more loops mean fewer tokens, a smaller model, or a stronger vanilla baseline. Comparing $N\times$ layer-loop against $N\times$ stored layers at 250B tokens (Figure 6): **the marginal benefit of recurrence is largest at $R=2$ and decays quickly.**

The authors add a caveat: this does not claim large loop counts are ineffective — cheap inference compute, adaptive computation, or studying recurrent reasoning per se all justify large $R$. But **frontier pretraining is bounded by total compute, and there $R=2$ is the best trade-off between iterative refinement, throughput, and compute-matched scaling.**

## 3. Key results

### 3.1 Compute-matched comparison (§2.5, Figure 3)

Loopie-20B-A2B versus a self-reproduced Qwen3-30B-A3B, each trained for 800B tokens under **the same pretraining budget**. Loopie trails early and **overtakes after ~600B tokens**, holding the lead (average over eight benchmarks: ARC-C/E, BoolQ, CSQA, HellaSwag, MMLU, OBQA, WinoGrande).

### 3.2 Scaling ladder (§2.6, Figure 4)

Four rungs: non-recurrent baselines at 0.15B / 0.25B / 0.5B / 1B active parameters versus compute-matched Loopies at 0.10B / … / 0.70B, each trained on 1000× its active parameter count in tokens (150B / 250B / 500B / 500B, the last capped by compute). **Loopie leads on all four rungs, and the gap does not shrink with scale.**

### 3.3 Pretraining recipe (§3)

- Stage 1: Nemotron-CC-v2-HQ, ~570B unique tokens, **4 epochs** (2.28T) — repeating high-quality data beats one pass over more, lower-quality data.
- Stage 2: 1.26T tokens of high-quality annealing data (Nemotron SFT-v1 27.8%, Specialized-v1 21.9%, Code-v2 20.7%, CC-v2-HQ-Synthetic 15.6%, CC-Math-v1 10.0%, …).
- ~3.5T total. Qwen3 tokenizer; AdamW, $\epsilon=10^{-15}$, weight decay 0.1, LR $5\times10^{-4}$ (6B) / $3\times10^{-4}$ (20B), **warm-up-stable with no decay**; batch 1024 × 8192.
- Initialization: embeddings $\mathcal N(0,d^{-1})$, block parameters SmallInit $\mathcal N(0,\tfrac{2}{5d})$ — the same Takase-style scheme Huginn used.

### 3.4 Post-training: Supervised Pre-training (SPT) + RL (§4)

**SPT** is the paper's second methodological contribution: SFT's loss masking (loss on target tokens only) combined with PT's optimization scale (global batch ≥1024, sequence ≥128K, ≥128M token positions per batch, 2T tokens total, ~10 epochs).

| | SPT | SFT | PT |
|---|---|---|---|
| Loss-bearing positions | target tokens | target tokens | all non-padding |
| Pretraining metrics (MMLU, ARC-C) | ↑ | **↓** | ↑ |
| Reasoning metrics | ↑ | ↑ | ≈ |
| Multi-epoch overfitting | not observed | at 2–4 epochs | not observed |
| Token positions per batch | ≥128M | 128K–1M | 8–32M |

SPT improves both metric families with no loss cliff over 10 epochs (Figures 9–11). The explanation: each update aggregates supervision from over a thousand sequences and >100M token positions, suppressing the rapid specialization and memorization of small-batch SFT. This directly challenges the received view that SFT necessarily causes catastrophic forgetting.

**RL**: GSPO (length-normalized sequence-level importance ratios and sequence-level clipping) plus DAPO's clip-higher and dynamic sampling; math first, then code; Guru-RL data; staged 32K → 64K response lengths.

### 3.5 Thinking-model results (Tables 3–4)

Loopie-20B-A2B Thinking (3.5T pretraining tokens) against peers:

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

Against the two 25T Nemotron models trained on the same data source, Loopie beats both on 5 of 7 knowledge/general benchmarks with under 1/7 of the tokens.

Loopie-6B-A0.6B: MMLU 78.36, **AIME24 80.42, AIME25 70.83** (Ouro 2.6B Thinking: 62.50 / 51.67), MATH-500 93.80. An 80 on AIME24 from 0.6B active parameters is the most striking number in the table.

## 4. Why it matters

1. **The first compute-matched win.** This is the boundary between "academic toy" and "scalable pretraining paradigm". Earlier comparisons were either parameter-matched (favoring loops) or FLOP-matched (disfavoring them); Loopie introduces measured-wall-clock matching — the third standard and the one industry cares about.
2. **Loops meet MoE.** Huginn's §9 predicted that recurrence (reasoning) and MoE (storage) are complementary and "a future architecture would contain both". Loopie is the first large-scale confirmation.
3. **Layer-loop has independent corroboration.** Training-Free Looped Transformers finds, without any training, that MoE needs layer-mode; SMELT (2609.01343) arrives at "loop the middle half twice" under FLOP/parameter/KV triple matching. Three papers, three experimental paradigms, one conclusion.
4. **SPT may be a contribution independent of looping.** Nothing in it is specific to looped models; if it reproduces on dense models it changes default post-training practice.

## 5. Limitations and caveats

- **"Compute-matched" means matched measured step time; Loopie's nominal FLOPs are 42% higher.** Fair for training cost, not for inference cost: Loopie-20B-A2B executes 27×2=54 block passes per token versus 48 for the reference, with a larger looped KV cache. No inference-latency comparison is reported.
- The Qwen3-30B-A3B comparison is a **self-reproduction** trained for 800B tokens (the official model: 36T); the gap to official Qwen3 Thinking in Table 3 (MMLU 81 vs 86, BBH 82 vs 87) is real.
- The scaling ladder tops out at 1B active parameters; the 20B-A2B compute-matched comparison is a single pair.
- In Figure 6's $N\times$ loop vs. $N\times$ layer comparison, the 2× layer baseline used "substantially more" compute than the 2× loop model (the authors say so); that figure cannot be read as "2× looping is dominated by 2× layers".
- Pretraining code is not released; data is entirely public Nemotron, so reproducibility is reasonable.

## 6. Relation to other work

- Predecessors: UT (layer tying), ALBERT, MoEUT (the first MoE + UT combination, but only on par with standard transformers at small scale), Relaxed Recursive Transformers.
- Same group: LoopCoder-v2 (PLT, $R=2$). The two papers reach $R=2$ by compute matching and by mechanistic diagnosis respectively.
- Successors / concurrent: SMELT (2609.01343) fits Chinchilla-style scaling laws for compute-matched looped MoE, saving 6.8–18.0% training FLOPs and finding that the second visit reduces the attention sink; Schwethelm et al.'s $\varphi=0.46$ explains why "trading parameters for loops" loses under FLOP matching — Loopie avoids that trade and buys width with the memory dividend instead.
- Contrast with Hidden Decoding (2607.08186, WeLM 617B): it argues looping is incompatible with pipeline parallelism and adds compute along the sequence dimension instead; Loopie's layer-loop exists precisely to make looping pipeline-friendly. These are the two competing routes to "more compute per token" today.

## 7. Practical takeaways

- Match compute by measured step time, not FLOPs, when comparing looped models: activation-memory savings are a real dividend of looped architectures and should count.
- Default to layer-loop on MoE backbones; it is also the easier choice for pipeline parallelism.
- Under frontier pretraining budgets use $R=2$; leave larger $R$ to adaptive inference-time compute.
- Try SPT on any model: treat SFT data as pretraining data (large batch, long sequences, many epochs) and watch whether pretraining metrics stop degrading.
- Inference cost of looped models remains open; measure latency and KV cache before deploying.

## Appendix: quick numbers

- Loopie-20B-A2B: $D=2304$, $L=27$, $R=2$, nominal compute 1.42×, activation memory 0.63×, step time equal to Qwen3-30B-A3B (MBS 2 vs 1).
- Compute-matched run: 800B tokens, overtakes after ~600B. Scaling ladder 4/4 wins.
- Pretraining 3.5T (2.28T = 4 epochs of HQ + 1.26T annealing); SPT 2T, 10 epochs; RL GSPO+DAPO, 32K→64K.
- 20B-A2B Thinking: MMLU 81.28, ARC-C 93.52, BBH 82.28, IFEval 84.72, AIME24 92.09, AMC 94.21.
- 6B-A0.6B Thinking: AIME24 80.42, AIME25 70.83, MATH-500 93.80.
