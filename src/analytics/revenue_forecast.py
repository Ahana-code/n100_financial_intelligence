import os
import sqlite3
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression

warnings.filterwarnings("ignore")

DB_PATH = "db/nifty100.db"

OUTPUT_DIR = "output"
REPORT_DIR = "reports"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

print("Loading database...")

conn = sqlite3.connect(DB_PATH)

profit = pd.read_sql("""
SELECT
    company_id,
    year,
    sales
FROM profitandloss
""", conn)

companies = pd.read_sql("""
SELECT
    id,
    company_name
FROM companies
""", conn)

conn.close()

print("Database loaded.")

# ----------------------------------
# Remove TTM
# ----------------------------------

profit = profit[profit["year"] != "TTM"]

profit["year_num"] = (
    profit["year"]
    .str.extract(r"(\d{4})")
    .astype(float)
)

forecast_rows = []

print("Running Revenue Forecast...")

for company, grp in profit.groupby("company_id"):

    grp = (
        grp.groupby("year_num", as_index=False)
        .agg({"sales": "sum"})
        .sort_values("year_num")
    )

    if len(grp) < 3:
        continue

    X = grp[["year_num"]]
    y = grp["sales"]

    model = LinearRegression()
    model.fit(X, y)

    future_years = np.array([
        grp["year_num"].max() + 1,
        grp["year_num"].max() + 2,
        grp["year_num"].max() + 3
    ]).reshape(-1, 1)

    predictions = model.predict(future_years)

    forecast_rows.append({
        "company_id": company,
        "forecast_1yr": round(predictions[0], 2),
        "forecast_2yr": round(predictions[1], 2),
        "forecast_3yr": round(predictions[2], 2),
    })

# ----------------------------------
# Forecast DataFrame
# ----------------------------------

forecast_df = pd.DataFrame(forecast_rows)

forecast_df = forecast_df.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)

forecast_df = forecast_df[
    [
        "company_id",
        "company_name",
        "forecast_1yr",
        "forecast_2yr",
        "forecast_3yr",
    ]
].sort_values(
    "forecast_3yr",
    ascending=False,
)

# ----------------------------------
# Save Excel
# ----------------------------------

output_file = os.path.join(
    OUTPUT_DIR,
    "revenue_forecast.xlsx",
)

forecast_df.to_excel(
    output_file,
    index=False,
)

# ----------------------------------
# Top 15 Forecast Chart
# ----------------------------------

plt.figure(figsize=(12,6))

top15 = forecast_df.head(15)

plt.bar(
    top15["company_name"],
    top15["forecast_3yr"],
)

plt.xticks(rotation=90)

plt.title("Top 15 Revenue Forecast (3 Years)")

plt.tight_layout()

chart_path = os.path.join(
    REPORT_DIR,
    "revenue_forecast.png",
)

plt.savefig(chart_path)

plt.close()

print("\nRevenue Forecast Generated Successfully!\n")

print(forecast_df.head(20))

print(f"\nExcel saved to: {output_file}")
print(f"Chart saved to: {chart_path}")