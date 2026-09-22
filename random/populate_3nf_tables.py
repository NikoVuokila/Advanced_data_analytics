import mysql.connector
import random
from datetime import date, datetime, timedelta


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Perttikalevi1",
    "database": "sales_3nf_example"
}


# ============================================================
# SETTINGS
# ============================================================

NUM_CUSTOMERS = 100_000
NUM_PRODUCTS = 5_000
NUM_STORES = 50
NUM_ORDERS = 500_000

BATCH_SIZE = 10_000

START_DATE = date(2025, 1, 1)
END_DATE = date(2026, 12, 31)


# ============================================================
# REFERENCE DATA
# ============================================================

locations = [
    ("London", "England", "United Kingdom"),
    ("Paris", "Île-de-France", "France"),
    ("Berlin", "Berlin", "Germany"),
    ("Madrid", "Madrid", "Spain"),
    ("Rome", "Lazio", "Italy"),
    ("Helsinki", "Uusimaa", "Finland"),
    ("Oslo", "Oslo", "Norway"),
    ("Stockholm", "Stockholm", "Sweden")
]

customer_types = [
    "Regular",
    "Premium",
    "Business"
]

categories = [
    "Electronics",
    "Books",
    "Clothing",
    "Sports",
    "Home"
]

brands = [
    "BrandA",
    "BrandB",
    "BrandC",
    "BrandD",
    "BrandE",
    "BrandF"
]

