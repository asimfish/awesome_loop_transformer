# Awesome Loop Transformer

Looped transformers, recurrent depth, and latent reasoning.

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re) [![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-596d75)](LICENSE) ![Entries](https://img.shields.io/badge/entries-333-17675d)

[Browse online](https://asimfish.github.io/awesome_loop_transformer/) · [Start reading](#start-reading) · [Browse by topic](#topics) · [Core readings](#core-readings) · [Contribute](CONTRIBUTING.md)

![A shared transformer block repeatedly updates a hidden state.](assets/overview.svg)

## Start reading

Explore looped transformers, recurrent depth, and latent reasoning. A curated path from foundational ideas to training, inference, and applications.

| Your goal | Start here |
| --- | --- |
| Understand the field | [English reading guide](guide.md) |
| Follow a short route | [Core readings](#core-readings) |
| Find a specific method | [Topic index](#topics) or the searchable [paper browser](https://asimfish.github.io/awesome_loop_transformer/#library) |
| Reuse the collection | [Machine-readable catalog](data/papers.csv) |

Open <code>index.html</code> in a browser for search, topic and year filters, sorting, saved readings, and links to papers and code. It works offline; external resources still need a connection. Filter links can be shared when the page is served over HTTP.

Browse the [open model directory](models.md) for released checkpoints and model families.

## Topics

Choose a subject first; use the core reading route for an introduction.

| Topic | Entries | Scope |
| --- | ---: | --- |
| [Foundations & theory](#foundations-theory) | 53 | Early architectures, expressivity, and generalization. |
| [Architectures & pretraining](#architectures-pretraining) | 99 | Recurrent depth at scale and compact recursive models. |
| [Training & adaptation](#training-adaptation) | 69 | Stable optimization, retrofitting, and reinforcement learning. |
| [Inference & efficiency](#inference-efficiency) | 82 | Adaptive halting, latency, memory, and quantization. |
| [Analysis & applications](#analysis-applications) | 106 | Latent dynamics and applications beyond text. |
| [Surveys & related reasoning](#surveys-related-reasoning) | 22 | Overviews and adjacent approaches to latent reasoning. |

Papers may appear in more than one topic; the catalog contains **333 unique entries**. Original fine-grained categories remain searchable in the browser.

## Core readings

1. **Universal Transformers.** [Paper](https://arxiv.org/abs/1807.03819) · [Code](https://github.com/tensorflow/tensor2tensor) · [Notes](reports/en/01_universal_transformers.md) · [PDF](papers/original/1807.03819.pdf)

   A shared transformer block with optional adaptive computation time.

2. **Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach.** [Paper](https://arxiv.org/abs/2502.05171) · [Code](https://github.com/seal-rg/recurrent-pretraining) · [Notes](reports/en/02_recurrent_depth_huginn.md) · [PDF](papers/original/2502.05171.pdf)

   Recurrent-depth pretraining with a variable amount of latent computation at inference.

3. **Training-Free Looped Transformers.** [Paper](https://arxiv.org/abs/2605.23872) · [Notes](reports/en/03_training_free_looped.md) · [PDF](papers/original/2605.23872.pdf)

   A training-free route to repeated computation in a pretrained transformer.

4. **LoopCoder-v2: Only Loop Once for Efficient Test-Time Computation Scaling.** [Paper](https://arxiv.org/abs/2606.18023) · [Model](https://huggingface.co/Multilingual-Multimodal-NLP/LoopCoder-V2) · [Notes](reports/en/04_loopcoder_v2.md) · [PDF](papers/original/2606.18023.pdf)

   Parallel looping for coding models, with explicit compute and latency trade-offs.

5. **Loop the Loopies!.** [Paper](https://arxiv.org/abs/2607.16051) · [Notes](reports/en/05_loop_the_loopies.md) · [PDF](papers/original/2607.16051.pdf)

   Studies loop granularity and mixture-of-experts models under matched training budgets.

## Catalog

Expand a topic to see its references. Listed years follow the source catalog and may reflect a publication venue rather than the first preprint date.

<a id="foundations-theory"></a>

### Foundations & theory

Early architectures, expressivity, and generalization.

<details>
<summary>View 53 entries</summary>

- **Beyond the Training Horizon: Mechanisms and Limits of Length Generalization in Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.33144)

- **Chain-of-Thought and Compressed Looped Transformers: A Memory-Budget Separation.** arXiv, 2026. [Paper](https://arxiv.org/abs/2605.30757)

- **DiscoLoop: Looping Discrete Embeddings and Continuous Hidden States for Multi-hop Reasoning.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.00341)

- **Dynamical phase selection controls compute scaling in looped transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.26556)

- **How Depth Growth and Looping Shape In-Context Learning in Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.31421)

- **How Much Is One Recurrence Worth? Iso-Depth Scaling Laws for Looped Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2604.21106)

- **Inside the Loop: A Mechanistic Study of Weight-Tied Transformers on Depth-Bound Algorithmic Tasks.** NeurIPS, 2026. [Paper](https://arxiv.org/abs/2610.24135) · [Code](https://github.com/magnus-sesodia/insidetheloop)

- **Internalizing Chain-of-thought into Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.25998)

- **Learning to Compute Is Not Learning to Retain or Reuse in Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.19768)

- **Learning to Extrapolate in Depth with Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.14456)

- **Length Generalization with Log-Depth Recurrent Units.** arXiv, 2026. [Paper](https://arxiv.org/abs/2605.26035)

- **Loop, Think, & Generalize: Implicit Reasoning in Recurrent-Depth Transformers.** COLM, 2026. [Paper](https://arxiv.org/abs/2604.07822)

- **Looped GNNs Beyond Fixed Depth: Graph Size Generalization and Parameter-Efficient Adaptation.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.24112)

- **Looped Transformers with Layer Normalization Provably Learn the Power Method.** arXiv, 2026. [Paper](https://arxiv.org/abs/2606.00605)

- **PAR: Progress-Aligned Recurrence for Length Generalization in State Tracking.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.27628)

- **Recurrent Looped Transformer.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.07591) · [Code](https://github.com/yifanzhang-pro/recurrent-looped-tranformer)

- **Repeated Shared Access Enables Grokking, but Edit Propagation Depends on an Addressable Memory.** arXiv, 2026. [Paper](https://arxiv.org/abs/2606.20737)

- **Rotate the Loop: Blockwise Conformality for Looped Transformers.** NeurIPS Workshop, 2026. [Paper](https://arxiv.org/abs/2610.14030)

- **SpiralFormer: Looped Transformers Can Learn Hierarchical Dependencies via Multi-Resolution Recursion.** arXiv, 2026. [Paper](https://arxiv.org/abs/2602.11698)

- **Stability and Generalization in Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2604.15259)

- **Statistical Gains from Looped Estimation under Parameter Budgets.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.25778)

- **Storing Is Not Remembering: LSTM-UT and Bounded Gated Memory for Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.19521)

- **Test-Time Forecasting: Recurrent Depth Enables In-Context Dynamics Prediction.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.19552)

- **Thinking Deeper, Not Longer: Depth-Recurrent Transformers for Compositional Generalization.** arXiv, 2026. [Paper](https://arxiv.org/abs/2603.21676)

- **Universal Transformers for Circuit Computations: Perfect Length Generalization in Tiny Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.31067)

- **Universal Transformers Need Memory: Depth-State Trade-offs in Adaptive Recursive Reasoning.** arXiv, 2026. [Paper](https://arxiv.org/abs/2604.21999)

- **When Does Recurrence Become an Algorithm? Convergence Selection in Weight-Tied Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.20594)

- **Bypassing the Exponential Dependency: Looped Transformers Efficiently Learn In-context by Multi-step Gradient Descent.** AISTATS, 2025. [Paper](https://arxiv.org/abs/2410.11268)

- **CoTFormer: A Chain-of-Thought Driven Architecture with Budget-Adaptive Computation Cost at Inference.** ICLR, 2025. [Paper](https://arxiv.org/abs/2310.10845)

- **Looped Transformers for Length Generalization.** ICLR, 2025. [Paper](https://arxiv.org/abs/2409.15647)

- **Reasoning with Latent Thoughts: On the Power of Looped Transformers.** ICLR, 2025. [Paper](https://arxiv.org/abs/2502.17416)

- **Relaxed Recursive Transformers: Effective Parameter Sharing with Layer-wise LoRA.** ICLR, 2025. [Paper](https://arxiv.org/abs/2410.20672)

- **To CoT or To Loop? A Formal Comparison Between Chain-of-Thought and Looped Transformers.** arXiv, 2025. [Paper](https://arxiv.org/abs/2505.19245)

- **What Makes Looped Transformers Perform Better Than Non-Recursive Ones.** arXiv, 2025. [Paper](https://arxiv.org/abs/2510.10089)

- **Can Looped Transformers Learn to Implement Multi-step Gradient Descent for In-context Learning?.** ICML, 2024. [Paper](https://arxiv.org/abs/2410.08292)

- **Looped ReLU MLPs May Be All You Need as Practical Programmable Computers.** arXiv, 2024. [Paper](https://arxiv.org/abs/2410.09375)

- **Looped Transformers are Better at Learning Learning Algorithms.** ICLR, 2024. [Paper](https://arxiv.org/abs/2311.12424)

- **MoEUT: Mixture-of-Experts Universal Transformers.** NeurIPS, 2024. [Paper](https://arxiv.org/abs/2405.16039)

- **On Expressive Power of Looped Transformers: Theoretical Analysis and Enhancement via Timestep Encoding.** arXiv, 2024. [Paper](https://arxiv.org/abs/2410.01405)

- **On the Role of Depth and Looping for In-Context Learning with Task Diversity.** arXiv, 2024. [Paper](https://arxiv.org/abs/2410.21698)

- **Simulation of Graph Algorithms with Looped Transformers.** ICML, 2024. [Paper](https://arxiv.org/abs/2402.01107)

- **Lessons on Parameter Sharing across Layers in Transformers.** arXiv, 2023. [Paper](https://arxiv.org/abs/2104.06022)

- **Looped Transformers as Programmable Computers.** ICML, 2023. [Paper](https://arxiv.org/abs/2301.13196)

- **Sparse Universal Transformer.** EMNLP, 2023. [Paper](https://arxiv.org/abs/2310.07096)

- **End-to-end Algorithm Synthesis with Recurrent Networks: Logical Extrapolation Without Overthinking.** NeurIPS, 2022. [Paper](https://arxiv.org/abs/2202.05826)

- **Path Independent Equilibrium Models Can Better Exploit Test-Time Computation.** NeurIPS, 2022. [Paper](https://arxiv.org/abs/2211.09961)

- **Can You Learn an Algorithm? Generalizing from Easy to Hard Problems with Recurrent Networks.** NeurIPS, 2021. [Paper](https://arxiv.org/abs/2106.04537)

- **PonderNet: Learning to Ponder.** ICML Workshop, 2021. [Paper](https://arxiv.org/abs/2107.05407)

- **ALBERT: A Lite BERT for Self-supervised Learning of Language Representations.** ICLR, 2020. [Paper](https://arxiv.org/abs/1909.11942)

- **Deep Equilibrium Models.** NeurIPS, 2019. [Paper](https://arxiv.org/abs/1909.01377)

- **Universal Transformers.** ICLR, 2019. [Paper](https://arxiv.org/abs/1807.03819) · [Code](https://github.com/tensorflow/tensor2tensor) · [Notes](reports/en/01_universal_transformers.md) · [PDF](papers/original/1807.03819.pdf)

  A shared transformer block with optional adaptive computation time.

- **Adaptive Computation Time for Recurrent Neural Networks.** arXiv, 2016. [Paper](https://arxiv.org/abs/1603.08983)

- **Neural GPUs Learn Algorithms.** ICLR, 2016. [Paper](https://arxiv.org/abs/1511.08228)

</details>

[Back to topics](#topics)

<a id="architectures-pretraining"></a>

### Architectures & pretraining

Recurrent depth at scale and compact recursive models.

<details>
<summary>View 99 entries</summary>

- **A Dual-Path Architecture for Scaling Compute and Capacity in LLMs.** arXiv, 2026. [Paper](https://arxiv.org/abs/2605.30202)

- **Accordion: Elastic-Depth Inference via Fixed-Prefix Layer Looping.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.32492)

- **Adaptive Loops and Memory in Transformers: Think Harder or Know More?.** ICLR Workshop, 2026. [Paper](https://arxiv.org/abs/2603.08391)

- **Adaptive-Depth Is a Finishing Stage.** NeurIPS Workshop, 2026. [Paper](https://arxiv.org/abs/2610.14252)

- **Allocating Recurrent Compute in Looped Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.18230)

- **Are Your Reasoning Models Reasoning or Guessing? A Mechanistic Analysis of Hierarchical Reasoning Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2601.10679)

- **ARLoop: Fully-Open Pre-trained Looped Transformers with Attention Residuals.** arXiv, 2026. [Paper](https://arxiv.org/abs/2611.05234)

- **Asymmetric Looped Transformers: Fixed Global Representations for an Iterative Decoder.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.28489)

- **BDH-CQ: In-Context Learning with Recurrent Latent Reasoning.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.09888) · [Code](https://github.com/pathwaycom/arc-task-gen)

- **Best-of-Depth: Learning Exploratory Dynamics in Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2611.04663)

- **Block Recursive Transformers for Structured Parameter Sharing.** EMNLP Findings, 2026. [Paper](https://arxiv.org/abs/2610.24998) · [Code](https://aim-skku.github.io/BRT/)

- **Causal Latent Workspaces for Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.22796) · [Code](https://github.com/izaznov/causal-latent-workspace-transformer)

- **Closing the Loop: Practical Training Recipes for Looped Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.00673)

- **Compute Time Scaling with Recursive Models for Combinatorial Optimization.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.34585)

- **DART: Distributional Adversarial Recurrent Training for Algorithm Learning.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.05988)

- **Depth-Recurrent Attention Mixtures: Giving Latent Reasoning the Attention it Deserves.** arXiv, 2026. [Paper](https://arxiv.org/abs/2601.21582)

- **Diffusion as a Training Curriculum for Timestep-Free Iterative Reasoning.** NeurIPS Workshop, 2026. [Paper](https://arxiv.org/abs/2609.01449)

- **Dissecting Hierarchical Reasoning Models: A Mechanistic Study.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.22197)

- **Dory1.0-4B: A Looped Normalized-GPT.** arXiv, 2026. [Paper](https://arxiv.org/abs/2611.03998)

- **Dual-Slot: From Serial Loops to Parallel Slots in Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.25086)

- **Dynamical Systems Theory Behind a Hierarchical Reasoning Model.** arXiv, 2026. [Paper](https://arxiv.org/abs/2603.22871)

- **Energy-guided Recursive Model.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.10128)

- **Evaluating Tiny Recursive Models Across Training for Code Generation.** CASCON, 2026. [Paper](https://arxiv.org/abs/2608.29376)

- **Fixed-Point Reasoners: Stable and Adaptive Deep Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2606.18206) · [Code](https://github.com/nilskiKonjIzDunava/fprm)

- **Flow Reasoning Models: Turning Flows Into Efficient Recurrent Reasoners.** arXiv, 2026. [Paper](https://arxiv.org/abs/2606.29150)

- **G-RRM: Guiding Symbolic Solvers with Recurrent Reasoning Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.02491)

- **Gated Recurrent Transformers: Expressive Depth through Recurrent Modulation.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.15062)

- **Hidden Decoding at Scale: Latent Computation Scaling for Large Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.08186)

  contrast: sequence-length scaling

- **How Model Growth, Recursion, and Boundary Operators Influence Scaling Exponents.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.19107) · [Code](https://github.com/qlabs-eng/scaling-exponents)

- **How Much Is One Recurrence Worth? Iso-Depth Scaling Laws for Looped Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2604.21106)

- **How to Loop MoE: Flatten the Experts, Untie the Attention.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.35751) · [Code](https://github.com/SR-A-W/how-to-loop-moe)

- **How to Loop Your Transformer: Loop Scaling, Specialization, and Parallel Inference.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.40325)

- **Hyperloop Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2604.21254)

- **Input-Conditioned Search for Efficient Test-Time Scaling of Recursive Reasoners.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.18547)

- **Invariant-Measure Reasoners: Stable Representations for Latent Reasoning.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.10996)

- **Knowledge transfer between simple discrete worlds.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.15081)

- **Latent Recurrent Thoughts: Recurrent Refinement of Proposed Latents for Reasoning with Frozen LLMs.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.01117)

- **Latent Recurrent Transformer: Architecture Exploration, Training Strategies, and Scaling Behavior.** arXiv, 2026. [Paper](https://arxiv.org/abs/2605.26797)

- **LatentLoop: Scaling Looped MoE Models with Asymmetric Compute Allocation.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.19975)

- **Look, Reason, Draw a Region: Recursive Refinement for Spatial Context Prediction.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.23302)

- **Loop Before You Leap: What Recurrent Depth Can and Cannot Buy in Data-Limited Pretraining.** BabyLM, 2026. [Paper](https://arxiv.org/abs/2611.06206)

- **Loop the Loopies!.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.16051) · [Notes](reports/en/05_loop_the_loopies.md) · [PDF](papers/original/2607.16051.pdf)

  Studies loop granularity and mixture-of-experts models under matched training budgets.

- **Loopback Transformer: Towards a Unified View of Residual Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2611.07226) · [Code](https://github.com/yancyou/Loopback)

- **LoopCoder-v2: Only Loop Once for Efficient Test-Time Computation Scaling.** arXiv, 2026. [Paper](https://arxiv.org/abs/2606.18023) · [Model](https://huggingface.co/Multilingual-Multimodal-NLP/LoopCoder-V2) · [Notes](reports/en/04_loopcoder_v2.md) · [PDF](papers/original/2606.18023.pdf)

  Parallel looping for coding models, with explicit compute and latency trade-offs.

- **Looped GPT-BERT: Trading Parameters for Computation in Small Language Modeling.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.09691)

- **Looped Reasoning Finishes Earlier Than You Think.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.18174)

- **Looping Beyond Twice: A Scalable Recipe for Looped Mixture-of-Experts.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.01153) · [Code](https://github.com/hed-ucas/LOOM)

- **LoopMoE: Unifying Iterative Computation with Mixture-of-Experts for Language Modeling.** arXiv, 2026. [Paper](https://arxiv.org/abs/2606.04438)

- **LoopVL: Recurrent Visual Intelligence.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.38426)

- **Mimir: A Sub-2B Hierarchical Reasoning Model Trained on Permissible Data Punches Above Its Weight Class.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.13517)

- **Mobius Learning: Cyclic Depth Folding in Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.17843)

- **Nanbeige4.2-3B: Unlocking Agentic Capabilities in a Compact Model.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.22083)

- **Nested Shared-Operator Recursion on ARC-AGI-1: An Empirical Study of HRM, TRM and URM.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.26666)

- **One Model to Loop Them All: Elastic Latent Recurrence for Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.12582)

- **One Step Forward and K Steps Back: Better Reasoning with Denoising Recursion Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2604.18839)

- **Pretraining and Test-Time Training Budgets Matter for ARC: A Controlled Study of VARC and TRM.** BNAIC/BeNeLearn, 2026. [Paper](https://arxiv.org/abs/2610.13660)

- **Quantizing Recursive Reasoning Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.16237)

- **Random Recursive Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.00541)

- **Reasoning on the Simplex: Geometric Fixed-Point Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.33540)

- **Recursive Vision Language Models for General Symbolic Reasoning.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.01534)

- **RELAGRAM: Recursive Latent Graph Model for the Capacitated Vehicle Routing Problem.** NeurIPS Workshop, 2026. [Paper](https://arxiv.org/abs/2610.15106)

- **Resample the Answer: Where to Spend Test-Time Compute in Recursive Reasoning.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.16427) · [Code](https://github.com/MaximeILL/GAR)

- **Scaling Laws for Looped Mixture of Experts.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.40316)

- **Scaling to Tens of Thousands of Test-Time Iterations with Loop-Native Attention Residuals.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.11570) · [Code](https://github.com/pixeli99/InfiLoop)

- **Scheduling Recursive Reasoning in Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.36653)

- **Slots, Transitions, Loops: Learning Composable World Models for ARC.** arXiv, 2026. [Paper](https://arxiv.org/abs/2606.12316)

- **SMELT: Scaling Laws for Compute-Matched MoE Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.01343)

- **Solve the Loop: Attractor Models for Language and Reasoning.** arXiv, 2026. [Paper](https://arxiv.org/abs/2605.12466)

- **Spherical Fixed-Point Reasoners: Adaptive Loop Halting on the Hypersphere.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.25646)

- **Squeezing More from Limited Data with Recursive Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.26973)

- **StateLoop: Persistent State for Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.35544)

- **Steering Recurrent Reasoners at Inference Time with Readout Feedback.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.24136)

- **Stream Recursion Model (SRM).** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.28809)

- **Structured Sparse Memory for Recurrent Reasoning.** NeurIPS, 2026. [Paper](https://arxiv.org/abs/2609.33270) · [Code](https://github.com/water-vapor/charm)

- **The Surprising Effectiveness of Shared Memory in Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.02383)

- **Think Before You Paint: Recursive Latent Reasoning for Diffusion Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.09876)

- **Think Deep, Speak Once: Relit, A Recursive Latent Implicit Transformer Framework.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.08113)

- **Think Twice: The Metis-1.6 Technical Report.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.37903) · [Model](https://huggingface.co/Lernex)

- **Thinking with Looped Flows.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.11801)

- **Tiny Recursive Message Passing.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.18649)

- **Tiny Recursive Policy: Recursive Latent Refinement for Visuomotor Control.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.33288)

- **Towards Looped Models Done Right, Part I: Topology, Input Injection, Recurrent-State Design.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.23036) · [Code](https://github.com/ifm-ai/xllm-loop)

- **TraceViT: Grounded Trace Supervision for Visual Abstract Reasoning.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.29586) · [Code](https://github.com/LiuBinnan/TraceViT)

- **Trading Depth for Time in Recurrent Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.21605)

- **Truncate or Not? A Scaling Study of Looped Transformers with Truncated Backpropagation.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.26030)

- **Tying the Loop -- Tied Expert Layers in Mixture-of-Experts Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2606.16825) · [Code](https://github.com/epfml/looped-moe)

- **UpLoop: Training Looped Transformers via Upcycling at No Extra Pretraining Compute.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.41720)

- **What Limits Recursive Reasoning Models: Optimization, Architecture and Test-Time Scaling.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.39967)

- **What Makes Recurrence Effective in Looped Language Models?.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.36636)

