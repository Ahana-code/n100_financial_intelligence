import streamlit as st
import plotly.express as px

from src.dashboard.utils.db import (
    get_companies,
    get_ratios,
    get_cf
)

st.title("💰 Capital Allocation")

companies = get_companies()

company_map = dict(
    zip(companies["company_name"], companies["id"])
)

selected_company = st.selectbox(
    "Select Company",
    sorted(company_map.keys())
)

ticker = company_map[selected_company]

ratios = get_ratios(ticker)
cf = get_cf(ticker)

# -----------------------------
# Capital Allocation KPIs
# -----------------------------

if not ratios.empty:

    latest = ratios.iloc[-1]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Free Cash Flow",
        f"{latest['free_cash_flow_cr']:.2f} Cr"
        if latest["free_cash_flow_cr"] is not None
        else "N/A"
    )

    c2.metric(
        "Total Debt",
        f"{latest['total_debt_cr']:.2f} Cr"
        if latest["total_debt_cr"] is not None
        else "N/A"
    )

    c3.metric(
        "Dividend Payout",
        f"{latest['dividend_payout_ratio_pct']:.2f}%"
        if latest["dividend_payout_ratio_pct"] is not None
        else "N/A"
    )

# -----------------------------
# Cash Flow Trend
# -----------------------------

if not cf.empty:

    chart = cf.copy()

    chart = chart.sort_values("year")

    fig = px.line(
    chart,
    x="year",
    y="operating_activity",
    markers=True,
    title="Operating Cash Flow Trend"
)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Cash Flow Statement")

    st.dataframe(
        chart,
        use_container_width=True
    )

else:

    st.info("Cash Flow data not available.")