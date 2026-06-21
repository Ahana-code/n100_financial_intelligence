import sqlite3

conn = sqlite3.connect("db/nifty100.db")

cursor = conn.cursor()

cursor.execute("""
SELECT name 
FROM sqlite_master 
WHERE type='table';
""")

tables = cursor.fetchall()

print("Tables in database:")

for table in tables:
    print(table[0])


cursor.execute("""
SELECT COUNT(*) FROM companies;
""")

count = cursor.fetchone()

print("Companies count:", count[0])

conn.close()
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")


duplicates = pd.read_sql(
    """
    SELECT company_id, year, COUNT(*) as count
    FROM profitandloss
    GROUP BY company_id, year
    HAVING COUNT(*) > 1
    """,
    conn
)


print(duplicates)