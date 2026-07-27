import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("reports/sector", exist_ok=True)

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT
    s.broad_sector,
    AVG(c.roe_percentage) AS avg_roe,
    COUNT(*) AS companies
FROM companies c
JOIN sectors s
ON c.id = s.company_id
GROUP BY s.broad_sector
ORDER BY avg_roe DESC
"""

df = pd.read_sql(query, conn)
conn.close()

df.to_csv("reports/sector/sector_summary.csv", index=False)

plt.figure(figsize=(10,6))
plt.bar(df["broad_sector"], df["avg_roe"])
plt.xticks(rotation=90)
plt.ylabel("Average ROE")
plt.title("Average ROE by Sector")
plt.tight_layout()
plt.savefig("reports/sector/sector_summary.png")
plt.close()

print("Sector report generated.")