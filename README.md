# Сервис управления списком гостей

Учебное приложение для учёта событий, гостей и приглашений на Python с веб-интерфейсом на Django и слоем реляционной базы данных SQLite (ПР7).
Консольная версия приложения (ПР3), JSON-хранилище и веб-интерфейс на Django Templates (ПР6) сохранены и продолжают работать.

## 1. Назначение проекта

Сервис помогает организатору мероприятий вести список гостей, отслеживать статус приглашений и контролировать количество свободных мест на событиях.
Проект развивается поэтапно: консольная версия дополнена веб-интерфейсом и последовательно переводится на возможности реляционной базы данных и Django.

## 2. Используемые технологии

- Python 3;
- SQLite3 и стандартная библиотека `sqlite3`;
- SQL (DDL, DML, DQL);
- Django 5.2;
- Django Template Language (DTL);
- HTML5, CSS3, Bootstrap 5.3, JavaScript;
- JSON для исходного хранения данных;
- Git;
- pytest;
- flake8.

## 3. Предметная область и структура базы данных

В системе используются четыре основные сущности:
1. **События (`events`)**:
   - `id` (INTEGER, PRIMARY KEY) — идентификатор события;
   - `name` (TEXT, NOT NULL) — название события;
   - `date` (TEXT, NOT NULL) — дата проведения (формат `YYYY-MM-DD`);
   - `places` (INTEGER, NOT NULL) — количество мест.
2. **Гости (`guests`)**:
   - `id` (INTEGER, PRIMARY KEY) — идентификатор гостя;
   - `name` (TEXT, NOT NULL) — имя гостя;
   - `age` (INTEGER, NOT NULL) — возраст.
3. **Статусы (`statuses`)**:
   - `id` (INTEGER, PRIMARY KEY) — идентификатор статуса;
   - `code` (TEXT, NOT NULL, UNIQUE) — символьный код (`pending`, `confirmed`, `declined`);
   - `title` (TEXT, NOT NULL) — название статуса.
4. **Приглашения (`invitations`)**:
   - `id` (INTEGER, PRIMARY KEY) — идентификатор приглашения;
   - `event_id` (INTEGER, NOT NULL, FOREIGN KEY -> `events.id`);
   - `guest_id` (INTEGER, NOT NULL, FOREIGN KEY -> `guests.id`);
   - `status_id` (INTEGER, NOT NULL, FOREIGN KEY -> `statuses.id`).

Внешние ключи гарантируют ссылочную целостность данных: проверка включена при каждом подключении через команду `PRAGMA foreign_keys = ON;`.

## 4. Структура проекта

