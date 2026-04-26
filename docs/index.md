# EchoSphere

<a href="https://github.com/MauriceKuenicke/EchoSphere/actions/workflows/deploy_docs.yaml">
  <img alt="Docs Deploy Status" src="https://github.com/MauriceKuenicke/EchoSphere/actions/workflows/deploy_docs.yaml/badge.svg">
</a>
<a href="https://github.com/MauriceKuenicke/EchoSphere/releases">
  <img alt="Version" src="https://img.shields.io/badge/version-v0.0.0-blue">
</a>
<a href="https://www.python.org/downloads/release/python-3100/">
  <img alt="Python" src="https://img.shields.io/badge/python-3.10%2B-blue">
</a>

<div class="es-hero">
  <p class="es-kicker">pytest for databases</p>
  <h2>Test your database like you test your code.</h2>
  <p>
    EchoSphere is a local-first CLI for SQL-native tests.
    Keep tests in git, run them in CI, and validate data logic with standard engineering workflows.
    Without DSL. Without Cloud. Without onboarding processes.
  </p>
  <p>
    <a class="md-button md-button--primary" href="getting-started/">Get Started</a>
    <a class="md-button" href="why-echosphere/vs-soda/">Compare with Soda</a>
    <a class="md-button" href="why-echosphere/ai-era/">Why This Matters in the AI Era</a>
  </p>
</div>

## Core Principles

<div class="es-grid">
  <section class="es-card">
    <h3>No DSL</h3>
    <p>Tests are plain <code>.es.sql</code> files. Your team already knows the language.</p>
  </section>
  <section class="es-card">
    <h3>No Cloud Dependency</h3>
    <p>Run locally and in CI with the <code>es</code> CLI. No external control plane required.</p>
  </section>
  <section class="es-card">
    <h3>No Onboarding Ceremony</h3>
    <p>Initialize with <code>es init</code>, add SQL tests, and run <code>es run</code>.</p>
  </section>
  <section class="es-card">
    <h3>Developer-Native Loop</h3>
    <p>Code review, versioning, CI gates, and test reports work exactly like application testing.</p>
  </section>
</div>

## What a Test Looks Like

EchoSphere has a single contract: a test passes when SQL returns zero rows.
If the query returns rows, the test fails and those rows explain the issue.

```sql
-- file: es_suite/orders_total.es.sql
-- @name: Orders Total Validation
-- @tag: critical, nightly
SELECT *
FROM (
  SELECT SUM(O_TOTALPRICE) AS total
  FROM ORDERS
  WHERE O_ORDERDATE = '1995-02-19'
)
WHERE total <> 944870465.07;
```

## Supported Connectors

<p style="margin-top: 0.5rem;">
  <img src="assets/img/postgres.svg" alt="PostgreSQL" width="48" style="vertical-align: -6px;" />
  &nbsp;&nbsp;
  <img src="assets/img/snowflake.svg" alt="Snowflake" width="48" style="vertical-align: -6px;" />
  &nbsp;&nbsp;
  <img src="assets/img/databricks.svg" alt="Databricks" width="48" style="vertical-align: -6px;" />
  &nbsp;&nbsp;
  <img src="assets/img/sqlite.svg" alt="SQLite" width="105" style="vertical-align: -10px;" scale="2" />
</p>

## Developer Workflow

1. `es init --platform <platform>`
2. Add SQL tests in `es_suite/`
3. Run `es run -e env.<platform>.dev`
4. Inspect suite with `es view tests --all` or `es view test <name>`
5. Optional exports:
   - `--junitxml` for CI test reports
   - `--export-failures` for failed rows in Excel

## Explore Next

- [Why EchoSphere](why-echosphere/index.md)
- [EchoSphere vs Soda](why-echosphere/vs-soda.md)
- [EchoSphere in the AI Era](why-echosphere/ai-era.md)
- [Getting Started](getting-started/index.md)
- [Command Reference](command-reference/index.md)
