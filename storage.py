"""Загрузка и сохранение данных проекта в JSON с преобразованием в объекты."""

import json
import os
from typing import List

from models import Event, Guest, Status, Invitation
from models.events import find_event_by_id
from models.guests import find_guest_by_id
from models.statuses import find_status_by_id


def _read_json(filename: str) -> list:
    """Прочитать JSON-файл, вернуть пустой список при ошибке."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        print(f"Не удалось прочитать {filename}: {error}")
        return []


def _write_json(filename: str, data: list) -> None:
    """Записать данные в JSON-файл."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except OSError as error:
        print(f"Не удалось сохранить {filename}: {error}")


def load_events(filename: str) -> List[Event]:
    """Загрузить события из JSON и вернуть список объектов Event."""
    return [Event.from_data(item) for item in _read_json(filename)]


def save_events(filename: str, events: List[Event]) -> None:
    """Сохранить события в JSON."""
    _write_json(filename, [event.to_data() for event in events])


def load_guests(filename: str) -> List[Guest]:
    """Загрузить гостей из JSON и вернуть список объектов Guest."""
    return [Guest.from_data(item) for item in _read_json(filename)]


def save_guests(filename: str, guests: List[Guest]) -> None:
    """Сохранить гостей в JSON."""
    _write_json(filename, [guest.to_data() for guest in guests])


def load_statuses(filename: str) -> List[Status]:
    """Загрузить статусы из JSON и вернуть список объектов Status."""
    return [Status.from_data(item) for item in _read_json(filename)]


def save_statuses(filename: str, statuses: List[Status]) -> None:
    """Сохранить статусы в JSON."""
    _write_json(filename, [status.to_data() for status in statuses])


def load_invitations(
    filename: str,
    events: List[Event],
    guests: List[Guest],
    statuses: List[Status],
) -> List[Invitation]:
    """Загрузить приглашения и восстановить связи с Event, Guest, Status."""
    invitations: List[Invitation] = []
    for item in _read_json(filename):
        event = find_event_by_id(events, item["event_id"])
        guest = find_guest_by_id(guests, item["guest_id"])
        status = find_status_by_id(statuses, item["status_id"])
        if event is None or guest is None or status is None:
            continue
        invitations.append(Invitation.from_data(item, event, guest, status))
    return invitations


def save_invitations(filename: str, invitations: List[Invitation]) -> None:
    """Сохранить приглашения в JSON."""
    _write_json(filename, [invitation.to_data() for invitation in invitations])