import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("shop.csv")
df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
df["day"] = df["date"].dt.day_name()

daily = df.groupby("day")["amount"].sum()
print(daily)
print("rows:", len(df), "| table total:", df["amount"].sum(), "| chart total:", daily.sum())

plt.bar(daily.index, daily.values)
plt.title("Shop sales by day (₹)")
plt.ylabel("sales ₹")
plt.savefig("chart1.png")
print("saved chart1.png")