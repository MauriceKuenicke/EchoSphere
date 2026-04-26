-- @name: SQLite Example - Always Pass
-- @tag: example, sqlite, should-pass
-- @timeout: 30
-- Intentionally always returns zero rows to demonstrate a passing test.
-- Replace this with a real assertion, e.g. checking for unexpected NULLs.
SELECT 1 AS always_passes WHERE 1 = 0;
