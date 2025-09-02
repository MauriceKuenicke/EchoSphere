from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Sequence


@dataclass(slots=True)
class TestResult:
    """
    Represents the outcome of a single EchoSphere SQL test execution.
    """

    name: str
    passed: bool
    duration: float  # seconds
    sql: str
    row_count: int
    timestamp: datetime
    failure_message: Optional[str] = None

    # Optional data for failed tests export
    failure_columns: Optional[list[str]] = None
    failure_rows: Optional[list[Sequence[object]]] = None

    @property
    def status(self) -> str:
        return "pass" if self.passed else "fail"
