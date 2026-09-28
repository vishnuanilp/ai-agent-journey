import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
df = pd.read_csv("shop.csv")
df["day"] = pd.to_datetime(df["date"], format="%Y-%m-%d").dt.day_name()

fig, (left, right) = plt.subplots(1, 2, figsize=(16, 4), sharey=True)
sns.barplot(data=df, x="day", y="amount", ax=left)
sns.barplot(data=df, x="day", y="amount", estimator="sum", errorbar=None, order=week, ax=right)
left.set_title("seaborn default")
right.set_title("estimator=sum, errorbar=None, order=week")

print("file:", df["amount"].sum(), "| left bars:", round(sum(b.get_height() for b in left.patches), 2), "| right bars:", sum(b.get_height() for b in right.patches))
fig.savefig("chart5.png")