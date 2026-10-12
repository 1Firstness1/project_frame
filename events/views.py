"""View-функции приложения events."""

from django.http import HttpResponse

from homepage.views import page
from storage import load_events
from models.events import find_event_by_id


def events(request):
    """Страница со списком событий."""
    items = ""
    for event in load_events("data/events.json"):
        text = f"{event.name} | {event.date} | мест: {event.places}"
        items += (
            f'<li class="list-group-item d-flex '
            f'justify-content-between align-items-center">'
            f'<span>{text}</span>'
            f'<a class="btn btn-sm btn-outline-primary" '
            f'href="/events/{event.id}/">Подробнее</a>'
            f'</li>'
        )

    if not items:
        items = '<li class="list-group-item">События не найдены.</li>'

    content = f"""
    <h1>События</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("События", content))


def event_detail(request, event_id):
    """Страница отдельного события."""
    events_list = load_events("data/events.json")
    event = find_event_by_id(events_list, event_id)

    if event is None:
        content = """
        <h1 class="text-danger">Событие не найдено</h1>
        <a href="/events/" class="btn btn-outline-secondary">
            ← к списку событий
        </a>
        """
        return HttpResponse(
            page("Событие не найдено", content),
            status=404,
        )

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{event.name}</h5>
            <p class="card-text"><strong>ID:</strong> {event.id}</p>
            <p class="card-text"><strong>Дата:</strong> {event.date}</p>
            <p class="card-text">
                <strong>Мест:</strong> {event.places}
            </p>
            <a href="/events/" class="btn btn-outline-secondary">
                ← к списку событий
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(event.name, content))