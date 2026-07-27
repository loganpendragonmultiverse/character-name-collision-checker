from __future__ import annotations

import json
import re
from itertools import combinations
from typing import Any

PROJECT = "character-name-collision-checker"


def _require(data: dict[str, Any], key: str) -> Any:
    value = data.get(key)
    if value is None or value == "" or value == []:
        raise ValueError(f"{key} is required")
    return value


def _distance(left: str, right: str) -> int:
    previous = list(range(len(right) + 1))
    for row, left_char in enumerate(left, 1):
        current = [row]
        for column, right_char in enumerate(right, 1):
            current.append(
                min(
                    current[-1] + 1,
                    previous[column] + 1,
                    previous[column - 1] + (left_char != right_char),
                )
            )
        previous = current
    return previous[-1]


def _name_collisions(data: dict[str, Any]) -> dict[str, Any]:
    names = [str(name).strip() for name in _require(data, "names") if str(name).strip()]
    if len(names) != len({name.casefold() for name in names}):
        raise ValueError("names must be unique ignoring case")
    threshold = float(data.get("visual_threshold", 0.72))
    if not 0 <= threshold <= 1:
        raise ValueError("visual_threshold must be between 0 and 1")
    allowed_pairs = {
        frozenset(str(name).strip().casefold() for name in pair)
        for pair in data.get("allowed_pairs", [])
        if isinstance(pair, list) and len(pair) == 2
    }
    collisions = []
    for left, right in combinations(names, 2):
        if frozenset({left.casefold(), right.casefold()}) in allowed_pairs:
            continue
        distance = _distance(left.casefold(), right.casefold())
        similarity = 1 - distance / max(len(left), len(right), 1)
        left_sound = re.sub("[aeiouy\\W]", "", left.casefold().replace("ph", "f"))
        right_sound = re.sub("[aeiouy\\W]", "", right.casefold().replace("ph", "f"))
        reasons = (["visual"] if similarity >= threshold else []) + (
            ["phonetic"] if left_sound == right_sound else []
        )
        if reasons:
            collisions.append(
                {
                    "names": [left, right],
                    "similarity": round(similarity, 3),
                    "edit_distance": distance,
                    "phonetic_keys": [left_sound, right_sound],
                    "reasons": reasons,
                }
            )
    return {
        "names_checked": len(names),
        "visual_threshold": threshold,
        "allowed_pair_count": len(allowed_pairs),
        "collisions": collisions,
    }


def analyze(data: dict[str, Any]) -> dict[str, Any]:
    return {"version": 1, "project": PROJECT, **_name_collisions(data)}


def render_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False) + "\n"


def render_markdown(report: dict[str, Any]) -> str:
    lines = [f"# {report['project'].replace('-', ' ').title()} report", ""]
    for key, value in report.items():
        if key not in {"version", "project"}:
            lines.append(f"## {key.replace('_', ' ').title()}")
            lines.append("")
            lines.append(f"```json\n{json.dumps(value, indent=2, ensure_ascii=False)}\n```")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"
