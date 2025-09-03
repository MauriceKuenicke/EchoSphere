# Command Reference

This section documents all EchoSphere CLI commands, their options, and examples.

EchoSphere uses the `es` command with subcommands.

## Global Behavior
- `-h`, `--help` shows help for any command.
- Exit code 0: success, non‑zero: failure.
- Some options accept environment variables for convenience.

## es setup
Initialize EchoSphere for your platform and scaffold a suite and configuration.

Usage:
```sh
es setup --platform SNOWFLAKE
```

- --platform PLATFORM
  - Required. Select the target platform to configure. Supported: `SNOWFLAKE`.

What it does:
- Creates a default tests directory
- Generates a configuration file (`es.ini`) with environment stanzas

## es run
Run all discovered tests concurrently.

Usage:
```sh
# choose environment via CLI
es run --environment dev

# or via environment variable
ES_ENV_NAME=dev es run

# export JUnit XML and failed rows to Excel
es run -e dev --junitxml reports/junit.xml --export-failures reports/failures.xlsx
```

Options:
- -e, --environment NAME
  - Select the environment to run against.
  - Environment variable: `ES_ENV_NAME` (if set, you may omit `-e`).
- --junitxml PATH
  - Write JUnit XML results to PATH (directories will be created if missing).
- --export-failures PATH
  - Write an Excel (.xlsx) with failing test result rows to PATH (directories will be created if missing).

Behavior:
- Discovers tests with the `.es.sql` suffix
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
