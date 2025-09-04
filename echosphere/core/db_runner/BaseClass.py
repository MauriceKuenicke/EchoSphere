from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Type


class BaseRunner(ABC):
    """
    Abstract base class that defines the common interface for all database runners.

    Runners must implement classmethods for:
    - dispatch_test(env, test_file_path) -> (row_count, execution_time_seconds, sql_text)
    - fetch_failure_sample(env, sql, limit=1000) -> (column_names, rows)
    """

    @classmethod
    @abstractmethod
    def dispatch_test(cls, env: str | None, test_file_path: str) -> tuple[int, float, str]:
        """Execute the SQL test file and return (row_count, execution_time_seconds, sql_text)."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def fetch_failure_sample(cls, env: str | None, sql: str, limit: int = 1000) -> tuple[list[str], list[tuple[Any]]]:
        """Return (column_names, rows) for a limited sample of the failing SQL output."""
        raise NotImplementedError


# Convenient alias for factory typing
RunnerType = Type[BaseRunner]
