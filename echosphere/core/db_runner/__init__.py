from typing import Type

from echosphere.core.db_runner.BaseClass import BaseRunner
from echosphere.core.platforms import PlatformEnum


def get_db_runner(platform: str) -> Type[BaseRunner]:
    if platform == "snowflake":
        try:
            from echosphere.core.db_runner.SnowflakeRunner import SnowflakeRunner as Runner
        except ImportError:
            raise ImportError(
                "This feature requires the snowflake extra. Install with 'pip install EchoSphere[snowflake]'"
            )
    elif platform == "postgres":
        try:
            from echosphere.core.db_runner.PostgresRunner import PostgresRunner as Runner  # type: ignore [assignment]
        except ImportError:
            raise ImportError(
                "This feature requires the postgres extra. Install with 'pip install EchoSphere[postgres]'"
            )
    elif platform == "databricks":
        try:
            from echosphere.core.db_runner.DatabricksRunner import (  # type: ignore [assignment]
                DatabricksRunner as Runner,
            )
        except ImportError:
            raise ImportError(
                "This feature requires the databricks extra. Install with 'pip install EchoSphere[databricks]'"
            )
    else:
        raise Exception(f"Unsupported platform name found in .ini file. Should be one of: [{','.join(PlatformEnum)}]")
    return Runner
