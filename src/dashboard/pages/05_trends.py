import streamlit as st
import plotly.express as px

from src.dashboard.utils.db import (
    get_companies,
    get_pl
)

st.title("📈 Financial Trends")

companies = get_companies()

company_map = dict(
    zip(
        companies["company_name"],
        companies["id"]
    )
)

selected_company = st.selectbox(
    "Select Company",
    sorted(company_map.keys())
)

ticker = company_map[selected_company]

pl = get_pl(ticker)

if pl.empty:

    st.warning("No Profit & Loss data available.")

else:

    years = pl["year"].astype(str)

    fig1 = px.line(
        pl,
        x=years,
        y="sales",
        markers=True,
        title="Sales Trend"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    fig2 = px.line(
        pl,
        x=years,
        y="net_profit",
        markers=True,
        title="Net Profit Trend"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    fig3 = px.line(
        pl,
        x=years,
        y="eps",
        markers=True,
        title="EPS Trend"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    st.subheader("Financial Data")

    st.dataframe(
        pl.sort_values("year"),
        use_container_width=True
    )