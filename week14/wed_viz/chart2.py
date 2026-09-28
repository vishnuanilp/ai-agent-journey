import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("shop.csv")
df["day"] = pd.to_datetime(df["date"], format="%Y-%m-%d").dt.day_name()

total = df.groupby("day")["amount"].sum()
avg = df.groupby("day")["amount"].mean()
print("file total:", df["amount"].sum(), "| sum chart:", total.sum(), "| mean chart:", round(avg.sum(), 2))

fig, (left, right) = plt.subplots(1, 2, figsize=(10, 4))
left.bar(total.index, total.values)
left.set_title("sum - money per day")
right.bar(avg.index, avg.values)
right.set_title("mean - typical sale per day")
fig.savefig("chart2.png")
print("saved chart2.png")