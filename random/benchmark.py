import mysql.connector
import time

DB_CONFIG={
    "host":"localhost",
    "user":"root",
    "password":"Perttikalevi1",
    "database":"olap_demo"
}

queries={

"VIP Monthly Revenue":(

"""
SELECT
DATE_FORMAT(o.order_date,'%Y-%m'),
SUM(oi.quantity*oi.unit_price)
FROM orders o
JOIN customers c
ON o.customer_id=c.customer_id
JOIN order_items oi
ON o.order_id=oi.order_id
WHERE c.customer_type='VIP'
AND o.order_date>='2026-01-01'
AND o.order_date<'2027-01-01'
GROUP BY DATE_FORMAT(o.order_date,'%Y-%m')
""",

"""
SELECT
DATE_FORMAT(f.date_key,'%Y-%m'),
SUM(f.sales_amount)
FROM FactSales f
JOIN DimCustomer c
ON f.customer_key=c.customer_key
WHERE c.customer_type='VIP'
AND f.date_key>='2026-01-01'
AND f.date_key<'2027-01-01'
GROUP BY DATE_FORMAT(f.date_key,'%Y-%m')
"""
),

"Revenue by Category":(

"""
SELECT
p.category,
SUM(oi.quantity*oi.unit_price)
FROM order_items oi
JOIN products p
ON oi.product_id=p.product_id
GROUP BY p.category
""",

"""
SELECT
p.category,
SUM(f.sales_amount)
FROM FactSales f
JOIN DimProduct p
ON f.product_key=p.product_key
GROUP BY p.category
"""
),

"Revenue by City":(

"""
SELECT
c.city,
SUM(oi.quantity*oi.unit_price)
FROM orders o
JOIN customers c
ON o.customer_id=c.customer_id
JOIN order_items oi
ON o.order_id=oi.order_id
GROUP BY c.city
""",

"""
SELECT
c.city,
SUM(f.sales_amount)
FROM FactSales f
JOIN DimCustomer c
ON f.customer_key=c.customer_key
GROUP BY c.city
"""
)

}

conn=mysql.connector.connect(**DB_CONFIG)
cur=conn.cursor()

print(f"{'Query':25} {'3NF(s)':>10} {'Star(s)':>10}")
print("-"*50)

for name,(q3,qstar) in queries.items():

    t=time.perf_counter()
    cur.execute(q3)
    cur.fetchall()
    t3=time.perf_counter()-t

    t=time.perf_counter()
    cur.execute(qstar)
    cur.fetchall()
    ts=time.perf_counter()-t

    print(f"{name:25} {t3:10.3f} {ts:10.3f}")

print("\nEXPLAIN ANALYZE (3NF)\n")

cur.execute("EXPLAIN ANALYZE "+queries["Revenue by City"][0])

for row in cur.fetchall():
    print(row[0])

print("\nEXPLAIN ANALYZE (Star Schema)\n")

cur.execute("EXPLAIN ANALYZE "+queries["Revenue by City"][1])

for row in cur.fetchall():
    print(row[0])

cur.close()
conn.close()