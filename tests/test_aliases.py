import pytest

from character_name_collision_checker.core import analyze


def test_same_character_excluded_cross_character_aliases_compared():
    r = analyze(
        {
            "characters": [
                {"id": "a", "name": "Mara", "aliases": ["Mira", "MARA"]},
                {"id": "b", "name": "Zed", "aliases": ["Mira"]},
            ]
        }
    )
    assert r["names_checked"] == 4
    assert all(c["character_ids"] == ["a", "b"] for c in r["collisions"])
    assert any(c["names"] == ["Mira", "Mira"] and c["edit_distance"] == 0 for c in r["collisions"])


def test_allowed_id_pairs_and_legacy():
    data = {"characters": [{"id": "a", "name": "Mara"}, {"id": "b", "name": "Mira"}]}
    assert analyze(data)["collisions"]
    assert not analyze({**data, "allowed_pairs": [["b", "a"]]})["collisions"]
    assert "characters_checked" not in analyze({"names": ["Mara", "Mira"]})


@pytest.mark.parametrize(
    "characters",
    [
        {},
        [None],
        [{"id": "a", "name": "A", "aliases": [""]}],
        [{"id": "a", "name": "A"}, {"id": "a", "name": "B"}],
    ],
)
def test_schema(characters):
    with pytest.raises((ValueError, TypeError)):
        analyze({"characters": characters})


def test_invalid_allowed_ids():
    with pytest.raises((ValueError, TypeError)):
        analyze({"characters": [], "allowed_pairs": [["missing", "other"]]})
