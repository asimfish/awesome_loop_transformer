# Report 04 · LoopCoder-v2: In a Parallel Loop Transformer, the Second Loop Is Almost Everything

| Item | Detail |
|---|---|
| Paper | LoopCoder-v2: Only Loop Once for Efficient Test-Time Computation Scaling |
| arXiv | [2606.18023](https://arxiv.org/abs/2606.18023) (Jun 2026) |
| Authors | Jian Yang, Shawn Guo, Wei Zhang, Tianyu Zheng, Yaxin Du, Haau-Sing Li, Jiajun Wu, Yue Song, Yan Xing, Qingsong Cai, Zelong Huang, Chuan Hao, Ran Tao, Xianglong Liu, Wayne Xin Zhao, Mingjie Tang, Weifeng Lv, Ming Zhou, Bryan Dai (Beihang U. / IQuest Research / Langboat / Renmin U.) |
| Model | [Multilingual-Multimodal-NLP/LoopCoder-V2](https://huggingface.co/Multilingual-Multimodal-NLP/LoopCoder-V2) |
| In this repo | Original `papers/original/2606.18023.pdf` · Chinese `papers/zh/2606.18023.zh.pdf` |

## One sentence

Train four 7B Parallel Loop Transformer (PLT) coders with loop counts $R\in\{1,2,3,4\}$ from scratch on 18T tokens under one recipe, then instruction-tune them identically: $R=2$ lifts SWE-bench Verified from 43.0 to 64.4 and Multi-SWE from 14.0 to 31.0, while $R=3$ falls to 27.6 and $R=4$ to 22.4. Per-loop diagnostics show that the second loop carries nearly all productive refinement; after it, marginal gains collapse while the cross-loop position offset (CLP) that PLT introduces for parallelism charges a fixed "positional tax" 30–45× larger than the gain from loop 3 onward.

## 2. Background: why PLT

Standard sequential looping has a deployment-killing property: $R$ loops mean $R$ serial passes through the shared block, so latency scales by $R$; each layer caches KV at every loop, so memory is $O(R\cdot L\cdot S\cdot d)$, also scaling by $R$.

The Parallel Loop Transformer (PLT; Wu et al. 2025, arXiv 2510.24824) flattens both to near-constant with two mechanisms (Table 1):

| | Sequential loop | PLT |
|---|---|---|
| Execution | serial | parallel, single pass |
| Latency | $O(R\,C_{\text{block}})$ | $\approx C_{\text{block}}$ |
| KV cache | $O(RLSd)$ | $O(LSd)$ |
| Inter-loop input | $\mathbf{h}^{(r-1)}$ | $\mathrm{Embed}(x)+\mathrm{shift}(\mathbf{h}^{(r-1)})$ |

1. **Shared KV + gated sliding-window attention (G-SWA).** The first loop's KV $K_{\text{share}},V_{\text{share}}$ is frozen and shared with all later loops; each later attention layer outputs a per-head gated mix of a global branch (full attention over the frozen KV) and a local branch (sliding-window attention of width $w=64$ over the current loop's KV): $\tilde y^{(r)}=g\odot y^{(r)}_{\text{global}}+(1-g)\odot y^{(r)}_{\text{local}}$, $g=\sigma(f_{\text{gate}}(\mathrm{RMSNorm}(\mathbf h)))$.
2. **Cross-loop position offset (CLP).** The input to loop $r\ge2$ is $B^{(r)}=\mathrm{Embed}(x)+\mathrm{shift}(\mathbf h^{(r-1)})$, where shift moves the previous loop's hidden states **one position to the right**. Loop $r$ of token $x_i$ can then run in the same forward pass as loop $r+1$ of token $x_{i-1}$.

**The price:** at loop $r$, token $x_i$ receives not its own previous state but its neighbor $x_{i-1}$'s. This is the **positional mismatch** — an information constraint unique to PLT that standard looping never incurs.

## 3. Question and method

PLT makes loop count a free deployment choice, which raises the question: how many? Training every candidate is expensive and explains nothing. The authors frame it as gain versus cost: each extra loop offers marginal refinement on one side and CLP's fixed mismatch cost on the other.

### 3.1 Macroscopic protocol

- 7B dense PLT, G-SWA window 64, first-loop KV sharing.
- Pretrained from scratch on 18T tokens, text:code 1:1, 100+ programming languages; Adam (0.9, 0.95), $\epsilon=10^{-15}$, weight decay 0.1, LR $4\times10^{-4}$ cosine with 5% warm-up; bf16; **1M GPU hours** total.
- Training and inference loop counts matched (trained at $R=r$, evaluated at $R=r$).
- All four models instruction-tuned on the same 6M examples; final checkpoint reported.
- Infrastructure: custom Megatron-LM unrolling $R$ loops into $R\cdot L$ scheduled layers with a single set of parameters; all loop instances of a layer co-located on one pipeline stage so weight sharing is communication-free.

### 3.2 Microscopic diagnostics (§3.2)

Four per-loop lens groups; a mechanism is credited only when they agree:

- **Hidden-state dynamics**: step size $\delta^{(r)}=\|\mathbf h^{(r)}-\mathbf h^{(r-1)}\|$; cosine between successive updates $\cos\theta^{(r)}$ (<0 = direction reversal, oscillation); effective rank $\mathrm{erank}$ (entropy-exponential of normalized singular values, a scale-free diversity measure); fixed-point gap $\Delta_{\text{FP}}^{(r)}=\|\mathbf h^{(r)}-f_\theta(\mathbf h^{(r)})\|$.
- **Attention evolution**: attention entropy, inter-loop attention KL $D_{\text{KL}}^{(r)}$, head–head cosine similarity, mean G-SWA gate $\bar g^{(r)}$.
- **Output-distribution shift**: logit-lens rank of the gold token, inter-loop output KL $\Delta p^{(r)}$, output entropy.
- **Intrinsic offset cost** $\Omega^{(r)}=\frac1S\sum_i\|\mathbf h^{(r-1)}_i-\mathbf h^{(r-1)}_{i-1}\|$: mean distance between adjacent token representations. The less alike neighbors are, the more distortion from substituting a neighbor's state for one's own.

## 4. Key results

### 4.1 Main table (Table 2, four 7B variants)

| Model | HE+ | MultiPL-E | BCB | LCB | SWE-V | Multi-SWE | TB-v1 | TB-v2 | M2W | BFCL | Avg |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Baseline $R=1$ | 81.1 | 69.5 | 40.1 | 27.4 | 43.0 | 14.0 | 26.3 | 11.2 | 35.3 | 32.2 | 38.0 |
| **$R=2$** | **84.1** | **73.9** | **46.1** | **35.4** | **64.4** | **31.0** | **34.2** | **21.0** | 34.5 | **40.1** | **46.5** |
| $R=3$ | 75.0 | 69.8 | 43.3 | 28.6 | 27.6 | 11.0 | 30.0 | 12.2 | 35.1 | 36.3 | 36.9 |
| $R=4$ | 76.8 | 67.3 | 40.8 | 24.5 | 22.4 | 9.3 | 26.3 | 9.0 | **41.4** | 39.5 | 34.3 |

Three observations:

- **Strongly non-monotonic.** $R=2$ averages +8.5; $R=3$ is 1.1 *below* baseline; $R=4$ lower still. SWE-bench Verified: 43.0 → 64.4 → 27.6 → 22.4.
- **One extra loop puts a 7B model among much larger systems.** 64.4 on SWE-bench Verified beats Kimi-Dev-72B (60.4) and Qwen3-235B-A22B (45.2) and approaches Qwen3-Coder-480B (67.0). On the held-out agentic SWE-bench-CC it reaches 33.4%.
- **Gains concentrate on agentic and reasoning tasks.** SWE, Terminal-Bench, LiveCodeBench move most; Mind2Web is best at $R=4$ — single-benchmark noise the authors do not over-read.

### 4.2 Diagnostics: what loop 2 does and why loop 3 hurts (§4.2, Table 3)

PLT4 statistics over 500 held-out samples:

| Loop | Step $\delta$ | Output shift $\Delta p$ | Eff. rank | $\cos\theta$ |
|---|---|---|---|---|
| $r=2$ | **846** | **1.75** | **174.6** | −0.72 |
| $r=3$ | 464 | 1.32 | 172.5 | −0.46 |
| $r=4$ | 1014 | 1.58 | 158.2 | 0.04 |

- **Loop 2 is the principal site of productive refinement**: largest attention re-routing $D_{\text{KL}}^{(2)}$, largest output shift, peak effective rank.
- **After loop 2, returns collapse**: $\Delta p$ and $D_{\text{KL}}$ drop sharply; effective rank declines from its peak — later loops **narrow** the representational subspace rather than enrich it; attention heads grow redundant (Figure 4); update directions reverse ($\cos\theta<0$) — oscillation, not convergence. In the four-loop model, loop 3 is nearly a dead pass-through and loop 4's large step is output readout, not new refinement (it has the lowest effective rank).
- **The gate stays above 0.5**: later loops keep leaning on the frozen loop-1 global KV rather than constructing qualitatively new context.
- **The offset is a fixed tax**: $\Omega^{(r)}$ is roughly constant across loops while $\Delta p^{(r)}$ collapses after loop 2. Figure 3's "scissors": at every extra loop the offset cost exceeds the marginal gain by **30–45×**.

Diminishing gains against a fixed cost: the net effect peaks at $R=2$ and turns negative afterward.

### 4.3 Explicit CoT and latent looping are complementary (Table 4)

At the optimal $R=2$, the instruction model (latent loop only) versus the thinking model (explicit CoT + loop):

| $R=2$ | LCB | CRUX | MultiPL-E | FullStackBench | BCB-Hard |
|---|---|---|---|---|---|
| Instruct (loop only) | 35.4 | 86.9 | 73.9 | 47.2 | 23.7 |
| Thinking (CoT + loop) | **62.3** | **93.5** | **77.8** | **49.9** | **26.4** |
| Δ | +26.9 | +6.6 | +3.9 | +2.7 | +2.7 |

LiveCodeBench +26.9 far exceeds the sum of the two ingredients: explicit CoT alone does not improve the non-looped model on these tasks, and the loop alone gives single digits. The authors' explanation is that the two act at different granularities — CoT decomposes the problem into textual steps, the loop refines the representation under each step — so they compound **super-additively**. This is the paper's most forward-looking conclusion: **latent depth recurrence and explicit reasoning are complementary axes of test-time compute, not substitutes.**

## 5. Where the conclusion applies (important)

"Two loops suffice, three regress" tends to lose its preconditions in circulation. The paper's own boundaries are clear:

1. **It is a PLT-specific phenomenon.** The mechanistic explanation of non-monotonicity depends on the fixed positional tax of CLP; standard sequential looping has no such term. Huginn (sequential, input-injected) improves monotonically from $r=4$ to $r=32$; Ouro uses 4 steps; Fixed-Point Reasoners and STARS study how to keep dozens of loops stable.
2. **Training and inference loop counts are tied.** Each $R$ is a separately trained model, not one model evaluated at different $R$. Here $R$ is part of the training recipe, not a test-time compute knob.
3. **Same $R=2$ answer as Loopie, different reason.** Loopie picks 2 because marginal returns decay fastest under a **fixed pretraining compute budget**; LoopCoder-v2 picks 2 because of CLP's fixed cost. The two papers share authors (Bryan Dai and Ran Tao appear on both), so they can be read as one group answering the same question from a compute-matching angle and a mechanistic angle.
4. **Effective rank is an actionable diagnostic.** If effective rank is still rising at the candidate loop, another loop may still refine; once it turns down, further loops mostly pay the positional tax. No exhaustive training sweep needed.

## 6. Limitations

- One run per variant, single seed; a 1M-GPU-hour budget rules out replication. The $R=3$ drop on SWE (−15.4) is too large to be noise, but the reverse swing on Mind2Web is a reminder that the main table has variance.
- One architecture (PLT), one scale (7B dense). Whether "two is optimal" changes with scale or MoE backbones is unknown (SMELT, 2609.01343, independently lands on "loop the middle half twice" for MoE).
- No ablation removing CLP (what would sequential looping do at $R=3$?). The mechanistic account is therefore convergent evidence, not a causal experiment.
- The 18T pretraining mixture is not released; only the code-language distribution is given.

## 7. Relation to other work

- Predecessor: PLT (Wu et al. 2025) supplies the architecture; LoopCoder-v1 details are not expanded here.
- Concurrent work on loop count: Schwethelm et al.'s (2026) iso-depth scaling law gives $\varphi=0.46$ — looping $r$ times is worth only $r^{0.46}$ unique blocks; Loopie's $N\times$ loop vs. $N\times$ layer comparison; Yang et al. (2026, STARS) observe peak-then-collapse with depth and fix it with Jacobian spectral-radius regularization.
- Efficiency line: MELT (cross-loop shared KV with gated updates), Looped Latent Attention (low-rank cross-loop KV compression), LT2 (linear attention + loops). PLT is the representative that also flattens latency.
- The CoT-complements-looping view echoes Xu & Sato's (2025) formal comparison: loops excel at deterministic parallel computation (DAG evaluation), CoT at approximate inference over self-reducible problems.

## 8. Practical takeaways

- Deploying PLT-style parallel loops: $R=2$ is the default — one extra forward buys ~20 points on SWE-style tasks.
- To decide whether one more loop helps, look at the effective-rank curve rather than sweeping training runs.
- "Two loops is enough" is not a universal ceiling for recurrent depth; it is the price of parallelization. If the latency budget allows sequential looping, the Huginn/Ouro line goes much deeper.
- Treat the latent loop as the substrate under CoT, not a replacement: loop first, then add a thinking mode, and the gains compound.

## Appendix: quick numbers

- 7B PLT, 18T tokens, 1:1 text/code, 1M GPU hours; $R\in\{1,2,3,4\}$ each trained from scratch.
- SWE-bench Verified: 43.0 → **64.4** → 27.6 → 22.4; Multi-SWE: 14.0 → **31.0** → 11.0 → 9.3; average 38.0 → **46.5** → 36.9 → 34.3.
- PLT4 effective rank: 174.6 / 172.5 / 158.2 ($r=2/3/4$); $\cos\theta$: −0.72 / −0.46 / 0.04.
- Offset cost $\Omega$ ≈ constant, 30–45× the marginal gain from loop 3 onward.
- Thinking vs. Instruct at $R=2$: LCB +26.9, CRUX +6.6.
