from __future__ import annotations

import json
import math
import re
from itertools import combinations
from typing import Any

PROJECT = "character-name-collision-checker"


def _threshold(data: dict[str, Any]) -> float:
    value = data.get("visual_threshold", 0.72)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("visual_threshold must be a finite number between 0 and 1")
    if not 0 <= value <= 1:
        raise ValueError("visual_threshold must be a finite number between 0 and 1")
    threshold = float(value)
    if not math.isfinite(threshold) or not 0 <= threshold <= 1:
        raise ValueError("visual_threshold must be a finite number between 0 and 1")
    return threshold


def _sound(name: str) -> str:
    return re.sub(r"[aeiouy\W_]", "", name.casefold().replace("ph", "f"))


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
    raw = data.get("names")
    if not isinstance(raw, list) or any(
        not isinstance(name, str) or not name.strip() for name in raw
    ):
        raise ValueError("names must be an array of non-empty strings")
    names = [name.strip() for name in raw]
    if len(names) != len({name.casefold() for name in names}):
        raise ValueError("names must be unique ignoring case")
    threshold = _threshold(data)
    allowed = data.get("allowed_pairs", [])
    known = {name.casefold() for name in names}
    if not isinstance(allowed, list) or any(
        not isinstance(pair, list)
        or len(pair) != 2
        or any(not isinstance(name, str) or name.strip().casefold() not in known for name in pair)
        or pair[0].strip().casefold() == pair[1].strip().casefold()
        for pair in allowed
    ):
        raise ValueError("allowed_pairs must contain two distinct known names")
    allowed_pairs = {frozenset(name.strip().casefold() for name in pair) for pair in allowed}
    collisions = []
    for left, right in combinations(names, 2):
        if frozenset({left.casefold(), right.casefold()}) in allowed_pairs:
            continue
        distance = _distance(left.casefold(), right.casefold())
        similarity = 1 - distance / max(len(left.casefold()), len(right.casefold()), 1)
        left_sound, right_sound = _sound(left), _sound(right)
        reasons = (["visual"] if similarity >= threshold else []) + (
            ["phonetic"] if left_sound and left_sound == right_sound else []
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
            sound = _sound(left)
            findings = [
                {
                    "names": [left, right],
                    "similarity": 1.0,
                    "edit_distance": 0,
                    "phonetic_keys": [sound, sound],
                    "reasons": ["visual"] + (["phonetic"] if sound else []),
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
    if not isinstance(data, dict):
        raise TypeError("input must be an object")
    if "names" in data and "characters" in data:
        raise ValueError("supply names or characters, not both")
    return {"version": 1, "project": PROJECT, **_name_collisions(data)}


def render_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False) + "\n"


def render_markdown(report: dict[str, Any]) -> str:
    lines = [f"# {report['project'].replace('-', ' ').title()} report", ""]
    for key, value in report.items():
        if key not in {"version", "project"}:
            lines.append(f"## {key.replace('_', ' ').title()}")
            lines.append("")
            payload = json.dumps(value, indent=2, ensure_ascii=False)
            fence = "`" * max(
                3, max((len(run) + 1 for run in re.findall(r"`+", payload)), default=3)
            )
            lines.append(f"{fence}json\n{payload}\n{fence}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"
