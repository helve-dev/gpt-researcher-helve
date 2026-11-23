# gpt-researcher-helve

Search retriever plugin for [GPT Researcher](https://github.com/assafelovic/gpt-researcher) backed by [Helve](https://helve.dev) (`POST https://helve.dev/v1/search`).

Registers the `helve` retriever via the `gpt_researcher.retrievers` entry-point group so GPT Researcher can use it without patching core.

## Install

```bash
pip install gpt-researcher-helve
```

## Configure

Set your Helve API key and select `helve` as a retriever:

```bash
export HELVE_API_KEY="sk_live_..."
export RETRIEVER="helve"
```

Optional: choose a specific search backend via `HELVE_SEARCH_PROVIDER` (default: `auto`, or e.g. `fusion`, `tavily`, `exa`, `brave`, `serper`) or pass `helve_provider` / `helve_api_key` in GPT Researcher `headers`.

## Direct Usage

```python
from gpt_researcher_helve import HelveSearch

results = HelveSearch(
    query="transformer attention scaling laws",
    query_domains=["arxiv.org"],
).search(max_results=5)
```

Each result is returned in GPT Researcher's standard format: `{"href": "<url>", "body": "<text>"}`.

## Links

- Docs: https://docs.helve.dev
- Issue tracker: https://github.com/helve-dev/gpt-researcher-helve/issues
