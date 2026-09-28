import pandas as pd
import matplotlib.pyplot as plt

WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def job_mail(by):
    if by not in ("day", "sender"):
        return {"error": "by must be 'day' or 'sender'"}
    df = pd.read_csv("jobs.csv")
    df["day"] = pd.to_datetime(df["received_utc"], utc=True).dt.tz_convert("Europe/Paris").dt.day_name()
    table = df.groupby(by).size()
    table = table.reindex(WEEK, fill_value=0) if by == "day" else table
    plt.figure(figsize=(10, 4)); plt.bar(table.index, table.values); plt.title(f"job emails per {by} (Paris time)"); plt.savefig(f"jobs_{by}.png"); plt.close()
    return {"per_" + by: {k: int(v) for k, v in table.items()}, "chart_total": int(table.sum()), "rows": len(df)}

if __name__ == "__main__":
    print(job_mail("day"))
    print(job_mail("sender"))
    print(job_mail("type"))