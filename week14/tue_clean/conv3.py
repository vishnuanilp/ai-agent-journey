import pandas as pd

df = pd.read_csv("bills.csv", encoding="utf-8")
print(df)
print("\namount type:", df["amount"].dtype)

try:
    pd.to_numeric(df["amount"])
except ValueError as e:
    print("\nraise stopped:", e)

before = df["amount"].isna().sum()
df["num"] = pd.to_numeric(df["amount"], errors="coerce")
after = df["num"].isna().sum()
print("\nNaN before:", before, " after:", after, " destroyed:", after - before)
print(df[df["num"].isna() & df["amount"].notna()])