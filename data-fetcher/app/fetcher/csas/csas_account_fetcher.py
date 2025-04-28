from dateutil import parser
import requests

from app.fetcher.account_fetcher import AccountFetcher
from app.models import Account, Bank


class CSASAccountFetcher(AccountFetcher):

    API_URL = 'https://api.csas.cz/webapi/api/v3/transparentAccounts'
    API_KEY = 'efbeb527-a609-4909-a1b9-1565d89d36dc'

    def fetch(self) -> list[Account]:
        # Prepare session with fixed API key
        s = requests.Session()
        s.headers.update({'Web-Api-Key': self.API_KEY})
        # First request to get the number of records
        response_data = s.get(self.API_URL).json()
        record_count = response_data['recordCount']
        # Second request to get all records
        url = f"{self.API_URL}/?size={record_count}"
        response_data = s.get(url).json()

        return list(map(self.account_to_class, response_data['accounts']))

    @staticmethod
    def account_to_class(acc: dict) -> Account:
        return Account(number=acc['accountNumber'],  # Account number from CSAS is already fully qualified
                       bank=Bank.CSAS,
                       name=acc.get('name'),
                       owner=acc.get('name'),
                       balance=acc.get('balance'),
                       currency=acc['currency'],
                       created=parser.parse(acc.get('transparencyFrom')).date())
