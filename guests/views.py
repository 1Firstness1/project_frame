"""View-функции приложения guests, работающие со слоем SQLite."""

import sqlite3
from django.shortcuts import render

from db.database import get_connection


def guests(request):
    """Страница со списком гостей из SQLite."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    try:
        guests_list = conn.execute(
            """
            SELECT id, name, age
            FROM guests
            ORDER BY name ASC;
            """
        ).fetchall()
    finally:
        conn.close()

    context = {
        "guests": guests_list,
    }
    return render(request, "guests/guest_list.html", context)


def guest_detail(request, guest_id):
    """Страница отдельного гостя из SQLite."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    try:
        guest = conn.execute(
            """
            SELECT id, name, age
            FROM guests
            WHERE id = ?;
            """,
            (guest_id,),
        ).fetchone()
    finally:
        conn.close()

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
    """Страница приглашений выбранного гостя с JOIN из SQLite."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    try:
        guest = conn.execute(
            """
            SELECT id, name, age
            FROM guests
            WHERE id = ?;
            """,
            (guest_id,),
        ).fetchone()

        if guest is None:
            return render(
                request,
                "guests/guest_invitations.html",
                {"guest": None, "invitations": []},
                status=404,
            )

        invitations_list = conn.execute(
            """
            SELECT invitations.id,
                   events.name AS event_name,
                   events.date AS event_date,
                   statuses.title AS status_title,
                   statuses.code AS status_code
            FROM invitations
            JOIN events ON invitations.event_id = events.id
            JOIN statuses ON invitations.status_id = statuses.id
            WHERE invitations.guest_id = ?
            ORDER BY events.date ASC;
            """,
            (guest_id,),
        ).fetchall()
    finally:
        conn.close()

    context = {
        "guest": guest,
        "invitations": invitations_list,
    }
    return render(request, "guests/guest_invitations.html", context)
