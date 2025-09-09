import importlib.resources
from enum import Enum
from pathlib import Path


class PlatformEnum(str, Enum):
    """Supported platforms for EchoSphere configuration."""

    SNOWFLAKE = "snowflake"
    DATABRICKS = "databricks"
    POSTGRES = "postgres"


SETUP_FILES_DIR = "ini_setup_files"
EXAMPLE_QUERY_DIR = "example_query_setup_files"

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
    PlatformEnum.DATABRICKS.value: get_resource_path(SETUP_FILES_DIR, "databricks.ini"),
}

EXAMPLE_SQL_FOLDER_MAPPING = {
    PlatformEnum.SNOWFLAKE.value: importlib.resources.files(f"echosphere.core.{EXAMPLE_QUERY_DIR}.snowflake"),
    PlatformEnum.POSTGRES.value: importlib.resources.files(f"echosphere.core.{EXAMPLE_QUERY_DIR}.postgres"),
    PlatformEnum.DATABRICKS.value: importlib.resources.files(f"echosphere.core.{EXAMPLE_QUERY_DIR}.databricks"),
}