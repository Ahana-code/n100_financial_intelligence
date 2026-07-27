from fastapi import APIRouter, HTTPException
from .database import *

router = APIRouter()


@router.get("/")
def home():
    return {"message": "N100 Financial Intelligence API"}


@router.get("/companies")
def companies():
    return fetch_companies().to_dict(orient="records")


@router.get("/company/{company_id}")
def company(company_id: str):
    df = fetch_company(company_id.upper())
    if df.empty:
        raise HTTPException(status_code=404, detail="Company not found")
    return df.to_dict(orient="records")


@router.get("/ratios/{company_id}")
def ratios(company_id: str):
    return fetch_ratios(company_id.upper()).to_dict(orient="records")


@router.get("/profit/{company_id}")
def profit(company_id: str):
    return fetch_profit(company_id.upper()).to_dict(orient="records")


@router.get("/balance/{company_id}")
def balance(company_id: str):
    return fetch_balance(company_id.upper()).to_dict(orient="records")


@router.get("/cashflow/{company_id}")
def cashflow(company_id: str):
    return fetch_cashflow(company_id.upper()).to_dict(orient="records")


@router.get("/analysis/{company_id}")
def analysis(company_id: str):
    return fetch_analysis(company_id.upper()).to_dict(orient="records")


@router.get("/pros/{company_id}")
def pros(company_id: str):
    return fetch_pros(company_id.upper()).to_dict(orient="records")


@router.get("/sector/{company_id}")
def sector(company_id: str):
    return fetch_sector(company_id.upper()).to_dict(orient="records")


@router.get("/peers/{company_id}")
def peers(company_id: str):
    return fetch_peer_group(company_id.upper()).to_dict(orient="records")


@router.get("/marketcap/{company_id}")
def marketcap(company_id: str):
    return fetch_market_cap(company_id.upper()).to_dict(orient="records")


@router.get("/prices/{company_id}")
def prices(company_id: str):
    return fetch_stock_prices(company_id.upper()).to_dict(orient="records")


@router.get("/documents/{company_id}")
def documents(company_id: str):
    return fetch_documents(company_id.upper()).to_dict(orient="records")


@router.get("/health")
def health():
    return {"status": "healthy"}


@router.get("/version")
def version():
    return {
        "version": "1.0",
        "sprint": 6
    }