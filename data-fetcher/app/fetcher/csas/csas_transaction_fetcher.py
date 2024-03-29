from datetime import datetime
from typing import Optional

import requests

from app.fetcher.transaction_fetcher import TransactionFetcher
from app.models import Transaction, TransactionType, TransactionTypeDetail


class CSASTransactionFetcher(TransactionFetcher):

    API_URL = 'https://api.csas.cz/webapi/api/v3/transparentAccounts/{}/transactions?dateFrom={}&dateTo={}'
    API_KEY = 'efbeb527-a609-4909-a1b9-1565d89d36dc'

    def fetch(self) -> list[Transaction]:
        # Fill the account number and the date interval into the url
        url = self.API_URL.format(self.account.number, self.get_date_from(), self.get_date_to())
        # Prepare session with fixed API key
        s = requests.Session()
        s.headers.update({'Web-Api-Key': self.API_KEY})
        # First request to get the number of records
        response_data = s.get(url).json()
        record_count = response_data['recordCount']
        # Second request to get all records
        url = f"{url}&size={record_count}"
        response_data = s.get(url).json()
        # Close the session
        s.close()

        return [self.transaction_to_class(transaction) for transaction in response_data.get('transactions', [])]

    def transaction_to_class(self, t: dict) -> Transaction:
        amount = t['amount']['value']
        counter_account = t['sender'].get('name') if t['sender'].get('name') != '-' else None
        t_type = TransactionType.from_float(amount)
        description = t['sender'].get('description', '')
        # Parse the counter account identifier and name
        ca_identifier = self.parse_identifier(description)
        ca_name = self.fetch_identifier_name(ca_identifier) if ca_identifier else None

        transaction = Transaction(
            date=datetime.strptime(t['processingDate'], '%Y-%m-%dT00:00:00').date(),
            amount=amount,
            currency=t['amount'].get('currency', self.account.currency),  # API may not return the currency
            counter_account=counter_account,
            type=t_type,
            type_str=t['typeDescription'],
            variable_symbol=t['sender'].get('variableSymbol', ''),
            constant_symbol=t['sender'].get('constantSymbol', ''),
            specific_symbol=t['sender'].get('specificSymbol', ''),
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
    def determine_detail_type(transaction: Transaction) -> TransactionTypeDetail:
        """
        Determine the detail type of the transaction.
        :param transaction: Transaction to determine the detail type for
        :return: detail type if determined, None otherwise
        """
        # ATM withdrawals
        if transaction.type == TransactionType.OUTGOING and 'bankomat' in transaction.type_str:
            return TransactionTypeDetail.ATM
        # Fee
        if transaction.type == TransactionType.OUTGOING and (transaction.type_str == 'Cena za vedení účtu' or transaction.type_str == 'Poskytnutí debetní karty'):
            return TransactionTypeDetail.FEE
        # Tax
        if transaction.type == TransactionType.OUTGOING and 'daň' in transaction.type_str:
            return TransactionTypeDetail.TAX
        # Card payments
        if transaction.type == TransactionType.OUTGOING and 'Platba kartou' == transaction.type_str:
            return TransactionTypeDetail.CARD
        # Try default detail type determination
        return TransactionFetcher.determine_detail_type(transaction)
