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
