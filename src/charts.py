import matplotlib.pyplot as plt

def bar_sales_by_category(df):
    g = df.groupby("Category")["Sales"].sum()
    fig, ax = plt.subplots()
    ax.bar(g.index, g.values)
    return fig

def pie_sales_by_region(df):
    g = df.groupby("Region")["Sales"].sum()
    fig, ax = plt.subplots()
    ax.pie(g.values, labels=g.index, autopct="%1.1f%%")
    return fig

def line_monthly_sales_profit(df):
    g = df.groupby("Year")["Sales"].sum()
    fig, ax = plt.subplots()
    ax.plot(g.index, g.values)
    return fig