- **What Survives When You Compress a Recursive Reasoner for the Edge?.** arXiv, 2026. [Paper](https://arxiv.org/abs/2606.26488)

- **When Recursive Models Finish Computing.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.26487)

- **Hierarchical Reasoning Model.** arXiv, 2025. [Paper](https://arxiv.org/abs/2506.21734)

- **Hierarchical Reasoning Models: Perspectives and Misconceptions.** arXiv, 2025. [Paper](https://arxiv.org/abs/2510.00355)

- **Latent Reasoning in TRMs is Secretly a Policy Improvement Operator.** arXiv, 2025. [Paper](https://arxiv.org/abs/2511.16886)

- **Less is More: Recursive Reasoning with Tiny Networks.** arXiv, 2025. [Paper](https://arxiv.org/abs/2510.04871)

- **Parallel Loop Transformer for Efficient Test-Time Computation Scaling.** arXiv, 2025. [Paper](https://arxiv.org/abs/2510.24824)

- **Scaling Latent Reasoning via Looped Language Models.** arXiv, 2025. [Paper](https://arxiv.org/abs/2510.25741) · [Code](http://ouro-llm.github.io)

- **Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach.** arXiv, 2025. [Paper](https://arxiv.org/abs/2502.05171) · [Code](https://github.com/seal-rg/recurrent-pretraining) · [Notes](reports/en/02_recurrent_depth_huginn.md) · [PDF](papers/original/2502.05171.pdf)

  Recurrent-depth pretraining with a variable amount of latent computation at inference.

- **MoEUT: Mixture-of-Experts Universal Transformers.** NeurIPS, 2024. [Paper](https://arxiv.org/abs/2405.16039)

</details>

[Back to topics](#topics)

<a id="training-adaptation"></a>

### Training & adaptation

Stable optimization, retrofitting, and reinforcement learning.

<details>
<summary>View 69 entries</summary>

- **A Tilted Bowl Is Not a Slippery Slope: Compressing Looped Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.39277)

- **Agreement rather than normalisation keeps depth reusable in looped language models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.31943)

- **Best-of-Depth: Learning Exploratory Dynamics in Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2611.04663)

- **Bridging the Gap Between Latent and Explicit Reasoning with Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2606.31779) · [Code](https://github.com/yingfan-bot/lotus)

- **Closing the Loop: Practical Training Recipes for Looped Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.00673)

- **DART: Distributional Adversarial Recurrent Training for Algorithm Learning.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.05988)

- **Decoding Looped Transformers Better for (Almost) Free.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.02185)

- **Deeper Backpropagation or More Updates? Training Looped Language Models Across Budgets.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.38422)

- **DeepLoop: Depth Scaling for Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.13491)

- **Demystifying Hidden-State Recurrence: Switchable Latent Reasoning with On-Policy Reinforcement Learning.** arXiv, 2026. [Paper](https://arxiv.org/abs/2606.13106)

- **Dense Supervision Is Not Enough: The Readout Blind Spot in Looped Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2606.24898)

- **Dynamic System Inspired Continuous Large Language Model for AI4Science Tasks.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.26959)

