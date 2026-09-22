"""Rebuilds Cleaned_data.csv from the three raw source files and prints
every number quoted in the README, so the README can't drift from the data.

Also documents the bug this rebuild fixed: the original query subtracted
COGS once per row, regardless of how many riders were in that row, instead
of scaling it by rider volume. That produced a 99.7% profit margin, which
isn't a real business's margin — a number that should have been sanity-
checked before it went in a README, not just computed and trusted.
"""

import os

import pandas as pd

ROOT = os.path.dirname(os.path.abspath(__file__))


def main():
    y1 = pd.read_csv(os.path.join(ROOT, "year_01.csv"))
    y2 = pd.read_csv(os.path.join(ROOT, "year_02.csv"))
    cost = pd.read_csv(os.path.join(ROOT, "cost.csv"))

    df = pd.concat([y1, y2], ignore_index=True)
    df = df.merge(cost, on="yr", how="left")
    if df["price"].isna().any() or df["COGS"].isna().any():
        raise SystemExit("a row's yr didn't match cost.csv — check the join")

    df["revenue"] = df["riders"] * df["price"]
    # COGS in cost.csv is cost PER RIDER (it lines up with price, which is
    # per rider) — so it has to scale with volume, the same way revenue does.
    df["profit"] = df["revenue"] - (df["riders"] * df["COGS"])

    out = df[["dteday", "season", "yr", "weekday", "hr", "rider_type", "riders",
              "price", "COGS", "revenue", "profit"]]
    out.to_csv(os.path.join(ROOT, "Cleaned_data.csv"), index=False)

    total_revenue = df["revenue"].sum()
    total_profit = df["profit"].sum()
    buggy_profit = (df["revenue"] - df["COGS"]).sum()  # the original formula, for comparison

    print(f"rows: {len(df):,}")
    print(f"total riders: {df['riders'].sum():,}")
    print(f"total revenue: ${total_revenue:,.2f}")
    print(f"total profit (corrected): ${total_profit:,.2f}  ({total_profit/total_revenue:.1%} margin)")
    print(f"total profit (original buggy formula): ${buggy_profit:,.2f}  ({buggy_profit/total_revenue:.1%} margin)")
    print()
    print("revenue share by rider type:")
    print((df.groupby("rider_type")["revenue"].sum() / total_revenue * 100).round(1))
    print()
    print("revenue by season (1=winter .. 4=fall):")
    print(df.groupby("season")["revenue"].sum().round(2))
    print()
    print("revenue by hour, top 6:")
    print(df.groupby("hr")["revenue"].sum().sort_values(ascending=False).head(6).round(2))
    print()
    print("revenue by weekday (0=Sun..6=Sat):")
    print(df.groupby("weekday")["revenue"].sum().sort_values(ascending=False).round(2))


if __name__ == "__main__":
    main()
