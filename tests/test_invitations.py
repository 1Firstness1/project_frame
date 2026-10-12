"""Тесты класса Invitation и функций работы с приглашениями."""

from models import Event, Guest, Status
from models.statuses import CODE_PENDING, CODE_CONFIRMED, CODE_DECLINED
from models.invitations import (
    create_invitation,
    confirm_invitation,
    decline_invitation,
    cancel_invitation,
    is_guest_invited,
    count_confirmed,
)


def make_event():
    return Event(1, "День рождения", "2026-10-15", 10)


def make_guest():
    return Guest(1, "Иван Петров", 25)


def make_statuses():
    return {
        "pending": Status(1, CODE_PENDING, "ожидает"),
        "confirmed": Status(2, CODE_CONFIRMED, "подтверждено"),
        "declined": Status(3, CODE_DECLINED, "отклонено"),
    }


def test_invitation_creation():
    event = make_event()
    guest = make_guest()
    statuses = make_statuses()
    invitation = create_invitation([], event, guest, statuses["pending"])
    assert invitation is not None
    assert invitation.event is event
    assert invitation.guest is guest
    assert invitation.status is statuses["pending"]


def test_duplicate_invitation_forbidden():
    event = make_event()
    guest = make_guest()
    statuses = make_statuses()
    invitations = []
    create_invitation(invitations, event, guest, statuses["pending"])
    result = create_invitation(invitations, event, guest, statuses["pending"])
    assert result is None
    assert len(invitations) == 1


def test_confirm_invitation():
    event = make_event()
    guest = make_guest()
    statuses = make_statuses()
    invitations = []
    invitation = create_invitation(
        invitations, event, guest, statuses["pending"]
    )
    assert confirm_invitation(
        invitations, invitation.id, statuses["confirmed"]
    )
    assert count_confirmed(invitations, event) == 1
    assert invitation.is_confirmed()


def test_decline_invitation():
    event = make_event()
    guest = make_guest()
    statuses = make_statuses()
    invitations = []
    invitation = create_invitation(
        invitations, event, guest, statuses["pending"]
    )
    assert decline_invitation(
        invitations, invitation.id, statuses["declined"]
    )
    assert invitation.is_declined()


def test_cancel_invitation():
    event = make_event()
    guest = make_guest()
    statuses = make_statuses()
    invitations = []
    invitation = create_invitation(
        invitations, event, guest, statuses["pending"]
    )
    assert cancel_invitation(invitations, invitation.id)
    assert not is_guest_invited(invitations, event, guest)


def test_invitation_str():
    event = make_event()
    guest = make_guest()
    statuses = make_statuses()
    invitation = create_invitation(
        [], event, guest, statuses["pending"]
    )
    text = str(invitation)
    assert "Иван Петров" in text
    assert "День рождения" in text