- **Extending Reasoning in Typed Decision Models via Looping.** arXiv, 2026. [Paper](https://arxiv.org/abs/2611.07736)

- **Fixed-Point Reasoners: Stable and Adaptive Deep Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2606.18206) · [Code](https://github.com/nilskiKonjIzDunava/fprm)

- **FlashLoop: Fast and Memory-Efficient Looped Transformers via Lazy Updates.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.29812)

- **From Chain-of-Thought to Loops: Non-Autoregressive Latent Reasoning via Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.11472)

- **How Much Gradient Does Truncated Backprop Lose in Looped Transformers?.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.28871) · [Code](https://github.com/Aur-Shalev-Merin/lost-gradient-looped-transformers)

- **Improving Test-Time Scaling with Adaptive Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.35748) · [Code](https://github.com/thu-nics/TaH)

- **Invariant-Measure Reasoners: Stable Representations for Latent Reasoning.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.10996)

- **LayerNorm as Implicit Gain Control in Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.10681)

- **Loop Dropout: Regularizing Shared Updates in Looped Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.34218) · [Code](https://github.com/NUS-HPC-AI-Lab/loop-dropout)

- **LoopCD: Loop-wise Contrastive Decoding for Improving Reasoning in Looped Language Models.** EMNLP, 2026. [Paper](https://arxiv.org/abs/2609.24196)

- **Looped Reasoning Finishes Earlier Than You Think.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.18174)

- **Looped Transformers as Optimizers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.37379)

