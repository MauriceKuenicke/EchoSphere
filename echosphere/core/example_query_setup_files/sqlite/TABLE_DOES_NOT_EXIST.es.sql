-- @name: SQLite Example - Table Does Not Exist
-- @tag: example, sqlite, should-pass
-- @timeout: 30
-- Example test which should pass
SELECT 1 AS should_pass WHERE 1 = 0;
