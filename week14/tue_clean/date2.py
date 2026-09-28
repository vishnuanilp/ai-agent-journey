import pandas as pd

df = pd.read_csv("clinic.csv")

try:
    pd.to_datetime(df["sent"])
except ValueError as e:
    print("mixed zones refused:", str(e).splitlines()[0])

df["local_day"] = pd.to_datetime(df["sent"].str[:10]).dt.day_name()
df["utc"] = pd.to_datetime(df["sent"], utc=True)
df["utc_day"] = df["utc"].dt.day_name()
df["paris"] = df["utc"].dt.tz_convert("Europe/Paris")
df["paris_day"] = df["paris"].dt.day_name()

print(df[["patient", "utc", "paris"]])
print(df[["patient", "local_day", "utc_day", "paris_day"]])