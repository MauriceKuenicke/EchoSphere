-- Example test which should fail
select * FROM information_schema.tables
where table_name = 'pg_statistic';