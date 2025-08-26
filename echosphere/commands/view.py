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
    List current test suite.

    This command retrieves a list of SQL test files and presents them in a
    structured table format.
    It uses the `Table` utility for formatting the
    output and prints it to the console.

    Options:
        -a, --all: Show all tests in the suite
        -d, --suite: Show only tests in the specified subsuite

    :return: None
    """
    if all_tests and subdir:
        typer.echo("Error: Cannot use both --all and --suite options together.")
        raise typer.Exit(code=1)

    display_test_names_table(subdir=None if all_tests else subdir)


@app.command(name="test", help="View the SQL code for a given test file.")
def view_test_sql(name: str) -> None:
    display_test_sql_code(name)
