import os
import sqlite3
import warnings

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")
print("Starting clustering...")

DB_PATH = "db/nifty100.db"

OUTPUT_DIR = "output"
REPORT_DIR = "reports"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)


def calculate_cagr(first, last, years):
    """
    CAGR calculator
    """
    if years <= 0:
        return np.nan

    if first is None or last is None:
        return np.nan

    if first <= 0 or last <= 0:
        return np.nan

    return ((last / first) ** (1 / years) - 1) * 100


conn = sqlite3.connect(DB_PATH)

companies = pd.read_sql(
    """
    SELECT
        id,
        company_name,
        roe_percentage
    FROM companies
    """,
    conn,
)

sectors = pd.read_sql(
    """
    SELECT
        company_id,
        broad_sector
    FROM sectors
    """,
    conn,
)

ratios = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        return_on_equity_pct,
        debt_to_equity,
        operating_profit_margin_pct
    FROM financial_ratios
    """,
    conn,
)

profit = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        sales
    FROM profitandloss
    """,
    conn,
)

cash = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        operating_activity
    FROM cashflow
    """,
    conn,
)

conn.close()
print("Database loaded")


# -----------------------------
# Remove TTM
# -----------------------------

profit = profit[profit["year"] != "TTM"]
cash = cash[cash["year"] != "TTM"]
ratios = ratios[ratios["year"] != "TTM"]


# -----------------------------
# Extract numeric year
# -----------------------------

profit["year_num"] = (
    profit["year"]
    .str.extract(r"(\d{4})")
    .astype(float)
)

cash["year_num"] = (
    cash["year"]
    .str.extract(r"(\d{4})")
    .astype(float)
)

ratios["year_num"] = (
    ratios["year"]
    .str.extract(r"(\d{4})")
    .astype(float)
)


# -----------------------------
# Latest financial ratios
# -----------------------------

latest_ratio = (
    ratios
    .sort_values("year_num")
    .groupby("company_id")
    .tail(1)
)

latest_ratio = latest_ratio[
    [
        "company_id",
        "return_on_equity_pct",
        "debt_to_equity",
        "operating_profit_margin_pct"
    ]
]


# -----------------------------
# Revenue CAGR
# -----------------------------

revenue_rows = []

for company, grp in profit.groupby("company_id"):

    grp = (
        grp
        .groupby("year_num", as_index=False)
        .agg({"sales": "sum"})
        .sort_values("year_num")
    )

    if len(grp) < 6:
        continue

    first = grp.iloc[-6]
    last = grp.iloc[-1]

    cagr = calculate_cagr(
        first["sales"],
        last["sales"],
        last["year_num"] - first["year_num"],
    )

    revenue_rows.append(
        {
            "company_id": company,
            "revenue_cagr_5yr": cagr,
        }
    )

revenue_cagr = pd.DataFrame(revenue_rows)


# -----------------------------
# Cashflow CAGR
# -----------------------------

cash_rows = []

for company, grp in cash.groupby("company_id"):

    grp = (
        grp
        .groupby("year_num", as_index=False)
        .agg({"operating_activity": "sum"})
        .sort_values("year_num")
    )

    if len(grp) < 6:
        continue

    first = grp.iloc[-6]
    last = grp.iloc[-1]

    cagr = calculate_cagr(
        first["operating_activity"],
        last["operating_activity"],
        last["year_num"] - first["year_num"],
    )

    cash_rows.append(
        {
            "company_id": company,
            "fcf_cagr_5yr": cagr,
        }
    )

fcf_cagr = pd.DataFrame(cash_rows)

# -----------------------------
# Merge Everything
# -----------------------------

cluster_df = companies.merge(
    latest_ratio,
    left_on="id",
    right_on="company_id",
    how="left"
).drop(columns=["company_id"])


cluster_df = cluster_df.merge(
    revenue_cagr,
    left_on="id",
    right_on="company_id",
    how="left"
).drop(columns=["company_id"])


cluster_df = cluster_df.merge(
    fcf_cagr,
    left_on="id",
    right_on="company_id",
    how="left"
).drop(columns=["company_id"])


cluster_df = cluster_df.merge(
    sectors,
    left_on="id",
    right_on="company_id",
    how="left"
).drop(columns=["company_id"])


# -----------------------------
# Features for Clustering
# -----------------------------

features = [
    "roe_percentage",
    "debt_to_equity",
    "operating_profit_margin_pct",
    "revenue_cagr_5yr",
    "fcf_cagr_5yr"
]

cluster_df[features] = cluster_df[features].fillna(
    cluster_df[features].median(numeric_only=True)
)


# -----------------------------
# Scale Features
# -----------------------------

scaler = StandardScaler()

scaled_data = scaler.fit_transform(
    cluster_df[features]
)

# -----------------------------
# Elbow Plot
# -----------------------------
inertia = []

for k in range(2, 11):
    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )
    model.fit(scaled_data)
    inertia.append(model.inertia_)

plt.figure(figsize=(7,5))
plt.plot(range(2,11), inertia, marker="o")
plt.xlabel("Number of Clusters (k)")
plt.ylabel("Inertia")
plt.title("KMeans Elbow Plot")
plt.grid(True)

plt.tight_layout()
plt.savefig(
    os.path.join(
        REPORT_DIR,
        "elbow_plot.png"
    )
)
plt.close()

# -----------------------------
# KMeans
# -----------------------------

print("Running KMeans...")

kmeans = KMeans(
    n_clusters=5,
    random_state=42,
    n_init=10
)

cluster_df["cluster"] = kmeans.fit_predict(
    scaled_data
)
# Distance from centroid
cluster_df["distance_from_centroid"] = (
    kmeans.transform(scaled_data)
    .min(axis=1)
    .round(4)
)


# -----------------------------
# Cluster Names
# -----------------------------

cluster_names = {
    0: "Stable Compounders",
    1: "High Growth",
    2: "Value Picks",
    3: "Turnaround / Risk",
    4: "Defensive"
}

cluster_df["cluster_name"] = (
    cluster_df["cluster"]
    .map(cluster_names)
)


# -----------------------------
# Save Output
# -----------------------------

cluster_df.to_excel(
    os.path.join(
        OUTPUT_DIR,
        "company_clusters.xlsx"
    ),
    index=False
)
cluster_df[
    [
        "id",
        "cluster",
        "cluster_name",
        "distance_from_centroid"
    ]
].rename(
    columns={
        "id": "company_id",
        "cluster": "cluster_id"
    }
).to_csv(
    os.path.join(
        OUTPUT_DIR,
        "cluster_labels.csv"
    ),
    index=False
)
print("\nCompany Clusters Generated Successfully!\n")

print(
    cluster_df[
        [
            "id",
            "company_name",
            "cluster_name"
        ]
    ].head(20)
)


# -----------------------------
# Cluster Distribution Plot
# -----------------------------

plt.figure(figsize=(7,5))

cluster_df["cluster_name"].value_counts().plot(
    kind="bar"
)

plt.title("Company Cluster Distribution")
plt.xlabel("Cluster")
plt.ylabel("Number of Companies")

plt.tight_layout()

plt.savefig(
    os.path.join(
        REPORT_DIR,
        "cluster_distribution.png"
    )
)

plt.close()

print("\nCluster chart saved successfully.")


# -----------------------------
# Correlation Heatmap
# -----------------------------
plt.figure(figsize=(8,6))

sns.heatmap(
    cluster_df[features].corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Correlation Heatmap")

plt.tight_layout()

plt.savefig(
    os.path.join(
        REPORT_DIR,
        "correlation_heatmap.png"
    )
)

plt.close()

# -----------------------------
# Outlier Report
# -----------------------------
outliers = []

for sector, grp in cluster_df.groupby("broad_sector"):

    temp = grp.copy()

    for col in features:

        std = temp[col].std()

        if std == 0 or pd.isna(std):
            continue

        z = (temp[col] - temp[col].mean()) / std

        flagged = temp[abs(z) > 3]

        for _, row in flagged.iterrows():

            outliers.append({
                "company_id": row["id"],
                "company_name": row["company_name"],
                "sector": sector,
                "metric": col,
                "z_score": round(float(z.loc[row.name]),2)
            })

pd.DataFrame(outliers).to_csv(
    os.path.join(
        OUTPUT_DIR,
        "outlier_report.csv"
    ),
    index=False
)

# -----------------------------
# Portfolio Statistics
# -----------------------------
stats = []

for col in features:

    s = cluster_df[col]

    stats.append({
        "Metric": col,
        "P10": s.quantile(0.10),
        "P25": s.quantile(0.25),
        "P50": s.quantile(0.50),
        "P75": s.quantile(0.75),
        "P90": s.quantile(0.90),
        "Mean": s.mean(),
        "Std": s.std()
    })

pd.DataFrame(stats).round(2).to_csv(
    os.path.join(
        OUTPUT_DIR,
        "portfolio_stats.csv"
    ),
    index=False
)