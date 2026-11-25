from __future__ import annotations

import pytest

from utils import (
    filter_aeroplanes,
    get_aeroplanes_by_altitude,
    get_top_aeroplanes,
    print_aeroplanes,
    sort_aeroplanes,
)


def test_filter_aeroplanes(sample_aeroplanes):
    assert len(filter_aeroplanes(sample_aeroplanes, [])) == 3
    assert len(filter_aeroplanes(sample_aeroplanes, ["", "  "])) == 3
    filtered = filter_aeroplanes(sample_aeroplanes, ["spain"])
    assert len(filtered) == 2
    assert all(p.origin_country == "Spain" for p in filtered)


def test_get_aeroplanes_by_altitude(sample_aeroplanes):
    assert len(get_aeroplanes_by_altitude(sample_aeroplanes, "")) == 3
    ranged = get_aeroplanes_by_altitude(sample_aeroplanes, "9500 - 11000")
    assert [p.callsign for p in ranged] == ["AAA111"]
    ranged_swapped = get_aeroplanes_by_altitude(sample_aeroplanes, "11000 - 9500")
    assert [p.callsign for p in ranged_swapped] == ["AAA111"]


def test_get_aeroplanes_by_altitude_invalid(sample_aeroplanes):
    with pytest.raises(ValueError):
        get_aeroplanes_by_altitude(sample_aeroplanes, "100-")
    with pytest.raises(ValueError):
        get_aeroplanes_by_altitude(sample_aeroplanes, "a-b")


def test_sort_and_top(sample_aeroplanes):
    sorted_planes = sort_aeroplanes(sample_aeroplanes)
    assert [p.callsign for p in sorted_planes] == ["CCC333", "AAA111", "BBB222"]
    top = get_top_aeroplanes(sorted_planes, 2)
    assert len(top) == 2
    assert top[0].callsign == "CCC333"


def test_get_top_aeroplanes_invalid(sample_aeroplanes):
    with pytest.raises(ValueError):
        get_top_aeroplanes(sample_aeroplanes, 0)
    with pytest.raises(ValueError):
        get_top_aeroplanes(sample_aeroplanes, -1)
    with pytest.raises(ValueError):
        get_top_aeroplanes(sample_aeroplanes, "1")


def test_print_aeroplanes(capsys, sample_aeroplanes):
    print_aeroplanes([])
    assert "No aeroplanes found." in capsys.readouterr().out
    print_aeroplanes(sample_aeroplanes[:1])
    out = capsys.readouterr().out
    assert "AAA111" in out
