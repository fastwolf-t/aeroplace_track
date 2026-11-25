# Aeroplanes by Country

Консольное приложение на Python для получения информации о самолетах в воздушном пространстве выбранной страны.

## Что делает проект

- Получает географические координаты страны через [Nominatim OpenStreetMap API](https://nominatim.org/release-docs/develop/api/Search/).
- Получает данные о самолетах в bounding box страны через [OpenSky Network API](https://openskynetwork.github.io/opensky-api/rest.html).
- Преобразует данные API в объекты `Aeroplane`.
- Сохраняет данные в JSON-файл.
- Позволяет фильтровать/сортировать самолеты и выводить топ N в консоль.

## Структура проекта

```text
.
├── data/
├── src/
│   ├── api.py        # Абстрактный и конкретный классы API
│   ├── main.py       # Точка входа и взаимодействие с пользователем
│   ├── models.py     # Класс Aeroplane
│   ├── storage.py    # Абстрактный storage и JSONSaver
│   └── utils.py      # Фильтрация, сортировка, вывод
├── tests/            # Pytest-тесты
├── pyproject.toml
└── todo.txt
```

## Установка

Требуется Python 3.10+.

```bash
python -m pip install requests pytest pytest-cov
```

## Запуск

```bash
python src/main.py
```

Программа запросит:

- название страны;
- количество самолетов для вывода в топ N;
- страны регистрации для фильтрации (через запятую, можно оставить пустым);
- диапазон высот полета, например `1000 - 12000`.

## Тесты

```bash
python -m pytest
```

С покрытием:

```bash
python -m pytest --cov=src --cov-report=term-missing
```

## Примечания

- OpenSky/Nominatim — внешние API, поэтому для реального запроса нужен интернет.
- В тестах сетевые вызовы замоканы.
