# Cookbook

Common recipes based on the SQL contract requirements you can copy‑paste and adapt to your project.

## Example Assertion Templates
- No NULLs in key column
```sql
SELECT MY_COL
FROM MY_TABLE
WHERE MY_COL IS NULL;
```

- No duplicates in key column
```sql
SELECT MY_COL
FROM MY_TABLE
GROUP BY MY_COL
HAVING COUNT(*) > 1;
```

- Aggregate value equals total expectation
```sql
SELECT *
FROM (
  SELECT SUM(AMOUNT) AS total
  FROM MY_TABLE
  WHERE DATE_COL = CURRENT_DATE - INTERVAL '1 DAY'
)
WHERE total <> 123.45;
```

## Export Reports for CI Pipelines
```sh
es run -e env.snowflake.dev --junitxml reports/junit.xml
```

## Run by Tags
```sh
# include tags (OR semantics)
es run --tag critical --tag nightly

# CSV syntax is also supported
es run --tag "critical,nightly"

# exclude matching tags
es run --exclude-tag slow
```

## Run a Subsuite Only
Organize tests into subdirectories and filter using `es view` for discovery, or simply commit only the subsuite you want to run in a branch.

Listing a subsuite:
```sh
es view tests --suite smoke
```

## Investigate a Single Test
```sh
es view test integrity/no_duplicate_orders
```

## Full Local Walkthrough
See [Tutorial Setup Walkthrough](tutorial-setup.md) for an end-to-end local flow using:

- `es init --platform tutorial`
- metadata headers (`@name`, `@tag`, `@timeout`)
- tag-based execution
- JUnit + Excel exports
