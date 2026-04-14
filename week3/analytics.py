import sqlite3
import os

if os.path.exists("analytics.db"):
    os.remove("analytics.db")

conn = sqlite3.connect("analytics.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        department TEXT
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
    CREATE TABLE IF NOT EXISTS sales  (
        id INTEGER PRIMARY KEY,
        employee_id INTEGER,
        product_id  INTEGER,
        quantity  INTEGER,
        month TEXT
               
    )
""")

# Employees
cursor.execute("INSERT INTO employees (name, department) VALUES ('Vishnu', 'Electronics')")
cursor.execute("INSERT INTO employees (name, department) VALUES ('Priya', 'Electronics')")
cursor.execute("INSERT INTO employees (name, department) VALUES ('Rahul', 'Furniture')")
cursor.execute("INSERT INTO employees (name, department) VALUES ('Anita', 'Furniture')")

# Products
cursor.execute("INSERT INTO products (product_name, price) VALUES ('Laptop', 50000)")
cursor.execute("INSERT INTO products (product_name, price) VALUES ('Phone', 20000)")
cursor.execute("INSERT INTO products (product_name, price) VALUES ('Chair', 5000)")
cursor.execute("INSERT INTO products (product_name, price) VALUES ('Desk', 15000)")

# Sales (who sold what, how many, which month)
cursor.execute("INSERT INTO sales (employee_id, product_id, quantity, month) VALUES (1, 1, 3, 'January')")
cursor.execute("INSERT INTO sales (employee_id, product_id, quantity, month) VALUES (1, 2, 5, 'January')")
cursor.execute("INSERT INTO sales (employee_id, product_id, quantity, month) VALUES (1, 1, 2, 'February')")
cursor.execute("INSERT INTO sales (employee_id, product_id, quantity, month) VALUES (2, 2, 4, 'January')")
cursor.execute("INSERT INTO sales (employee_id, product_id, quantity, month) VALUES (2, 1, 1, 'February')")
cursor.execute("INSERT INTO sales (employee_id, product_id, quantity, month) VALUES (2, 2, 6, 'February')")
cursor.execute("INSERT INTO sales (employee_id, product_id, quantity, month) VALUES (3, 3, 10, 'January')")
cursor.execute("INSERT INTO sales (employee_id, product_id, quantity, month) VALUES (3, 4, 3, 'January')")
cursor.execute("INSERT INTO sales (employee_id, product_id, quantity, month) VALUES (3, 3, 8, 'February')")
cursor.execute("INSERT INTO sales (employee_id, product_id, quantity, month) VALUES (4, 4, 5, 'January')")
cursor.execute("INSERT INTO sales (employee_id, product_id, quantity, month) VALUES (4, 3, 7, 'February')")
cursor.execute("INSERT INTO sales (employee_id, product_id, quantity, month) VALUES (4, 4, 4, 'February')")
conn.commit()

cursor.execute("""
    SELECT employees.name, SUM(products.price * sales.quantity) as total_revenue
    FROM sales
    INNER JOIN employees ON sales.employee_id = employees.id
    INNER JOIN products ON sales.product_id = products.id
    GROUP BY employees.name
""")

cursor.execute("""
    SELECT AVG(products.price * sales.quantity) as avg_sale_value
    FROM sales
    INNER JOIN products ON sales.product_id = products.id
""")

cursor.execute("""
SELECT employees.department, AVG(products.price * sales.quantity) as avg_sale
FROM sales
INNER JOIN employees ON sales.employee_id = employees.id
INNER JOIN products ON sales.product_id = products.id
GROUP BY employees.department
""")

cursor.execute("""
    SELECT employees.name,
           SUM(products.price * sales.quantity) as total_revenue,
           RANK() OVER (ORDER BY SUM(products.price * sales.quantity) DESC) as rank
    FROM sales
    INNER JOIN employees ON sales.employee_id = employees.id
    INNER JOIN products ON sales.product_id = products.id
    GROUP BY employees.name
""")
cursor.execute("""
    SELECT employees.name,
           employees.department,
           SUM(products.price * sales.quantity) as total_revenue,
           RANK() OVER (PARTITION BY employees.department ORDER BY SUM(products.price * sales.quantity) DESC) as dept_rank
    FROM sales
    INNER JOIN employees ON sales.employee_id = employees.id
    INNER JOIN products ON sales.product_id = products.id
    GROUP BY employees.name
""")

cursor.execute("""
    SELECT sales.month,
           SUM(products.price * sales.quantity) as monthly_revenue
    FROM sales
    INNER JOIN products ON sales.product_id = products.id
    GROUP BY sales.month
""")
cursor.execute("""
    SELECT month,
           monthly_revenue,
           LAG(monthly_revenue) OVER (ORDER BY month) as previous_month,
           monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY month) as change
    FROM (
        SELECT sales.month,
               SUM(products.price * sales.quantity) as monthly_revenue
        FROM sales
        INNER JOIN products ON sales.product_id = products.id
        GROUP BY sales.month
    )
""")
cursor.execute("""
    SELECT employees.name,
           sales.month,
           SUM(products.price * sales.quantity) as revenue,
           RANK() OVER (PARTITION BY sales.month ORDER BY SUM(products.price * sales.quantity) DESC) as monthly_rank
    FROM sales
    INNER JOIN employees ON sales.employee_id = employees.id
    INNER JOIN products ON sales.product_id = products.id
    GROUP BY employees.name, sales.month
""")

cursor.execute("""
    SELECT month,
           monthly_revenue,
           LAG(monthly_revenue) OVER (
               ORDER BY CASE month
                   WHEN 'January' THEN 1
                   WHEN 'February' THEN 2
                   WHEN 'March' THEN 3
               END
           ) as previous_month
    FROM (
        SELECT sales.month,
               SUM(products.price * sales.quantity) as monthly_revenue
        FROM sales
        INNER JOIN products ON sales.product_id = products.id
        GROUP BY sales.month
    )
    ORDER BY CASE month
        WHEN 'January' THEN 1
        WHEN 'February' THEN 2
        WHEN 'March' THEN 3
    END
""")

rows = cursor.fetchall()
for row in rows:
    print(row)


rows = cursor.fetchall()
for row in rows:
    print(row) 






