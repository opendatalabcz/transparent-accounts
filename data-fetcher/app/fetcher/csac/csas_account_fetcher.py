from datetime import datetime

import requests

from ..account_fetcher import AccountFetcher
from ...models import Account, Currency


class CSASAccountFetcher(AccountFetcher):

    API_URL = 'https://api.csas.cz/webapi/api/v3/transparentAccounts'
    API_KEY = 'efbeb527-a609-4909-a1b9-1565d89d36dc'

    def fetch(self) -> map:
        # Prepare session with fixed API key
        s = requests.Session()
        s.headers.update({'Web-Api-Key': self.API_KEY})

        # First request to get the number of records
        response = s.get(self.API_URL).json()
        record_count = response['recordCount']

        # Second request to get all records
        url = f"{self.API_URL}/?size={record_count}"
        response = s.get(url).json()

        return map(self.account_to_class, response['accounts'])

    @staticmethod
    def account_to_class(acc: dict) -> Account:
        return Account(number=acc.get('accountNumber'),
                       bank_code=acc.get('bankCode'),
                       name=acc.get('name'),
                       owner=acc.get('name'),
                       balance=acc.get('balance', 0),
                       currency=Currency.from_str(acc.get('currency')),
                       created=datetime.strptime(acc.get('transparencyFrom'), '%Y-%m-%dT00:00:00').date())