- **Looped Transformers with Source-Centered State Evolution.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.27656)

- **Looping Beyond Twice: A Scalable Recipe for Looped Mixture-of-Experts.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.01153) · [Code](https://github.com/hed-ucas/LOOM)

- **LoopMTP: A looped transformer guided by latent multi-token prediction.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.03624)

- **LoopRPT: Reinforcement Pre-Training for Looped Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2603.19714)

- **LoOPSD: On-Policy Self-Distillation with Looped Teachers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.18162)

- **MACRO: Markov Chain Routing of Transformer Layers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.05872) · [Code](https://github.com/Batorskq/MACRO)

- **On the Residual Scaling of Looped Transformers: Stability and Transferability.** arXiv, 2026. [Paper](https://arxiv.org/abs/2606.18524)

- **One Model, Two Paths: Balancing Single-Pass and Looped Performance in Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.33517)

- **Ouroboros: Dynamic Weight Generation for Recursive Transformers via Input-Conditioned LoRA Modulation.** arXiv, 2026. [Paper](https://arxiv.org/abs/2604.02051)

- **Penelope: Localized Latent Recurrence for Efficient Structured Reasoning.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.25915)

- **Prioritize the Process, Not Just the Outcome: Rewarding Latent Thought Trajectories Improves Reasoning in Looped Language Models.** ICML, 2026. [Paper](https://arxiv.org/abs/2602.10520) · [Code](https://github.com/jonwill8/RLTT)

- **Reasoning on the Simplex: Geometric Fixed-Point Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.33540)

- **Recurrent Self-Improvement: Dynamic Cross-Loop On-Policy Distillation for Looped Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.10623)

- **Retrofitting Recurrent Depth into a Pretrained Language Model: Installation, Extrapolation, Transfer, and Retention at Two Parameter Budgets.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.11233)

- **Retrofitting Recurrent Vision-Language Models from Pretrained Backbones.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.22075) · [Code](https://madhavesdios.github.io/recurrent-vlms)

- **Right Direction, Wrong Step: Geometric Analysis of Finite-Step Failure in Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.16665)

- **Rotate the Loop: Blockwise Conformality for Looped Transformers.** NeurIPS Workshop, 2026. [Paper](https://arxiv.org/abs/2610.14030)

- **Running Fewer Loops Removes Refusal Behaviour in Recurrent-Depth Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.15218)

- **Safe at One Loop, Risky at Another: Aligning Safety Across Recurrent Depths in Looped Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.10625)

- **SanSi: A Looped Typed Decision Model for System 1.5 Thinking.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.07730) · [Code](https://minnesotanlp.github.io/Sansi/)

- **ScaleRLT: Exact Log-Probabilities and Fast Deferred Rollouts for Reinforcement Learning on Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.34427)

- **Scaling to Tens of Thousands of Test-Time Iterations with Loop-Native Attention Residuals.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.11570) · [Code](https://github.com/pixeli99/InfiLoop)

- **Scheduling Recursive Reasoning in Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.36653)

