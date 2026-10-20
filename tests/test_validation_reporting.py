import json

import pytest

from character_name_collision_checker.cli import main
from character_name_collision_checker.core import analyze, render_markdown


@pytest.mark.parametrize(
    "data",
    [
        None,
        [],
        {"names": "Mara"},
        {"names": [4]},
        {"names": [" "]},
        {"names": ["Mara"], "characters": []},
        {"names": ["A"], "allowed_pairs": [["A", "B"]]},
        {"names": ["A"], "allowed_pairs": "bad"},
        {"names": ["A"], "allowed_pairs": [["A", "A"]]},
    ],
)
def test_bad_input_is_rejected(data):
    with pytest.raises((ValueError, TypeError)):
        analyze(data)


@pytest.mark.parametrize("threshold", [True, "0.5", None, float("nan"), float("inf"), -1])
def test_threshold_is_finite_number(threshold):
    with pytest.raises((ValueError, TypeError), match="visual_threshold"):
        analyze({"names": [], "visual_threshold": threshold})


def test_empty_names_and_unicode_scores():
    assert analyze({"names": []})["names_checked"] == 0
    report = analyze({"names": ["ß", "a"], "visual_threshold": 0})
    assert 0 <= report["collisions"][0]["similarity"] <= 1
    assert not analyze({"names": ["Aya", "Eve"], "visual_threshold": 1})["collisions"]
    assert analyze({"names": ["Ph-an", "Fan"], "visual_threshold": 1})["collisions"][0][
        "phonetic_keys"
    ] == ["fn", "fn"]


def test_markdown_fence_cannot_be_closed_by_name():
    rendered = render_markdown(
        analyze({"names": ["```<img src=x>", "```<img src=y>"], "visual_threshold": 0})
    )
    assert "````json" in rendered


def test_cli_malformed_and_dangling_symlink_output(tmp_path, capsys):
    source = tmp_path / "data.json"
    source.write_text("[]")
    assert main([str(source)]) == 2
    assert "Traceback" not in capsys.readouterr().err
    source.write_text(json.dumps({"names": []}))
    output = tmp_path / "output.json"
    target = tmp_path / "missing.json"
    output.symlink_to(target)
    assert main([str(source), "--output", str(output)]) == 2
    assert not target.exists()


def test_oversized_threshold_cli_and_api(tmp_path):
    data = {"names": [], "visual_threshold": 10**400}
    with pytest.raises(ValueError):
        analyze(data)
    source = tmp_path / "input.json"
    source.write_text(json.dumps(data))
    assert main([str(source)]) == 2
