# Development contract

Flag character names that are visually or phonetically easy to confuse.

Version 1.1 makes visual thresholds and intentional exceptions explicit and exposes the mechanical evidence behind each prompt.

Preserve deterministic, source-safe behavior and the interpretation boundary documented in the README. Every feature release must update tests, version metadata, `CHANGELOG.md`, README claims and limitations, repository metadata, release assets, and the Forge catalog together.

## 1.2.0

Use optional `characters` instead of legacy `names`: `[{"id":"mara","name":"Mara","aliases":["Captain"]},{"id":"mira","name":"Mira","aliases":["Captain"]}]`. Comparisons cross character IDs only; duplicate spellings within one character are collapsed ignoring case. Shared aliases across characters are reported. In this mode `allowed_pairs` contains character ID pairs and suppresses all their spellings; findings include `character_ids`. IDs are case-sensitive. The existing small English-oriented phonetic key remains a review aid, not pronunciation analysis.
