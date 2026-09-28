import pandas as pd

df = pd.read_csv("sales.csv")

mask = df["qty"] > 5
print("=== THE MASK ===")
print(mask)

print("\n=== ROWS WHERE TRUE ===")
print(df[mask])

print("\n=== TWO CONDITIONS ===")
print(df[(df["qty"] > 1) & (df["price"] > 100)])