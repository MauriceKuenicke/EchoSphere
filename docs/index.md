# EchoSphere

<a href="https://github.com/MauriceKuenicke/EchoSphere/actions/workflows/deploy_docs.yaml">
    <img alt="Docs Deploy Status" src="https://github.com/MauriceKuenicke/EchoSphere/actions/workflows/deploy_docs.yaml/badge.svg">
  </a>
  <a href="https://github.com/MauriceKuenicke/EchoSphere/releases">
    <img alt="Version" src="https://img.shields.io/badge/version-v0.0.0-blue"></a>
  <a href="https://www.python.org/downloads/release/python-3100/">
    <img alt="Python" src="https://img.shields.io/badge/python-3.10%2B-blue"></a>

EchoSphere is a fast, lightweight SQL testing framework designed to validate your 
data quality with simple, readable SQL files.
It focuses on developer experience and velocity.
Write tests as SQL, run them in parallel, and integrate the results into your CI/CD.

> EchoSphere derives from the mythological nymph Echo — a symbol of reflection and resonance. Your tests “echo” the health of your data systems.

## Supported Connectors 🔬
<p style="margin-top: 0.5rem;">
    <img src="assets/img/postgres.svg" alt="PostgreSQL" width="48" style="vertical-align: -6px;" />
  &nbsp;&nbsp;
    <img src="assets/img/snowflake.svg" alt="Snowflake" width="48" style="vertical-align: -6px;" />
  &nbsp;&nbsp;
    <img src="assets/img/databricks.svg" alt="Databricks" width="48" style="vertical-align: -6px;" />
  &nbsp;&nbsp;
    <img src="assets/img/sqlite.svg" alt="SQLite" width="105" style="vertical-align: -10px;" scale="2" />
</p>

## Why EchoSphere? ⚡
- Simple: Tests are plain SQL (`.es.sql`) files
- Fast: Concurrent execution for quick feedback
- CI-ready: JUnit output and machine-readable results
- Visibility: Export data issues into Excel files

## Quick Links 🔗
- [Getting Started](getting-started/index.md): installation, first setup, and a 5‑minute quickstart
- [User Guide](user-guide/index.md): workflows, environment management, and writing effective tests
- [Command Reference](command-reference/index.md): full CLI documentation for `es`
- [Tutorial Walkthrough](examples/tutorial-setup.md): local `tutorial` setup with tags and exports
- [Advanced Topics](advanced/ci-cd.md): CI/CD, performance, and extensions
- [Troubleshooting](troubleshooting/index.md): common issues and debugging tips

## What a Test Looks Like 🧪
EchoSphere considers a test successful if it returns zero rows. That is the only requirement.
Everything else is up to you.
If the query returns one or more rows, the test fails and the rows explain what went wrong.

```sql
-- file: tests/orders_total.es.sql
SELECT *
FROM (
  SELECT SUM(O_TOTALPRICE) AS total
  FROM ORDERS
  WHERE O_ORDERDATE = '1995-02-19'
)
WHERE total <> 944870465.07;
```
