-- Verify data consistency across multiple tables
SELECT
    l.l_orderkey,
    o.o_orderdate,
    l.l_shipdate,
    l.l_commitdate,
    l.l_receiptdate
FROM
    lineitem l
        JOIN
    orders o ON l.l_orderkey = o.o_orderkey
WHERE
   -- Test temporal consistency
    l.l_shipdate < o.o_orderdate -- Ship date should not be before order date
   OR l.l_receiptdate < l.l_shipdate -- Receipt date should not be before ship date
   OR (l.l_commitdate < o.o_orderdate) -- Commit date should not be before order date