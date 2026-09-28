import pandas as pd
import matplotlib.pyplot as plt

week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
df = pd.read_csv("shop.csv")
df["day"] = pd.to_datetime(df["date"], format="%Y-%m-%d").dt.day_name()

alpha = df.groupby("day")["amount"].sum()
ordered = alpha.reindex(week, fill_value=0)
print(alpha)
print(ordered)
print("rows:", len(df), "| file:", df["amount"].sum(), "| alpha:", alpha.sum(), "| ordered:", ordered.sum())

fig, (left, right) = plt.subplots(1, 2, figsize=(16, 4), sharey=True)
left.bar(alpha.index, alpha.values)
left.set_title("groupby default - alphabetical")
right.bar(ordered.index, ordered.values)
right.set_title("reindex - calendar order")
fig.savefig("chart4.png")