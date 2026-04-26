-- @name: Postgres Example - Table Does Not Exist
-- @tag: example, postgres, should-pass
-- @timeout: 30
-- Example test which should pass
select * FROM information_schema.tables
where table_name = 'SHOULD_NOT_EXIST';
