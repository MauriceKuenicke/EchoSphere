from datetime import datetime

from echosphere import main
from echosphere.core.test_result import TestResult


def test_normalize_tag_filters_supports_csv_and_case_normalization() -> None:
    normalized = main._normalize_tag_filters(["Critical, nightly", "critical", "  slow  "])
    assert normalized == {"critical", "nightly", "slow"}


def test_run_suite_applies_tag_filters_and_metadata_fields(monkeypatch) -> None:
    suite = {
        "check_primary_keys": {
            "full_path": "/tmp/check_primary_keys.es.sql",
            "subfolder": None,
            "name": "PK Integrity",
            "tags": ["critical", "nightly"],
            "timeout": 30,
        },
        "orders_freshness": {
            "full_path": "/tmp/orders_freshness.es.sql",
            "subfolder": "daily",
            "name": None,
            "tags": ["nightly", "slow"],
            "timeout": None,
        },
    }
    displayed_test_keys: set[str] = set()
    executed: list[dict[str, object]] = []

    monkeypatch.setattr(main, "get_sql_test_files", lambda: suite)

    def fake_display_test_names_table(subdir=None, test_files=None) -> None:
        nonlocal displayed_test_keys
        _ = subdir
        displayed_test_keys = set((test_files or {}).keys())

    monkeypatch.setattr(main, "display_test_names_table", fake_display_test_names_table)

    def fake_run_async_test_and_poll(
        test_name: str,
        test_file_path: str,
        env: str | None,
        capture_failure_data: bool = False,
        timeout_seconds: int | None = None,
    ) -> TestResult:
        executed.append(
            {
                "name": test_name,
                "path": test_file_path,
                "env": env,
                "capture_failure_data": capture_failure_data,
                "timeout_seconds": timeout_seconds,
            }
        )
        return TestResult(
            name=test_name,
            passed=True,
            duration=0.001,
            sql="SELECT 1",
            row_count=0,
            timestamp=datetime.now(),
        )

    monkeypatch.setattr(main, "run_async_test_and_poll", fake_run_async_test_and_poll)

    main.run_suite(
        env=None,
        junitxml=None,
        export_failures=None,
        tag=["critical, nightly"],
        exclude_tag=["slow"],
    )

    assert displayed_test_keys == {"check_primary_keys"}
    assert len(executed) == 1
    assert executed[0]["name"] == "PK Integrity"
    assert executed[0]["path"] == "/tmp/check_primary_keys.es.sql"
    assert executed[0]["timeout_seconds"] == 30
