import pandas as pd
from read2 import read_and_label

def analyse(rows):
    df = pd.DataFrame(rows, columns=["id", "From", "Date", "Subject"])
    df["sender"] = df["From"].str.extract(r"<([^>]+)>", expand=False).fillna(df["From"]).str.lower()
    df["paris"] = pd.to_datetime(df["Date"], utc=True, format="%a, %d %b %Y %H:%M:%S %z").dt.tz_convert("Europe/Paris")
    df["day"] = df["paris"].dt.day_name()
    by_sender = df["sender"].value_counts()
    by_day = df["day"].value_counts()
    assert by_sender.sum() == by_day.sum() == len(df), "counts do not add up"
    df.to_csv("jobmail.csv", index=False, encoding="utf-8")
    return df, by_sender, by_day

if __name__ == "__main__":
    rows, total = read_and_label()
    df, by_sender, by_day = analyse(rows)
    print("rows", len(df), "| paris column type:", df["paris"].dtype)
    print(df[["sender", "paris", "day"]].to_string(index=False))
    print(by_sender.to_string())
    print(by_day.to_string())