import pandas as pd

def _safe_nunique(df: pd.DataFrame, col: str) -> int:
    return int(df[col].nunique()) if col in df.columns else 0

def kpis(df: pd.DataFrame) -> dict:
    total_sales = float(df["Sales"].sum()) if "Sales" in df.columns else 0.0
    total_profit = float(df["Profit"].sum()) if "Profit" in df.columns else 0.0

    orders = _safe_nunique(df, "Order ID") or _safe_nunique(df, "OrderID")

    
    customers = _safe_nunique(df, "Customer ID") or _safe_nunique(df, "CustomerID")

    avg_ticket = total_sales / orders if orders else 0.0
    margin = (total_profit / total_sales) if total_sales else 0.0

    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "orders": orders,
        "customers": customers,
        "avg_ticket": avg_ticket,
        "margin": margin
    }

def top_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    if "Product Name" not in df.columns:
        return pd.DataFrame()

    # garante que as colunas existam
    tmp = df.copy()
    for col in ["Sales", "Profit", "Quantity"]:
        if col not in tmp.columns:
            tmp[col] = 0

    out = (
        tmp.groupby("Product Name", as_index=False)
           .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Qty=("Quantity", "sum"))
           .sort_values("Sales", ascending=False)
           .head(n)
    )
    return out

def profit_by_subcategory(df: pd.DataFrame) -> pd.DataFrame:
    if "Sub-Category" not in df.columns:
        return pd.DataFrame()

    tmp = df.copy()
    if "Profit" not in tmp.columns:
        tmp["Profit"] = 0
    if "Sales" not in tmp.columns:
        tmp["Sales"] = 0

    return (
        tmp.groupby("Sub-Category", as_index=False)
           .agg(Profit=("Profit", "sum"), Sales=("Sales", "sum"))
           .sort_values("Profit", ascending=True)
    )

def monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    tmp = df.copy()

    # se não tiver YearMonth, cria
    if "YearMonth" not in tmp.columns:
        if "Order Date" in tmp.columns:
            tmp["Order Date"] = pd.to_datetime(tmp["Order Date"], errors="coerce")
            tmp["YearMonth"] = tmp["Order Date"].dt.to_period("M").astype(str)
        else:
            tmp["YearMonth"] = "Unknown"

    for col in ["Sales", "Profit"]:
        if col not in tmp.columns:
            tmp[col] = 0

    return (
        tmp.groupby("YearMonth", as_index=False)
           .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    )
