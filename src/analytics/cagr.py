def calculate_cagr(start_value, end_value, years, available_years=None):


    if years <= 0:
        return None, "INVALID_YEARS"


    if available_years is not None:

        if available_years < years:
            return None, "INSUFFICIENT"



    if start_value == 0:
        return None, "ZERO_BASE"



    # Positive to Positive
    if start_value > 0 and end_value > 0:

        cagr = (
            (end_value / start_value) ** (1 / years) - 1
        ) * 100

        return cagr, None



    # Positive to Negative
    if start_value > 0 and end_value < 0:

        return None, "DECLINE_TO_LOSS"



    # Negative to Positive
    if start_value < 0 and end_value > 0:

        return None, "TURNAROUND"



    # Negative to Negative
    if start_value < 0 and end_value < 0:

        return None, "BOTH_NEGATIVE"



    return None, "UNKNOWN"