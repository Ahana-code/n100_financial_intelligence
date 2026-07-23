import streamlit as st
import plotly.express as px
import pandas as pd

from src.dashboard.utils.db import (
    get_companies,
    get_pl,
    get_ratios,
    get_pros_cons
)

st.title("🏢 Company Profile")

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

company = companies[
    companies["id"] == ticker
].iloc[0]

st.header(company["company_name"])
# ==========================
# Load Sprint 6 Outputs
# ==========================

health = pd.read_excel("output/company_health_score.xlsx")

forecast = pd.read_excel("output/revenue_forecast.xlsx")

recommendation = pd.read_excel("output/investment_recommendation.xlsx")

clusters = pd.read_excel("output/company_clusters.xlsx")

col1, col2 = st.columns(2)

with col1:
    st.write("**Company ID:**", company["id"])
    st.write("**Face Value:**", company["face_value"])
    st.write("**Book Value:**", company["book_value"])
    st.write("**ROCE:**", f"{company['roce_percentage']}%")
    st.write("**ROE:**", f"{company['roe_percentage']}%")

with col2:
    st.write("**Website:**", company["website"])
    st.write("**NSE Profile:**", company["nse_profile"])
    st.write("**BSE Profile:**", company["bse_profile"])

# ==========================
# AI Analytics Summary
# ==========================

st.subheader("AI Analytics Summary")

health_row = health[health["id"] == ticker]

forecast_row = forecast[forecast["company_id"] == ticker]

recommendation_row = recommendation[
    recommendation["id"] == ticker
]

cluster_row = clusters[
    clusters["id"] == ticker
]

c1, c2, c3 = st.columns(3)

with c1:

    if not health_row.empty:

        st.metric(
            "Health Score",
            round(float(health_row.iloc[0]["Health_Score"]), 2)
        )

        st.write(
            "**Investment Grade:**",
            health_row.iloc[0]["Investment_Grade"]
        )

with c2:

    if not recommendation_row.empty:

        st.metric(
            "Recommendation",
            recommendation_row.iloc[0]["Recommendation"]
        )

        st.write(
            recommendation_row.iloc[0]["Reason"]
        )

with c3:

    if not cluster_row.empty:

        st.metric(
            "Cluster",
            cluster_row.iloc[0]["cluster_name"]
        )

st.subheader("About Company")

st.write(company["about_company"])

ratios = get_ratios(ticker)

if not ratios.empty:

    latest = ratios.iloc[-1]

    st.subheader("Latest Financial Ratios")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "ROE",
        f"{latest['return_on_equity_pct']:.2f}%"
    )

    c2.metric(
        "Debt / Equity",
        f"{latest['debt_to_equity']:.2f}"
    )

    c3.metric(
        "Net Profit Margin",
        f"{latest['net_profit_margin_pct']:.2f}%"
    )

pl = get_pl(ticker)

if not pl.empty:

   if not pl.empty:

    pl = pl.sort_values("year")

    st.subheader("Revenue & Net Profit (10 Years)")

    fig = px.bar(
        pl,
        x="year",
        y=["sales", "net_profit"],
        barmode="group",
        title="Revenue vs Net Profit"
    )

    st.plotly_chart(fig, use_container_width=True)

if not ratios.empty:

    ratios = ratios.sort_values("year")

    st.subheader("ROE & ROCE Trend")

    roce_values = []

    for yr in ratios["year"]:
        match = pl[pl["year"] == yr]

        if not match.empty:
            roce_values.append(company["roce_percentage"])
        else:
            roce_values.append(None)

    trend = ratios.copy()
    trend["ROCE"] = roce_values

    fig2 = px.line(
        trend,
        x="year",
        y=["return_on_equity_pct", "ROCE"],
        markers=True,
        title="ROE & ROCE Over Time"
    )

    fig2.update_layout(
        xaxis_title="Year",
        yaxis_title="Percentage"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # ==========================
# Revenue Forecast
# ==========================

if not forecast_row.empty:

    st.subheader("3-Year Revenue Forecast")

    forecast_df = pd.DataFrame({

        "Year": [
            "1 Year",
            "2 Years",
            "3 Years"
        ],

        "Forecast Revenue": [

            forecast_row.iloc[0]["forecast_1yr"],
            forecast_row.iloc[0]["forecast_2yr"],
            forecast_row.iloc[0]["forecast_3yr"]

        ]

    })

    fig_forecast = px.bar(

        forecast_df,

        x="Year",

        y="Forecast Revenue",

        text_auto=".2s",

        title="Predicted Revenue Growth"

    )

    st.plotly_chart(
        fig_forecast,
        use_container_width=True
    )

# ===========================
# Pros & Cons
# ===========================

pros_cons = get_pros_cons(ticker)

st.subheader("Pros & Cons")

if pros_cons.empty:

    st.info("No Pros & Cons data available for this company.")

else:

    col1, col2 = st.columns(2)

    with col1:

        st.success("Pros")

        pros_list = str(pros_cons.iloc[0]["pros"]).split(".")

        for item in pros_list:

            item = item.strip()

            if item:
                st.write(f"✅ {item}")

    with col2:

        st.error("Cons")

        cons_list = str(pros_cons.iloc[0]["cons"]).split(".")

        for item in cons_list:

            item = item.strip()

            if item:
                st.write(f"❌ {item}")