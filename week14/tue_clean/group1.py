import pandas as pd

df = pd.DataFrame({
    "stylist": ["Priya", "Ravi", "Priya", "Ravi", "priya ", "Meera", None, "Ravi", "Meera"],
    "amount": [500, 300, 700, None, 400, None, 250, 350, None],
})

g = df.groupby("stylist")["amount"]
print(pd.DataFrame({"sum": g.sum(), "size": g.size(), "count": g.count()}))
print("\ntotal in table:", df["amount"].sum(), " total in groups:", g.sum().sum())

print("\nwith dropna=False:")
print(df.groupby("stylist", dropna=False)["amount"].sum())

df["stylist"] = df["stylist"].str.strip().str.title()
print("\nafter cleaning keys:")
print(df.groupby("stylist")["amount"].sum())