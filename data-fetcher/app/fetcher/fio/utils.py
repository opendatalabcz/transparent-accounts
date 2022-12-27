def get_html_formatted_acc_num(acc_num: str) -> str:
    """
    Returns Fio html pages formatted account number.
    Account number format required by the Fio html pages is such that:
    It does not contain the prefix.
    It does not contain a dash.
    It contains or does not contain leading zeros in the account number itself.
    :param acc_num: account number in the fully qualified format
    :return: account number in the format required by the Fio html pages
    """
    _, number = acc_num.split('-')
    return number
