import mysql.connector
import random
from datetime import date, timedelta

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Perttikalevi1",
    "database": "oltp_demo"
}

N_CUSTOMERS = 100000
N_PRODUCTS = 5000
N_ORDERS = 500000
AVG_ITEMS = 3
BATCH = 10000

random.seed(42)

conn = mysql.connector.connect(**DB_CONFIG)
cur = conn.cursor()

cur.execute("CREATE DATABASE IF NOT EXISTS olap_demo")
cur.execute("USE olap_demo")

cur.execute("SET FOREIGN_KEY_CHECKS=0")

for table in ["payments","order_items","orders","products","customers"]:
    cur.execute(f"DROP TABLE IF EXISTS {table}")

cur.execute("SET FOREIGN_KEY_CHECKS=1")

cur.execute("""
CREATE TABLE customers(
    customer_id INT PRIMARY KEY,
    customer_type VARCHAR(20),
    city VARCHAR(50)
)
""")

cur.execute("""
CREATE TABLE products(
    product_id INT PRIMARY KEY,
    category VARCHAR(30),
    price DECIMAL(10,2)
)
""")

cur.execute("""
CREATE TABLE orders(
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
)
""")

cur.execute("""
CREATE TABLE order_items(
    order_item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    FOREIGN KEY(order_id) REFERENCES orders(order_id),
    FOREIGN KEY(product_id) REFERENCES products(product_id)
)
""")

cur.execute("""
CREATE TABLE payments(
    payment_id INT PRIMARY KEY,
    order_id INT,
    status VARCHAR(20),
    method VARCHAR(20),
    amount DECIMAL(12,2),
    FOREIGN KEY(order_id) REFERENCES orders(order_id)
)
""")

cities = ["London","Paris","Berlin","Madrid","Rome","Helsinki","Oslo","Stockholm"]
categories = ["Electronics","Books","Clothing","Sports","Home"]

print("Generating customers...")

rows = []
for i in range(1, N_CUSTOMERS+1):
    rows.append((
        i,
        "VIP" if random.random()<0.15 else "Regular",
        random.choice(cities)
    ))
    if len(rows)==BATCH:
        cur.executemany("INSERT INTO customers VALUES(%s,%s,%s)", rows)
        conn.commit()
        rows=[]

if rows:
    cur.executemany("INSERT INTO customers VALUES(%s,%s,%s)", rows)
    conn.commit()

print("Generating products...")

rows=[]
for i in range(1,N_PRODUCTS+1):
    rows.append((
        i,
        random.choice(categories),
        round(random.uniform(5,500),2)
    ))
    if len(rows)==BATCH:
        cur.executemany("INSERT INTO products VALUES(%s,%s,%s)", rows)
        conn.commit()
        rows=[]

if rows:
    cur.executemany("INSERT INTO products VALUES(%s,%s,%s)", rows)
    conn.commit()

print("Generating orders and order items...")

start=date(2025,1,1)

order_rows=[]
item_rows=[]
payment_rows=[]

item_id=1

for order_id in range(1,N_ORDERS+1):

    customer=random.randint(1,N_CUSTOMERS)
    d=start+timedelta(days=random.randint(0,730))

    order_rows.append((order_id,customer,d))

    total=0

    items=max(1,int(random.expovariate(1/AVG_ITEMS)))

    for _ in range(items):

        product=random.randint(1,N_PRODUCTS)
        qty=random.randint(1,5)
        price=round(random.uniform(5,500),2)

        total += qty*price

        item_rows.append((
            item_id,
            order_id,
            product,
            qty,
            price
        ))
        item_id+=1

    payment_rows.append((
        order_id,
        order_id,
        "Paid" if random.random()<0.97 else "Failed",
        random.choice(["Card","PayPal"]),
        round(total,2)
    ))

    if len(order_rows)==BATCH:

        cur.executemany("INSERT INTO orders VALUES(%s,%s,%s)",order_rows)
        cur.executemany("INSERT INTO order_items VALUES(%s,%s,%s,%s,%s)",item_rows)
        cur.executemany("INSERT INTO payments VALUES(%s,%s,%s,%s,%s)",payment_rows)

        conn.commit()

        order_rows=[]
        item_rows=[]
        payment_rows=[]

if order_rows:
    cur.executemany("INSERT INTO orders VALUES(%s,%s,%s)",order_rows)
    cur.executemany("INSERT INTO order_items VALUES(%s,%s,%s,%s,%s)",item_rows)
    cur.executemany("INSERT INTO payments VALUES(%s,%s,%s,%s,%s)",payment_rows)
    conn.commit()

print("Creating indexes...")

cur.execute("CREATE INDEX idx_orders_date ON orders(order_date)")
cur.execute("CREATE INDEX idx_orders_customer ON orders(customer_id)")
cur.execute("CREATE INDEX idx_orderitems_order ON order_items(order_id)")
cur.execute("CREATE INDEX idx_customers_type ON customers(customer_type)")

conn.commit()

cur.close()
conn.close()

print("3NF database created.")