import pandas as pd

def kpis(df):
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    orders = df["Order ID"].nunique()
    customers = df["Customer ID"].nunique()

    avg_ticket = total_sales / orders if orders else 0
    margin = total_profit / total_sales if total_sales else 0

    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "orders": orders,
        "customers": customers,
        "avg_ticket": avg_ticket,
        "margin": margin
    }

def top_products(df, n=10):
    return (
        df.groupby("Product Name")["Sales"]
          .sum()
          .sort_values(ascending=False)
          .head(n)
          .reset_index()
    )

def profit_by_subcategory(df):
    return (
        df.groupby("Sub-Category")["Profit"]
          .sum()
          .sort_values()
          .reset_index()
    )

def monthly_trend(df):
    df["YearMonth"] = df["Order Date"].dt.to_period("M").astype(str)
    return (
        df.groupby("YearMonth")[["Sales", "Profit"]]
          .sum()
          .reset_index()
    )
