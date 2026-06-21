# N100 Financial Intelligence Platform

A financial analytics platform built for Nifty 100 companies. The project focuses on building a reliable ETL pipeline, structured financial database, and data quality validation system for downstream analytics.

## Project Overview

The platform ingests multiple financial datasets, cleans and normalizes the data, stores it in SQLite, and validates data quality using automated checks.

## Sprint 1 - Data Foundation

Completed:

- Excel data ingestion pipeline
- Data cleaning and normalization
- SQLite database creation
- Data quality validation
- Load audit generation
- ETL testing


## ETL Architecture
Raw Excel Files
|
↓
Loader Pipeline
|
↓
Cleaning & Normalization
|
↓
SQLite Database
|
↓
Validation Checks
|
↓
Audit Reports
## Datasets Used12 source datasets:- Companies- Profit and Loss- Balance Sheet- Cash Flow- Analysis- Financial Ratios- Stock Prices- Documents- Pros and Cons- Sectors- Peer Groups- Market Capital## Database TablesThe SQLite database contains:- companies- profitandloss- balancesheet- cashflow- analysis- financial_ratios- stock_prices- documents- prosandcons- sectors- peer_groups- market_cap## Data Quality ChecksImplemented validations:- Primary key uniqueness- Company-year uniqueness- Foreign key integrity- Company reference validation- Dataset row count validation## Project Structure
n100_financial_intelligence
├── data/raw
├── db
├── output
├── src/etl
├── tests/etl
└── README.md
## How to RunInstall dependencies:
pip install pandas openpyxl pytest
Run ETL:
python src/etl/loader.py
Run validation:
python src/etl/validator.py
Run tests:
python -m pytest
## Current StatusSprint 1 completed successfully.ETL pipeline loads and validates financial datasets with automated testing.
