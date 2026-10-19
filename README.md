# Сервис управления списком гостей

Учебное приложение для учёта событий, гостей и приглашений на Python с веб-интерфейсом на Django.
Консольная версия приложения (ПР3) сохранена и продолжает работать. Веб-интерфейс переведён на систему шаблонов Django Template Language (ПР6).

## 1. Назначение проекта

Сервис помогает организатору мероприятий вести список гостей, отслеживать статус приглашений и контролировать количество свободных мест.
Проект развивается поэтапно: консольная версия дополнена веб-интерфейсом и последовательно переводится на возможности Django.

## 2. Используемые технологии

- Python 3;
- Django 5.2;
- Django Template Language (DTL);
- HTML5;
- CSS3 и собственный файл стилей;
- JavaScript;
- Bootstrap 5.3;
- JSON для хранения данных;
- Git;
- pytest;
- flake8.

## 3. Предметная область

В системе используются четыре основные сущности:
- **Событие (Event)** — идентификатор, название, дата и лимит мест;
- **Гость (Guest)** — идентификатор, имя, возраст и проверка совершеннолетия;
- **Статус (Status)** — идентификатор, символьный код (`confirmed`, `pending`, `declined`) и название;
- **Приглашение (Invitation)** — идентификатор, связывает объект события, объект гостя и объект статуса.

Для предметной области реализованы собственные Python-классы в пакете `models/`.
На текущем этапе данные хранятся в JSON-файлах. Django ORM и база данных приложения пока не используются.

## 4. Структура проекта

