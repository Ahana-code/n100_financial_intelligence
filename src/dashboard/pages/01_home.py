import streamlit as st
import pandas as pd
import plotly.express as px

from src.dashboard.utils.db import (
    get_companies,
    get_ratios,
    get_years,
    get_sectors
)

st.title("🏠 Home Dashboard")

# ---------------- Sidebar ---------------- #

years = get_years()

selected_year = st.sidebar.selectbox(
    "Select Year",
    sorted(years)
)

# ---------------- Load Data ---------------- #

companies = get_companies()
sectors = get_sectors()

all_ratios = []

for ticker in companies["id"]:
    df = get_ratios(ticker, selected_year)

    if not df.empty:
        all_ratios.append(df)

if not all_ratios:
    st.warning("No data available.")
    st.stop()

ratios = pd.concat(all_ratios, ignore_index=True)

# ---------------- KPI Cards ---------------- #

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Companies",
    companies.shape[0]
)

col2.metric(
    "Average ROE",
    f"{ratios['return_on_equity_pct'].mean():.2f}%"
)

col3.metric(
    "Median D/E",
    f"{ratios['debt_to_equity'].median():.2f}"
)

debt_free = ratios[
    ratios["debt_to_equity"] == 0
].shape[0]

col4.metric(
    "Debt-Free Companies",
    debt_free
)

col5, col6 = st.columns(2)

col5.metric(
    "Average Net Profit Margin",
    f"{ratios['net_profit_margin_pct'].mean():.2f}%"
)

col6.metric(
    "Average Interest Coverage",
    f"{ratios['interest_coverage'].mean():.2f}"
)

st.divider()

# ---------------- Sector Donut ---------------- #

st.subheader("Sector Breakdown")

sector_counts = (
    sectors.groupby("broad_sector")
    .size()
    .reset_index(name="Company Count")
)

fig = px.pie(
    sector_counts,
    names="broad_sector",
    values="Company Count",
    hole=0.55
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------- Top Companies ---------------- #

st.subheader("Top Companies by ROE")

latest = (
    ratios.sort_values("return_on_equity_pct", ascending=False)
    .head(5)
)

top5 = latest.merge(
    companies,
    left_on="company_id",
    right_on="id"
)

st.dataframe(
    top5[
        [
            "company_name",
            "return_on_equity_pct",
            "debt_to_equity",
            "interest_coverage"
        ]
    ],
    use_container_width=True
)