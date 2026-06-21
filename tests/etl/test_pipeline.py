import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"



def get_connection():

    return sqlite3.connect(DB_PATH)



def test_database_exists():

    assert DB_PATH.exists()



def test_tables_exist():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT name 
        FROM sqlite_master 
        WHERE type='table'
        """
    )


    tables = [
        row[0]
        for row in cursor.fetchall()
    ]


    expected_tables = [
        "companies",
        "profitandloss",
        "balancesheet",
        "cashflow",
        "analysis",
        "financial_ratios",
        "stock_prices",
        "documents",
        "prosandcons",
        "sectors",
        "peer_groups",
        "market_cap"
    ]


    for table in expected_tables:

        assert table in tables


    conn.close()



def test_company_count():

    conn = get_connection()


    cursor = conn.cursor()


    cursor.execute(
        "SELECT COUNT(*) FROM companies"
    )


    count = cursor.fetchone()[0]


    assert count >= 92


    conn.close()