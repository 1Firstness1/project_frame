"""Функции работы с приглашениями."""

from utils import next_id

STATUS_PENDING = "ожидает"
STATUS_CONFIRMED = "подтверждено"


def get_invitation_status(is_confirmed: bool) -> str:
    """Вернуть текстовый статус приглашения (функция из ПР1)."""
    if is_confirmed:
        return "Приглашение подтверждено"
    return "Приглашение ожидает подтверждения"


def is_guest_invited(
    invitations: list[dict], event_id: int, guest_id: int
) -> bool:
    """Проверить, приглашён ли гость на событие."""
    for invitation in invitations:
        if (
            invitation["event_id"] == event_id
            and invitation["guest_id"] == guest_id
        ):
            return True
    return False


def create_invitation(
    invitations: list[dict], event_id: int, guest_id: int
) -> dict | None:
    """Создать приглашение, если гостя ещё нет в списке события."""
    if is_guest_invited(invitations, event_id, guest_id):
        return None
    invitation = {
        "invitation_id": next_id(invitations, "invitation_id"),
        "event_id": event_id,
        "guest_id": guest_id,
        "status": STATUS_PENDING,
    }
    invitations.append(invitation)
    return invitation


def confirm_invitation(
    invitations: list[dict], invitation_id: int
) -> bool:
    """Подтвердить приглашение по идентификатору."""
    for invitation in invitations:
        if invitation["invitation_id"] == invitation_id:
            invitation["status"] = STATUS_CONFIRMED
            return True
    return False


def cancel_invitation(
    invitations: list[dict], invitation_id: int
) -> bool:
    """Отменить (удалить) приглашение по идентификатору."""
    for invitation in invitations:
        if invitation["invitation_id"] == invitation_id:
            invitations.remove(invitation)
            return True
    return False


def count_confirmed(invitations: list[dict], event_id: int) -> int:
    """Посчитать подтверждённые приглашения на событие."""
    return sum(
        1
        for invitation in invitations
        if invitation["event_id"] == event_id
        and invitation["status"] == STATUS_CONFIRMED
    )


def find_invitations_by_event(
    invitations: list[dict], event_id: int
) -> list[dict]:
    """Вернуть список приглашений на событие."""
    return [
        invitation
        for invitation in invitations
        if invitation["event_id"] == event_id
    ]


def build_guest_card(name, age, is_confirmed, current_guests, places):
    status = get_invitation_status(is_confirmed)

    if age < 18:
        age_note = "Гость несовершеннолетний — нужен сопровождающий"
    else:
        age_note = "Гость совершеннолетний"

    return (
        f"Гость: {name}\n"
        f"Возраст: {age}\n"
        f"Статус: {status}\n"
        f"Примечание: {age_note}\n"
    )
