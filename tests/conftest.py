import os
from pathlib import Path

import pytest


@pytest.fixture(scope="session", autouse=True)
def set_cwd_to_repo_root() -> None:
    """Ensure tests run with the repository root as the current working directory."""
    repo_root = Path(__file__).resolve().parent.parent
    os.chdir(repo_root)


@pytest.fixture(scope="session")
def example_suites_path() -> Path:
    # Use the repository-provided example suite for tests
    return Path("tests") / "example_suites"


@pytest.fixture(autouse=True)
def patch_suite_display_fetcher(monkeypatch: pytest.MonkeyPatch, example_suites_path: Path):
    """
    Ensure core.suite_display uses our tests/example_suites directory for fetching
    SQL files so tests don't rely on ./es_suite.
    """
    from echosphere.core import suite_display as sd
    from echosphere.utils import sql_test_fetcher as fetcher

    def replacement(subdir: str | None = None):
        return fetcher.get_sql_test_files(path=str(example_suites_path), subdir=subdir)

    monkeypatch.setattr(sd, "get_sql_test_files", replacement)
    yield
