-- @name: Postgres Example - Check Existence
-- @tag: example, postgres, should-fail
-- @timeout: 30
-- Example test which should fail
select * FROM information_schema.tables
where table_name = 'pg_statistic';
