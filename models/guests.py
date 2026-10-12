"""Класс Guest и функции работы с гостями."""

from __future__ import annotations
from typing import List, Optional

from utils import next_id


class Guest:
    """Гость мероприятия."""

    def __init__(self, guest_id: int, name: str, age: int) -> None:
        self.id = guest_id
        self.name = name
        self.age = age

    def is_adult(self) -> bool:
        """Проверить, является ли гость совершеннолетним."""
        return self.age >= 18

    @staticmethod
    def validate_age(age: int) -> bool:
        """Проверить корректность возраста."""
        return 0 < age < 120

    @classmethod
    def from_data(cls, data: dict) -> "Guest":
        """Создать объект Guest из словаря данных."""
        return cls(
            guest_id=data["id"],
            name=data["name"],
            age=data["age"],
        )

    def to_data(self) -> dict:
        """Преобразовать объект в словарь для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
        }

    def __str__(self) -> str:
        return f"[{self.id}] {self.name}, возраст: {self.age}"


def add_guest(guests: List[Guest], name: str, age: int) -> Guest:
    """Создать гостя и добавить его в коллекцию."""
    guest = Guest(
        guest_id=next_id([g.to_data() for g in guests], "id"),
        name=name,
        age=age,
    )
    guests.append(guest)
    return guest


def find_guest_by_id(guests: List[Guest], guest_id: int) -> Optional[Guest]:
    """Найти гостя по идентификатору."""
    for guest in guests:
        if guest.id == guest_id:
            return guest
    return None


def find_guests(guests: List[Guest], query: str) -> List[Guest]:
    """Найти гостей по подстроке имени."""
    query_lower = query.lower()
    return [guest for guest in guests if query_lower in guest.name.lower()]


def count_adults(guests: List[Guest]) -> int:
    """Посчитать количество совершеннолетних гостей."""
    return sum(1 for guest in guests if guest.is_adult())


def sort_guests_by_age(guests: List[Guest]) -> List[Guest]:
    """Отсортировать гостей по возрасту."""
    return sorted(guests, key=lambda guest: guest.age)


def show_guests(guests: List[Guest]) -> None:
    """Вывести список гостей."""
    if not guests:
        print("Гости не найдены.")
        return
    print("--- Гости ---")
    for guest in guests:
        print(guest)