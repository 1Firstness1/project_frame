"""View-функции приложения guests."""

from django.shortcuts import render

from models.guests import find_guest_by_id
from storage import (
    load_events,
    load_guests,
    load_invitations,
    load_statuses,
)


def guests(request):
    """Страница со списком гостей."""
    guests_list = load_guests("data/guests.json")
    context = {
        "guests": guests_list,
    }
    return render(request, "guests/guest_list.html", context)


def guest_detail(request, guest_id):
    """Страница отдельного гостя."""
    guests_list = load_guests("data/guests.json")
    guest = find_guest_by_id(guests_list, guest_id)
    context = {
        "guest": guest,
    }
    return render(
        request,
        "guests/guest_detail.html",
        context,
        status=404 if guest is None else 200,
    )


def guest_invitations(request, guest_id):
    """Страница приглашений выбранного гостя."""
    guests_list = load_guests("data/guests.json")
    guest = find_guest_by_id(guests_list, guest_id)

    if guest is None:
        return render(
            request,
            "guests/guest_invitations.html",
            {"guest": None, "invitations": []},
            status=404,
        )

    events_list = load_events("data/events.json")
    statuses_list = load_statuses("data/statuses.json")
    invitations_list = load_invitations(
        "data/invitations.json",
        events_list,
        guests_list,
        statuses_list,
    )
    user_invitations = [
        inv for inv in invitations_list if inv.guest.id == guest.id
    ]

    context = {
        "guest": guest,
        "invitations": user_invitations,
    }
    return render(request, "guests/guest_invitations.html", context)
