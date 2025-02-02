import typer
import os
import sys
import glob
from rich.console import Console
from rich.table import Table
import snowflake.connector
from rich import print
import concurrent.futures
from snowflake.connector import ProgrammingError
from echosphere.ConfigParser import SnowflakeAgentConfig
from typing_extensions import Annotated
import time
from typing import Optional


def get_sql_test_files(path: Optional[str] = "./es_suite") -> dict[str, str]:
    """
    Generates a dictionary of SQL test file identifiers and their corresponding file paths
    from the specified directory. The function searches for files with the `.es.sql` extension
    within the provided directory path and creates a mapping where the keys are the base names
    of the files (without the `.es.sql` suffix) and the values are the full paths to those files.

    :param path: Optional; Directory path where the `.es.sql` test files are stored. If not
                 specified, defaults to "./es_suite".
    :type path: Optional[str]

    :return: A dictionary mapping the base names of the `.es.sql` files (without the file
             extension) to their full paths.
    """
    pattern = os.path.join(path, '*.es.sql')
    files = glob.glob(pattern)
    base_names = {os.path.basename(f)[:-7]: f
                  for f in files}
    return base_names

def display_test_names_table() -> None:
    test_files = get_sql_test_files()
    if len(test_files.keys()) == 0:
        print(f"[bold red]No tests detected.[/red bold]")
        sys.exit(-1)
    table = Table("To be executed")
    for i in test_files.keys():
        table.add_row(i)
    console.print(table)

console = Console()

app = typer.Typer(
    name="EchoSphere Testing Suite",
    help="Database Testing Suite.",
    context_settings={"help_option_names": ["-h", "--help"]},
    add_completion=False,
    pretty_exceptions_show_locals=True,
    pretty_exceptions_short=True,
)


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
                'QUERY_TAG': 'EchoSphere Testing Suite Run',
            },
            application="EchoSphere"
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
            raise Exception('Programming Error: {0}'.format(err))

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


@app.command(name="run",
             help="""Run the current test suite.""")
def run_suite(agent: Annotated[Optional[str], typer.Option(..., "--agent", "-a",
                                                           envvar="ES_AGENT_NAME", show_envvar=False,
                                                           show_default=False, rich_help_panel="Options",
                                                           help="Agent name config.")] = None):
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


@app.command(name="list",
             help="""List current test suite.""")
def list_test_suite():
    """
    List current test suite.

    This command retrieves a list of SQL test files and presents them in a
    structured table format. It uses the `Table` utility for formatting the
    output and prints it to the console.

    :raises RuntimeError: If there are issues in retrieving test files or
        displaying the table on the console.
    :return: None
    """
    display_test_names_table()


@app.command(name="setup",
             help="""Create the necessary setup.""")
def configure_setup():
    """
    Setup
    :return:
    """
    path = "./es_suite"
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        raise Exception("Sub-Directory already exists.")

    filename = os.path.join(path, "EXAMPLE.es.sql")
    with open(filename, 'w') as file:
        file.write("-- This is a sample SQL query. Each test query should return zero rows, if the test was successful.\n")
        file.write("SELECT * FROM table_name;\n")

    with open("es.ini", "w") as ini_file:
        example = """[default]
agent = agent.snowflake.dev
            
[agent.snowflake.dev]
user = ...
password = ...
account = ...
warehouse =...
role = ...
database = ...
schema = ...
            
[agent.snowflake.prod]
user = ...
password = ...
account = ...
warehouse = ...
role = ...
database = ...
schema = ...
"""
        ini_file.write(example)


if __name__ == "__main__":
    app()
