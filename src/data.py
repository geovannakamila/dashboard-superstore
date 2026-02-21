import pandas as pd

def load_data(path):
    df = pd.read_csv(path)
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Year"] = df["Order Date"].dt.year
    return df

def apply_filters(df, years=None, regions=None, segments=None, categories=None):
    if years:
        df = df[df["Year"].isin(years)]
    if regions:
        df = df[df["Region"].isin(regions)]
    if segments:
        df = df[df["Segment"].isin(segments)]
    if categories:
        df = df[df["Category"].isin(categories)]
    return df
