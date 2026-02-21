import matplotlib.pyplot as plt
import pandas as pd

def bar_sales_by_category(df: pd.DataFrame):
    g = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots()
    ax.bar(g.index, g.values)
    ax.set_title("Sales by Category / Vendas por Categoria")
    ax.tick_params(axis="x", rotation=0)
    fig.tight_layout()
    return fig

def pie_sales_by_region(df: pd.DataFrame):
    g = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots()
    ax.pie(g.values, labels=g.index, autopct="%1.1f%%")
    ax.set_title("Sales Share by Region / Participação por Região")
    fig.tight_layout()
    return fig

def line_monthly_sales_profit(monthly_df: pd.DataFrame):
    fig, ax = plt.subplots()
    ax.plot(monthly_df["YearMonth"], monthly_df["Sales"], label="Sales")
    ax.plot(monthly_df["YearMonth"], monthly_df["Profit"], label="Profit")
    ax.set_title("Monthly Trend / Tendência Mensal")
    ax.tick_params(axis="x", rotation=60)
    ax.legend()
    fig.tight_layout()
    return fig