```text
guest-list-service/
├── templates/
│   ├── includes/
│   │   └── navigation.html
│   ├── base.html
│   └── 404.html
│
├── homepage/
│   ├── static/
│   │   └── homepage/
│   │       ├── css/
│   │       │   └── style.css
│   │       ├── img/
│   │       │   └── logo.png
│   │       └── js/
│   │           └── main.js
│   ├── templates/
│   │   └── homepage/
│   │       └── index.html
│   ├── apps.py
│   ├── urls.py
│   └── views.py
│
├── events/
│   ├── templates/
│   │   └── events/
│   │       ├── includes/
│   │       │   └── event_card.html
│   │       ├── event_detail.html
│   │       └── event_list.html
│   ├── apps.py
│   ├── urls.py
│   └── views.py
│
├── guests/
│   ├── templates/
│   │   └── guests/
│   │       ├── includes/
│   │       │   └── guest_card.html
│   │       ├── guest_detail.html
│   │       ├── guest_invitations.html
│   │       └── guest_list.html
│   ├── apps.py
│   ├── urls.py
│   └── views.py
│
├── invitations/
│   ├── templates/
│   │   └── invitations/
│   │       ├── includes/
│   │       │   ├── invitation_card.html
│   │       │   └── invitation_status.html
│   │       ├── invitation_detail.html
│   │       └── invitation_list.html
│   ├── apps.py
│   ├── urls.py
│   └── views.py
│
├── guestlist/                     (пакет конфигурации Django-проекта)
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── models/                        (пакет предметной области из ПР3)
│   ├── __init__.py
│   ├── events.py
│   ├── guests.py
│   ├── statuses.py
│   └── invitations.py
│
├── data/
│   ├── events.json
│   ├── guests.json
│   ├── statuses.json
│   └── invitations.json
│
├── tests/                         (автоматизированные тесты pytest)
│   ├── test_events.py
│   ├── test_guests.py
│   ├── test_statuses.py
│   └── test_invitations.py
│
├── main.py                        (консольная версия из ПР3)
├── storage.py                     (модуль загрузки/сохранения JSON)
├── utils.py                       (вспомогательные функции)
├── manage.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## 5. Веб-интерфейс

Веб-часть приложения полностью переведена на Django-шаблоны.
Основные страницы:
- Главная страница (`/`);
- Список событий (`/events/`);
- Страница отдельного события (`/events/<int:event_id>/`);
- Список гостей (`/guests/`);
- Страница отдельного гостя (`/guests/<int:guest_id>/`);
- Список приглашений выбранного гостя (`/guests/<int:guest_id>/invitations/`);
- Список приглашений (`/invitations/`);
- Страница отдельного приглашения (`/invitations/<int:invitation_id>/`);
- Пользовательская страница ошибки 404.

Генерация HTML непосредственно в Python-коде не используется (функция `page()` удалена).
Представления подготавливают данные и передают их в шаблоны через словарь контекста.

## 6. Django Template Language

### Базовый шаблон
Общий шаблон страниц — `templates/base.html`.
Он содержит общую HTML-структуру страницы, подключение Bootstrap, подключение собственных стилей `style.css`, логотипа `logo.png`, навигации `navigation.html`, подвала с автоматической установкой года через `main.js` и блоки для содержимого отдельных страниц:
- `{% block title %}` — заголовок страницы;
- `{% block content %}` — основное содержимое.

Дочерние шаблоны используют наследование:
```html
{% extends "base.html" %}
```

### Включаемые шаблоны
Повторяющиеся фрагменты вынесены во включаемые шаблоны:
- `templates/includes/navigation.html` — общая навигация сайта;
- `events/templates/events/includes/event_card.html` — карточка события;
- `guests/templates/guests/includes/guest_card.html` — карточка гостя;
- `invitations/templates/invitations/includes/invitation_card.html` — карточка приглашения в списке;
- `invitations/templates/invitations/includes/invitation_status.html` — цветной бейдж статуса приглашения.

Подключение выполняется тегом `{% include "..." %}`.

### Контекст
Представления передают данные в шаблоны через словарь `context`.
Например, во view:
```python
context = {"events": events_list}
return render(request, "events/event_list.html", context)
```
В шаблоне данные доступны по именам ключей словаря: `{{ events }}`.

### Циклы и условия
Для формирования списков используются циклы `{% for %}` с веткой отсутствия данных `{% empty %}`:
```html
{% for event in events %}
    {% include "events/includes/event_card.html" %}
{% empty %}
    <p>События не найдены.</p>
{% endfor %}
```
Условия `{% if %}` используются для отображения статусов, проверки совершеннолетия гостя и обработки отсутствия объектов на детальных страницах.

## 7. Фильтры шаблонов

В шаблонах применяются стандартные фильтры Django:
- `{{ events|length }}` — подсчёт общего количества элементов в списке;
- `{{ event.name|default:"Без названия" }}` — вывод значения по умолчанию при отсутствии имени.

Фильтры используются исключительно для форматирования представления и не содержат бизнес-логику.

## 8. URL-маршрутизация и пространства имён

Для всех приложений настроены пространства имён (`app_name`):
- `homepage` (`homepage:index`);
- `events` (`events:list`, `events:detail`);
- `guests` (`guests:list`, `guests:detail`, `guests:invitations`);
- `invitations` (`invitations:list`, `invitations:detail`).

Ссылки в шаблонах формируются исключительно через тег `{% url %}`, например:
```html
<a href="{% url 'events:list' %}">События</a>
<a href="{% url 'events:detail' event.id %}">Подробнее</a>
```

## 9. Статические файлы

Статические файлы проекта размещены в приложении `homepage`:
`homepage/static/homepage/`
- `css/style.css` — собственные стили для карточек (`.event-card`, `.guest-card`, `.invitation-card`), логотипа (`.guestlist-logo`) и бейджей;
- `js/main.js` — клиентский скрипт, автоматически устанавливающий текущий год в футере;
- `img/logo.png` — графический логотип проекта.

Для подключения статики в базовом шаблоне используется `{% load static %}` и теги `{% static "..." %}`.

## 10. Хранение данных

Данные приложения по-прежнему хранятся в JSON-файлах:
- `data/events.json`;
- `data/guests.json`;
- `data/statuses.json`;
- `data/invitations.json`.

Загрузка данных выполняется функциями модуля `storage.py`. Предметные объекты создаются на основе классов каталога `models/`.
Django ORM на текущем этапе не используется.

## 11. Запуск проекта

Веб-версия (Django):
```text
python manage.py runserver
```
После запуска веб-интерфейс доступен по адресу:
`http://127.0.0.1:8000/`

Консольная версия:
```text
python main.py
```

## 12. Тестирование и качество кода

Запуск автоматических тестов:
```text
pytest -v
```

Системная проверка Django:
```text
python manage.py check
```

Проверка соответствия PEP 8 (flake8):
```text
flake8 . --extend-exclude=.venv
```

## 13. Текущее состояние и дальнейшее развитие

Реализовано в ПР6:
- Веб-интерфейс полностью переведён на Django-шаблоны;
- Создан базовый каркас `templates/base.html`;
- Организовано наследование шаблонов (`extends`) и блоки (`block`);
- Вынесены включаемые шаблоны (`include`);
- Настроена передача данных через контекст;
- Использованы циклы (`for`), ветки `empty` и условия (`if`);
- Настроены именованные маршруты и пространства имён (`app_name`);
- Применены фильтры шаблонов (`length`, `default`);
- Подключены собственные статические файлы (CSS, JS, логотип);
- Сохранена полная работоспособность консольной версии и тестов ПР3.

Планируется на следующих этапах:
- Переход от JSON-файлов к реляционной базе данных и Django ORM;
- Формы создания, изменения и удаления объектов;
- Аутентификация и разграничение прав пользователей;
- Разработка REST API;
- Контейнеризация и настройка CI/CD.