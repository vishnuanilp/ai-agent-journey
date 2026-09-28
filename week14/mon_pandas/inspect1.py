import pandas as pd

df = pd.read_csv("sales.csv")

print("=== HEAD ===")
print(df.head())

print("\n=== INFO ===")
df.info()

print("\n=== DESCRIBE ===")
print(df.describe())