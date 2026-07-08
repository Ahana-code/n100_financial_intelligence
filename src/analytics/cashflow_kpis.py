def free_cash_flow(
        operating_activity,
        investing_activity
):

    return operating_activity + investing_activity


def cfo_quality_score(
        cfo,
        pat
):

    if pat == 0:
        return None


    ratio = cfo / pat


    if ratio > 1:
        return "High Quality"

    elif ratio >= 0.5:
        return "Moderate"

    else:
        return "Accrual Risk"



def capex_intensity(
        investing_activity,
        sales
):

    if sales == 0:
        return None


    value = (
        abs(investing_activity)
        / sales
    ) * 100


    if value < 3:
        return "Asset Light"

    elif value <= 8:
        return "Moderate"

    else:
        return "Capital Intensive"



def fcf_conversion(
        free_cash_flow,
        operating_profit
):

    if operating_profit == 0:
        return None


    return (
        free_cash_flow
        / operating_profit
    ) * 100

def capital_allocation_pattern(
        cfo,
        cfi,
        cff,
        cfo_quality=None
):

    cfo_sign = "+" if cfo >= 0 else "-"
    cfi_sign = "+" if cfi >= 0 else "-"
    cff_sign = "+" if cff >= 0 else "-"

    pattern = (cfo_sign, cfi_sign, cff_sign)

    if pattern == ("+", "-", "-"):

        if cfo_quality == "High Quality":
            return "Shareholder Returns"

        return "Reinvestor"

    elif pattern == ("+", "+", "-"):
        return "Liquidating Assets"

    elif pattern == ("-", "+", "+"):
        return "Distress Signal"

    elif pattern == ("-", "-", "+"):
        return "Growth Funded by Debt"

    elif pattern == ("+", "+", "+"):
        return "Cash Accumulator"

    elif pattern == ("-", "-", "-"):
        return "Pre-Revenue"

    elif pattern == ("+", "-", "+"):
        return "Mixed"

    return "Unknown"