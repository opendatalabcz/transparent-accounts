import re

import bs4
import requests

from app.fetcher.account_fetcher import AccountFetcher
from app.models import Account
from app.utils import get_fully_qualified_acc_num


class FioAccountFetcher(AccountFetcher):

    URL = 'https://www.fio.cz/bankovni-sluzby/bankovni-ucty/transparentni-ucet/vypis-transparentnich-uctu?offset={}'
    OFFSET_STEP = 30

    def fetch(self) -> list:
        # Prepare session
        s = requests.Session()
        # First request to get the last offset
        last_offset = self.get_last_offset(s)
        # Scrape page by page and add accounts to the result list
        accounts = []
        for offset in range(0, last_offset + 1, self.OFFSET_STEP):
            accounts += self.scrape_page(offset, s)

        return accounts

    def get_last_offset(self, s: requests.Session) -> int:
        response_text = s.get(self.URL.format(0)).text
        soup = bs4.BeautifulSoup(response_text, 'html.parser')
        last_page_url = soup.select_one('.paginator a:last-child').get('href')
        # Parse the last offset using regex
        pattern = r'\/bankovni-sluzby\/bankovni-ucty\/transparentni-ucet\/vypis-transparentnich-uctu\?offset=(\d+)'
        search = re.search(pattern, last_page_url)
        last_offset = int(search.group(1))
        return last_offset

    def scrape_page(self, offset: int, s: requests.Session) -> list:
        # Get list of divs containing account info
        response_text = s.get(self.URL.format(offset)).text
        soup = bs4.BeautifulSoup(response_text, 'html.parser')
        rows = soup.select('.tbl2.tbl-sazby tbody tr')

        # Scrape row by row and add accounts to the result list
        accounts = []
        for row in rows:
            account = self.scrape_account(row)
            if account is not None:
                accounts.append(account)

        return accounts

    def scrape_account(self, tr: bs4.element.Tag) -> Account | None:
        # Get td tags, first contains owner and second contains number
        owner_td, number_td, *_ = tr.children
        # Owner tag may contain his url
        owner_url = owner_td.get('href')
        # Extract text from tags
        owner = owner_td.string
        number = number_td.string
        # TODO TEMPORARY
        if number is None:
            return None
        # Get fully qualified account number
        number = get_fully_qualified_acc_num(number)

        return Account(number=number,
                       bank_code='2010',
                       owner=owner,
                       description=owner_url)
