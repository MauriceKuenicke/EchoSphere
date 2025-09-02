-- Order total price should match sum of line items
SELECT
    o.o_orderkey,
    o.o_totalprice AS order_total,
    SUM(l.l_quantity * l.l_extendedprice * (1 - l.l_discount) * (1 + l.l_tax)) AS calculated_total
FROM
    orders o
        JOIN
    lineitem l ON o.o_orderkey = l.l_orderkey
GROUP BY
    o.o_orderkey, o.o_totalprice
HAVING
    ABS(o.o_totalprice - SUM(l.l_quantity * l.l_extendedprice * (1 - l.l_discount) * (1 + l.l_tax))) > 0.01
