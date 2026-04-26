import time
from pathlib import Path

import pytest

from echosphere.core import run_async_tests as rat


class _SlowRunner:
    @classmethod
    def dispatch_test(cls, env: str | None, test_file_path: str) -> tuple[int, float, str]:
        _ = env
        _ = test_file_path
        time.sleep(0.2)
        return 0, 0.2, "SELECT 1;"

    @classmethod
    def fetch_failure_sample(cls, env: str | None, sql: str, limit: int = 1000) -> tuple[list[str], list[tuple]]:
        _ = env
        _ = sql
        _ = limit
        return [], []


def test_run_async_test_and_poll_marks_timeout_as_failure(monkeypatch, tmp_path: Path) -> None:
    sql_file = tmp_path / "timeout.es.sql"
    sql_file.write_text("SELECT 1;", encoding="utf-8")

    monkeypatch.setattr(rat.PlatformExtractor, "extract_platform_info", lambda env_name=None: "postgres")
    monkeypatch.setattr(rat, "get_db_runner", lambda platform_name: _SlowRunner)

    result = rat.run_async_test_and_poll(
        test_name="timeout_test",
        test_file_path=str(sql_file),
        env=None,
        timeout_seconds=0,
    )

    assert result.passed is False
    assert result.name == "timeout_test"
    assert result.failure_message == "Test exceeded timeout of 0 seconds."


def test_run_async_test_and_poll_rejects_unsupported_platform(monkeypatch, tmp_path: Path) -> None:
    sql_file = tmp_path / "unsupported.es.sql"
    sql_file.write_text("SELECT 1;", encoding="utf-8")

    monkeypatch.setattr(rat.PlatformExtractor, "extract_platform_info", lambda env_name=None: "unsupported_db")

    with pytest.raises(Exception, match="Unsupported platform name found in .ini file."):
        rat.run_async_test_and_poll(
            test_name="unsupported_test",
            test_file_path=str(sql_file),
            env=None,
        )
