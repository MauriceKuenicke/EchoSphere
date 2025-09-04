-- Example test which should pass
select * FROM information_schema.tables
where table_name = 'SHOULD_NOT_EXIST'
