"""View-функции приложения events, работающие со слоем SQLite."""

import sqlite3
from django.shortcuts import render

from db.database import get_connection


def events(request):
    """Страница со списком событий из SQLite."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    try:
        events_list = conn.execute(
            """
            SELECT id, name, date, places
            FROM events
            ORDER BY name ASC;
            """
        ).fetchall()
    finally:
        conn.close()

    context = {
        "events": events_list,
    }
    return render(request, "events/event_list.html", context)


def event_detail(request, event_id):
    """Страница отдельного события из SQLite."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    try:
        event = conn.execute(
            """
            SELECT id, name, date, places
            FROM events
            WHERE id = ?;
            """,
            (event_id,),
        ).fetchone()
    finally:
        conn.close()

    context = {
        "event": event,
    }
    return render(
        request,
        "events/event_detail.html",
        context,
        status=404 if event is None else 200,
    )


def search_events(request):
    """Поиск событий по минимальной вместимости (параметризованный запрос)."""
    min_places = request.GET.get("min_places", "").strip()
    events_found = []

    if min_places:
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        try:
            places_num = int(min_places)
            events_found = conn.execute(
                """
                SELECT id, name, date, places
                FROM events
                WHERE places >= ?
                ORDER BY places ASC;
                """,
                (places_num,),
            ).fetchall()
        except ValueError:
            events_found = []
        finally:
            conn.close()

    context = {
        "events": events_found,
        "min_places": min_places,
    }
    return render(request, "events/event_search.html", context)


def event_statistics(request):
    """Страница статистики с использованием GROUP BY и HAVING."""
    threshold_str = request.GET.get("threshold", "1").strip()
    try:
        threshold = int(threshold_str)
    except ValueError:
        threshold = 1

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    try:
        # Группировка по связанным сущностям (событиям)
        stats = conn.execute(
            """
            SELECT events.id,
                   events.name AS event_name,
                   events.date AS event_date,
                   events.places,
                   COUNT(invitations.id) AS invitations_count
            FROM events
            LEFT JOIN invitations ON events.id = invitations.event_id
            GROUP BY events.id, events.name, events.date, events.places
            ORDER BY invitations_count DESC;
            """
        ).fetchall()

        # Группировка по категориям (статусам приглашений)
        status_stats = conn.execute(
            """
            SELECT statuses.title AS status_title,
                   statuses.code AS status_code,
                   COUNT(invitations.id) AS count
            FROM statuses
            LEFT JOIN invitations ON statuses.id = invitations.status_id
            GROUP BY statuses.id, statuses.title, statuses.code
            ORDER BY count DESC;
            """
        ).fetchall()

        # Фильтрация групп с помощью HAVING
        having_stats = conn.execute(
            """
            SELECT events.id,
                   events.name AS event_name,
                   COUNT(invitations.id) AS invitations_count
            FROM events
            JOIN invitations ON events.id = invitations.event_id
            GROUP BY events.id, events.name
            HAVING COUNT(invitations.id) > ?
            ORDER BY invitations_count DESC;
            """,
            (threshold,),
        ).fetchall()

        total_guests = conn.execute(
            "SELECT COUNT(*) AS total FROM guests;"
        ).fetchone()["total"]

        total_invitations = conn.execute(
            "SELECT COUNT(*) AS total FROM invitations;"
        ).fetchone()["total"]
    finally:
        conn.close()

    context = {
        "statistics": stats,
        "status_stats": status_stats,
        "having_stats": having_stats,
        "threshold": threshold,
        "total_guests": total_guests,
        "total_invitations": total_invitations,
    }
    return render(request, "events/statistics.html", context)
