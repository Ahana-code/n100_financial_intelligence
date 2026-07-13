import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

os.makedirs("reports/radar_charts", exist_ok=True)

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql(
    "SELECT * FROM financial_ratios LIMIT 20",
    conn
)

conn.close()

metrics = [
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "asset_turnover",
    "debt_to_equity",
    "interest_coverage"
]

for _, row in df.iterrows():

    values = []

    for m in metrics:
        val = row[m]

        if pd.isna(val):
            val = 0

        values.append(float(val))

    values += values[:1]

    angles = np.linspace(
        0,
        2*np.pi,
        len(metrics),
        endpoint=False
    ).tolist()

    angles += angles[:1]

    fig = plt.figure(figsize=(5,5))

    ax = plt.subplot(111, polar=True)

    ax.plot(angles, values)

    ax.fill(angles, values, alpha=0.25)

    ax.set_xticks(angles[:-1])

    ax.set_xticklabels(metrics, fontsize=8)

    plt.title(row["company_id"])

    plt.savefig(
        f"reports/radar_charts/{row['company_id']}.png"
    )

    plt.close()

print("Radar charts generated successfully!")