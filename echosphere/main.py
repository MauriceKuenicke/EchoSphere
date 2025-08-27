import concurrent.futures
import os
import sys
import time
from typing import Optional

import snowflake.connector
import typer
from rich import print
from rich.console import Console
from snowflake.connector import ProgrammingError
from typing_extensions import Annotated

from echosphere.commands import view
from echosphere.ConfigParser import SnowflakeAgentConfig
from echosphere.core.setup_es import PlatformEnum, init_es

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
def configure_setup(platform: PlatformEnum = typer.Option(None, help="Platform to configure.")):
    if platform is None:
        console.print(
            "[bold red]Error:[/bold red] Please specify a platform. Use [bold green]--help[/bold green] for more info."
        )
        raise typer.Exit(code=-1)
    init_es(platform)


def run_async_test_and_poll(test_name: str, test_file_path: str, agent: Optional[str]):
    test_run_successful = False
    sf_agent = SnowflakeAgentConfig(agent_name=agent)
    with snowflake.connector.connect(
        user=sf_agent.user,
        password=sf_agent.password,
        account=sf_agent.account,
        warehouse=sf_agent.warehouse,
        role=sf_agent.role,
        database=sf_agent.database,
        schema=sf_agent.schema,
        session_parameters={
            "QUERY_TAG": "EchoSphere Testing Suite Run",
        },
        application="EchoSphere",
    ) as conn:
        cur = conn.cursor()
        with open(test_file_path, "r") as s:
            sql = s.read()

        start_time = time.time()
        cur.execute_async(sql)

        try:
            qry_id = cur.sfqid
            while conn.is_still_running(conn.get_query_status(qry_id)):
                time.sleep(1)
        except ProgrammingError as err:
            raise Exception("Programming Error: {0}".format(err))

        end_time = time.time()
        execution_time = round(end_time - start_time, 3)
        cur.query_result(qry_id)
        row_count = cur.rowcount

    if row_count:
        error_msg = f"""{test_name}...[red bold]Failed[/red bold] [yellow bold]{execution_time}s[/yellow bold][red]
{sql}\nMore than zero rows ({row_count}) detected.[/red]"""
        print(error_msg)
    else:
        print(f"{test_name}...[green bold]Passed[/green bold] [yellow bold]{execution_time}s[/yellow bold]")
        test_run_successful = True
    return test_run_successful


@app.command(name="run", help="""Run the current test suite.""")
def run_suite(
    agent: Annotated[
        Optional[str],
        typer.Option(
            ...,
            "--agent",
            "-a",
            envvar="ES_AGENT_NAME",
            show_envvar=False,
            show_default=False,
            rich_help_panel="Options",
            help="Agent name config.",
        ),
    ] = None,
):
    """
    Run all tests.
    :return:
    """
    s_t = time.time()
    print("================================================================")
    print("[bold]Test Suite[/bold]")
    print("================================================================")
    display_test_names_table()
    print("================================================================")
    print("[bold]Starting Async EchoSphere Test Run[/bold]")
    print("================================================================")

    results = []
    test_files = get_sql_test_files()
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(run_async_test_and_poll, t_n, t_fp, agent) for t_n, t_fp in test_files.items()]
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
