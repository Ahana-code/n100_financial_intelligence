import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("reports/portfolio", exist_ok=True)

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT
    company_name,
    roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10
"""

df = pd.read_sql(query, conn)
conn.close()

df.to_csv("reports/portfolio/top_portfolio.csv", index=False)

plt.figure(figsize=(10,6))
plt.bar(df["company_name"], df["roe_percentage"])
plt.xticks(rotation=45, ha="right")
plt.ylabel("ROE (%)")
plt.title("Top 10 Companies by ROE")
plt.tight_layout()
plt.savefig("reports/portfolio/top_portfolio.png")
plt.close()

print("Portfolio report generated.")