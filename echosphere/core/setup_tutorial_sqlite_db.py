import sqlite3
from configparser import ConfigParser
from pathlib import Path

import typer

from echosphere.core.platforms import PlatformEnum


INIT_FILE_TO_BE_CREATED_NAME = "es.ini"
TUTORIAL_SQLITE_DB_FALLBACK = Path(".echosphere") / "tutorial.db"

def get_sqlite_database_path_from_config() -> Path:
    """
    Resolve the SQLite database path from `es.ini`.

    If `es.ini` is missing or incomplete, a fallback tutorial path is returned.
    """
    config = ConfigParser()
    config.read(INIT_FILE_TO_BE_CREATED_NAME)
    try:
        default_env = config.get("default", "env")
        platform = config.get(default_env, "platform").lower()
        if platform not in {PlatformEnum.SQLITE.value, PlatformEnum.TUTORIAL.value}:
            return TUTORIAL_SQLITE_DB_FALLBACK
        db_path = config.get(default_env, "database")
        return Path(db_path)
    except Exception:
        return TUTORIAL_SQLITE_DB_FALLBACK


def setup_tutorial_sqlite_database() -> None:
    """
    Create and seed a local SQLite database used by the tutorial setup.

    The database path is read from `es.ini` and falls back to
    `.echosphere/tutorial.db` when unavailable.
    """
    db_path = get_sqlite_database_path_from_config()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    db_existed_before = db_path.exists()

    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS customers (
                                                     customer_id INTEGER PRIMARY KEY,
                                                     customer_name TEXT NOT NULL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                                                  order_id INTEGER PRIMARY KEY,
                                                  customer_id INTEGER NOT NULL,
                                                  amount REAL NOT NULL,
                                                  created_at TEXT NOT NULL,
                                                  FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
                )
            """
        )

        customer_count = cur.execute("SELECT COUNT(*) FROM customers").fetchone()
        if not customer_count or int(customer_count[0]) == 0:
            cur.executemany(
                "INSERT INTO customers(customer_id, customer_name) VALUES (?, ?)",
                [
                    (1, "Alice"),
                    (2, "Bob"),
                    (3, "Carol"),
                ],
            )

        order_count = cur.execute("SELECT COUNT(*) FROM orders").fetchone()
        if not order_count or int(order_count[0]) == 0:
            cur.executemany(
                "INSERT INTO orders(order_id, customer_id, amount, created_at) VALUES (?, ?, ?, ?)",
                [
                    (1001, 1, 49.90, "2026-01-10"),
                    (1002, 2, 19.99, "2026-01-12"),
                    (1003, 3, 99.50, "2026-01-20"),
                ],
            )

        conn.commit()

    action = "Using existing" if db_existed_before else "Created"
    typer.echo(f"{action} tutorial SQLite database at '{db_path}'.")
