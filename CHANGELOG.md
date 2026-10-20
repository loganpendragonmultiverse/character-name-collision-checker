# Changelog

## 1.2.3 - 2026-10-20

- Bundle operating documentation and JSON examples in wheels as well as source distributions.

- Validate legacy names and intentional exceptions without coercion; handle empty casts, finite thresholds, Unicode casefold lengths and consistent non-empty phonetic keys. Fence report data safely and create output files exclusively, including dangling symlink refusal.

## 1.2.1

- Correct released documentation labels; package behavior is unchanged.
- Preserve the original v1.2.0 tags and artifacts. This patch supplies corrected documentation in new artifacts.

## 1.2.0 - 2026-10-15

- Use optional `characters` instead of legacy `names`: `[{"id":"mara","name":"Mara","aliases":["Captain"]},{"id":"mira","name":"Mira","aliases":["Captain"]}]`.

## 1.1.0 - 2026-07-27

- Added configurable visual-similarity thresholds and intentional allowed pairs.
- Added edit-distance and phonetic-key evidence to each finding.

## 1.0.0 - 2026-07-26

- Released the first complete Character Name Collision Checker command-line workflow.
- Added deterministic JSON and Markdown reporting, representative examples, and cross-platform tests.

## Unpublished verification candidate: v1.2.2

The immutable v1.2.2 tag was a verification candidate, with no public GitHub release. Its wheel did not bundle the separate operating guides and examples. v1.2.3 supersedes that candidate and includes the reviewed runtime repairs together with complete installed guidance.
