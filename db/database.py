"""Модуль подключения к базе данных SQLite."""

from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "guestlist.sqlite"


def get_connection():
    """Создать и настроить соединение с базой данных SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
