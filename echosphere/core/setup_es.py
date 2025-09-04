import importlib.resources
import os
from enum import Enum
from pathlib import Path
from typing import Union

import typer

SETUP_FILES_DIR = "ini_setup_files"
EXAMPLE_QUERY_DIR = "example_query_setup_files"
INIT_FILE_TO_BE_CREATED_NAME = "es.ini"
ES_SUITE_TO_BE_CREATED_DEFAULT_DIR = "es_suite"


class PlatformEnum(str, Enum):
    """Supported platforms for EchoSphere configuration."""

    SNOWFLAKE = "snowflake"
    # DATABRICKS = "databricks"
    POSTGRES = "postgres"
    # SQLITE = "sqlite"


def get_resource_path(dir_name: str, resource_name: str) -> Path:
    """
    Return a Path to a packaged resource.

    :param dir_name: Name of the resource directory within `echosphere.core`.
    :param resource_name: File name of the resource to resolve.
    :return: Filesystem path to the requested resource.
    """
    with importlib.resources.path(f"echosphere.core.{dir_name}", resource_name) as path:
        return path


SETUP_INI_FILE_MAPPING = {
    PlatformEnum.SNOWFLAKE.value: get_resource_path(SETUP_FILES_DIR, "snowflake.ini"),
    PlatformEnum.POSTGRES.value: get_resource_path(SETUP_FILES_DIR, "postgres.ini"),
}

EXAMPLE_SQL_FOLDER_MAPPING = {
    PlatformEnum.SNOWFLAKE.value: importlib.resources.files(f"echosphere.core.{EXAMPLE_QUERY_DIR}.snowflake"),
    PlatformEnum.POSTGRES.value: importlib.resources.files(f"echosphere.core.{EXAMPLE_QUERY_DIR}.postgres"),
}


def create_file_if_not_exists(file_path: Union[str, Path], content: str) -> bool:
    """
    Create a file with the given content if it does not already exist.

    :param file_path: Target file path.
    :param content: Text content to write to the file when created.
    :return: True if the file was created, False if it already existed.
    """
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            file.write(content)
        return True
    return False


def setup_es_directory(dir_name: str, platform: Union[str, PlatformEnum]) -> None:
    """
    Create the default `es_suite` directory and an example SQL test file.

    If the directory already exists, creation is skipped and a message is printed.

    :param platform: platform
    :param dir_name: Name of the directory to create for the test suite.
    :return: None
    """
    es_suite_path = Path(dir_name)
    if es_suite_path.exists():
        typer.echo(f"Directory '{dir_name}' already exists. Skipping creation.")
        return
    es_suite_path.mkdir()

    platform_key = platform.value if isinstance(platform, PlatformEnum) else platform
    example_query_dir_path = EXAMPLE_SQL_FOLDER_MAPPING[platform_key]

    for sql_file in example_query_dir_path.iterdir():
        if ".sql" in sql_file.name:
            example_query_content = sql_file.read_text()
            example_query_path = es_suite_path / sql_file.name
            create_file_if_not_exists(example_query_path, example_query_content)
    typer.echo(f"Created '{dir_name}' directory with example query file.")


def setup_config_file(platform: Union[str, PlatformEnum]) -> None:
    """
    Create the `es.ini` configuration file for the given platform.

    If the configuration file already exists, creation is skipped.

    :param platform: Target platform identifier (e.g., "snowflake"). Can be
                     provided as a `PlatformEnum` or a plain string.
    :return: None
    """
    platform_key = platform.value if isinstance(platform, PlatformEnum) else platform
    config_content = SETUP_INI_FILE_MAPPING[platform_key].read_text()

    if create_file_if_not_exists(INIT_FILE_TO_BE_CREATED_NAME, config_content):
        typer.echo(f"Created '{INIT_FILE_TO_BE_CREATED_NAME}' configuration file.")
    else:
        typer.echo(f"File '{INIT_FILE_TO_BE_CREATED_NAME}' already exists. Skipping creation.")


def init_es(platform: Union[str, PlatformEnum], dir_name: str = ES_SUITE_TO_BE_CREATED_DEFAULT_DIR) -> None:
    """
    Initialize EchoSphere structure and config for the selected platform.

    This performs two steps:
    1) Create the test suite directory with example SQL; 2) Create `es.ini`.

    :param platform: Target platform identifier as `PlatformEnum` or string.
    :param dir_name: Name of the directory to initialize for the suite.
    :return: None
    """
    setup_es_directory(dir_name, platform)
    setup_config_file(platform)
