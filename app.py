import streamlit as st

from src.data import load_data, apply_filters
from src.metrics import kpis, top_products, profit_by_subcategory, monthly_trend
from src.charts import bar_sales_by_category, pie_sales_by_region, line_monthly_sales_profit

st.set_page_config(page_title="Dashboard | Superstore", layout="wide")

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
        "year": "Ano",
        "region": "Região",
        "segment": "Segmento",
        "category": "Categoria",
        "subcategory": "Sub-Categoria",
        "sales": "Vendas",
        "profit": "Lucro",
        "orders": "Pedidos",
        "customers": "Clientes",
        "ticket": "Ticket Médio",
        "margin": "Margem",
        "tab_overview": "Visão Geral",
        "tab_trends": "Tendências",
        "tab_products": "Produtos",
        "tab_data": "Dados",
        "download": "Baixar CSV"
    },
    "English": {
        "title": "📊 Advanced Sales Dashboard",
        "subtitle": "Portfolio project using Python and Streamlit",
        "filters": "Filters",
        "year": "Year",
        "region": "Region",
        "segment": "Segment",
        "category": "Category",
        "subcategory": "Sub-Category",
        "sales": "Sales",
        "profit": "Profit",
        "orders": "Orders",
        "customers": "Customers",
        "ticket": "Average Ticket",
        "margin": "Margin",
        "tab_overview": "Overview",
        "tab_trends": "Trends",
        "tab_products": "Products",
        "tab_data": "Data",
        "download": "Download CSV"
    }
}

T = TEXT[lang]

st.title(T["title"])
st.caption(T["subtitle"])

st.sidebar.header(T["filters"])

years = sorted(df["Year"].unique())
regions = sorted(df["Region"].unique())
segments = sorted(df["Segment"].unique())
categories = sorted(df["Category"].unique())

year_sel = st.sidebar.multiselect(T["year"], years, default=years)
region_sel = st.sidebar.multiselect(T["region"], regions, default=regions)
segment_sel = st.sidebar.multiselect(T["segment"], segments, default=segments)
category_sel = st.sidebar.multiselect(T["category"], categories, default=categories)

df_filtered = apply_filters(
    df,
    years=year_sel,
    regions=region_sel,
    segments=segment_sel,
    categories=category_sel
)

k = kpis(df_filtered)

c1, c2, c3 = st.columns(3)
c1.metric(T["sales"], f"R$ {k['total_sales']:,.2f}")
c2.metric(T["profit"], f"R$ {k['total_profit']:,.2f}")
c3.metric(T["orders"], f"{k['orders']}")

tab1, tab2, tab3, tab4 = st.tabs([
    T["tab_overview"],
    T["tab_trends"],
    T["tab_products"],
    T["tab_data"]
])

with tab1:
    st.pyplot(bar_sales_by_category(df_filtered))
    st.pyplot(pie_sales_by_region(df_filtered))

with tab2:
    st.pyplot(line_monthly_sales_profit(monthly_trend(df_filtered)))

with tab3:
    st.dataframe(top_products(df_filtered, 10), use_container_width=True)

    # (opcional) tabela de lucro por subcategoria
    st.dataframe(profit_by_subcategory(df_filtered), use_container_width=True)

with tab4:
    st.dataframe(df_filtered.head(50), use_container_width=True)
    st.download_button(
        T["download"],
        data=df_filtered.to_csv(index=False).encode("utf-8"),
        file_name="data.csv",
        mime="text/csv"
    )
