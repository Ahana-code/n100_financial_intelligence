import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

companies = pd.read_sql(
    """
    SELECT
        id,
        roce_percentage,
        roe_percentage
    FROM companies
    """,
    conn
)

ratios = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        return_on_equity_pct
    FROM financial_ratios
    """,
    conn
)

merged = ratios.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)

logs = []

for _, row in merged.iterrows():

    # ROE comparison
    if (
        pd.notna(row["return_on_equity_pct"])
        and pd.notna(row["roe_percentage"])
    ):

        diff = abs(
            row["return_on_equity_pct"]
            - row["roe_percentage"]
        )

        if diff > 5:

            logs.append(
                {
                    "company_id": row["company_id"],
                    "year": row["year"],
                    "metric": "ROE",
                    "computed": row["return_on_equity_pct"],
                    "source": row["roe_percentage"],
                    "difference": round(diff,2),
                    "category": "Version Difference"
                }
            )

log_df = pd.DataFrame(logs)

log_df.to_csv(
    "output/ratio_edge_cases.log",
    index=False
)

print("Anomalies Found:", len(log_df))
print(log_df.head())

conn.close()