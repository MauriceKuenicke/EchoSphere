# Cookbook

Common recipes you can copy‑paste and adapt to your project.

## Export Reports in CI
```sh
es run -e dev --junitxml reports/junit.xml --export-failures reports/failures.xlsx
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

## Create a New Project
```sh
pip install git+https://github.com/MauriceKuenicke/EchoSphere
es setup --platform SNOWFLAKE
```

## Example Assertion Templates
- No NULLs in key column
```sql
SELECT KEY
FROM MY_TABLE
WHERE KEY IS NULL;
```

- No duplicates in key
```sql
SELECT KEY
FROM MY_TABLE
GROUP BY KEY
HAVING COUNT(*) > 1;
```

- Aggregate value equals expectation
```sql
SELECT *
FROM (
  SELECT SUM(AMOUNT) AS total
  FROM MY_TABLE
  WHERE DATE_COL = CURRENT_DATE - INTERVAL '1 DAY'
)
WHERE total <> 123.45;
```
