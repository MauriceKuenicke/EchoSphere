-- No orders should have dates in the future
SELECT o_orderkey, o_orderdate
FROM orders
WHERE o_orderdate > CURRENT_DATE;
