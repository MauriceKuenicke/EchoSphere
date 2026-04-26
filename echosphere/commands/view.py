import typer

from echosphere.core.suite_display import display_test_names_table, display_test_sql_code

app = typer.Typer(help="Explore the test suite: list tests or display SQL for a specific test.")


@app.command(name="tests", help="List test suite content. Use -a to show all tests or -s to filter by subsuite.")
def list_test_suite(
    all_tests: bool = typer.Option(False, "-a", "--all", help="Show all tests including those in subsuites"),
    subdir: str | None = typer.Option(None, "-s", "--suite", help="Filter tests by subsuite"),
) -> None:
    """
    List the current test suite in a table format.

    Retrieves all `.es.sql` tests and prints a table to stdout.
    By default shows only root-level tests; use --all to include subsuites.

    :param all_tests: If True, show all tests including those in subsuites.
    :param subdir: Optional subsuite to filter by when `all_tests` is False.
    :return: None
    """
    if all_tests and subdir:
        typer.echo("Error: Cannot use both --all and --suite options together.")
        raise typer.Exit(code=1)

    display_test_names_table(subdir=None if all_tests else subdir, root_only=not all_tests and subdir is None)


@app.command(name="test", help="View the SQL code for a given test file.")
def view_test_sql(name: str) -> None:
    """
    Print the SQL code for the specified test.

    :param name: Test identifier, optionally including subsuite as
                 `<subsuite>/<test_name>`.
    :return: None
    """
    display_test_sql_code(name)
