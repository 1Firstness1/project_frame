"""View-функции приложения invitations."""

from django.shortcuts import render

from models.invitations import find_invitation_by_id
from storage import (
    load_events,
    load_guests,
    load_invitations,
    load_statuses,
)


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
    context = {
        "invitations": invitations_list,
    }
    return render(request, "invitations/invitation_list.html", context)


def invitation_detail(request, invitation_id):
    """Страница отдельного приглашения."""
    _, _, _, invitations_list = _load_all()
    invitation = find_invitation_by_id(invitations_list, invitation_id)
    context = {
        "invitation": invitation,
    }
    return render(
        request,
        "invitations/invitation_detail.html",
        context,
        status=404 if invitation is None else 200,
    )
