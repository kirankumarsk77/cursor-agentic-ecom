import sqlite3
import json
import os

# Database name
DB_NAME = "ecommerce.db"

# Create database connection
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Create tables
print("Creating database tables...")

# Customers table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        city TEXT
    )
""")

# Products table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT,
        price REAL
    )
""")

# Orders table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        product_id INTEGER,
        qty INTEGER,
        date TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
""")

# Payments table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        order_id INTEGER PRIMARY KEY,
        amount REAL,
        payment_method TEXT,
        status TEXT,
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
    )
""")

# Shipments table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS shipments (
        order_id INTEGER PRIMARY KEY,
        shipment_status TEXT,
        shipment_date TEXT,
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
    )
""")

print("Tables created successfully.")

# Load and insert data from JSON files
data_dir = "data"

# Load customers
print("Loading customers...")
with open(os.path.join(data_dir, "customers.json"), "r", encoding="utf-8") as f:
    customers = json.load(f)
    for customer in customers:
        cursor.execute(
            "INSERT OR REPLACE INTO customers (id, name, email, city) VALUES (?, ?, ?, ?)",
            (customer["id"], customer["name"], customer["email"], customer["city"])
        )
print(f"Inserted {len(customers)} customers.")

# Load products
print("Loading products...")
with open(os.path.join(data_dir, "products.json"), "r", encoding="utf-8") as f:
    products = json.load(f)
    for product in products:
        cursor.execute(
            "INSERT OR REPLACE INTO products (id, name, category, price) VALUES (?, ?, ?, ?)",
            (product["id"], product["name"], product["category"], product["price"])
        )
print(f"Inserted {len(products)} products.")

# Load orders
print("Loading orders...")
with open(os.path.join(data_dir, "orders.json"), "r", encoding="utf-8") as f:
    orders = json.load(f)
    for order in orders:
        cursor.execute(
            "INSERT OR REPLACE INTO orders (order_id, customer_id, product_id, qty, date) VALUES (?, ?, ?, ?, ?)",
            (order["order_id"], order["customer_id"], order["product_id"], order["qty"], order["date"])
        )
print(f"Inserted {len(orders)} orders.")

# Load payments
print("Loading payments...")
with open(os.path.join(data_dir, "payments.json"), "r", encoding="utf-8") as f:
    payments = json.load(f)
    for payment in payments:
        cursor.execute(
            "INSERT OR REPLACE INTO payments (order_id, amount, payment_method, status) VALUES (?, ?, ?, ?)",
            (payment["order_id"], payment["amount"], payment["payment_method"], payment["status"])
        )
print(f"Inserted {len(payments)} payments.")

# Load shipments
print("Loading shipments...")
with open(os.path.join(data_dir, "shipments.json"), "r", encoding="utf-8") as f:
    shipments = json.load(f)
    for shipment in shipments:
        cursor.execute(
            "INSERT OR REPLACE INTO shipments (order_id, shipment_status, shipment_date) VALUES (?, ?, ?)",
            (shipment["order_id"], shipment["shipment_status"], shipment["shipment_date"])
        )
print(f"Inserted {len(shipments)} shipments.")

# Commit all changes
conn.commit()

# Close connection
conn.close()

print("Data ingestion completed")

