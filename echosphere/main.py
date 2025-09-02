import concurrent.futures
import sys
import time
from typing import Optional, cast

import typer
from rich import print
from rich.console import Console
from typing_extensions import Annotated

from echosphere.commands import view
from echosphere.core.excel_export import FailedTestExporter
from echosphere.core.junit_export import JUnitXmlExporter
from echosphere.core.run_async_tests import run_async_test_and_poll
from echosphere.core.setup_es import PlatformEnum, init_es
from echosphere.core.suite_display import display_test_names_table
from echosphere.core.test_result import TestResult
from echosphere.utils.sql_test_fetcher import TestFileInfo, get_sql_test_files

console = Console()

app = typer.Typer(
    name="EchoSphere Testing Suite",
    help="EchoSphere Testing Suite.",
    context_settings={"help_option_names": ["-h", "--help"]},
    add_completion=False,
    pretty_exceptions_show_locals=True,
    pretty_exceptions_short=True,
)

app.add_typer(view.app, name="view")


@app.command(name="setup", help="Create the necessary setup.")
def configure_setup(platform: PlatformEnum = typer.Option(None, help="Platform to configure.")) -> None:
    """
    Initialize EchoSphere for the selected platform by creating config and example suite.

    :param platform: Target platform to configure (e.g., PlatformEnum.SNOWFLAKE).
    :return: None
    """
    if platform is None:
        console.print(
            "[bold red]Error:[/bold red] Please specify a platform. Use [bold green]--help[/bold green] for more info."
        )
        raise typer.Exit(code=-1)
    init_es(platform)


@app.command(name="run", help="Run the current test suite.")
def run_suite(
    env: Annotated[
        Optional[str],
        typer.Option(
            ...,
            "--environment",
            "-e",
            envvar="ES_ENV_NAME",
            show_envvar=False,
            show_default=False,
            rich_help_panel="Options",
            help="Environment name config.",
        ),
    ] = None,
    junitxml: Annotated[
        Optional[str],
        typer.Option(
            ...,
            "--junitxml",
            help="Path to write JUnit XML results (directories will be created if missing).",
            rich_help_panel="Options",
            show_default=False,
        ),
    ] = None,
    export_failures: Annotated[
        Optional[str],
        typer.Option(
            ...,
            "--export-failures",
            help="Path to write failed test data to an Excel (.xlsx) file (directories will be created if missing).",
            rich_help_panel="Options",
            show_default=False,
        ),
    ] = None,
) -> None:
    """
    Run all tests.
    :return:
    """
    s_t = time.time()
    print("================================================================")
    print("[bold]Test Suite[/bold]")
    print("================================================================")
    display_test_names_table()
    print("\n================================================================")
    print("[bold]Starting Async EchoSphere Test Run[/bold]")
    print("================================================================")

    results: list[TestResult] = []
    test_files: dict[str, TestFileInfo] = get_sql_test_files()
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures: list[concurrent.futures.Future[TestResult]] = []
        for t_n, t_fp in test_files.items():
            fut = executor.submit(
                run_async_test_and_poll,
                t_n,
                t_fp["full_path"],
                env,
                bool(export_failures),
            )
            futures.append(cast(concurrent.futures.Future[TestResult], fut))  # type: ignore
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    # Export JUnit XML if requested
    if junitxml:
        try:
            j_exporter = JUnitXmlExporter()
            j_exporter.add_results(results)
            abs_path = j_exporter.write_to_file(junitxml)
            console.print(f"[bold green]JUnit XML results written to:[/bold green] {abs_path}")
        except Exception as e:
            console.print(f"[bold red]Failed to write JUnit XML:[/bold red] {e}")

    # Export failed test details to Excel if requested
    if export_failures:
        try:
            e_exporter = FailedTestExporter()
            e_exporter.add_results(results)
            abs_xlsx = e_exporter.write_to_file(export_failures)
            failed_count = sum(1 for r in results if not r.passed)
            console.print(
                f"[bold green]Failed test data exported to:[/bold green] {abs_xlsx} ({failed_count} tests exported)"
            )
        except Exception as e:
            console.print(f"[bold red]Failed to export failed test data:[/bold red] {e}")

    e_t = time.time()
    cum_t = round(e_t - s_t, 3)
    print("================================================================")
    if len(results) == 0:
        print("[bold]No Tests Executed.[/bold]")
        sys.exit(-1)
    if all(r.passed for r in results):
        print(f"[bold green]Test Run Successful. [/green bold][yellow bold]{cum_t}s[/yellow bold]")
    else:
        print(f"[bold red]Test Run Failed. [/red bold][yellow bold]{cum_t}s[/yellow bold]")
        sys.exit(-1)


if __name__ == "__main__":
    app()
