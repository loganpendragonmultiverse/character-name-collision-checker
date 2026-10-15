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
    if "characters" in data:
        return _character_collisions(data)
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


def _character_collisions(data: dict[str, Any]) -> dict[str, Any]:
    characters = data["characters"]
    if not isinstance(characters, list):
        raise TypeError("characters must be an array")
    ids: set[str] = set()
    spellings: list[tuple[str, str]] = []
    for character in characters:
        if not isinstance(character, dict):
            raise TypeError("characters must contain objects")
        identifier, name = character.get("id"), character.get("name")
        aliases = character.get("aliases", [])
        if (
            not isinstance(identifier, str)
            or not identifier.strip()
            or identifier in ids
            or not isinstance(name, str)
            or not name.strip()
            or not isinstance(aliases, list)
            or any(not isinstance(alias, str) or not alias.strip() for alias in aliases)
        ):
            raise ValueError("characters need unique ids, names and text aliases")
        ids.add(identifier)
        seen: set[str] = set()
        for spelling in [name, *aliases]:
            spelling = spelling.strip()
            if spelling.casefold() not in seen:
                seen.add(spelling.casefold())
                spellings.append((identifier, spelling))
    allowed = data.get("allowed_pairs", [])
    if not isinstance(allowed, list) or any(
        not isinstance(pair, list)
        or len(pair) != 2
        or any(not isinstance(key, str) or key not in ids for key in pair)
        or pair[0] == pair[1]
        for pair in allowed
    ):
        raise ValueError("allowed_pairs must contain two distinct character ids")
    permitted = {frozenset(pair) for pair in allowed}
    # Reuse the existing threshold/key rules; identical cross-character spellings are explicit.
    base = _name_collisions(
        {"names": ["validation"], "visual_threshold": data.get("visual_threshold", 0.72)}
    )
    collisions = []
    for (left_id, left), (right_id, right) in combinations(spellings, 2):
        if left_id == right_id or frozenset((left_id, right_id)) in permitted:
            continue
        if left.casefold() == right.casefold():
            sound = re.sub(r"[aeiouy\W]", "", left.casefold().replace("ph", "f"))
            findings = [
                {
                    "names": [left, right],
                    "similarity": 1.0,
                    "edit_distance": 0,
                    "phonetic_keys": [sound, sound],
                    "reasons": ["visual", "phonetic"],
                }
            ]
        else:
            findings = _name_collisions(
                {"names": [left, right], "visual_threshold": base["visual_threshold"]}
            )["collisions"]
        for finding in findings:
            collisions.append({**finding, "character_ids": [left_id, right_id]})
    return {
        **base,
        "names_checked": len(spellings),
        "characters_checked": len(ids),
        "allowed_pair_count": len(permitted),
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
