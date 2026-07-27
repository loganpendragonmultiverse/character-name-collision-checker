import json
from pathlib import Path

import pytest

from character_name_collision_checker.cli import main
from character_name_collision_checker.core import PROJECT, analyze, render_json, render_markdown


def test_representative_sample_has_expected_result():
    data = json.loads(
        (Path(__file__).parents[1] / "examples" / "sample.json").read_text(encoding="utf-8")
    )
    report = analyze(data)
    assert report["version"] == 1
    assert report["project"] == PROJECT
    assert report["collisions"][0]["names"] == ["Mara", "Mira"]
    assert report["collisions"][0]["edit_distance"] == 1
    assert len(report["collisions"][0]["phonetic_keys"]) == 2
    assert f'"project": "{PROJECT}"' in render_json(report)
    assert PROJECT.replace("-", " ").title() in render_markdown(report)


def test_missing_required_input_is_rejected():
    with pytest.raises(ValueError):
        analyze({})


def test_configurable_threshold_and_allowed_pairs():
    report = analyze(
        {
            "names": ["Mara", "Mira", "Ivo"],
            "visual_threshold": 0.7,
            "allowed_pairs": [["Mara", "Mira"]],
        }
    )
    assert report["allowed_pair_count"] == 1
    assert report["collisions"] == []
    with pytest.raises(ValueError, match="visual_threshold"):
        analyze({"names": ["Mara", "Mira"], "visual_threshold": 2})


def test_cli_json_and_output_safety(tmp_path, capsys):
    source = Path(__file__).parents[1] / "examples" / "sample.json"
    assert main([str(source), "--format", "json"]) == 0
    assert json.loads(capsys.readouterr().out)["project"] == PROJECT
    output = tmp_path / "report.md"
    output.write_text("keep", encoding="utf-8")
    assert main([str(source), "--output", str(output)]) == 2
