-- Every order should have a valid customer
SELECT o_orderkey
FROM orders o
         LEFT JOIN customer c ON o.o_custkey = c.c_custkey
WHERE c.c_custkey IS NULL