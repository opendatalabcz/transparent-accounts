import re
from typing import Optional

import bs4
import requests

from app.fetcher.account_fetcher import AccountFetcher
from app.models import Account, Bank
from app.utils import get_fully_qualified_acc_num


class FioAccountFetcher(AccountFetcher):

    URL = 'https://www.fio.cz/bankovni-sluzby/bankovni-ucty/transparentni-ucet/vypis-transparentnich-uctu?offset={}'
    OFFSET_STEP = 30

    def fetch(self) -> list[Account]:
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
        """
        Scrape the offset number of the last page.
        Should be determined by class 'paginator' and being the last 'a' tag in there.
        """
        response_text = s.get(self.URL.format(0)).text
        soup = bs4.BeautifulSoup(response_text, 'html.parser')
        last_page_url = soup.select_one('.paginator a:last-child')['href']
        # Parse the last page offset using regex
        pattern = r'\/bankovni-sluzby\/bankovni-ucty\/transparentni-ucet\/vypis-transparentnich-uctu\?offset=([0-9]+)'
        search = re.search(pattern, last_page_url)
        # Convert the last page offset to int
        return int(search.group(1))

    def scrape_page(self, offset: int, s: requests.Session) -> list[Account]:
        """
        Scrape table row by table row and map them to the Account class, then return them in the list.
        """
        # Get list of table rows containing account info
        response_text = s.get(self.URL.format(offset)).text
        soup = bs4.BeautifulSoup(response_text, 'html.parser')
        # Table with accounts is determined by classes 'tbl2' and 'tbl-sazby'
        rows = soup.select('.tbl2.tbl-sazby tbody tr')

        # Scrape row by row
        accounts = []
        for row in rows:
            account = self.scrape_account(row)
            if account is not None:
                accounts.append(account)

        return accounts

    def scrape_account(self, tr: bs4.element.Tag) -> Optional[Account]:
        """
        Scrape an Account and map it into Account instance.
        """
        # Get td tags, first contains owner and second contains number
        owner_td, number_td, *_ = tr.children
        # Owner tag may contain owner's url
        owner_url = owner_td.get('href')
        # Extract text from tags
        owner = owner_td.get_text(strip=True)
        number = number_td.get_text(strip=True)
        # No account number is specified -> skip
        if not number:
            return None

        return Account(number=get_fully_qualified_acc_num(number),
                       bank=Bank.FIO,
                       owner=owner,
                       description=owner_url)
