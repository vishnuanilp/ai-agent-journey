import pandas as pd

df = pd.read_csv("clinic.csv")
print(df)

try:
    pd.to_datetime(df["appt"])
except ValueError as e:
    print("\nguess failed:", str(e).splitlines()[0])

df["dayfirst"] = pd.to_datetime(df["appt"], format="%d/%m/%Y", errors="coerce")
df["monthfirst"] = pd.to_datetime(df["appt"], format="%m/%d/%Y", errors="coerce")
print(df[["patient", "appt", "dayfirst", "monthfirst"]])
print("\nholes day-first:", df["dayfirst"].isna().sum(), " month-first:", df["monthfirst"].isna().sum())