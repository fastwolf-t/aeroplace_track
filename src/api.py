"""Abstract base classes and implementations for external APIs."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import requests


class BaseAPI(ABC):
    """Abstract base class for API integrations."""

    @abstractmethod
    def connect(self) -> bool:
        """Check whether the API is reachable."""

    @abstractmethod
    def get_country_coordinates(self, country_name: str) -> dict[str, float]:
        """Get country bounding box coordinates."""

    @abstractmethod
    def get_aeroplanes(self, country_name: str) -> list[dict[str, Any]]:
        """Get aeroplanes within the country's bounding box."""


class AeroplanesAPI(BaseAPI):
    """API client for nominatim.openstreetmap.org and opensky-network.org."""

    NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
    OPENSKY_URL = "https://opensky-network.org/api/states/all"

    def __init__(self, timeout: int = 20) -> None:
        self.timeout = timeout
        self.aeroplanes: list[dict[str, Any]] = []

    def connect(self) -> bool:
        """Check whether required APIs respond successfully."""
        try:
            nominatim_response = requests.get(
                self.NOMINATIM_URL,
                params={
                    "q": "Spain",
                    "format": "json",
                    "limit": "1",
                },
                headers={"User-Agent": "aeroplane-course-project/1.0"},
                timeout=self.timeout,
            )

            opensky_response = requests.get(
                self.OPENSKY_URL,
                params={
                    "lamin": 0.0,
                    "lomin": 0.0,
                    "lamax": 1.0,
                    "lomax": 1.0,
                },
                timeout=self.timeout,
            )

            return (
                nominatim_response.status_code == 200
                and opensky_response.status_code == 200
            )

        except requests.RequestException:
            return False

    def get_country_coordinates(self, country_name: str) -> dict[str, float]:
        """Get south, north, west, and east coordinates for a country."""
        if not isinstance(country_name, str) or not country_name.strip():
            raise ValueError("Country name must be a non-empty string.")

        try:
            response = requests.get(
                self.NOMINATIM_URL,
                params={
                    "q": country_name.strip(),
                    "format": "json",
                    "limit": "1",
                },
                headers={"User-Agent": "aeroplane-course-project/1.0"},
                timeout=self.timeout,
            )

            response.raise_for_status()
            data = response.json()

        except requests.RequestException as exc:
            raise ConnectionError(
                f"Failed to fetch country coordinates: {exc}"
            ) from exc

        except ValueError as exc:
            raise ValueError("Invalid response from Nominatim API.") from exc

        if not data:
            raise ValueError(f"Country not found: {country_name}")

        bounding_box = data[0].get("boundingbox")

        if not bounding_box or len(bounding_box) != 4:
            raise ValueError("Bounding box is missing in Nominatim response.")

        try:
            south, north, west, east = [float(value) for value in bounding_box]

        except (TypeError, ValueError) as exc:
            raise ValueError("Invalid bounding box values.") from exc

        return {
            "south": south,
            "north": north,
            "west": west,
            "east": east,
        }

    def get_aeroplanes(self, country_name: str) -> list[dict[str, Any]]:
        """Get aeroplane state vectors in the specified country's area."""
        coordinates = self.get_country_coordinates(country_name)

        params: dict[str, float] = {
            "lamin": coordinates["south"],
            "lamax": coordinates["north"],
            "lomin": coordinates["west"],
            "lomax": coordinates["east"],
        }

        try:
            response = requests.get(
                self.OPENSKY_URL,
                params=params,
                timeout=self.timeout,
            )

            response.raise_for_status()
            data = response.json()

        except requests.RequestException as exc:
            raise ConnectionError(
                f"Failed to fetch aeroplane data: {exc}"
            ) from exc

        except ValueError as exc:
            raise ValueError("Invalid response from OpenSky API.") from exc

        states = data.get("states") or []
        aeroplanes: list[dict[str, Any]] = []

        for state in states:
            aeroplanes.append(
                {
                    "icao24": state[0],
                    "callsign": state[1],
                    "origin_country": state[2],
                    "time_position": state[3],
                    "last_contact": state[4],
                    "longitude": state[5],
                    "latitude": state[6],
                    "baro_altitude": state[7],
                    "on_ground": state[8],
                    "velocity": state[9],
                    "true_track": state[10],
                    "vertical_rate": state[11],
                    "geo_altitude": state[13],
                }
            )

        self.aeroplanes = aeroplanes
        return aeroplanes