- **SCORE: Replacing Layer Stacking with Contractive Recurrent Depth.** arXiv, 2026. [Paper](https://arxiv.org/abs/2603.10544)

- **Simply Stabilizing the Loop via Fully Looped Transformer.** arXiv, 2026. [Paper](https://arxiv.org/abs/2605.18797)

- **Skip a Layer or Loop It? Learning Program-of-Layers in LLMs.** ICML, 2026. [Paper](https://arxiv.org/abs/2606.06574)

- **SLPO: Scaling Latent Reasoning via a Surrogate Policy.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.19691)

- **Solve the Loop: Attractor Models for Language and Reasoning.** arXiv, 2026. [Paper](https://arxiv.org/abs/2605.12466)

- **Stabilizing Extrapolation in Looped Transformers via Learned Stochastic Stopping.** arXiv, 2026. [Paper](https://arxiv.org/abs/2606.29983)

- **Stabilizing Recurrent Dynamics for Test-Time Scalable Latent Reasoning in Looped Language Models.** ICML, 2026. [Paper](https://arxiv.org/abs/2605.26733)

- **Storing Is Not Remembering: LSTM-UT and Bounded Gated Memory for Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.19521)

- **T^2MLR: Transformer with Temporal Middle-Layer Recurrence.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.15178)

- **There Is No Free Loop: When Does Looping a Trained Model Pay for Its Inference Compute?.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.42030)

- **Think Deep, Speak Once: Relit, A Recursive Latent Implicit Transformer Framework.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.08113)

- **Think Shallow, Solve Deep: Controlling Recurrent Dynamics for Reliable Test-Time Depth.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.18222)

- **Towards Looped Models Done Right, Part II: Rethinking at Fixed Points.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.06833) · [Code](https://github.com/ifm-ai/xllm-loop)

- **Training-Free Hidden-State Refinement for Flow-Matching Image Generators.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.29160)

- **Training-Free Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2605.23872) · [Notes](reports/en/03_training_free_looped.md) · [PDF](papers/original/2605.23872.pdf)

  A training-free route to repeated computation in a pretrained transformer.

- **Truncate or Not? A Scaling Study of Looped Transformers with Truncated Backpropagation.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.26030)

- **UpLoop: Upcycling Large Language Models with Gated Loop.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.25004)

- **What Limits Recursive Reasoning Models: Optimization, Architecture and Test-Time Scaling.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.39967)

- **Enhancing Auto-regressive Chain-of-Thought through Loop-Aligned Reasoning.** arXiv, 2025. [Paper](https://arxiv.org/abs/2502.08482)

- **Improving Recursive Transformers with Mixture of LoRAs.** arXiv, 2025. [Paper](https://arxiv.org/abs/2512.12880)

- **Relaxed Recursive Transformers: Effective Parameter Sharing with Layer-wise LoRA.** ICLR, 2025. [Paper](https://arxiv.org/abs/2410.20672)

- **Teaching Pretrained Language Models to Think Deeper with Retrofitted Recurrence.** arXiv, 2025. [Paper](https://arxiv.org/abs/2511.07384) · [Code](https://github.com/mcleish7/retrofitting-recurrence)

</details>

[Back to topics](#topics)

<a id="inference-efficiency"></a>

### Inference & efficiency

Adaptive halting, latency, memory, and quantization.

<details>
<summary>View 82 entries</summary>

- **A Tilted Bowl Is Not a Slippery Slope: Compressing Looped Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.39277)

- **Accordion: Elastic-Depth Inference via Fixed-Prefix Layer Looping.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.32492)

- **AdaLoop: Adaptive-Depth Latent Reasoning for Audio Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.06949)

- **Adaptive Depth in Looped Transformers: Diagnosing Learned Halting Gates and Trajectory Readouts.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.20519)

- **Adaptive Loops and Memory in Transformers: Think Harder or Know More?.** ICLR Workshop, 2026. [Paper](https://arxiv.org/abs/2603.08391)

- **Adaptive-Depth Is a Finishing Stage.** NeurIPS Workshop, 2026. [Paper](https://arxiv.org/abs/2610.14252)

- **ALoDLM: Adaptively Looped Diffusion Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.04198)

- **Attention Routing Stabilizes Early: Working-Set Inference for Recurrent Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.27373) · [Code](https://github.com/tbn5pj/WISE_code)

- **BeNice! Closing Looping's Inference-Memory Gap via KV-Sharing.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.31633)

- **bioMoR: Biology-Guided Mixture-of-Recursions for Effective Genomic Learning.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.06727)

- **CHASE: Cache-Hole-Adapted Skip Exit for Looped State-Space Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.10110)

- **CopyLoop: Fast Looped Transformer Decoding via Context Copying and Shallow Screening.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.38822)

- **Decoding Looped Transformers Better for (Almost) Free.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.02185)

- **Depth-adaptive Inference of Looped Language Models via Continuous Depth Batching.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.09444)

- **Do Halting Heads Really Save Compute in Looped Language Models?.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.32246)

- **Dual-Slot: From Serial Loops to Parallel Slots in Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.25086)

- **Dynamic K-Head: Difficulty-Supervised Budget Selection for Continuous Latent Reasoning.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.17679)

- **ElTab: Elastically Looped Tabular Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.41819)

- **Enabling Dynamic Computation in Looped LMs.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.09013)

- **Energy-guided Recursive Model.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.10128)

- **Extending Reasoning in Typed Decision Models via Looping.** arXiv, 2026. [Paper](https://arxiv.org/abs/2611.07736)

- **FlashLoop: Fast and Memory-Efficient Looped Transformers via Lazy Updates.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.29812)

- **FlexLoop: Depth-Elastic Looped Policies for Adaptive Test-Time Computation in Deep RL.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.34488)

- **How to Loop Your Transformer: Loop Scaling, Specialization, and Parallel Inference.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.40325)

- **Hybrid Latent Attention for Looped Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.07940)

- **Hyperloop Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2604.21254)

- **Improving Test-Time Scaling with Adaptive Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.35748) · [Code](https://github.com/thu-nics/TaH)

- **LEV: Thinking Fast and Deep with Looped Decision Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.20951) · [Code](https://github.com/OpenLAIR/lev)

- **Library of Layers (LoL): Adaptively Ordering Transformer Layers at Runtime.** arXiv, 2026. [Paper](https://arxiv.org/abs/2611.03526)

- **LooM: Loop-Invariant Memory for Causal Encoder-Decoder Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2611.06835)

- **Loop to Look Better: Learning Adaptive Depth for Question-Guided Perception in Vision-Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.30824)

- **LoopAhead: Speculating Ahead for Faster Decoding in Looped Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.21594)

- **Looped Actor: Depth-Recurrent Reasoning Models for Reinforcement Learning.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.37432) · [Code](https://github.com/camail-official/LoopedActor)

- **Looped Latent Attention: Cross-Loop KV Compression for Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.15456)

- **Looped World Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2606.18208)

- **LoopFold: Parallelizing Recurrent Depth in Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.35556)

- **LoopFormer: Elastic-Depth Looped Transformers for Latent Reasoning via Shortcut Modulation.** ICLR, 2026. [Paper](https://arxiv.org/abs/2602.11451)

- **LoopKV: Loop-Aware KV Cache Compression for Serving Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2611.04137)

- **LoopMoEVR: Loop-Based Degradation-Aware Mixture-of-Experts for Unified UHD Video Restoration.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.05109)

- **LoopQ: Quantization for Recursive Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2605.16343)

- **LoopQuant: Accurate and Efficient Post-Training Quantization for Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.16368) · [Code](https://github.com/Kishon-zzx/LoopQuant)

- **LoopSpec: Pipelined Self-Speculative Decoding for Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.17184)

