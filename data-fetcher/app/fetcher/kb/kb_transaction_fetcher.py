import hashlib
import re
from datetime import datetime, date
from typing import Optional

import requests

from app.fetcher.kb.utils import get_kb_formatted_acc_num
from app.fetcher.transaction_fetcher import TransactionFetcher
from app.models import Account, Transaction, TransactionType, TransactionCategory
from app.utils import float_from_cz


class KBTransactionFetcher(TransactionFetcher):

    URL = 'https://www.kb.cz/cs/transparentni-ucty/{}'
    API_URL = 'https://www.kb.cz/transparentsapi/transactions/{}?skip={}&token={}'
    API_BALANCE_URL = 'https://www.kb.cz/transparentsapi/balance/{}'
    SALT = 'ab5ac41b-4d25-4c49-a97b-a160d0b41204'
    RECORDS_PER_REQUEST = 50

    def __init__(self, account: Account):
        super().__init__(account)
        # Modify the account number so that it can be used in KB API
        self.acc_num = get_kb_formatted_acc_num(self.account.number, True)
        # It is crucial to use session here because of the required session cookies
        self.s = requests.Session()

    def fetch(self) -> list[Transaction]:
        # Set account balance
        self.account.balance = self.fetch_balance()
        # Get initial pure token and set session cookies by accessing the html page
        pure_token = self.get_token_and_set_cookies()
        # Get transactions
        fetched = self.fetch_transactions(pure_token)
        # Close the session
        self.s.close()

        transactions = map(self.transaction_to_class, fetched)

        # Filter out transactions that does not belong to the desired interval
        return list(filter(self.check_date_interval, transactions))

    def get_token_and_set_cookies(self) -> str:
        # First request to get the initial pure token and session cookies
        url = self.URL.format(get_kb_formatted_acc_num(self.account.number, False))
        response = self.s.get(url)
        # Parse the initial pure token using regex
        pattern = r"token: '(.*)'"
        search = re.search(pattern, response.text)
        return search.group(1)

    def fetch_balance(self) -> float:
        url = self.API_BALANCE_URL.format(self.acc_num)
        response = requests.get(url).json()
        balance, _ = self.parse_money_amount(response['balance'])
        return balance

    def fetch_transactions(self, pure_token) -> list:
        """
        Return a list of transactions in a dictionary format.
        Fetch KB API as long as there are records or until we encounter transactions older than we are interested in.
        """
        result = []
        skip = 0

        while True:
            # The resulting token is a sha256 of the static salt and the pure token
            token = hashlib.sha256((self.SALT + pure_token).encode('utf-8')).hexdigest()
            url = self.API_URL.format(self.acc_num, skip, token)
            response_data = self.s.get(url).json()
            # Add response to the result list
            result += response_data['items']
            # No more records to fetch - either the KB API announced the end of records
            # or we have encountered a transaction that is older than we are interested in
            if not response_data['loadMore'] or self.parse_date(result[-1]['date']) < self.get_date_from():
                return result
            # Pure token for the next request
            pure_token = response_data['token']
            skip += self.RECORDS_PER_REQUEST

    def transaction_to_class(self, t: dict) -> Transaction:
        t_date = self.parse_date(t['date'])
        amount, currency = self.parse_money_amount(t['amount'])
        t_type = TransactionType.from_float(amount)
        # Split symbols by slashes and remove whitespaces from them
        variable_s, constant_s, specific_s = map(lambda s: s.replace(' ', ''),  t['symbols'].split('/'))
        counter_account, str_type, description = self.parse_details(t['notes'], t_type)
        # Parse the counter account identifier and name
        ca_identifier = self.parse_identifier(description)
        ca_name = self.fetch_identifier_name(ca_identifier) if ca_identifier else None

        transaction = Transaction(
            date=t_date,
            amount=amount,
            currency=currency,
            counter_account=counter_account,
            type=t_type,
            str_type=str_type,
            variable_symbol=variable_s,
            constant_symbol=constant_s,
            specific_symbol=specific_s,
            description=description,
            ca_identifier=ca_identifier,
            ca_name=ca_name,
            account_number=self.account.number,
            account_bank=self.account.bank,
        )
        transaction.category = self.determine_category(transaction)
        return transaction

    @staticmethod
    def parse_money_amount(string: str) -> tuple[float, str]:
        """
        Parse amount and currency from the KB API transaction amount.
        Example of KB API transaction amount: '4 186,33 EUR'.
        """
        # Parse the amount and currency using regex
        pattern = r'(-?[\d ]+,[\d ]+) ([A-Z]{3})'
        search = re.search(pattern, string)
        amount, currency = search.groups()
        return float_from_cz(amount), currency

    @staticmethod
    def parse_date(string: str) -> date:
        """
        Parse date from the KB API to the date object.
        Example of KB API date: '01.&nbsp;01.&nbsp;2022'.
        """
        return datetime.strptime(string, '%d.&nbsp;%m.&nbsp;%Y').date()

    @staticmethod
    def parse_details(string: str, t_type: TransactionType) -> tuple[str | None, str, str]:
        """
        Parse counter_account, type and description from the KB API to the three separate variables.
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
                    # Special case - if the type is 'Vklad' then values are swapped
                    if str_type == 'Vklad':
                        counter_account, str_type = str_type, counter_account
                else:
                    str_type = parsed[0]
                    description = parsed[1]
            case 3:
                counter_account = parsed[0]
                str_type = parsed[1]
                description = parsed[2]
            case _:
                raise AttributeError(string)
        return counter_account, str_type, description

    @staticmethod
    def determine_category(transaction: Transaction) -> Optional[TransactionCategory]:
        """
        Determine the category of the transaction.
        :param transaction: Transaction to determine the category for
        :return: category if determined, None otherwise
        """
        # Fee
        if transaction.type == TransactionType.OUTGOING and transaction.str_type == 'Poplatek':
            return TransactionCategory.FEE
        # Try default category determination
        return TransactionFetcher.determine_category(transaction)
