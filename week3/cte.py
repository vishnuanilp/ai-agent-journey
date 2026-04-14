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
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY,
        employee_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        month TEXT
    )
""")

cursor.execute("INSERT INTO employees (name, department) VALUES ('Vishnu', 'Electronics')")
cursor.execute("INSERT INTO employees (name, department) VALUES ('Priya', 'Electronics')")
cursor.execute("INSERT INTO employees (name, department) VALUES ('Rahul', 'Furniture')")
cursor.execute("INSERT INTO employees (name, department) VALUES ('Anita', 'Furniture')")

cursor.execute("INSERT INTO products (product_name, price) VALUES ('Laptop', 50000)")
cursor.execute("INSERT INTO products (product_name, price) VALUES ('Phone', 20000)")
cursor.execute("INSERT INTO products (product_name, price) VALUES ('Chair', 5000)")
cursor.execute("INSERT INTO products (product_name, price) VALUES ('Desk', 15000)")

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
    WITH monthly_totals AS (
        SELECT month, SUM(products.price * sales.quantity) as revenue
        FROM sales
        INNER JOIN products ON sales.product_id = products.id
        GROUP BY month
    )
    SELECT * FROM monthly_totals
""")



cursor.execute("""
    WITH employee_revenue AS (
        SELECT employees.name,
               employees.department,
               SUM(products.price * sales.quantity) as total_revenue
        FROM sales
        INNER JOIN employees ON sales.employee_id = employees.id
        INNER JOIN products ON sales.product_id = products.id
        GROUP BY employees.name
    ),
    dept_average AS (
        SELECT department, AVG(total_revenue) as avg_revenue
        FROM employee_revenue
        GROUP BY department
    )
    SELECT employee_revenue.name,
           employee_revenue.department,
           employee_revenue.total_revenue,
           dept_average.avg_revenue
    FROM employee_revenue
    INNER JOIN dept_average ON employee_revenue.department = dept_average.department
""")

cursor.execute("""
    CREATE VIEW IF NOT EXISTS employee_sales AS
    SELECT employees.name,
           employees.department,
           products.product_name,
           products.price * sales.quantity as sale_value,
           sales.month
    FROM sales
    INNER JOIN employees ON sales.employee_id = employees.id
    INNER JOIN products ON sales.product_id = products.id
""")
cursor.execute("SELECT * FROM employee_sales")

cursor.execute("""
    SELECT name, SUM(sale_value) as total
    FROM employee_sales
    GROUP BY name
""")

cursor.execute("""
    WITH top_sellers AS (
        SELECT name, SUM(sale_value) as total
        FROM employee_sales
        GROUP BY name
    )
    SELECT * FROM top_sellers WHERE total > 200000
""")

cursor.execute("""
    CREATE VIEW IF NOT EXISTS dept_monthly AS
    SELECT department, month, SUM(sale_value) as revenue
    FROM employee_sales
    GROUP BY department, month
""")
cursor.execute("SELECT * FROM dept_monthly")

cursor.execute("""
    WITH ranked_depts AS (
        SELECT department, month, revenue,
               RANK() OVER (PARTITION BY month ORDER BY revenue DESC) as rank
        FROM dept_monthly
    )
    SELECT * FROM ranked_depts WHERE rank = 1
""")

rows = cursor.fetchall()
for row in rows:
    print(row)
    
rows = cursor.fetchall()
for row in rows:
    print(row)

