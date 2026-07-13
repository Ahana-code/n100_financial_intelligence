import sqlite3
import pandas as pd

DB = "db/nifty100.db"

conn = sqlite3.connect(DB)

# Load tables
ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)
peers = pd.read_sql("SELECT * FROM peer_groups", conn)

# Merge
df = ratios.merge(peers, on="company_id", how="left")
df["peer_group_name"] = df["peer_group_name"].fillna("No peer group assigned")

# Metrics to rank
metrics = [
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "asset_turnover",
    "free_cash_flow_cr",
    "interest_coverage"
]

results = []

for metric in metrics:

    temp = df.copy()

    temp["percentile_rank"] = (
        temp.groupby("peer_group_name")[metric]
        .rank(pct=True)
    )

    temp["metric"] = metric
    temp["value"] = temp[metric]

    results.append(
        temp[
            [
                "company_id",
                "peer_group_name",
                "year",
                "metric",
                "value",
                "percentile_rank",
            ]
        ]
    )

peer_percentiles = pd.concat(results, ignore_index=True)

peer_percentiles.to_sql(
    "peer_percentiles",
    conn,
    if_exists="replace",
    index=False,
)

print(peer_percentiles.head())

print("\nRows:", len(peer_percentiles))

conn.close()