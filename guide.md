# Reading guide: Loop Transformer

[Back to the collection](README.md)

## Start with the mechanism

A looped transformer applies a shared transformation repeatedly to a hidden state. Keep three choices separate: which layers repeat, how many times they repeat, and whether the loop count changes at inference.

[Universal Transformers](https://arxiv.org/abs/1807.03819) · [English report](reports/en/01_universal_transformers.md)

## Choose a reading path

Read Universal Transformers for the architecture, Huginn for recurrent-depth pretraining, Training-Free Looped Transformers for retrofitting, LoopCoder-v2 for parallel looping, and Loop the Loopies for compute-matched pretraining.

[Five core papers](index.html?core=1#library) · [Detailed survey](survey/en/survey_en.md)

## Separate the compute budgets

A fixed pretraining budget and a variable inference budget answer different questions. Compare parameter count, training compute, inference latency, and KV-cache use separately. A result at one loop count does not establish a universal optimum.

[Inference & efficiency](index.html?category=Inference+%26+efficiency#library)

## Understand the taxonomy

The collection has six broad reading areas. Original fine-grained topics remain searchable on every record, and a paper can belong to more than one area. Core papers are a reading route rather than a separate research category.

[Training & adaptation](index.html?category=Training+%26+adaptation#library) · [Architectures & pretraining](index.html?category=Architectures+%26+pretraining#library)

## Read claims with their conditions

Check the baseline, data budget, model size, and evaluation setting before comparing results. The collection's listed year follows the existing catalog and may be a venue year rather than the first preprint date. External articles are context, not evidence of a proprietary model's architecture.

[Complete paper catalog](data/papers.csv) · [Original core PDFs](https://github.com/asimfish/awesome_loop_transformer/tree/main/papers/original)
