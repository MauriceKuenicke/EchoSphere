# Supported Platforms

This page provides an overview of the platforms 
you can use to execute SQL-based tests and the necessary 
configuration values required for the setup.

## Supported
1. ![PostgreSQL](../assets/img/postgres.svg){ width=20 style="vertical-align: -3px" } [PostgreSQL](#postgresql) ✅
2. ![Snowflake](../assets/img/snowflake.svg){ width=20 style="vertical-align: -3px" } [Snowflake](#snowflake) ✅
3. ![Databricks](../assets/img/databricks.svg){ width=20 style="vertical-align: -3px" } [Databricks](#databricks) ✅
4. ![SQLite](../assets/img/sqlite.svg){ width=100 style="vertical-align: -6px" } [SQLite](#sqlite) ✅
5. Tutorial (SQLite local starter) ✅

## In Planning
3. [Firebolt](#) ❌
4. [AWS Redshift](#) ❌
5. [Azure Synapse](#) ❌
6. [Google BigQuery](#) ❌
7. [MS SQL Server](#) ❌

---

## ![PostgreSQL](../assets/img/postgres.svg){ width=28 style="vertical-align: -6px" } PostgreSQL

PostgreSQL is a powerful, open-source relational database system.:

**Configuration Values:**
- `host`: The hostname or IP address of your PostgreSQL server.
- `port`: The port on which PostgreSQL is running (default is `5432`).
- `dbname`: The name of the database to connect to.
- `user`: The username for authentication.
- `password`: The password for the user.
- `schema`: The schema to set in the current connection session.
- `sslmode` (optional): The SSL mode for the connection (e.g., `disable`, `allow`, `prefer`, `require`).

**Example Configuration File:**
```ini
[DEFAULT]
host = your-postgresql-host
port = 5432
dbname = your-database-name
user = your-username
password = your-password
schema = your-schema-name
sslmode = disable
```

---

## ![Snowflake](../assets/img/snowflake.svg){ width=28 style="vertical-align: -6px" } Snowflake

Snowflake is a fully managed cloud data platform that supports scalable storage and high-performance analytics.
Here is how to configure Snowflake for executing your SQL-based tests.

**Configuration Values:**
- `account`: Your Snowflake account identifier 
- `user`: The username for Snowflake authentication.
- `password`: The password for your Snowflake account.
- `warehouse`: The name of the virtual warehouse to use for computations.
- `database`: The name of the database to connect to.
- `schema`: The schema to use within the specified database.
- `role` (optional): The role to assume for the session (default is the user's default role).

**Example Configuration File:**
```ini
[DEFAULT]
account = your-snowflake-account
user = your-snowflake-user
password = your-snowflake-password
warehouse = your-virtual-warehouse
database = your-database
schema = your-schema-name
role = your-role-name
```



---

## ![Databricks](../assets/img/databricks.svg){ width=28 style="vertical-align: -6px" } Databricks

Databricks provides a cloud-based data analytics platform
and SQL-based querying engine.:

**Configuration Values:**
- `server_hostname`: The Databricks server's hostname.
- `http_path`: The HTTP Path of the Databricks SQL endpoint.
- `access_token`: Your personal access token for authentication.

**Example Configuration File:**
```ini
[DEFAULT]
server_hostname = your-databricks-hostname
http_path = your-databricks-http-path
access_token = your-access-token
```

---

## SQLite

SQLite uses a local file database and requires only a database file path.

**Configuration Values:**
- `database`: Relative or absolute path to the SQLite `.db` file.

**Example Configuration File:**
```ini
[default]
env = env.sqlite.dev

[env.sqlite.dev]
platform = sqlite
database = ./.echosphere/tutorial.db
```

---

## Tutorial

`TUTORIAL` is a setup shortcut built on top of SQLite:

- uses the same configuration as `SQLITE`
- additionally creates and seeds a local SQLite database for immediate testing
