import sqlite3
import pandas as pd
import numpy as np

print("Loading database...")

conn = sqlite3.connect("db/nifty100.db")

companies = pd.read_sql("""
SELECT
    id,
    company_name
FROM companies
""", conn)

profit = pd.read_sql("""
SELECT
    company_id,
    year,
    sales
FROM profitandloss
ORDER BY company_id, year
""", conn)

conn.close()

print("Database loaded.")
print("Running Backtest Validation...")

# -----------------------------
# Keep latest 4 years
# -----------------------------
profit["year"] = profit["year"].astype(str)

profit = profit.sort_values(
    ["company_id", "year"]
)

results = []

for company_id, group in profit.groupby("company_id"):

    group = group.tail(4)

    if len(group) < 4:
        continue

    revenues = group["sales"].values

    actual_growth = (
        (revenues[-1] - revenues[0])
        / revenues[0]
    ) * 100

    predicted_growth = np.mean(
        np.diff(revenues) / revenues[:-1]
    ) * 100 * 3

    error = abs(
        predicted_growth - actual_growth
    )

    if error <= 10:
        verdict = "Excellent"

    elif error <= 20:
        verdict = "Good"

    else:
        verdict = "Poor"

    results.append({

        "company_id": company_id,

        "actual_growth_%": round(actual_growth, 2),

        "predicted_growth_%": round(predicted_growth, 2),

        "absolute_error_%": round(error, 2),

        "validation": verdict

    })

backtest = pd.DataFrame(results)

backtest = backtest.merge(

    companies,

    left_on="company_id",

    right_on="id",

    how="left"

)

backtest = backtest[[
    "company_id",
    "company_name",
    "actual_growth_%",
    "predicted_growth_%",
    "absolute_error_%",
    "validation"
]]

backtest = backtest.sort_values(
    "absolute_error_%"
)

backtest.to_excel(
    "output/backtest_validation.xlsx",
    index=False
)

summary = backtest["validation"].value_counts()

print("\nBacktest Validation Completed!\n")

print(backtest.head(20))

print("\nValidation Summary:\n")
print(summary)

print("\nExcel saved to: output/backtest_validation.xlsx")