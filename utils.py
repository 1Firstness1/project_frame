"""Вспомогательные функции ввода с обработкой ошибок."""

from datetime import date, datetime


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число.")


def input_date(prompt: str) -> date:
    """Запросить у пользователя дату в формате ДД.ММ.ГГГГ."""
    while True:
        try:
            return datetime.strptime(input(prompt), "%d.%m.%Y").date()
        except ValueError:
            print("Ошибка: используйте формат ДД.ММ.ГГГГ.")


def next_id(items: list[dict], key: str) -> int:
    """Вернуть следующий свободный идентификатор для коллекции."""
    if not items:
        return 1
    return max(item[key] for item in items) + 1
