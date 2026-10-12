"""Тесты класса Guest и функций работы с гостями."""

from models import Guest
from models.guests import add_guest, find_guests, count_adults


def test_guest_creation():
    guest = Guest(1, "Иван Петров", 20)
    assert guest.id == 1
    assert guest.name == "Иван Петров"
    assert guest.age == 20


def test_guest_is_adult():
    adult = Guest(1, "Иван", 20)
    minor = Guest(2, "Петя", 15)
    assert adult.is_adult()
    assert not minor.is_adult()


def test_count_adults():
    guests = [Guest(1, "Иван", 17), Guest(2, "Мария", 25)]
    assert count_adults(guests) == 1


def test_add_guest():
    guests = []
    guest = add_guest(guests, "Иван", 20)
    assert len(guests) == 1
    assert guest.name == "Иван"


def test_find_guests():
    guests = []
    add_guest(guests, "Иван Петров", 20)
    add_guest(guests, "Мария Смирнова", 25)
    assert len(find_guests(guests, "иван")) == 1