import re

import bs4
import requests

from app.fetcher.account_fetcher import AccountFetcher
from app.models import Account, Bank
from app.utils import get_fully_qualified_acc_num


class KBAccountFetcher(AccountFetcher):

    URL = 'https://www.kb.cz/cs/transparentni-ucty?page={}'

    def fetch(self) -> list[Account]:
        # Prepare session
        s = requests.Session()
        # First request to get the last page
        last_page = self.get_last_page(s)
        # Scrape page by page and add accounts to the result list
        accounts = []
        for page in range(1, last_page + 1):
            accounts += self.scrape_page(page, s)

        return accounts

    def get_last_page(self, s: requests.Session) -> int:
        """
        Scrapes the number of the last page.
        Should be determined by class 'pagination__page-number'.
        """
        response_text = s.get(self.URL.format(1)).text
        soup = bs4.BeautifulSoup(response_text, 'html.parser')
        # Convert the last page number to int
        return int(soup.select_one('.pagination__page-number').string)

    def scrape_page(self, page: int, s: requests.Session) -> list[Account]:
        """
        Scrapes div by div and maps them to the Account class, and returns them in the list.
        """
        # Get list of divs containing account info
        response_text = s.get(self.URL.format(page)).text
        soup = bs4.BeautifulSoup(response_text, 'html.parser')
        # Div with account is determined by classes 'd-md-flex' and 'w-100'
        divs = soup.select('.d-md-flex.w-100')

        # Scrape div by div and map then to the Account class
        return [self.scrape_account(div) for div in divs]

    def scrape_account(self, div: bs4.element.Tag) -> Account:
        """
        Scrapes an Account and maps it into Account instance.
        """
        # Scrape the basic account info
        # It's important to strip whitespaces and to remove all newlines
        name = div.select_one('h2').get_text(strip=True)
        details = div.select_one('.serp-text').get_text(strip=True).replace('\n', '')
        # Parse the account info using regex
        pattern = r'majitel: (.*), měna: (.*), číslo účtu: ([0-9]{0,6}-?[0-9]{1,10})'
        search = re.search(pattern, details)
        owner, currency, number = search.groups()

        return Account(number=get_fully_qualified_acc_num(number),
                       bank=Bank.KB,
                       name=name,
                       owner=owner,
                       currency=currency)
