# Getting Started

This section helps you install EchoSphere, perform the first-time setup, and run a “Hello World” test in minutes.

- Installation
- Initial configuration
- Hello World: first test
- Key concepts
- 5‑minute quickstart

## Installation Options

### Using pip (recommended)
```sh
# Install from PyPI with platform extras:
# Snowflake:
pip install EchoSphere[snowflake]
# Postgres:
pip install EchoSphere[postgres]

# Alternatively, install latest from GitHub:
pip install git+https://github.com/MauriceKuenicke/EchoSphere
```

### From source (development)
```sh
# clone the repo
git clone https://github.com/MauriceKuenicke/EchoSphere
cd EchoSphere

# install in editable mode
pip install -e .[dev]
```

## Initial Configuration
After installation, run the setup command to scaffold a test suite and configuration:

```sh
es setup --platform SNOWFLAKE  # or POSTGRES
```

This will:
- create a default folder for your SQL tests
- create a configuration file for your platform credentials and environments

Note: If you omit the platform, EchoSphere will ask for one. Use `--help` to list platforms.

## Hello World: First Test
1. Create a file named `example.es.sql` in your tests directory.
2. Paste a simple query that fails only when your expectation is violated:

```sql
SELECT 1 WHERE 1 <> 1;  -- returns zero rows, therefore passes
```

3. Run the test suite:
```sh
es run --environment dev
```

- Success: exit code 0, no failing tests
- Failure: non‑zero exit code; failed tests are reported with their returned rows

Tip: You can export results to JUnit XML and export failing rows to Excel. See the Command Reference for details.

## Key Concepts
- Test success: a test passes if the SQL returns zero rows.
- Naming: use the `.es.sql` suffix so EchoSphere can discover your tests.
- Environments: define credentials and defaults in `es.ini` for your platform; select at runtime with `--environment` or the `ES_ENV_NAME` env var.
- Parallelism: tests are executed concurrently to minimize runtime.

## 5‑Minute Quickstart
1. Install EchoSphere
2. Run `es setup --platform SNOWFLAKE` or `es setup --platform POSTGRES`
3. Configure your platform credentials in `es.ini`
4. Add `orders_total.es.sql` with your first assertion query
5. Run `es run -e dev` and inspect the output
6. Optional: `es run -e dev --junitxml reports/junit.xml --export-failures reports/failures.xlsx`
