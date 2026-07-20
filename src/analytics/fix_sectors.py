import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql("SELECT * FROM sectors", conn)

print("Current columns:")
print(df.columns)

df.columns = [
    "id",
    "company_id",
    "sector",
    "sub_sector",
    "weight",
    "market_cap_category"
]

df.to_sql(
    "sectors",
    conn,
    if_exists="replace",
    index=False
)

print("\nFixed Successfully!")

print(pd.read_sql("SELECT * FROM sectors LIMIT 5", conn))

conn.close()