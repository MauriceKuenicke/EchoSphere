from pathlib import Path

import os

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
