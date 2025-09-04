import time
from typing import Any

import psycopg2

from echosphere.core.db_runner.BaseClass import BaseRunner
from echosphere.env_config_parser.PostgresEnvConfigParser import PostgresAgentConfig


class PostgresRunner(BaseRunner):
    """
    A utility class for executing SQL tests against a PostgreSQL database.
    """

    @classmethod
    def dispatch_test(cls, env: str | None, test_file_path: str) -> tuple[int, float, str]:
        """
        Execute a SQL test against Postgres and return results.

        The test SQL is expected to be a SELECT of violating rows. To get a
        reliable row count without materializing all rows client-side, we wrap
        the query in SELECT COUNT(*). The original SQL text is returned for
        reporting and failure sampling.
        """
        cfg = PostgresAgentConfig(env_name=env)
        conn_kwargs: dict[str, Any] = {
            "host": cfg.host,
            "port": cfg.port,
            "dbname": cfg.database,
            "user": cfg.user,
            "password": cfg.password,
            "options": "-c application_name=EchoSphere",
        }
        if cfg.sslmode:
            conn_kwargs["sslmode"] = cfg.sslmode

        with psycopg2.connect(**conn_kwargs) as conn:
            with conn.cursor() as cur:
                # Optional schema search path
                if cfg.schema:
                    cur.execute(f"SET search_path TO {cfg.schema}")

                with open(test_file_path, "r") as s:
                    sql = s.read()
                sql_clean = sql.strip().rstrip(";")
                count_sql = f"SELECT COUNT(*) FROM ({sql_clean}) AS t"

                start_time = time.time()
                cur.execute(count_sql)
                row_count_obj = cur.fetchone()
                end_time = time.time()

                if not row_count_obj:
                    raise Exception("Failed to retrieve row count from Postgres.")
                row_count = int(row_count_obj[0])

        execution_time = round(end_time - start_time, 3)
        return row_count, execution_time, sql

    @classmethod
    def fetch_failure_sample(
        cls, env: str | None, sql: str, limit: int = 1000
    ) -> tuple[list[str], list[tuple[Any, ...]]]:
        """
        Fetch up to `limit` rows and column names for a failed test's SQL query.

        The SQL is wrapped with a LIMIT to avoid loading too much data.
        """
        cfg = PostgresAgentConfig(env_name=env)
        sql_clean = sql.strip().rstrip(";")
        wrapped_sql = f"SELECT * FROM ({sql_clean}) AS t LIMIT {int(limit)}"

        conn_kwargs: dict[str, Any] = {
            "host": cfg.host,
            "port": cfg.port,
            "dbname": cfg.database,
            "user": cfg.user,
            "password": cfg.password,
            "options": "-c application_name=EchoSphere",
        }
        if cfg.sslmode:
            conn_kwargs["sslmode"] = cfg.sslmode

        with psycopg2.connect(**conn_kwargs) as conn:
            with conn.cursor() as cur:
                # Optional schema search path
                if cfg.schema:
                    cur.execute(f"SET search_path TO {cfg.schema}")
                cur.execute(wrapped_sql)
                rows = cur.fetchmany(size=limit)
                cols = [d[0] for d in cur.description] if cur.description else []
        return list(cols), list(rows)
