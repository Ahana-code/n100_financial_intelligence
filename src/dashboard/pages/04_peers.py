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

health = pd.read_excel("output/company_health_score.xlsx")
recommendation = pd.read_excel("output/investment_recommendation.xlsx")
clusters = pd.read_excel("output/company_clusters.xlsx")

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

        health_row = health[health["id"] == peer_id]

        if not health_row.empty:
            health_score = health_row.iloc[0]["Health_Score"]
            grade = health_row.iloc[0]["Investment_Grade"]
        else:
            health_score = None
            grade = "N/A"

        rec_row = recommendation[
            recommendation["id"] == peer_id
        ]

        if not rec_row.empty:
            rec = rec_row.iloc[0]["Recommendation"]
        else:
            rec = "N/A"

        cluster_row = clusters[
            clusters["id"] == peer_id
        ]

        if not cluster_row.empty:
            cluster = cluster_row.iloc[0]["cluster_name"]
        else:
            cluster = "N/A"

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
            latest["net_profit_margin_pct"],

            "Health Score":
            health_score,

            "Investment Grade":
            grade,

            "Recommendation":
            rec,

            "Cluster":
            cluster

        })

    conn.close()

    peer_df = pd.DataFrame(rows)

    st.dataframe(
        peer_df,
        use_container_width=True
    )