headers = {
    'Accept-Language': 'cs',
    # In fact only the Referer header is mandatory, the value is not checked
    'Referer': 'https://www.csob.cz/portal/firmy/bezne-ucty/transparentni-ucty',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0'
}


def get_csob_formatted_acc_num(acc_num: str) -> str:
    """
        Return CSOB formatted account number.
        Account number format required by CSOB is one that:
        It does not contain the prefix (to 02-08-2023 there is no CSOB account with a prefix so the behaviour is unknown).
        It does not contain a dash.
        It contains or does not contain leading zeros in the account number itself.
        :param acc_num: account number in the fully qualified format
        :return: account number in the format required by CSOB
        """
    _, number = acc_num.split('-')
    return number
