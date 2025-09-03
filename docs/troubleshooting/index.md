# Troubleshooting

Having issues? This guide helps you diagnose and fix common problems.

## Connection Problems
- Symptom: authentication or network errors.
- Checks:
  - Verify `es.ini` credentials for the selected environment.
  - Ensure your Snowflake account, role, warehouse, database, and schema are correct.
  - Confirm network access to Snowflake from your environment/CI.

## No Tests Discovered
- Symptom: EchoSphere reports zero tests executed.
- Checks:
  - Ensure test files end with `.es.sql`.
  - Verify your tests directory path and that files are readable.
  - Run `es view tests --all` to see what EchoSphere detects.

## Failing Tests Without Clear Cause
- Use `es view test <name>` to print the SQL and review logic.
- Inspect the failing rows (export with `--export-failures` for deeper analysis).
- Temporarily narrow the scope (e.g., one partition/day) to isolate the issue.

## Slow Test Runs
- Check Performance Optimization for tips (parallelism, query tuning, resource sizing).
- Split very heavy checks into smaller targeted tests.

## CI Fails but Works Locally
- Ensure `es.ini` is templated correctly in CI and secrets are passed.
- Match Python versions and dependency versions between local and CI.
- Publish JUnit XML and view CI test logs for details.

## When to File a Bug Report
- Provide EchoSphere version, platform details, minimal reproduction (test SQL), and logs.
- Open an issue on GitHub with all relevant context and redacted credentials.
