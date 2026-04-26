# EchoSphere vs Soda

<div class="es-hero es-hero--compact">
  <p class="es-kicker">Comparison</p>
  <h2>Two different philosophies for data quality</h2>
  <p>
    <strong>Soda:</strong> "Define what good data looks like."<br>
    <strong>EchoSphere:</strong> "Test your database like you test your code."
  </p>
</div>

!!! info "EchoSphere position"
    Without DSL. Without Cloud. Without onboarding processes.

## Positioning at a Glance

| Category | Soda (typical positioning) | EchoSphere |
| --- | --- | --- |
| Core abstraction | Data quality checks and policies | SQL tests (`.es.sql`) with a zero-row contract |
| Authoring style | Configuration/check definitions plus SQL options | Plain SQL with optional metadata comments |
| Execution model | Often platform/workspace-centric workflows | Local-first CLI and CI pipelines |
| Developer workflow | Product/onboarding driven | Git + code review + test runs |
| Failure output | Rule/check failures | Returned rows from failing SQL queries |
| Adoption path | Team onboarding into platform conventions | `es init`, write SQL, run `es run` |

## Why Engineering Teams Choose EchoSphere

- Existing SQL skills transfer immediately.
- Test logic and data logic stay in one language.
- No custom DSL parser to learn or debug.
- No dependency on cloud control planes to get started.
- Easy to review in pull requests because tests are plain text SQL.

## Example: Same Intent, Different Approach

Check that `orders` has no null `order_id` values and that row count is not zero.

```sql
-- file: es_suite/orders_integrity.es.sql
-- @name: Orders Integrity
-- @tag: critical
SELECT 'order_id_null' AS issue, order_id
FROM orders
WHERE order_id IS NULL

UNION ALL

SELECT 'orders_empty' AS issue, NULL AS order_id
WHERE (SELECT COUNT(*) FROM orders) = 0;
```

If this query returns rows, the test fails and the output gives a direct debugging starting point.

## When EchoSphere Is a Better Fit

- Your team already works SQL-first and code-first.
- You want database tests to behave like unit/integration tests.
- You want minimal platform overhead and direct CI control.

## Related

- [Why EchoSphere](index.md)
- [EchoSphere in the AI Era](ai-era.md)
