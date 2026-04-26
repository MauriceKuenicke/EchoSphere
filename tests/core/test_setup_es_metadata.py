from pathlib import Path

from echosphere.core.setup_es import setup_es_directory
from echosphere.utils.sql_test_fetcher import get_sql_test_files


def test_setup_es_directory_provides_metadata_in_sqlite_examples(tmp_path: Path) -> None:
    suite_dir = tmp_path / "es_suite"
    setup_es_directory(dir_name=str(suite_dir), platform="sqlite")

    files = get_sql_test_files(path=str(suite_dir))
    assert set(files.keys()) == {"check_existence", "table_does_not_exist"}

    check_existence = files["check_existence"]
    assert check_existence["name"] == "SQLite Example - Check Existence"
    assert check_existence["tags"] == ["example", "should-fail", "sqlite"]
    assert check_existence["timeout"] == 30

    table_does_not_exist = files["table_does_not_exist"]
    assert table_does_not_exist["name"] == "SQLite Example - Table Does Not Exist"
    assert table_does_not_exist["tags"] == ["example", "should-pass", "sqlite"]
    assert table_does_not_exist["timeout"] == 30
