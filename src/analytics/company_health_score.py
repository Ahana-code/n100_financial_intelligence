import os
import sqlite3
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

DB_PATH = "db/nifty100.db"

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Loading database...")

conn = sqlite3.connect(DB_PATH)

companies = pd.read_sql("""
SELECT
    id,
    company_name,
    book_value,
    roe_percentage
FROM companies
""", conn)

ratios = pd.read_sql("""
SELECT
    company_id,
    year,
    return_on_equity_pct,
    debt_to_equity,
    interest_coverage,
    operating_profit_margin_pct,
    free_cash_flow_cr
FROM financial_ratios
""", conn)


cashflow = pd.read_sql("""
SELECT
    company_id,
    year,
    operating_activity
FROM cashflow
""", conn)

conn.close()

print("Database loaded.")

# ----------------------------------
# Remove TTM
# ----------------------------------

ratios = ratios[ratios["year"] != "TTM"]

ratios["year_num"] = (
    ratios["year"]
    .str.extract(r"(\d{4})")
    .astype(float)
)

latest_ratios = (
    ratios
    .sort_values("year_num")
    .groupby("company_id")
    .tail(1)
)

health_df = companies.merge(
    latest_ratios,
    left_on="id",
    right_on="company_id",
    how="left"
).drop(columns=["company_id"])


# ----------------------------------
# Health Score
# ----------------------------------

health_df["Health_Score"] = 0


# ROE (30 marks)

health_df["Health_Score"] += np.where(
    health_df["return_on_equity_pct"] >= 20,
    30,
    np.where(
        health_df["return_on_equity_pct"] >= 15,
        20,
        np.where(
            health_df["return_on_equity_pct"] >= 10,
            10,
            0,
        ),
    ),
)


# Debt (20 marks)

health_df["Health_Score"] += np.where(
    health_df["debt_to_equity"] <= 0.5,
    20,
    np.where(
        health_df["debt_to_equity"] <= 1,
        10,
        0,
    ),
)


# Interest Coverage (20 marks)

health_df["Health_Score"] += np.where(
    health_df["interest_coverage"] >= 5,
    20,
    np.where(
        health_df["interest_coverage"] >= 2,
        10,
        0,
    ),
)


# Operating Margin (15 marks)

health_df["Health_Score"] += np.where(
    health_df["operating_profit_margin_pct"] >= 20,
    15,
    np.where(
        health_df["operating_profit_margin_pct"] >= 10,
        8,
        0,
    ),
)


# Free Cash Flow (15 marks)

health_df["Health_Score"] += np.where(
    health_df["free_cash_flow_cr"] > 0,
    15,
    0,
)

# ----------------------------------
# Investment Grade
# ----------------------------------

health_df["Investment_Grade"] = np.where(
    health_df["Health_Score"] >= 75,
    "Strong",
    np.where(
        health_df["Health_Score"] >= 50,
        "Moderate",
        "Weak",
    ),
)

# ----------------------------------
# Keep useful columns
# ----------------------------------

final_df = health_df[
    [
        "id",
        "company_name",
        "return_on_equity_pct",
        "debt_to_equity",
        "interest_coverage",
        "operating_profit_margin_pct",
        "free_cash_flow_cr",
        "Health_Score",
        "Investment_Grade",
    ]
].sort_values(
    "Health_Score",
    ascending=False,
)

# ----------------------------------
# Export
# ----------------------------------

output_file = os.path.join(
    OUTPUT_DIR,
    "company_health_score.xlsx",
)

final_df.to_excel(
    output_file,
    index=False,
)

print("\nCompany Health Scores Generated Successfully!\n")

print(final_df.head(20))

print(f"\nExcel saved to: {output_file}")