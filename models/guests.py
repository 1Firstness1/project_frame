"""Функции работы с гостями."""

from utils import next_id


def add_guest(guests: list[dict], name: str, age: int) -> None:
    """Добавить гостя в список guests."""
    guest = {
        "guest_id": next_id(guests, "guest_id"),
        "name": name,
        "age": age,
    }
    guests.append(guest)

def can_add_guest(current_guests, places):
    if current_guests < places:
        return True
    return False

def find_guest(guests: list[dict], query: str) -> list[dict]:
    """Найти гостей по подстроке имени."""
    query_lower = query.lower()
    return [guest for guest in guests if query_lower in guest["name"].lower()]


def sort_guests_by_age(guests: list[dict]) -> list[dict]:
    """Отсортировать гостей по возрасту."""
    return sorted(guests, key=lambda guest: guest["age"])


def count_adults(guests: list[dict]) -> int:
    """Посчитать количество совершеннолетних гостей."""
    return sum(1 for guest in guests if guest["age"] >= 18)


def find_guest_by_id(guests: list[dict], guest_id: int) -> dict | None:
    """Найти гостя по идентификатору."""
    for guest in guests:
        if guest["guest_id"] == guest_id:
            return guest
    return None
