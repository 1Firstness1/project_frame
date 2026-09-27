"""Функции работы с событиями."""

from utils import next_id


def add_event(
    events: list[dict], name: str, event_date: str, places: int
) -> None:
    """Добавить событие в список events."""
    event = {
        "event_id": next_id(events, "event_id"),
        "name": name,
        "date": event_date,
        "places": places,
    }
    events.append(event)


def find_event(events: list[dict], query: str) -> list[dict]:
    """Найти события по подстроке названия."""
    query_lower = query.lower()
    return [event for event in events if query_lower in event["name"].lower()]


def filter_events_by_places(
    events: list[dict], min_places: int
) -> list[dict]:
    """Отобрать события с числом мест не меньше min_places."""
    return [event for event in events if event["places"] >= min_places]


def sort_events_by_places(events: list[dict]) -> list[dict]:
    """Отсортировать события по числу мест по возрастанию."""
    return sorted(events, key=lambda event: event["places"])


def find_event_by_id(events: list[dict], event_id: int) -> dict | None:
    """Найти событие по идентификатору."""
    for event in events:
        if event["event_id"] == event_id:
            return event
    return None
