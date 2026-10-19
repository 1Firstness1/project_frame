"""Тесты класса Event и функций работы с событиями."""

from models import Event
from models.events import add_event, find_events, sort_events_by_places


def test_event_creation():
    event = Event(1, "День рождения", "2026-10-15", 10)
    assert event.id == 1
    assert event.name == "День рождения"
    assert event.places == 10


def test_event_fits_places():
    event = Event(1, "День рождения", "2026-10-15", 10)
    assert event.fits_places(5)
    assert not event.fits_places(15)


def test_event_str():
    event = Event(1, "День рождения", "2026-10-15", 10)
    assert "День рождения" in str(event)


def test_add_event():
    events = []
    event = add_event(events, "Свадьба", "2026-11-01", 30)
    assert len(events) == 1
    assert event.name == "Свадьба"


def test_find_events():
    events = []
    add_event(events, "День рождения", "2026-10-15", 10)
    add_event(events, "Свадьба", "2026-11-01", 30)
    assert len(find_events(events, "день")) == 1


def test_sort_events_by_places():
    events = []
    add_event(events, "A", "2026-10-15", 50)
    add_event(events, "B", "2026-10-16", 20)
    sorted_events = sort_events_by_places(events)
    assert sorted_events[0].places == 20
