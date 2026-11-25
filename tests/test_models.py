from __future__ import annotations

import pytest

from models import Aeroplane


def test_aeroplane_init_and_properties():
    plane = Aeroplane("CALL1", "Spain", 250.5, 10000, icao24="abc", geo_altitude=10100)
    assert plane.callsign == "CALL1"
    assert plane.origin_country == "Spain"
    assert plane.velocity == 250.5
    assert plane.baro_altitude == 10000.0
    assert plane.icao24 == "abc"
    assert plane.geo_altitude == 10100.0
    assert plane.on_ground is False


def test_aeroplane_defaults_and_validation():
    plane = Aeroplane(None, None, None, None)
    assert plane.callsign == "Unknown"
    assert plane.origin_country == "Unknown"
    assert plane.velocity == 0.0
    assert plane.baro_altitude == 0.0
    assert plane.icao24 == ""

    plane2 = Aeroplane("A", "B", -10, -5)
    assert plane2.velocity == 0.0
    assert plane2.baro_altitude == -5.0


def test_aeroplane_invalid_numbers():
    with pytest.raises(ValueError):
        Aeroplane("A", "B", "fast", 100)
    with pytest.raises(ValueError):
        Aeroplane("A", "B", 100, "high")


def test_aeroplane_comparisons():
    low = Aeroplane("A", "X", 100, 5000)
    high = Aeroplane("B", "Y", 200, 6000)
    same_as_low = Aeroplane("C", "Z", 100, 5000)

    assert low < high
    assert low <= high
    assert high > low
    assert high >= low
    assert low == same_as_low
    assert (low == "not-plane") is False
    with pytest.raises(TypeError):
        _ = low < 1


def test_aeroplane_to_from_dict():
    data = {
        "icao24": "abc",
        "callsign": "CALL1",
        "origin_country": "Spain",
        "velocity": 250.0,
        "baro_altitude": 10000.0,
        "geo_altitude": 10100.0,
        "longitude": 1.0,
        "latitude": 2.0,
        "on_ground": False,
    }
    plane = Aeroplane.from_dict(data)
    assert plane.to_dict() == data


def test_aeroplane_from_dict_invalid():
    with pytest.raises(TypeError):
        Aeroplane.from_dict(["not", "dict"])


def test_cast_to_object_list():
    data = [
        {"callsign": "A", "origin_country": "ES", "velocity": 1, "baro_altitude": 2},
        {"callsign": "B", "origin_country": "FR", "velocity": 3, "baro_altitude": 4},
    ]
    planes = Aeroplane.cast_to_object_list(data)
    assert len(planes) == 2
    assert all(isinstance(p, Aeroplane) for p in planes)
    with pytest.raises(TypeError):
        Aeroplane.cast_to_object_list({"not": "list"})


def test_str_repr():
    plane = Aeroplane("CALL1", "Spain", 250, 10000)
    assert "CALL1" in str(plane)
    assert "Spain" in str(plane)
    assert "Aeroplane" in repr(plane)
