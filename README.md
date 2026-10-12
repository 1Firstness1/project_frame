# Сервис управления списком гостей

Веб-приложение на Django для учёта событий, гостей, статусов
приглашений и самих приглашений. Консольная версия (ПР3) сохранена
и продолжает работать.

## Используемые технологии

- Python 3;
- Django 5.2;
- HTML, CSS, Bootstrap 5.3;
- pytest, flake8.

## Назначение

Приложение помогает организатору мероприятия вести список гостей,
отслеживать статус приглашений и контролировать количество
свободных мест на событии.

## Целевая аудитория

Организаторы частных и корпоративных мероприятий: дни рождения,
свадьбы, конференции, встречи команд.

## Предметная область

Управление приглашениями на событие: учёт гостей, подтверждение
участия, контроль лимита мест.

## Основные сущности (ПР3)

### Event — событие
Атрибуты: `id`, `name`, `date`, `places`.
Методы: `fits_places()`, `validate_places()` (`@staticmethod`),
`from_data()` (`@classmethod`), `to_data()`, `__str__()`.

### Guest — гость

Атрибуты: `id`, `name`, `age`.

Методы: `is_adult()`, `validate_age()` (`@staticmethod`),
`from_data()`, `to_data()`, `__str__()`.

### Status — статус приглашения

Атрибуты: `id`, `code`, `title`.

Методы: `is_confirmed()`, `is_pending()`, `is_declined()`,
`validate_code()` (`@staticmethod`), `from_data()`, `to_data()`,
`__str__()`.

Допустимые коды: `pending`, `confirmed`, `declined`.

### Invitation — приглашение

Связывает `Event`, `Guest` и `Status`.

Атрибуты: `id`, `event`, `guest`, `status`.

Методы: `confirm()`, `decline()`, `reset()`, `is_confirmed()`,
`is_pending()`, `is_declined()`, `from_data()`, `to_data()`,
`__str__()`.

## Возможности веб-интерфейса

- просмотр списка событий и карточки события;
- просмотр списка гостей и карточки гостя;
- просмотр приглашений выбранного гостя;
- просмотр списка приглашений и карточки приглашения;
- отображение статуса приглашения цветным бейджем;
- пользовательская страница 404.

## Страницы и URL

| Страница | URL | View |
|---|---|---|
| Главная | `/` | `homepage.views.index` |
| События | `/events/` | `events.views.events` |
| Событие | `/events/<int:event_id>/` | `events.views.event_detail` |
| Гости | `/guests/` | `guests.views.guests` |
| Гость | `/guests/<int:guest_id>/` | `guests.views.guest_detail` |
| Приглашения гостя | `/guests/<int:guest_id>/invitations/` | `guests.views.guest_invitations` |
| Приглашения | `/invitations/` | `invitations.views.invitations` |
| Приглашение | `/invitations/<int:invitation_id>/` | `invitations.views.invitation_detail` |

## Структура проекта

```text
guest-list-service/
├── README.md
├── requirements.txt
├── .gitignore
├── manage.py
├── main.py                    (консольная версия из ПР3)
├── storage.py                 (из ПР3)
├── utils.py                   (из ПР3)
├── models/                    (пакет предметной области из ПР3)
│   ├── __init__.py
│   ├── events.py
│   ├── guests.py
│   ├── statuses.py
│   └── invitations.py
├── data/
│   ├── events.json
│   ├── guests.json
│   ├── statuses.json
│   └── invitations.json
├── tests/                     (тесты ПР3)
│   ├── test_events.py
│   ├── test_guests.py
│   ├── test_statuses.py
│   └── test_invitations.py
├── guestlist/                 (Django-проект)
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── homepage/                  (Django-приложение)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── events/                    (Django-приложение)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── guests/                    (Django-приложение)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── invitations/               (Django-приложение)
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── migrations/
    ├── models.py
    ├── tests.py
    ├── urls.py
    └── views.py
```

## Хранение данных

- `data/events.json`;
- `data/guests.json`;
- `data/statuses.json`;
- `data/invitations.json`.

При загрузке JSON преобразуется в объекты `Event`, `Guest`, `Status`,
`Invitation` (ПР3). Веб-слой использует функции `storage.py` и
`models/*.py`, не дублируя предметную логику.

## Запуск веб-версии

```text
python manage.py migrate
python manage.py runserver
```

Откройте `http://127.0.0.1:8000/`.

## Запуск консольной версии

```text
python main.py
```

## Тесты

```text
pytest -v
```

## Проверка качества кода

```text
flake8 . --extend-exclude=venv
```

## План развития

- перенос сущностей в Django ORM и подключение базы данных;
- переход на Django-шаблоны (`templates/`) и отказ от функции `page()`;
- формы создания и редактирования событий, гостей и приглашений;
- пользователи и аутентификация;
- REST API;
- контейнеризация и CI/CD.