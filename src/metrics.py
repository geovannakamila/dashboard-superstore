import pandas as pd

def kpis(df: pd.DataFrame) -> dict:
    total_sales = float(df["Sales"].sum())
    total_profit = float(df["Profit"].sum())
    orders = int(df["Order ID"].nunique())
    customers = int(df["Customer ID"].nunique())
    avg_ticket = total_sales / orders if orders else 0
    margin = (total_profit / total_sales) if total_sales else 0

    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "orders": orders,
        "customers": customers,
        "avg_ticket": avg_ticket,
        "margin": margin
    }

def top_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    return (
        df.groupby("Product Name", as_index=False)
          .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Qty=("Quantity", "sum"))
          .sort_values("Sales", ascending=False)
          .head(n)
    )

def profit_by_subcategory(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Sub-Category", as_index=False)
          .agg(Profit=("Profit", "sum"), Sales=("Sales", "sum"))
          .sort_values("Profit", ascending=True)
    )

def monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    tmp = df.copy()
    tmp["YearMonth"] = tmp["Order Date"].dt.to_period("M").astype(str)
    return (
        tmp.groupby("YearMonth", as_index=False)
           .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    )
