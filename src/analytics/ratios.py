def net_profit_margin(net_profit, sales):

    if sales == 0:
        return None

    return (net_profit / sales) * 100



def operating_profit_margin(operating_profit, sales):

    if sales == 0:
        return None

    return (operating_profit / sales) * 100



def return_on_equity(net_profit, equity_capital, reserves):

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return (net_profit / equity) * 100



def return_on_capital_employed(
        ebit,
        equity_capital,
        reserves,
        borrowings
):

    capital = (
        equity_capital
        + reserves
        + borrowings
    )


    if capital <= 0:
        return None


    return (ebit / capital) * 100




def return_on_assets(net_profit, total_assets):

    if total_assets == 0:
        return None


    return (net_profit / total_assets) * 100

def check_opm_difference(
        calculated_opm,
        source_opm
):

    if calculated_opm is None or source_opm is None:
        return None


    difference = abs(
        calculated_opm - source_opm
    )


    if difference > 1:

        return {
            "mismatch": True,
            "difference": difference
        }


    return {
        "mismatch": False,
        "difference": difference
    }

def debt_to_equity(
        borrowings,
        equity_capital,
        reserves
):

    equity = equity_capital + reserves


    if borrowings == 0:
        return 0


    if equity <= 0:
        return None


    return borrowings / equity



def high_leverage_flag(
        debt_to_equity,
        sector
):

    if debt_to_equity is None:
        return False


    if (
        debt_to_equity > 5
        and sector != "Financials"
    ):
        return True


    return False



def interest_coverage_ratio(
        operating_profit,
        other_income,
        interest
):

    if interest == 0:
        return None


    return (
        operating_profit + other_income
    ) / interest



def interest_coverage_label(
        interest_coverage
):

    if interest_coverage is None:
        return "Debt Free"


    return None



def interest_warning_flag(
        interest_coverage
):

    if interest_coverage is None:
        return False


    return interest_coverage < 1.5



def net_debt(
        borrowings,
        investments
):

    return borrowings - investments



def asset_turnover(
        sales,
        total_assets
):

    if total_assets == 0:
        return None


    return sales / total_assets