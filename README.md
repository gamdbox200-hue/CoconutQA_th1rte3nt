# CoconutQA — автотесты для API Cinescope

Проект автотестов на Python (Pytest) для тестирования API сервиса Cinescope.

## Технологии
- Python 3.12
- Pytest
- Requests
- Faker

## Структура проекта
- `api/` — API-классы (AuthAPI, UserAPI, ApiManager)
- `custom_requester/` — кастомный враппер над requests
- `tests/api/` — тесты API
- `utils/` — генераторы тестовых данных
- `constants.py` — константы и эндпоинты

## Запуск тестов
```bash
pip install -r requirements.txt
pytest -v