```text
guest-list-service/
├── data/
│   ├── events.json
│   ├── guests.json
│   ├── statuses.json
│   ├── invitations.json
│   └── guestlist.sqlite           (файл реляционной базы данных SQLite)
│
├── sql/
│   ├── schema.sql                 (DDL-скрипт создания таблиц и внешних ключей)
│   └── queries.sql                (набор из 12 проверенных SQL-запросов)
│
├── db/
│   ├── __init__.py
│   ├── database.py                (модуль подключения get_connection)
│   └── import_json.py             (скрипт переноса данных из JSON в SQLite)
│
├── templates/
│   ├── includes/
│   │   └── navigation.html
│   ├── base.html
│   └── 404.html
│
├── homepage/
│   ├── static/
│   ├── templates/
│   ├── urls.py
│   └── views.py
│
├── events/
│   ├── templates/
│   │   └── events/
│   │       ├── includes/
│   │       │   └── event_card.html
│   │       ├── event_detail.html
│   │       ├── event_list.html
│   │       ├── event_search.html  (поиск событий по параметрам)
│   │       └── statistics.html    (страница статистики)
│   ├── urls.py
│   └── views.py                   (SQL-запросы к SQLite с sqlite3.Row)
│
├── guests/
│   ├── templates/
│   │   └── guests/
│   │       ├── includes/
│   │       │   └── guest_card.html
│   │       ├── guest_detail.html
│   │       ├── guest_invitations.html
│   │       └── guest_list.html
│   ├── urls.py
│   └── views.py                   (SQL-запросы к SQLite)
│
├── invitations/
│   ├── templates/
│   │   └── invitations/
│   │       ├── includes/
│   │       │   ├── invitation_card.html
│   │       │   └── invitation_status.html
│   │       ├── invitation_detail.html
│   │       └── invitation_list.html
│   ├── urls.py
│   └── views.py                   (JOIN-запросы к SQLite)
│
├── guestlist/                     (пакет конфигурации Django-проекта)
├── models/                        (классы предметной области из ПР3)
├── tests/                         (автоматизированные тесты pytest)
├── main.py                        (консольная версия из ПР3)
├── storage.py                     (модуль загрузки/сохранения JSON)
├── utils.py                       (вспомогательные функции)
├── manage.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## 5. Слой работы с базой данных (ПР7)

1. **Создание схемы**:
   Файл `sql/schema.sql` содержит команды `CREATE TABLE IF NOT EXISTS` с ограничениями `PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`, `UNIQUE`.
2. **Подключение к базе**:
   Модуль `db/database.py` предоставляет функцию `get_connection()`, которая открывает соединение с `data/guestlist.sqlite` и включает проверку внешних ключей `PRAGMA foreign_keys = ON;`.
3. **Импорт данных из JSON**:
   Скрипт `db/import_json.py` выполняет однократный или повторный перенос данных из `data/*.json` в SQLite с помощью `executemany()` и параметризованных вставок `VALUES (?, ?, ...)`, с защитой транзакции (`commit()` / `rollback()`).
   Запуск:
   ```text
   python -m db.import_json
   ```
4. **SQL-запросы проекта**:
   В `sql/queries.sql` зафиксировано 12 запросов, покрывающих все требуемые категории:
   - Простая выборка (`SELECT`, `ORDER BY`);
   - Фильтрация (`WHERE`);
   - Многотабличные соединения (`JOIN`);
   - Подзапросы (`NOT IN`);
   - Агрегатные функции (`COUNT`, `MIN`, `MAX`, `AVG`);
   - Группировка (`GROUP BY` и `LEFT JOIN`);
   - Фильтрация групп (`HAVING`).
5. **Интеграция с Django**:
   Представления приложений `events`, `guests`, `invitations` получают данные из SQLite через соединение с `conn.row_factory = sqlite3.Row`, что позволяет обращаться к полям по именам столбцов и алиасов (`{{ event.name }}`, `{{ invitation.guest_name }}`).

## 6. Веб-интерфейс и страницы

- `/` — главная страница проекта;
- `/events/` — список событий из SQLite;
- `/events/<int:event_id>/` — карточка события;
- `/events/search/` — параметризованный поиск событий по минимальной вместимости (`WHERE places >= ?`);
- `/events/statistics/` — сводная статистика по событиям и приглашениям (`LEFT JOIN`, `GROUP BY`);
- `/guests/` — список гостей из SQLite;
- `/guests/<int:guest_id>/` — карточка гостя;
- `/guests/<int:guest_id>/invitations/` — список приглашений гостя (выборка с `JOIN`);
- `/invitations/` — список приглашений (объединение `invitations`, `events`, `guests`, `statuses`);
- `/invitations/<int:invitation_id>/` — детальная страница приглашения.

## 7. Запуск проекта

Импорт данных в SQLite (при необходимости пересоздания базы):
```text
python -m db.import_json
```

Запуск веб-сервера Django:
```text
python manage.py runserver
```
Веб-интерфейс доступен по адресу: `http://127.0.0.1:8000/`

Консольная версия:
```text
python main.py
```

## 8. Тестирование и качество кода

- Системная проверка Django:
  ```text
  python manage.py check
  ```
- Запуск тестов:
  ```text
  pytest -v
  ```
- Проверка PEP 8:
  ```text
  flake8 . --extend-exclude=.venv
  ```

## 9. Текущее состояние и дальнейшее развитие

Реализовано в ПР7:
- Спроектирована реляционная база данных `guestlist.sqlite`;
- Разработана схема таблиц `sql/schema.sql` с внешними ключами;
- Реализован скрипт импорта `db/import_json.py`;
- Написаны и протестированы 12 SQL-запросов в `sql/queries.sql`;
- Django-представления переведены на получение данных из SQLite через `sqlite3.Row`;
- Реализованы сценарии поиска по параметрам и страницы статистики;
- Сохранена полная совместимость с ПР1–ПР6 (JSON, ООП-модели, тесты).

Планируется на следующих этапах:
- Переход к Django ORM и моделям Django;
- Использование миграций Django вместо прямых SQL-скриптов;
- Создание веб-форм для добавления и изменения данных через POST-запросы.