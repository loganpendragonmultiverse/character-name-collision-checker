# Testing

Run `python -m pip install -e ".[dev]"`, `ruff format --check .`, `ruff check .`, `mypy src`, `pytest`, and `python -m build`.

## 1.2.0 acceptance

Exercise the optional input with the full regression suite, including validation, inclusive boundaries, deterministic ordering and legacy default behavior. Use optional `characters` instead of legacy `names`: `[{"id":"mara","name":"Mara","aliases":["Captain"]},{"id":"mira","name":"Mira","aliases":["Captain"]}]`. Comparisons cross character IDs only; duplicate spellings within one character are collapsed ignoring case. Shared aliases across characters are reported. In this mode `allowed_pairs` contains character ID pairs and suppresses all their spellings; findings include `character_ids`. IDs are case-sensitive. The existing small English-oriented phonetic key remains a review aid, not pronunciation analysis.

## 1.2.3 input and report reliability

Validate legacy names and intentional exceptions without coercion; handle empty casts, finite thresholds, Unicode casefold lengths and consistent non-empty phonetic keys. Fence report data safely and create output files exclusively, including dangling symlink refusal.

Run all documented checks plus the validation/report regressions. Install both the wheel and source distribution in fresh environments and exercise every documented output format; source files must remain unchanged. Linux acceptance supplements the required GitHub Windows/macOS/Linux CI matrix.

The wheel installs the README, development/testing contract, changelog and JSON examples under the installation data directory at `share/character-name-collision-checker/`. The source distribution also includes these files in their original paths. Release acceptance compares both archives with the exact tagged files before testing fresh installations.
