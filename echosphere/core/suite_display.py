"""
Display helpers for EchoSphere test suite output.

This module renders a table of discovered tests and prints the SQL code
of a specific test. It follows the docstring style demonstrated in
`echosphere.utils.sql_test_fetcher`.
"""

import sys

from rich import print
from rich.console import Console
from rich.table import Table

from echosphere.utils.sql_test_fetcher import TestFileInfo, get_sql_test_files

console = Console()

NO_TESTS_MESSAGE = "No tests detected."
TABLE_TITLE = "Test cases found:"
ERROR_EXIT_CODE = -1


def display_no_tests_error() -> None:
    """
    Display an error and exit when no tests are found.

    Prints a bold red message and terminates the process with a
    non-zero exit code to indicate an error state.

    :return: None
    """
    print(f"[bold red]{NO_TESTS_MESSAGE}[/red bold]")
    sys.exit(ERROR_EXIT_CODE)


def display_test_names_table(
    subdir: str | None = None,
    test_files: dict[str, TestFileInfo] | None = None,
    root_only: bool = False,
) -> None:
    """
    Render a table of discovered test names.

    The table lists the base names of `.es.sql` files. If a test resides in a
    subsuite (subdirectory), the displayed name will be `subsuite/<test>`.

    :param subdir: Optional subsuite name. If provided and `test_files` is not
                   supplied, only tests within this subsuite are shown.
    :param test_files: Optional pre-filtered mapping of tests to display.
                       If omitted, tests are discovered via `get_sql_test_files`.
    :param root_only: If True and `test_files` is not supplied, show only
                      root-level tests (no subsuites).
    :return: None
    """
    if test_files is None:
        test_files = get_sql_test_files(subdir=subdir, root_only=root_only)
    if not test_files:
        display_no_tests_error()
        return

    table = Table(TABLE_TITLE)
    for test_name, test_info in test_files.items():
        display_name = test_info["name"] or test_name
        if test_info["subfolder"] and test_info["name"] is None:
            display_name = f"{test_info['subfolder']}/{test_name}"
        table.add_row(display_name)

    console.print(table)


ERROR_TEST_NOT_FOUND = "[bold red]Error:[/bold red] Test '{}' not found."
ERROR_READING_FILE = "[bold red]Error:[/bold red] Failed to read test file: {}"


def display_test_sql_code(test_identifier: str) -> None:
    """
    Print the SQL content for a given test identifier.

    The identifier can be provided as either `<test_name>` or
    `<subsuite>/<test_name>`. The test name is case-insensitive.

    :param test_identifier: Name of the test to display. May include an
                            optional subsuite prefix separated by `/`.
    :return: None
    """
    subsuite: str | None = None
    test_name = test_identifier
    if "/" in test_identifier:
        subsuite, test_name = test_identifier.split("/")

    # Get test files and normalize the test name
    test_files = get_sql_test_files(subdir=subsuite)
    normalized_name = test_name.lower()

    # Fall back to @name match when file-stem lookup fails
    if normalized_name not in test_files:
        matched = next(
            (key for key, info in test_files.items() if (info.get("name") or "").lower() == normalized_name),
            None,
        )
        if matched is None:
            console.print(ERROR_TEST_NOT_FOUND.format(test_identifier))
            console.print("Available tests (use file name or @name):", ", ".join(sorted(test_files.keys())))
            sys.exit(ERROR_EXIT_CODE)
        normalized_name = matched

    # Get file path
    test_file = test_files[normalized_name]
    file_path = test_file.get("full_path")
    if not file_path:
        console.print(ERROR_READING_FILE.format("File path not found"))
        sys.exit(ERROR_EXIT_CODE)

    # Display SQL content
    try:
        with open(file_path, "r") as file:
            sql_content = file.read()
            console.print(f"[bold green]{sql_content}[/bold green]")
    except (IOError, OSError) as e:
        console.print(ERROR_READING_FILE.format(e))
        sys.exit(ERROR_EXIT_CODE)
