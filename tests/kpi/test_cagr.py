from src.analytics.cagr import calculate_cagr


def test_insufficient_data():

    value, flag = calculate_cagr(
        100,
        200,
        5,
        available_years=3
    )

    assert flag == "INSUFFICIENT"


def test_normal_cagr():

    value, flag = calculate_cagr(
        100,
        200,
        5
    )

    assert flag == None
    assert round(value,2) == 14.87



def test_zero_base():

    value, flag = calculate_cagr(
        0,
        100,
        5
    )

    assert flag == "ZERO_BASE"



def test_turnaround():

    value, flag = calculate_cagr(
        -100,
        200,
        5
    )

    assert flag == "TURNAROUND"



def test_decline_loss():

    value, flag = calculate_cagr(
        100,
        -50,
        5
    )

    assert flag == "DECLINE_TO_LOSS"



def test_both_negative():

    value, flag = calculate_cagr(
        -100,
        -200,
        5
    )

    assert flag == "BOTH_NEGATIVE"

