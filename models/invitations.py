"""Класс Invitation и функции работы с приглашениями."""

from __future__ import annotations
from typing import List, Optional

from utils import next_id
from .events import Event
from .guests import Guest
from .statuses import Status


class Invitation:
    """Приглашение гостя на событие."""

    def __init__(
        self, invitation_id: int, event: Event, guest: Guest, status: Status
    ) -> None:
        self.id = invitation_id
        self.event = event
        self.guest = guest
        self.status = status

    def confirm(self, confirmed_status: Status) -> None:
        """Подтвердить приглашение, установив статус 'подтверждено'."""
        self.status = confirmed_status

    def decline(self, declined_status: Status) -> None:
        """Отклонить приглашение, установив статус 'отклонено'."""
        self.status = declined_status

    def reset(self, pending_status: Status) -> None:
        """Вернуть приглашение в статус 'ожидает'."""
        self.status = pending_status

    def is_confirmed(self) -> bool:
        """Проверить, подтверждено ли приглашение."""
        return self.status.is_confirmed()

    def is_pending(self) -> bool:
        """Проверить, ожидает ли приглашение."""
        return self.status.is_pending()

    def is_declined(self) -> bool:
        """Проверить, отклонено ли приглашение."""
        return self.status.is_declined()

    @classmethod
    def from_data(
        cls, data: dict, event: Event, guest: Guest, status: Status
    ) -> "Invitation":
        """Создать объект Invitation из данных JSON и связанных объектов."""
        return cls(
            invitation_id=data["id"],
            event=event,
            guest=guest,
            status=status,
        )

    def to_data(self) -> dict:
        """Преобразовать объект в словарь для JSON."""
        return {
            "id": self.id,
            "event_id": self.event.id,
            "guest_id": self.guest.id,
            "status_id": self.status.id,
        }

    def __str__(self) -> str:
        return (
            f"[{self.id}] {self.guest.name} -> {self.event.name} "
            f"({self.status.title})"
        )


def get_invitation_status(is_confirmed: bool) -> str:
    """Вернуть текстовый статус приглашения (функция из ПР1)."""
    if is_confirmed:
        return "Приглашение подтверждено"
    return "Приглашение ожидает подтверждения"


def is_guest_invited(
    invitations: List[Invitation], event: Event, guest: Guest
) -> bool:
    """Проверить, приглашён ли гость на событие."""
    for invitation in invitations:
        if invitation.event is event and invitation.guest is guest:
            return True
    return False


def create_invitation(
    invitations: List[Invitation], event: Event, guest: Guest, status: Status
) -> Optional[Invitation]:
    """Создать приглашение, если гостя ещё нет в списке события."""
    if is_guest_invited(invitations, event, guest):
        return None
    invitation = Invitation(
        invitation_id=next_id([i.to_data() for i in invitations], "id"),
        event=event,
        guest=guest,
        status=status,
    )
    invitations.append(invitation)
    return invitation


def find_invitation_by_id(
    invitations: List[Invitation], invitation_id: int
) -> Optional[Invitation]:
    """Найти приглашение по идентификатору."""
    for invitation in invitations:
        if invitation.id == invitation_id:
            return invitation
    return None


def confirm_invitation(
    invitations: List[Invitation], invitation_id: int, confirmed_status: Status
) -> bool:
    """Подтвердить приглашение по идентификатору."""
    invitation = find_invitation_by_id(invitations, invitation_id)
    if invitation is None:
        return False
    invitation.confirm(confirmed_status)
    return True


def decline_invitation(
    invitations: List[Invitation], invitation_id: int, declined_status: Status
) -> bool:
    """Отклонить приглашение по идентификатору."""
    invitation = find_invitation_by_id(invitations, invitation_id)
    if invitation is None:
        return False
    invitation.decline(declined_status)
    return True


def cancel_invitation(
    invitations: List[Invitation], invitation_id: int
) -> bool:
    """Отменить приглашение (удалить из коллекции)."""
    invitation = find_invitation_by_id(invitations, invitation_id)
    if invitation is None:
        return False
    invitations.remove(invitation)
    return True


def count_confirmed(invitations: List[Invitation], event: Event) -> int:
    """Посчитать подтверждённые приглашения на событие."""
    return sum(
        1
        for invitation in invitations
        if invitation.event is event and invitation.is_confirmed()
    )


def find_invitations_by_event(
    invitations: List[Invitation], event: Event
) -> List[Invitation]:
    """Вернуть список приглашений на событие."""
    return [inv for inv in invitations if inv.event is event]


def show_invitations(invitations: List[Invitation]) -> None:
    """Вывести список приглашений."""
    if not invitations:
        print("Приглашения не найдены.")
        return
    print("--- Приглашения ---")
    for invitation in invitations:
        print(invitation)
