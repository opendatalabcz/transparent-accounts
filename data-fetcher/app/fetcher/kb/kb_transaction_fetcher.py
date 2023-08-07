import re
from datetime import datetime, date
from typing import Optional

import requests
import bs4

from app.fetcher.kb.utils import get_kb_formatted_acc_num
from app.fetcher.transaction_fetcher import TransactionFetcher
from app.models import Transaction, TransactionType, TransactionTypeDetail
from app.utils import float_from_cz


class KBTransactionFetcher(TransactionFetcher):

    URL = 'https://www.kb.cz/cs/transparentni-ucty/{}'
    API_URL = 'https://www.kb.cz/api/transparentaccount/detail'

    def fetch(self) -> list[Transaction]:
        # Prepare session (for mandatory cookies)
        s = requests.Session()
        # Get verification token from the html page
        response_text = s.get(self.URL.format(get_kb_formatted_acc_num(self.account.number, False))).text
        verification_token = re.search(r'\"requestVerificationToken\":\s\"(.*)\"', response_text).group(1)
        s.headers.update({'__RequestVerificationToken': verification_token})
        # Scrape and set account info
        self.scrape_account_info(response_text)
        # Prepare body
        body = {
            'query': get_kb_formatted_acc_num(self.account.number, True),
            'limit': 1,
            'offset': 0,
            'cultureCode': 'cs-CZ',
            'maxVisibleDays': (date.today() - self.get_date_from()).days + 1
        }
        # First request to get the number of records
        response_data = s.post(self.API_URL, json=body).json()
        # Set the limit to the number of records
        pagination = response_data['payload']['pagination']
        # No transactions to fetch
        if pagination is None:
            return []
        body['limit'] = pagination['rowsCount']
        # Second request to get all records
        response_data = s.post(self.API_URL, json=body).json()

        return [self.transaction_to_class(t) for t in response_data['payload']['data']]

    def scrape_account_info(self, text: str) -> None:
        # Set balance
        balance = re.search(r'\"balance\":\s+{\s+\"amount\":\s+\"(-?[\d\s]+,[\d\s]+) ([A-Z]{3})\"', text).group(1)
        self.account.balance = float_from_cz(balance)
        # Set description
        soup = bs4.BeautifulSoup(text, 'html.parser')
        self.account.description = soup.select_one('div.mb-4.text-base.text-grey-200').get_text(strip=True)

    def transaction_to_class(self, t: dict) -> Transaction:
        amount, currency = self.parse_money_amount(t['amount']['value'])
        counter_account, type_str, description = self.parse_details(t)
        variable_symbol, constant_symbol, specific_symbol = self.parse_symbols(t['info']['additionalInfo'])
        # Parse the counter account identifier and name
        ca_identifier = self.parse_identifier(description)
        ca_name = self.fetch_identifier_name(ca_identifier) if ca_identifier else None

        transaction = Transaction(
            date=self.parse_date(t),
            amount=amount,
            currency=currency,
            counter_account=counter_account,
            type=TransactionType.from_float(amount),
            type_str=type_str,
            variable_symbol=variable_symbol,
            constant_symbol=constant_symbol,
            specific_symbol=specific_symbol,
            description=description,
            ca_identifier=ca_identifier,
            ca_name=ca_name,
            account_number=self.account.number,
            account_bank=self.account.bank
        )
        transaction.type_detail = self.determine_detail_type(transaction)
        transaction.category = self.determine_category(transaction)
        return transaction

    @staticmethod
    def parse_date(t: dict) -> date:
        day, month = re.search(r'([0-9]{1,2})\. ([0-9]{1,2})\.', t['date']).groups()
        year = t['year'] if t['year'] != '' else datetime.now().year
        return date(int(year), int(month), int(day))

    @staticmethod
    def parse_money_amount(string: str) -> tuple[float, str]:
        """
        Parse amount and currency from the KB API transaction amount.
        Example of KB API transaction amount: '-19 057,50 CZK'.
        """
        # Parse the amount and currency using regex
        pattern = r'(-?[\d\s]+,[\d\s]+) ([A-Z]{3})'
        search = re.search(pattern, string)
        amount, currency = search.groups()
        return float_from_cz(amount), currency

    @staticmethod
    def parse_symbols(string: str) -> tuple[str, str, str]:
        # Parse the symbols using regex
        pattern = r'VS: ([0-9]{1,10})'
        variable_symbol = re.search(pattern, string).group(1) if re.search(pattern, string) else ''
        pattern = r'KS: ([0-9]{1,10})'
        constant_symbol = re.search(pattern, string).group(1) if re.search(pattern, string) else ''
        pattern = r'SS: ([0-9]{1,10})'
        specific_symbol = re.search(pattern, string).group(1) if re.search(pattern, string) else ''
        return variable_symbol, constant_symbol, specific_symbol

    @staticmethod
    def parse_details(t: dict) -> tuple[Optional[str], str, str]:
        # Outgoing transaction, no info about the counter account
        if t['amount']['type'] == 'expense':
            return None, t['info']['title'], t['info']['transparentAccountInfo']
        # Incoming transaction
        if '<br />' in t['info']['title']:
            counter_account, type_str = re.search(r'(.*)<br />(.*)', t['info']['title']).groups()
        else:
            counter_account, type_str = None, t['info']['title']
        return counter_account, type_str, t['info']['transparentAccountInfo']

    @staticmethod
    def determine_detail_type(transaction: Transaction) -> Optional[TransactionTypeDetail]:
        """
        Determine the detail type of the transaction.
        :param transaction: Transaction to determine the detail type for
        :return: detail type if determined, None otherwise
        """
        # Fee
        if transaction.type == TransactionType.OUTGOING and transaction.type_str == 'Poplatek':
            return TransactionTypeDetail.FEE
        # Try default detail type determination
        return TransactionFetcher.determine_detail_type(transaction)
