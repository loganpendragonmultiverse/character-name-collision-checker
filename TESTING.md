# Testing

Run `python -m pip install -e ".[dev]"`, `ruff format --check .`, `ruff check .`, `mypy src`, `pytest`, and `python -m build`.

## 1.2.0 acceptance

Exercise the optional input with the full regression suite, including validation, inclusive boundaries, deterministic ordering and legacy default behavior. Use optional `characters` instead of legacy `names`: `[{"id":"mara","name":"Mara","aliases":["Captain"]},{"id":"mira","name":"Mira","aliases":["Captain"]}]`. Comparisons cross character IDs only; duplicate spellings within one character are collapsed ignoring case. Shared aliases across characters are reported. In this mode `allowed_pairs` contains character ID pairs and suppresses all their spellings; findings include `character_ids`. IDs are case-sensitive. The existing small English-oriented phonetic key remains a review aid, not pronunciation analysis.
