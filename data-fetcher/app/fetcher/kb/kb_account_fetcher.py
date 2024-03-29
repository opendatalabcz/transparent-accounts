import re

import bs4
import requests

from app.fetcher.account_fetcher import AccountFetcher
from app.models import Account, Bank
from app.utils import get_fully_qualified_acc_num


class KBAccountFetcher(AccountFetcher):

    URL = 'https://www.kb.cz/cs/transparentni-ucty'
    API_URL = 'https://www.kb.cz/api/transparentaccount/list'

    def fetch(self) -> list[Account]:
        # Prepare session (for mandatory cookies)
        s = requests.Session()
        # Get verification token from the html page
        response_text = s.get(self.URL).text
        soup = bs4.BeautifulSoup(response_text, 'html.parser')
        verification_token = soup.select_one('input[name="__RequestVerificationToken"]')['value']
        s.headers.update({'__RequestVerificationToken': verification_token})
        # Prepare body
        body = {
            'query': '',
            'limit': 1,
            'offset': 0,
            'cultureCode': 'cs-CZ',
            'baseUrl': '/cs/transparentni-ucty'
        }
        # First request to get the number of records
        response_data = s.post(self.API_URL, json=body).json()
        # Set the limit to the number of records
        body['limit'] = response_data['payload']['pagination']['rowsCount']
        # Second request to get all records
        response_data = s.post(self.API_URL, json=body).json()

        return list(map(self.account_to_class, response_data['payload']['data']))

    @staticmethod
    def account_to_class(acc: dict) -> Account:
        owner, number, currency = KBAccountFetcher.parse_details(acc.get('perex'))
        return Account(number=get_fully_qualified_acc_num(number),
                       bank=Bank.KB,
                       name=acc.get('title'),
                       owner=owner,
                       currency=currency)

    @staticmethod
    def parse_details(string: str) -> tuple[str, str, str]:
        pattern = r'majitel účtu: (.*),.*číslo účtu: (.*)\/0100,.*měna: (.{3})'
        owner, number, currency = re.search(pattern, string, re.DOTALL).groups()
        return owner, number, currency