- **LoopVQ: Sub 1-bit KV Cache Quantization for Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2611.05304)

- **Loopy: Low-Bit Quantization Framework for Looped Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.05265) · [Code](https://github.com/Shameless0817/Loopy-review.git)

- **LSTM-Style Looped Transformers with Shared KV Caches.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.33360)

- **LT2: Linear-Time Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2605.20670)

- **Memory-Efficient Looped Transformer: Decoupling Compute from Memory in Looped Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2605.07721)

- **MergeOver: Post-Training Token Merging for Recursive Vision Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.13141)

- **MoR-MLLM: Mixture of Recursions for Efficient Multimodal Large Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.08830)

- **Nanbeige4.2-3B on Apple Silicon: Fixing Deployment Bugs and Decreasing Looped Transformer Memory Overhead.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.13987) · [Code](https://github.com/johnhalloran321/Nanbeige4.2-3B-mps-fix)

- **Not All Loops Cost the Same: Phase-Dependent Depth for Serving Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2611.07211)

- **One Model to Loop Them All: Elastic Latent Recurrence for Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.12582)

- **Per-Token Fixed-Point Convergence in Depth-Recurrent Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.14427)

- **Quantizing Looped Transformers: Feedback Exposure and Calibration Blindness.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.30820)

- **Quantizing Recursive Reasoning Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.16237)

- **RAMP: Recurrent Adaptive Mixed Precision for Efficient Prefill in Recurrent-Depth Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.13041)

- **recAMPLIFY: Large-Scale Pretraining of Recursive Protein Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.26747) · [Code](https://github.com/chandar-lab/AMPLIFY/tree/recamplify)

- **Recency Is the Wrong Axis: A Negative Result on Windowed Deepest-Plane KV Caching in Looped Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.34436)

- **Recursive Scaling in Masked Diffusion Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2606.18022)

- **RecurTrace: Adaptive Latent Reasoning with Loop-Time Memory.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.03379)

- **ResidualQuant: KV Cache Quantization for Looped Transformers with 2-Bit Residuals.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.10381)

- **ScaleRLT: Exact Log-Probabilities and Fast Deferred Rollouts for Reinforcement Learning on Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.34427)

- **Shallow Queries, Mature Values: Depth-Asynchronous Self-Speculation for Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.34538)

- **Spherical Fixed-Point Reasoners: Adaptive Loop Halting on the Hypersphere.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.25646)

- **Stabilizing Extrapolation in Looped Transformers via Learned Stochastic Stopping.** arXiv, 2026. [Paper](https://arxiv.org/abs/2606.29983)

- **T-LoopFormer: Token-Level Elastic-Depth Looped Transformers with Dynamic Routing.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.15160) · [Code](https://github.com/YuMingQian1234/T-LoopFormer)

- **The Surprising Effectiveness of Shared Memory in Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.02383)

- **Think Harder Where It Matters: Item-Level Adaptive Recursion for Sequential Recommendation.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.30128) · [Code](https://github.com/Elpmis117/LoopRec)

- **Think-at-Hard: Dynamic Looped Transformers for Improved Reasoning.** ICML, 2026. [Paper](https://arxiv.org/abs/2511.08577) · [Code](https://github.com/thu-nics/TaH)

- **Towards Looped Models Done Right, Part II: Rethinking at Fixed Points.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.06833) · [Code](https://github.com/ifm-ai/xllm-loop)

- **WaveFront Decoding: Parallelized Self-Speculative Decoding for Looped Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.23033) · [Code](https://github.com/summerbro-hhj/wavefront-decoding)

- **What Sets the Serving Speed of Looped Language Models? Measurements and Optimizations Graded by Exactness.** arXiv, 2026. [Paper](https://arxiv.org/abs/2611.05150)

- **What Survives When You Compress a Recursive Reasoner for the Edge?.** arXiv, 2026. [Paper](https://arxiv.org/abs/2606.26488)

- **When Does Adaptive Halting Win? Selection Rules Matter in Looped Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2611.02333) · [Code](https://github.com/lonewolf15116/lookahead-halting)

- **Where Cognition Lives: Dissecting Emergent from Computed Function in a Minimal Complete Cognitive Architecture.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.22347) · [Code](https://github.com/fmarrabal/miuracognitive)

- **Where KV-Cache Error Lives in Looped Language Models: A Diagnostic Study of Ouro and Huginn.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.41825)

- **CoTFormer: A Chain-of-Thought Driven Architecture with Budget-Adaptive Computation Cost at Inference.** ICLR, 2025. [Paper](https://arxiv.org/abs/2310.10845)

- **Efficient Parallel Samplers for Recurrent-Depth Models and Their Connection to Diffusion Language Models.** arXiv, 2025. [Paper](https://arxiv.org/abs/2510.14961) · [Code](https://github.com/seal-rg/recurrent-pretraining)

- **Mixture-of-Recursions: Learning Dynamic Recursive Depths for Adaptive Token-Level Computation.** NeurIPS, 2025. [Paper](https://arxiv.org/abs/2507.10524) · [Code](https://github.com/raymin0223/mixture_of_recursions)

- **Parallel Loop Transformer for Efficient Test-Time Computation Scaling.** arXiv, 2025. [Paper](https://arxiv.org/abs/2510.24824)

- **Two-Scale Latent Dynamics for Recurrent-Depth Transformers.** arXiv, 2025. [Paper](https://arxiv.org/abs/2509.23314)

- **PonderNet: Learning to Ponder.** ICML Workshop, 2021. [Paper](https://arxiv.org/abs/2107.05407)

</details>

[Back to topics](#topics)

<a id="analysis-applications"></a>

### Analysis & applications

Latent dynamics and applications beyond text.

<details>
<summary>View 106 entries</summary>

- **AdaLoop: Adaptive-Depth Latent Reasoning for Audio Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.06949)

- **ALoDLM: Adaptively Looped Diffusion Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.04198)

- **Behaviour Is an Incomplete Measure of Reasoning Development: Cross-surface pre-arrival accessibility and the limits of developmental inference in a recurrent-depth reasoner.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.16085)

- **Beyond Depth Truncation: Controlled Evaluation of Depth Utilization in Recursive Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.19934)

- **Beyond the Training Horizon: Mechanisms and Limits of Length Generalization in Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.33144)

- **bioMoR: Biology-Guided Mixture-of-Recursions for Effective Genomic Learning.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.06727)

- **Chain Dimension Scaling: Communication-Efficient Loop-Style Scaling for Industrial Short-Video Ranking.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.16415)

- **Compute Time Scaling with Recursive Models for Combinatorial Optimization.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.34585)

- **Cross-Loop Query Handoff: How Later Loops Redirect Two-Hop Retrieval in the Ouro Looped Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.34639) · [Code](https://github.com/Muuzzziiy/cql-handoff)

- **Depth through recurrence: Looped transformers for flow-matching TTS.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.29768)

- **Depth through Recurrence: Towards Ultra-Efficient On-Device ASR.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.37833)

- **Dissecting Hierarchical Reasoning Models: A Mechanistic Study.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.22197)

- **Does Latent Chain-of-Thought Actually Reason? A Single, Unifying Taxonomy for Latent Reasoning.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.21182)

- **Dynamic System Inspired Continuous Large Language Model for AI4Science Tasks.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.26959)

- **Dynamical phase selection controls compute scaling in looped transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.26556)

