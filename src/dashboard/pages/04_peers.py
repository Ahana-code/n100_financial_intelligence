import streamlit as st
import pandas as pd
import sqlite3

from src.dashboard.utils.db import (
    get_companies,
    get_ratios
)

DB_PATH = "db/nifty100.db"

st.title("👥 Peer Comparison")

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

conn = sqlite3.connect(DB_PATH)

peer_group = pd.read_sql(
    """
    SELECT peer_group_name
    FROM peer_groups
    WHERE company_id=?
    """,
    conn,
    params=(ticker,)
)

if peer_group.empty:

    st.warning("No peer group found.")

else:

    group = peer_group.iloc[0]["peer_group_name"]

    st.subheader(f"Peer Group : {group}")

    peers = pd.read_sql(
        """
        SELECT *
        FROM peer_groups
        WHERE peer_group_name=?
        """,
        conn,
        params=(group,)
    )

    rows = []

    for _, peer in peers.iterrows():

        peer_id = peer["company_id"]

        company = companies[
            companies["id"] == peer_id
        ]

        if company.empty:
            continue

        ratios = get_ratios(peer_id)

        if ratios.empty:
            continue

        latest = ratios.iloc[-1]

        rows.append({

            "Company":
            company.iloc[0]["company_name"],

            "Ticker":
            peer_id,

            "Benchmark":
            "Yes" if peer["is_benchmark"] == 1 else "No",

            "ROE (%)":
            latest["return_on_equity_pct"],

            "Debt/Equity":
            latest["debt_to_equity"],

            "Net Profit Margin (%)":
            latest["net_profit_margin_pct"]

        })

    conn.close()

    peer_df = pd.DataFrame(rows)

    st.dataframe(
        peer_df,
        use_container_width=True
    )