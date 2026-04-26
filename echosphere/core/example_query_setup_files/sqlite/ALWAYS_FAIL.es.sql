-- @name: SQLite Example - Always Fail
-- @tag: example, sqlite, should-fail
-- @timeout: 30
-- Intentionally always returns a row to demonstrate a failing test.
-- Replace this with a real assertion, e.g. rows that violate a data rule.
SELECT 1 AS always_fails;
