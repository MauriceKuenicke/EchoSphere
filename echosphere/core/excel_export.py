from __future__ import annotations

import os
import re
from collections.abc import Iterable
from typing import Any

from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.worksheet.worksheet import Worksheet

from echosphere.core.test_result import TestResult

INVALID_SHEET_CHARS = r"[\\/*?:\[\]]"  # Excel-invalid sheet name characters
MAX_SHEET_NAME_LEN = 31


class FailedTestExporter:
    """
    Exports failed EchoSphere tests into an Excel workbook. Each failed test gets its own worksheet.
    """

    def __init__(self) -> None:
        """
        A class responsible for managing and storing test results.
        """
        self._results: list[TestResult] = []

    def add_results(self, results: Iterable[TestResult]) -> None:
        """
        Adds test results to the result list if they are not marked as passed.

        :param results: An iterable collection of TestResult objects to be processed.
        """
        for r in results:
            if not r.passed:
                self._results.append(r)

    @staticmethod
    def _sanitize_sheet_name(name: str, used: set[str]) -> str:
        """
        Sanitizes a sheet name by replacing invalid characters, enforcing a maximum length,
        and ensuring uniqueness among already used sheet names.

        :param name: The original name of the sheet to be sanitized.
        :param used: A set of already used sheet names to ensure the new name is unique.
        :return: A sanitized and unique sheet name.
        """
        # Replace invalid characters
        sanitized = re.sub(INVALID_SHEET_CHARS, "_", name)
        # Trim to max length
        sanitized = sanitized[:MAX_SHEET_NAME_LEN].strip()
        if not sanitized:
            sanitized = "Sheet"
        base = sanitized
        i = 1
        # Ensure uniqueness
        while sanitized in used:
            suffix = f" ({i})"
            trimmed = base[: MAX_SHEET_NAME_LEN - len(suffix)]
            sanitized = f"{trimmed}{suffix}"
            i += 1
        used.add(sanitized)
        return sanitized

    @staticmethod
    def _auto_fit_columns(ws: Worksheet) -> None:
        """
        Automatically adjusts the width of columns in the given worksheet based on the
        content lengths. This method ensures that columns are wide enough to display
        cell contents clearly while maintaining a reasonable maximum width.

        :param ws: The worksheet object whose column widths need to be adjusted.
        :return: None
        """
        # Compute max width per column based on string length, with cap
        max_width: dict[Any, Any] = {}
        for row in ws.iter_rows(values_only=True):
            for idx, cell in enumerate(row, start=1):
                val = "" if cell is None else str(cell)
                max_width[idx] = max(max_width.get(idx, 0), len(val))
        for idx, width in max_width.items():
            # Set a reasonable cap to prevent extreme widths
            ws.column_dimensions[ws.cell(row=1, column=idx).column_letter].width = min(max(10, width + 2), 80)

    def write_to_file(self, path: str) -> str:
        """
        Writes the test results to an Excel file at the specified path.

        :param path: The relative or absolute path where the Excel file will be written.
            If the file extension is not `.xlsx`, it will be added automatically.
        :return: The absolute path of the created Excel file.
        """
        if not path.lower().endswith(".xlsx"):
            path = f"{path}.xlsx"

        abs_path = os.path.abspath(path)
        dir_name = os.path.dirname(abs_path)
        if dir_name and not os.path.exists(dir_name):
            try:
                os.makedirs(dir_name, exist_ok=True)
            except OSError as e:
                raise Exception(f"Failed to create directories for path '{abs_path}': {e}")

        wb = Workbook()
        # Remove the default sheet created by openpyxl if present, and we have failures
        if self._results:
            default_ws = wb.active
            wb.remove(default_ws)

        used_names: set[str] = set()
        header_font = Font(bold=True)
        meta_label_font = Font(bold=True)
        wrap_alignment = Alignment(wrap_text=True, vertical="top")

        for r in self._results:
            sheet_name = self._sanitize_sheet_name(r.name, used_names)
            ws = wb.create_sheet(title=sheet_name)

            # Metadata section
            meta_rows = [
                ("Test Name:", r.name),
                ("Execution Time:", f"{r.duration:.3f} seconds"),
                ("Failed With:", f"{r.row_count} rows (showing first 1,000)"),
                ("SQL Query:", r.sql),
                ("Execution Timestamp:", r.timestamp.replace(microsecond=0).isoformat()),
            ]
            row_idx = 1
            for label, value in meta_rows:
                ws.cell(row=row_idx, column=1, value=label).font = meta_label_font
                cell = ws.cell(row=row_idx, column=2, value=value)
                cell.alignment = wrap_alignment
                row_idx += 1

            # Blank row before data
            row_idx += 1

            # Data section
            columns = r.failure_columns or []
            rows = r.failure_rows or []

            # Header
            for col_idx, col_name in enumerate(columns, start=1):
                c = ws.cell(row=row_idx, column=col_idx, value=col_name)
                c.font = header_font
            header_row = row_idx

            # Data rows
            for dr in rows:
                row_idx += 1
                for col_idx, cell_val in enumerate(dr, start=1):
                    if isinstance(cell_val, datetime):
                        cell_val = cell_val.replace(tzinfo=None)
                    ws.cell(row=row_idx, column=col_idx, value=cell_val)

            # Freeze pane below header
            ws.freeze_panes = ws.cell(row=header_row + 1, column=1)

            # Auto-fit columns
            self._auto_fit_columns(ws)

        # If no failed results, still create an empty workbook with a note
        if not self._results:
            ws = wb.active
            ws.title = "No Failures"
            ws.cell(row=1, column=1, value="No failed tests to export.")

        try:
            print("BEFORE")
            wb.save(abs_path)
        except OSError as e:
            raise Exception(f"Failed to write Excel file to '{abs_path}': {e}")

        return abs_path
