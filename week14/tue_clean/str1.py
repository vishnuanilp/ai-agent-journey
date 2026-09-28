import pandas as pd

df = pd.read_csv("bills.csv", encoding="utf-8")
before = df["amount"].isna().sum()

df["fixed"] = df["amount"].str.strip()
df["fixed"] = df["fixed"].str.replace("₹", "")
df["fixed"] = df["fixed"].str.replace(",", "")

df["num"] = pd.to_numeric(df["fixed"], errors="coerce")
after = df["num"].isna().sum()

print(df)
print("\nNaN before:", before, " after:", after, " destroyed:", after - before)
print("total:", df["num"].sum())