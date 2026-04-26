# Command Reference

The `es` CLI is the operational core of EchoSphere's "pytest for databases" workflow.

This section documents all EchoSphere CLI commands, their options, and examples.

EchoSphere uses the `es` command with subcommands.

## Global Behavior
- `-h`, `--help` shows help for any command.
- Exit code 0: success, non‑zero: failure.
- Some options accept environment variables for convenience.

## es init
Initialize EchoSphere for your platform and scaffold a suite and configuration.

Usage:
```sh
es init --platform snowflake
es init --platform postgres
es init --platform databricks
es init --platform sqlite
es init --platform tutorial
```

- --platform PLATFORM
  - Required. Select the target platform to configure.
  - Supported values: `snowflake`, `postgres`, `databricks`, `sqlite`, `tutorial`.

What it does:
- Creates the default `es_suite/` directory (if missing) with example SQL tests
- Generates a configuration file (`es.ini`) with environment stanzas
- `tutorial` additionally creates and seeds a local SQLite database (`./.echosphere/tutorial.db` by default).
- If `es_suite/` or `es.ini` already exist, those parts are skipped.

## es run
Run all discovered tests concurrently.

Usage:
```sh
# choose environment via CLI
es run --environment env.snowflake.dev

# or via environment variable
ES_ENV_NAME=env.snowflake.dev es run

# export JUnit XML and failed rows to Excel
es run -e env.snowflake.dev --junitxml reports/junit.xml --export-failures reports/failures.xlsx

# run only tagged tests
es run --tag critical

# exclude slow tests
es run --exclude-tag slow

# combine repeated and CSV tag filters
es run --tag critical --tag nightly,smoke --exclude-tag slow
```

Options:
- -e, --environment NAME
  - Select the environment to run against.
  - Environment variable: `ES_ENV_NAME` (if set, you may omit `-e`).
- --junitxml PATH
  - Write JUnit XML results to PATH (directories will be created if missing).
- --export-failures PATH
  - Write an Excel (.xlsx) with failing test result rows to PATH (directories will be created if missing).
  - Captures up to 1000 rows per failed test (including column headers). May increase query time and warehouse/DB cost.
- --tag TAG
  - Run only tests that include at least one matching tag.
  - You can repeat this option or pass comma-separated values.
  - Tags come from SQL metadata comments like `-- @tag: critical, nightly`.
- --exclude-tag TAG
  - Skip tests that include any matching tag.
  - You can repeat this option or pass comma-separated values.

Behavior:
- Discovers tests in `es_suite/` and one nested subsuite level (`es_suite/<subsuite>/*.es.sql`)
- Reads optional metadata comments at the top of each SQL test (`@name`, `@tag`, `@timeout`)
- `@timeout` must be a positive integer (seconds)
- A test passes if the executed SQL returns zero rows
- If a test exceeds `@timeout`, it is marked as failed
- Runs tests concurrently and prints a summary
- Non‑zero exit on any failure

## es view
Explore your suite: list tests or display the SQL code of a single test.

### es view tests
List the test suite. You can show all tests or filter by subsuite.

```sh
# list all tests
es view tests --all

# filter by subsuite (subdirectory)
es view tests --suite smoke
```

Options:
- -a, --all
  - Show all tests regardless of subsuite.
- -s, --suite NAME
  - Filter tests by subsuite. Cannot be used together with `--all`.
  - The subsuite name corresponds to the immediate subdirectory under `es_suite/`.

### es view test
Print the SQL code for a given test.

```sh
# show SQL for a test named orders_total.es.sql in the root suite
es view test orders_total

# or when inside a subsuite
es view test smoke/orders_total
```

Parameters:
- name: The test identifier, optionally including subsuite as `<subsuite>/<test_name>`.
