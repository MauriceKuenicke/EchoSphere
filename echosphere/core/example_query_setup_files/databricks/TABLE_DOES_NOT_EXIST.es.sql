-- @name: Databricks Example - Table Does Not Exist
-- @tag: example, databricks, should-fail
-- @timeout: 30
-- Example test which should fail
select * FROM catalogs
WHERE catalog_name = 'system';
