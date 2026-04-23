import sqlite3
import time
from typing import Any

from echosphere.core.db_runner.BaseClass import BaseRunner
from echosphere.env_config_parser.SQLiteEnvConfigParser import SQLiteAgentConfig


class SQLiteRunner(BaseRunner):
    """Execute SQL tests against a SQLite database."""

    @classmethod
    def dispatch_test(cls, env: str | None, test_file_path: str) -> tuple[int, float, str]:
        """Execute the SQL test file and return (row_count, execution_time_seconds, sql_text)."""
        cfg = SQLiteAgentConfig(env_name=env)
        with open(test_file_path, "r") as s:
            sql = s.read()
        sql_clean = sql.strip().rstrip(";")
        count_sql = f"SELECT COUNT(*) FROM ({sql_clean}) AS t"

        with sqlite3.connect(cfg.database) as conn:
            cur = conn.cursor()
            start_time = time.time()
            cur.execute(count_sql)
            end_time = time.time()
            row = cur.fetchone()

        if not row:
            raise Exception("Failed to retrieve row count from SQLite.")
        row_count = int(row[0])
        execution_time = round(end_time - start_time, 3)
        return row_count, execution_time, sql

    @classmethod
    def fetch_failure_sample(
        cls, env: str | None, sql: str, limit: int = 1000
    ) -> tuple[list[str], list[tuple[Any, ...]]]:
        """Return (column_names, rows) for a limited sample of the failing SQL output."""
        cfg = SQLiteAgentConfig(env_name=env)
        sql_clean = sql.strip().rstrip(";")
        wrapped_sql = f"SELECT * FROM ({sql_clean}) AS t LIMIT {int(limit)}"

        with sqlite3.connect(cfg.database) as conn:
            cur = conn.cursor()
            cur.execute(wrapped_sql)
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description] if cur.description else []
        return list(cols), list(rows)
