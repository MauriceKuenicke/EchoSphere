import os
from pathlib import Path

import pytest

from echosphere.utils.sql_test_fetcher import get_sql_test_files


class TestGetSqlTestFiles:
    def test_discovers_root_and_subfolder_files(self, example_suites_path: Path) -> None:
        files = get_sql_test_files(path=str(example_suites_path))

        assert "example" in files
        assert "sub_test" in files

        # Root file
        root_info = files["example"]
        assert root_info["subfolder"] is None
        assert isinstance(root_info["full_path"], str)
        assert os.path.exists(root_info["full_path"]) is True

        # Subfolder file
        sub_info = files["sub_test"]
        assert sub_info["subfolder"] == "hello"
        assert isinstance(sub_info["full_path"], str)
        assert os.path.exists(sub_info["full_path"]) is True

    def test_filter_by_subdir(self, example_suites_path: Path) -> None:
        files = get_sql_test_files(path=str(example_suites_path), subdir="hello")
        assert set(files.keys()) == {"sub_test"}
        info = files["sub_test"]
        assert info["subfolder"] == "hello"

    def test_name_normalization_lowercase(self, tmp_path: Path) -> None:
        # Create mixed-case file name and ensure key is lowercased
        (tmp_path / "MixedCase.es.sql").write_text("SELECT 1;")
        results = get_sql_test_files(path=str(tmp_path))
        assert "mixedcase" in results

    def test_empty_directory_returns_empty_dict(self, tmp_path: Path) -> None:
        results = get_sql_test_files(path=str(tmp_path))
        assert results == {}

    def test_full_path_points_to_existing_file(self, example_suites_path: Path) -> None:
        files = get_sql_test_files(path=str(example_suites_path))
        for info in files.values():
            assert info["full_path"], "full_path should be populated"
            assert Path(info["full_path"]).exists(), f"{info['full_path']} should exist"

    def test_metadata_defaults_when_not_present(self, tmp_path: Path) -> None:
        (tmp_path / "no_metadata.es.sql").write_text("SELECT 1;", encoding="utf-8")
        files = get_sql_test_files(path=str(tmp_path))
        info = files["no_metadata"]
        assert info["name"] is None
        assert info["tags"] == []
        assert info["timeout"] is None

    def test_example_suite_metadata_is_available_out_of_the_box(self, example_suites_path: Path) -> None:
        files = get_sql_test_files(path=str(example_suites_path))

        root_test = files["example"]
        assert root_test["name"] == "Example Root Test"
        assert root_test["tags"] == ["example", "smoke"]
        assert root_test["timeout"] == 15

        sub_test = files["sub_test"]
        assert sub_test["name"] == "Example Subsuite Test"
        assert sub_test["tags"] == ["example", "subsuite"]
        assert sub_test["timeout"] == 20

    def test_metadata_parsing_from_header_comments(self, tmp_path: Path) -> None:
        test_sql = """-- @name: Example Test
-- @tag: critical, example, nightly
-- @timeout: 30
SELECT 1;
"""
        (tmp_path / "metadata.es.sql").write_text(test_sql, encoding="utf-8")
        files = get_sql_test_files(path=str(tmp_path))
        info = files["metadata"]
        assert info["name"] == "Example Test"
        assert info["tags"] == ["critical", "example", "nightly"]
        assert info["timeout"] == 30

    def test_metadata_outside_header_is_ignored(self, tmp_path: Path) -> None:
        sql = """SELECT 1;
-- @name: should_not_apply
-- @tag: hidden
-- @timeout: 15
"""
        (tmp_path / "late_metadata.es.sql").write_text(sql, encoding="utf-8")
        files = get_sql_test_files(path=str(tmp_path))
        info = files["late_metadata"]
        assert info["name"] is None
        assert info["tags"] == []
        assert info["timeout"] is None

    def test_invalid_timeout_metadata_raises(self, tmp_path: Path) -> None:
        sql = """-- @timeout: not_a_number
SELECT 1;
"""
        (tmp_path / "bad_timeout.es.sql").write_text(sql, encoding="utf-8")
        with pytest.raises(ValueError, match="Invalid @timeout value"):
            get_sql_test_files(path=str(tmp_path))
