from __future__ import annotations

from unittest.mock import Mock, patch

import pytest
import requests

from api import AeroplanesAPI


def make_response(json_data=None, status_code=200, raise_exc=None):
    response = Mock()
    response.status_code = status_code
    response.json.return_value = json_data
    if raise_exc:
        response.raise_for_status.side_effect = raise_exc
    else:
        response.raise_for_status.return_value = None
    return response


def test_connect_success():
    api = AeroplanesAPI()
    with patch("api.requests.get", side_effect=[make_response([]), make_response({})]):
        assert api.connect() is True


def test_connect_failure():
    api = AeroplanesAPI()
    with patch("api.requests.get", side_effect=requests.RequestException("boom")):
        assert api.connect() is False


def test_get_country_coordinates_success():
    api = AeroplanesAPI()
    nominatim_data = [{"boundingbox": ["27.0", "44.0", "-18.0", "4.0"]}]
    with patch("api.requests.get", return_value=make_response(nominatim_data)):
        coords = api.get_country_coordinates("Spain")
    assert coords == {"south": 27.0, "north": 44.0, "west": -18.0, "east": 4.0}


@pytest.mark.parametrize("name", ["", "   ", None, 123])
def test_get_country_coordinates_invalid_name(name):
    api = AeroplanesAPI()
    with pytest.raises(ValueError):
        api.get_country_coordinates(name)


def test_get_country_coordinates_not_found():
    api = AeroplanesAPI()
    with patch("api.requests.get", return_value=make_response([])):
        with pytest.raises(ValueError, match="Country not found"):
            api.get_country_coordinates("Narnia")


def test_get_country_coordinates_request_error():
    api = AeroplanesAPI()
    with patch("api.requests.get", side_effect=requests.RequestException("net")):
        with pytest.raises(ConnectionError):
            api.get_country_coordinates("Spain")


def test_get_aeroplanes_success():
    api = AeroplanesAPI()
    coords = {"south": 1.0, "north": 2.0, "west": 3.0, "east": 4.0}
    opensky_data = {
        "states": [
            [
                "abc123",
                "CALL1  ",
                "Spain",
                1,
                2,
                3.5,
                4.5,
                10000.0,
                False,
                250.0,
                90.0,
                1.2,
                None,
                10100.0,
            ]
        ]
    }
    with patch.object(api, "get_country_coordinates", return_value=coords):
        with patch("api.requests.get", return_value=make_response(opensky_data)) as mock_get:
            result = api.get_aeroplanes("Spain")
    assert len(result) == 1
    assert result[0]["callsign"] == "CALL1  "
    assert result[0]["origin_country"] == "Spain"
    assert result[0]["velocity"] == 250.0
    assert result[0]["baro_altitude"] == 10000.0
    assert api.aeroplanes == result
    mock_get.assert_called_once()


def test_get_aeroplanes_empty_states():
    api = AeroplanesAPI()
    coords = {"south": 1.0, "north": 2.0, "west": 3.0, "east": 4.0}
    with patch.object(api, "get_country_coordinates", return_value=coords):
        with patch("api.requests.get", return_value=make_response({"states": None})):
            assert api.get_aeroplanes("Spain") == []


def test_get_aeroplanes_request_error():
    api = AeroplanesAPI()
    coords = {"south": 1.0, "north": 2.0, "west": 3.0, "east": 4.0}
    with patch.object(api, "get_country_coordinates", return_value=coords):
        with patch("api.requests.get", side_effect=requests.RequestException("net")):
            with pytest.raises(ConnectionError):
                api.get_aeroplanes("Spain")
