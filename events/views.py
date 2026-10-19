"""View-функции приложения events."""

from django.shortcuts import render

from models.events import find_event_by_id
from storage import load_events


def events(request):
    """Страница со списком событий."""
    events_list = load_events("data/events.json")
    context = {
        "events": events_list,
    }
    return render(request, "events/event_list.html", context)


def event_detail(request, event_id):
    """Страница отдельного события."""
    events_list = load_events("data/events.json")
    event = find_event_by_id(events_list, event_id)
    context = {
        "event": event,
    }
    return render(
        request,
        "events/event_detail.html",
        context,
        status=404 if event is None else 200,
    )
