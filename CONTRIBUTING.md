# Contributing

Thanks for helping keep this list complete and correct. 中文贡献者同样欢迎，issue 和 PR 可用中文书写。

## Suggest a paper without touching code

Open an issue with the [paper suggestion template](https://github.com/asimfish/awesome_loop_transformer/issues/new?template=paper-suggestion.md) and give the arXiv ID, the category, and a code link if one exists.

## Add a paper by pull request

`README.md` is generated. Do not edit it by hand; edit the sources and regenerate.

1. Add a tuple to `CURATED` in [`src/fetch_metadata.py`](src/fetch_metadata.py):

   ```python
   ("YYMM.NNNNN", "Scaled Pretraining;Efficiency: Latency, KV Cache & Quantization", "arXiv", 2026, "https://github.com/org/repo", "", "YYYY-MM-DD"),
   #  arXiv ID     categories, primary first, ';'-separated                          venue    year  code URL or ""          note added (today)
   ```

   - **Categories** must be names from `CATEGORY_ORDER` in [`src/generator.py`](src/generator.py). Use at most two.
   - **Venue** is the accepted venue (`ICLR`, `NeurIPS`, `ICML Workshop`, …) or `arXiv`. Update it when a preprint is accepted.
   - **Note** is optional and shows in italics after the links (for example `contrast: sequence-length scaling`). Leave `core` to the five core papers.
   - **Added** is today's date. Entries carrying the latest date get a 🆕 marker.

2. Refresh metadata and regenerate:

   ```bash
   python3 src/fetch_metadata.py   # pulls exact titles, authors and dates from the arXiv API into data/papers.csv
   python3 src/generator.py        # renders README.md; fails on an unknown category
   ```

   If you cannot reach the arXiv API, append the row to [`data/papers.csv`](data/papers.csv) by hand with the exact arXiv title and author list.

3. Commit `src/fetch_metadata.py`, `data/papers.csv` and `README.md` together and open a pull request.

## What belongs here

A paper fits when looping or recurrence **in depth** is its method or its object of analysis: weight-tied or looped transformers, recurrent-depth language models, Universal Transformer descendants, mixture-of-recursions, tiny recursive reasoners, and their theory, training, inference, and applications. Latent-reasoning methods that add computation without looping weights go under *Related: Latent Reasoning Beyond Looping*. Recurrence over time (RNNs, state-space models used only as sequence mixers) and agent "loops" are out of scope.

## Editing text

`data/header.md` and `data/footer.md` hold the prose around the list. They may use `{{N_PAPERS}}`, `{{N_NEW}}`, `{{N_CATEGORIES}}`, `{{UPDATED}}` and `{{UPDATED_BADGE}}`, which the generator fills from `data/papers.csv`. State claims plainly with their numbers and sources; see *How this was made* in the README for the writing conventions used in the reports.
