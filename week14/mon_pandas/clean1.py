import pandas as pd

df = pd.read_csv("sales.csv")

print("=== SORTED BY PRICE ===")
print(df.sort_values("price"))

print("\n=== df IS UNCHANGED ===")
print(df.head(3))

print("\n=== HOLES PER COLUMN ===")
print(df.isna().sum())

print("\n=== THE ROWS WITH HOLES ===")
print(df[df.isna().any(axis=1)])