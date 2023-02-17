def get_kb_formatted_acc_num(acc_num: str, for_api: bool) -> str:
    """
    Return KB formatted account number.
    Account number format required by KB is one that:
    It does not contain leading zeros in the prefix.
    If it is for KB API then it does not contain a dash and the number itself has to be 10 digits long.
    For HTML pages, it contains a dash and the number itself is as short as possible (no leading zeros).
    :param acc_num: account number in the fully qualified format
    :param for_api: True - format for KB API, False - format for KB html pages
    :return: account number in the format required by KB
    """
    prefix, number = acc_num.split('-')
    prefix = prefix.lstrip('0')
    number = number if for_api else number.lstrip('0')

    if len(prefix) == 0:
        return number

    return f"{prefix}{number}" if for_api else f"{prefix}-{number}"
