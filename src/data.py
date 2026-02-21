import pandas as pd

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]

    # Datas
    if "Order Date" in df.columns:
        df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    else:
        raise ValueError("CSV precisa ter a coluna 'Order Date'.")

    if "Ship Date" in df.columns:
        df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")

    df = df.dropna(subset=["Order Date"])

    # Numéricos
    for col in ["Sales", "Profit", "Discount"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    if "Quantity" in df.columns:
        df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0).astype(int)
    else:
        df["Quantity"] = 0

    # Features
    df["Year"] = df["Order Date"].dt.year
    df["YearMonth"] = df["Order Date"].dt.to_period("M").astype(str)

    # Shipping days (se existir Ship Date)
    if "Ship Date" in df.columns:
        df["Ship Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
    return df

def apply_filters(
    df,
    years=None,
    regions=None,
    segments=None,
    categories=None,
    subcategories=None,
    ship_modes=None,
    states=None,
    cities=None,
    date_range=None
):
    out = df.copy()

    if date_range and len(date_range) == 2:
        start, end = date_range
        out = out[(out["Order Date"] >= pd.to_datetime(start)) & (out["Order Date"] <= pd.to_datetime(end))]

    if years:
        out = out[out["Year"].isin(years)]
    if regions and "Region" in out.columns:
        out = out[out["Region"].isin(regions)]
    if segments and "Segment" in out.columns:
        out = out[out["Segment"].isin(segments)]
    if categories and "Category" in out.columns:
        out = out[out["Category"].isin(categories)]
    if subcategories and "Sub-Category" in out.columns:
        out = out[out["Sub-Category"].isin(subcategories)]
    if ship_modes and "Ship Mode" in out.columns:
        out = out[out["Ship Mode"].isin(ship_modes)]
    if states and "State" in out.columns:
        out = out[out["State"].isin(states)]
    if cities and "City" in out.columns:
        out = out[out["City"].isin(cities)]

    return out
