# Tutorial Setup Walkthrough

This walkthrough uses the built-in local starter (`tutorial`) to demonstrate:

- metadata-driven test names/tags/timeouts
- tag-based execution
- JUnit + Excel exports

## 1. Initialize the tutorial workspace

```sh
es init --platform tutorial
```

This creates:

- `es.ini` (default env: `env.sqlite.dev`)
- `es_suite/` with example tests
- `./.echosphere/tutorial.db` seeded with sample `customers` and `orders` data

## 2. Run the bundled tests

```sh
es run
```

The bundled tutorial tests include metadata in-file (`@name`, `@tag`, `@timeout`) and are displayed using their `@name` values:

- **SQLite Example - Always Fail** — tagged `should-fail`: always returns a row (intentional failure demo)
- **SQLite Example - Always Pass** — tagged `should-pass`: always returns zero rows (passing test demo)

## 3. Filter execution by tags

```sh
# run only the passing tutorial example
es run --tag should-pass

# run only the intentionally failing tutorial example
es run --tag should-fail

# run all examples except intentional failures
es run --tag example --exclude-tag should-fail
```

Notes:

- `--tag` matches if any provided tag matches.
- `--exclude-tag` removes tests with matching tags.
- Both flags support repetition and comma-separated values.

## 4. Export JUnit + failing rows

```sh
es run --tag should-fail --junitxml reports/tutorial-junit.xml --export-failures reports/tutorial-failures.xlsx
```

This command is expected to finish with a non-zero exit code (because the selected test fails), while still writing:

- `reports/tutorial-junit.xml`
- `reports/tutorial-failures.xlsx`

## 5. Add one custom metadata test

Create `es_suite/tutorial_no_orphan_orders.es.sql`:

```sql
-- @name: Tutorial - No Orphan Orders
-- @tag: tutorial, integrity
-- @timeout: 10
SELECT o.order_id
FROM orders o
LEFT JOIN customers c ON c.customer_id = o.customer_id
WHERE c.customer_id IS NULL;
```

Run only your tutorial-tagged checks:

```sh
es run --tag tutorial
```
