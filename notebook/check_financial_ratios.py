import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

print("Financial Ratios Row Count")
print(
    pd.read_sql(
        "SELECT COUNT(*) AS total FROM financial_ratios",
        conn
    )
)

conn.close()