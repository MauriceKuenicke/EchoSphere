-- @name: Databricks Example - Check Existence
-- @tag: example, databricks, should-pass
-- @timeout: 30
-- Example test which should pass
SELECT * FROM catalogs
WHERE catalog_name = 'SHOULD_NEVER_EXIST';
