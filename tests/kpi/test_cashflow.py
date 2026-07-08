from src.analytics.cashflow_kpis import *


def test_free_cash_flow():

    assert free_cash_flow(
        500,
        -200
    ) == 300


def test_cfo_quality():

    assert cfo_quality_score(
        150,
        100
    ) == "High Quality"


def test_capex():

    assert capex_intensity(
        -20,
        1000
    ) == "Asset Light"


def test_fcf_conversion():

    assert fcf_conversion(
        300,
        600
    ) == 50


def test_capital_pattern():

    assert capital_allocation_pattern(
        100,
        -50,
        -30,
        "High Quality"
    ) == "Shareholder Returns"