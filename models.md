# Open model directory

[Back to the collection](README.md) · [Browse research](https://asimfish.github.io/awesome_loop_transformer/#library)

Model information retained from the November 6, 2026 collection. Consult the linked model cards and papers for current availability and configuration.

| Model | Params | Tokens | Loops | Link |
|---|---|---|---|---|
| Huginn-0125 | 3.5B dense | 0.8T | random at train, free at test (r̄=32) | [HF](https://huggingface.co/tomg-group-umd/huginn-0125) · [code](https://github.com/seal-rg/recurrent-pretraining) |
| Ouro 1.4B / 2.6B (+Thinking) | dense | 7.7T | 4 | [site](http://ouro-llm.github.io) |
| LoopCoder-V2 | 7B dense PLT | 18T | 2 | [HF](https://huggingface.co/Multilingual-Multimodal-NLP/LoopCoder-V2) |
| Loopie-20B-A2B / 6B-A0.6B | MoE | 3.5T | 2 (layer-loop) | see paper [2607.16051](https://arxiv.org/abs/2607.16051) (megatron-loopie, vllm-loopie) |
| Nanbeige4.2-3B | 3B | 28T | 2 | see paper [2607.22083](https://arxiv.org/abs/2607.22083) |
| Mimir v1 / v1.5 | 1.78B HRM-Text (L/H stacks) | 70.5B / 103B per epoch, multi-epoch | interleaved L/H schedule | see paper [2608.13517](https://arxiv.org/abs/2608.13517) |
| Metis-1.6 Praxis / Logos | 2.94B-A0.46B / 10.23B-A1.18B hybrid Mamba-2/attention MoE | 1.02T | 2 (whole stack) | [HF](https://huggingface.co/Lernex) · paper [2610.37903](https://arxiv.org/abs/2610.37903) |
| Dory1.0-4B | 4B nGPT, elastic depth | 6T | variable; KV cached from the last loop only | BF16 / MXFP8 / NVFP4 / GGUF checkpoints, see paper [2611.03998](https://arxiv.org/abs/2611.03998) |
| ARLoop 0.6B / 1.2B | attention residuals over depth | 0.5T (1.2B) | 3 | fully open, see paper [2611.05234](https://arxiv.org/abs/2611.05234) |