payment_methods = [
    "Card",
    "PayPal"
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def random_date(start_date, end_date):
    """Return a random date between two dates."""
    days = (end_date - start_date).days

    return start_date + timedelta(
        days=random.randint(0, days)
    )


def random_datetime():
    """Return a random datetime between 2025-01-01 and 2026-12-31."""

    start = datetime(2025, 1, 1)
    end = datetime(2026, 8, 31)

    seconds = int(
        (end - start).total_seconds()
    )

    return start + timedelta(
        seconds=random.randint(0, seconds)
    )


# ============================================================
# CONNECT TO MYSQL
# ============================================================

print("Connecting to MySQL...")

conn = mysql.connector.connect(**DB_CONFIG)

cursor = conn.cursor()

print("Connected successfully.")


try:

    # ========================================================
    # CUSTOMERS
    # ========================================================

    print()
    print("========================================")
    print("Creating customers...")
    print("========================================")

    customer_batch = []

    for customer_id in range(1, NUM_CUSTOMERS + 1):

        city, state, country = random.choice(locations)

        first_name = f"FirstName{customer_id}"
        last_name = f"LastName{customer_id}"

        customer_type = random.choice(
            customer_types
        )

        updated_at = random_datetime()

        customer_batch.append((
            customer_id,
            first_name,
            last_name,
            customer_type,
            city,
            state,
            country,
            updated_at
        ))

        # Insert full batch
        if len(customer_batch) >= BATCH_SIZE:

            cursor.executemany("""
                INSERT INTO customers
                (
                    customer_id,
                    first_name,
                    last_name,
                    customer_type,
                    city,
                    state_name,
                    country_name,
                    updated_at
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, customer_batch)

            conn.commit()

            customer_batch.clear()

            print(
                f"Customers inserted: "
                f"{customer_id:,}"
            )

    # Insert final partial batch
    if customer_batch:

        cursor.executemany("""
            INSERT INTO customers
            (
                customer_id,
                first_name,
                last_name,
                customer_type,
                city,
                state_name,
                country_name,
                updated_at
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, customer_batch)

        conn.commit()

        customer_batch.clear()


    # ========================================================
    # PRODUCTS
    # ========================================================

    print()
    print("========================================")
    print("Creating products...")
    print("========================================")

    product_batch = []

    for product_id in range(1, NUM_PRODUCTS + 1):

        category = random.choice(categories)

        brand = random.choice(brands)

        product_name = f"Product {product_id}"

        price = round(
            random.uniform(5, 500),
            2
        )

        updated_at = random_datetime()

        product_batch.append((
            product_id,
            product_name,
            category,
            brand,
            price,
            updated_at
        ))

        # Insert full batch
        if len(product_batch) >= BATCH_SIZE:

            cursor.executemany("""
                INSERT INTO products
                (
                    product_id,
                    product_name,
                    category,
                    brand_name,
                    price,
                    updated_at
                )
                VALUES (%s,%s,%s,%s,%s,%s)
            """, product_batch)

            conn.commit()

            product_batch.clear()

            print(
                f"Products inserted: "
                f"{product_id:,}"
            )

    # IMPORTANT:
    # Insert final partial batch.
    if product_batch:

        cursor.executemany("""
            INSERT INTO products
            (
                product_id,
                product_name,
                category,
                brand_name,
                price,
                updated_at
            )
            VALUES (%s,%s,%s,%s,%s,%s)
        """, product_batch)

        conn.commit()

        product_batch.clear()

        print(
            f"Products inserted: "
            f"{NUM_PRODUCTS:,}"
        )


    # ========================================================
    # STORES
    # ========================================================

    print()
    print("========================================")
    print("Creating stores...")
    print("========================================")

    store_batch = []

    for store_id in range(1, NUM_STORES + 1):

        store_name = f"Store {store_id}"

        region_name = (
            f"Region {((store_id - 1) % 10) + 1}"
        )

        updated_at = random_datetime()

        store_batch.append((
            store_id,
            store_name,
            region_name,
            updated_at
        ))

    cursor.executemany("""
        INSERT INTO stores
        (
            store_id,
            store_name,
            region_name,
            updated_at
        )
        VALUES (%s,%s,%s,%s)
    """, store_batch)

    conn.commit()

    print(
        f"Stores inserted: "
        f"{NUM_STORES:,}"
    )


    # ========================================================
    # VERIFY PARENT TABLES
    # ========================================================

    print()
    print("========================================")
    print("Checking parent tables...")
    print("========================================")

    cursor.execute("""
        SELECT COUNT(*)
        FROM customers
    """)

    customer_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM products
    """)

    product_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM stores
    """)

    store_count = cursor.fetchone()[0]

    print(
        f"Customers in database: {customer_count:,}"
    )

    print(
        f"Products in database: {product_count:,}"
    )

    print(
        f"Stores in database: {store_count:,}"
    )

    if customer_count != NUM_CUSTOMERS:
        raise Exception(
            "Customer count is incorrect."
        )

    if product_count != NUM_PRODUCTS:
        raise Exception(
            "Product count is incorrect."
        )

    if store_count != NUM_STORES:
        raise Exception(
            "Store count is incorrect."
        )


    # ========================================================
    # ORDERS + ORDER ITEMS + PAYMENTS
    # ========================================================

    print()
    print("========================================")
    print("Creating orders, order items and payments...")
    print("========================================")

    order_batch = []

    item_batch = []

    payment_batch = []

    order_item_id = 1

    payment_id = 1


    for order_id in range(1, NUM_ORDERS + 1):

        # ----------------------------------------------------
        # ORDER
        # ----------------------------------------------------

        customer_id = random.randint(
            1,
            NUM_CUSTOMERS
        )

        store_id = random.randint(
            1,
            NUM_STORES
        )

        order_date = random_date(
            START_DATE,
            END_DATE
        )

        order_updated_at = random_datetime()

        order_batch.append((
            order_id,
            customer_id,
            store_id,
            order_date,
            order_updated_at
        ))


        # ----------------------------------------------------
        # ORDER ITEMS
        # ----------------------------------------------------

        num_items = random.randint(1, 5)

        order_total = 0


        for _ in range(num_items):

            product_id = random.randint(
                1,
                NUM_PRODUCTS
            )

            quantity = random.randint(
                1,
                5
            )

            unit_price = round(
                random.uniform(5, 500),
                2
            )

            item_updated_at = random_datetime()

            item_batch.append((
                order_item_id,
                order_id,
                product_id,
                quantity,
                unit_price,
                item_updated_at
            ))

            order_total += (
                quantity * unit_price
            )

            order_item_id += 1


        # ----------------------------------------------------
        # PAYMENT
        # ----------------------------------------------------

        if random.random() < 0.97:
            payment_status = "Paid"
        else:
            payment_status = "Failed"

        payment_method = random.choice(
            payment_methods
        )

        payment_batch.append((
            payment_id,
            order_id,
            payment_status,
            payment_method,
            round(order_total, 2),
            random_datetime()
        ))

        payment_id += 1


        # ----------------------------------------------------
        # INSERT BATCH
        # ----------------------------------------------------

        if len(order_batch) >= BATCH_SIZE:

            # Insert orders first because order_items
            # has a foreign key referencing orders.

            cursor.executemany("""
                INSERT INTO orders
                (
                    order_id,
                    customer_id,
                    store_id,
                    order_date,
                    updated_at
                )
                VALUES (%s,%s,%s,%s,%s)
            """, order_batch)


            # Products already exist, so order_items
            # can now safely reference them.

            cursor.executemany("""
                INSERT INTO order_items
                (
                    order_item_id,
                    order_id,
                    product_id,
                    quantity,
                    unit_price,
                    updated_at
                )
                VALUES (%s,%s,%s,%s,%s,%s)
            """, item_batch)


            cursor.executemany("""
                INSERT INTO payments
                (
                    payment_id,
                    order_id,
                    status,
                    method,
                    amount,
                    updated_at
                )
                VALUES (%s,%s,%s,%s,%s,%s)
            """, payment_batch)


            conn.commit()


            order_batch.clear()
            item_batch.clear()
            payment_batch.clear()


            print(
                f"Orders inserted: "
                f"{order_id:,}"
            )


    # ========================================================
    # INSERT FINAL PARTIAL BATCH
    # ========================================================

    if order_batch:

        cursor.executemany("""
            INSERT INTO orders
            (
                order_id,
                customer_id,
                store_id,
                order_date,
                updated_at
            )
            VALUES (%s,%s,%s,%s,%s)
        """, order_batch)


        cursor.executemany("""
            INSERT INTO order_items
            (
                order_item_id,
                order_id,
                product_id,
                quantity,
                unit_price,
                updated_at
            )
            VALUES (%s,%s,%s,%s,%s,%s)
        """, item_batch)


        cursor.executemany("""
            INSERT INTO payments
            (
                payment_id,
                order_id,
                status,
                method,
                amount,
                updated_at
            )
            VALUES (%s,%s,%s,%s,%s,%s)
        """, payment_batch)


        conn.commit()


    # ========================================================
    # FINAL COUNTS
    # ========================================================

    print()
    print("========================================")
    print("Final row counts")
    print("========================================")


    cursor.execute("""
        SELECT COUNT(*)
        FROM customers
    """)

    print(
        f"Customers: "
        f"{cursor.fetchone()[0]:,}"
    )


    cursor.execute("""
        SELECT COUNT(*)
        FROM products
    """)

    print(
        f"Products: "
        f"{cursor.fetchone()[0]:,}"
    )


    cursor.execute("""
        SELECT COUNT(*)
        FROM stores
    """)

    print(
        f"Stores: "
        f"{cursor.fetchone()[0]:,}"
    )


    cursor.execute("""
        SELECT COUNT(*)
        FROM orders
    """)

    print(
        f"Orders: "
        f"{cursor.fetchone()[0]:,}"
    )


    cursor.execute("""
        SELECT COUNT(*)
        FROM order_items
    """)

    print(
        f"Order items: "
        f"{cursor.fetchone()[0]:,}"
    )


    cursor.execute("""
        SELECT COUNT(*)
        FROM payments
    """)

    print(
        f"Payments: "
        f"{cursor.fetchone()[0]:,}"
    )


    print()
    print("========================================")
    print("Data generation completed successfully!")
    print("========================================")


except Exception as e:

    # --------------------------------------------------------
    # ROLLBACK IF ANYTHING FAILS
    # --------------------------------------------------------

    conn.rollback()

    print()
    print("ERROR!")
    print(e)

    print()
    print("Transaction rolled back.")


finally:

    # ========================================================
    # CLOSE CONNECTION
    # ========================================================

    cursor.close()

    conn.close()

    print()
    print("Database connection closed.")