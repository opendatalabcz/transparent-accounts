import re


def float_from_cz(num: str) -> float:
    """
    Convert czech localized format of number to float.
    Replace the comma with a dot and remove spaces.
    :param num: number in the czech localized format
    :return: converted str to float
    """
    return float(num.replace(',', '.').replace(' ', '').replace(' ', ''))


def get_fully_qualified_acc_num(acc_num: str) -> str:
    """
    Check the validity of the account number and return it in a fully qualified format.
    Fully qualified account number is one that:
    It contains a six-digit prefix.
    It contains a dash.
    It contains a ten-digit account number.
    :param acc_num: account number in any valid format
    :return: fully qualified account number
    :raises ValueError: on unrecognized account number input
    """
    # Check if the input is a valid account number
    pattern = r'([0-9]{1,6}-)?[0-9]{1,10}'
    if not re.fullmatch(pattern, acc_num):
        raise ValueError(f"Unrecognized account number format: {acc_num}")

    # Split the account into a prefix and a number
    prefix = number = ''
    tokens = acc_num.split('-')
    if len(tokens) == 1:
        number = tokens[0]
    elif len(tokens) == 2:
        prefix = tokens[0]
        number = tokens[1]

    # Pad zeros so that prefix has 6 digits and number has 10 digits
    prefix = prefix.zfill(6)
    number = number.zfill(10)

    return f"{prefix}-{number}"
