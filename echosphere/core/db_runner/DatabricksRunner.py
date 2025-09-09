import time
import logging
from typing import Any

from echosphere.core.db_runner.BaseClass import BaseRunner
from echosphere.env_config_parser.DatabricksEnvConfigParser import DatabricksAgentConfig

logger = logging.getLogger(__name__)


class DatabricksRunner(BaseRunner):
    """
    Execute SQL tests against Databricks using databricks-sql-connector.

    The test SQL is expected to return violating rows; we wrap it in COUNT(*) to
    get a reliable count without materializing all rows client-side.
    """

    @classmethod
    def _connect(cls, cfg: DatabricksAgentConfig):
        """Return a context-managed Databricks SQL connection.

        Import is within the method to avoid hard dependency at import time.
        """
        try:
            from databricks import sql as dbsql  # type: ignore
        except Exception as e:  # pragma: no cover - import error surface
            raise ImportError(
                "This feature requires the databricks-sql-connector package. Install with 'pip install EchoSphere[databricks]'"
            ) from e

        return dbsql.connect(
            server_hostname=cfg.server_hostname,
            http_path=cfg.http_path,
            access_token=cfg.access_token,
        )

    @classmethod
    def dispatch_test(cls, env: str | None, test_file_path: str) -> tuple[int, float, str]:
        cfg = DatabricksAgentConfig(env_name=env)
        with open(test_file_path, "r") as s:
            sql = s.read()
        sql_clean = sql.strip().rstrip(";")
        count_sql = f"SELECT COUNT(*) FROM ({sql_clean}) AS t"

        logger.info("Executing Databricks test (COUNT wrapper)")
        start_time = time.time()
        try:
            with cls._connect(cfg) as connection:  # type: ignore[attr-defined]
                with connection.cursor() as cursor:
                    # Optional initial USE statements for catalog/schema if provided
                    if getattr(cfg, "catalog", None):
                        try:
                            cursor.execute(f"USE CATALOG {cfg.catalog}")
                        except Exception:
                            # Not all instances support catalogs; ignore silently
                            pass
                    if getattr(cfg, "schema", None):
                        try:
                            cursor.execute(f"USE SCHEMA {cfg.schema}")
                        except Exception:
                            pass

                    cursor.execute(count_sql)
                    row = cursor.fetchone()
        except Exception as e:
            logger.exception("Databricks query execution failed")
            raise Exception(f"Failed to execute test on Databricks: {e}")
        end_time = time.time()

        if not row:
            raise Exception("Failed to retrieve row count from Databricks.")
        try:
            row_count = int(row[0])
        except Exception as e:
            raise Exception(f"Unexpected COUNT(*) result from Databricks: {row}") from e

        execution_time = round(end_time - start_time, 3)
        return row_count, execution_time, sql

    @classmethod
    def fetch_failure_sample(
        cls, env: str | None, sql: str, limit: int = 1000
    ) -> tuple[list[str], list[tuple[Any, ...]]]:
        cfg = DatabricksAgentConfig(env_name=env)
        sql_clean = sql.strip().rstrip(";")
        wrapped_sql = f"SELECT * FROM ({sql_clean}) AS t LIMIT {int(limit)}"

        logger.info("Fetching Databricks failure sample (limit=%s)", limit)
        try:
            with cls._connect(cfg) as connection:  # type: ignore[attr-defined]
                with connection.cursor() as cursor:
                    if getattr(cfg, "catalog", None):
                        try:
                            cursor.execute(f"USE CATALOG {cfg.catalog}")
                        except Exception:
                            pass
                    if getattr(cfg, "schema", None):
                        try:
                            cursor.execute(f"USE SCHEMA {cfg.schema}")
                        except Exception:
                            pass

                    cursor.execute(wrapped_sql)
                    rows = cursor.fetchmany(size=limit)
                    cols = [d[0] for d in cursor.description] if cursor.description else []
        except Exception as e:
            logger.exception("Databricks failure sample fetch failed")
            raise Exception(f"Failed to fetch failure sample from Databricks: {e}")

        return list(cols), list(rows)
