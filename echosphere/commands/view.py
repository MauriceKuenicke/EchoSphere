from typing import Optional

import typer

from echosphere.core.suite_display import display_test_names_table, display_test_sql_code

app = typer.Typer()


@app.command(name="tests", help="List test suite content. Use -a to view all tests or -d to filter by subdirectory.")
def list_test_suite(
    all_tests: bool = typer.Option(False, "-a", "--all", help="Show all tests regardless of subsuite"),
    subdir: Optional[str] = typer.Option(None, "-s", "--suite", help="Filter tests by subsuite"),
) -> None:
    """
    List the current test suite in a table format.

    Retrieves all `.es.sql` tests and prints a table to stdout.
    Optionally filters by subsuite.

    :param all_tests: If True, ignore `subdir` and show all tests.
    :param subdir: Optional subsuite to filter by when `all_tests` is False.
    :return: None
    """
    if all_tests and subdir:
        typer.echo("Error: Cannot use both --all and --suite options together.")
        raise typer.Exit(code=1)

    display_test_names_table(subdir=None if all_tests else subdir)


@app.command(name="test", help="View the SQL code for a given test file.")
def view_test_sql(name: str) -> None:
    """
    Print the SQL code for the specified test.

    :param name: Test identifier, optionally including subsuite as
                 `<subsuite>/<test_name>`.
    :return: None
    """
    display_test_sql_code(name)
