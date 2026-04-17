import sqlite3
import os

if os.path.exists("store.db"):
    os.remove("store.db")

conn = sqlite3.connect("store.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT,
        city TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        price REAL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        product_id INTEGER,
        quantity INTEGER
    )
""")

# Add customers
cursor.execute("INSERT INTO customers (name, email, city) VALUES ('Vishnu', 'vishnu@email.com', 'Mumbai')")
cursor.execute("INSERT INTO customers (name, email, city) VALUES ('Priya', 'priya@email.com', 'Delhi')")
cursor.execute("INSERT INTO customers (name, email, city) VALUES ('Rahul', 'rahul@email.com', 'Mumbai')")
cursor.execute("INSERT INTO customers (name, email, city) VALUES ('Anita', 'anita@email.com', 'Chennai')")
conn.commit()

# Add products
cursor.execute("INSERT INTO products (product_name, price) VALUES ('Laptop', 50000)")
cursor.execute("INSERT INTO products (product_name, price) VALUES ('Phone', 20000)")
cursor.execute("INSERT INTO products (product_name, price) VALUES ('Headphones', 2000)")
conn.commit()

# Add orders (who bought what)
cursor.execute("INSERT INTO orders (customer_id, product_id, quantity) VALUES (1, 1, 1)")  # Vishnu bought 1 Laptop
cursor.execute("INSERT INTO orders (customer_id, product_id, quantity) VALUES (1, 3, 2)")  # Vishnu bought 2 Headphones
cursor.execute("INSERT INTO orders (customer_id, product_id, quantity) VALUES (2, 2, 1)")  # Priya bought 1 Phone
cursor.execute("INSERT INTO orders (customer_id, product_id, quantity) VALUES (2, 1, 1)")  # Priya bought 1 Laptop
cursor.execute("INSERT INTO orders (customer_id, product_id, quantity) VALUES (3, 3, 3)")  # Rahul bought 3 Headphones
conn.commit()

cursor.execute("""
 SELECT customers.name,
       SUM(products.price * orders.quantity) as total_revenue,
       RANK() OVER(
               PARTITION BY customers.products
               (ORDER BY SUM(products.price * orders.quantity) DESC)
              as rank
FROM orders
INNER JOIN customers ON orders.customer_id = customers.id
INNER JOIN products ON orders.product_id = products.id
GROUP BY customers.name
""")
rows = cursor.fetchall()
for rows in rows:
    print(rows)