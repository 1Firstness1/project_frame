"""Класс Status и функции работы со статусами приглашений."""

from __future__ import annotations
from typing import List, Optional

from utils import next_id


CODE_PENDING = "pending"
CODE_CONFIRMED = "confirmed"
CODE_DECLINED = "declined"


class Status:
    """Статус приглашения (ожидает, подтверждено, отклонено)."""

    def __init__(self, status_id: int, code: str, title: str) -> None:
        self.id = status_id
        self.code = code
        self.title = title

    def is_confirmed(self) -> bool:
        """Проверить, означает ли статус подтверждение."""
        return self.code == CODE_CONFIRMED

    def is_pending(self) -> bool:
        """Проверить, означает ли статус ожидание."""
        return self.code == CODE_PENDING

    def is_declined(self) -> bool:
        """Проверить, означает ли статус отклонение."""
        return self.code == CODE_DECLINED

    @staticmethod
    def validate_code(code: str) -> bool:
        """Проверить, что код статуса входит в допустимый набор."""
        return code in (CODE_PENDING, CODE_CONFIRMED, CODE_DECLINED)

    @classmethod
    def from_data(cls, data: dict) -> "Status":
        """Создать объект Status из словаря данных."""
        return cls(
            status_id=data["id"],
            code=data["code"],
            title=data["title"],
        )

    def to_data(self) -> dict:
        """Преобразовать объект в словарь для JSON."""
        return {
            "id": self.id,
            "code": self.code,
            "title": self.title,
        }

    def __str__(self) -> str:
        return f"[{self.id}] {self.title} ({self.code})"


def add_status(statuses: List[Status], code: str, title: str) -> Status:
    """Создать статус и добавить его в коллекцию."""
    status = Status(
        status_id=next_id([s.to_data() for s in statuses], "id"),
        code=code,
        title=title,
    )
    statuses.append(status)
    return status


def find_status_by_id(statuses: List[Status], status_id: int) -> Optional[Status]:
    """Найти статус по идентификатору."""
    for status in statuses:
        if status.id == status_id:
            return status
    return None


def find_status_by_code(statuses: List[Status], code: str) -> Optional[Status]:
    """Найти статус по коду."""
    for status in statuses:
        if status.code == code:
            return status
    return None


def show_statuses(statuses: List[Status]) -> None:
    """Вывести список статусов."""
    if not statuses:
        print("Статусы не найдены.")
        return
    print("--- Статусы ---")
    for status in statuses:
        print(status)