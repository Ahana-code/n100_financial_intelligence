import os
import sqlite3
import pandas as pd

os.makedirs("output", exist_ok=True)

conn = sqlite3.connect("db/nifty100.db")

peer = pd.read_sql(
    "SELECT * FROM peer_percentiles",
    conn
)

conn.close()

# Convert long format to wide format
peer_report = peer.pivot_table(
    index=["company_id", "peer_group_name", "year"],
    columns="metric",
    values="percentile_rank"
).reset_index()

writer = pd.ExcelWriter(
    "output/peer_comparison.xlsx",
    engine="openpyxl"
)

groups = peer_report["peer_group_name"].dropna().unique()

for group in groups:

    temp = peer_report[
        peer_report["peer_group_name"] == group
    ]

    temp.to_excel(
        writer,
        sheet_name=str(group)[:31],
        index=False
    )

writer.close()

print("\npeer_comparison.xlsx created successfully!")
print("Peer Groups:", len(groups))