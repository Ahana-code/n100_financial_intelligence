import sqlite3
import pandas as pd

DB = "db/nifty100.db"

conn = sqlite3.connect(DB)

# Read Excel correctly
df = pd.read_excel("data/raw/peer_groups.xlsx")

print("Original Columns:")
print(df.columns)

# Rename columns
df.columns = [
    "id",
    "peer_group_name",
    "company_id",
    "is_benchmark"
]

# Replace table
df.to_sql(
    "peer_groups",
    conn,
    if_exists="replace",
    index=False
)

print("\npeer_groups table recreated successfully!")
print(df.head())

conn.close()