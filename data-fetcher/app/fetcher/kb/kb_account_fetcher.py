import re

import requests
import bs4

from ..account_fetcher import AccountFetcher
from ...models import Account, Currency
from ...utils import get_fully_qualified_acc_num


class KBAccountFetcher(AccountFetcher):

    URL = 'https://www.kb.cz/cs/transparentni-ucty?page={}'
    API_BALANCE_URL = 'https://www.kb.cz/transparentsapi/balance/{}'

    def fetch(self) -> list:
        # Prepare session
        s = requests.Session()
        # First request to get the number of pages
        response = s.get(self.URL.format(1))
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        last_page = int(soup.find(class_='pagination__page-number').string)

        # Scrape page by page and add accounts to the result list
        accounts = []
        for page in range(1, last_page + 1):
            accounts += self.scrape_page(page, s)

        return accounts

    def scrape_page(self, page: int, s: requests.Session) -> list:
        # Get list of divs containing account info
        response = s.get(self.URL.format(page))
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        divs = soup.find_all(class_='d-md-flex w-100')

        # Scrape div by div and add accounts to the result list
        accounts = []
        for div in divs:
            accounts.append(self.scrape_account(div))

        return accounts

    def scrape_account(self, div: bs4.element.Tag) -> Account:
        # Scrape the basic account info
        # It's important to strip whitespaces and to remove all newlines
        name = div.find('h2').get_text(strip=True)
        details = div.find(class_='serp-text').get_text(strip=True).replace('\n', '')
        # Parse the account info using regex
        pattern = r'majitel: (.*), měna: (.*), číslo účtu: (\d{0,6}-?\d{2,10})'
        search = re.search(pattern, details)
        owner, currency, number = search.groups()
        # Get fully qualified account number
        number = get_fully_qualified_acc_num(number)

        return Account(number=number,
                       bank_code='0100',
                       name=name,
                       owner=owner,
                       currency=Currency.from_str(currency))
