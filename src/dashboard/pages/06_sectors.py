import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

DB_PATH = "db/nifty100.db"

st.title("🏭 Sector Analysis")

conn = sqlite3.connect(DB_PATH)

sectors = pd.read_sql(
    "SELECT * FROM sectors",
    conn
)

companies = pd.read_sql(
    "SELECT id, company_name FROM companies",
    conn
)

conn.close()

# Merge company names
sectors = sectors.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)

sector_list = sorted(
    sectors["broad_sector"].dropna().unique()
)

selected_sector = st.selectbox(
    "Select Sector",
    sector_list
)

filtered = sectors[
    sectors["broad_sector"] == selected_sector
]

st.metric(
    "Companies",
    len(filtered)
)

fig = px.pie(
    filtered,
    names="sub_sector",
    title=f"{selected_sector} - Sub Sector Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

fig2 = px.bar(
    filtered.sort_values(
        "index_weight_pct",
        ascending=False
    ),
    x="company_name",
    y="index_weight_pct",
    title="Index Weight by Company"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.subheader("Sector Companies")

st.dataframe(
    filtered[
        [
            "company_name",
            "company_id",
            "sub_sector",
            "index_weight_pct",
            "market_cap_category"
        ]
    ],
    use_container_width=True
)