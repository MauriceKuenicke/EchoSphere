-- @name: Referential Integrity Orders to Customers
-- @tag: example, snowflake, referential-integrity
-- @timeout: 60
-- Every order should have a valid customer
SELECT o_orderkey
FROM orders o
         LEFT JOIN customer c ON o.o_custkey = c.c_custkey
WHERE c.c_custkey IS NULL;
