import pandas as pd

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]

    # Aceita "Order Date" ou "OrderDate"
    if "Order Date" in df.columns:
        df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    elif "OrderDate" in df.columns:
        df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")
        df = df.rename(columns={"OrderDate": "Order Date"})
    else:
        raise ValueError("CSV não tem coluna de data (Order Date / OrderDate)")

    df = df.dropna(subset=["Order Date"])

    # numéricos (se existirem)
    for col in ["Sales", "Profit", "Discount"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    if "Quantity" in df.columns:
        df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0).astype(int)
    else:
        df["Quantity"] = 0

    # features
    df["Year"] = df["Order Date"].dt.year
    df["YearMonth"] = df["Order Date"].dt.to_period("M").astype(str)

    return df

def apply_filters(df, years=None, regions=None, segments=None, categories=None, subcategories=None):
    out = df.copy()

    if years:
        out = out[out["Year"].isin(years)]
    if regions:
        out = out[out["Region"].isin(regions)]
    if segments:
        out = out[out["Segment"].isin(segments)]
    if categories:
        out = out[out["Category"].isin(categories)]
    if subcategories:
        out = out[out["Sub-Category"].isin(subcategories)]

    return out
