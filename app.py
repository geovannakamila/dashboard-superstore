import streamlit as st

from src.data import load_data, apply_filters
from src.metrics import kpis, top_products, profit_by_subcategory, monthly_trend
from src.charts import (
    sales_by_category,
    profit_by_subcategory as chart_profit_by_subcat,
    sales_share_by_region,
    monthly_sales_profit,
    heatmap_category_region,
    top_bar
)

st.set_page_config(page_title="Sales Dashboard | Superstore", layout="wide")

@st.cache_data
def get_df():
    return load_data("data/superstore.csv")

df = get_df()

lang = st.sidebar.radio("🌐 Language / Idioma", ["Português", "English"])

TEXT = {
    "Português": {
        "title": "📊 Dashboard Avançado de Análise de Vendas",
        "subtitle": "Projeto de portfólio com Python, Pandas, Matplotlib e Streamlit",
        "filters": "Filtros",
        "date": "Período",
        "year": "Ano",
        "region": "Região",
        "segment": "Segmento",
        "category": "Categoria",
        "subcategory": "Sub-Categoria",
        "shipmode": "Modo de Envio",
        "state": "Estado",
        "city": "Cidade",
        "sales": "Vendas",
        "profit": "Lucro",
        "orders": "Pedidos",
        "customers": "Clientes",
        "avg_ticket": "Ticket Médio",
        "margin": "Margem",
        "avg_discount": "Desconto Médio",
        "qty": "Qtd Itens",
        "ship_days": "Dias p/ Entrega (média)",
        "tab_overview": "Visão Geral",
        "tab_trends": "Tendências",
        "tab_products": "Produtos",
        "tab_profit": "Rentabilidade",
        "tab_data": "Dados",
        "download": "Baixar CSV filtrado",
        "download_agg": "Baixar relatório (Sub-Category)"
    },
    "English": {
        "title": "📊 Advanced Sales Dashboard",
        "subtitle": "Portfolio project using Python, Pandas, Matplotlib and Streamlit",
        "filters": "Filters",
        "date": "Date range",
        "year": "Year",
        "region": "Region",
        "segment": "Segment",
        "category": "Category",
        "subcategory": "Sub-Category",
        "shipmode": "Ship Mode",
        "state": "State",
        "city": "City",
        "sales": "Sales",
        "profit": "Profit",
        "orders": "Orders",
        "customers": "Customers",
        "avg_ticket": "Average Ticket",
        "margin": "Margin",
        "avg_discount": "Avg Discount",
        "qty": "Items Qty",
        "ship_days": "Ship Days (avg)",
        "tab_overview": "Overview",
        "tab_trends": "Trends",
        "tab_products": "Products",
        "tab_profit": "Profitability",
        "tab_data": "Data",
        "download": "Download filtered CSV",
        "download_agg": "Download report (Sub-Category)"
    }
}
T = TEXT[lang]

def money(v: float) -> str:
    # simples e bonito (sem depender de locale)
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if lang == "Português" else f"${v:,.2f}"

st.title(T["title"])
st.caption(T["subtitle"])

# ---------- Sidebar filters ----------
st.sidebar.header(T["filters"])

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()
date_range = st.sidebar.date_input(T["date"], value=(min_date, max_date), min_value=min_date, max_value=max_date)

years = sorted(df["Year"].unique())

def _opts(col):
    return sorted(df[col].dropna().unique()) if col in df.columns else []

regions = _opts("Region")
segments = _opts("Segment")
categories = _opts("Category")
subcats = _opts("Sub-Category")
ship_modes = _opts("Ship Mode")
states = _opts("State")
cities = _opts("City")

year_sel = st.sidebar.multiselect(T["year"], years, default=years)

region_sel = st.sidebar.multiselect(T["region"], regions, default=regions) if regions else []
segment_sel = st.sidebar.multiselect(T["segment"], segments, default=segments) if segments else []
category_sel = st.sidebar.multiselect(T["category"], categories, default=categories) if categories else []
subcat_sel = st.sidebar.multiselect(T["subcategory"], subcats, default=subcats) if subcats else []

# filtros extras só se existirem
ship_sel = st.sidebar.multiselect(T["shipmode"], ship_modes, default=ship_modes) if ship_modes else []
state_sel = st.sidebar.multiselect(T["state"], states, default=states) if states else []
city_sel = st.sidebar.multiselect(T["city"], cities, default=cities) if cities else []

df_filtered = apply_filters(
    df,
    date_range=date_range,
    years=year_sel,
    regions=region_sel,
    segments=segment_sel,
    categories=category_sel,
    subcategories=subcat_sel,
    ship_modes=ship_sel,
    states=state_sel,
    cities=city_sel
)

# ---------- KPIs ----------
k = kpis(df_filtered)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric(T["sales"], money(k["sales"]))
col2.metric(T["profit"], money(k["profit"]))
col3.metric(T["orders"], f"{k['orders']}")
col4.metric(T["avg_ticket"], money(k["avg_ticket"]))
col5.metric(T["margin"], f"{k['margin']*100:.1f}%")

col6, col7, col8 = st.columns(3)
col6.metric(T["avg_discount"], f"{k['avg_discount']*100:.1f}%")
col7.metric(T["qty"], f"{k['qty']}")
col8.metric(T["ship_days"], "-" if k["ship_days_avg"] is None else f"{k['ship_days_avg']:.1f}")

# ---------- Tabs ----------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    T["tab_overview"], T["tab_trends"], T["tab_products"], T["tab_profit"], T["tab_data"]
])

with tab1:
    left, right = st.columns([1, 1])
    with left:
        st.pyplot(sales_by_category(df_filtered, "Sales by Category / Vendas por Categoria"))
    with right:
        if "Region" in df_filtered.columns:
            st.pyplot(sales_share_by_region(df_filtered, "Sales Share by Region / Participação por Região"))
        else:
            st.info("Region column not found.")

    if "Region" in df_filtered.columns and "Category" in df_filtered.columns:
        st.pyplot(heatmap_category_region(df_filtered, "Heatmap: Category x Region (Sales) / Mapa de Calor"))

with tab2:
    m = monthly_trend(df_filtered)
    st.pyplot(monthly_sales_profit(m, "Monthly Trend / Tendência Mensal"))
    st.dataframe(m, use_container_width=True)

with tab3:
    st.pyplot(top_bar(df_filtered, "Product Name", "Sales", "Top Products (Sales) / Top Produtos", top_n=10))
    st.dataframe(top_products(df_filtered, 15), use_container_width=True)

with tab4:
    st.pyplot(chart_profit_by_subcat(df_filtered, "Profit by Sub-Category / Lucro por Sub-Categoria", top_n=15))
    prof_table = profit_by_subcategory(df_filtered)
    st.dataframe(prof_table, use_container_width=True)

    st.download_button(
        T["download_agg"],
        data=prof_table.to_csv(index=False).encode("utf-8"),
        file_name="report_subcategory.csv",
        mime="text/csv"
    )

with tab5:
    st.dataframe(df_filtered, use_container_width=True)
    st.download_button(
        T["download"],
        data=df_filtered.to_csv(index=False).encode("utf-8"),
        file_name="filtered_data.csv",
        mime="text/csv"
    )
