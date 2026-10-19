"""Тесты класса Status и функций работы со статусами."""

from models import Status
from models.statuses import (
    add_status,
    find_status_by_code,
    find_status_by_id,
    CODE_PENDING,
    CODE_CONFIRMED,
    CODE_DECLINED,
)


def test_status_creation():
    status = Status(1, CODE_PENDING, "ожидает")
    assert status.id == 1
    assert status.code == CODE_PENDING
    assert status.title == "ожидает"


def test_status_checks():
    pending = Status(1, CODE_PENDING, "ожидает")
    confirmed = Status(2, CODE_CONFIRMED, "подтверждено")
    declined = Status(3, CODE_DECLINED, "отклонено")
    assert pending.is_pending()
    assert confirmed.is_confirmed()
    assert declined.is_declined()


def test_validate_code():
    assert Status.validate_code(CODE_PENDING)
    assert not Status.validate_code("unknown")


def test_add_and_find_status():
    statuses = []
    add_status(statuses, CODE_CONFIRMED, "подтверждено")
    assert find_status_by_code(statuses, CODE_CONFIRMED) is not None
    assert find_status_by_id(statuses, 1) is not None


def test_status_str():
    status = Status(1, CODE_PENDING, "ожидает")
    assert "ожидает" in str(status)
