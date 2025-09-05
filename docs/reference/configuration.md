# Configuration Reference

EchoSphere reads environment configuration from an `es.ini` file. This file defines one or more environments and a default.

## File Structure
```ini
[default]
env = env.snowflake.dev  # Name of the default environment (could also be env.postgres.dev)

[env.snowflake.dev]
platform = snowflake
user = ...
password = ...
account = ...
warehouse = ...
role = ...
database = ...
schema = ...

[env.snowflake.prod]
platform = snowflake
user = ...
password = ...
account = ...
warehouse = ...
role = ...
database = ...
schema = ...

[env.postgres.dev]
platform = postgres
host = ...
port = 5432
database = ...
schema = public
user = ...
password = ...
sslmode = ...  # optional
```

## Sections
- [default]
  - `env`: the environment name to use when no `--environment` is provided.
- [env.<platform>.<name>]
  - `platform`: `snowflake` or `postgres`.
  - For Snowflake: `user`, `password`, `account`, `warehouse`, `role`, `database`, `schema`.
  - For Postgres: `host`, `port`, `database`, `schema`, `user`, `password`, `sslmode` (optional).

## Selecting the Environment
- CLI option: `es run --environment dev`
- Environment variable: `ES_ENV_NAME=dev es run`

If neither is provided, EchoSphere uses the environment defined in `[default]`.

## Test Discovery
- EchoSphere discovers tests with the `.es.sql` suffix.
- Organize tests into subdirectories for logical grouping; all are discovered recursively.

## Runtime Options
- Parallel execution is enabled by default to speed up test runs.
- Export options:
  - `--junitxml PATH` — write JUnit XML report
  - `--export-failures PATH` — write failing rows to Excel (.xlsx)

## Best Practices for Configuration
- Avoid hardcoding secrets in `es.ini`. Use your secret store or CI secrets to template values at runtime.
- Use separate environments for dev/staging/prod with least privilege.
- Keep `database` and `schema` values environment-specific for flexibility.
