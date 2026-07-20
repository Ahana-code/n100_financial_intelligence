import streamlit as st
import pandas as pd
from src.dashboard.utils.db import (
    get_companies,
    get_ratios,
    get_pl,
    get_bs,
    get_cf
)

st.title("📄 Company Report")

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

st.subheader("Company Information")

info = pd.DataFrame({
    "Field": [
        "Company ID",
        "Face Value",
        "Book Value",
        "ROCE",
        "ROE"
    ],
    "Value": [
        company["id"],
        company["face_value"],
        company["book_value"],
        f"{company['roce_percentage']}%",
        f"{company['roe_percentage']}%"
    ]
})

st.table(info)

ratios = get_ratios(ticker)
pl = get_pl(ticker)
bs = get_bs(ticker)
cf = get_cf(ticker)

st.divider()

st.subheader("Financial Ratios")

if not ratios.empty:
    st.dataframe(
        ratios.sort_values("year", ascending=False),
        use_container_width=True
    )
else:
    st.info("No Financial Ratios available.")

st.divider()

st.subheader("Profit & Loss")

if not pl.empty:
    st.dataframe(
        pl.sort_values("year", ascending=False),
        use_container_width=True
    )
else:
    st.info("No Profit & Loss data available.")

st.divider()

st.subheader("Balance Sheet")

if not bs.empty:
    st.dataframe(
        bs.sort_values("year", ascending=False),
        use_container_width=True
    )
else:
    st.info("No Balance Sheet data available.")

st.divider()

st.subheader("Cash Flow")

if not cf.empty:
    st.dataframe(
        cf.sort_values("year", ascending=False),
        use_container_width=True
    )
else:
    st.info("No Cash Flow data available.")

csv = ratios.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Financial Ratios CSV",
    data=csv,
    file_name=f"{ticker}_financial_ratios.csv",
    mime="text/csv"
)