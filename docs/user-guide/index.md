# User Guide

This section covers day-to-day workflows, environment setup, writing effective tests, and how to run and read results.

- Commands overview
- Environment configuration
- Writing tests
- Best practices
- Troubleshooting

Use this guide if you prefer task-oriented, practical how‑to instructions.

## Typical Workflow
1. Initialize: `es setup --platform SNOWFLAKE` or `es setup --platform POSTGRES`
2. Configure `es.ini` with credentials and defaults
3. Create tests: add `.es.sql` files expressing assertions
4. Run: `es run -e dev`
5. Inspect output, and optionally export reports (JUnit XML / Excel)
6. Commit tests to version control and run in CI

## Reading Test Output
- EchoSphere prints a summary table of discovered tests and a final success/failure status.
- Pass criteria: a test passes if the executed SQL returns zero rows.
- Exit codes: 0 for success, non‑zero for failure — ideal for CI gates.
- Optional exports:
  - `--junitxml path/to/results.xml` to integrate with CI test report viewers
  - `--export-failures path/to/failures.xlsx` to capture failing row details (captures up to 1000 rows per failed test, including column headers)

## Environments
Set your active environment via:
- CLI: `es run --environment dev`
- Environment variable: `ES_ENV_NAME=dev es run`

See Reference → Configuration for the `es.ini` format and fields.
