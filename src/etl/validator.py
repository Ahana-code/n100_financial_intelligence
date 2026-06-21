import sqlite3
import pandas as pd


conn = sqlite3.connect("db/nifty100.db")

failures = []


# DQ-01
duplicates = pd.read_sql("""
SELECT id, COUNT(*) as count
FROM companies
GROUP BY id
HAVING COUNT(*) > 1
""", conn)


if len(duplicates) > 0:
    failures.append(
        ["DQ-01","CRITICAL","Duplicate company IDs found"]
    )


# DQ-02
duplicates_year = pd.read_sql("""
SELECT company_id, year, COUNT(*) as count
FROM profitandloss
GROUP BY company_id, year
HAVING COUNT(*) > 1
""", conn)


if len(duplicates_year) > 0:
    failures.append(
        ["DQ-02","CRITICAL","Duplicate company-year records found"]
    )


# DQ-03
missing_company = pd.read_sql("""
SELECT *
FROM profitandloss
WHERE company_id NOT IN
(
SELECT id FROM companies
)
""", conn)


if len(missing_company) > 0:
    failures.append(
        ["DQ-03","CRITICAL","Invalid company reference"]
    )


df = pd.DataFrame(
    failures,
    columns=[
        "rule",
        "severity",
        "issue"
    ]
)


df.to_csv(
    "output/validation_failures.csv",
    index=False
)


print("Validation completed")
print(df)


conn.close()