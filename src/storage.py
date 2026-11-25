"""Abstract and concrete file storage for aeroplanes."""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from models import Aeroplane


class BaseStorage(ABC):
    """Abstract storage interface for aeroplane data."""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Add an aeroplane to storage."""

    @abstractmethod
    def get_aeroplanes(
        self, criteria: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """Get aeroplanes matching criteria."""

    @abstractmethod
    def delete_aeroplanes(self, criteria: dict[str, Any] | None = None) -> int:
        """Delete aeroplanes matching criteria and return deleted count."""


class JSONSaver(BaseStorage):
    """JSON file storage for aeroplanes."""

    def __init__(self, filename: str = "data/aeroplanes.json") -> None:
        self._path = Path(filename)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if not self._path.exists():
            self._write_data([])

    @property
    def path(self) -> Path:
        return self._path

    def _read_data(self) -> list[dict[str, Any]]:
        try:
            with self._path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []
        if not isinstance(data, list):
            return []
        return [item for item in data if isinstance(item, dict)]

    def _write_data(self, data: list[dict[str, Any]]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    @staticmethod
    def _matches(
        item: dict[str, Any], criteria: dict[str, Any] | None
    ) -> bool:
        if not criteria:
            return True
        for key, value in criteria.items():
            if item.get(key) != value:
                return False
        return True

    @staticmethod
    def _identity(item: dict[str, Any]) -> tuple[Any, ...]:
        return (
            item.get("icao24"),
            item.get("callsign"),
            item.get("origin_country"),
            item.get("velocity"),
            item.get("baro_altitude"),
            item.get("longitude"),
            item.get("latitude"),
        )

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Add an aeroplane if it is not already stored."""
        if not isinstance(aeroplane, Aeroplane):
            raise TypeError("aeroplane must be an Aeroplane instance.")

        data = self._read_data()
        new_item = aeroplane.to_dict()
        new_identity = self._identity(new_item)
        if any(self._identity(item) == new_identity for item in data):
            return
        data.append(new_item)
        self._write_data(data)

    def get_aeroplanes(
        self, criteria: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """Return aeroplanes matching all criteria key-value pairs."""
        if criteria is not None and not isinstance(criteria, dict):
            raise TypeError("criteria must be a dictionary or None.")
        data = self._read_data()
        return [item for item in data if self._matches(item, criteria)]

    def delete_aeroplanes(self, criteria: dict[str, Any] | None = None) -> int:
        """Delete matching aeroplanes. If criteria is None, clear storage."""
        if criteria is not None and not isinstance(criteria, dict):
            raise TypeError("criteria must be a dictionary or None.")

        data = self._read_data()
        if criteria is None:
            deleted = len(data)
            self._write_data([])
            return deleted

        remaining = [
            item for item in data if not self._matches(item, criteria)
        ]
        deleted = len(data) - len(remaining)
        if deleted:
            self._write_data(remaining)
        return deleted

    def delete_aeroplane(self, aeroplane: Aeroplane | dict[str, Any]) -> int:
        """Delete a single aeroplane by object or criteria dict."""
        if isinstance(aeroplane, Aeroplane):
            criteria = aeroplane.to_dict()
        elif isinstance(aeroplane, dict):
            criteria = aeroplane
        else:
            raise TypeError("aeroplane must be an Aeroplane instance or dict.")
        return self.delete_aeroplanes(criteria)
