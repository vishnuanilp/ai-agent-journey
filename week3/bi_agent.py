import sqlite3
import os
from anthropic import Anthropic
from dotenv import load_dotenv
load_dotenv ()

if os.path.exists("business.db"):
    os.remove("business.db")

conn = sqlite3.connect("business.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE customers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT,
        city TEXT
    )
""")

cursor.execute("""
    CREATE TABLE products (
        id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        price REAL
    )
""")
cursor.execute("""
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        order_date TEXT
    )
""")

customers = [
    ('Vishnu', 'vishnu@email.com', 'Mumbai'),
    ('Priya', 'priya@email.com', 'Delhi'),
    ('Rahul', 'rahul@email.com', 'Mumbai'),
    ('Anita', 'anita@email.com', 'Chennai'),
    ('Deepak', 'deepak@email.com', 'Delhi'),
    ('Meera', 'meera@email.com', 'Chennai')
]
cursor.executemany("INSERT INTO customers (name, email, city) VALUES (?, ?, ?)", customers)
conn.commit()

products = [
    ('Laptop', 50000),
    ('Phone', 20000),
    ('Headphones', 2000),
    ('Tablet', 30000),
    ('Keyboard', 1500)
]
cursor.executemany("INSERT INTO products (product_name, price) VALUES (?, ?)", products)
conn.commit()

orders = [
    (1, 1, 1, '2025-01-15'),
    (1, 3, 2, '2025-01-20'),
    (2, 2, 1, '2025-01-18'),
    (2, 1, 1, '2025-02-10'),
    (3, 3, 3, '2025-02-14'),
    (3, 4, 1, '2025-02-20'),
    (4, 1, 2, '2025-01-25'),
    (5, 2, 1, '2025-02-05'),
    (5, 5, 4, '2025-02-28'),
    (6, 4, 1, '2025-01-10'),
    (6, 1, 1, '2025-02-15'),
    (1, 2, 1, '2025-02-22')
]
cursor.executemany("INSERT INTO orders (customer_id, product_id, quantity, order_date) VALUES (?, ?, ?, ?)", orders)
conn.commit()

def run_sql(query):
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return f"Columns: {columns}\nResults: {results}"
    except Exception as e:
        return f"SQL Error: {e}"
    
tools = [
    {
        "name": "run_sql",
        "description": "Run a SQL query on the business database. The database has three tables: customers (id, name, email, city), products (id, product_name, price), orders (id, customer_id, product_id, quantity, order_date)",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The SQL query to execute"
                }
            },
            "required": ["query"]
        }
    }
]

def run_tool(tool_name, tool_input):
    if tool_name == "run_sql":
        return run_sql(tool_input["query"])
    else:
        return "Tool not found"
    
client = Anthropic()

system_prompt = """You are a Business Intelligence Agent. You analyze business data by writing and running SQL queries.

The database has these tables:
- customers (id, name, email, city)
- products (id, product_name, price)  
- orders (id, customer_id, product_id, quantity, order_date)

When asked a question:
1. Think about what SQL query you need
2. Use the run_sql tool to execute it
3. Look at the results
4. Either run more queries or give a final answer

Use JOINs, GROUP BY, SUM, COUNT, RANK() and other SQL features as needed."""

user_question = input("Ask a business question: ")

messages = [
    {"role": "user", "content": user_question}
]

while True:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=system_prompt,
        tools=tools,
        messages=messages
    )

    messages.append({"role": "assistant", "content": response.content})

    if response.stop_reason == "end_turn":
        for block in response.content:
            if hasattr(block, "text"):
                print(block.text)
        break

    for block in response.content:
        if block.type == "tool_use":
            tool_name = block.name
            tool_input = block.input

            print(f"\n🔧 Agent wants to use: {tool_name}")
            print(f"📝 Query: {tool_input}")

            result = run_tool(tool_name, tool_input)

            print(f"📊 Result: {result}")

            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    }
                ]
            })



