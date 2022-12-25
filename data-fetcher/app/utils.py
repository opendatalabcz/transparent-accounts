def get_fully_qualified_acc_num(acc_num: str) -> str:
    """
    Returns fully qualified account number.
    A fully qualified account number is one that contains a six-digit prefix, a dash and a ten-digit account number.
    :param acc_num: account number in short format
    :return: fully qualified account number
    """
    # Split the account into a prefix and a number
    tokens = acc_num.split('-')
    if len(tokens) == 1:
        prefix = ''
        number = tokens[0]
    elif len(tokens) == 2:
        prefix = tokens[0]
        number = tokens[1]
    else:
        raise ValueError(acc_num)

    # Pad zeros so that prefix has 6 digits and number has 10 digits
    prefix = prefix.zfill(6)
    number = number.zfill(10)

    return f"{prefix}-{number}"
