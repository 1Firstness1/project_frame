"""Скрипт импорта данных из JSON в SQLite."""

import json
from pathlib import Path

from db.database import BASE_DIR, get_connection

EVENTS_FILE = BASE_DIR / "data" / "events.json"
GUESTS_FILE = BASE_DIR / "data" / "guests.json"
STATUSES_FILE = BASE_DIR / "data" / "statuses.json"
INVITATIONS_FILE = BASE_DIR / "data" / "invitations.json"
SCHEMA_FILE = BASE_DIR / "sql" / "schema.sql"


def load_json(filepath: Path):
    """Прочитать данные из JSON-файла."""
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)


def init_schema(conn):
    """Инициализировать схему базы данных."""
    with open(SCHEMA_FILE, "r", encoding="utf-8") as file:
        conn.executescript(file.read())


def import_events(conn):
    """Импортировать события."""
    events = load_json(EVENTS_FILE)
    conn.executemany(
        """
        INSERT OR REPLACE INTO events (id, name, date, places)
        VALUES (?, ?, ?, ?)
        """,
        [(e["id"], e["name"], e["date"], e["places"]) for e in events],
    )


def import_guests(conn):
    """Импортировать гостей."""
    guests = load_json(GUESTS_FILE)
    conn.executemany(
        """
        INSERT OR REPLACE INTO guests (id, name, age)
        VALUES (?, ?, ?)
        """,
        [(g["id"], g["name"], g["age"]) for g in guests],
    )


def import_statuses(conn):
    """Импортировать статусы."""
    statuses = load_json(STATUSES_FILE)
    conn.executemany(
        """
        INSERT OR REPLACE INTO statuses (id, code, title)
        VALUES (?, ?, ?)
        """,
        [(s["id"], s["code"], s["title"]) for s in statuses],
    )


def import_invitations(conn):
    """Импортировать приглашения."""
    invitations = load_json(INVITATIONS_FILE)
    conn.executemany(
        """
        INSERT OR REPLACE INTO invitations (id, event_id, guest_id, status_id)
        VALUES (?, ?, ?, ?)
        """,
        [
            (
                inv["id"],
                inv["event_id"],
                inv["guest_id"],
                inv["status_id"],
            )
            for inv in invitations
        ],
    )


def main():
    """Основная функция импорта данных."""
    conn = get_connection()
    try:
        init_schema(conn)
        import_events(conn)
        import_guests(conn)
        import_statuses(conn)
        import_invitations(conn)
        conn.commit()
        print("Импорт в SQLite успешно завершён.")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
