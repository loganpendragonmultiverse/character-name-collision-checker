# Character Name Collision Checker

[![CI](https://github.com/loganpendragonmultiverse/character-name-collision-checker/actions/workflows/ci.yml/badge.svg)](https://github.com/loganpendragonmultiverse/character-name-collision-checker/actions/workflows/ci.yml)

Flag character names that are visually or phonetically easy to confuse. The command runs locally, uses explicit UTF-8 JSON input, and produces deterministic JSON or Markdown reports without modifying the supplied source material.

## Three-minute start

```bash
python -m pip install .
name-collisions examples/sample.json
name-collisions examples/sample.json --format json --output report.json
```

The example documents the complete input shape. Set `visual_threshold` to tune lexical sensitivity and list intentional two-name `allowed_pairs` to suppress known exceptions. Version 1.1 findings include edit-distance and phonetic-key evidence. Markdown is intended for immediate review; JSON preserves structured evidence for scripts and later comparison. An existing output file is never overwritten.

## Privacy and platforms

All character names stay local.

Python 3.10 or newer is supported on Windows, macOS, and Linux. The package has no runtime dependencies, telemetry, account, or hosted service.

## Interpretation boundary

Similarity scores are review aids, not claims that readers will be confused. Phonetic comparison uses a deliberately small English-oriented key.

## Development

```bash
python -m pip install -e ".[dev]"
ruff format --check .
ruff check .
mypy src
pytest
python -m build
```

The project is feature-complete for its documented v1 scope. Maintenance focuses on correctness, security, compatibility, and well-supported input improvements.

Part of the [Logan Pendragon Forge open-source collection](https://www.loganpendragonforge.com/open-source/). Licensed under the [MIT License](LICENSE).

## Version 1.2.0

Use optional `characters` instead of legacy `names`: `[{"id":"mara","name":"Mara","aliases":["Captain"]},{"id":"mira","name":"Mira","aliases":["Captain"]}]`. Comparisons cross character IDs only; duplicate spellings within one character are collapsed ignoring case. Shared aliases across characters are reported. In this mode `allowed_pairs` contains character ID pairs and suppresses all their spellings; findings include `character_ids`. IDs are case-sensitive. The existing small English-oriented phonetic key remains a review aid, not pronunciation analysis.

## Version 1.2.1: documentation correction

Version 1.2.0 was released on October 15, 2026. Version 1.2.1 corrects its release labels without changing behavior. The original v1.2.0 tag and downloadable artifacts remain unchanged; use v1.2.1 for the corrected packaged documentation.

## 1.2.2 input and report reliability

Validate legacy names and intentional exceptions without coercion; handle empty casts, finite thresholds, Unicode casefold lengths and consistent non-empty phonetic keys. Fence report data safely and create output files exclusively, including dangling symlink refusal.

Run all documented checks plus the validation/report regressions. Install both the wheel and source distribution in fresh environments and exercise every documented output format; source files must remain unchanged. Linux acceptance supplements the required GitHub Windows/macOS/Linux CI matrix.
