"""View-функции приложения guests."""

from django.http import HttpResponse

from homepage.views import page
from storage import (
    load_events,
    load_guests,
    load_statuses,
    load_invitations,
)
from models.guests import find_guest_by_id


def guests(request):
    """Страница со списком гостей."""
    items = ""
    for guest in load_guests("data/guests.json"):
        text = f"{guest.name}, возраст: {guest.age}"
        items += (
            f'<li class="list-group-item d-flex '
            f'justify-content-between align-items-center">'
            f'<span>{text}</span>'
            f'<a class="btn btn-sm btn-outline-primary" '
            f'href="/guests/{guest.id}/">Подробнее</a>'
            f'</li>'
        )

    if not items:
        items = '<li class="list-group-item">Гости не найдены.</li>'

    content = f"""
    <h1>Гости</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Гости", content))


def guest_detail(request, guest_id):
    """Страница отдельного гостя."""
    guests_list = load_guests("data/guests.json")
    guest = find_guest_by_id(guests_list, guest_id)

    if guest is None:
        content = """
        <h1 class="text-danger">Гость не найден</h1>
        <a href="/guests/" class="btn btn-outline-secondary">
            ← к списку гостей
        </a>
        """
        return HttpResponse(
            page("Гость не найден", content),
            status=404,
        )

    if guest.is_adult():
        badge = "bg-success"
        adult = "совершеннолетний"
    else:
        badge = "bg-warning text-dark"
        adult = "несовершеннолетний"

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{guest.name}</h5>
            <p class="card-text"><strong>ID:</strong> {guest.id}</p>
            <p class="card-text"><strong>Возраст:</strong> {guest.age}</p>
            <p class="card-text">
                Статус:
                <span class="badge {badge}">{adult}</span>
            </p>
            <a href="/guests/" class="btn btn-outline-secondary">
                ← к списку гостей
            </a>
            <a href="/guests/{guest.id}/invitations/"
               class="btn btn-outline-primary">
                Приглашения гостя
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(guest.name, content))


def guest_invitations(request, guest_id):
    """Страница приглашений выбранного гостя."""
    guests_list = load_guests("data/guests.json")
    events_list = load_events("data/events.json")
    statuses_list = load_statuses("data/statuses.json")
    invitations_list = load_invitations(
        "data/invitations.json",
        events_list,
        guests_list,
        statuses_list,
    )

    guest = find_guest_by_id(guests_list, guest_id)
    if guest is None:
        content = """
        <h1 class="text-danger">Гость не найден</h1>
        <a href="/guests/" class="btn btn-outline-secondary">
            ← к списку гостей
        </a>
        """
        return HttpResponse(
            page("Гость не найден", content),
            status=404,
        )

    rows = ""
    for inv in invitations_list:
        if inv.guest is guest:
            rows += (
                f"<tr>"
                f"<td>{inv.event.name}</td>"
                f"<td>{inv.event.date}</td>"
                f"<td>{inv.status.title}</td>"
                f"</tr>"
            )

    if not rows:
        rows = (
            '<tr><td colspan="3" class="text-center">'
            "Приглашений нет.</td></tr>"
        )

    content = f"""
    <h1>Приглашения гостя: {guest.name}</h1>
    <table class="table table-striped">
        <thead>
            <tr>
                <th>Событие</th>
                <th>Дата</th>
                <th>Статус</th>
            </tr>
        </thead>
        <tbody>{rows}</tbody>
    </table>
    <a href="/guests/" class="btn btn-outline-secondary">
        ← к списку гостей
    </a>
    """
    return HttpResponse(
        page(f"Приглашения: {guest.name}", content)
    )