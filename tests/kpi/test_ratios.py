from src.analytics.ratios import *


def test_net_profit_margin():

    assert net_profit_margin(100,1000) == 10



def test_zero_sales():

    assert net_profit_margin(100,0) == None



def test_roe_negative_equity():

    assert return_on_equity(
        100,
        -50,
        -20
    ) == None



def test_roa():

    assert return_on_assets(
        100,
        1000
    ) == 10

def test_opm_cross_check():

     result = check_opm_difference(
        20,
        22
    )


     assert result["mismatch"] == True

def test_debt_free_debt_equity():

    assert debt_to_equity(
        0,
        100,
        100
    ) == 0


def test_interest_zero():

    assert interest_coverage_ratio(
        100,
        20,
        0
    ) == None


def test_debt_free_label():

    assert interest_coverage_label(
        None
    ) == "Debt Free"


def test_high_leverage():

    assert high_leverage_flag(
        6,
        "IT"
    ) == True

def test_interest_warning():

    assert interest_warning_flag(
        1
    ) == True



def test_net_debt():

    assert net_debt(
        500,
        100
    ) == 400



def test_asset_turnover():

    assert asset_turnover(
        1000,
        500
    ) == 2