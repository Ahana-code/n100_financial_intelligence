import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"
EXCEL_PATH = "data/raw/sectors.xlsx"

# Read original Excel
df = pd.read_excel(EXCEL_PATH)

print("\nOriginal Columns:")
print(df.columns.tolist())

conn = sqlite3.connect(DB_PATH)

# Replace the table with the original data
df.to_sql(
    "sectors",
    conn,
    if_exists="replace",
    index=False
)

print("\nsectors table recreated successfully!")

print(pd.read_sql(
    "SELECT * FROM sectors LIMIT 5",
    conn
))

print("\nTotal Rows:")
print(
    pd.read_sql(
        "SELECT COUNT(*) AS total FROM sectors",
        conn
    )
)

conn.close()