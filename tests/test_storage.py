from __future__ import annotations

import json

import pytest

from models import Aeroplane
from storage import JSONSaver


def test_json_saver_add_and_get(json_file):
    saver = JSONSaver(str(json_file))
    plane = Aeroplane("CALL1", "Spain", 250, 10000, icao24="a1")
    saver.add_aeroplane(plane)
    saver.add_aeroplane(plane)  # duplicate

    data = saver.get_aeroplanes()
    assert len(data) == 1
    assert data[0]["callsign"] == "CALL1"

    filtered = saver.get_aeroplanes({"origin_country": "Spain"})
    assert len(filtered) == 1
    assert saver.get_aeroplanes({"origin_country": "France"}) == []


def test_json_saver_delete(json_file):
    saver = JSONSaver(str(json_file))
    saver.add_aeroplane(Aeroplane("A", "Spain", 100, 1000, icao24="1"))
    saver.add_aeroplane(Aeroplane("B", "France", 100, 1000, icao24="2"))

    deleted = saver.delete_aeroplanes({"origin_country": "Spain"})
    assert deleted == 1
    assert len(saver.get_aeroplanes()) == 1

    deleted_all = saver.delete_aeroplanes()
    assert deleted_all == 1
    assert saver.get_aeroplanes() == []


def test_json_saver_type_errors(json_file):
    saver = JSONSaver(str(json_file))
    with pytest.raises(TypeError):
        saver.add_aeroplane({"not": "aeroplane"})
    with pytest.raises(TypeError):
        saver.get_aeroplanes("bad")
    with pytest.raises(TypeError):
        saver.delete_aeroplanes("bad")


def test_json_saver_handles_bad_file(tmp_path):
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{broken", encoding="utf-8")
    saver = JSONSaver(str(bad_file))
    assert saver.get_aeroplanes() == []

    bad_file.write_text(json.dumps({"not": "list"}), encoding="utf-8")
    assert saver.get_aeroplanes() == []


def test_delete_aeroplane_by_object(json_file):
    saver = JSONSaver(str(json_file))
    plane = Aeroplane("CALL1", "Spain", 250, 10000, icao24="a1")
    saver.add_aeroplane(plane)
    assert saver.delete_aeroplane(plane) == 1
    assert saver.get_aeroplanes() == []
