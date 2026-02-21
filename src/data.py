import pandas as pd

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]

    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df = df.dropna(subset=["Order Date"])

    # numéricos
    for col in ["Sales", "Profit", "Discount"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0).astype(int)

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
