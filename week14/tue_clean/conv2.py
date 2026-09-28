import pandas as pd

df = pd.read_csv("sales.csv")
df["when"] = pd.to_datetime(df["date"], format="%Y-%m-%d")

print(df[["date", "when"]].dtypes)

df["weekday"] = df["when"].dt.day_name()
df["days_in"] = (df["when"] - df["when"].min()).dt.days
print(df[["date", "when", "weekday", "days_in"]])

try:
    print(df["date"].dt.day_name())
except AttributeError as e:
    print("\ntext column refused:", e)