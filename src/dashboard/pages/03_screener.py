import streamlit as st
import pandas as pd

from src.dashboard.utils.db import (
    get_companies,
    get_ratios
)

st.title("📊 Stock Screener")

companies = get_companies()

# Load AI outputs
health = pd.read_excel("output/company_health_score.xlsx")
recommendation = pd.read_excel("output/investment_recommendation.xlsx")

records = []

for ticker in companies["id"]:

    ratios = get_ratios(ticker)

    if ratios.empty:
        continue

    latest = ratios.iloc[-1]

    company = companies[companies["id"] == ticker].iloc[0]

    # Health Score
    health_row = health[health["id"] == ticker]

    if not health_row.empty:
        health_score = health_row.iloc[0]["Health_Score"]
    else:
        health_score = None

    # Recommendation
    rec_row = recommendation[recommendation["id"] == ticker]

    if not rec_row.empty:
        rec = rec_row.iloc[0]["Recommendation"]
    else:
        rec = "N/A"

    records.append({
        "Company": company["company_name"],
        "Ticker": ticker,
        "ROE (%)": latest["return_on_equity_pct"],
        "Debt/Equity": latest["debt_to_equity"],
        "Net Profit Margin (%)": latest["net_profit_margin_pct"],
        "Interest Coverage": latest["interest_coverage"],
        "Health Score": health_score,
        "Recommendation": rec
    })

screen = pd.DataFrame(records)

st.sidebar.header("Filters")

min_roe = st.sidebar.slider(
    "Minimum ROE",
    0.0,
    100.0,
    10.0
)

max_de = st.sidebar.slider(
    "Maximum Debt/Equity",
    0.0,
    10.0,
    2.0
)

filtered = screen[
    (screen["ROE (%)"] >= min_roe) &
    (screen["Debt/Equity"] <= max_de)
]

st.metric("Companies Found", len(filtered))

st.dataframe(
    filtered,
    use_container_width=True
)

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download CSV",
    csv,
    "stock_screener.csv",
    "text/csv"
)