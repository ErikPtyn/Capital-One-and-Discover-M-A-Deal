import pandas as pd
import numpy as np

df = pd.read_csv("COF_prices_2024-02-04_2025-06-18.csv", sep=";", parse_dates=["Date"])
df = df.sort_values("Date")

df["Relative_stock"] = df["COF"] / df["COF"].shift(1)
df["u"] = np.log(df["Relative_stock"])
df["u2"] = df["u"] ** 2
df = df.dropna()

def period_label(d):
    if d < pd.Timestamp("2024-02-19"):
        return "Pre_announcement"
    elif d <= pd.Timestamp("2025-05-18"):
        return "Deal_pending"
    else:
        return "Post_closing"

df["Period"] = df["Date"].apply(period_label)

df.to_csv("COF_returns_by_period.csv", sep=";", index=False)

group = df.groupby("Period").agg(
    n=("u", "count"),
    sum_u=("u", "sum"),
    sum_u2=("u2", "sum")
).reset_index()

group["mean_u"] = group["sum_u"] / group["n"]
group["var_u"] = (group["sum_u2"] - group["n"] * group["mean_u"]**2) / (group["n"] - 1)
group["sigma_daily"] = np.sqrt(group["var_u"])
group["sigma_annual"] = group["sigma_daily"] * np.sqrt(250)

group.to_csv("COF_volatility_by_period.csv", sep=";", index=False)

print(group)
