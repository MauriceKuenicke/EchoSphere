import glob
import os
import re
from typing import TypedDict

SQL_FILE_EXT = ".es.sql"
METADATA_PATTERN = re.compile(r"^\s*--\s*@(?P<key>name|tag|timeout)\s*:\s*(?P<value>.*?)\s*$", re.IGNORECASE)


class TestFileInfo(TypedDict):
    """Typed information about a discovered SQL test file."""

    full_path: str
    subfolder: str | None
    name: str | None
    tags: list[str]
    timeout: int | None


def _parse_timeout(value: str, file_path: str) -> int:
    """
    Parse timeout metadata as a positive integer number of seconds.

    :param value: Raw timeout value from metadata comment.
    :param file_path: SQL file path for contextual error reporting.
    :return: Parsed timeout in seconds.
    """
    timeout_str = value.strip()
    try:
        timeout_seconds = int(timeout_str)
    except ValueError as exc:
        raise ValueError(f"Invalid @timeout value '{value}' in '{file_path}'. Expected a positive integer.") from exc

    if timeout_seconds <= 0:
        raise ValueError(f"Invalid @timeout value '{value}' in '{file_path}'. Expected a value greater than zero.")
    return timeout_seconds


def parse_sql_test_metadata(file_path: str) -> tuple[str | None, list[str], int | None]:
    """
    Parse supported metadata comments from the start of a SQL test file.

    Supported keys:
    - @name: Free-form display name
    - @tag: Comma-separated tags
    - @timeout: Positive integer timeout (seconds)

    Only metadata found in leading comment/blank lines is considered. Once the
    first non-comment SQL line appears, metadata parsing stops.

    :param file_path: Path to the SQL test file.
    :return: Tuple of (name, tags, timeout_seconds).
    """
    name: str | None = None
    tags: list[str] = []
    timeout: int | None = None

    with open(file_path, "r", encoding="utf-8") as sql_file:
        for raw_line in sql_file:
            line = raw_line.lstrip("\ufeff")
            stripped = line.strip()

            if not stripped:
                continue

            if not stripped.startswith("--"):
                break

            metadata_match = METADATA_PATTERN.match(stripped)
            if not metadata_match:
                continue

            key = metadata_match.group("key").lower()
            value = metadata_match.group("value").strip()

            if key == "name":
                name = value or None
            elif key == "tag":
                tags.extend(tag.strip().lower() for tag in value.split(",") if tag.strip())
            elif key == "timeout":
                timeout = _parse_timeout(value=value, file_path=file_path)

    deduped_tags = sorted(set(tags))
    return name, deduped_tags, timeout


def get_sql_test_files(
    path: str = "./es_suite",
    subdir: str | None = None,
    root_only: bool = False,
) -> dict[str, TestFileInfo]:
    """
    Generates a dictionary of SQL test file identifiers and their corresponding file information
    from the specified directory and its immediate subfolders. The function searches for files
    with the `.es.sql` extension and creates a mapping where the keys are the base names
    of the files (without the `.es.sql` suffix) in lower case, and the values are dictionaries
    containing the full path and subfolder information.

    :param path: Directory path where the `.es.sql` test files are stored. Defaults to "./es_suite".
    :param subdir: Optional subfolder name to filter results. If provided, only
                   files from this subfolder will be included.
    :param root_only: If True, only return tests in the root of `path` (no subfolders).
                      Ignored when `subdir` is set.
    :return: A dictionary mapping the base names of the `.es.sql` files to dictionaries containing:
             - 'full_path': The complete path to the file
             - 'subfolder': The subfolder name if the file is in a subfolder, None otherwise
             - 'name': Optional display name from metadata
             - 'tags': Normalized tags from metadata
             - 'timeout': Optional timeout in seconds from metadata
    """
    def process_file_path(f_p: str) -> tuple[str, str | None]:
        """Extract the file name and subfolder from a file path."""
        f_n = os.path.basename(f_p)[: -len(SQL_FILE_EXT)].lower()
        relative_path = os.path.relpath(f_p, path)
        subfolder = os.path.dirname(relative_path) if os.path.dirname(relative_path) else None
        return f_n, subfolder

    # Create the result dictionary
    file_info: dict[str, TestFileInfo] = {}

    # Process all files with the SQL extension (root only, or root + subfolders)
    all_patterns = (
        [os.path.join(path, f"*{SQL_FILE_EXT}")]
        if root_only and not subdir
        else [
            os.path.join(path, f"*{SQL_FILE_EXT}"),  # Main directory
            os.path.join(path, "*", f"*{SQL_FILE_EXT}"),  # Subfolders
        ]
    )

    for pattern in all_patterns:
        for file_path in glob.glob(pattern):
            file_name, folder = process_file_path(file_path)
            name, tags, timeout = parse_sql_test_metadata(file_path=file_path)

            # Skip if we are filtering by subfolder and this file is not in that subfolder
            if subdir and folder != subdir:
                continue

            file_info[file_name] = {
                "full_path": file_path,
                "subfolder": folder,
                "name": name,
                "tags": tags,
                "timeout": timeout,
            }

    return file_info
