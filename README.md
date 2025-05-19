# barter_platform

**barter_platform** — это веб-приложение на Django для организации обмена вещами между пользователями.

---

## Функциональность

- Регистрация и вход пользователей
- Создание и удаление объявлений
- Фильтрация по категории, состоянию и ключевым словам
- Пагинация (4 строки × 4 карточки)
- Отправка и получение предложений обмена
- Подтверждение/отклонение предложений
- REST API с авто-документацией (Swagger)
- Unit-тесты: модели, формы, представления
- Адаптивный интерфейс (карточки, фильтры)

---

## Установка и запуск

```bash
# 1. Клонируй проект
git clone https://github.com/KiT0LiT0/barter_platform.git
cd barter_platform

# 2. Создай и активируй виртуальное окружение
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Установи зависимости
pip install "Django>=4.0"
pip install "djangorestframework>=3.13"
pip install drf-spectacular
pip install pytest

# 4. Примени миграции
python manage.py migrate

# 5. Запусти сервер
python manage.py runserver
```

---

## Тестирование

```bash
python manage.py test
```

Тестируются:
- Views: отображение, создание, удаление, защита
- Forms: валидация `AdForm` и `ExchangeProposalForm`
- Models: базовая логика моделей

---

## API-документация

- Swagger UI: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
- OpenAPI JSON: [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)

Документация сгенерирована через `drf-spectacular` и описывает все доступные эндпоинты API, включая фильтрацию, сериализаторы и права доступа.

---

## Структура проекта

```text
ads/
├── models.py            # Модели Ad, ExchangeProposal
├── views.py             # Представления
├── serializers.py       # DRF-сериализаторы
├── forms.py             # Django-формы
├── templates/           # HTML-шаблоны
├── urls.py              # Маршруты
├── tests/
│   ├── test_views.py
│   ├── test_forms.py
│   └── test_models.py (опционально)
```

---

## Используемые технологии

- Python 3.11
- Django 5.2
- Django REST Framework
- drf-spectacular
- SQLite (по умолчанию)
- HTML / CSS (Django Templates)
- Git / GitHub

---

## Лицензия

MIT License