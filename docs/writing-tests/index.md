# Writing Tests

EchoSphere tests are plain SQL files with the `.es.sql` suffix. A test passes when the query returns zero rows. If the query returns one or more rows, the test fails and the returned rows explain what was wrong.

## File and Directory Structure
- Use `.es.sql` as the file extension so EchoSphere can discover tests automatically
- Organize tests in subdirectories ("subsuites") for logical grouping (e.g., `smoke/`, `daily/`, `integrity/`)
- Reference tests by subsuite using `es view` (e.g., `es view test smoke/orders_total`)

Example layout:
```
.es_suite/
  smoke/
    orders_total.es.sql
  integrity/
    no_duplicate_keys.es.sql
```

## Test Authoring Principles
- Assert via row presence: return a row only when a rule is violated
- Keep tests focused and isolated — one assertion per file is easier to triage
- Prefer deterministic logic; avoid nondeterministic functions unless controlled
- Keep queries performant; filter early and leverage indexes/partitions where applicable

## Naming Conventions
- Use descriptive, intent‑revealing names: `no_null_customer_ids.es.sql`
- Consider a prefix for categories or ownership if helpful

## Example Tests
Validate a specific aggregation is as expected:
```sql
-- orders_total.es.sql
SELECT *
FROM (
  SELECT SUM(O_TOTALPRICE) AS total
  FROM ORDERS
  WHERE O_ORDERDATE = '1995-02-19'
)
WHERE total <> 944870465.07;
```

Check for unexpected NULLs:
```sql
-- no_null_customer_ids.es.sql
SELECT CUSTOMER_ID
FROM CUSTOMERS
WHERE CUSTOMER_ID IS NULL;
```

Detect duplicate business keys:
```sql
-- no_duplicate_orders.es.sql
SELECT ORDER_ID
FROM ORDERS
GROUP BY ORDER_ID
HAVING COUNT(*) > 1;
```

## Best Practices
- Avoid using fully qualified table paths across environments. Rely on environment configuration (database/schema) via `es.ini`.
- Keep tests small and composable — split overly complex checks into multiple tests.
- Use comments to explain the business rule and failure rationale at the top of each test.
- For long‑running queries, consider limiting the scope (e.g., date partitions) or creating summarized tables upstream.

## Running and Inspecting
Run all tests:
```sh
es run -e dev
```

List discovered tests:
```sh
es view tests --all
```

Print the SQL of a specific test:
```sh
es view test integrity/no_duplicate_orders
```
