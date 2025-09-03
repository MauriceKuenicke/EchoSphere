# SQL Testing Syntax (EchoSphere)

EchoSphere follows a simple, explicit convention:

- A test is any file ending with `.es.sql`.
- A test PASSES when the query returns zero rows.
- A test FAILS when the query returns one or more rows — those rows explain the failure.

This design keeps tests readable and leverages the full expressiveness of SQL.

## Patterns

### Assert Equality
Return a row only when the value differs.
```sql
SELECT *
FROM (
  SELECT SUM(AMOUNT) AS total
  FROM PAYMENTS
  WHERE DATE = CURRENT_DATE - 1
)
WHERE total <> 123.45;
```

### Assert Non‑Null
```sql
SELECT CUSTOMER_ID
FROM CUSTOMERS
WHERE CUSTOMER_ID IS NULL;
```

### Assert Uniqueness
```sql
SELECT ORDER_ID
FROM ORDERS
GROUP BY ORDER_ID
HAVING COUNT(*) > 1;
```

### Conditional/Scoped Checks
Use WHERE clauses to scope checks to recent partitions or specific segments.
```sql
SELECT *
FROM (
  SELECT COUNT(*) AS cnt
  FROM EVENTS
  WHERE EVENT_DATE >= CURRENT_DATE - 7
)
WHERE cnt = 0;  -- Fail if no events in the last 7 days
```

## Recommendations
- Keep each test focused (one assertion per file when possible).
- Avoid cross‑environment fully qualified names; rely on environment config for DB/SCHEMA.
- Prefer deterministic logic; control time windows to reduce flakes.
- Add comments at the top explaining the business rule and what a failure row means.