- **Déjà View: Looping Transformers for Multi-View 3D Reconstruction.** arXiv, 2026. [Paper](https://arxiv.org/abs/2605.30215)

- **ELT: Elastic Looped Transformers for Visual Generation.** arXiv, 2026. [Paper](https://arxiv.org/abs/2604.09168)

- **ElTab: Elastically Looped Tabular Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.41819)

- **Evaluating Tiny Recursive Models Across Training for Code Generation.** CASCON, 2026. [Paper](https://arxiv.org/abs/2608.29376)

- **Exploring Recurrent-Depth Language Models for Multitask Clinical Text Processing.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.27559)

- **FlexLoop: Depth-Elastic Looped Policies for Adaptive Test-Time Computation in Deep RL.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.34488)

- **FlowTSFM: Turning Encoder Depth into Quantile Transport.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.13640)

- **G-RRM: Guiding Symbolic Solvers with Recurrent Reasoning Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.02491)

- **HistoLoop: Iterative Contextual Inference with a Looped Transformer for Histology-Based Spatial Gene Expression Prediction.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.28339)

- **How Depth Growth and Looping Shape In-Context Learning in Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.31421)

- **Inside the Loop: A Mechanistic Study of Weight-Tied Transformers on Depth-Bound Algorithmic Tasks.** NeurIPS, 2026. [Paper](https://arxiv.org/abs/2610.24135) · [Code](https://github.com/magnus-sesodia/insidetheloop)

- **LAST: Looped Audio Spectrogram Transformer.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.01926)

- **LatentMT: Machine Translation with Latent Reasoning.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.18618)

- **Learning to Compute Is Not Learning to Retain or Reuse in Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.19768)

- **LEV: Thinking Fast and Deep with Looped Decision Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.20951) · [Code](https://github.com/OpenLAIR/lev)

- **LiFT: Loop Flow Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.05538)

- **Look, Reason, Draw a Region: Recursive Refinement for Spatial Context Prediction.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.23302)

- **Loop as a Bridge: Can Looped Transformers Truly Link Representation Space and Natural Language Outputs?.** arXiv, 2026. [Paper](https://arxiv.org/abs/2601.10242)

- **Loop Before You Leap: What Recurrent Depth Can and Cannot Buy in Data-Limited Pretraining.** BabyLM, 2026. [Paper](https://arxiv.org/abs/2611.06206)

- **Loop to Look Better: Learning Adaptive Depth for Question-Guided Perception in Vision-Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.30824)

- **Looped Actor: Depth-Recurrent Reasoning Models for Reinforcement Learning.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.37432) · [Code](https://github.com/camail-official/LoopedActor)

- **Looped Diffusion Transformer.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.40305)

- **Looped GNNs Beyond Fixed Depth: Graph Size Generalization and Parameter-Efficient Adaptation.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.24112)

- **Looped GPT-BERT: Trading Parameters for Computation in Small Language Modeling.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.09691)

- **Looped Language Models Improve Compositional Tool Calling.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.18171)

- **Looped Transformers under the Jacobian Lens: Does the Global Workspace Survive Recurrence?.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.01924)

- **Looped Uniform Diffusion Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.30066)

- **Looped World Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2606.18208)

- **LoopGR: Parameter-Efficient Scaling for Generative Recommendation via Recurrent Depth.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.34157)

- **LoopICL: Looping a single transformer block to solve tabular tasks.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.36108)

- **Looping Back to Move Forward: Recursive Transformers for Efficient and Flexible Large Multimodal Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2602.09080)

- **LoopMoEVR: Loop-Based Degradation-Aware Mixture-of-Experts for Unified UHD Video Restoration.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.05109)

- **LoopREG: Representation Supervision Enables Test-Time Recurrent Depth in Diffusion Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.17877)

- **LoopTrack: A Simple Baseline for Parameter-Efficient Transformer Tracking.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.33306)

- **LoopVAE: Recurrent Depth Across Scales for Visual Tokenization.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.11516)

- **LoopViT: Scaling Visual ARC with Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2602.02156) · [Code](https://github.com/WenjieShu/LoopViT)

- **LoopVL: Recurrent Visual Intelligence.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.38426)

- **MergeOver: Post-Training Token Merging for Recursive Vision Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.13141)

- **Monitoring latent reasoning in looped language models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.18127)

- **MoR-MLLM: Mixture of Recursions for Efficient Multimodal Large Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.08830)

- **Nanbeige4.2-3B: Unlocking Agentic Capabilities in a Compact Model.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.22083)

- **Not All Thinking is Created Equal: Latent Reasoning Discovers a Recurrent Search Algorithm for Depth Generalization.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.35643)

- **Observable Patterns Are Not Explanations: A Causal-Geometric Analysis of Latent Reasoning Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2606.12689)

- **On the Chain-of-Thought Monitorability of Looped Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.02741)

- **One Block, Multiple Depths: Recurrent Vision Transformers with Depth-Programmed Experts.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.12448)

- **Operational Proto-Introspection in Looped Language Models: Process-Quality Taps, Executable Branching, and the Readout-Control Boundary.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.18553)

- **Prediction Dynamics in Depth-Recurrent Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.21383)

- **Present but Hard to Read: Probing Latent Reasoning with Minimal Pairs.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.28498) · [Code](https://github.com/Aur-Shalev-Merin/present-but-hard-to-read)

- **RD-ViT: Recurrent-Depth Vision Transformer for Semantic Segmentation with Reduced Data Dependence Extending the Recurrent-Depth Transformer Architecture to Dense Prediction.** arXiv, 2026. [Paper](https://arxiv.org/abs/2605.03999)

- **recAMPLIFY: Large-Scale Pretraining of Recursive Protein Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.26747) · [Code](https://github.com/chandar-lab/AMPLIFY/tree/recamplify)

- **RecRec: Latent Interests Recursive Reasoning for Sequential Recommendation.** RecSys, 2026. [Paper](https://arxiv.org/abs/2607.12945)

- **RecRec: Recursive Refinement for Sequential Recommendation.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.10541)

- **Recurrent In-Context Learning for Tabular Foundation Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.14998)

- **Recurrent-Depth VLA: Implicit Test-Time Compute Scaling of Vision-Language-Action Models via Latent Iterative Reasoning.** arXiv, 2026. [Paper](https://arxiv.org/abs/2602.07845) · [Code](https://rd-vla.github.io/)

- **Recursive CLIP: Vision-Language Distillation with Looped Transformer Blocks.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.34563)

- **Recursive Scaling in Masked Diffusion Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2606.18022)

- **Recursive transformers for semiconductor thermo-mechanical reliability.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.27251)

- **REIMU: Efficient Heterogeneous Hierarchical Reasoning for SSL-Based Speech Deepfake Detection.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.00857)

- **RELAGRAM: Recursive Latent Graph Model for the Capacitated Vehicle Routing Problem.** NeurIPS Workshop, 2026. [Paper](https://arxiv.org/abs/2610.15106)

- **ReLoop-UME: Recurrent Depth with Learnable Retrieval Registers for Universal Multimodal Embedding.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.28751)

- **Repeated Shared Access Enables Grokking, but Edit Propagation Depends on an Addressable Memory.** arXiv, 2026. [Paper](https://arxiv.org/abs/2606.20737)

- **Rethinking Depth: A study of the Recursive-Transformer for Speech Recognition.** arXiv, 2026. [Paper](https://arxiv.org/abs/2606.09357)

- **Retrofitting Recurrent Vision-Language Models from Pretrained Backbones.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.22075) · [Code](https://madhavesdios.github.io/recurrent-vlms)

- **Right Direction, Wrong Step: Geometric Analysis of Finite-Step Failure in Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.16665)

- **Running Fewer Loops Removes Refusal Behaviour in Recurrent-Depth Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.15218)

- **Safe at One Loop, Risky at Another: Aligning Safety Across Recurrent Depths in Looped Language Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.10625)

