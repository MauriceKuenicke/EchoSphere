import threading
from datetime import datetime
from typing import Sequence

from rich import print

from echosphere.core.db_runner import get_db_runner
from echosphere.core.db_runner.BaseClass import BaseRunner
from echosphere.core.platforms import PlatformEnum
from echosphere.core.test_result import TestResult
from echosphere.env_config_parser.PlatformExtractor import PlatformExtractor

FAILED_TEST_MESSAGE = "{test_name}...[red bold]Failed[/red bold] [yellow bold]{execution_time}s[/yellow bold][red]\n{sql}\nMore than zero rows ({row_count}) detected.[/red]"
SUCCESS_TEST_MESSAGE = "{test_name}...[green bold]Passed[/green bold] [yellow bold]{execution_time}s[/yellow bold]"
TIMEOUT_TEST_MESSAGE = "{test_name}...[red bold]Failed[/red bold] [yellow bold]{execution_time}s[/yellow bold][red]\n{sql}\nExceeded timeout ({timeout}s).[/red]"


class _TestExecutionTimeoutError(Exception):
    """Raised when a test exceeds its configured timeout."""


def _read_sql_file(test_file_path: str) -> str:
    """Read and return SQL file contents for reporting."""
    with open(test_file_path, "r", encoding="utf-8") as sql_file:
        return sql_file.read()


def _dispatch_test_with_optional_timeout(
    runner: type[BaseRunner], env: str | None, test_file_path: str, timeout_seconds: int | None
) -> tuple[int, float, str]:
    """
    Execute a test with optional timeout enforcement.

    When `timeout_seconds` is provided, query execution runs in a daemon thread
    and this function raises `_TestExecutionTimeoutError` if the deadline is exceeded.
    """
    if timeout_seconds is None:
        return runner.dispatch_test(env=env, test_file_path=test_file_path)

    result: tuple[int, float, str] | None = None
    error: Exception | None = None

    def run_dispatch() -> None:
        nonlocal result, error
        try:
            result = runner.dispatch_test(env=env, test_file_path=test_file_path)
        except Exception as exc:  # pragma: no cover - delegated connector errors
            error = exc

    worker = threading.Thread(target=run_dispatch, daemon=True)
    worker.start()
    worker.join(timeout=timeout_seconds)

    if worker.is_alive():
        raise _TestExecutionTimeoutError(f"Test exceeded timeout of {timeout_seconds} seconds.")
    if error is not None:
        raise error
    if result is None:
        raise Exception("No result was produced by the test runner.")

    return result


def run_async_test_and_poll(
    test_name: str,
    test_file_path: str,
    env: str | None,
    capture_failure_data: bool = False,
    timeout_seconds: int | None = None,
) -> TestResult:
    """
    Run a single SQL test asynchronously on the configured platform and evaluate its result.

    A test is considered successful when the executed query returns zero rows.

    :param test_name: Human-friendly identifier of the test (used for output).
    :param test_file_path: Full path to the SQL file to execute.
    :param env: Optional environment/agent name from es.ini; if None, default is used.
    :param capture_failure_data: If True, fetch up to 1000 rows and columns when the test fails.
    :param timeout_seconds: Optional timeout in seconds for this test.
    :return: TestResult with pass/fail and details.
    """
    platform_name = PlatformExtractor.extract_platform_info(env_name=env)
    supported_platforms = [platform.value for platform in PlatformEnum]
    if platform_name not in supported_platforms:
        raise Exception(
            f"Unsupported platform name found in .ini file. Should be one of: [{','.join(supported_platforms)}]"
        )

    runner = get_db_runner(platform_name)
    try:
        row_count, execution_time, sql = _dispatch_test_with_optional_timeout(
            runner=runner,
            env=env,
            test_file_path=test_file_path,
            timeout_seconds=timeout_seconds,
        )
    except _TestExecutionTimeoutError:
        timestamp = datetime.now()
        sql = _read_sql_file(test_file_path)
        execution_time = float(timeout_seconds or 0)
        timeout_value = int(timeout_seconds or 0)
        timeout_msg = TIMEOUT_TEST_MESSAGE.format(
            test_name=test_name, execution_time=execution_time, sql=sql, timeout=timeout_value
        )
        print(timeout_msg)
        return TestResult(
            name=test_name,
            passed=False,
            duration=execution_time,
            sql=sql,
            row_count=0,
            timestamp=timestamp,
            failure_message=f"Test exceeded timeout of {timeout_value} seconds.",
            failure_columns=None,
            failure_rows=None,
        )

    timestamp = datetime.now()
    failed = bool(row_count)

    if failed:
        error_msg = FAILED_TEST_MESSAGE.format(
            test_name=test_name, execution_time=execution_time, sql=sql, row_count=row_count
        )
        print(error_msg)

        failure_columns: list[str] | None = None
        failure_rows: list[Sequence[object]] | None = None
        if capture_failure_data:
            try:
                cols, rows = runner.fetch_failure_sample(env=env, sql=sql, limit=1000)
                failure_columns = cols
                # Ensure rows are a list of sequences
                failure_rows = list(rows[:1000]) if rows else []
            except Exception:
                # Keep exporting flow robust; just record message
                pass

        return TestResult(
            name=test_name,
            passed=False,
            duration=execution_time,
            sql=sql,
            row_count=int(row_count or 0),
            timestamp=timestamp,
            failure_message=f"Test returned {row_count} rows. Expected 0 rows.",
            failure_columns=failure_columns,
            failure_rows=failure_rows,
        )

    success_message = SUCCESS_TEST_MESSAGE.format(test_name=test_name, execution_time=execution_time)
    print(success_message)
    return TestResult(
        name=test_name,
        passed=True,
        duration=execution_time,
        sql=sql,
        row_count=int(row_count or 0),
        timestamp=timestamp,
        failure_message=None,
    )
