import concurrent.futures
import sys
import time
from typing import Optional

import typer
from rich import print
from rich.console import Console
from typing_extensions import Annotated

from echosphere.commands import view
from echosphere.core.run_async_tests import run_async_test_and_poll
from echosphere.core.setup_es import PlatformEnum, init_es
from echosphere.core.suite_display import display_test_names_table
from echosphere.utils.sql_test_fetcher import get_sql_test_files

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

    results = []
    test_files = get_sql_test_files()
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = [
            executor.submit(run_async_test_and_poll, t_n, t_fp["full_path"], env)  # type: ignore[arg-type]
            for t_n, t_fp in test_files.items()
        ]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    e_t = time.time()
    cum_t = round(e_t - s_t, 3)
    print("================================================================")
    if len(results) == 0:
        print("[bold]No Tests Executed.[/bold]")
        sys.exit(-1)
    if all(results):
        print(f"[bold green]Test Run Successful. [/green bold][yellow bold]{cum_t}s[/yellow bold]")
    else:
        print(f"[bold red]Test Run Failed. [/red bold][yellow bold]{cum_t}s[/yellow bold]")
        sys.exit(-1)


if __name__ == "__main__":
    app()
