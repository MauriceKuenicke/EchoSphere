from pathlib import Path

from echosphere.core.setup_es import setup_es_directory
from echosphere.utils.sql_test_fetcher import get_sql_test_files


def test_setup_es_directory_provides_metadata_in_sqlite_examples(tmp_path: Path) -> None:
    suite_dir = tmp_path / "es_suite"
    setup_es_directory(dir_name=str(suite_dir), platform="sqlite")

    files = get_sql_test_files(path=str(suite_dir))
    assert set(files.keys()) == {"always_fail", "always_pass"}

    always_fail = files["always_fail"]
    assert always_fail["name"] == "SQLite Example - Always Fail"
    assert always_fail["tags"] == ["example", "should-fail", "sqlite"]
    assert always_fail["timeout"] == 30

    always_pass = files["always_pass"]
    assert always_pass["name"] == "SQLite Example - Always Pass"
    assert always_pass["tags"] == ["example", "should-pass", "sqlite"]
    assert always_pass["timeout"] == 30
