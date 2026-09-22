import mysql.connector

DB_CONFIG={
    "host":"localhost",
    "user":"root",
    "password":"Perttikalevi1",
    "database":"olap_demo"
}

conn=mysql.connector.connect(**DB_CONFIG)
cur=conn.cursor()

for table in ["FactSales","DimDate","DimProduct","DimCustomer"]:
    cur.execute(f"DROP TABLE IF EXISTS {table}")

cur.execute("""
CREATE TABLE DimCustomer(
    customer_key INT PRIMARY KEY,
    customer_type VARCHAR(20),
    city VARCHAR(50)
)
""")

cur.execute("""
CREATE TABLE DimProduct(
    product_key INT PRIMARY KEY,
    category VARCHAR(30)
)
""")

cur.execute("""
CREATE TABLE DimDate(
    date_key DATE PRIMARY KEY,
    year INT,
    month INT
)
""")

cur.execute("""
CREATE TABLE FactSales(
    sales_key BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_key INT,
    product_key INT,
    date_key DATE,
    quantity INT,
    sales_amount DECIMAL(12,2)
)
""")

print("Loading dimensions...")

cur.execute("INSERT INTO DimCustomer SELECT customer_id,customer_type,city FROM customers")
cur.execute("INSERT INTO DimProduct SELECT product_id,category FROM products")

cur.execute("""
INSERT INTO DimDate
SELECT DISTINCT
    order_date,
    YEAR(order_date),
    MONTH(order_date)
FROM orders
""")

print("Loading fact table...")

cur.execute("""
INSERT INTO FactSales(customer_key,product_key,date_key,quantity,sales_amount)
SELECT
    o.customer_id,
    oi.product_id,
    o.order_date,
    oi.quantity,
    oi.quantity*oi.unit_price
FROM orders o
JOIN order_items oi
ON o.order_id=oi.order_id
""")

cur.execute("CREATE INDEX idx_fact_customer ON FactSales(customer_key)")
cur.execute("CREATE INDEX idx_fact_date ON FactSales(date_key)")
cur.execute("CREATE INDEX idx_fact_product ON FactSales(product_key)")

conn.commit()

cur.close()
conn.close()

print("Star schema created.")