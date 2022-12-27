def get_api_formatted_acc_num(acc_num: str) -> str:
    """
    Returns KB API formatted account number.
    Account number format required by the KB API is such that:
    It does not contain leading zeros in the prefix.
    It does not contain a dash.
    It does not contain leading zeros in the account number itself.
    :param acc_num: account number in the fully qualified format
    :return: account number in the format required by the KB API
    """
    prefix, number = acc_num.split('-')
    prefix = prefix.lstrip('0')
    number = number.lstrip('0')

    return f"{prefix}{number}"


def get_html_formatted_acc_num(acc_num: str) -> str:
    """
    Returns KB html pages formatted account number.
    Account number format required by the KB html pages is such that:
    It does not contain leading zeros in the prefix.
    It contains a dash.
    It does not contain leading zeros in the account number itself.
    :param acc_num: account number in the fully qualified format
    :return: account number in the format required by the KB html pages
    """
    prefix, number = acc_num.split('-')
    prefix = prefix.lstrip('0')
    number = number.lstrip('0')

    if len(prefix) == 0:
        return number

    return f"{prefix}-{number}"
