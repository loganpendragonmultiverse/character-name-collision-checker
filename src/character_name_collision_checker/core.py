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
    if len(names) != len(set(name.casefold() for name in names)):
        raise ValueError("names must be unique ignoring case")
    collisions = []
    for left, right in combinations(names, 2):
        similarity = 1 - _distance(left.casefold(), right.casefold()) / max(
            len(left), len(right), 1
        )
        left_sound = re.sub("[aeiouy\\W]", "", left.casefold().replace("ph", "f"))
        right_sound = re.sub("[aeiouy\\W]", "", right.casefold().replace("ph", "f"))
        reasons = (["visual"] if similarity >= 0.72 else []) + (
            ["phonetic"] if left_sound == right_sound else []
        )
        if reasons:
            collisions.append(
                {"names": [left, right], "similarity": round(similarity, 3), "reasons": reasons}
            )
    return {"names_checked": len(names), "collisions": collisions}


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