- **Same path, different walk: a mechanistic comparison of looped and stacked transformer encoders on 12-lead ECG.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.15498)

- **SanSi: A Looped Typed Decision Model for System 1.5 Thinking.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.07730) · [Code](https://minnesotanlp.github.io/Sansi/)

- **Scaling RNA Foundation Models through Iterative Refinement.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.13106)

- **Shared Weights, Selected Computations: How Looped Transformers Route What Each Loop Does.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.39892) · [Code](https://github.com/wjjpku/howloop)

- **Slots, Transitions, Loops: Learning Composable World Models for ARC.** arXiv, 2026. [Paper](https://arxiv.org/abs/2606.12316)

- **Soft Mixture-of-Recursions: Going Deeper with Recursive Vision Transformers.** WACV, 2026. [Paper](https://arxiv.org/abs/2607.00774) · [Code](https://github.com/sangin-lee/sr-vit)

- **Solv3R: 3D Looped Transformer as a Multi-view Solver.** arXiv, 2026. [Paper](https://arxiv.org/abs/2611.02857) · [Code](https://ubc-vision.github.io/solv3r/)

- **Step-resolved data attribution for looped transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2602.10097)

- **Stream Recursion Model (SRM).** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.28809)

- **TAFFY: A Task-Adaptive Tabular Foundation Model with In-Context Diversity.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.07559)

- **Test-Time Compute Scaling for ASR with Depth-Conditioned Looped Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2606.04678)

- **Test-Time Forecasting: Recurrent Depth Enables In-Context Dynamics Prediction.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.19552)

- **The Ignition Is Real, and It Lives at the Readout: Latent composition, difficulty-clocked ignition, and the interface-constituted commit in a recurrent-depth reasoner.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.03263)

- **Think Before You Paint: Recursive Latent Reasoning for Diffusion Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.09876)

- **Think Harder Where It Matters: Item-Level Adaptive Recursion for Sequential Recommendation.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.30128) · [Code](https://github.com/Elpmis117/LoopRec)

- **Thinking in Depth, Speaking Directly: Recurrent Latent Reasoning for Paralinguistically Grounded Spoken Dialogue.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.37818)

- **Tiny Recursive Policy: Recursive Latent Refinement for Visuomotor Control.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.33288)

- **TraceViT: Grounded Trace Supervision for Visual Abstract Reasoning.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.29586) · [Code](https://github.com/LiuBinnan/TraceViT)

- **Training Crossroads for Recurrent Vision Transformers: Recurrence, Neural ODEs, and Deep Supervision.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.04879)

- **Training-Free Hidden-State Refinement for Flow-Matching Image Generators.** arXiv, 2026. [Paper](https://arxiv.org/abs/2608.29160)

- **When Recursive Models Finish Computing.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.26487)

- **Where KV-Cache Error Lives in Looped Language Models: A Diagnostic Study of Ouro and Huginn.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.41825)

- **Block-Recurrent Dynamics in Vision Transformers.** arXiv, 2025. [Paper](https://arxiv.org/abs/2512.19941)

- **Latent Chain-of-Thought? Decoding the Depth-Recurrent Transformer.** Workshop, 2025. [Paper](https://arxiv.org/abs/2507.02199) · [Code](https://github.com/wenquanlu/huginn-latent-cot)

- **Two-Scale Latent Dynamics for Recurrent-Depth Transformers.** arXiv, 2025. [Paper](https://arxiv.org/abs/2509.23314)

</details>

[Back to topics](#topics)

<a id="surveys-related-reasoning"></a>

### Surveys & related reasoning

Overviews and adjacent approaches to latent reasoning.

<details>
<summary>View 22 entries</summary>

- **Assessing Adversarial Robustness of Latent Reasoning Models.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.22228) · [Code](https://github.com/PKU-ML/latent-reasoning-model-assessment)

- **Does Latent Chain-of-Thought Actually Reason? A Single, Unifying Taxonomy for Latent Reasoning.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.21182)

- **Dynamic K-Head: Difficulty-Supervised Budget Selection for Continuous Latent Reasoning.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.17679)

- **INTACT: Inducing Latent Reasoning on a Frozen Backbone.** arXiv, 2026. [Paper](https://arxiv.org/abs/2610.19568)

- **J-CoT: Chain-of-Thought in J-Space.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.21981)

- **Latent Recurrent Thoughts: Recurrent Refinement of Proposed Latents for Reasoning with Frozen LLMs.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.01117)

- **Learning When to Think Aloud in Latent Reasoning.** arXiv, 2026. [Paper](https://arxiv.org/abs/2611.06108)

- **Not All Thinking is Created Equal: Latent Reasoning Discovers a Recurrent Search Algorithm for Depth Generalization.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.35643)

- **Penelope: Localized Latent Recurrence for Efficient Structured Reasoning.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.25915)

- **SLPO: Scaling Latent Reasoning via a Surrogate Policy.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.19691)

- **T^2MLR: Transformer with Temporal Middle-Layer Recurrence.** arXiv, 2026. [Paper](https://arxiv.org/abs/2607.15178)

- **Trading Depth for Time in Recurrent Transformers.** arXiv, 2026. [Paper](https://arxiv.org/abs/2609.21605)

- **Why Limit the Residual Stream to Layers and Not Tokens? Persistent Memory for Continuous Latent Reasoning.** arXiv, 2026. [Paper](https://arxiv.org/abs/2606.07720)

- **A Survey on Latent Reasoning.** arXiv, 2025. [Paper](https://arxiv.org/abs/2507.06203) · [Code](https://github.com/multimodal-art-projection/LatentCoT-Horizon/)

- **AbbIE: Autoregressive Block-Based Iterative Encoder for Efficient Sequence Modeling.** arXiv, 2025. [Paper](https://arxiv.org/abs/2507.08567)

- **Closed-Loop Transformers: Autoregressive Modeling as Iterative Latent Equilibrium.** arXiv, 2025. [Paper](https://arxiv.org/abs/2511.21882)

- **Encode, Think, Decode: Scaling test-time reasoning with recursive latent thoughts.** arXiv, 2025. [Paper](https://arxiv.org/abs/2510.07358)

- **PonderLM: Pretraining Language Models to Ponder in Continuous Space.** arXiv, 2025. [Paper](https://arxiv.org/abs/2505.20674)

- **Training Large Language Models to Reason in a Continuous Latent Space.** COLM, 2025. [Paper](https://arxiv.org/abs/2412.06769)

- **Compressed Chain of Thought: Efficient Reasoning Through Dense Representations.** arXiv, 2024. [Paper](https://arxiv.org/abs/2412.13171)

- **Mixture-of-Depths: Dynamically allocating compute in transformer-based language models.** arXiv, 2024. [Paper](https://arxiv.org/abs/2404.02258)

- **Think before you speak: Training Language Models With Pause Tokens.** ICLR, 2024. [Paper](https://arxiv.org/abs/2310.02226)

</details>

[Back to topics](#topics)

## Maintain the collection

Collection snapshot: **2026-11-06**. This presentation update does not claim a new literature search.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the catalog fields and validation steps.

~~~bash
python3 src/generator.py
~~~

This rebuilds the README, reading guide, diagrams, and offline browser from the catalog. It requires only the Python standard library.

## Citation

~~~bibtex
@misc{awesome_loop_transformer_2026,
  title = {Awesome Loop Transformer},
  author = {{Repository contributors}},
  year = {2026},
  url = {https://github.com/asimfish/awesome_loop_transformer}
}
~~~

## License

Repository text is available under [CC BY 4.0](LICENSE). Original papers and third-party software retain their respective licenses.
