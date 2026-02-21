import pandas as pd

def _col(df, name):
    return name in df.columns

def kpis(df: pd.DataFrame) -> dict:
    sales = float(df["Sales"].sum()) if _col(df, "Sales") else 0.0
    profit = float(df["Profit"].sum()) if _col(df, "Profit") else 0.0

    orders = int(df["Order ID"].nunique()) if _col(df, "Order ID") else 0
    customers = int(df["Customer ID"].nunique()) if _col(df, "Customer ID") else 0

    avg_ticket = sales / orders if orders else 0.0
    margin = (profit / sales) if sales else 0.0

    avg_discount = float(df["Discount"].mean()) if _col(df, "Discount") else 0.0
    qty = int(df["Quantity"].sum()) if _col(df, "Quantity") else 0

    ship_days_avg = None
    if _col(df, "Ship Days"):
        ship_days_avg = float(df["Ship Days"].mean())

    return {
        "sales": sales,
        "profit": profit,
        "orders": orders,
        "customers": customers,
        "avg_ticket": avg_ticket,
        "margin": margin,
        "avg_discount": avg_discount,
        "qty": qty,
        "ship_days_avg": ship_days_avg
    }

def monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    tmp = df.copy()
    if "YearMonth" not in tmp.columns:
        tmp["YearMonth"] = tmp["Order Date"].dt.to_period("M").astype(str)

    for col in ["Sales", "Profit"]:
        if col not in tmp.columns:
            tmp[col] = 0

    return (
        tmp.groupby("YearMonth", as_index=False)
           .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    )

def top_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    if "Product Name" not in df.columns:
        return pd.DataFrame()

    tmp = df.copy()
    for col in ["Sales", "Profit", "Quantity"]:
        if col not in tmp.columns:
            tmp[col] = 0

    return (
        tmp.groupby("Product Name", as_index=False)
           .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Qty=("Quantity", "sum"))
           .sort_values("Sales", ascending=False)
           .head(n)
    )

def profit_by_subcategory(df: pd.DataFrame) -> pd.DataFrame:
    if "Sub-Category" not in df.columns:
        return pd.DataFrame()

    tmp = df.copy()
    for col in ["Sales", "Profit"]:
        if col not in tmp.columns:
            tmp[col] = 0

    out = (
        tmp.groupby("Sub-Category", as_index=False)
           .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    )
    out["Margin"] = out["Profit"] / out["Sales"].replace(0, 1)
    return out.sort_values("Profit", ascending=False)
