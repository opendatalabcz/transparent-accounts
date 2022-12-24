from datetime import datetime

import requests

from ...models import Transaction
from ..transaction_fetcher import TransactionFetcher


class CSASTransactionFetcher(TransactionFetcher):

    API_URL = 'https://api.csas.cz/webapi/api/v3/transparentAccounts/{}/transactions?dateFrom={}&dateTo={}'
    API_KEY = 'efbeb527-a609-4909-a1b9-1565d89d36dc'

    def fetch(self) -> map:
        # Get the interval at which transactions should be fetched
        date_from = self.get_date_from()
        date_to = self.get_date_to()

        # Fill the account number and the date interval into the url
        url = self.API_URL.format(self.account.number, date_from, date_to)
        # Prepare session with fixed API key
        s = requests.Session()
        s.headers.update({'Web-Api-Key': self.API_KEY})

        # First request to get the number of records
        response = s.get(url).json()
        record_count = response.get('recordCount', 0)

        # Second request to get all records
        url = f"{url}&size={record_count}"
        response = s.get(url).json()

        return map(self.transaction_to_class, response.get('transactions', []))

    def transaction_to_class(self, t: dict) -> Transaction:
        return Transaction(
            date=datetime.strptime(t.get('processingDate'), '%Y-%m-%dT00:00:00').date(),
            amount=t.get('amount').get('value'),
            counter_account=t.get('sender').get('name'),
            type=t.get('typeDescription'),
            variable_symbol=t.get('sender').get('variableSymbol', ''),
            constant_symbol=t.get('sender').get('constantSymbol', ''),
            specific_symbol=t.get('sender').get('specificSymbol', ''),
            description=t.get('sender').get('description', ''),
            account_id=self.account.number
        )
