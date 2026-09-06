# Report 03 · Training-Free Looped Transformers: A Loop Wrapper for Frozen Checkpoints

| Item | Detail |
|---|---|
| Paper | Training-Free Looped Transformers |
| arXiv | [2605.23872](https://arxiv.org/abs/2605.23872) (May 2026) |
| Authors | Lizhang Chen\*, Jonathan Li\*, Chen Liang, Ni Lao, Qiang Liu (UT Austin) |
| In this repo | Original `papers/original/2605.23872.pdf` · Chinese `papers/zh/2605.23872.zh.pdf` |

## One sentence

Without touching a single weight or adding a parameter, treat four contiguous mid-stack layers of a released model as the vector field of an ODE and re-integrate it to the *same* endpoint with $K$ damped Euler (Runge–Kutta-style) sub-steps at inference; across seven model families (Qwen3, Llama-3.2, Qwen1.5-MoE, Moonlight, DeepSeek-V2-Lite) and 45 (model, benchmark) cells, 87% are non-negative and knowledge-heavy multiple-choice benchmarks such as MMLU-Pro and GPQA gain about 2 points.

## 1. The problem

Every earlier looped transformer had to be *trained* to loop: the parameters are tied and optimized under the loop structure, so loop and weights are inseparable. Almost every publicly released checkpoint — each the endpoint of continued pretraining, SFT, and several rounds of RLHF/DPO — therefore cannot benefit from looping.

The paper asks: **can a frozen, off-the-shelf checkpoint be looped directly at inference, with no fine-tuning, no continued training, no auxiliary parameters, and no architectural change?**

Three existing results point to yes: Men et al. (2025) delete whole mid-layer blocks with minimal loss; Lad et al. (2024) skip, swap, or repeat mid-layers without catastrophe; Belrose et al.'s (2023) tuned lens shows intermediate logits already encode much of the final prediction. The standard reading is "mid-layers are redundant, so we can remove them". The authors add the other half: **the same redundancy that makes a mid-layer safe to delete makes it safe to re-apply.**

## 2. Method

### 2.1 The wrapper

Let $f=L_{N-1}\circ\cdots\circ L_0$; choose a contiguous window $[a,b]$ and set $g=L_b\circ\cdots\circ L_a$. The wrapped model is

$$\hat f(x)=\underbrace{(L_{N-1}\circ\cdots\circ L_{b+1})}_{\text{post-loop}}\circ\,g^{(K)}\circ\underbrace{(L_{a-1}\circ\cdots\circ L_0)}_{\text{pre-loop}}(x)$$

at an extra cost of $(b-a+1)(K-1)$ layer forwards. $g^{(K)}$ comes in two modes:

- **block-mode**: $(L_b\circ\cdots\circ L_a)^K$ — the whole window repeated $K$ times.
- **layer-mode**: $L_b^K\circ\cdots\circ L_a^K$ — each layer repeated $K$ times before moving on.

For dense models the two are similar. **MoE models require layer-mode**: in block-mode every iteration shows the gating network a slightly perturbed state, routing to different experts, and the accumulated routing noise overwhelms the intended refinement ("routing thrash"). Layer-mode computes the gate once and applies the same expert mixture $K$ times.

### 2.2 The key insight: one layer = one forward-Euler step

A pre-norm layer is $L(x)=x+F(x)$ with $F$ the attention + MLP residual. Define the window residual field $F_g(x):=g(x)-x$; then $g(x)=x+1\cdot F_g(x)$ is exactly one forward-Euler step of size $h=1$ on the autonomous ODE

$$\dot x=F_g(x).$$

The post-loop layers were trained on this approximation of $x(t{=}1)$.

**Why naive looping fails:** applying $x\leftarrow g(x)$ $K$ times is $K$ Euler steps of size 1, landing at $x(t{=}K)$, a point on the trajectory the post-loop layers have never seen. A toy network with a 2-D bottleneck (Figure 2) shows the naive endpoints drifting out of the trained low-loss valley as $K$ grows: MSE goes from 0.015 to 2.88 at $K=2$ and to 335 at $K=8$.

**The right target is not $t=K$ but a finer integration of $[0,1]$.** $K$ Euler steps of size $h=1/K$ give the damped update

$$x_{k+1}=\Big(1-\tfrac1K\Big)x_k+\tfrac1K\,g(x_k),$$

which converges to the true $x(t{=}1)$ at order $O(1/K)$ and strictly improves on the single step the network already implements. On the toy problem, sub-stepping at $K=8$ gives MSE 1.04 versus 335 for naive looping — a ~320× gap.

### 2.3 A particularly effective Runge–Kutta tableau

Generalize damped Euler to $s$-stage explicit RK, $x_1=x_0+h\sum_i b_i k_i$. The authors pick $h=1$, $s=K$, $a_{ij}=\tfrac1K\,\mathbb{I}(j<i)$, and output weights

$$b_1=\beta+\frac{1-\beta}{K},\qquad b_i=\frac{1-\beta}{K}\ (i\ge2),$$

under which the RK output is exactly

$$x_1=\beta\,g(x_0)+(1-\beta)\,F^K(x_0),$$

an **interpolation between the original single-step output and the $K$-step damped-Euler endpoint** (Algorithm 3). $\beta=0$ is pure sub-stepping, $\beta=1$ leaves the model untouched; intermediate $\beta$ biases the trajectory toward the trained one-step endpoint. This anchor weight is the method's safety valve.

Seven iteration strategies are compared (Table 1): naive loop, forward Euler, midpoint/Heun (RK2), RK4, heavy-ball, Anderson acceleration, Aitken $\Delta^2$, and Uniform Loop. **No fixed-point accelerator robustly beats $K$-stage RK**, which the authors read as evidence that the looped middle of a pretrained transformer "is not contractive in any useful sense" — it is a segment of an ODE flow, not a fixed-point iteration.

## 3. Key experiments and numbers

One recipe, **no per-cell tuning**: 3-stage RK on the middle 4 layers, block-mode for dense, layer-mode for MoE; lm-eval-harness 0.4.11, bf16; ~20,000 H100 hours.

### 3.1 Main results (Table 3)

| Model | Benchmark | Base | Looped | Δ pp |
|---|---|---|---|---|
| Qwen3-4B-Instruct | MMLU-Pro 5-shot | 0.5714 | 0.5979 | **+2.64** |
| | GPQA-Main 0-shot | 0.3371 | 0.3571 | **+2.01** |
| | CommonsenseQA 7-shot | 0.7887 | 0.7993 | +1.06 |
| Llama-3.2-3B-Instruct | GPQA-Main | 0.2991 | 0.3103 | +1.12 |
| | MMLU-Pro | 0.3164 | 0.3236 | +0.71 |
| Llama-3.2-1B-Instruct | GPQA-Main | 0.2790 | 0.2969 | +1.79 |
| Qwen1.5-MoE-A2.7B | ARC-Challenge 25-shot | 0.4829 | 0.5060 | **+2.30** |
| | CommonsenseQA | 0.7961 | 0.8133 | +1.72 |
| | OpenBookQA | 0.3160 | 0.3320 | +1.60 |
| Moonlight-16B-A3B | MMLU 0-shot | 0.6786 | 0.6860 | +0.74 |
| | OpenBookQA | 0.3160 | 0.3280 | +1.20 |
| DeepSeek-V2-Lite-Chat | ARC-Challenge | 0.5794 | 0.5879 | +0.85 |

The largest gains (+2.0 to +2.6) are on the hardest knowledge MC tasks (MMLU-Pro, GPQA, ARC-C) with the strongest MHA backbones; MLA+MoE models (DeepSeek-V2-Lite, Moonlight) move the same way at 3–4× smaller magnitude.

### 3.2 Window size: $n=4$ is the sweet spot, $n\ge6$ a cliff (Table 2a)

Qwen3-1.7B-Base, forward Euler $K=2$, 16-task average:

| Window layers $n$ | 1 | 2 | 3 | **4** | 6 | 12 | 28 (all) |
|---|---|---|---|---|---|---|---|
| Δ | +0.18 | +0.06 | +0.21 | **+0.55** | −0.82 | −0.63 | −27.73 |

$n=4$ wins on Qwen3-1.7B/4B and Llama-3.2-3B ($n=3$ slightly better on 0.6B). Looping the whole model loses 27.7 points — a sharp contrast with the "model-loop" paradigm on *trained* looped models. **An untrained model can only be looped in a small mid-stack window.**

### 3.3 The depth-fraction rule (§3.2)

Across eight architectures the optimal window center lies in a narrow band of fractional depth: 0.43–0.71 (mode ≈ 0.50) for models above 1.7B, shifting earlier to 0.25–0.56 below 1B. Hypothesis: head specialization concentrates in late layers, which the loop must avoid; in small and heavily distilled models the "late" fraction is larger, so the safe window starts earlier.

### 3.4 Leakage-free transfer: Qwen3-30B-A3B (Table 4)

Configuration $[22,24]$ fixed in advance from the depth-fraction rule, committed before any cell was scored. 8 of 9 benchmarks improve: CSQA +1.14, MMLU-flex +0.79, SuperGPQA +0.70, TruthfulQA +0.49; LAMBADA perplexity 4.12 → 4.11. All positive but small — the rule transfers, and gains on a large MoE are modest.

### 3.5 The full picture (§3.5)

45 cells: 27 positive (Δ > +0.3, 60%), 12 neutral (27%), 6 negative. Negatives concentrate in **sub-3B distilled checkpoints on knowledge MC** (e.g. Llama-3.2-1B on MMLU). Even there, GPQA flips positive on Llama-3.2-1B (+1.79) with a very early window $[4,7]$ — the failure boundary is task-dependent, not absolute.

### 3.6 Against other looping methods (§3.7, Figures 4–5)

- Naive looping à la Giannou et al. (2023) collapses on **every** cell; at $K=6$ the 16-task mean falls to 37.89% (−17.71 pp).
- Uniform Loop (Lys et al. 2026) fails for $K\ge6$.
- This method stays stable for $K\in\{1,\dots,24\}$.

## 4. Why it matters

1. **It lowers the barrier.** Looping used to mean "train from scratch, big-lab only"; now anyone gets 1–2.5 points on an existing open model for free.
2. **It supplies a testable theory.** "Layer = Euler step" is not new (Neural ODE, DEQ), but turning it into an inference-time prescription — keep the endpoint, refine the step, anchor with $\beta$ — is. The same view explains why naive looping fails, why MoE needs layer-mode, and why fixed-point accelerators do not help.
3. **Layer-mode for MoE** agrees with Loopie's (2607.16051) independently derived "layer-loop scales better on MoE"; one paper trains nothing, the other trains from scratch, and both land on the same conclusion.

## 5. Limitations

- Gains cap at ~2–3 points, an order of magnitude below from-scratch looped models (Huginn: +20 on ARC-E). This squeezes existing weights; it is not a new scaling axis.
- Gains concentrate on knowledge MC; the paper reports no systematic improvement on generative tasks (GSM8K, code).
- Extra inference cost of about $4\times(K-1)$ layer forwards ($K=3$ ≈ 8 extra layers), i.e. 15–30% latency on 28–48-layer models.
- Small distilled models lose points and need family-specific window placement; "no tuning" is per-cell — the recipe itself was found on these models.

## 6. Relation to other work

- Theory: DEQ (Bai et al. 2019, 2020) treats weight-tied nets as fixed-point solvers; this paper argues the pretrained mid-stack behaves as an ODE flow, not a contraction.
- Training-free depth manipulation cousins: layer skipping (Men 2025, Lad 2024); Program-of-Layers (Li et al. 2026, ICML) learns a small network that decides per input which layers to skip or repeat — a learnable version of this idea.
- Retrofit-with-training: Relaxed Recursive Transformers (Bae 2025, per-layer LoRA), Retrofitted Recurrence (McLeish 2025, curriculum continued training) — they train and gain more, forming a zero-cost / low-cost / from-scratch spectrum with this paper.

## 7. Practical takeaways

- To try looping on an existing model: middle 4 layers, 3-stage RK, intermediate $\beta$, block-mode for dense, layer-mode for MoE. Validate on knowledge MC first; the signal is clearest there.
- Never repeat layers naively. Any "run this block twice" experiment should use the damped update $x\leftarrow(1-1/K)x+(1/K)g(x)$ instead of $x\leftarrow g(x)$.
- On MoE, freeze routing before repeating anything.
- Most valuable when a model is already strong and stuck on the last few points; for small models or generative reasoning, look at from-scratch approaches.

## Appendix: quick numbers

- Recipe: middle 4 layers, $K=3$ RK, dense block / MoE layer.
- 45 cells: 60% positive, 27% neutral, 87% non-negative; ~20k H100 hours.
- Qwen3-4B-Instruct MMLU-Pro +2.64, GPQA +2.01; Qwen1.5-MoE ARC-C +2.30.
- Window $n=4$ +0.55, $n=6$ −0.82, whole model −27.73; naive loop $K=6$ −17.71.
- Optimal window fractional depth: 0.43–0.71 (>1.7B), 0.25–0.56 (<1B).
