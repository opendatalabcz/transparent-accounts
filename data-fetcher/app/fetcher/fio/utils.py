def get_fio_formatted_acc_num(acc_num: str) -> str:
    """
    Return Fio formatted account number.
    Account number format required by Fio is one that:
    It does not contain the prefix (to 17-02-2023 there is no Fio account with a prefix so the behaviour is unknown).
    It does not contain a dash.
    It contains or does not contain leading zeros in the account number itself.
    :param acc_num: account number in the fully qualified format
    :return: account number in the format required by Fio
    """
    _, number = acc_num.split('-')
    return number
