from __future__ import annotations

import os
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Iterable, List

from echosphere.core.test_result import TestResult


class JUnitXmlExporter:
    """
    Builds and writes JUnit XML results for EchoSphere test executions.
    """

    def __init__(self, suite_name: str = "EchoSphere SQL Tests", classname: str = "echosphere.sql_tests") -> None:
        """
        Initializes a test suite with a specified name and classname.

        :param suite_name: Name of the test suite. Defaults to "EchoSphere SQL Tests".
        :param classname: Identifier for the class associated with the test suite.
                          Defaults to "echosphere.sql_tests".
        """
        self.suite_name = suite_name
        self.classname = classname
        self._results: List[TestResult] = []

    def add_result(self, result: TestResult) -> None:
        """
        Appends a given ``TestResult`` object to the internal results storage.

        :param result: The ``TestResult`` instance that represents the test outcome to
            be added.
        """
        self._results.append(result)

    def add_results(self, results: Iterable[TestResult]) -> None:
        """
        Adds multiple test results to the current collection.

        :param results: An iterable of `TestResult` objects representing test
            outcomes to be added.
        """
        for r in results:
            self.add_result(r)

    def _build_xml_tree(self) -> ET.ElementTree:
        """
        Builds an XML tree representation for test results, encapsulating the details
        of the test cases, their execution times, and the results such as passed,
        failures, skipped, and errors.

        :return: An ElementTree object representing the complete XML tree for the
            test results.
        """
        tests = len(self._results)
        failures = sum(1 for r in self._results if not r.passed)
        errors = 0
        skipped = 0
        total_time = round(sum(r.duration for r in self._results), 3) if self._results else 0.0
        # Use the timestamp of the first test, or now if none
        suite_timestamp_dt: datetime = self._results[0].timestamp if self._results else datetime.now()
        suite_timestamp = suite_timestamp_dt.replace(microsecond=0).isoformat()

        root = ET.Element("testsuites")
        suite = ET.SubElement(
            root,
            "testsuite",
            attrib={
                "name": self.suite_name,
                "tests": str(tests),
                "failures": str(failures),
                "errors": str(errors),
                "skipped": str(skipped),
                "time": f"{total_time:.3f}",
                "timestamp": suite_timestamp,
            },
        )

        for r in self._results:
            tc = ET.SubElement(
                suite,
                "testcase",
                attrib={
                    "name": r.name,
                    "classname": self.classname,
                    "time": f"{r.duration:.3f}",
                },
            )
            if not r.passed:
                failure = ET.SubElement(
                    tc,
                    "failure",
                    attrib={
                        "message": r.failure_message or "Test failed",
                    },
                )
                # Detailed block (escaped by ElementTree)
                details_lines = [
                    "SQL:",
                    r.sql,
                    "",
                    f"Execution time: {r.duration:.3f}s",
                    f"Row count: {r.row_count}",
                ]
                failure.text = "\n" + "\n".join(details_lines) + "\n"

        return ET.ElementTree(root)

    def write_to_file(self, path: str) -> str:
        """
        Write the generated JUnit XML to the specified file path.
        Creates directories if they do not exist.

        :param path: Path to the output xml file.
        :return: The absolute path to the written file.
        """
        if not path.lower().endswith(".xml"):
            # Ensure xml extension for clarity
            path = f"{path}.xml"

        abs_path = os.path.abspath(path)
        dir_name = os.path.dirname(abs_path)
        if dir_name and not os.path.exists(dir_name):
            try:
                os.makedirs(dir_name, exist_ok=True)
            except OSError as e:
                raise Exception(f"Failed to create directories for path '{abs_path}': {e}")

        tree = self._build_xml_tree()
        try:
            tree.write(abs_path, encoding="utf-8", xml_declaration=True)
        except OSError as e:
            raise Exception(f"Failed to write JUnit XML file to '{abs_path}': {e}")

        return abs_path
