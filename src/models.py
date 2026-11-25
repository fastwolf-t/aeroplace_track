"""Aeroplane domain model."""

from __future__ import annotations

from typing import Any


class Aeroplane:
    """Represents an aeroplane with validated flight attributes."""

    __slots__ = (
        "_icao24",
        "_callsign",
        "_origin_country",
        "_velocity",
        "_baro_altitude",
        "_geo_altitude",
        "_longitude",
        "_latitude",
        "_on_ground",
    )

    def __init__(
        self,
        callsign: str | None,
        origin_country: str | None,
        velocity: float | int | None,
        baro_altitude: float | int | None,
        icao24: str | None = None,
        geo_altitude: float | int | None = None,
        longitude: float | int | None = None,
        latitude: float | int | None = None,
        on_ground: bool | None = None,
    ) -> None:
        self._icao24 = self._validate_text(icao24, "icao24", allow_empty=True)
        self._callsign = self._validate_text(callsign, "callsign")
        self._origin_country = self._validate_text(
            origin_country, "origin_country"
        )
        self._velocity = self._validate_number(
            velocity, "velocity", min_value=0
        )
        self._baro_altitude = self._validate_number(
            baro_altitude, "baro_altitude"
        )
        self._geo_altitude = self._validate_optional_number(
            geo_altitude, "geo_altitude"
        )
        self._longitude = self._validate_optional_number(
            longitude, "longitude"
        )
        self._latitude = self._validate_optional_number(latitude, "latitude")
        self._on_ground = bool(on_ground) if on_ground is not None else False

    @staticmethod
    def _validate_text(
        value: Any, field_name: str, allow_empty: bool = False
    ) -> str:
        if value is None:
            return "Unknown" if not allow_empty else ""
        if not isinstance(value, str):
            value = str(value)
        cleaned = value.strip()
        if not cleaned and not allow_empty:
            return "Unknown"
        return cleaned

    @staticmethod
    def _validate_number(
        value: Any, field_name: str, min_value: float | None = None
    ) -> float:
        if value is None or value == "":
            return 0.0
        try:
            number = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{field_name} must be a number.") from exc
        if min_value is not None and number < min_value:
            return float(min_value)
        return number

    @staticmethod
    def _validate_optional_number(value: Any, field_name: str) -> float | None:
        if value is None or value == "":
            return None
        try:
            return float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"{field_name} must be a number or None."
            ) from exc

    @property
    def icao24(self) -> str:
        return self._icao24

    @property
    def callsign(self) -> str:
        return self._callsign

    @property
    def origin_country(self) -> str:
        return self._origin_country

    @property
    def velocity(self) -> float:
        return self._velocity

    @property
    def baro_altitude(self) -> float:
        return self._baro_altitude

    @property
    def geo_altitude(self) -> float | None:
        return self._geo_altitude

    @property
    def longitude(self) -> float | None:
        return self._longitude

    @property
    def latitude(self) -> float | None:
        return self._latitude

    @property
    def on_ground(self) -> bool:
        return self._on_ground

    def _comparison_value(self, other: object) -> "Aeroplane":
        if not isinstance(other, Aeroplane):
            raise TypeError(
                "Comparison is supported only between Aeroplane objects."
            )
        return other

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return (self.velocity, self.baro_altitude) == (
            other.velocity,
            other.baro_altitude,
        )

    def __lt__(self, other: object) -> bool:
        other_plane = self._comparison_value(other)
        return (self.velocity, self.baro_altitude) < (
            other_plane.velocity,
            other_plane.baro_altitude,
        )

    def __le__(self, other: object) -> bool:
        other_plane = self._comparison_value(other)
        return (self.velocity, self.baro_altitude) <= (
            other_plane.velocity,
            other_plane.baro_altitude,
        )

    def __gt__(self, other: object) -> bool:
        other_plane = self._comparison_value(other)
        return (self.velocity, self.baro_altitude) > (
            other_plane.velocity,
            other_plane.baro_altitude,
        )

    def __ge__(self, other: object) -> bool:
        other_plane = self._comparison_value(other)
        return (self.velocity, self.baro_altitude) >= (
            other_plane.velocity,
            other_plane.baro_altitude,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert the aeroplane to a serializable dictionary."""
        return {
            "icao24": self.icao24,
            "callsign": self.callsign,
            "origin_country": self.origin_country,
            "velocity": self.velocity,
            "baro_altitude": self.baro_altitude,
            "geo_altitude": self.geo_altitude,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "on_ground": self.on_ground,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Aeroplane":
        """Create an Aeroplane from a dictionary."""
        if not isinstance(data, dict):
            raise TypeError("Aeroplane data must be a dictionary.")
        return cls(
            callsign=data.get("callsign"),
            origin_country=data.get("origin_country"),
            velocity=data.get("velocity"),
            baro_altitude=data.get("baro_altitude"),
            icao24=data.get("icao24"),
            geo_altitude=data.get("geo_altitude"),
            longitude=data.get("longitude"),
            latitude=data.get("latitude"),
            on_ground=data.get("on_ground"),
        )

    @classmethod
    def cast_to_object_list(
        cls, data: list[dict[str, Any]]
    ) -> list["Aeroplane"]:
        """Convert a list of dictionaries to a list of Aeroplane objects."""
        if not isinstance(data, list):
            raise TypeError("Aeroplanes data must be a list.")
        return [cls.from_dict(item) for item in data]

    def __str__(self) -> str:
        return (
            f"{self.callsign} ({self.origin_country}) | "
            f"velocity={self.velocity} m/s | altitude={self.baro_altitude} m"
        )

    def __repr__(self) -> str:
        return (
            f"Aeroplane(callsign={self.callsign!r}, "
            f"origin_country={self.origin_country!r}, "
            f"velocity={self.velocity!r}, "
            f"baro_altitude={self.baro_altitude!r})"
        )
