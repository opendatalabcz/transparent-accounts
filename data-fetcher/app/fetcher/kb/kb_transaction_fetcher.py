import re
import hashlib
from datetime import datetime, date

import requests

from ..transaction_fetcher import TransactionFetcher
from .utils import get_api_formatted_acc_num, get_html_formatted_acc_num
from ...models import Account, Transaction, TransactionType


class KBTransactionFetcher(TransactionFetcher):

    URL = 'https://www.kb.cz/cs/transparentni-ucty/{}'
    API_URL = 'https://www.kb.cz/transparentsapi/transactions/{}?skip={}&token={}'
    API_BALANCE_URL = 'https://www.kb.cz/transparentsapi/balance/{}'
    SALT = 'ab5ac41b-4d25-4c49-a97b-a160d0b41204'
    RECORDS_PER_REQUEST = 50

    def __init__(self, account: Account):
        super().__init__(account)
        # Modify the account number so that it can be used in KB API
        self.acc_num = get_api_formatted_acc_num(self.account.number)
        # It is crucial to use session here because of the required session cookies
        self.s = requests.Session()

    def fetch(self) -> list:
        # Set account balance
        self.account.balance = self.fetch_balance()
        # Get initial pure token and set session cookies by accessing the html page
        pure_token = self.get_token_and_set_cookies()
        # Get transactions
        fetched = self.fetch_transactions(pure_token)
        # Close the session
        self.s.close()

        transactions = map(self.transaction_to_class, fetched)

        return list(filter(self.check_date_interval, transactions))

    def get_token_and_set_cookies(self) -> str:
        # First request to get the initial pure token and session cookies
        url = self.URL.format(get_html_formatted_acc_num(self.account.number))
        response = self.s.get(url)
        # Parse the initial pure token using regex
        pattern = r"token: '(.*)'"
        search = re.search(pattern, response.text)
        return search.group(1)

    def fetch_balance(self) -> float:
        url = self.API_BALANCE_URL.format(self.acc_num)
        response = requests.get(url).json()
        return self.parse_money_amount(response.get('balance'))

    def fetch_transactions(self, pure_token) -> list:
        """
        Returns a list of transactions in a dictionary format.
        Fetches KB API as long as there are records or until it encounters transactions older than we are interested in.
        :param pure_token: initial pure token
        :return: list of transactions as dictionaries
        """
        result = []
        skip = 0

        while True:
            # The resulting token is a sha256 of the static salt and the pure token
            token = hashlib.sha256((self.SALT + pure_token).encode('utf-8')).hexdigest()
            url = self.API_URL.format(self.acc_num, skip, token)
            response = self.s.get(url).json()
            # Add response to the result list
            result += response.get('items')
            # No more records to fetch - either the KB API announced the end of records
            # or we have encountered a transaction that is older than we are interested in
            if not response.get('loadMore') or self.parse_date(result[-1].get('date')) < self.get_date_from():
                return result
            # Pure token for the next request
            pure_token = response.get('token')
            skip += self.RECORDS_PER_REQUEST

    def transaction_to_class(self, t: dict) -> Transaction:
        """
        :param t: transaction in a dictionary format
        :return: transaction as class
        """
        t_date = self.parse_date(t.get('date'))
        amount = self.parse_money_amount(t.get('amount'))
        t_type = TransactionType.from_float(amount)
        # Split symbols by slashes and remove whitespaces from them
        variable_s, constant_s, specific_s = map(lambda s: s.replace(' ', ''),  t.get('symbols').split('/'))
        counter_account, str_type, description = self.parse_details(t.get('notes'), t_type)

        return Transaction(
            date=t_date,
            amount=amount,
            counter_account=counter_account,
            type=t_type,
            str_type=str_type,
            variable_symbol=variable_s,
            constant_symbol=constant_s,
            specific_symbol=specific_s,
            description=description,
            account_number=self.account.number
        )

    @staticmethod
    def parse_money_amount(string: str) -> float:
        """
        Parses amount of money from the KB API to float.
        Example of KB API amount of money: '4 186,33 EUR'.
        :param string:
        :return:
        """
        # Parse the amount of money using regex
        pattern = r'(-?[\d ]+,[\d ]+).*'
        balance = re.search(pattern, string).group(1)
        # Replace a comma with a dot, remove fixed spaces and cast to float
        return float(balance.replace(',', '.').replace(' ', ''))

    @staticmethod
    def parse_date(string: str) -> date:
        """
        Parses date from the KB API to the date object.
        Example of KB API date: '01.&nbsp;01.&nbsp;2022'.
        :param string: date as a raw string
        :return: date as object
        """
        return datetime.strptime(string, '%d.&nbsp;%m.&nbsp;%Y').date()

    @staticmethod
    def parse_details(string: str, t_type: TransactionType) -> tuple[str | None, str, str]:
        """
        Parses counter_account, type and description from the KB API to the three separate variables.
        Example of KB API details string: 'A<br />B<br />C'.
        :param string: details
        :param t_type: type of transaction
        :return: counter_account, type and description
        :raises AttributeError: unsupported format of details string
        """
        parsed = string.split('<br />')
        counter_account = None
        description = ''
        match len(parsed):
            case 1:
                str_type = parsed[0]
            case 2:
                # In case of incoming transaction, the counter account is always shown,
                # while in case of outgoing transaction it is never shown
                if t_type == TransactionType.INCOMING:
                    counter_account = parsed[0]
                    str_type = parsed[1]
                else:
                    str_type = parsed[0]
                    description = parsed[1]
            case 3:
                counter_account = parsed[0]
                str_type = parsed[1]
                description = parsed[2]
            case _:
                raise AttributeError(str)
        return counter_account, str_type, description
