"""View-функции приложения invitations, работающие со слоем SQLite."""

import sqlite3
from django.shortcuts import render

from db.database import get_connection


def invitations(request):
    """Страница со списком приглашений (JOIN 4 таблиц) из SQLite."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    try:
        invitations_list = conn.execute(
            """
            SELECT invitations.id,
                   events.name AS event_name,
                   events.date AS event_date,
                   guests.name AS guest_name,
                   statuses.title AS status_title,
                   statuses.code AS status_code
            FROM invitations
            JOIN events ON invitations.event_id = events.id
            JOIN guests ON invitations.guest_id = guests.id
            JOIN statuses ON invitations.status_id = statuses.id
            ORDER BY events.date ASC;
            """
        ).fetchall()
    finally:
        conn.close()

    context = {
        "invitations": invitations_list,
    }
    return render(request, "invitations/invitation_list.html", context)


def invitation_detail(request, invitation_id):
    """Страница отдельного приглашения из SQLite."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    try:
        invitation = conn.execute(
            """
            SELECT invitations.id,
                   events.name AS event_name,
                   events.date AS event_date,
                   guests.name AS guest_name,
                   guests.age AS guest_age,
                   statuses.title AS status_title,
                   statuses.code AS status_code
            FROM invitations
            JOIN events ON invitations.event_id = events.id
            JOIN guests ON invitations.guest_id = guests.id
            JOIN statuses ON invitations.status_id = statuses.id
            WHERE invitations.id = ?;
            """,
            (invitation_id,),
        ).fetchone()
    finally:
        conn.close()

    context = {
        "invitation": invitation,
    }
    return render(
        request,
        "invitations/invitation_detail.html",
        context,
        status=404 if invitation is None else 200,
    )
