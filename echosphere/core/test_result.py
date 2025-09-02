from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


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

    @property
    def status(self) -> str:
        return "pass" if self.passed else "fail"
