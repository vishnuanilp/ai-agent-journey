import pandas as pd

df = pd.read_csv("sales.csv")

prices = df["price"]
print("=== ONE COLUMN (Series) ===")
print(prices)
print("type:", type(prices))

print("\n=== TWO COLUMNS (DataFrame) ===")
print(df[["item", "price"]])

print("\n=== REVENUE ===")
print(df["qty"] * df["price"])