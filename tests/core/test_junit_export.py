import os
import xml.etree.ElementTree as ET
from datetime import datetime

from echosphere.core.junit_export import JUnitXmlExporter
from echosphere.core.test_result import TestResult


def _sample_results(now: datetime) -> list[TestResult]:
    return [
        TestResult(
            name="Validate Customer Data",
            passed=True,
            duration=0.823,
            sql="SELECT 1;",
            row_count=0,
            timestamp=now,
        ),
        TestResult(
            name="Check Order Integrity",
            passed=False,
            duration=0.934,
            sql=(
                "SELECT order_id, customer_id\nFROM orders\nWHERE customer_id NOT IN (SELECT customer_id FROM customers)"
            ),
            row_count=5,
            timestamp=now,
            failure_message="Test returned 5 rows. Expected 0 rows.",
        ),
        TestResult(
            name="Verify Product Inventory",
            passed=True,
            duration=0.699,
            sql="SELECT 1;",
            row_count=0,
            timestamp=now,
        ),
    ]


def test_junit_exporter_writes_valid_xml(tmp_path) -> None:
    now = datetime.fromisoformat("2023-07-15T14:30:24")
    exporter = JUnitXmlExporter()
    exporter.add_results(_sample_results(now))

    out_dir = tmp_path / "test-results"
    out_file = out_dir / "results.xml"
    abs_path = exporter.write_to_file(str(out_file))

    assert os.path.exists(abs_path)
    tree = ET.parse(abs_path)
    root = tree.getroot()

    # Root and suite checks
    assert root.tag == "testsuites"
    suite = root.find("testsuite")
    assert suite is not None
    assert suite.get("name") == "EchoSphere SQL Tests"
    assert suite.get("tests") == "3"
    assert suite.get("failures") == "1"
    assert suite.get("errors") == "0"
    assert suite.get("skipped") == "0"
    assert suite.get("timestamp") == now.replace(microsecond=0).isoformat()

    # Testcase checks
    tcs = list(suite.findall("testcase"))
    assert len(tcs) == 3
    names = [tc.get("name") for tc in tcs]
    assert "Validate Customer Data" in names
    assert "Check Order Integrity" in names
    assert "Verify Product Inventory" in names

    # Failure content check
    fail_tc = next(tc for tc in tcs if tc.get("name") == "Check Order Integrity")
    failure = fail_tc.find("failure")
    assert failure is not None
    assert "Row count: 5" in (failure.text or "")


def test_junit_exporter_adds_xml_extension_when_missing(tmp_path) -> None:
    now = datetime.now()
    exporter = JUnitXmlExporter()
    exporter.add_result(
        TestResult(
            name="Example",
            passed=True,
            duration=0.1,
            sql="SELECT 1;",
            row_count=0,
            timestamp=now,
        )
    )

    out_path = tmp_path / "junit" / "report"  # no .xml
    written = exporter.write_to_file(str(out_path))
    assert written.endswith(".xml")
    assert os.path.exists(written)
