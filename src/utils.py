"""Utility functions for filtering, sorting, and displaying aeroplanes."""

from __future__ import annotations

from models import Aeroplane


def filter_aeroplanes(
    aeroplanes: list[Aeroplane], filter_words: list[str]
) -> list[Aeroplane]:
    """Filter aeroplanes by origin country names."""
    if not filter_words:
        return list(aeroplanes)

    normalized = {
        word.strip().casefold()
        for word in filter_words
        if word and word.strip()
    }
    if not normalized:
        return list(aeroplanes)

    return [
        plane
        for plane in aeroplanes
        if plane.origin_country.casefold() in normalized
    ]


def _parse_altitude_range(altitude_range: str) -> tuple[float, float] | None:
    """Parse altitude range in format 'min - max'."""
    if not isinstance(altitude_range, str):
        return None
    text = altitude_range.strip()
    if not text:
        return None

    separator = "-" if "-" in text else "—"
    parts = [part.strip().replace(" ", "") for part in text.split(separator)]
    if len(parts) != 2 or not all(parts):
        raise ValueError("Altitude range must be in format: min - max")

    try:
        min_altitude = float(parts[0])
        max_altitude = float(parts[1])
    except ValueError as exc:
        raise ValueError("Altitude range values must be numbers.") from exc

    if min_altitude > max_altitude:
        min_altitude, max_altitude = max_altitude, min_altitude
    return min_altitude, max_altitude


def get_aeroplanes_by_altitude(
    aeroplanes: list[Aeroplane], altitude_range: str
) -> list[Aeroplane]:
    """Filter aeroplanes by barometric altitude range."""
    parsed = _parse_altitude_range(altitude_range)
    if parsed is None:
        return list(aeroplanes)

    min_altitude, max_altitude = parsed
    return [
        plane
        for plane in aeroplanes
        if min_altitude <= plane.baro_altitude <= max_altitude
    ]


def sort_aeroplanes(aeroplanes: list[Aeroplane]) -> list[Aeroplane]:
    """Sort aeroplanes by altitude descending, then by velocity descending."""
    return sorted(
        aeroplanes,
        key=lambda plane: (plane.baro_altitude, plane.velocity),
        reverse=True,
    )


def get_top_aeroplanes(
    aeroplanes: list[Aeroplane], top_n: int
) -> list[Aeroplane]:
    """Return top N aeroplanes."""
    if not isinstance(top_n, int) or top_n <= 0:
        raise ValueError("N must be a positive integer.")
    return list(aeroplanes[:top_n])


def print_aeroplanes(aeroplanes: list[Aeroplane]) -> None:
    """Print aeroplanes in a human-readable format."""
    if not aeroplanes:
        print("No aeroplanes found.")
        return

    for index, plane in enumerate(aeroplanes, start=1):
        print(f"{index}. {plane}")
