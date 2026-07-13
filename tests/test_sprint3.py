import sqlite3
import pandas as pd
import os

DB = "db/nifty100.db"

conn = sqlite3.connect(DB)

# -----------------------------
# Load Tables
# -----------------------------
tables = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table'",
    conn
)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

peer = pd.read_sql(
    "SELECT * FROM peer_percentiles",
    conn
)

# -----------------------------
# TEST 1
# financial_ratios exists
# -----------------------------
assert "financial_ratios" in tables["name"].values

# -----------------------------
# TEST 2
# peer_percentiles exists
# -----------------------------
assert "peer_percentiles" in tables["name"].values

# -----------------------------
# TEST 3
# ratios table not empty
# -----------------------------
assert len(ratios) > 0

# -----------------------------
# TEST 4
# peer table not empty
# -----------------------------
assert len(peer) > 0

# -----------------------------
# TEST 5
# no duplicate company-year
# -----------------------------
assert (
    ratios.duplicated(
        subset=["company_id", "year"]
    ).sum()
    == 0
)

# -----------------------------
# TEST 6
# ROE available
# -----------------------------
assert ratios["return_on_equity_pct"].notna().sum() > 0

# -----------------------------
# TEST 7
# Debt/Equity available
# -----------------------------
assert ratios["debt_to_equity"].notna().sum() > 0

# -----------------------------
# TEST 8
# Free Cash Flow available
# -----------------------------
assert ratios["free_cash_flow_cr"].notna().sum() > 0

# -----------------------------
# TEST 9
# Percentiles valid ONLY where
# metric value exists
# -----------------------------
valid_peer = peer[
    (peer["peer_group_name"] != "No peer group assigned")
    &
    (peer["value"].notna())
]

assert (
    valid_peer["percentile_rank"]
    .between(0, 1)
    .all()
)

# -----------------------------
# TEST 10
# company_id exists
# -----------------------------
assert peer["company_id"].notna().all()

# -----------------------------
# TEST 11
# metric exists
# -----------------------------
assert peer["metric"].notna().all()

# -----------------------------
# TEST 12
# screener export exists
# -----------------------------
assert os.path.exists(
    "output/screener_output.xlsx"
)

# -----------------------------
# TEST 13
# peer export exists
# -----------------------------
assert os.path.exists(
    "output/peer_comparison.xlsx"
)

# -----------------------------
# TEST 14
# radar folder exists
# -----------------------------
assert os.path.exists(
    "reports/radar_charts"
)

conn.close()

print("\n===================================")
print(" ALL 14 SPRINT 3 TESTS PASSED ")
print("===================================")