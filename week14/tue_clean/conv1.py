import pandas as pd

df = pd.read_csv("sales.csv")

print("--- date column as pandas loaded it ---")
print(df["date"])

print("\n--- the column's type ---")
print(df["date"].dtype)

print("\n--- one single value, and its Python type ---")
print(repr(df["date"][0]), type(df["date"][0]))

print("\n--- sorted as it is now ---")
print(df["date"].sort_values(kind="mergesort"))