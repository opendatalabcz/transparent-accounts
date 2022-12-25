def get_api_formatted_acc_num(acc_num: str) -> str:
    """
    Returns KB API formatted account number.
    Account number format required by the KB API is such that it does not contain leading zeros in the prefix,
    does not contain a dash and the account number has 10 digits.
    :param acc_num: account number in the fully qualified format
    :return: account number in the format required by KB API
    """
    # Remove zeros from the prefix
    acc_num = acc_num.lstrip('0')
    # Remove the dash
    return acc_num.replace('-', '')
