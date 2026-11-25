from __future__ import annotations

from unittest.mock import patch

from main import user_interaction


def test_user_interaction_happy_path(monkeypatch, capsys, tmp_path):
    inputs = iter(["Spain", "1", "Spain", "9000 - 11000"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    api_data = [
        {
            "icao24": "a1",
            "callsign": "AAA111",
            "origin_country": "Spain",
            "velocity": 250.0,
            "baro_altitude": 10000.0,
        },
        {
            "icao24": "a2",
            "callsign": "BBB222",
            "origin_country": "France",
            "velocity": 260.0,
            "baro_altitude": 10500.0,
        },
    ]

    with patch("main.AeroplanesAPI") as mock_api_cls, patch("main.JSONSaver") as mock_saver_cls:
        mock_api_cls.return_value.get_aeroplanes.return_value = api_data
        mock_saver = mock_saver_cls.return_value
        user_interaction()

    out = capsys.readouterr().out
    assert "AAA111" in out
    assert "BBB222" not in out
    assert mock_saver.add_aeroplane.call_count == 2


def test_user_interaction_invalid_n(monkeypatch, capsys):
    inputs = iter(["Spain", "abc", "", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    user_interaction()
    assert "N must be an integer." in capsys.readouterr().out


def test_user_interaction_empty_country(monkeypatch, capsys):
    inputs = iter(["   "])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    user_interaction()
    assert "Country name cannot be empty." in capsys.readouterr().out
