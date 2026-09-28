import pandas as pd

df = pd.DataFrame({
    "room": ["deluxe", "deluxe", "standard", "standard", "standard", "suite", "deluxe", "standard"],
    "day": ["Mon", "Mon", "Mon", "Tue", "Tue", "Mon", "Tue", "Fri"],
    "amount": [2000, 2000, 1500, 1000, 2000, 5000, 2000, 1200],
})

print(pd.pivot_table(df, index="room", columns="day", values="amount"))

p = pd.pivot_table(df, index="room", columns="day", values="amount",
                   aggfunc="sum", fill_value=0, margins=True)
print("\nwith aggfunc=sum:")
print(p)
print("\ntable total:", df["amount"].sum(), " All corner:", p.loc["All", "All"])
print("\nreordered:")
print(p[["Mon", "Tue", "Fri", "All"]])