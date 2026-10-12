"""View-функции приложения invitations."""

from django.http import HttpResponse

from homepage.views import page
from storage import (
    load_events,
    load_guests,
    load_statuses,
    load_invitations,
)
from models.invitations import find_invitation_by_id


def _load_all():
    """Загрузить все связанные коллекции предметной области."""
    events = load_events("data/events.json")
    guests = load_guests("data/guests.json")
    statuses = load_statuses("data/statuses.json")
    invitations = load_invitations(
        "data/invitations.json", events, guests, statuses
    )
    return events, guests, statuses, invitations


def invitations(request):
    """Страница со списком приглашений."""
    _, _, _, invitations_list = _load_all()

    items = ""
    for inv in invitations_list:
        if inv.is_confirmed():
            badge = "bg-success"
        else:
            badge = "bg-secondary"
        items += (
            f'<li class="list-group-item d-flex '
            f'justify-content-between align-items-center">'
            f'<span>{inv.guest.name} → {inv.event.name}</span>'
            f'<span class="badge {badge}">{inv.status.title}</span>'
            f'<a class="btn btn-sm btn-outline-primary" '
            f'href="/invitations/{inv.id}/">Подробнее</a>'
            f'</li>'
        )

    if not items:
        items = (
            '<li class="list-group-item">Приглашения не найдены.</li>'
        )

    content = f"""
    <h1>Приглашения</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Приглашения", content))


def invitation_detail(request, invitation_id):
    """Страница отдельного приглашения."""
    _, _, _, invitations_list = _load_all()
    invitation = find_invitation_by_id(invitations_list, invitation_id)

    if invitation is None:
        content = """
        <h1 class="text-danger">Приглашение не найдено</h1>
        <a href="/invitations/" class="btn btn-outline-secondary">
            ← к списку приглашений
        </a>
        """
        return HttpResponse(
            page("Приглашение не найдено", content),
            status=404,
        )

    if invitation.is_confirmed():
        badge = "bg-success"
    else:
        badge = "bg-secondary"

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">
                Приглашение №{invitation.id}
            </h5>
            <p class="card-text">
                <strong>Гость:</strong> {invitation.guest.name}
            </p>
            <p class="card-text">
                <strong>Событие:</strong> {invitation.event.name}
            </p>
            <p class="card-text">
                <strong>Дата события:</strong> {invitation.event.date}
            </p>
            <p class="card-text">
                Статус:
                <span class="badge {badge}">
                    {invitation.status.title}
                </span>
            </p>
            <a href="/invitations/" class="btn btn-outline-secondary">
                ← к списку приглашений
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(f"Приглашение №{invitation.id}", content)
    )