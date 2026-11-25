# зеркало PyPI
# python3 -m poetry source remove tsinghua
# python3 -m poetry source add --priority=primary tsinghua
# #https://pypi.tuna.tsinghua.edu.cn/simple/
# python3 -m poetry install

"""Main user interaction flow."""

from __future__ import annotations

from api import AeroplanesAPI
from models import Aeroplane
from storage import JSONSaver
from utils import (
    filter_aeroplanes,
    get_aeroplanes_by_altitude,
    get_top_aeroplanes,
    print_aeroplanes,
    sort_aeroplanes,
)


def _parse_filter_words(raw_value: str) -> list[str]:
    if not raw_value.strip():
        return []
    return [word.strip() for word in raw_value.split(",") if word.strip()]


def user_interaction() -> None:
    """Interact with the user through console."""
    try:
        country = input("Введите название страны: ").strip()
        if not country:
            print("Country name cannot be empty.")
            return

        top_n_raw = input(
            "Введите количество самолетов для вывода в топ N: "
        ).strip()
        try:
            top_n = int(top_n_raw)
        except ValueError:
            print("N must be an integer.")
            return

        filter_words_raw = input(
            "Введите названия стран для фильтрации "
            "по стране регистрации (через запятую): "
        )
        filter_words = _parse_filter_words(filter_words_raw)

        altitude_range = input("Введите диапазон высот полета: ").strip()

        api = AeroplanesAPI()
        aeroplanes_data = api.get_aeroplanes(country)
        aeroplanes = Aeroplane.cast_to_object_list(aeroplanes_data)

        saver = JSONSaver()
        for plane in aeroplanes:
            saver.add_aeroplane(plane)

        filtered_aeroplanes = filter_aeroplanes(aeroplanes, filter_words)
        ranged_aeroplanes = get_aeroplanes_by_altitude(
            filtered_aeroplanes, altitude_range
        )
        sorted_aeroplanes = sort_aeroplanes(ranged_aeroplanes)
        top_aeroplanes = get_top_aeroplanes(sorted_aeroplanes, top_n)
        print_aeroplanes(top_aeroplanes)
    except ValueError as exc:
        print(f"Input error: {exc}")
    except ConnectionError as exc:
        print(f"API error: {exc}")
    except Exception as exc:  # pragma: no cover - defensive fallback
        print(f"Unexpected error: {exc}")


if __name__ == "__main__":
    user_interaction()
