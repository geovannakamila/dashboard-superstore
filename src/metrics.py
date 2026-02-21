def kpis(df):
    return {
        "total_sales": df["Sales"].sum(),
        "total_profit": df["Profit"].sum(),
        "orders": df["Order ID"].nunique()
    }

def top_products(df):
    return df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(10)
