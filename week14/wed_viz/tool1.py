import pandas as pd
import matplotlib.pyplot as plt

WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def sales_by_day(how):
    if how not in ("sum", "count"):
        return {"error": "how must be 'sum' or 'count'"}
    df = pd.read_csv("shop.csv")
    df["day"] = pd.to_datetime(df["date"], format="%Y-%m-%d").dt.day_name()
    table = df.groupby("day")["amount"].agg(how).reindex(WEEK, fill_value=0)
    plt.figure(figsize=(10, 4)); plt.bar(table.index, table.values); plt.savefig("report.png"); plt.close()
    return {"per_day": {d: int(v) for d, v in table.items()}, "chart_total": int(table.sum()), "rows": len(df), "file_amount": int(df["amount"].sum())}

print(sales_by_day("sum"))
print(sales_by_day("count"))
print(sales_by_day("mean"))