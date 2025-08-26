import glob
import os
from typing import Optional


def get_sql_test_files(path: str = "./es_suite", subdir: Optional[str] = None) -> dict[str, dict[str, Optional[str]]]:
    """
    Generates a dictionary of SQL test file identifiers and their corresponding file information
    from the specified directory and its immediate subfolders. The function searches for files
    with the `.es.sql` extension and creates a mapping where the keys are the base names
    of the files (without the `.es.sql` suffix) in lower case, and the values are dictionaries
    containing the full path and subfolder information.

    :param path: Directory path where the `.es.sql` test files are stored. Defaults to "./es_suite".
    :param subdir: Optional subfolder name to filter results. If provided, only
                   files from this subfolder will be included.
    :return: A dictionary mapping the base names of the `.es.sql` files to dictionaries containing:
             - 'full_path': The complete path to the file
             - 'subfolder': The subfolder name if the file is in a subfolder, None otherwise
    """
    SQL_FILE_EXT = ".es.sql"

    def process_file_path(f_p: str) -> tuple[str, Optional[str]]:
        """Extract the file name and subfolder from a file path."""
        f_n = os.path.basename(f_p)[: -len(SQL_FILE_EXT)].lower()
        relative_path = os.path.relpath(f_p, path)
        subfolder = os.path.dirname(relative_path) if os.path.dirname(relative_path) else None
        return f_n, subfolder

    # Create the result dictionary
    file_info: dict[str, dict[str, Optional[str]]] = {}

    # Process all files with the SQL extension (both in the main dir and subfolders)
    all_patterns = [
        os.path.join(path, f"*{SQL_FILE_EXT}"),  # Main directory
        os.path.join(path, "*", f"*{SQL_FILE_EXT}"),  # Subfolders
    ]

    for pattern in all_patterns:
        for file_path in glob.glob(pattern):
            file_name, folder = process_file_path(file_path)

            # Skip if we are filtering by subfolder and this file is not in that subfolder
            if subdir and folder != subdir:
                continue

            file_info[file_name] = {"full_path": file_path, "subfolder": folder}

    return file_info
