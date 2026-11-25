from __future__ import annotations

from pathlib import Path

import pytest

from models import Aeroplane


@pytest.fixture
def sample_aeroplanes() -> list[Aeroplane]:
    return [
        Aeroplane("AAA111", "Spain", 250.0, 10000.0, icao24="abc1"),
        Aeroplane("BBB222", "France", 300.0, 9000.0, icao24="abc2"),
        Aeroplane("CCC333", "Spain", 200.0, 12000.0, icao24="abc3"),
    ]


@pytest.fixture
def json_file(tmp_path: Path) -> Path:
    return tmp_path / "aeroplanes.json"
