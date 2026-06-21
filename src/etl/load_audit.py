import sqlite3
import pandas as pd


conn = sqlite3.connect("db/nifty100.db")


tables = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "analysis",
    "financial_ratios",
    "stock_prices",
    "documents",
    "prosandcons",
    "sectors",
    "peer_groups",
    "market_cap"
]


audit = []


for table in tables:

    count = pd.read_sql(
        f"SELECT COUNT(*) as rows FROM {table}",
        conn
    )

    audit.append(
        {
            "table": table,
            "row_count": count["rows"][0]
        }
    )


df = pd.DataFrame(audit)


df.to_csv(
    "output/load_audit.csv",
    index=False
)


print(df)


conn.close()