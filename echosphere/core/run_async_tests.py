from rich import print

from echosphere.core.db_runner.SnowflakeRunner import SnowflakeRunner
from echosphere.env_config_parser.PlatformExtractor import PlatformExtractor

FAILED_TEST_MESSAGE = "{test_name}...[red bold]Failed[/red bold] [yellow bold]{execution_time}s[/yellow bold][red]\n{sql}\nMore than zero rows ({row_count}) detected.[/red]"
SUCCESS_TEST_MESSAGE = "{test_name}...[green bold]Passed[/green bold] [yellow bold]{execution_time}s[/yellow bold]"


def run_async_test_and_poll(test_name: str, test_file_path: str, env: str | None) -> bool:
    """
    Run a single SQL test asynchronously on the configured platform and evaluate its result.

    A test is considered successful when the executed query returns zero rows.

    :param test_name: Human-friendly identifier of the test (used for output).
    :param test_file_path: Full path to the SQL file to execute.
    :param env: Optional environment/agent name from es.ini; if None, default is used.
    :return: True if the test passes (zero rows), False otherwise.
    """
    platform_name = PlatformExtractor.extract_platform_info(env_name=env)
    if platform_name not in ("snowflake",):
        raise Exception("Unsupported platform name found in .ini file. Should be one of: [snowflake]")

    if platform_name == "snowflake":
        row_count, execution_time, sql = SnowflakeRunner.dispatch_test(env=env, test_file_path=test_file_path)
    else:
        raise Exception("Unsupported platform name found in .ini file. Should be one of: [snowflake]")

    if row_count:
        error_msg = FAILED_TEST_MESSAGE.format(
            test_name=test_name, execution_time=execution_time, sql=sql, row_count=row_count
        )
        print(error_msg)
        return False

    success_message = SUCCESS_TEST_MESSAGE.format(test_name=test_name, execution_time=execution_time)
    print(success_message)
    return True
