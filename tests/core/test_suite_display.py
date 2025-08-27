import pytest

from echosphere.core import suite_display as sd


class TestSuiteDisplay:
    def test_display_no_tests_error_exits(self) -> None:
        with pytest.raises(SystemExit) as ex:
            sd.display_no_tests_error()
        assert ex.value.code == -1

    def test_display_test_names_table_shows_all(self, capsys) -> None:
        sd.display_test_names_table()
        out = capsys.readouterr().out.lower()
        assert "example" in out
        assert "hello/sub_test" in out

    def test_display_test_names_table_filters_subdir(self, capsys) -> None:
        sd.display_test_names_table(subdir="hello")
        out = capsys.readouterr().out.lower()
        assert "hello/sub_test" in out
        assert "example" not in out

    def test_display_test_names_table_no_tests_exits(self, monkeypatch) -> None:
        monkeypatch.setattr(sd, "get_sql_test_files", lambda subdir=None: {})
        with pytest.raises(SystemExit) as ex:
            sd.display_test_names_table()
        assert ex.value.code == -1

    def test_display_test_sql_code_prints_sql(self, capsys) -> None:
        sd.display_test_sql_code("example")
        out = capsys.readouterr().out
        assert "SELECT * FROM table_name;" in out

    def test_display_test_sql_code_with_subsuite(self, capsys) -> None:
        sd.display_test_sql_code("hello/sub_test")
        out = capsys.readouterr().out
        assert "SELECT * FROM table_name;" in out

    def test_display_test_sql_code_missing_test(self) -> None:
        with pytest.raises(SystemExit) as ex:
            sd.display_test_sql_code("not_here")
        assert ex.value.code == -1

    def test_display_test_sql_code_missing_file_path(self, monkeypatch) -> None:
        # Provide mapping missing the full_path for example
        monkeypatch.setattr(
            sd,
            "get_sql_test_files",
            lambda subdir=None: {"example": {"full_path": None, "subfolder": None}},
        )
        with pytest.raises(SystemExit) as ex:
            sd.display_test_sql_code("example")
        assert ex.value.code == -1
