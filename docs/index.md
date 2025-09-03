# EchoSphere

EchoSphere is a fast, lightweight SQL testing framework designed to validate your data workflows with simple, readable SQL files. It focuses on developer experience and velocity: write tests as SQL, run them in parallel, and integrate the results into your CI/CD.

> EchoSphere derives from the mythological nymph Echo — a symbol of reflection and resonance. Your tests “echo” the health of your data systems.

![EchoSphere Logo](assets/logo-color-cropped.svg){ width=300 }

## Why EchoSphere?
- Simple: Tests are plain SQL files with a `.es.sql` suffix
- Fast: Concurrent execution for quick feedback
- CI-ready: JUnit output, clear exit codes, and machine-readable results
- Safe defaults: Convention over configuration to get started quickly

## Quick Links
- [Getting Started](getting-started/index.md): installation, first setup, and a 5‑minute quickstart
- [User Guide](user-guide/index.md): workflows, environment management, and writing effective tests
- [Command Reference](command-reference/index.md): full CLI documentation for `es`
- [Advanced Topics](advanced/ci-cd.md): CI/CD, performance, and extensions
- [Troubleshooting](troubleshooting/index.md): common issues and debugging tips

## What a Test Looks Like
EchoSphere considers a test successful if it returns zero rows. If the query returns one or more rows, the test fails and the rows explain what was wrong.

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

## Latest Version and Changelog
- Versioning aligns with project releases on GitHub.
- See the repository releases tab for changelog highlights.

## Next steps
- Start with the 5‑minute quickstart
- Or jump to Installation if you prefer pip, Docker, or from source
