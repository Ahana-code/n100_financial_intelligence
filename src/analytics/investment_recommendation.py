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

health = pd.read_excel("output/company_health_score.xlsx")

forecast = pd.read_excel("output/revenue_forecast.xlsx")

clusters = pd.read_excel("output/company_clusters.xlsx")

conn.close()

print("Database loaded.")
print("Generating investment recommendations...")

# Rename company_id -> id so every dataframe uses the same key
forecast = forecast.rename(columns={"company_id": "id"})

df = (
    companies
    .merge(
        health,
        on=["id", "company_name"],
        how="left"
    )
    .merge(
        forecast,
        on=["id", "company_name"],
        how="left"
    )
    .merge(
        clusters[["id", "cluster_name"]],
        on="id",
        how="left"
    )
)

conditions = [

    (
        (df["Health_Score"] >= 80)
        &
        (df["forecast_3yr"] > df["forecast_1yr"])
    ),

    (
        df["Health_Score"] >= 60
    ),

    (
        df["Health_Score"] < 60
    )

]

choices = [
    "Strong Buy",
    "Hold",
    "Avoid"
]

df["Recommendation"] = np.select(
    conditions,
    choices,
    default="Watchlist"
)

df["Reason"] = np.select(

    [
        df["Recommendation"] == "Strong Buy",
        df["Recommendation"] == "Hold",
        df["Recommendation"] == "Avoid"
    ],

    [
        "High health score with positive revenue growth",
        "Stable financials",
        "Weak financial health"
    ],

    default="Needs monitoring"

)

final = df[
    [
        "id",
        "company_name",
        "Health_Score",
        "Investment_Grade",
        "cluster_name",
        "forecast_1yr",
        "forecast_2yr",
        "forecast_3yr",
        "Recommendation",
        "Reason"
    ]
]

final = final.sort_values(
    by=["Health_Score", "forecast_3yr"],
    ascending=False
)

final.to_excel(
    "output/investment_recommendation.xlsx",
    index=False
)

print("\nInvestment Recommendation Generated Successfully!\n")

print(final.head(20))

print("\nExcel saved to: output/investment_recommendation.xlsx")