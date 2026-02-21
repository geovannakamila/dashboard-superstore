import matplotlib.pyplot as plt
import pandas as pd

def _fig(ax_title: str, w=10, h=4.2):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_title(ax_title, fontsize=14, pad=12)
    return fig, ax

def sales_by_category(df: pd.DataFrame, title: str):
    g = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    fig, ax = _fig(title, w=10, h=4.2)
    ax.bar(g.index, g.values)
    ax.set_ylabel("Sales")
    fig.tight_layout()
    return fig

def profit_by_subcategory(df: pd.DataFrame, title: str, top_n: int = 15):
    g = df.groupby("Sub-Category")["Profit"].sum().sort_values(ascending=False).head(top_n)
    fig, ax = _fig(title, w=12, h=5.2)
    ax.barh(g.index[::-1], g.values[::-1])
    ax.set_xlabel("Profit")
    fig.tight_layout()
    return fig

def sales_share_by_region(df: pd.DataFrame, title: str):
    g = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
    fig, ax = _fig(title, w=8.5, h=4.8)
    ax.pie(g.values, labels=g.index, autopct="%1.1f%%", startangle=90)
    fig.tight_layout()
    return fig

def monthly_sales_profit(df_month: pd.DataFrame, title: str):
    fig, ax = _fig(title, w=12, h=4.6)
    ax.plot(df_month["YearMonth"], df_month["Sales"], label="Sales")
    ax.plot(df_month["YearMonth"], df_month["Profit"], label="Profit")
    ax.tick_params(axis="x", rotation=50)
    ax.legend()
    fig.tight_layout()
    return fig

def heatmap_category_region(df: pd.DataFrame, title: str):
    pivot = pd.pivot_table(
        df, values="Sales", index="Category", columns="Region",
        aggfunc="sum", fill_value=0
    )
    fig, ax = _fig(title, w=10.5, h=4.8)
    im = ax.imshow(pivot.values)
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns, rotation=30, ha="right")
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    return fig

def top_bar(df: pd.DataFrame, x_col: str, y_col: str, title: str, top_n: int = 10):
    g = df.groupby(x_col)[y_col].sum().sort_values(ascending=False).head(top_n)
    fig, ax = _fig(title, w=12, h=5.0)
    ax.barh(g.index[::-1], g.values[::-1])
    ax.set_xlabel(y_col)
    fig.tight_layout()
    return fig
