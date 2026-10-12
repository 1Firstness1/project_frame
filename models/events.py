"""Класс Event и функции работы с событиями."""

from __future__ import annotations
from typing import List, Optional

from utils import next_id


class Event:
    """Событие, на которое приглашаются гости."""

    def __init__(self, event_id: int, name: str, date: str, places: int) -> None:
        self.id = event_id
        self.name = name
        self.date = date
        self.places = places

    def fits_places(self, guests_count: int) -> bool:
        """Проверить, хватает ли мест для указанного числа гостей."""
        return self.places >= guests_count

    @staticmethod
    def validate_places(places: int) -> bool:
        """Проверить корректность числа мест."""
        return places > 0

    @classmethod
    def from_data(cls, data: dict) -> "Event":
        """Создать объект Event из словаря данных."""
        return cls(
            event_id=data["id"],
            name=data["name"],
            date=data["date"],
            places=data["places"],
        )

    def to_data(self) -> dict:
        """Преобразовать объект в словарь для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "places": self.places,
        }

    def __str__(self) -> str:
        return f"[{self.id}] {self.name} | {self.date} | мест: {self.places}"


def add_event(events: List[Event], name: str, date: str, places: int) -> Event:
    """Создать событие и добавить его в коллекцию."""
    event = Event(
        event_id=next_id([e.to_data() for e in events], "id"),
        name=name,
        date=date,
        places=places,
    )
    events.append(event)
    return event


def find_event_by_id(events: List[Event], event_id: int) -> Optional[Event]:
    """Найти событие по идентификатору."""
    for event in events:
        if event.id == event_id:
            return event
    return None


def find_events(events: List[Event], query: str) -> List[Event]:
    """Найти события по подстроке названия."""
    query_lower = query.lower()
    return [event for event in events if query_lower in event.name.lower()]


def filter_events_by_places(events: List[Event], min_places: int) -> List[Event]:
    """Отобрать события с числом мест не меньше min_places."""
    return [event for event in events if event.fits_places(min_places)]


def sort_events_by_places(events: List[Event]) -> List[Event]:
    """Отсортировать события по числу мест."""
    return sorted(events, key=lambda event: event.places)


def show_events(events: List[Event]) -> None:
    """Вывести список событий."""
    if not events:
        print("События не найдены.")
        return
    print("--- События ---")
    for event in events:
        print(event)