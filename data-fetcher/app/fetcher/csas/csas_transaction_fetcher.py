from datetime import datetime
from typing import Optional

import requests

from app.fetcher.transaction_fetcher import TransactionFetcher
from app.models import Transaction, TransactionType, TransactionCategory


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

        return list(map(self.transaction_to_class, response_data.get('transactions', [])))

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
            currency=t['amount']['currency'],
            counter_account=counter_account,
            type=t_type,
            str_type=t['typeDescription'],
            variable_symbol=t['sender'].get('variableSymbol', ''),
            constant_symbol=t['sender'].get('constantSymbol', ''),
            specific_symbol=t['sender'].get('specificSymbol', ''),
            description=description,
            ca_identifier=ca_identifier,
            ca_name=ca_name,
            account_number=self.account.number,
            account_bank=self.account.bank
        )
        transaction.category = self.determine_category(transaction)
        return transaction

    @staticmethod
    def determine_category(transaction: Transaction) -> Optional[TransactionCategory]:
        """
        Determines the category of the transaction.
        :param transaction: Transaction to determine the category for
        :return: category if determined, None otherwise
        """
        # ATM withdrawals
        if transaction.type == TransactionType.OUTGOING and 'bankomat' in transaction.str_type:
            return TransactionCategory.ATM
        # Fee
        if transaction.type == TransactionType.OUTGOING and (transaction.str_type == 'Cena za vedení účtu' or transaction.str_type == 'Poskytnutí debetní karty'):
            return TransactionCategory.FEE
        # Tax
        if transaction.type == TransactionType.OUTGOING and 'daň' in transaction.str_type:
            return TransactionCategory.TAX
        # Card payments
        if transaction.type == TransactionType.OUTGOING and 'Platba kartou' == transaction.str_type:
            return TransactionCategory.CARD
        # Try default category determination
        return TransactionFetcher.determine_category(transaction)
