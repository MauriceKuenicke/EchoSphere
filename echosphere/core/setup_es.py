import importlib.resources
import os
from enum import Enum
from pathlib import Path

import typer

SETUP_FILES_DIR = "ini_setup_files"
EXAMPLE_QUERY_DIR = "example_query_setup_files"
INIT_FILE_TO_BE_CREATED_NAME = "es.ini"
ES_SUITE_TO_BE_CREATED_DEFAULT_DIR = "es_suite"


class PlatformEnum(str, Enum):
    SNOWFLAKE = "snowflake"
    # DATABRICKS = "databricks"
    # POSTGRES = "postgres"
    # SQLITE = "sqlite"


def get_resource_path(dir_name, resource_name):
    with importlib.resources.path(f"echosphere.core.{dir_name}", resource_name) as path:
        return path


SETUP_INI_FILE_MAPPING = {
    PlatformEnum.SNOWFLAKE.value: get_resource_path(SETUP_FILES_DIR, "snowflake.ini"),
}


def create_file_if_not_exists(file_path, content):
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            file.write(content)
        return True
    return False


def setup_es_directory(dir_name: str) -> None:
    es_suite_path = Path(dir_name)
    if es_suite_path.exists():
        typer.echo(f"Directory '{dir_name}' already exists. Skipping creation.")
        return

    es_suite_path.mkdir()
    example_query_content = get_resource_path(EXAMPLE_QUERY_DIR, "EXAMPLE.es.sql").read_text()
    example_query_path = es_suite_path / "EXAMPLE.es.sql"
    create_file_if_not_exists(example_query_path, example_query_content)
    typer.echo(f"Created '{dir_name}' directory with example query file.")


def setup_config_file(platform: str) -> None:
    config_content = SETUP_INI_FILE_MAPPING[platform].read_text()

    if create_file_if_not_exists(INIT_FILE_TO_BE_CREATED_NAME, config_content):
        typer.echo(f"Created '{INIT_FILE_TO_BE_CREATED_NAME}' configuration file.")
    else:
        typer.echo(f"File '{INIT_FILE_TO_BE_CREATED_NAME}' already exists. Skipping creation.")


def init_es(platform: str, dir_name: str = ES_SUITE_TO_BE_CREATED_DEFAULT_DIR):
    setup_es_directory(dir_name)
    setup_config_file(platform)
