import sys

from rich import print
from rich.console import Console
from rich.table import Table

from echosphere.utils.sql_test_fetcher import get_sql_test_files

console = Console()

NO_TESTS_MESSAGE = "No tests detected."
TABLE_TITLE = "Test cases found:"
ERROR_EXIT_CODE = -1


def display_no_tests_error() -> None:
    """Display an error message when no tests are found and exit."""
    print(f"[bold red]{NO_TESTS_MESSAGE}[/red bold]")
    sys.exit(ERROR_EXIT_CODE)


def display_test_names_table(subdir: str | None = None) -> None:
    test_files = get_sql_test_files(subdir=subdir)
    if not test_files:
        display_no_tests_error()
        return

    table = Table(TABLE_TITLE)
    for test_name, test_info in test_files.items():
        display_name = test_name
        if test_info["subfolder"]:
            display_name = f"{test_info['subfolder']}/{test_name}"
        table.add_row(display_name)

    console.print(table)


ERROR_TEST_NOT_FOUND = "[bold red]Error:[/bold red] Test '{}' not found."
ERROR_READING_FILE = "[bold red]Error:[/bold red] Failed to read test file: {}"


def display_test_sql_code(test_identifier: str) -> None:
    subsuite = None
    test_name = test_identifier
    if "/" in test_identifier:
        subsuite, test_name = test_identifier.split("/")

    # Get test files and normalize the test name
    test_files = get_sql_test_files(subdir=subsuite)
    normalized_name = test_name.lower()

    # Check if the test exists
    if normalized_name not in test_files:
        console.print(ERROR_TEST_NOT_FOUND.format(test_identifier))
        console.print("Available tests:", ", ".join(sorted(test_files.keys())))
        sys.exit(ERROR_EXIT_CODE)

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
